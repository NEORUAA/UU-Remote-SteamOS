#ifndef UURB_IMAGE_DATA_OBJECT_H
#define UURB_IMAGE_DATA_OBJECT_H

/* Independent, read-only OLE image publisher. The source handles become
 * object-owned only when construction succeeds. GetData returns a fresh copy. */
typedef struct {
    IDataObject iface;
    LONG references;
    HGLOBAL images[3];
    UINT formats[3];
    ULONG count;
} uurb_image_object;

typedef struct {
    IEnumFORMATETC iface;
    LONG references;
    ULONG position;
    UINT formats[3];
    ULONG count;
} uurb_image_formats;

static const IID uurb_iid_unknown =
    {0, 0, 0, {0xc0, 0, 0, 0, 0, 0, 0, 0x46}};
static const IID uurb_iid_data =
    {0x10e, 0, 0, {0xc0, 0, 0, 0, 0, 0, 0, 0x46}};
static const IID uurb_iid_formats =
    {0x103, 0, 0, {0xc0, 0, 0, 0, 0, 0, 0, 0x46}};

static FORMATETC uurb_image_format(UINT format)
{
    FORMATETC result = {(CLIPFORMAT)format,
        NULL, DVASPECT_CONTENT, -1, TYMED_HGLOBAL};
    return result;
}

static ULONG STDMETHODCALLTYPE uurb_formats_addref(IEnumFORMATETC *iface)
{
    return InterlockedIncrement(&((uurb_image_formats *)iface)->references);
}

static ULONG STDMETHODCALLTYPE uurb_formats_release(IEnumFORMATETC *iface)
{
    uurb_image_formats *object = (uurb_image_formats *)iface;
    ULONG references = InterlockedDecrement(&object->references);
    if (!references) HeapFree(GetProcessHeap(), 0, object);
    return references;
}

static HRESULT STDMETHODCALLTYPE uurb_formats_query(IEnumFORMATETC *iface,
    REFIID iid, void **output)
{
    if (!output) return E_POINTER;
    *output = NULL;
    if (!IsEqualIID(iid, &uurb_iid_unknown) && !IsEqualIID(iid, &uurb_iid_formats))
        return E_NOINTERFACE;
    *output = iface;
    uurb_formats_addref(iface);
    return S_OK;
}

static HRESULT STDMETHODCALLTYPE uurb_formats_next(IEnumFORMATETC *iface,
    ULONG count, FORMATETC *output, ULONG *fetched)
{
    uurb_image_formats *object = (uurb_image_formats *)iface;
    ULONG completed = 0;
    if (fetched) *fetched = 0;
    if (!output || (!fetched && count != 1)) return E_POINTER;
    while (completed < count && object->position < object->count)
        output[completed++] = uurb_image_format(object->formats[object->position++]);
    if (fetched) *fetched = completed;
    return completed == count ? S_OK : S_FALSE;
}

static HRESULT STDMETHODCALLTYPE uurb_formats_skip(IEnumFORMATETC *iface,
    ULONG count)
{
    uurb_image_formats *object = (uurb_image_formats *)iface;
    ULONG available = object->count - object->position;
    object->position += count < available ? count : available;
    return count <= available ? S_OK : S_FALSE;
}

static HRESULT STDMETHODCALLTYPE uurb_formats_reset(IEnumFORMATETC *iface)
{
    ((uurb_image_formats *)iface)->position = 0;
    return S_OK;
}

static HRESULT uurb_formats_new(const UINT *formats, ULONG count, ULONG position,
    IEnumFORMATETC **output);

static HRESULT STDMETHODCALLTYPE uurb_formats_clone(IEnumFORMATETC *iface,
    IEnumFORMATETC **output)
{
    uurb_image_formats *object = (uurb_image_formats *)iface;
    return uurb_formats_new(object->formats, object->count, object->position, output);
}

static IEnumFORMATETCVtbl uurb_formats_vtable = {
    uurb_formats_query, uurb_formats_addref, uurb_formats_release,
    uurb_formats_next, uurb_formats_skip, uurb_formats_reset, uurb_formats_clone
};

static HRESULT uurb_formats_new(const UINT *formats, ULONG count, ULONG position,
    IEnumFORMATETC **output)
{
    uurb_image_formats *object;
    if (!output) return E_POINTER;
    *output = NULL;
    object = HeapAlloc(GetProcessHeap(), HEAP_ZERO_MEMORY, sizeof(*object));
    if (!object) return E_OUTOFMEMORY;
    object->iface.lpVtbl = &uurb_formats_vtable;
    object->references = 1;
    object->position = position;
    object->count = count;
    memcpy(object->formats, formats, count * sizeof(*formats));
    *output = &object->iface;
    return S_OK;
}

static ULONG STDMETHODCALLTYPE uurb_image_addref(IDataObject *iface)
{
    return InterlockedIncrement(&((uurb_image_object *)iface)->references);
}

static ULONG STDMETHODCALLTYPE uurb_image_release(IDataObject *iface)
{
    uurb_image_object *object = (uurb_image_object *)iface;
    ULONG references = InterlockedDecrement(&object->references);
    if (!references) {
        for (ULONG i = 0; i < object->count; i++) GlobalFree(object->images[i]);
        HeapFree(GetProcessHeap(), 0, object);
    }
    return references;
}

static HRESULT STDMETHODCALLTYPE uurb_image_query(IDataObject *iface,
    REFIID iid, void **output)
{
    if (!output) return E_POINTER;
    *output = NULL;
    if (!IsEqualIID(iid, &uurb_iid_unknown) && !IsEqualIID(iid, &uurb_iid_data))
        return E_NOINTERFACE;
    *output = iface;
    uurb_image_addref(iface);
    return S_OK;
}

