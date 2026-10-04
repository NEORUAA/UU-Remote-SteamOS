#ifndef UURB_TERMINAL_DIRECT_IO_H
#define UURB_TERMINAL_DIRECT_IO_H

#include "terminal_bridge_protocol.h"
#include "uu_terminal_runtime_config.h"

/* One UU conpty_bridge process owns one viewer. Its Wine pseudoconsole is
 * private; only these pipe workers carry the viewer's terminal bytes. */
static struct {
    HPCON pc;
    HANDLE input, output, private_input, private_output;
    HANDLE ready, done, worker, drain;
    SOCKET connection;
    CRITICAL_SECTION send_lock;
    COORD size;
    BOOL authenticated;
} direct_io;
static HANDLE child_ready, child_done;

static void direct_trace(const char *phase, DWORD value)
{
    char path[32768];
    DWORD length = GetModuleFileNameA(NULL, path, ARRAYSIZE(path));
    char *leaf = length && length < ARRAYSIZE(path) ? strrchr(path, '\\') : NULL;
    if (!leaf) return;
    if ((size_t)(leaf + 1 - path) + sizeof("uu-terminal-direct.trace") > sizeof(path)) return;
    strcpy(leaf + 1, "uu-terminal-direct.trace");
    HANDLE file = CreateFileA(path, FILE_APPEND_DATA, FILE_SHARE_READ | FILE_SHARE_WRITE,
                              NULL, OPEN_ALWAYS, FILE_ATTRIBUTE_NORMAL, NULL);
    if (file == INVALID_HANDLE_VALUE) return;
    SYSTEMTIME t; GetSystemTime(&t);
    char line[192];
    int count = snprintf(line, sizeof(line), "%04u-%02u-%02uT%02u:%02u:%02u.%03uZ pid=%lu phase=%s value=%lu\r\n",
                         t.wYear, t.wMonth, t.wDay, t.wHour, t.wMinute, t.wSecond,
                         t.wMilliseconds, GetCurrentProcessId(), phase, value);
    DWORD written;
    if (count > 0 && count < (int)sizeof(line)) WriteFile(file, line, (DWORD)count, &written, NULL);
    CloseHandle(file);
}

static BOOL direct_controller(void)
{
    WCHAR module[4096];
    DWORD length = GetModuleFileNameW(NULL, module, ARRAYSIZE(module));
    WCHAR *leaf = length && length < ARRAYSIZE(module) ? wcsrchr(module, L'\\') : NULL;
    if (!leaf || _wcsicmp(leaf + 1, L"conpty_bridge.exe")) return FALSE;
    int argc;
    WCHAR **argv = CommandLineToArgvW(GetCommandLineW(), &argc);
    if (!argv) return FALSE;
    BOOL managed = FALSE;
    for (int i = 1; i + 1 < argc; i++) if (!wcscmp(argv[i], L"--uuyc-mux-session")) {
        const WCHAR *name = argv[i + 1]; size_t count = 0;
        while (name[count] && ((name[count] >= L'a' && name[count] <= L'z') ||
               (name[count] >= L'A' && name[count] <= L'Z') ||
               (name[count] >= L'0' && name[count] <= L'9') ||
               name[count] == L'_' || name[count] == L'-' || name[count] == L'.')) count++;
        managed = count > 0 && count < 256 && !name[count];
        break;
    }
    LocalFree(argv);
    return managed;
}

static BOOL direct_send_all(SOCKET connection, const void *data, size_t length)
{
    const char *cursor = data;
    while (length) {
        int sent = send(connection, cursor, (int)length, 0);
        if (sent <= 0) return FALSE;
        cursor += sent; length -= (size_t)sent;
    }
    return TRUE;
}

static BOOL direct_frame_locked(uint8_t type, const void *data, uint32_t length)
{
    struct uurb_terminal_frame frame = {0};
    frame.type = type; frame.length = htonl(length);
    return direct_io.connection != INVALID_SOCKET &&
        direct_send_all(direct_io.connection, &frame, sizeof(frame)) &&
        (!length || direct_send_all(direct_io.connection, data, length));
}

