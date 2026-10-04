#ifndef UURB_X11_CLIPBOARD_PROTOCOL_H
#define UURB_X11_CLIPBOARD_PROTOCOL_H

#include <stdint.h>

/* Authenticated Wine-to-desktop transport. Kind zero retains the original
 * text request; extended kinds carry images, image reads and incoming files. */
#define UURB_X11_CLIPBOARD_MAGIC UINT32_C(0x43425555)
#define UURB_X11_CLIPBOARD_VERSION UINT32_C(1)
#define UURB_X11_CLIPBOARD_TOKEN_SIZE 64
#define UURB_X11_CLIPBOARD_MAX_TEXT_BYTES UINT32_C(4194304)
#define UURB_CLIPBOARD_MAX_BINARY UINT32_C(67108864)
#define UURB_CLIPBOARD_PNG 1U
#define UURB_CLIPBOARD_DIB 2U
#define UURB_CLIPBOARD_GET_IMAGE 3U
#define UURB_CLIPBOARD_FILE 4U
/* Read response payload: uint32 kind followed by UTF-8 text or DIBV5. */
#define UURB_CLIPBOARD_GET_HOST 5U

#define UURB_X11_CLIPBOARD_ERROR_BAD_REQUEST UINT32_C(0x3001)
#define UURB_X11_CLIPBOARD_ERROR_INVALID_TEXT UINT32_C(0x3002)
#define UURB_X11_CLIPBOARD_ERROR_OWNER UINT32_C(0x3003)

typedef struct uurb_x11_clipboard_handshake {
    uint32_t magic;
    uint32_t version;
    char token[UURB_X11_CLIPBOARD_TOKEN_SIZE];
} uurb_x11_clipboard_handshake;

typedef struct uurb_x11_clipboard_request {
    uint32_t magic;
    uint32_t sequence;
    uint32_t text_bytes;
    uint32_t reserved;
} uurb_x11_clipboard_request;

typedef struct uurb_x11_clipboard_response {
    uint32_t magic;
    uint32_t sequence;
    uint32_t result;
    uint32_t error;
} uurb_x11_clipboard_response;

#endif
