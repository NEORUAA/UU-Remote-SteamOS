#ifndef UURB_TERMINAL_MUX_RECOVERY_H
#define UURB_TERMINAL_MUX_RECOVERY_H

/* Only a successful fixed UU bootstrap can grant recovery ownership. A Windows
 * process ID is deliberately absent: Linux tmux owns the persistent shell. */
static BOOL mux_persistent(void)
{
    WCHAR mode[16];
    DWORD length = GetEnvironmentVariableW(L"UURB_TERMINAL_SESSION_MODE", mode, ARRAYSIZE(mode));
    if (length) return length == 10 && !wcscmp(mode, L"persistent");
    return mux_runtime_persistent();
}

/* Win32 accepts either separator for this same config file. UU's bootstrap
 * and its later CLI queries can spell the path differently. */
static WCHAR mux_config_char(WCHAR ch)
{
    return ch == L'/' ? L'\\' : ch;
}

static BOOL mux_same_config(const WCHAR *left, const WCHAR *right)
{
    while (mux_config_char(*left) == mux_config_char(*right)) {
        if (!*left) return TRUE;
        left++; right++;
    }
    return FALSE;
}

static unsigned long long mux_identity(const struct uurb_mux_plan *plan)
{
    unsigned long long hash = 14695981039346656037ULL;
    const WCHAR *parts[] = {plan->config, plan->session};
    for (unsigned i = 0; i < ARRAYSIZE(parts); i++) {
        for (const WCHAR *p = parts[i]; *p; p++) {
            hash ^= (unsigned)(i == 0 ? mux_config_char(*p) : *p);
            hash *= 1099511628211ULL;
        }
        hash ^= 0; hash *= 1099511628211ULL;
    }
    return hash;
}

static BOOL mux_owned_path(const struct uurb_mux_plan *plan, WCHAR *path, size_t capacity)
{
    return swprintf(path, capacity, L"%ls.uu-owned-%016llx", plan->config,
                    mux_identity(plan)) > 0;
}

struct uurb_mux_record { DWORD magic; struct uurb_mux_plan plan; };

static BOOL mux_read_owned(struct uurb_mux_plan *plan)
{
    WCHAR path[8192];
    struct uurb_mux_record record;
    DWORD bytes = 0;
    LARGE_INTEGER size;
    if (!mux_owned_path(plan, path, ARRAYSIZE(path))) return FALSE;
    HANDLE file = CreateFileW(path, GENERIC_READ, FILE_SHARE_READ, NULL, OPEN_EXISTING, 0, NULL);
    if (file == INVALID_HANDLE_VALUE) return FALSE;
    BOOL read = GetFileSizeEx(file, &size) && size.QuadPart == sizeof(record) &&
        ReadFile(file, &record, sizeof(record), &bytes, NULL) && bytes == sizeof(record);
    CloseHandle(file);
    if (!read || record.magic != 0x314d5555 || !record.plan.create ||
        record.plan.mux[4095] || record.plan.config[4095] || record.plan.shell[4095] ||
        record.plan.session[255] || record.plan.title[1023] ||
        wcscmp(record.plan.mux, plan->mux) || !mux_same_config(record.plan.config, plan->config) ||
        wcscmp(record.plan.session, plan->session) ||
        !mux_executable(record.plan.shell, L"powershell.exe")) return FALSE;
    *plan = record.plan;
    return TRUE;
}

static BOOL mux_save_owned(const struct uurb_mux_plan *plan)
{
    WCHAR path[8192];
    if (!mux_owned_path(plan, path, ARRAYSIZE(path))) return FALSE;
    if (!mux_persistent()) {
        struct uurb_mux_plan previous = *plan;
        if (mux_read_owned(&previous)) DeleteFileW(path);
        return TRUE;
    }
    struct uurb_mux_record record = {0x314d5555, *plan};
    HANDLE file = CreateFileW(path, GENERIC_WRITE, 0, NULL, CREATE_NEW, 0, NULL);
    if (file == INVALID_HANDLE_VALUE &&
        (GetLastError() == ERROR_FILE_EXISTS || GetLastError() == ERROR_ALREADY_EXISTS)) {
        struct uurb_mux_plan previous = *plan;
        if (!mux_read_owned(&previous)) return FALSE;
        file = CreateFileW(path, GENERIC_WRITE, 0, NULL, OPEN_EXISTING, 0, NULL);
    }
    if (file == INVALID_HANDLE_VALUE) return FALSE;
    DWORD bytes = 0;
    BOOL saved = WriteFile(file, &record, sizeof(record), &bytes, NULL) && bytes == sizeof(record);
    CloseHandle(file);
    return saved;
}

