/* Capture-only adaptation of panxuc/uur, MIT; see LICENSE and SOURCE.json.
 * Shares the Plus input/clipboard/terminal base; no input hooks are installed. */
#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <tlhelp32.h>
#include <dxgi.h>
#include <dxgi1_2.h>
#include <d3d11.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "cursor-overlay.h"
#include "frame-protocol.h"
static HRESULT(WINAPI *original_create_dxgi_factory1)(REFIID, void **);
static FARPROC(WINAPI *original_get_proc_address)(HMODULE, LPCSTR);
UINT WINAPI hook_send_input(UINT count, LPINPUT inputs, int size);

static volatile LONG dxgi_factories_patched = 0;
static volatile LONG dxgi_adapters_patched = 0;
static volatile LONG dxgi_outputs_patched = 0;
static volatile LONG dxgi_duplicate_calls = 0;
static volatile LONG dxgi_native_success = 0;
static volatile LONG dxgi_native_errors = 0;
static volatile LONG dxgi_dup_acquires = 0;
static volatile LONG dxgi_dup_frames = 0;

/* ---- DXGI duplication disable ----------------------------------------- */

/* The client's primary capture is IDXGIOutput1::DuplicateOutput.  Wine's
 * implementation succeeds but only delivers the empty XWayland desktop
 * (black video).  Forcing DuplicateOutput to fail makes the client fall
 * back to its GDI capture path, which the frame feed below supplies. */

static const GUID uur_iid_idxgioutput1 = {
    0x00cddea8, 0x939b, 0x4b83,
    {0xa3, 0x40, 0xa6, 0x85, 0x22, 0x66, 0x66, 0xcc}
};

/* Minimal IDXGIOutput1 shape: mingw's C-mode dxgi.h lacks it.  The
 * vtable is IUnknown(3) + IDXGIOutput(12) methods, then DuplicateOutput. */
typedef struct uur_idxgioutput1_vtbl {
    void *methods[15];
    HRESULT(STDMETHODCALLTYPE *DuplicateOutput)(void *, IUnknown *, IDXGIOutputDuplication **);
} uur_idxgioutput1_vtbl;
typedef struct uur_idxgioutput1 {
    uur_idxgioutput1_vtbl *lpVtbl;
} uur_idxgioutput1;

#ifndef DXGI_ERROR_UNSUPPORTED
#define DXGI_ERROR_UNSUPPORTED ((HRESULT)0x887A0004)
#endif

static HRESULT(STDMETHODCALLTYPE *original_dxgi_enum_adapters1)(
    IDXGIFactory1 *factory, UINT index, IDXGIAdapter1 **adapter) = NULL;
static HRESULT(STDMETHODCALLTYPE *original_dxgi_enum_outputs)(
    IDXGIAdapter *adapter, UINT index, IDXGIOutput **output) = NULL;
static HRESULT STDMETHODCALLTYPE hook_dxgi_enum_adapters1(
    IDXGIFactory1 *factory, UINT index, IDXGIAdapter1 **adapter);
static HRESULT STDMETHODCALLTYPE hook_dxgi_enum_outputs(
    IDXGIAdapter *adapter, UINT index, IDXGIOutput **output);
static HRESULT WINAPI hook_dxgi_duplicate_output(uur_idxgioutput1 *output,
                                                 IUnknown *device, IDXGIOutputDuplication **capture);

static int patch_vtable_slot(void **slot, void *hook, void **original)
{
    DWORD old_protect = 0;
    if (*slot == hook)
        return 1;
    if (original != NULL)
        *original = *slot;
    if (!VirtualProtect(slot, sizeof(void *), PAGE_READWRITE, &old_protect))
        return 0;
    *slot = hook;
    VirtualProtect(slot, sizeof(void *), old_protect, &old_protect);
    return 1;
}

static HRESULT(STDMETHODCALLTYPE *original_dxgi_enum_adapters)(
    IDXGIFactory *factory, UINT index, IDXGIAdapter **adapter) = NULL;
