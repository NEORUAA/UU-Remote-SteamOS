#define _WIN32_WINNT 0x0600
#define _UNICODE
#include <windows.h>
#include <tlhelp32.h>
#include <stdio.h>
#include <stdint.h>
#include <string.h>

static unsigned mux_count(void)
{
    unsigned count = 0;
    HANDLE snapshot = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
    PROCESSENTRY32W entry = {0}; entry.dwSize = sizeof(entry);
    if (snapshot != INVALID_HANDLE_VALUE && Process32FirstW(snapshot, &entry)) do {
        const WCHAR *name = wcsrchr(entry.szExeFile, L'\\');
        if (!_wcsicmp(name ? name + 1 : entry.szExeFile, L"uuyc-mux.exe")) count++;
    } while (Process32NextW(snapshot, &entry));
    if (snapshot != INVALID_HANDLE_VALUE) CloseHandle(snapshot);
    return count;
}

static DWORD cli(WCHAR **argv, const WCHAR *exe, const WCHAR *command, const WCHAR *session, const WCHAR *extra)
{
    WCHAR text[8192];
    swprintf(text, ARRAYSIZE(text), L"\"%ls\" -L uuyc-terminal -f \"Z:%ls\" %ls %ls%ls %ls", exe, argv[2], command, session ? L"-t " : L"", session ? session : L"", extra ? extra : L"");
    STARTUPINFOW startup = {0}; PROCESS_INFORMATION child = {0};
    startup.cb = sizeof(startup);
    if (!CreateProcessW(exe, text, NULL, NULL, TRUE, CREATE_NO_WINDOW, NULL, NULL, &startup, &child)) return 99;
    DWORD code = 99;
    if (WaitForSingleObject(child.hProcess, 15000) == WAIT_OBJECT_0) GetExitCodeProcess(child.hProcess, &code);
    else { TerminateProcess(child.hProcess, 99); WaitForSingleObject(child.hProcess, 1000); }
    CloseHandle(child.hThread); CloseHandle(child.hProcess);
    return code;
}

