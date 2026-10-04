#define COBJMACROS
#include <windows.h>
#include <ole2.h>
#include <shlobj.h>
#include <shellapi.h>
#include <stdio.h>
#include <wchar.h>

static const char content[] = "virtual-file\0\xff\n";
static ULONG refs = 1;
static BOOL multiple_virtual;
static HRESULT STDMETHODCALLTYPE query(IDataObject *self, REFIID iid, void **out)
{
    if (IsEqualIID(iid, &IID_IUnknown) || IsEqualIID(iid, &IID_IDataObject)) {
        *out = self; refs++; return S_OK;
    }
    *out = NULL; return E_NOINTERFACE;
}
static ULONG STDMETHODCALLTYPE addref(IDataObject *self) { (void)self; return ++refs; }
static ULONG STDMETHODCALLTYPE release(IDataObject *self) { (void)self; return --refs; }
static HRESULT STDMETHODCALLTYPE getdata(IDataObject *self, FORMATETC *f, STGMEDIUM *m)
{
    (void)self;
    ZeroMemory(m, sizeof(*m));
    if (f->cfFormat == RegisterClipboardFormatW(L"FileGroupDescriptorW")) {
        FILEGROUPDESCRIPTORW *g;
        m->tymed = TYMED_HGLOBAL;
        m->hGlobal = GlobalAlloc(GMEM_MOVEABLE | GMEM_ZEROINIT,
            sizeof(*g) + (multiple_virtual ? sizeof(FILEDESCRIPTORW) : 0));
        g = GlobalLock(m->hGlobal);
        if (!g) return E_OUTOFMEMORY;
        g->cItems = multiple_virtual ? 2 : 1;
        g->fgd[0].dwFlags = FD_FILESIZE;
        g->fgd[0].nFileSizeLow = sizeof(content) - 1;
        wcscpy(g->fgd[0].cFileName, L"virtual.txt");
        if (multiple_virtual)
            wcscpy(g->fgd[1].cFileName, L"unknown-size.txt");
        GlobalUnlock(m->hGlobal);
        return S_OK;
    }
    if (f->cfFormat == RegisterClipboardFormatW(L"FileContents") &&
        (f->lindex == 0 || (multiple_virtual && f->lindex == 1))) {
        LARGE_INTEGER beginning = { .QuadPart = 0 };
        ULONG written;
        m->tymed = TYMED_ISTREAM;
        if (FAILED(CreateStreamOnHGlobal(NULL, TRUE, &m->pstm))) return E_OUTOFMEMORY;
        IStream_Write(m->pstm, content, sizeof(content) - 1, &written);
        IStream_Seek(m->pstm, beginning, STREAM_SEEK_SET, NULL);
        return S_OK;
    }
    return DV_E_FORMATETC;
}
static HRESULT STDMETHODCALLTYPE here(IDataObject *s, FORMATETC *f, STGMEDIUM *m)
{ (void)s; (void)f; (void)m; return E_NOTIMPL; }
static HRESULT STDMETHODCALLTYPE can_get(IDataObject *s, FORMATETC *f)
{ (void)s; return (f->cfFormat == RegisterClipboardFormatW(L"FileGroupDescriptorW") ||
                   f->cfFormat == RegisterClipboardFormatW(L"FileContents")) ? S_OK : DV_E_FORMATETC; }