static BOOL direct_frame(uint8_t type, const void *data, uint32_t length)
{
    EnterCriticalSection(&direct_io.send_lock);
    BOOL result = direct_frame_locked(type, data, length);
    LeaveCriticalSection(&direct_io.send_lock);
    return result;
}

static DWORD WINAPI direct_input(void *unused)
{
    (void)unused;
    unsigned char bytes[16384]; DWORD count;
    while (WaitForSingleObject(direct_io.done, 0) == WAIT_TIMEOUT) {
        BOOL read = ReadFile(direct_io.input, bytes, sizeof(bytes), &count, NULL);
        if (!read || !count) {
            direct_trace(read ? "input-eof" : "input-read-failed", read ? 0 : GetLastError());
            direct_frame(UURB_TERMINAL_FRAME_EOF, NULL, 0);
            break;
        }
        if (!direct_frame(UURB_TERMINAL_FRAME_DATA, bytes, count)) {
            direct_trace("input-send-failed", WSAGetLastError());
            break;
        }
        DWORD interrupts = 0;
        for (DWORD i = 0; i < count; i++) if (bytes[i] == 0x03) interrupts++;
        if (interrupts) direct_trace("input-Ctrl03", interrupts);
        direct_trace("input-bytes", count);
    }
    SetEvent(direct_io.done);
    EnterCriticalSection(&direct_io.send_lock);
    if (direct_io.connection != INVALID_SOCKET) shutdown(direct_io.connection, SD_BOTH);
    LeaveCriticalSection(&direct_io.send_lock);
    return 0;
}

static DWORD WINAPI direct_drain(void *unused)
{
    (void)unused;
    char bytes[4096]; DWORD count;
    while (ReadFile(direct_io.private_output, bytes, sizeof(bytes), &count, NULL) && count) { }
    return 0;
}