static BOOL connect_once(WCHAR **argv, BOOL attach, BOOL direct_input)
{
    SECURITY_ATTRIBUTES security = {sizeof(security), NULL, TRUE};
    HANDLE inr, inw, outr, outw, ctlr, ctlw;
    if (!CreatePipe(&inr, &inw, &security, 0) ||
        !CreatePipe(&outr, &outw, &security, 0) ||
        !CreatePipe(&ctlr, &ctlw, &security, 0)) return FALSE;
    SetHandleInformation(inw, HANDLE_FLAG_INHERIT, 0);
    SetHandleInformation(outr, HANDLE_FLAG_INHERIT, 0);
    SetHandleInformation(ctlw, HANDLE_FLAG_INHERIT, 0);
    WCHAR command[2048];
    swprintf(command, 2048,
        L"\"%ls\" --shell powershell --cols 80 --rows 24 --stdin-handle %llx --stdout-handle %llx --ctl-handle %llx --display-name UURB-Probe %ls --uuyc-mux-session uurb-probe-%lu --uuyc-mux-config \"Z:%ls\"",
        argv[1], (unsigned long long)(uintptr_t)inr,
        (unsigned long long)(uintptr_t)outw, (unsigned long long)(uintptr_t)ctlr,
        attach ? L"--uuyc-mux-attach-existing" : L"", GetCurrentProcessId(), argv[2]);
    STARTUPINFOW startup = {0}; PROCESS_INFORMATION child = {0};
    startup.cb = sizeof(startup);
    BOOL started = CreateProcessW(argv[1], command, NULL, NULL, TRUE,
        CREATE_NO_WINDOW, NULL, NULL, &startup, &child);
    printf("phase=%s bridge_started=%d error=%lu\n", attach ? "attach" : "new", started, GetLastError());
    fflush(stdout);
    CloseHandle(inr); CloseHandle(outw); CloseHandle(ctlr);
    if (!started) { CloseHandle(inw); CloseHandle(outr); CloseHandle(ctlw); return FALSE; }
    HANDLE capture = CreateFileW(argv[3], FILE_APPEND_DATA, FILE_SHARE_READ,
        NULL, OPEN_ALWAYS, 0, NULL);
    char captured[65536] = {0}; DWORD length = 0, code = STILL_ACTIVE;
    BOOL sent = FALSE, executed = FALSE, ctrl_marker = FALSE;
    unsigned signal_stage = 0;
    const char *marker = attach ? "UURB_REATTACH_OK" : "UURB_BEFORE_CLOSE_OK";
    for (unsigned tick = 0; tick < (direct_input ? 150U : 80U); tick++) {
        if (tick == 20) {
            char work[2048], state[2048], input[8192];
            WideCharToMultiByte(CP_UTF8, 0, argv[4], -1, work, sizeof(work), NULL, NULL);
            WideCharToMultiByte(CP_UTF8, 0, argv[5], -1, state, sizeof(state), NULL, NULL);
            if (attach) snprintf(input, sizeof(input),
                "printf '%%s %%s\\n' \"$$\" \"$uurb_recovery_job\" > '%s-after'; printf 'UURB_REATTACH_%%s\\n' 'OK'; pwd\r", state);
            else snprintf(input, sizeof(input),
                "cd '%s'; sleep 90 & uurb_recovery_job=$!; printf '%%s %%s\\n' \"$$\" \"$uurb_recovery_job\" > '%s'; printf 'UURB_BEFORE_CLOSE_%%s\\n' 'OK'\r", work, state);
            DWORD written = 0;
            sent = WriteFile(inw, input, (DWORD)strlen(input), &written, NULL)
                && written == strlen(input);
        }
        if (direct_input && executed && signal_stage == 0) {
            char state[2048], input[4096]; DWORD written = 0;
            WideCharToMultiByte(CP_UTF8, 0, argv[5], -1, state, sizeof(state), NULL, NULL);
            snprintf(input, sizeof(input), "sleep 180 & uurb_fg_job=$!; printf '%%s\\n' \"$uurb_fg_job\" > '%s-fg-%s'; fg\r",
                state, attach ? "attach" : "new");
            if (!WriteFile(inw, input, (DWORD)strlen(input), &written, NULL) || written != strlen(input)) break;
            signal_stage = 1;
        }
        if (direct_input && signal_stage == 1) {
            WCHAR ready[4096];
            swprintf(ready, ARRAYSIZE(ready), L"Z:%ls-fg-%ls-ready", argv[5], attach ? L"attach" : L"new");
            if (GetFileAttributesW(ready) != INVALID_FILE_ATTRIBUTES) {
                char state[2048], input[4096]; DWORD written = 0; const char interrupt = 0x03;
                WideCharToMultiByte(CP_UTF8, 0, argv[5], -1, state, sizeof(state), NULL, NULL);
                if (!WriteFile(inw, &interrupt, 1, &written, NULL) || written != 1) break;
                Sleep(200);
                snprintf(input, sizeof(input), "printf 'UURB_CTRL_%s_%%s\\n' 'OK'; printf '%%s %%s\\n' \"$$\" \"$uurb_recovery_job\" > '%s-ctrl-%s'\r",
                    attach ? "ATTACH" : "NEW", state, attach ? "attach" : "new");
                if (!WriteFile(inw, input, (DWORD)strlen(input), &written, NULL) || written != strlen(input)) break;
                signal_stage = 2;
            }
        }
        DWORD available = 0;
        if (PeekNamedPipe(outr, NULL, 0, NULL, &available, NULL) && available) {
            char bytes[4096]; DWORD got = 0, written = 0;
            if (ReadFile(outr, bytes, sizeof(bytes), &got, NULL)) {
                if (capture != INVALID_HANDLE_VALUE) WriteFile(capture, bytes, got, &written, NULL);
                if (length + got < sizeof(captured)) {
                    memcpy(captured + length, bytes, got); length += got; captured[length] = 0;
                    executed = strstr(captured, marker) != NULL;
                    ctrl_marker = strstr(captured, attach ? "UURB_CTRL_ATTACH_OK" : "UURB_CTRL_NEW_OK") != NULL;
                }
            }
        }
        if (GetExitCodeProcess(child.hProcess, &code) && code != STILL_ACTIVE) break;
        Sleep(100);
        if (direct_input && ctrl_marker) break;
    }
    printf("phase=%s before_close_exit=%lu bytes=%lu input_sent=%d exact_marker=%d mux_count=%u retained_cwd=%d\n",
        attach ? "attach" : "new", code, length, sent, executed, mux_count(),
        attach && (strstr(captured, "\r\n/tmp\r\n") != NULL || strstr(captured, "\n/tmp\n") != NULL));
    fflush(stdout);
    if (direct_input) {
        printf("phase=%s plain_marker_before_control=%d raw_Ctrl03_sent=%d post_control_marker=%d viewer_alive=%d\n",
            attach ? "attach" : "new", executed, signal_stage == 2, ctrl_marker, code == STILL_ACTIVE);
        fflush(stdout);
    }
    if (capture != INVALID_HANDLE_VALUE) CloseHandle(capture);
    CloseHandle(inw); CloseHandle(ctlw);
    if (code == STILL_ACTIVE && WaitForSingleObject(child.hProcess, 2000) != WAIT_OBJECT_0) {
        TerminateProcess(child.hProcess, 99); WaitForSingleObject(child.hProcess, 2000);
    }
    GetExitCodeProcess(child.hProcess, &code);
    printf("phase=%s after_close_exit=%lu\n", attach ? "attach" : "new", code);
    fflush(stdout);
    CloseHandle(outr); CloseHandle(child.hThread); CloseHandle(child.hProcess);
    return sent && executed && (!direct_input || (signal_stage == 2 && ctrl_marker && code == 0));
}

