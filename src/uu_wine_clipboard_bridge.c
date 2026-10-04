#define WIN32_LEAN_AND_MEAN
#define COBJMACROS
#include <winsock2.h>
#include <windows.h>
#include <ole2.h>
#include <shellapi.h>
#include <shlobj.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <wchar.h>

#include "x11_clipboard_protocol.h"

#define UURB_CLIPBOARD_POLL_MS 125UL
#define UURB_CLIPBOARD_MAX_UNITS 1048576UL

static SOCKET clipboard_socket = INVALID_SOCKET;
static BOOL winsock_initialized;
static unsigned short clipboard_port;
static char clipboard_token[UURB_X11_CLIPBOARD_TOKEN_SIZE + 1];
static unsigned int diagnostic_reports;
static BOOL extended_clipboard;
static HWND image_owner;
static HRESULT (WINAPI *get_ole_clipboard)(IDataObject **);
static void (WINAPI *release_medium)(STGMEDIUM *);
static BOOL owner_is_gameviewer(void);

static BOOL copy_global(HGLOBAL handle, char **output, DWORD *size)
{
    SIZE_T length = GlobalSize(handle);
    void *source = GlobalLock(handle);

    if (!source || !length || length > UURB_CLIPBOARD_MAX_BINARY) {
        if (source)
            GlobalUnlock(handle);
        return FALSE;
    }
    *output = HeapAlloc(GetProcessHeap(), 0, length);
    if (*output)
        memcpy(*output, source, length);
    GlobalUnlock(handle);
    *size = (DWORD)length;
    return *output != NULL;
}

static BOOL file_header(const wchar_t *name, char **packet, DWORD *length)
{
    int bytes = WideCharToMultiByte(CP_UTF8, WC_ERR_INVALID_CHARS, name, -1,
                                   NULL, 0, NULL, NULL);
    DWORD name_bytes;

    if (bytes <= 1 || bytes > 1024)
        return FALSE;
    name_bytes = (DWORD)bytes - 1;
    *packet = HeapAlloc(GetProcessHeap(), 0, 4 + (DWORD)bytes);
    if (!*packet)
        return FALSE;
    memcpy(*packet, &name_bytes, 4);
    WideCharToMultiByte(CP_UTF8, WC_ERR_INVALID_CHARS, name, -1,
                        *packet + 4, bytes, NULL, NULL);
    *length = name_bytes + 4;
    return TRUE;
}

static BOOL append_file(char **packet, DWORD *length, const void *data, DWORD size)
{
    char *next;

    if (size > UURB_CLIPBOARD_MAX_BINARY - *length)
        return FALSE;
    next = HeapReAlloc(GetProcessHeap(), 0, *packet, (SIZE_T)*length + size);
    if (!next)
        return FALSE;
    if (size)
        memcpy(next + *length, data, size);
    *packet = next;
    *length += size;
    return TRUE;
}

static BOOL read_drop_file(const wchar_t *path, DWORD sequence,
                           char **packet, DWORD *size)
{
    const wchar_t *name = wcsrchr(path, L'\\');
    const wchar_t *slash = wcsrchr(path, L'/');
    HANDLE file;
    LARGE_INTEGER length;
    char block[65536];
    DWORD received;
    BOOL result = FALSE;

    name = name ? name + 1 : path;
    if (slash && slash + 1 > name)
        name = slash + 1;
    if (!file_header(name, packet, size))
        return FALSE;
    file = CreateFileW(path, GENERIC_READ, FILE_SHARE_READ, NULL, OPEN_EXISTING,
                       FILE_ATTRIBUTE_NORMAL, NULL);
    if (file == INVALID_HANDLE_VALUE)
        return FALSE;
    if (!GetFileSizeEx(file, &length) || length.QuadPart < 0 ||
        (ULONGLONG)length.QuadPart > UURB_CLIPBOARD_MAX_BINARY - *size)
        goto done;
    for (;;) {
        if (GetClipboardSequenceNumber() != sequence ||
            !ReadFile(file, block, sizeof(block), &received, NULL))
            goto done;
        if (received == 0)
            break;
        if (!append_file(packet, size, block, received))
            goto done;
    }
    result = TRUE;
done:
    CloseHandle(file);
    return result;
}