static void patch_dxgi_adapter(IDXGIAdapter *adapter);

static void patch_dxgi_output(IDXGIOutput *output)
{
    uur_idxgioutput1 *output1 = NULL;

    if (output == NULL || output->lpVtbl == NULL)
        return;
    if (output->lpVtbl->QueryInterface(
            output, &uur_iid_idxgioutput1, (void **)&output1) != S_OK)
        return;
    if (output1 != NULL && output1->lpVtbl != NULL) {
        if (patch_vtable_slot((void **)&output1->lpVtbl->DuplicateOutput,
                              (void *)hook_dxgi_duplicate_output, NULL)) {
            InterlockedIncrement(&dxgi_outputs_patched);
        }
        /* release through the known-good base interface */
        output->lpVtbl->Release(output);
    }
}

static HRESULT STDMETHODCALLTYPE hook_dxgi_enum_adapters(
    IDXGIFactory *factory, UINT index, IDXGIAdapter **adapter)
{
    HRESULT result = original_dxgi_enum_adapters
        ? original_dxgi_enum_adapters(factory, index, adapter)
        : DXGI_ERROR_INVALID_CALL;

    if (result == S_OK && adapter != NULL && *adapter != NULL)
        patch_dxgi_adapter(*adapter);
    return result;
}

static void patch_dxgi_adapter(IDXGIAdapter *adapter)
{
    if (adapter == NULL || adapter->lpVtbl == NULL)
        return;
    if (patch_vtable_slot((void **)&adapter->lpVtbl->EnumOutputs,
                          (void *)hook_dxgi_enum_outputs,
                          (void **)&original_dxgi_enum_outputs)) {
        InterlockedIncrement(&dxgi_adapters_patched);
    }
}

static HRESULT STDMETHODCALLTYPE hook_dxgi_enum_adapters1(
    IDXGIFactory1 *factory, UINT index, IDXGIAdapter1 **adapter)
{
    HRESULT result = original_dxgi_enum_adapters1
        ? original_dxgi_enum_adapters1(factory, index, adapter)
        : DXGI_ERROR_INVALID_CALL;

    if (result == S_OK && adapter != NULL && *adapter != NULL)
        patch_dxgi_adapter((IDXGIAdapter *)*adapter);
    return result;
}

static HRESULT STDMETHODCALLTYPE hook_dxgi_enum_outputs(
    IDXGIAdapter *adapter, UINT index, IDXGIOutput **output)
{
    HRESULT result = original_dxgi_enum_outputs
        ? original_dxgi_enum_outputs(adapter, index, output)
        : DXGI_ERROR_INVALID_CALL;

    if (result == S_OK && output != NULL && *output != NULL)
        patch_dxgi_output(*output);
    return result;
}

static HRESULT WINAPI hook_dxgi_duplicate_output(uur_idxgioutput1 *output,
                                                 IUnknown *device, IDXGIOutputDuplication **capture)
{
#ifdef UURB_NATIVE_GPU
    char endpoint[108];
    WCHAR loader[32768];
    if (!capture) return E_INVALIDARG;
    *capture = NULL;
    if (!GetEnvironmentVariableA("UURB_NATIVE_GPU_SOCKET", endpoint, sizeof(endpoint)) ||
        !GetEnvironmentVariableW(L"UURB_NATIVE_GPU_LOADER", loader, 32768)) return DXGI_ERROR_UNSUPPORTED;
    HMODULE backend = LoadLibraryW(loader);
    if (!backend) return DXGI_ERROR_UNSUPPORTED;
    union { FARPROC address; HRESULT (WINAPI *create)(ID3D11Device *, const char *, IUnknown *, IDXGIOutputDuplication **); } method;
    method.address = original_get_proc_address(backend, "UurbCreateDuplicationEndpoint");
    if (!method.address) return DXGI_ERROR_UNSUPPORTED;
    InterlockedIncrement(&dxgi_duplicate_calls);
    HRESULT result = method.create((ID3D11Device *)device, endpoint, (IUnknown *)output, capture);
    InterlockedIncrement(SUCCEEDED(result) ? &dxgi_native_success : &dxgi_native_errors);
    return result;
#else
    (void)output;
    (void)device;
    (void)capture;
    InterlockedIncrement(&dxgi_duplicate_calls);
    /* Wine's duplication succeeds but delivers the empty XWayland desktop.
     * Failing it sends the client to its GDI capture path. */
    return DXGI_ERROR_UNSUPPORTED;
#endif
}

