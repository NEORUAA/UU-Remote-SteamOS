#ifndef UURB_TERMINAL_MUX_BOOTSTRAP_H
#define UURB_TERMINAL_MUX_BOOTSTRAP_H
#include <wchar.h>
#include <shellapi.h>
#include "uu_terminal_console.h"

/* Match the two fixed UU 4.42 bootstrap templates. This is not a PowerShell
 * interpreter: all commands, flags, and control flow below are fixed. */
struct uurb_mux_plan {
    WCHAR mux[4096], config[4096], shell[4096];
    WCHAR session[256], title[1024];
    BOOL create;
};
static BOOL mux_expect(const WCHAR **cursor, const WCHAR *literal)
{
    size_t length = wcslen(literal);
    if (wcsncmp(*cursor, literal, length)) return FALSE;
    *cursor += length;
    return TRUE;
}
static BOOL mux_quoted(const WCHAR **cursor, WCHAR *value, size_t capacity)
{
    size_t length = 0;
    if (**cursor != L'\'') return FALSE;
    (*cursor)++;
    while (**cursor) {
        WCHAR ch = *(*cursor)++;
        if (ch == L'\'') {
            if (**cursor != L'\'') { value[length] = 0; return TRUE; }
            (*cursor)++;
        }
        if (ch == L'\r' || ch == L'\n' || length + 1 >= capacity) return FALSE;
        value[length++] = ch;
    }
    return FALSE;
}
static BOOL mux_same_quoted(const WCHAR **cursor, const WCHAR *expected)
{
    WCHAR value[4096];
    return mux_quoted(cursor, value, 4096) && !wcscmp(value, expected);
}
static BOOL mux_invocation(const WCHAR **cursor, struct uurb_mux_plan *plan, BOOL first)
{
    if (!mux_expect(cursor, L"& ")) return FALSE;
    if (first) {
        if (!mux_quoted(cursor, plan->mux, 4096)) return FALSE;
    } else if (!mux_same_quoted(cursor, plan->mux)) return FALSE;
    if (!mux_expect(cursor, L" -L uuyc-terminal -f ")) return FALSE;
    if (first) return mux_quoted(cursor, plan->config, 4096) && mux_expect(cursor, L" ");
    return mux_same_quoted(cursor, plan->config) && mux_expect(cursor, L" ");
}
static BOOL mux_exit_check(const WCHAR **cursor, const WCHAR *name)
{
    WCHAR text[256];
    swprintf(text, 256, L"; $%ls = $LASTEXITCODE; if ($%ls -ne 0) { exit $%ls }; ", name, name, name);
    return mux_expect(cursor, text);
}
static BOOL mux_executable(const WCHAR *path, const WCHAR *basename)
{
    const WCHAR *leaf = wcsrchr(path, L'\\');
    const WCHAR *slash = wcsrchr(path, L'/');
    if (slash && (!leaf || slash > leaf)) leaf = slash;
    return wcslen(path) > 3 && path[1] == L':' &&
           (path[2] == L'\\' || path[2] == L'/') &&
           leaf && !_wcsicmp(leaf + 1, basename);
}
static BOOL mux_parse(const WCHAR *script, struct uurb_mux_plan *plan)
{
    WCHAR chcp[4096], target[258];
    const WCHAR *cursor = script;
    memset(plan, 0, sizeof(*plan));
    if (!mux_expect(&cursor, L"[Console]::OutputEncoding = [Text.Encoding]::UTF8; [Console]::InputEncoding = [Text.Encoding]::UTF8; $OutputEncoding = [Text.Encoding]::UTF8; & ") ||
        !mux_quoted(&cursor, chcp, 4096) || !mux_executable(chcp, L"chcp.com") ||
        !mux_expect(&cursor, L" 65001 | Out-Null; ") ||
        !mux_invocation(&cursor, plan, TRUE) || !mux_executable(plan->mux, L"uuyc-mux.exe")) return FALSE;
    if (mux_expect(&cursor, L"new -d -s ")) {
        plan->create = TRUE;
        if (!mux_quoted(&cursor, plan->session, 256) || !plan->session[0] ||
            !mux_expect(&cursor, L" -- ") || !mux_quoted(&cursor, plan->shell, 4096) ||
            !mux_executable(plan->shell, L"powershell.exe") ||
            !mux_expect(&cursor, L" -NoLogo -NoProfile") || !mux_exit_check(&cursor, L"newExit")) return FALSE;
        swprintf(target, 258, L"%ls:", plan->session);
        if (!mux_invocation(&cursor, plan, FALSE) || !mux_expect(&cursor, L"set-option -t ") ||
            !mux_same_quoted(&cursor, target) || !mux_expect(&cursor, L" set-titles-string '#W'") ||
            !mux_exit_check(&cursor, L"titlesStringExit")) return FALSE;
        if (!mux_invocation(&cursor, plan, FALSE) || !mux_expect(&cursor, L"set-option -t ") ||
            !mux_same_quoted(&cursor, target) || !mux_expect(&cursor, L" set-titles on") ||
            !mux_exit_check(&cursor, L"titlesExit")) return FALSE;
        if (!mux_invocation(&cursor, plan, FALSE) || !mux_expect(&cursor, L"rename-window -t ") ||
            !mux_same_quoted(&cursor, target) || !mux_expect(&cursor, L" ") ||
            !mux_quoted(&cursor, plan->title, 1024) || !mux_exit_check(&cursor, L"renameExit")) return FALSE;
        if (!mux_invocation(&cursor, plan, FALSE) || !mux_expect(&cursor, L"set-option -t ") ||
            !mux_same_quoted(&cursor, target) || !mux_expect(&cursor, L" status off") ||
            !mux_exit_check(&cursor, L"statusExit") || !mux_invocation(&cursor, plan, FALSE)) return FALSE;
    } else {
        if (!mux_expect(&cursor, L"attach -t ") || !mux_quoted(&cursor, plan->session, 256) ||
            !plan->session[0] || !mux_expect(&cursor, L"; exit $LASTEXITCODE") || *cursor) return FALSE;
        return TRUE;
    }
    return mux_expect(&cursor, L"attach -t ") && mux_same_quoted(&cursor, plan->session) &&
           mux_expect(&cursor, L"; exit $LASTEXITCODE") && !*cursor;
}
/* Quote argv for CreateProcessW, including literal quotes and trailing slashes. */
static BOOL mux_append(WCHAR *command, size_t capacity, const WCHAR *argument)
{
    size_t at = wcslen(command), slashes = 0;
    if (at + 3 >= capacity) return FALSE;
    if (at) command[at++] = L' ';
    command[at++] = L'"';
    for (;;) {
        WCHAR ch = *argument++;
        if (ch == L'\\') { slashes++; continue; }
        size_t count = slashes * ((ch == L'"' || !ch) ? 2 : 1) + (ch == L'"' ? 1 : 0);
        if (at + count + 2 >= capacity) return FALSE;
        while (count--) command[at++] = L'\\';
        slashes = 0;
        if (!ch) break;
        command[at++] = ch;
    }
    command[at++] = L'"'; command[at] = 0;
    return TRUE;
}
static DWORD mux_run(const WCHAR *exe, const WCHAR *const *arguments, BOOL interactive)
{
    WCHAR command[32768] = {0};
    STARTUPINFOW startup = {0};
    PROCESS_INFORMATION child = {0};
    DWORD code = 1;
    if (interactive && (!uurb_console_stdio() || !SetConsoleCP(CP_UTF8) || !SetConsoleOutputCP(CP_UTF8))) return 4;
    for (size_t i = 0; arguments[i]; i++)
        if (!mux_append(command, 32768, arguments[i])) return 2;
    startup.cb = sizeof(startup);
    startup.dwFlags = STARTF_USESTDHANDLES;
    startup.hStdInput = GetStdHandle(STD_INPUT_HANDLE);
    startup.hStdOutput = GetStdHandle(STD_OUTPUT_HANDLE);
    startup.hStdError = GetStdHandle(STD_ERROR_HANDLE);
    if (!CreateProcessW(exe, command, NULL, NULL, TRUE, 0, NULL, NULL, &startup, &child)) return 3;
    if (WaitForSingleObject(child.hProcess, INFINITE) != WAIT_OBJECT_0 || !GetExitCodeProcess(child.hProcess, &code)) code = 3;
    CloseHandle(child.hThread); CloseHandle(child.hProcess);
    return code;
}
static DWORD mux_create_session(struct uurb_mux_plan *plan)
{
    WCHAR target[258];
    const WCHAR *base[] = {plan->mux, L"-L", L"uuyc-terminal", L"-f", plan->config};
    DWORD code;
    swprintf(target, 258, L"%ls:", plan->session);
    {
        const WCHAR *create[] = {base[0],base[1],base[2],base[3],base[4],L"new",L"-d",L"-s",plan->session,L"--",plan->shell,L"-NoLogo",L"-NoProfile",NULL};
        const WCHAR *titles[] = {base[0],base[1],base[2],base[3],base[4],L"set-option",L"-t",target,L"set-titles-string",L"#W",NULL};
        const WCHAR *enable[] = {base[0],base[1],base[2],base[3],base[4],L"set-option",L"-t",target,L"set-titles",L"on",NULL};
        const WCHAR *rename[] = {base[0],base[1],base[2],base[3],base[4],L"rename-window",L"-t",target,plan->title,NULL};
        const WCHAR *status[] = {base[0],base[1],base[2],base[3],base[4],L"set-option",L"-t",target,L"status",L"off",NULL};
        const WCHAR *const *commands[] = {create,titles,enable,rename,status};
        for (size_t i = 0; i < 5; i++) if ((code = mux_run(plan->mux, commands[i], FALSE)) != 0) {
            fprintf(stderr, "terminal-mux-bootstrap-failed command_index=%u exit=%lu\n", (unsigned)i, code);
            return code;
        }
    }
    return 0;
}