int wmain(int argc, WCHAR **argv)
{
    BOOL direct_input = argc == 7 && !wcscmp(argv[6], L"--direct-input");
    if (argc != 6 && !direct_input) return 2;
    BOOL first = connect_once(argv, FALSE, direct_input);
    Sleep(1000);
    printf("after_first_close_mux_count=%u\n", mux_count()); fflush(stdout);
    if (direct_input) return first && connect_once(argv, TRUE, TRUE) ? 0 : 5;
    WCHAR session[256], wrapper[4096], original[4096];
    swprintf(session, ARRAYSIZE(session), L"uurb-probe-%lu", GetCurrentProcessId());
    wcscpy(wrapper, argv[1]); WCHAR *leaf = wcsrchr(wrapper, L'/');
    if (!leaf) leaf = wcsrchr(wrapper, L'\\');
    if (!leaf) return 2;
    wcscpy(leaf + 1, L"uuyc-mux.exe");
    wcscpy(original, wrapper);
    WCHAR *vendor_leaf = wcsrchr(original, L'/');
    if (!vendor_leaf) vendor_leaf = wcsrchr(original, L'\\');
    wcscpy(vendor_leaf + 1, L"uu-terminal-vendor\\uuyc-mux.exe");
    DWORD killed = cli(argv, original, L"kill-server", NULL, NULL);
    DWORD absent = cli(argv, original, L"has-session", session, NULL);
    SetEnvironmentVariableW(L"UURB_TERMINAL_SESSION_MODE", L"fresh");
    DWORD fresh = cli(argv, wrapper, L"set-option", session, L"set-clipboard on");
    SetEnvironmentVariableW(L"UURB_TERMINAL_SESSION_MODE", NULL);
    WCHAR mode[16];
    BOOL mode_absent = !GetEnvironmentVariableW(L"UURB_TERMINAL_SESSION_MODE", mode, ARRAYSIZE(mode));
    DWORD foreign = cli(argv, wrapper, L"set-option", L"uurb-foreign-never-created", L"set-clipboard on");
    DWORD unknown = cli(argv, wrapper, L"set-option", session, L"default-shell powershell.exe");
    DWORD invalid = cli(argv, wrapper, L"set-option", session, L"set-clipboard unknown");
    DWORD still_absent = cli(argv, original, L"has-session", session, NULL);
    DWORD recovered = cli(argv, wrapper, L"set-option", session, L"set-clipboard on");
    printf("forced_loss_kill_exit=%lu original_missing_exit=%lu fresh_setting_exit=%lu foreign_setting_exit=%lu "
           "unknown_option_exit=%lu invalid_value_exit=%lu still_missing_before_known_setting=%lu "
           "Windows_mode_absent=%d owned_first_setting_exit=%lu\n",
           killed, absent, fresh, foreign, unknown, invalid, still_absent, mode_absent, recovered);
    fflush(stdout);
    if (recovered != 0) return 5;
    DWORD off = cli(argv, wrapper, L"set-option", session, L"set-clipboard off");
    printf("owned_second_setting_off_exit=%lu\n", off); fflush(stdout);
    BOOL second = connect_once(argv, TRUE, FALSE);
    return first && second && killed == 0 && absent == 1 && fresh == 1 && foreign == 1 &&
           unknown == 1 && invalid == 1 && still_absent == 1 && mode_absent && recovered == 0 && off == 0 ? 0 : 5;
}