static BOOL read_virtual_file(DWORD sequence, char **packet, DWORD *size)
{
    IDataObject *object = NULL;
    FORMATETC format;
    STGMEDIUM medium;
    FILEGROUPDESCRIPTORW *group;
    wchar_t name[MAX_PATH];
    BOOL result = FALSE;

    if (!get_ole_clipboard || !release_medium ||
        FAILED(get_ole_clipboard(&object)))
        return FALSE;
    ZeroMemory(&format, sizeof(format));
    format.cfFormat = (CLIPFORMAT)RegisterClipboardFormatW(L"FileGroupDescriptorW");
    format.dwAspect = DVASPECT_CONTENT;
    format.lindex = -1;
    format.tymed = TYMED_HGLOBAL;
    if (FAILED(IDataObject_GetData(object, &format, &medium)))
        goto done;
    group = GlobalLock(medium.hGlobal);
    if (!group || GlobalSize(medium.hGlobal) < sizeof(FILEGROUPDESCRIPTORW) ||
        group->cItems != 1 ||
        (group->fgd[0].dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY) ||
        wcsnlen(group->fgd[0].cFileName, MAX_PATH) == MAX_PATH) {
        if (group)
            GlobalUnlock(medium.hGlobal);
        release_medium(&medium);
        goto done;
    }
    wcscpy(name, group->fgd[0].cFileName);
    GlobalUnlock(medium.hGlobal);
    release_medium(&medium);
    if (!file_header(name, packet, size))
        goto done;
    format.cfFormat = (CLIPFORMAT)RegisterClipboardFormatW(L"FileContents");
    format.lindex = 0;
    format.tymed = TYMED_ISTREAM | TYMED_HGLOBAL;
    if (FAILED(IDataObject_GetData(object, &format, &medium)))
        goto done;
    if (medium.tymed == TYMED_ISTREAM) {
        char block[65536];
        ULONG received;
        HRESULT status;

        result = TRUE;
        do {
            received = 0;
            status = IStream_Read(medium.pstm, block, sizeof(block), &received);
            if (FAILED(status) || GetClipboardSequenceNumber() != sequence ||
                !append_file(packet, size, block, received)) {
                result = FALSE;
                break;
            }
        } while (received != 0 && status == S_OK);
    } else if (medium.tymed == TYMED_HGLOBAL) {
        SIZE_T bytes = GlobalSize(medium.hGlobal);
        void *data = GlobalLock(medium.hGlobal);

        if (bytes <= UURB_CLIPBOARD_MAX_BINARY && (data || bytes == 0))
            result = append_file(packet, size, data, (DWORD)bytes);
        if (data)
            GlobalUnlock(medium.hGlobal);
    }
    release_medium(&medium);
done:
    IDataObject_Release(object);
    return result;
}

static BOOL read_clipboard_binary(DWORD sequence, char **output,
                                 DWORD *size, DWORD *kind)
{
    UINT png = RegisterClipboardFormatW(L"PNG");
    UINT format = 0;
    wchar_t path[32768];
    BOOL virtual_file = FALSE;
    BOOL result = FALSE;

    if (!OpenClipboard(NULL))
        return FALSE;
    if (GetClipboardSequenceNumber() != sequence || !owner_is_gameviewer())
        goto closed;
    if (IsClipboardFormatAvailable(png)) {
        format = png;
        *kind = UURB_CLIPBOARD_PNG;
    } else if (IsClipboardFormatAvailable(CF_DIBV5) ||
               IsClipboardFormatAvailable(CF_DIB)) {
        format = IsClipboardFormatAvailable(CF_DIBV5) ? CF_DIBV5 : CF_DIB;
        *kind = UURB_CLIPBOARD_DIB;
    }
    if (format)
        result = copy_global(GetClipboardData(format), output, size);
    else if (IsClipboardFormatAvailable(CF_HDROP)) {
        HDROP drop = (HDROP)GetClipboardData(CF_HDROP);
        if (drop && DragQueryFileW(drop, 0xFFFFFFFF, NULL, 0) == 1 &&
            DragQueryFileW(drop, 0, path, ARRAYSIZE(path)) != 0) {
            CloseClipboard();
            *kind = UURB_CLIPBOARD_FILE;
            result = read_drop_file(path, sequence, output, size);
            goto checked;
        }
    } else {
        virtual_file = IsClipboardFormatAvailable(
            RegisterClipboardFormatW(L"FileGroupDescriptorW"));
    }
closed:
    CloseClipboard();
    if (virtual_file) {
        *kind = UURB_CLIPBOARD_FILE;
        result = read_virtual_file(sequence, output, size);
    }
checked:
    return result && GetClipboardSequenceNumber() == sequence && owner_is_gameviewer();
}

