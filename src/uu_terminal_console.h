#ifndef UURB_TERMINAL_CONSOLE_H
#define UURB_TERMINAL_CONSOLE_H
#include <windows.h>
/* Wine attaches ConPTY but can leave the inherited stdio handles in place. */
static BOOL uurb_console_stdio(void)
{
    DWORD mode;
    HANDLE input = CreateFileW(L"CONIN$", GENERIC_READ | GENERIC_WRITE,
        FILE_SHARE_READ | FILE_SHARE_WRITE, NULL, OPEN_EXISTING, 0, NULL);
    if (input == INVALID_HANDLE_VALUE || !GetConsoleMode(input, &mode)) {
        if (input != INVALID_HANDLE_VALUE) CloseHandle(input);
        return FALSE;
    }
    HANDLE output = CreateFileW(L"CONOUT$", GENERIC_READ | GENERIC_WRITE,
        FILE_SHARE_READ | FILE_SHARE_WRITE, NULL, OPEN_EXISTING, 0, NULL);
    if (output == INVALID_HANDLE_VALUE) {
        CloseHandle(input);
        return FALSE;
    }
    if (!SetHandleInformation(input, HANDLE_FLAG_INHERIT, HANDLE_FLAG_INHERIT) ||
        !SetHandleInformation(output, HANDLE_FLAG_INHERIT, HANDLE_FLAG_INHERIT)) {
        DWORD error = GetLastError();
        CloseHandle(input);
        CloseHandle(output);
        SetLastError(error);
        return FALSE;
    }
    if (!SetStdHandle(STD_INPUT_HANDLE, input) ||
        !SetStdHandle(STD_OUTPUT_HANDLE, output) ||
        !SetStdHandle(STD_ERROR_HANDLE, output))
        return FALSE;
    return TRUE;
}
#endif