static DWORD WINAPI direct_worker(void *unused)
{
    (void)unused;
    HANDLE events[] = {direct_io.done, direct_io.ready};
    if (WaitForMultipleObjects(2, events, FALSE, INFINITE) != WAIT_OBJECT_0 + 1) return 0;
    char token[UURB_TERMINAL_TOKEN_LENGTH + 1] = {0};
    uint16_t port;
    WSADATA winsock;
    HANDLE input = NULL;
    SOCKET connection = INVALID_SOCKET;
    BOOL initialized = FALSE;
    if (!load_configuration(token, &port) || WSAStartup(MAKEWORD(2, 2), &winsock)) goto done;
    initialized = TRUE;
    connection = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    if (connection == INVALID_SOCKET) goto done;
    DWORD timeout = 5000;
    setsockopt(connection, SOL_SOCKET, SO_RCVTIMEO, (const char *)&timeout, sizeof(timeout));
    setsockopt(connection, SOL_SOCKET, SO_SNDTIMEO, (const char *)&timeout, sizeof(timeout));
    struct sockaddr_in address = {0};
    address.sin_family = AF_INET; address.sin_port = htons(port);
    address.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
    EnterCriticalSection(&direct_io.send_lock);
    direct_io.connection = connection;
    BOOL stopping = WaitForSingleObject(direct_io.done, 0) != WAIT_TIMEOUT;
    LeaveCriticalSection(&direct_io.send_lock);
    if (stopping || connect(connection, (struct sockaddr *)&address, sizeof(address))) goto done;
    struct uurb_terminal_hello hello = {0};
    hello.magic = htonl(UURB_TERMINAL_MAGIC); hello.version = htons(UURB_TERMINAL_VERSION);
    hello.token_length = htons(UURB_TERMINAL_TOKEN_LENGTH);
    EnterCriticalSection(&direct_io.send_lock);
    hello.columns = htons((uint16_t)direct_io.size.X); hello.rows = htons((uint16_t)direct_io.size.Y);
    LeaveCriticalSection(&direct_io.send_lock);
    unsigned char accepted = 0;
    if (!direct_send_all(connection, &hello, sizeof(hello)) ||
        !direct_send_all(connection, token, UURB_TERMINAL_TOKEN_LENGTH) ||
        recv(connection, (char *)&accepted, 1, 0) != 1 || accepted != UURB_TERMINAL_ACCEPTED) goto done;
    SecureZeroMemory(token, sizeof(token));
    timeout = 0;
    setsockopt(connection, SOL_SOCKET, SO_RCVTIMEO, (const char *)&timeout, sizeof(timeout));
    EnterCriticalSection(&direct_io.send_lock);
    uint16_t dimensions[] = {htons((uint16_t)direct_io.size.X), htons((uint16_t)direct_io.size.Y)};
    BOOL resized = dimensions[0] != hello.columns || dimensions[1] != hello.rows;
    BOOL size_sent = !resized || direct_frame_locked(UURB_TERMINAL_FRAME_RESIZE, dimensions, sizeof(dimensions));
    direct_io.authenticated = size_sent;
    LeaveCriticalSection(&direct_io.send_lock);
    if (!size_sent) goto done;
    direct_trace("authenticated", ((DWORD)ntohs(hello.columns) << 16) | ntohs(hello.rows));
    input = CreateThread(NULL, 0, direct_input, NULL, 0, NULL);
    if (!input) goto done;
    char bytes[16384]; int count;
    while ((count = recv(connection, bytes, sizeof(bytes), 0)) > 0) {
        DWORD at = 0;
        while (at < (DWORD)count) {
            DWORD written;
            if (!WriteFile(direct_io.output, bytes + at, count - at, &written, NULL) || !written) goto done;
            at += written;
        }
        direct_trace("output-bytes", (DWORD)count);
    }
    direct_trace("output-end", count < 0 ? WSAGetLastError() : 0);
done:
    SecureZeroMemory(token, sizeof(token));
    SetEvent(direct_io.done);
    EnterCriticalSection(&direct_io.send_lock);
    if (connection != INVALID_SOCKET) shutdown(connection, SD_BOTH);
    LeaveCriticalSection(&direct_io.send_lock);
    if (input) { CancelSynchronousIo(input); WaitForSingleObject(input, INFINITE); CloseHandle(input); }
    EnterCriticalSection(&direct_io.send_lock);
    direct_io.connection = INVALID_SOCKET;
    direct_io.authenticated = FALSE;
    LeaveCriticalSection(&direct_io.send_lock);
    if (connection != INVALID_SOCKET) closesocket(connection);
    if (initialized) WSACleanup();
    direct_trace("viewer-done", 0);
    return 0;
}

static void direct_close(void)
{
    SetEvent(direct_io.done);
    EnterCriticalSection(&direct_io.send_lock);
    if (direct_io.connection != INVALID_SOCKET) shutdown(direct_io.connection, SD_BOTH);
    LeaveCriticalSection(&direct_io.send_lock);
    if (direct_io.worker) { CancelSynchronousIo(direct_io.worker); WaitForSingleObject(direct_io.worker, INFINITE); CloseHandle(direct_io.worker); }
    if (direct_io.private_input) CloseHandle(direct_io.private_input);
    if (!direct_io.drain && direct_io.private_output) {
        CloseHandle(direct_io.private_output); direct_io.private_output = NULL;
    }
    if (direct_io.pc) ClosePseudoConsole(direct_io.pc);
    if (direct_io.drain) { WaitForSingleObject(direct_io.drain, INFINITE); CloseHandle(direct_io.drain); }
    HANDLE handles[] = {direct_io.input, direct_io.output, direct_io.private_output, direct_io.ready, direct_io.done};
    for (unsigned i = 0; i < ARRAYSIZE(handles); i++) if (handles[i]) CloseHandle(handles[i]);
    DeleteCriticalSection(&direct_io.send_lock);
    memset(&direct_io, 0, sizeof(direct_io));
}