static HRESULT STDMETHODCALLTYPE canonical(IDataObject *s, FORMATETC *a, FORMATETC *b)
{ (void)s; (void)a; b->ptd = NULL; return E_NOTIMPL; }
static HRESULT STDMETHODCALLTYPE setdata(IDataObject *s, FORMATETC *f, STGMEDIUM *m, BOOL free_it)
{ (void)s; (void)f; (void)m; (void)free_it; return E_NOTIMPL; }
static HRESULT STDMETHODCALLTYPE formats(IDataObject *s, DWORD direction, IEnumFORMATETC **out)
{
    FORMATETC f[2] = {
        {0, NULL, DVASPECT_CONTENT, -1, TYMED_HGLOBAL},
        {0, NULL, DVASPECT_CONTENT, 0, TYMED_ISTREAM}};
    (void)s;
    if (direction != DATADIR_GET) return E_NOTIMPL;
    f[0].cfFormat = (CLIPFORMAT)RegisterClipboardFormatW(L"FileGroupDescriptorW");
    f[1].cfFormat = (CLIPFORMAT)RegisterClipboardFormatW(L"FileContents");
    return SHCreateStdEnumFmtEtc(2, f, out);
}
static HRESULT STDMETHODCALLTYPE advise(IDataObject *s, FORMATETC *f, DWORD a, IAdviseSink *sink, DWORD *id)
{ (void)s; (void)f; (void)a; (void)sink; (void)id; return OLE_E_ADVISENOTSUPPORTED; }
static HRESULT STDMETHODCALLTYPE unadvise(IDataObject *s, DWORD id)
{ (void)s; (void)id; return OLE_E_ADVISENOTSUPPORTED; }
static HRESULT STDMETHODCALLTYPE enum_advise(IDataObject *s, IEnumSTATDATA **out)
{ (void)s; *out = NULL; return OLE_E_ADVISENOTSUPPORTED; }
static IDataObjectVtbl methods = {query, addref, release, getdata, here, can_get,
    canonical, setdata, formats, advise, unadvise, enum_advise};
static IDataObject object = {&methods};

