#define _GNU_SOURCE
#include <dlfcn.h>
#include <pthread.h>
#include <stdint.h>
#include <limits.h>
#include <stdio.h>
#include <string.h>

/* Plasma 6.4 KRDP binds fake-input but never calls authenticate. KWin 6.4
 * ignores input from that unauthenticated device. Interpose the fixed-argument
 * public marshaller used by both Wayland constructor APIs, and authenticate
 * only the newly bound fake-input proxy in this KRDP process. */
struct wl_proxy;
struct wl_interface;
union wl_argument { int32_t i; uint32_t u; void *pointer; };
static pthread_once_t once = PTHREAD_ONCE_INIT;
static struct wl_proxy *(*real_marshal)(struct wl_proxy *, uint32_t,
    const struct wl_interface *, uint32_t, uint32_t, union wl_argument *);
static const char *(*proxy_class)(struct wl_proxy *);
static uint32_t (*proxy_version)(struct wl_proxy *);
static struct wl_proxy *(*marshal)(struct wl_proxy *, uint32_t,
    const struct wl_interface *, uint32_t, uint32_t, ...);

static void initialize(void)
{
    void *symbol = dlsym(RTLD_NEXT, "wl_proxy_marshal_array_flags");
    memcpy(&real_marshal, &symbol, sizeof(real_marshal));
    symbol = dlsym(RTLD_NEXT, "wl_proxy_get_class");
    memcpy(&proxy_class, &symbol, sizeof(proxy_class));
    symbol = dlsym(RTLD_NEXT, "wl_proxy_get_version");
    memcpy(&proxy_version, &symbol, sizeof(proxy_version));
    symbol = dlsym(RTLD_NEXT, "wl_proxy_marshal_flags");
    memcpy(&marshal, &symbol, sizeof(marshal));
}

static int32_t scaled_fixed(int32_t value, int32_t scale)
{
    int64_t fixed = (int64_t)value * scale;
    return fixed < INT32_MIN ? INT32_MIN :
           fixed > INT32_MAX ? INT32_MAX : (int32_t)fixed;
}

struct wl_proxy *wl_proxy_marshal_array_flags(struct wl_proxy *proxy, uint32_t opcode,
    const struct wl_interface *interface, uint32_t version, uint32_t flags,
    union wl_argument *arguments)
{
    pthread_once(&once, initialize);
    if (!real_marshal)
        return NULL;
    if (proxy && proxy_class && arguments && (opcode == 9 || opcode == 3)) {
        const char *name = proxy_class(proxy);
        if (name && strcmp(name, "org_kde_kwin_fake_input") == 0) {
            /* KRDP 6.4.3 passes pixel doubles to QtWayland's wl_fixed_t
             * parameters. Restore the required 24.8 fixed-point encoding. */
            if (opcode == 9) {
                for (unsigned int index = 0; index < 2; ++index)
                    arguments[index].i = scaled_fixed(arguments[index].i, 256);
            } else {
                /* KRDP passes Qt wheel notches as an unencoded integer.
                 * Preserve the UU/FreeRDP direction selected by the controller.
                 * One standard wheel notch is 15 axis units in 24.8 encoding. */
                arguments[1].i = scaled_fixed(arguments[1].i, 15 * 256);
            }
        }
    }
    struct wl_proxy *created = real_marshal(proxy, opcode, interface, version, flags, arguments);
    if (created && interface && proxy_class && proxy_version && marshal) {
        const char *name = proxy_class(created);
        if (name && strcmp(name, "org_kde_kwin_fake_input") == 0) {
            marshal(created, 0, NULL, proxy_version(created), 0,
                    "UU SteamOS Desktop Relay", "Remote desktop input");
            fprintf(stderr, "UU KRDP: authenticated the Plasma input proxy\n");
        }
    }
    return created;
}