static void patch_dxgi_factory(IDXGIFactory1 *factory)
{
    if (factory == NULL || factory->lpVtbl == NULL)
        return;
    patch_vtable_slot((void **)&factory->lpVtbl->EnumAdapters1,
                      (void *)hook_dxgi_enum_adapters1,
                      (void **)&original_dxgi_enum_adapters1);
    patch_vtable_slot((void **)&factory->lpVtbl->EnumAdapters,
                      (void *)hook_dxgi_enum_adapters,
                      (void **)&original_dxgi_enum_adapters);
}

static HRESULT WINAPI hook_create_dxgi_factory1(REFIID interface_id,
                                                void **factory)
{
    HRESULT result = original_create_dxgi_factory1 != NULL
        ? original_create_dxgi_factory1(interface_id, factory)
        : DXGI_ERROR_INVALID_CALL;

    if (result == S_OK && factory != NULL && *factory != NULL) {
        IDXGIFactory1 *f = (IDXGIFactory1 *)*factory;
        if (f->lpVtbl != NULL) {
            patch_dxgi_factory(f);
            InterlockedIncrement(&dxgi_factories_patched);
        }
    }
    return result;
}
static BOOL(WINAPI *original_bit_blt)(HDC, int, int, int, int, HDC, int, int,
                                      DWORD);
static BOOL(WINAPI *original_stretch_blt)(HDC, int, int, int, int, HDC, int,
                                          int, int, int, DWORD);
static volatile LONG capture_calls = 0;
static volatile LONG capture_rendered = 0;
static volatile LONG capture_fallbacks = 0;
static volatile LONG iat_hooks_installed = 0;

/* ---- capture frame feed (docs/capture-protocol.md) -------------------- */

static void *frame_map = NULL;
static HANDLE frame_map_handle = NULL;
static uint32_t frame_width;
static uint32_t frame_height;
static uint32_t frame_stride;
static uint64_t frame_slot_bytes;
static unsigned char *frame_snapshot;
static size_t frame_snapshot_capacity;
static size_t frame_map_size;
static SRWLOCK capture_lock = SRWLOCK_INIT;

static char *read_ini_value(const char *path, const char *key);

static int resolve_frame_path(WCHAR *path, int capacity)
{
    DWORD count = GetEnvironmentVariableW(L"UURB_NATIVE_FRAME_PATH", path,
                                          (DWORD)capacity);
    if (count > 0 && count < (DWORD)capacity)
        return 1;

    char *utf8 = read_ini_value("C:\\uurb-native-video.ini", "frame_path");
    if (utf8 == NULL)
        return 0;
    int converted = MultiByteToWideChar(CP_UTF8, MB_ERR_INVALID_CHARS, utf8,
                                        -1, path, capacity);
    free(utf8);
    return converted > 0;
}

static uint32_t load_u32(const unsigned char *p)
{
    return (uint32_t)p[0] | ((uint32_t)p[1] << 8) | ((uint32_t)p[2] << 16) |
           ((uint32_t)p[3] << 24);
}

static uint64_t load_u64(const unsigned char *p)
{
    return load_u32(p) | ((uint64_t)load_u32(p + 4) << 32);
}

/* Open (or re-open after a resolution change) the capture file that the
 * native uur-pw-capture helper publishes. */