#include "uu_terminal_mux_recovery.h"

static int mux_execute(struct uurb_mux_plan *plan)
{
    DWORD code;
    if (plan->create) {
        struct uurb_mux_plan creation = *plan;
        WCHAR original[4096];
        if (!mux_original_path(plan->mux, original, ARRAYSIZE(original))) return 64;
        if (GetFileAttributesW(original) != INVALID_FILE_ATTRIBUTES)
            wcscpy(creation.mux, original);
        if ((code = mux_create_session(&creation)) != 0) return (int)code;
        if (!mux_save_owned(plan)) {
            write_error("UU terminal proxy could not record its owned persistent session");
            return 4;
        }
    }
    const WCHAR *base[] = {plan->mux, L"-L", L"uuyc-terminal", L"-f", plan->config};
    const WCHAR *attach[] = {base[0],base[1],base[2],base[3],base[4],L"attach",L"-t",plan->session,NULL};
    return (int)mux_run(plan->mux, attach, TRUE);
}
/* Return -1 for ordinary interactive/pipe invocation; reject unknown scripts. */
static int mux_dispatch(void)
{
    int argc, result = -1;
    WCHAR **argv = CommandLineToArgvW(GetCommandLineW(), &argc);
    if (!argv) return 64;
    WCHAR module[4096];
    DWORD length = GetModuleFileNameW(NULL, module, ARRAYSIZE(module));
    if (length && length < ARRAYSIZE(module) && mux_executable(module, L"uuyc-mux.exe")) {
        result = mux_cli_dispatch(argc, argv, module);
        LocalFree(argv);
        return result;
    }
    for (int i = 1; i < argc; i++) if (!_wcsicmp(argv[i], L"-Command")) {
        struct uurb_mux_plan plan;
        if (argc != 5 || i != 3 || _wcsicmp(argv[1], L"-NoLogo") || _wcsicmp(argv[2], L"-NoProfile") || !mux_parse(argv[i+1], &plan)) {
            write_error("UU terminal proxy rejected an unsupported bootstrap script"); result = 64;
        } else result = mux_execute(&plan);
        break;
    }
    LocalFree(argv);
    return result;
}
#endif