static BOOL mux_load_compat(const WCHAR *module)
{
    WCHAR path[4096];
    wcscpy(path, module);
    WCHAR *leaf = wcsrchr(path, L'\\');
    WCHAR *slash = wcsrchr(path, L'/');
    if (slash && (!leaf || slash > leaf)) leaf = slash;
    if (!leaf || (size_t)(leaf - path) + 12 >= ARRAYSIZE(path)) return FALSE;
    wcscpy(leaf + 1, L"conpty.dll");
    return LoadLibraryW(path) != NULL;
}

/* The vendor daemon requires its original executable basename. Keep the
 * audited backup untouched and run that same binary in an owned subdirectory. */
static BOOL mux_original_path(const WCHAR *module, WCHAR *path, size_t capacity)
{
    static const WCHAR suffix[] = L"uu-terminal-vendor\\uuyc-mux.exe";
    const WCHAR *leaf = wcsrchr(module, L'\\');
    const WCHAR *slash = wcsrchr(module, L'/');
    if (slash && (!leaf || slash > leaf)) leaf = slash;
    size_t directory = leaf ? (size_t)(leaf - module) + 1 : 0;
    if (!directory || directory + ARRAYSIZE(suffix) > capacity) return FALSE;
    wmemcpy(path, module, directory);
    wcscpy(path + directory, suffix);
    return TRUE;
}

static DWORD mux_recover(struct uurb_mux_plan *plan, const WCHAR *original)
{
    WCHAR mutex_name[64];
    swprintf(mutex_name, ARRAYSIZE(mutex_name), L"Local\\UURB-Mux-%016llx", mux_identity(plan));
    HANDLE lock = CreateMutexW(NULL, FALSE, mutex_name);
    if (!lock) return 1;
    DWORD wait = WaitForSingleObject(lock, 5000), code = 1;
    if (wait == WAIT_OBJECT_0 || wait == WAIT_ABANDONED) {
        const WCHAR *check[] = {original,L"-L",L"uuyc-terminal",L"-f",plan->config,
                              L"has-session",L"-t",plan->session,NULL};
        code = mux_run(original, check, FALSE);
        if (code == 1 && mux_load_compat(plan->mux)) {
            struct uurb_mux_plan recovery = *plan;
            wcscpy(recovery.mux, original);
            code = mux_create_session(&recovery);
        }
        ReleaseMutex(lock);
    }
    CloseHandle(lock);
    return code;
}

/* Forward the vendor CLI unchanged except an exact owned has-session/attach
 * can reconstruct its Windows mux metadata in persistent mode. */
static int mux_cli_dispatch(int argc, WCHAR **argv, const WCHAR *module)
{
    WCHAR original[4096];
    if (!mux_original_path(module, original, ARRAYSIZE(original))) return 64;
    const WCHAR **forward = HeapAlloc(GetProcessHeap(), 0, (argc + 1) * sizeof(*forward));
    if (!forward) return 4;
    for (int i = 0; i < argc; i++) forward[i] = i ? argv[i] : original;
    forward[argc] = NULL;
    struct uurb_mux_plan plan = {0};
    BOOL exact = argc == 8 && !wcscmp(argv[1], L"-L") && !wcscmp(argv[2], L"uuyc-terminal") &&
        !wcscmp(argv[3], L"-f") && !wcscmp(argv[6], L"-t") &&
        wcslen(argv[4]) < ARRAYSIZE(plan.config) && wcslen(argv[7]) < ARRAYSIZE(plan.session);
    BOOL has = exact && !wcscmp(argv[5], L"has-session");
    BOOL attach = exact && !wcscmp(argv[5], L"attach");
    BOOL kill = exact && !wcscmp(argv[5], L"kill-session");
    if (exact) { wcscpy(plan.mux, module); wcscpy(plan.config, argv[4]); wcscpy(plan.session, argv[7]); }
    BOOL owned = exact && mux_read_owned(&plan);
    DWORD code;
    if ((has || attach) && owned && mux_persistent()) {
        code = mux_recover(&plan, original);
        if (code != 0 || has) goto done;
    }
    if ((argc > 5 && (!wcscmp(argv[5], L"new") || !wcscmp(argv[5], L"attach"))) &&
        !mux_load_compat(module)) { code = 4; goto done; }
    code = mux_run(original, forward, attach);
    if (kill && owned && code == 0) {
        WCHAR path[8192];
        if (mux_owned_path(&plan, path, ARRAYSIZE(path))) DeleteFileW(path);
    }
done:
    HeapFree(GetProcessHeap(), 0, forward);
    return (int)code;
}
#endif