static int ensure_frame_map(void)
{
    HANDLE file;
    void *view;
    const unsigned char *header;
    LARGE_INTEGER size;
    WCHAR path[32768];

    if (frame_map != NULL)
        return 1;

    if (!resolve_frame_path(path, (int)(sizeof(path) / sizeof(path[0]))))
        return 0;
    file = CreateFileW(path, GENERIC_READ,
                       FILE_SHARE_READ | FILE_SHARE_WRITE, NULL, OPEN_EXISTING,
                       0, NULL);
    if (file == INVALID_HANDLE_VALUE)
        return 0;
    if (!GetFileSizeEx(file, &size) || size.QuadPart < UURF_HEADER_BYTES ||
        (uint64_t)size.QuadPart > SIZE_MAX) {
        CloseHandle(file);
        return 0;
    }
    frame_map_handle = CreateFileMappingW(file, NULL, PAGE_READONLY, 0, 0,
                                          NULL);
    CloseHandle(file);
    if (frame_map_handle == NULL)
        return 0;
    view = MapViewOfFile(frame_map_handle, FILE_MAP_READ, 0, 0, 0);
    if (view == NULL)
        return 0;

    header = (const unsigned char *)view;
    if (load_u32(header) != UURF_MAGIC ||
        load_u32(header + 4) != UURF_VERSION || load_u32(header + 20) != 1u) {
        UnmapViewOfFile(view);
        CloseHandle(frame_map_handle);
        frame_map_handle = NULL;
        return 0;
    }
    frame_width = load_u32(header + 8);
    frame_height = load_u32(header + 12);
    frame_stride = load_u32(header + 16);
    frame_slot_bytes = 8ull + (uint64_t)frame_stride * frame_height;
    uint64_t expected = UURF_HEADER_BYTES + UURF_SLOT_COUNT * frame_slot_bytes;
    if (frame_width == 0 || frame_height == 0 || frame_stride < frame_width * 4 ||
        expected > (uint64_t)size.QuadPart) {
        UnmapViewOfFile(view);
        CloseHandle(frame_map_handle);
        frame_map_handle = NULL;
        return 0;
    }
    frame_map_size = (size_t)size.QuadPart;
    frame_map = view;
    return 1;
}

static BOOL source_is_screen_dc(HDC source)
{
    return GetObjectType(source) == OBJ_DC &&
           GetDeviceCaps(source, TECHNOLOGY) == DT_RASDISPLAY;
}

/* GDI screen captures do not include the X11 hardware cursor.  Keep the
 * cursor visible in the fallback path used on X11 by compositing Wine's
 * current cursor onto the capture destination after the desktop blit. */
static void draw_cursor_overlay(HDC hdc_dest, int x, int y, int width, int height,
                                int source_x, int source_y, int source_width,
                                int source_height)
{
    CURSORINFO cursor;
    ICONINFO icon;
    BITMAP mask;
    POINT position;
    uur_cursor_rect source = {source_x, source_y, source_width, source_height};
    uur_cursor_rect destination = {x, y, width, height};
    uur_cursor_rect overlay;
    uur_cursor_shape shape;

    if (hdc_dest == NULL || width <= 0 || height <= 0 || source_width <= 0 ||
        source_height <= 0 || source_is_screen_dc(hdc_dest))
        return;
    ZeroMemory(&cursor, sizeof(cursor));
    cursor.cbSize = sizeof(cursor);
    if (!GetCursorInfo(&cursor) || !(cursor.flags & CURSOR_SHOWING) ||
        !GetCursorPos(&position))
        return;
    /* Wine can report a visible cursor with a null handle until the first
     * real window has selected a class cursor.  A generic arrow is preferable
     * to dropping the cursor from the remote frame altogether. */
    if (cursor.hCursor == NULL)
        cursor.hCursor = LoadCursor(NULL, IDC_ARROW);
    if (cursor.hCursor == NULL)
        return;

    ZeroMemory(&icon, sizeof(icon));
    if (!GetIconInfo(cursor.hCursor, &icon))
        return;

    /* GetIconInfo's mask holds the cursor's actual bitmap dimensions. For a
     * monochrome cursor the AND/XOR masks are stacked vertically. */
    if (icon.hbmMask != NULL &&
        GetObjectW(icon.hbmMask, sizeof(mask), &mask) == sizeof(mask)) {
        shape.x = position.x;
        shape.y = position.y;
        shape.width = mask.bmWidth;
        shape.height = uur_cursor_bitmap_height(mask.bmHeight,
                                                 icon.hbmColor != NULL);
        shape.hotspot_x = (int)icon.xHotspot;
        shape.hotspot_y = (int)icon.yHotspot;
        if (uur_map_cursor_overlay(&source, &destination, &shape, &overlay))
            DrawIconEx(hdc_dest, overlay.x, overlay.y, cursor.hCursor,
                       overlay.width, overlay.height, 0, NULL, DI_NORMAL);
    }
    if (icon.hbmColor != NULL)
        DeleteObject(icon.hbmColor);
    if (icon.hbmMask != NULL)
        DeleteObject(icon.hbmMask);
}

