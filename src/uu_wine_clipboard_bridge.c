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

static BOOL read_clipboard_binary(DWORD sequence, char **output,
                                 DWORD *size, DWORD *kind)
{
    UINT png = RegisterClipboardFormatW(L"PNG");
    UINT format = 0;
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
        /* Wine can retain a synthesized V5 after the owner's original DIB
         * changes. Preserve the publication order rather than prefer it. */
        for (UINT candidate = EnumClipboardFormats(0); candidate;
             candidate = EnumClipboardFormats(candidate)) {
            if (candidate == CF_DIB || candidate == CF_DIBV5) {
                format = candidate;
                break;
            }
        }
        *kind = UURB_CLIPBOARD_DIB;
    }
    if (format)
        result = copy_global(GetClipboardData(format), output, size);
closed:
    CloseClipboard();
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
    BOOL no_delay = TRUE;
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
    setsockopt(clipboard_socket, IPPROTO_TCP, TCP_NODELAY,
               (const char *)&no_delay, sizeof(no_delay));
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

typedef struct clipboard_file {
    wchar_t name[MAX_PATH];
    wchar_t *path;
    ULONGLONG size;
    BOOL known;
} clipboard_file;

static BOOL send_clipboard_packet(DWORD sequence, DWORD kind,
                                  const void *data, DWORD size)
{
    uurb_x11_clipboard_request request = {
        UURB_X11_CLIPBOARD_MAGIC, sequence, size, kind};
    uurb_x11_clipboard_response response;

    if (!connect_clipboard_listener())
        return FALSE;
    if (!socket_write_all(clipboard_socket, &request, sizeof(request)) ||
        !socket_write_all(clipboard_socket, data, (int)size) ||
        !socket_read_all(clipboard_socket, &response, sizeof(response)) ||
        response.magic != UURB_X11_CLIPBOARD_MAGIC ||
        response.sequence != sequence || response.result != size || response.error) {
        close_clipboard_socket();
        return FALSE;
    }
    return TRUE;
}

static BOOL send_file_block(DWORD sequence, DWORD index, const void *data,
                            DWORD size, ULONGLONG *received, ULONGLONG *batch)
{
    char packet[sizeof(DWORD) + UURB_CLIPBOARD_FILE_BLOCK];

    if (GetClipboardSequenceNumber() != sequence || !owner_is_gameviewer() ||
        *received + size > UURB_CLIPBOARD_MAX_BINARY ||
        *batch + size > UURB_CLIPBOARD_MAX_BATCH)
        return FALSE;
    memcpy(packet, &index, sizeof(index));
    memcpy(packet + sizeof(index), data, size);
    if (!send_clipboard_packet(sequence, UURB_CLIPBOARD_FILE_CHUNK,
                              packet, sizeof(index) + size))
        return FALSE;
    *received += size;
    *batch += size;
    return TRUE;
}

static BOOL stream_drop_file(const clipboard_file *entry, DWORD sequence,
                             DWORD index, ULONGLONG *batch)
{
    HANDLE file = CreateFileW(entry->path, GENERIC_READ, FILE_SHARE_READ, NULL,
                              OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);
    char block[UURB_CLIPBOARD_FILE_BLOCK];
    DWORD size;
    ULONGLONG received = 0;
    BOOL result = FALSE;

    if (file == INVALID_HANDLE_VALUE)
        return FALSE;
    for (;;) {
        if (GetClipboardSequenceNumber() != sequence ||
            !ReadFile(file, block, sizeof(block), &size, NULL))
            break;
        if (!size) {
            result = !entry->known || received == entry->size;
            break;
        }
        if (!send_file_block(sequence, index, block, size, &received, batch))
            break;
    }
    CloseHandle(file);
    return result;
}