static void report_clipboard_failure(const char *stage)
{
    if (diagnostic_reports++ < 64U) {
        fprintf(stderr, "controller-clipboard-failure stage=%s\n", stage);
        fflush(stderr);
    }
}

static void close_clipboard_socket(void)
{
    if (clipboard_socket != INVALID_SOCKET) {
        closesocket(clipboard_socket);
        clipboard_socket = INVALID_SOCKET;
    }
}

static BOOL socket_write_all(SOCKET socket_handle, const void *buffer, int size)
{
    const char *position = (const char *)buffer;

    while (size > 0) {
        int written = send(socket_handle, position, size, 0);

        if (written == SOCKET_ERROR || written == 0)
            return FALSE;
        position += written;
        size -= written;
    }
    return TRUE;
}

static BOOL socket_read_all(SOCKET socket_handle, void *buffer, int size)
{
    char *position = (char *)buffer;

    while (size > 0) {
        int received = recv(socket_handle, position, size, 0);

        if (received == SOCKET_ERROR || received == 0)
            return FALSE;
        position += received;
        size -= received;
    }
    return TRUE;
}

static BOOL configure_bridge(void)
{
    wchar_t port_value[16];
    wchar_t token_value[UURB_X11_CLIPBOARD_TOKEN_SIZE + 1];
    wchar_t *end = NULL;
    DWORD port_length;
    DWORD token_length;
    unsigned long parsed_port;
    DWORD index;

    port_length = GetEnvironmentVariableW(L"UURB_X11_CLIPBOARD_PORT",
                                           port_value, ARRAYSIZE(port_value));
    token_length = GetEnvironmentVariableW(L"UURB_X11_CLIPBOARD_TOKEN",
                                            token_value, ARRAYSIZE(token_value));
    if (port_length == 0 || port_length >= ARRAYSIZE(port_value) ||
        token_length != UURB_X11_CLIPBOARD_TOKEN_SIZE)
        return FALSE;
    parsed_port = wcstoul(port_value, &end, 10);
    if (end == port_value || *end != L'\0' || parsed_port == 0 ||
        parsed_port > 65535)
        return FALSE;
    for (index = 0; index < UURB_X11_CLIPBOARD_TOKEN_SIZE; index++) {
        wchar_t character = token_value[index];

        if (!((character >= L'0' && character <= L'9') ||
              (character >= L'a' && character <= L'f') ||
              (character >= L'A' && character <= L'F')))
            return FALSE;
        clipboard_token[index] = (char)character;
    }
    clipboard_token[UURB_X11_CLIPBOARD_TOKEN_SIZE] = '\0';
    clipboard_port = (unsigned short)parsed_port;
    return TRUE;
}