/* Feed the newest desktop frame into the capture destination by drawing
 * our shared-memory frame with StretchDIBits.  Works regardless of the
 * destination bitmap type (DDB or DIB section). */
static BOOL feed_capture_frame(HDC hdc_dest, int x, int y, int width,
                               int height, int source_x, int source_y,
                               int source_width, int source_height)
{
    const unsigned char *header;
    uint32_t fw, fh, fstride;
    uint64_t total;
    int tries;
    int ok = 0;

    if (!ensure_frame_map())
        return FALSE;
    header = (const unsigned char *)frame_map;
    fw = load_u32(header + 8);
    fh = load_u32(header + 12);
    fstride = load_u32(header + 16);
    size_t frame_bytes = (size_t)fstride * fh;
    total = load_u64(header + 24);
    if (fw == 0 || fh == 0 || fstride < fw * 4 || total == 0 ||
        frame_bytes / fstride != fh ||
        UURF_HEADER_BYTES + UURF_SLOT_COUNT * frame_slot_bytes > frame_map_size)
        return FALSE;
    if (frame_snapshot_capacity < frame_bytes) {
        unsigned char *fresh = HeapReAlloc(GetProcessHeap(), 0, frame_snapshot,
                                           frame_bytes);
        if (fresh == NULL && frame_snapshot == NULL)
            fresh = HeapAlloc(GetProcessHeap(), 0, frame_bytes);
        if (fresh == NULL)
            return FALSE;
        frame_snapshot = fresh;
        frame_snapshot_capacity = frame_bytes;
    }

    for (tries = 0; tries < 16 && !ok; ++tries) {
        const unsigned char *shm_slot =
            frame_map + uurf_slot_offset(total, (size_t)frame_slot_bytes);
        uint64_t before = load_u64(shm_slot);
        if ((before & 1) == 0 && before / 2 == total) {
            MemoryBarrier();
            memcpy(frame_snapshot, shm_slot + 8, frame_bytes);
            MemoryBarrier();
            uint64_t after = load_u64(shm_slot);
            if (before != after)
                continue;
            BITMAPINFOHEADER bmp_header;
            ZeroMemory(&bmp_header, sizeof(bmp_header));
            bmp_header.biSize = sizeof(BITMAPINFOHEADER);
            bmp_header.biWidth = (LONG)fw;
            bmp_header.biHeight = -(LONG)fh; /* top-down */
            bmp_header.biPlanes = 1;
            bmp_header.biBitCount = 32;
            bmp_header.biCompression = BI_RGB;
            bmp_header.biSizeImage = fstride * fh;

            int screen_width = GetSystemMetrics(SM_CXVIRTUALSCREEN);
            int screen_height = GetSystemMetrics(SM_CYVIRTUALSCREEN);
            if (screen_width < 1)
                screen_width = (int)fw;
            if (screen_height < 1)
                screen_height = (int)fh;
            int sx = (int)((int64_t)source_x * fw / screen_width);
            int sy = (int)((int64_t)source_y * fh / screen_height);
            int sw = (int)((int64_t)source_width * fw / screen_width);
            int sh = (int)((int64_t)source_height * fh / screen_height);
            if (sw < 1)
                sw = (int)fw;
            if (sh < 1)
                sh = (int)fh;
            int result = StretchDIBits(
                hdc_dest, x, y, width, height, sx, sy, sw, sh,
                (const void *)frame_snapshot, (const BITMAPINFO *)&bmp_header,
                DIB_RGB_COLORS, SRCCOPY);
            ok = result != 0 && (DWORD)result != GDI_ERROR;
        } else {
            uint64_t now = load_u64(header + 24);
            total = (now < total) ? now : total - 1;
            if (total == 0)
                return FALSE;
        }
    }
    return ok;
}