static BOOL stream_virtual_file(IDataObject *object, DWORD sequence,
                                DWORD index, ULONGLONG *batch)
{
    FORMATETC format;
    STGMEDIUM medium;
    ULONGLONG received = 0;
    BOOL result = FALSE;

    ZeroMemory(&format, sizeof(format));
    format.cfFormat = (CLIPFORMAT)RegisterClipboardFormatW(L"FileContents");
    format.dwAspect = DVASPECT_CONTENT;
    format.lindex = (LONG)index;
    format.tymed = TYMED_ISTREAM | TYMED_HGLOBAL;
    if (FAILED(IDataObject_GetData(object, &format, &medium)))
        return FALSE;
    if (medium.tymed == TYMED_ISTREAM) {
        char block[UURB_CLIPBOARD_FILE_BLOCK];
        HRESULT status;
        ULONG size;

        for (;;) {
            size = 0;
            status = IStream_Read(medium.pstm, block, sizeof(block), &size);
            if (FAILED(status) || GetClipboardSequenceNumber() != sequence)
                break;
            if (size && !send_file_block(sequence, index, block, size, &received, batch))
                break;
            if (!size || status == S_FALSE) {
                result = TRUE;
                break;
            }
        }
    } else if (medium.tymed == TYMED_HGLOBAL) {
        SIZE_T size = GlobalSize(medium.hGlobal);
        char *data = GlobalLock(medium.hGlobal);

        if (size <= UURB_CLIPBOARD_MAX_BINARY && (data || !size)) {
            result = TRUE;
            for (DWORD offset = 0; offset < size;) {
                DWORD block = (DWORD)(size - offset);
                if (block > UURB_CLIPBOARD_FILE_BLOCK)
                    block = UURB_CLIPBOARD_FILE_BLOCK;
                if (!send_file_block(sequence, index, data + offset, block, &received, batch)) {
                    result = FALSE;
                    break;
                }
                offset += block;
            }
        }
        if (data)
            GlobalUnlock(medium.hGlobal);
    }
    release_medium(&medium);
    return result;
}

/* Return zero only when this is not a file offer. Consume failed file offers
 * too, so a rejected batch neither becomes filename text nor retries forever. */