static HRESULT STDMETHODCALLTYPE uurb_image_query_data(IDataObject *iface,
    FORMATETC *format)
{
    uurb_image_object *object = (uurb_image_object *)iface;
    if (!format) return E_POINTER;
    ULONG index;
    for (index = 0; index < object->count; index++)
        if (format->cfFormat == object->formats[index]) break;
    if (index == object->count) return DV_E_FORMATETC;
    if (format->dwAspect != DVASPECT_CONTENT) return DV_E_DVASPECT;
    if (format->lindex != -1) return DV_E_LINDEX;
    if (format->ptd) return DV_E_DVTARGETDEVICE;
    return (format->tymed & TYMED_HGLOBAL) ? S_OK : DV_E_TYMED;
}

static HRESULT STDMETHODCALLTYPE uurb_image_get(IDataObject *iface,
    FORMATETC *format, STGMEDIUM *medium)
{
    uurb_image_object *object = (uurb_image_object *)iface;
    HRESULT result;
    HGLOBAL source, copy;
    void *from, *to;
    SIZE_T size;
    if (!medium) return E_POINTER;
    memset(medium, 0, sizeof(*medium));
    result = uurb_image_query_data(iface, format);
    if (FAILED(result)) return result;
    ULONG index = 0;
    while (object->formats[index] != format->cfFormat) index++;
    source = object->images[index];
    size = GlobalSize(source);
    from = GlobalLock(source);
    if (!from) return STG_E_MEDIUMFULL;
    copy = GlobalAlloc(GMEM_MOVEABLE, size);
    to = copy ? GlobalLock(copy) : NULL;
    if (!to) {
        if (copy) GlobalFree(copy);
        GlobalUnlock(source);
        return STG_E_MEDIUMFULL;
    }
    memcpy(to, from, size);
    GlobalUnlock(copy);
    GlobalUnlock(source);
    medium->tymed = TYMED_HGLOBAL;
    medium->hGlobal = copy;
    return S_OK;
}

static HRESULT STDMETHODCALLTYPE uurb_image_get_here(IDataObject *iface,
    FORMATETC *format, STGMEDIUM *medium)
{
    (void)iface; (void)format; (void)medium;
    return DV_E_TYMED;
}

static HRESULT STDMETHODCALLTYPE uurb_image_canonical(IDataObject *iface,
    FORMATETC *input, FORMATETC *output)
{
    HRESULT result;
    if (!output) return E_POINTER;
    memset(output, 0, sizeof(*output));
    result = uurb_image_query_data(iface, input);
    if (FAILED(result)) return result;
    *output = *input;
    return DATA_S_SAMEFORMATETC;
}

static HRESULT STDMETHODCALLTYPE uurb_image_set(IDataObject *iface,
    FORMATETC *format, STGMEDIUM *medium, BOOL release)
{
    (void)iface; (void)format; (void)medium; (void)release;
    return E_NOTIMPL;
}

static HRESULT STDMETHODCALLTYPE uurb_image_enum(IDataObject *iface,
    DWORD direction, IEnumFORMATETC **output)
{
    uurb_image_object *object = (uurb_image_object *)iface;
    if (!output) return E_POINTER;
    *output = NULL;
    return direction == DATADIR_GET ? uurb_formats_new(object->formats,
        object->count, 0, output) : E_NOTIMPL;
}

static HRESULT STDMETHODCALLTYPE uurb_image_advise(IDataObject *iface,
    FORMATETC *format, DWORD flags, IAdviseSink *sink, DWORD *connection)
{
    (void)iface; (void)format; (void)flags; (void)sink;
    if (connection) *connection = 0;
    return OLE_E_ADVISENOTSUPPORTED;
}

static HRESULT STDMETHODCALLTYPE uurb_image_unadvise(IDataObject *iface,
    DWORD connection)
{
    (void)iface; (void)connection;
    return OLE_E_ADVISENOTSUPPORTED;
}

static HRESULT STDMETHODCALLTYPE uurb_image_enum_advise(IDataObject *iface,
    IEnumSTATDATA **output)
{
    (void)iface;
    if (!output) return E_POINTER;
    *output = NULL;
    return OLE_E_ADVISENOTSUPPORTED;
}

static IDataObjectVtbl uurb_image_vtable = {
    uurb_image_query, uurb_image_addref, uurb_image_release,
    uurb_image_get, uurb_image_get_here, uurb_image_query_data,
    uurb_image_canonical, uurb_image_set, uurb_image_enum,
    uurb_image_advise, uurb_image_unadvise, uurb_image_enum_advise
};

static IDataObject *uurb_image_object_new(HGLOBAL v5, HGLOBAL dib, HGLOBAL png)
{
    uurb_image_object *object;
    if (!v5 || !dib) return NULL;
    UINT png_format = png ? RegisterClipboardFormatW(L"PNG") : 0;
    if (png && !png_format) return NULL;
    object = HeapAlloc(GetProcessHeap(), HEAP_ZERO_MEMORY, sizeof(*object));
    if (!object) return NULL;
    object->iface.lpVtbl = &uurb_image_vtable;
    object->references = 1;
    object->count = png ? 3 : 2;
    object->images[0] = png ? png : v5;
    object->images[1] = png ? v5 : dib;
    object->formats[0] = png ? png_format : CF_DIBV5;
    object->formats[1] = png ? CF_DIBV5 : CF_DIB;
    if (png) {
        object->images[2] = dib;
        object->formats[2] = CF_DIB;
    }
    return &object->iface;
}

#endif