int wmain(int argc, wchar_t **argv)
{
    HWND window = CreateWindowExW(0, L"STATIC", L"bitmap/file fixture", 0,
        0, 0, 1, 1, NULL, NULL, GetModuleHandleW(NULL), NULL);
    MSG message;
    ULONGLONG deadline;
    if (argc < 2 || !window) return 2;
    OleInitialize(NULL);
    if (wcscmp(argv[1], L"read-png") == 0 || wcscmp(argv[1], L"read-dib-ole") == 0) {
        IDataObject *image = NULL;
        STGMEDIUM medium = {0};
        UINT png = RegisterClipboardFormatW(L"PNG");
        FORMATETC format = {wcscmp(argv[1], L"read-png") == 0 ? (CLIPFORMAT)png : CF_DIB,
            NULL, DVASPECT_CONTENT, -1, TYMED_HGLOBAL};
        if (argc != 3 || FAILED(OleGetClipboard(&image))) return 3;
        IEnumFORMATETC *enumerator = NULL;
        FORMATETC first = {0};
        BOOL png_first = SUCCEEDED(IDataObject_EnumFormatEtc(image, DATADIR_GET, &enumerator)) &&
            IEnumFORMATETC_Next(enumerator, 1, &first, NULL) == S_OK && first.cfFormat == png;
        if (enumerator) IEnumFORMATETC_Release(enumerator);
        if (!png_first || FAILED(IDataObject_GetData(image, &format, &medium))) {
            IDataObject_Release(image); return 4;
        }
        void *bytes = GlobalLock(medium.hGlobal);
        HANDLE file = bytes ? CreateFileW(argv[2], GENERIC_WRITE, 0, NULL, CREATE_NEW,
            FILE_ATTRIBUTE_NORMAL, NULL) : INVALID_HANDLE_VALUE;
        DWORD written = 0;
        BOOL saved = file != INVALID_HANDLE_VALUE && WriteFile(file, bytes,
            (DWORD)GlobalSize(medium.hGlobal), &written, NULL);
        if (file != INVALID_HANDLE_VALUE) CloseHandle(file);
        if (bytes) GlobalUnlock(medium.hGlobal);
        ReleaseStgMedium(&medium); IDataObject_Release(image); OleUninitialize();
        return saved ? 0 : 5;
    }
    if (wcscmp(argv[1], L"read-image") == 0 || wcscmp(argv[1], L"read-text") == 0) {
        HANDLE data, file;
        void *bytes;
        DWORD written;
        if (argc != 3 || !OpenClipboard(window)) return 3;
        data = GetClipboardData(wcscmp(argv[1], L"read-text") == 0 ? CF_UNICODETEXT : CF_DIBV5);
        bytes = data ? GlobalLock(data) : NULL;
        if (!bytes) { CloseClipboard(); return 4; }
        file = CreateFileW(argv[2], GENERIC_WRITE, 0, NULL, CREATE_NEW,
                           FILE_ATTRIBUTE_NORMAL, NULL);
        if (file == INVALID_HANDLE_VALUE) return 5;
        WriteFile(file, bytes, (DWORD)GlobalSize(data), &written, NULL);
        CloseHandle(file); GlobalUnlock(data); CloseClipboard(); return 0;
    }
    if (wcscmp(argv[1], L"virtual") == 0 || wcscmp(argv[1], L"virtual-multiple") == 0) {
        multiple_virtual = wcscmp(argv[1], L"virtual-multiple") == 0;
        if (FAILED(OleSetClipboard(&object))) return 6;
    } else {
        HGLOBAL allocation;
        if (!OpenClipboard(window) || !EmptyClipboard()) return 7;
        if (wcscmp(argv[1], L"drop") == 0 && argc >= 3) {
            DROPFILES *drop;
            SIZE_T length = sizeof(wchar_t);
            wchar_t *position;
            for (int index = 2; index < argc; index++)
                length += (wcslen(argv[index]) + 1) * sizeof(wchar_t);
            allocation = GlobalAlloc(GMEM_MOVEABLE | GMEM_ZEROINIT, sizeof(*drop) + length);
            drop = GlobalLock(allocation);
            drop->pFiles = sizeof(*drop); drop->fWide = TRUE;
            position = (wchar_t *)((char *)drop + sizeof(*drop));
            for (int index = 2; index < argc; index++) {
                wcscpy(position, argv[index]);
                position += wcslen(position) + 1;
            }
            GlobalUnlock(allocation);
            SetClipboardData(CF_HDROP, allocation);
        } else if (wcscmp(argv[1], L"text") == 0) {
            static const wchar_t text[] = L"Windows 中文\r\nsecond line";
            void *bytes;
            allocation = GlobalAlloc(GMEM_MOVEABLE, sizeof(text));
            bytes = GlobalLock(allocation);
            memcpy(bytes, text, sizeof(text));
            GlobalUnlock(allocation);
            SetClipboardData(CF_UNICODETEXT, allocation);
        } else {
            BITMAPV5HEADER *h;
            static const unsigned char pixels[] = {
                0,0,255,255, 0,255,0,128, 255,0,0,255,
                255,255,255,0, 30,20,10,255, 0,0,0,255};
            if (wcscmp(argv[1], L"dib-stale-v5") == 0) {
                BITMAPINFOHEADER *primary;
                allocation = GlobalAlloc(GMEM_MOVEABLE | GMEM_ZEROINIT, 40 + sizeof(pixels));
                primary = GlobalLock(allocation);
                primary->biSize = 40; primary->biWidth = 3; primary->biHeight = -2;
                primary->biPlanes = 1; primary->biBitCount = 32;
                memcpy((char *)primary + 40, pixels, sizeof(pixels));
                GlobalUnlock(allocation);
                SetClipboardData(CF_DIB, allocation);
            }
            allocation = GlobalAlloc(GMEM_MOVEABLE | GMEM_ZEROINIT, 124 + sizeof(pixels));
            h = GlobalLock(allocation);
            h->bV5Size = 124; h->bV5Width = 3; h->bV5Height = -2;
            h->bV5Planes = 1; h->bV5BitCount = 32; h->bV5Compression = BI_BITFIELDS;
            h->bV5RedMask = 0xff0000; h->bV5GreenMask = 0xff00;
            h->bV5BlueMask = 0xff; h->bV5AlphaMask = 0xff000000;
            memcpy((char *)h + 124, pixels, sizeof(pixels));
            if (wcscmp(argv[1], L"dib-stale-v5") == 0) {
                h->bV5Width = 1; h->bV5Height = -1;
                memset((char *)h + 124, 0, sizeof(pixels));
            }
            GlobalUnlock(allocation);
            SetClipboardData(CF_DIBV5, allocation);
        }
        CloseClipboard();
    }
    puts("fixture ready"); fflush(stdout);
    deadline = GetTickCount64() + 15000;
    while (GetTickCount64() < deadline) {
        while (PeekMessageW(&message, NULL, 0, 0, PM_REMOVE)) {
            TranslateMessage(&message); DispatchMessageW(&message);
        }
        Sleep(10);
    }
    return 0;
}
