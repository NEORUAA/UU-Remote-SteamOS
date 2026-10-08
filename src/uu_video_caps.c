/* Reviewed H.264/NV12 capability queries for the private Proton video copy. */
typedef unsigned int U32;
typedef unsigned long long U64;
typedef int HRESULT;
#define E_INVALIDARG ((HRESULT)0x80070057)
struct GUID { U64 low, high; };
struct Desc { struct GUID profile; U32 width, height, format; };
static __attribute__((always_inline)) int valid(const struct Desc *d) {
    return d && d->profile.low == 0x11d3a0c71b81be68ULL &&
        d->profile.high == 0xc5732e4fc00084b9ULL && d->format == 103 &&
        d->width && d->height && d->width <= 4096 && d->height <= 4096 &&
        !((d->width | d->height) & 1);
}
HRESULT check_format(void *self, const struct GUID *profile, U32 format, U32 *supported) {
    (void)self;
    if (!profile || !supported) return E_INVALIDARG;
    *supported = profile->low == 0x11d3a0c71b81be68ULL &&
        profile->high == 0xc5732e4fc00084b9ULL && format == 103;
    return 0;
}
HRESULT config_count(void *self, const struct Desc *d, U32 *count) {
    (void)self;
    if (!d || !count) return E_INVALIDARG;
    *count = valid(d) ? 1 : 0;
    return 0;
}
HRESULT get_config(void *self, const struct Desc *d, U32 index, volatile U32 *config) {
    (void)self;
    if (!valid(d) || index || !config) return E_INVALIDARG;
    for (U32 i = 0; i < 25; ++i) config[i] = 0;
    for (U32 i = 0; i < 3; ++i) {
        volatile U64 *guid = (volatile U64 *)(config + i * 4);
        guid[0] = 0x11d3a0c71b81bed0ULL;
        guid[1] = 0xc5732e4fc00084b9ULL;
    }
    /* DXVA H.264 short slices; no encryption and 16 DPB surfaces. */
    config[12] = 2;
    config[24] = 16;
    return 0;
}