static BOOL try_capture_feed(HDC hdc_dest, int x, int y, DWORD rop,
                             HDC hdc_src, int width, int height, int source_x,
                             int source_y, int source_width, int source_height)
{
    InterlockedIncrement(&capture_calls);
    /* The client's desktop capture is an SRCCOPY blit whose source is the
     * screen DC; anything else falls through untouched. */
    if ((rop & 0x00ffffffu) == SRCCOPY && hdc_src != NULL &&
        source_is_screen_dc(hdc_src)) {
        AcquireSRWLockExclusive(&capture_lock);
        BOOL fed = feed_capture_frame(hdc_dest, x, y, width, height, source_x,
                                     source_y, source_width, source_height);
        ReleaseSRWLockExclusive(&capture_lock);
        if (fed) {
            InterlockedIncrement(&capture_rendered);
            return TRUE;
        }
    }
    InterlockedIncrement(&capture_fallbacks);
    return FALSE;
}

BOOL WINAPI hook_bit_blt(HDC hdc_dest, int x, int y, int width, int height,
                         HDC hdc_src, int x_src, int y_src, DWORD rop)
{
    BOOL result;
    if (try_capture_feed(hdc_dest, x, y, rop, hdc_src, width, height, x_src,
                         y_src, width, height))
        return TRUE;
    result = original_bit_blt(hdc_dest, x, y, width, height, hdc_src, x_src,
                              y_src, rop);
    if (result && (rop & 0x00ffffffu) == SRCCOPY && hdc_src != NULL &&
        source_is_screen_dc(hdc_src))
        draw_cursor_overlay(hdc_dest, x, y, width, height, x_src, y_src,
                            width, height);
    return result;
}

BOOL WINAPI hook_stretch_blt(HDC hdc_dest, int x, int y, int w, int h,
                             HDC hdc_src, int xs, int ys, int sw, int sh,
                             DWORD rop)
{
    BOOL result;
    if (try_capture_feed(hdc_dest, x, y, rop, hdc_src, w, h, xs, ys, sw, sh))
        return TRUE;
    result = original_stretch_blt(hdc_dest, x, y, w, h, hdc_src, xs, ys, sw,
                                  sh, rop);
    if (result && (rop & 0x00ffffffu) == SRCCOPY && hdc_src != NULL &&
        source_is_screen_dc(hdc_src))
        draw_cursor_overlay(hdc_dest, x, y, w, h, xs, ys, sw, sh);
    return result;
}