static BOOL connect_clipboard_listener(void)
{
    struct sockaddr_in address;
    uurb_x11_clipboard_handshake handshake;
    uurb_x11_clipboard_response response;
    DWORD timeout_ms = 1000;
    WSADATA data;

    if (clipboard_socket != INVALID_SOCKET)
        return TRUE;
    if (!winsock_initialized) {
        if (WSAStartup(MAKEWORD(2, 2), &data) != 0)
            return FALSE;
        winsock_initialized = TRUE;
    }
    clipboard_socket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    if (clipboard_socket == INVALID_SOCKET)
        return FALSE;
    setsockopt(clipboard_socket, SOL_SOCKET, SO_SNDTIMEO,
               (const char *)&timeout_ms, sizeof(timeout_ms));
    setsockopt(clipboard_socket, SOL_SOCKET, SO_RCVTIMEO,
               (const char *)&timeout_ms, sizeof(timeout_ms));
    ZeroMemory(&address, sizeof(address));
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
    address.sin_port = htons(clipboard_port);
    if (connect(clipboard_socket, (struct sockaddr *)&address,
                sizeof(address)) == SOCKET_ERROR) {
        close_clipboard_socket();
        return FALSE;
    }
    ZeroMemory(&handshake, sizeof(handshake));
    handshake.magic = UURB_X11_CLIPBOARD_MAGIC;
    handshake.version = UURB_X11_CLIPBOARD_VERSION;
    memcpy(handshake.token, clipboard_token, UURB_X11_CLIPBOARD_TOKEN_SIZE);
    if (!socket_write_all(clipboard_socket, &handshake, sizeof(handshake)) ||
        !socket_read_all(clipboard_socket, &response, sizeof(response)) ||
        response.magic != UURB_X11_CLIPBOARD_MAGIC || response.sequence != 0 ||
        response.result != 1 || response.error != 0) {
        close_clipboard_socket();
        return FALSE;
    }
    return TRUE;
}

static BOOL owner_is_gameviewer(void)
{
    HWND owner;
    DWORD process_id = 0;
    HANDLE process;
    wchar_t path[MAX_PATH];
    DWORD length = ARRAYSIZE(path);
    const wchar_t *basename;
    const wchar_t *slash_basename;

    owner = GetClipboardOwner();
    if (!owner)
        return FALSE;
    if (!GetWindowThreadProcessId(owner, &process_id) || process_id == 0)
        return FALSE;
    process = OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, FALSE, process_id);
    if (!process)
        return FALSE;
    if (!QueryFullProcessImageNameW(process, 0, path, &length)) {
        CloseHandle(process);
        return FALSE;
    }
    CloseHandle(process);
    basename = wcsrchr(path, L'\\');
    basename = basename ? basename + 1 : path;
    /* Wine can expose a Unix-style path here, while Windows uses a
     * backslash-separated DOS path.  Authorize the executable name, not one
     * platform's path spelling. */
    slash_basename = wcsrchr(basename, L'/');
    if (slash_basename)
        basename = slash_basename + 1;
    return lstrcmpiW(basename, L"GameViewer.exe") == 0;
}