static HRESULT direct_create(COORD size, HANDLE input, HANDLE output, DWORD flags, HPCON *pc)
{
    if (!pc) return E_POINTER;
    *pc = NULL;
    if (direct_io.pc || size.X <= 0 || size.Y <= 0 || size.X > 1000 || size.Y > 1000 ||
        GetFileType(input) != FILE_TYPE_PIPE || GetFileType(output) != FILE_TYPE_PIPE) return E_INVALIDARG;
    InitializeCriticalSection(&direct_io.send_lock);
    direct_io.connection = INVALID_SOCKET; direct_io.size = size;
    direct_io.ready = CreateEventW(NULL, TRUE, FALSE, NULL);
    direct_io.done = CreateEventW(NULL, TRUE, FALSE, NULL);
    HANDLE private_read = NULL, private_write = NULL;
    HRESULT result = E_FAIL;
    if (!direct_io.ready || !direct_io.done ||
        !DuplicateHandle(GetCurrentProcess(), input, GetCurrentProcess(), &direct_io.input, 0, FALSE, DUPLICATE_SAME_ACCESS) ||
        !DuplicateHandle(GetCurrentProcess(), output, GetCurrentProcess(), &direct_io.output, 0, FALSE, DUPLICATE_SAME_ACCESS) ||
        !CreatePipe(&private_read, &direct_io.private_input, NULL, 0) ||
        !CreatePipe(&direct_io.private_output, &private_write, NULL, 0)) goto failed;
    result = CreatePseudoConsole(size, private_read, private_write, flags & ~PSEUDOCONSOLE_INHERIT_CURSOR, &direct_io.pc);
    CloseHandle(private_read); CloseHandle(private_write); private_read = private_write = NULL;
    if (FAILED(result)) goto failed;
    direct_io.drain = CreateThread(NULL, 0, direct_drain, NULL, 0, NULL);
    direct_io.worker = CreateThread(NULL, 0, direct_worker, NULL, 0, NULL);
    if (!direct_io.drain || !direct_io.worker) { result = E_OUTOFMEMORY; goto failed; }
    *pc = direct_io.pc;
    direct_trace("created", ((DWORD)size.X << 16) | (WORD)size.Y);
    return S_OK;
failed:
    if (private_read) CloseHandle(private_read);
    if (private_write) CloseHandle(private_write);
    direct_close();
    return result;
}

static HRESULT direct_resize(COORD size)
{
    if (size.X <= 0 || size.Y <= 0 || size.X > 1000 || size.Y > 1000) return E_INVALIDARG;
    /* The private Wine console only owns child lifetime. Viewer dimensions
     * belong to the native PTY and do not depend on Wine's resize support. */
    EnterCriticalSection(&direct_io.send_lock);
    direct_io.size = size;
    uint16_t dimensions[] = {htons((uint16_t)size.X), htons((uint16_t)size.Y)};
    BOOL sent = !direct_io.authenticated || direct_frame_locked(UURB_TERMINAL_FRAME_RESIZE, dimensions, sizeof(dimensions));
    LeaveCriticalSection(&direct_io.send_lock);
    if (!sent) return E_FAIL;
    direct_trace("resize", ((DWORD)size.X << 16) | (WORD)size.Y);
    return S_OK;
}

struct direct_child_events { HANDLE ready, done; };

DWORD WINAPI uurb_bind_direct(void *argument)
{
    const struct direct_child_events *events = argument;
    child_ready = events->ready; child_done = events->done;
    return child_ready && child_done;
}

DWORD WINAPI uurb_direct_bound(void)
{
    return child_ready && child_done;
}

int WINAPI uurb_wait_direct(void)
{
    if (!child_ready || !child_done) return -1;
    SetEvent(child_ready);
    direct_trace("metadata-ready", 0);
    DWORD result = WaitForSingleObject(child_done, INFINITE);
    CloseHandle(child_ready); CloseHandle(child_done); child_ready = child_done = NULL;
    return result == WAIT_OBJECT_0 ? 0 : 4;
}

#endif