static FARPROC WINAPI hook_get_proc_address(HMODULE module, LPCSTR name)
{
    union {
        FARPROC generic;
        BOOL(WINAPI *bit_blt)(HDC, int, int, int, int, HDC, int, int, DWORD);
        BOOL(WINAPI *stretch_blt)(HDC, int, int, int, int, HDC, int, int,
                                  int, int, DWORD);
        HRESULT(WINAPI *create_dxgi_factory1)(REFIID, void **);
    } replacement;
    FARPROC resolved = original_get_proc_address(module, name);
    if (name == NULL || ((uintptr_t)name >> 16) == 0)
        return resolved;
    if (lstrcmpiA(name, "BitBlt") == 0) {
        original_bit_blt = (void *)resolved;
        replacement.bit_blt = hook_bit_blt;
        return replacement.generic;
    }
    if (lstrcmpiA(name, "StretchBlt") == 0) {
        original_stretch_blt = (void *)resolved;
        replacement.stretch_blt = hook_stretch_blt;
        return replacement.generic;
    }
    if (lstrcmpiA(name, "CreateDXGIFactory1") == 0) {
        original_create_dxgi_factory1 = (void *)resolved;
        replacement.create_dxgi_factory1 = hook_create_dxgi_factory1;
        return replacement.generic;
    }
    return resolved;
}

/* Minimal ini reader: returns a malloc'd value for `key` or NULL. */
static char *read_ini_value(const char *path, const char *key)
{
    FILE *f = fopen(path, "r");
    char line[512];
    size_t key_len;

    if (f == NULL)
        return NULL;
    key_len = strlen(key);
    while (fgets(line, sizeof(line), f) != NULL) {
        if (strncmp(line, key, key_len) == 0 && line[key_len] == '=') {
            char *end = line + strlen(line);
            char *value = line + key_len + 1;
            char *out;
            size_t len;
            while (end > value &&
                   (end[-1] == '\n' || end[-1] == '\r' || end[-1] == ' '))
                *--end = '\0';
            fclose(f);
            len = (size_t)(end - value);
            out = malloc(len + 1);
            if (out != NULL) {
                memcpy(out, value, len);
                out[len] = '\0';
            }
            return out;
        }
    }
    fclose(f);
    return NULL;
}

/* ---- IAT rewrite ------------------------------------------------------ */

static int patch_module_iat(HMODULE base)
{
    if (base == NULL)
        return 0;

    IMAGE_DOS_HEADER *dos = (IMAGE_DOS_HEADER *)base;
    if (dos->e_magic != IMAGE_DOS_SIGNATURE)
        return 0;
    IMAGE_NT_HEADERS *nt = (IMAGE_NT_HEADERS *)((char *)base + dos->e_lfanew);
    if (nt->Signature != IMAGE_NT_SIGNATURE)
        return 0;

    IMAGE_DATA_DIRECTORY *dir =
        &nt->OptionalHeader.DataDirectory[IMAGE_DIRECTORY_ENTRY_IMPORT];
    if (dir->VirtualAddress == 0)
        return 0;

    int patched = 0;
    IMAGE_IMPORT_DESCRIPTOR *descriptor = (IMAGE_IMPORT_DESCRIPTOR *)
        ((char *)base + dir->VirtualAddress);
    for (; descriptor->Name != 0; ++descriptor) {
        const char *module_name = (const char *)base + descriptor->Name;
        if (_stricmp(module_name, "USER32.dll") != 0 &&
            _stricmp(module_name, "GDI32.dll") != 0 &&
            _stricmp(module_name, "dxgi.dll") != 0 &&
            _stricmp(module_name, "KERNEL32.dll") != 0 &&
            _stricmp(module_name, "KERNELBASE.dll") != 0)
            continue;

        IMAGE_THUNK_DATA *thunk = (IMAGE_THUNK_DATA *)
            ((char *)base + descriptor->FirstThunk);
        IMAGE_THUNK_DATA *original = thunk;
        if (descriptor->OriginalFirstThunk != 0)
            original = (IMAGE_THUNK_DATA *)
                ((char *)base + descriptor->OriginalFirstThunk);

        for (; original->u1.AddressOfData != 0; ++thunk, ++original) {
            if (original->u1.Ordinal & IMAGE_ORDINAL_FLAG)
                continue;
            IMAGE_IMPORT_BY_NAME *name = (IMAGE_IMPORT_BY_NAME *)
                ((char *)base + original->u1.AddressOfData);
            void *hook_fn = NULL;
            void **original_slot = NULL;

            if (lstrcmpiA(name->Name, "BitBlt") == 0) {
                hook_fn = (void *)hook_bit_blt;
                original_slot = (void **)&original_bit_blt;
            } else if (lstrcmpiA(name->Name, "StretchBlt") == 0) {
                hook_fn = (void *)hook_stretch_blt;
                original_slot = (void **)&original_stretch_blt;
            } else if (lstrcmpiA(name->Name, "CreateDXGIFactory1") == 0) {
                hook_fn = (void *)hook_create_dxgi_factory1;
                original_slot = (void **)&original_create_dxgi_factory1;
            } else if (lstrcmpiA(name->Name, "GetProcAddress") == 0) {
                hook_fn = (void *)hook_get_proc_address;
                original_slot = (void **)&original_get_proc_address;
            }
            if (hook_fn == NULL)
                continue;
            if (thunk->u1.Function == (uintptr_t)hook_fn)
                continue;
            *original_slot = (void *)thunk->u1.Function;
            DWORD old_protect = 0;
            if (!VirtualProtect(&thunk->u1.Function, sizeof(thunk->u1.Function),
                                PAGE_READWRITE, &old_protect))
                continue;
            thunk->u1.Function = (uintptr_t)hook_fn;
            VirtualProtect(&thunk->u1.Function, sizeof(thunk->u1.Function),
                           old_protect, &old_protect);
            ++patched;
            InterlockedIncrement(&iat_hooks_installed);
        }
    }
    return patched;
}

