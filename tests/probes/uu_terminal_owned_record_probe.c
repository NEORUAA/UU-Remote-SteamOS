#define main uurb_proxy_main
#include "uu_terminal_proxy.c"
#undef main

int wmain(int argc, WCHAR **argv)
{
    if (argc != 2 || mux_dispatch() != -1) return 2;
    struct uurb_mux_plan plan = {0};
    wcscpy(plan.mux, L"C:\\owned\\uuyc-mux.exe");
    wcscpy(plan.config, argv[1]); wcscpy(plan.session, L"owned-marker-probe");
    wcscpy(plan.shell, L"C:\\owned\\powershell.exe"); plan.create = TRUE;
    WCHAR path[8192]; if (!mux_owned_path(&plan, path, ARRAYSIZE(path))) return 3;
    HANDLE file = CreateFileW(path, GENERIC_WRITE, 0, NULL, CREATE_NEW, 0, NULL);
    if (file == INVALID_HANDLE_VALUE) return 4;
    DWORD bytes; WriteFile(file, "foreign", 7, &bytes, NULL); CloseHandle(file);
    SetEnvironmentVariableW(L"UURB_TERMINAL_SESSION_MODE", L"persistent");
    BOOL rejected = !mux_save_owned(&plan);
    SetEnvironmentVariableW(L"UURB_TERMINAL_SESSION_MODE", L"fresh");
    BOOL fresh_ok = mux_save_owned(&plan);
    char content[8] = {0};
    file = CreateFileW(path, GENERIC_READ, FILE_SHARE_READ, NULL, OPEN_EXISTING, 0, NULL);
    BOOL preserved = file != INVALID_HANDLE_VALUE && ReadFile(file, content, 7, &bytes, NULL) &&
                     bytes == 7 && !strcmp(content, "foreign");
    if (file != INVALID_HANDLE_VALUE) CloseHandle(file);
    DeleteFileW(path);
    SetEnvironmentVariableW(L"UURB_TERMINAL_SESSION_MODE", L"persistent");
    BOOL created = mux_save_owned(&plan), updated = mux_save_owned(&plan);
    struct uurb_mux_plan readback = plan, alternate = plan;
    BOOL owned = mux_read_owned(&readback);
    for (WCHAR *p = alternate.config; *p; p++) {
        if (*p == L'/') *p = L'\\';
        else if (*p == L'\\') *p = L'/';
    }
    BOOL same_identity = mux_identity(&alternate) == mux_identity(&plan);
    BOOL alternate_read = mux_read_owned(&alternate);
    struct uurb_mux_plan different = plan;
    wcscat(different.config, L".other");
    BOOL other_config_rejected = !mux_read_owned(&different);
    different = plan; wcscpy(different.session, L"other-session");
    BOOL other_session_rejected = !mux_read_owned(&different);
    file = CreateFileW(path, GENERIC_WRITE, 0, NULL, OPEN_EXISTING, 0, NULL);
    if (file == INVALID_HANDLE_VALUE) return 4;
    WriteFile(file, "broken", 6, &bytes, NULL); CloseHandle(file);
    readback = plan;
    BOOL corrupt_rejected = !mux_read_owned(&readback) && !mux_save_owned(&plan);
    DeleteFileW(path);
    BOOL recreated = mux_save_owned(&plan);
    SetEnvironmentVariableW(L"UURB_TERMINAL_SESSION_MODE", L"fresh");
    BOOL removed = mux_save_owned(&plan) && GetFileAttributesW(path) == INVALID_FILE_ATTRIBUTES;
    printf("foreign_rejected=%d foreign_preserved=%d fresh_foreign_untouched=%d valid_created=%d "
           "valid_overwrite=%d valid_read=%d separator_identity=%d separator_read=%d "
           "other_config_rejected=%d other_session_rejected=%d corrupt_rejected=%d fresh_owned_removed=%d\n",
           rejected, preserved, fresh_ok && preserved, created, updated, owned, same_identity,
           alternate_read, other_config_rejected, other_session_rejected, corrupt_rejected, recreated && removed);
    return rejected && preserved && fresh_ok && created && updated && owned && same_identity &&
           alternate_read && other_config_rejected && other_session_rejected && corrupt_rejected &&
           recreated && removed ? 0 : 5;
}