static int forward_clipboard_files(DWORD sequence)
{
    clipboard_file *files = NULL;
    IDataObject *object = NULL;
    DWORD count = 0, index, length = sizeof(DWORD);
    ULONGLONG batch = 0;
    char *manifest = NULL;
    BOOL offered = FALSE, drop_offer = FALSE, success = FALSE;
    const char *failure = "File transfer failed or source copy changed";

    if (!OpenClipboard(NULL))
        return 0;
    if (GetClipboardSequenceNumber() != sequence || !owner_is_gameviewer()) {
        CloseClipboard();
        return 0;
    }
    drop_offer = IsClipboardFormatAvailable(CF_HDROP);
    offered = drop_offer || IsClipboardFormatAvailable(
        RegisterClipboardFormatW(L"FileGroupDescriptorW"));
    if (!offered) {
        CloseClipboard();
        return 0;
    }
    files = HeapAlloc(GetProcessHeap(), HEAP_ZERO_MEMORY,
                      UURB_CLIPBOARD_MAX_FILES * sizeof(*files));
    if (!files) {
        CloseClipboard();
        goto done;
    }
    if (drop_offer) {
        HDROP drop = (HDROP)GetClipboardData(CF_HDROP);
        count = drop ? DragQueryFileW(drop, 0xFFFFFFFF, NULL, 0) : 0;
        if (!count || count > UURB_CLIPBOARD_MAX_FILES) {
            failure = "A copy supports 1 to 64 files";
            CloseClipboard();
            goto done;
        }
        for (index = 0; index < count; index++) {
            UINT units = DragQueryFileW(drop, index, NULL, 0);
            const wchar_t *name, *slash;
            WIN32_FILE_ATTRIBUTE_DATA attributes;

            if (!units || units > 32767) {
                CloseClipboard();
                goto done;
            }
            files[index].path = HeapAlloc(GetProcessHeap(), 0, (units + 1) * sizeof(wchar_t));
            if (!files[index].path || !DragQueryFileW(drop, index, files[index].path, units + 1)) {
                CloseClipboard();
                goto done;
            }
            name = wcsrchr(files[index].path, L'\\');
            name = name ? name + 1 : files[index].path;
            slash = wcsrchr(files[index].path, L'/');
            if (slash && slash + 1 > name)
                name = slash + 1;
            if (wcslen(name) >= MAX_PATH ||
                !GetFileAttributesExW(files[index].path, GetFileExInfoStandard, &attributes) ||
                (attributes.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY)) {
                failure = "Folders are not supported; copy individual files";
                CloseClipboard();
                goto done;
            }
            wcscpy(files[index].name, name);
            files[index].known = TRUE;
            files[index].size = ((ULONGLONG)attributes.nFileSizeHigh << 32) | attributes.nFileSizeLow;
        }
        CloseClipboard();
    } else {
        FORMATETC format;
        STGMEDIUM medium;
        FILEGROUPDESCRIPTORW *group;
        CloseClipboard();
        if (!get_ole_clipboard || !release_medium || FAILED(get_ole_clipboard(&object)))
            goto done;
        ZeroMemory(&format, sizeof(format));
        format.cfFormat = (CLIPFORMAT)RegisterClipboardFormatW(L"FileGroupDescriptorW");
        format.dwAspect = DVASPECT_CONTENT;
        format.lindex = -1;
        format.tymed = TYMED_HGLOBAL;
        if (FAILED(IDataObject_GetData(object, &format, &medium)))
            goto done;
        group = GlobalLock(medium.hGlobal);
        if (group && GlobalSize(medium.hGlobal) >= sizeof(UINT))
            count = group->cItems;
        if (!group || !count || count > UURB_CLIPBOARD_MAX_FILES ||
            GlobalSize(medium.hGlobal) < sizeof(UINT) + (SIZE_T)count * sizeof(FILEDESCRIPTORW)) {
            if (group)
                GlobalUnlock(medium.hGlobal);
            release_medium(&medium);
            count = 0;
            failure = "Invalid file descriptors; a copy supports up to 64 files";
            goto done;
        }
        for (index = 0; index < count; index++) {
            FILEDESCRIPTORW *entry = &group->fgd[index];
            if ((entry->dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY) ||
                wcsnlen(entry->cFileName, MAX_PATH) == MAX_PATH)
                break;
            wcscpy(files[index].name, entry->cFileName);
            files[index].known = (entry->dwFlags & FD_FILESIZE) != 0;
            files[index].size = ((ULONGLONG)entry->nFileSizeHigh << 32) | entry->nFileSizeLow;
        }
        GlobalUnlock(medium.hGlobal);
        release_medium(&medium);
        if (index != count)
            goto done;
    }
    manifest = HeapAlloc(GetProcessHeap(), 0, 4 + count * (12 + 256));
    if (!manifest)
        goto done;
    memcpy(manifest, &count, 4);
    for (index = 0; index < count; index++) {
        int bytes = WideCharToMultiByte(CP_UTF8, WC_ERR_INVALID_CHARS,
            files[index].name, -1, NULL, 0, NULL, NULL);
        DWORD name_bytes;
        LONGLONG size = files[index].known ? (LONGLONG)files[index].size : -1;
        if (bytes <= 1 || bytes > 256) {
            failure = "Invalid filename or basename exceeds 255 UTF-8 bytes";
            goto done;
        }
        if (files[index].known) {
            batch += files[index].size;
            if (files[index].size > UURB_CLIPBOARD_MAX_BINARY || batch > UURB_CLIPBOARD_MAX_BATCH) {
                failure = "Each file is limited to 64 MiB; a copy to 256 MiB";
                goto done;
            }
        }
        name_bytes = (DWORD)bytes - 1;
        memcpy(manifest + length, &name_bytes, 4);
        memcpy(manifest + length + 4, &size, 8);
        WideCharToMultiByte(CP_UTF8, WC_ERR_INVALID_CHARS, files[index].name, -1,
                            manifest + length + 12, bytes, NULL, NULL);
        length += 12 + name_bytes;
    }
    if (GetClipboardSequenceNumber() != sequence || !owner_is_gameviewer() ||
        !send_clipboard_packet(sequence, UURB_CLIPBOARD_FILE_BEGIN, manifest, length))
        goto done;
    batch = 0;
    for (index = 0; index < count; index++) {
        if (!(drop_offer ? stream_drop_file(&files[index], sequence, index, &batch) :
                         stream_virtual_file(object, sequence, index, &batch)) ||
            GetClipboardSequenceNumber() != sequence || !owner_is_gameviewer() ||
            !send_clipboard_packet(sequence, UURB_CLIPBOARD_FILE_END, &index, sizeof(index)))
            goto done;
    }
    success = TRUE;
done:
    if (!success) {
        send_clipboard_packet(sequence, UURB_CLIPBOARD_FILE_ABORT, failure, (DWORD)strlen(failure));
        report_clipboard_failure("file-transfer");
    }
    if (object)
        IDataObject_Release(object);
    if (files) {
        for (index = 0; index < count && index < UURB_CLIPBOARD_MAX_FILES; index++)
            if (files[index].path)
                HeapFree(GetProcessHeap(), 0, files[index].path);
        HeapFree(GetProcessHeap(), 0, files);
    }
    if (manifest)
        HeapFree(GetProcessHeap(), 0, manifest);
    return 1;
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
    char *text = NULL;
    DWORD text_size;
    DWORD kind = 0;
    BOOL sent = FALSE;

    if (extended_clipboard && forward_clipboard_files(sequence))
        return TRUE;

    if (!extended_clipboard || !read_clipboard_binary(sequence, &text, &text_size, &kind)) {
        if (text)
            HeapFree(GetProcessHeap(), 0, text);
        text = NULL;
        kind = 0;
        if (!read_clipboard_utf8(sequence, &text, &text_size))
            return FALSE;
    }
    sent = send_clipboard_packet(sequence, kind, text, text_size);
    if (!sent)
        report_clipboard_failure("native-owner");
    HeapFree(GetProcessHeap(), 0, text);
    return sent;
}