static BOOL read_clipboard_utf8(DWORD expected_sequence, char **output,
                                DWORD *output_size)
{
    HANDLE handle;
    const wchar_t *source;
    SIZE_T allocation_bytes;
    SIZE_T source_units;
    SIZE_T index;
    wchar_t *normalized;
    SIZE_T normalized_units = 0;
    int bytes;
    char *result;

    *output = NULL;
    *output_size = 0;
    if (!OpenClipboard(NULL))
        return FALSE;
    /* The sequence and owner are one authorization decision.  Checking the
     * owner before OpenClipboard leaves a race where another process can take
     * the clipboard between the check and the read. */
    if (GetClipboardSequenceNumber() != expected_sequence) {
        CloseClipboard();
        return FALSE;
    }
    if (!owner_is_gameviewer()) {
        CloseClipboard();
        return FALSE;
    }
    handle = GetClipboardData(CF_UNICODETEXT);
    if (!handle) {
        CloseClipboard();
        return FALSE;
    }
    source = GlobalLock(handle);
    allocation_bytes = GlobalSize(handle);
    if (!source || allocation_bytes < sizeof(wchar_t) ||
        allocation_bytes / sizeof(wchar_t) > UURB_CLIPBOARD_MAX_UNITS) {
        if (source)
            GlobalUnlock(handle);
        CloseClipboard();
        return FALSE;
    }
    source_units = allocation_bytes / sizeof(wchar_t);
    for (index = 0; index < source_units && source[index] != L'\0'; index++)
        ;
    if (index == source_units) {
        GlobalUnlock(handle);
        CloseClipboard();
        return FALSE;
    }
    normalized = HeapAlloc(GetProcessHeap(), 0,
                           (index + 1) * sizeof(wchar_t));
    if (!normalized) {
        GlobalUnlock(handle);
        CloseClipboard();
        return FALSE;
    }
    for (source_units = 0; source_units < index; source_units++) {
        wchar_t character = source[source_units];

        if (character == L'\0') {
            HeapFree(GetProcessHeap(), 0, normalized);
            GlobalUnlock(handle);
            CloseClipboard();
            return FALSE;
        }
        if (character == L'\r') {
            normalized[normalized_units++] = L'\n';
            if (source_units + 1 < index && source[source_units + 1] == L'\n')
                source_units++;
        } else {
            normalized[normalized_units++] = character;
        }
    }
    GlobalUnlock(handle);
    if (GetClipboardSequenceNumber() != expected_sequence) {
        CloseClipboard();
        HeapFree(GetProcessHeap(), 0, normalized);
        return FALSE;
    }
    if (!owner_is_gameviewer()) {
        CloseClipboard();
        HeapFree(GetProcessHeap(), 0, normalized);
        return FALSE;
    }
    CloseClipboard();
    if (normalized_units == 0) {
        HeapFree(GetProcessHeap(), 0, normalized);
        return FALSE;
    }
    bytes = WideCharToMultiByte(CP_UTF8, WC_ERR_INVALID_CHARS, normalized,
                                (int)normalized_units, NULL, 0, NULL, NULL);
    if (bytes <= 0 || (DWORD)bytes > UURB_X11_CLIPBOARD_MAX_TEXT_BYTES) {
        HeapFree(GetProcessHeap(), 0, normalized);
        return FALSE;
    }
    result = HeapAlloc(GetProcessHeap(), 0, (SIZE_T)bytes);
    if (!result || WideCharToMultiByte(CP_UTF8, WC_ERR_INVALID_CHARS,
                                       normalized, (int)normalized_units,
                                       result, bytes, NULL, NULL) != bytes) {
        if (result)
            HeapFree(GetProcessHeap(), 0, result);
        HeapFree(GetProcessHeap(), 0, normalized);
        return FALSE;
    }
    HeapFree(GetProcessHeap(), 0, normalized);
    *output = result;
    *output_size = (DWORD)bytes;
    return TRUE;
}

static BOOL forward_current_clipboard(DWORD sequence)
{
    uurb_x11_clipboard_request request;
    uurb_x11_clipboard_response response;
    char *text = NULL;
    DWORD text_size;
    DWORD kind = 0;
    BOOL sent = FALSE;

    if (!extended_clipboard || !read_clipboard_binary(sequence, &text, &text_size, &kind)) {
        if (text)
            HeapFree(GetProcessHeap(), 0, text);
        text = NULL;
        kind = 0;
        if (!read_clipboard_utf8(sequence, &text, &text_size))
            return FALSE;
    }
    if (!connect_clipboard_listener()) {
        report_clipboard_failure("connect");
        goto cleanup;
    }
    request.magic = UURB_X11_CLIPBOARD_MAGIC;
    request.sequence = sequence;
    request.text_bytes = text_size;
    request.reserved = kind;
    if (!socket_write_all(clipboard_socket, &request, sizeof(request)) ||
        !socket_write_all(clipboard_socket, text, (int)text_size) ||
        !socket_read_all(clipboard_socket, &response, sizeof(response)) ||
        response.magic != UURB_X11_CLIPBOARD_MAGIC ||
        response.sequence != sequence || response.result != text_size ||
        response.error != 0) {
        report_clipboard_failure("native-owner");
        close_clipboard_socket();
        goto cleanup;
    }
    sent = TRUE;

cleanup:
    HeapFree(GetProcessHeap(), 0, text);
    return sent;
}