static int patch_loaded_modules(void)
{
    int patched = 0;
    HANDLE snapshot = CreateToolhelp32Snapshot(TH32CS_SNAPMODULE,
                                               GetCurrentProcessId());
    if (snapshot == INVALID_HANDLE_VALUE)
        return 0;
    MODULEENTRY32W entry;
    entry.dwSize = sizeof(entry);
    if (Module32FirstW(snapshot, &entry)) {
        do {
            patched += patch_module_iat(entry.hModule);
        } while (Module32NextW(snapshot, &entry));
    }
    CloseHandle(snapshot);
    return patched;
}

/* ---- late-module watchdog --------------------------------------------- */

static DWORD WINAPI patch_watchdog(LPVOID parameter)
{
    (void)parameter;
    for (;;) {
        Sleep(2000);
        patch_loaded_modules();
        char status_path[MAX_PATH];
#ifdef UURB_NATIVE_GPU
        sprintf(status_path, "C:\\uurb-native-gpu-status-%lu.txt",
#else
        sprintf(status_path, "C:\\uurb-native-cpu-status-%lu.txt",
#endif
                (unsigned long)GetCurrentProcessId());
        FILE *f = fopen(status_path, "w");
        if (f != NULL) {
            fprintf(f,
                    "pid=%lu iat=%ld dxgi_f=%ld dxgi_a=%ld dxgi_o=%ld dup=%ld\n\
                     calls=%ld rendered=%ld fallbacks=%ld native_success=%ld native_errors=%ld\n",
                    GetCurrentProcessId(), iat_hooks_installed,
                    dxgi_factories_patched, dxgi_adapters_patched,
                    dxgi_outputs_patched, dxgi_duplicate_calls,
                    capture_calls, capture_rendered, capture_fallbacks,
                    dxgi_native_success, dxgi_native_errors);
            fclose(f);
        }
    }
    return 0;
}

BOOL WINAPI DllMain(HINSTANCE instance, DWORD reason, LPVOID reserved)
{
    (void)reserved;
    if (reason != DLL_PROCESS_ATTACH) return TRUE;
    DisableThreadLibraryCalls(instance);
    patch_loaded_modules();
    HANDLE thread = CreateThread(NULL, 0, patch_watchdog, NULL, 0, NULL);
    if (thread) CloseHandle(thread);
    return TRUE;
}