static BOOL receive_host_clipboard(void)
{
    uurb_x11_clipboard_request request = {
        UURB_X11_CLIPBOARD_MAGIC, 0, 0, UURB_CLIPBOARD_GET_HOST};
    uurb_x11_clipboard_response response;
    HGLOBAL v5 = NULL, dib = NULL;
    char *packet = NULL, *data;
    DWORD kind, size;
    UINT format;
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
    packet = HeapAlloc(GetProcessHeap(), 0, response.result);
    if (!packet || !socket_read_all(clipboard_socket, packet, (int)response.result) ||
        response.result <= sizeof(DWORD)) {
        close_clipboard_socket();
        goto done;
    }
    memcpy(&kind, packet, sizeof(kind));
    size = response.result - sizeof(kind);
    data = packet + sizeof(kind);
    if (kind == 0) {
        int units;
        wchar_t *text;
        if (size > UURB_X11_CLIPBOARD_MAX_TEXT_BYTES)
            goto done;
        units = MultiByteToWideChar(CP_UTF8, MB_ERR_INVALID_CHARS, data, size, NULL, 0);
        if (units <= 0)
            goto done;
        v5 = GlobalAlloc(GMEM_MOVEABLE, ((SIZE_T)units + 1) * sizeof(wchar_t));
        text = v5 ? GlobalLock(v5) : NULL;
        if (!text)
            goto done;
        MultiByteToWideChar(CP_UTF8, MB_ERR_INVALID_CHARS, data, size, text, units);
        text[units] = L'\0';
        GlobalUnlock(v5);
        format = CF_UNICODETEXT;
    } else if (kind == UURB_CLIPBOARD_DIB && size >= 124 && *(DWORD *)data == 124) {
        void *pixels;
        v5 = GlobalAlloc(GMEM_MOVEABLE, size);
        pixels = v5 ? GlobalLock(v5) : NULL;
        if (!pixels)
            goto done;
        memcpy(pixels, data, size);
        GlobalUnlock(v5);
        dib = GlobalAlloc(GMEM_MOVEABLE, size - 124 + 40);
        header = dib ? GlobalLock(dib) : NULL;
        if (!header)
            goto done;
        memcpy(header, data, 40);
        header->biSize = 40;
        header->biCompression = BI_RGB;
        memcpy((char *)header + 40, data + 124, size - 124);
        GlobalUnlock(dib);
        format = CF_DIBV5;
    } else {
        goto done;
    }
    if (!OpenClipboard(image_owner))
        goto done;
    if (EmptyClipboard()) {
        if (SetClipboardData(format, v5)) {
            v5 = NULL;
            result = TRUE;
        }
        if (dib && SetClipboardData(CF_DIB, dib))
            dib = NULL;
    }
    CloseClipboard();
done:
    if (packet)
        HeapFree(GetProcessHeap(), 0, packet);
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
        image_owner = CreateWindowExW(0, L"STATIC", L"UU native clipboard",
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
        if (extended_clipboard && receive_host_clipboard())
            delivered_sequence = GetClipboardSequenceNumber();
        while (PeekMessageW(&message, NULL, 0, 0, PM_REMOVE)) {
            TranslateMessage(&message);
            DispatchMessageW(&message);
        }
        Sleep(UURB_CLIPBOARD_POLL_MS);
    }
}