static BOOL receive_host_image(void)
{
    uurb_x11_clipboard_request request = {
        UURB_X11_CLIPBOARD_MAGIC, 0, 0, UURB_CLIPBOARD_GET_IMAGE};
    uurb_x11_clipboard_response response;
    HGLOBAL v5 = NULL, dib = NULL;
    char *data;
    BITMAPINFOHEADER *header;
    BOOL result = FALSE;

    if (!connect_clipboard_listener())
        return FALSE;
    if (!socket_write_all(clipboard_socket, &request, sizeof(request)) ||
        !socket_read_all(clipboard_socket, &response, sizeof(response)) ||
        response.magic != UURB_X11_CLIPBOARD_MAGIC || response.error != 0 ||
        response.result > UURB_CLIPBOARD_MAX_BINARY) {
        close_clipboard_socket();
        return FALSE;
    }
    if (!response.result)
        return FALSE;
    v5 = GlobalAlloc(GMEM_MOVEABLE, response.result);
    data = v5 ? GlobalLock(v5) : NULL;
    if (!data || !socket_read_all(clipboard_socket, data, (int)response.result) ||
        response.result < 124 || *(DWORD *)data != 124) {
        if (data)
            GlobalUnlock(v5);
        close_clipboard_socket();
        goto done;
    }
    dib = GlobalAlloc(GMEM_MOVEABLE, response.result - 124 + 40);
    header = dib ? GlobalLock(dib) : NULL;
    if (!header) {
        GlobalUnlock(v5);
        goto done;
    }
    memcpy(header, data, 40);
    header->biSize = 40;
    header->biCompression = BI_RGB;
    memcpy((char *)header + 40, data + 124, response.result - 124);
    GlobalUnlock(dib);
    GlobalUnlock(v5);
    if (!OpenClipboard(image_owner))
        goto done;
    if (EmptyClipboard()) {
        if (SetClipboardData(CF_DIBV5, v5)) {
            v5 = NULL;
            result = TRUE;
        }
        if (SetClipboardData(CF_DIB, dib))
            dib = NULL;
    }
    CloseClipboard();
done:
    if (v5)
        GlobalFree(v5);
    if (dib)
        GlobalFree(dib);
    return result;
}

int wmain(void)
{
    DWORD delivered_sequence;
    wchar_t extended[4];
    HMODULE ole;
    MSG message;
    union {
        FARPROC address;
        HRESULT (WINAPI *initialize)(void *);
        HRESULT (WINAPI *get)(IDataObject **);
        void (WINAPI *release)(STGMEDIUM *);
    } method;

    if (!configure_bridge())
        return 2;
    extended_clipboard = GetEnvironmentVariableW(L"UURB_CLIPBOARD_EXTENDED",
        extended, ARRAYSIZE(extended)) == 1 && extended[0] == L'1';
    if (extended_clipboard) {
        image_owner = CreateWindowExW(0, L"STATIC", L"UU bitmap clipboard",
            0, 0, 0, 0, 0, HWND_MESSAGE, NULL, GetModuleHandleW(NULL), NULL);
        if (!image_owner)
            return 3;
        ole = LoadLibraryW(L"ole32.dll");
        if (ole) {
            method.address = GetProcAddress(ole, "OleInitialize");
            if (method.address && SUCCEEDED(method.initialize(NULL))) {
                method.address = GetProcAddress(ole, "OleGetClipboard");
                get_ole_clipboard = method.get;
                method.address = GetProcAddress(ole, "ReleaseStgMedium");
                release_medium = method.release;
            }
        }
    }
    /* Do not replay whatever happened to be in GameViewer's clipboard before
     * this helper was started.  Only sequence changes observed after startup
     * are eligible for forwarding. */
    delivered_sequence = GetClipboardSequenceNumber();
    fprintf(stderr,
            "Wine clipboard companion ready; extended=%u.\n", extended_clipboard);
    fflush(stderr);
    for (;;) {
        DWORD sequence = GetClipboardSequenceNumber();

        if (sequence != 0 && sequence != delivered_sequence &&
            forward_current_clipboard(sequence))
            delivered_sequence = sequence;
        if (extended_clipboard && receive_host_image())
            delivered_sequence = GetClipboardSequenceNumber();
        while (PeekMessageW(&message, NULL, 0, 0, PM_REMOVE)) {
            TranslateMessage(&message);
            DispatchMessageW(&message);
        }
        Sleep(UURB_CLIPBOARD_POLL_MS);
    }
}
