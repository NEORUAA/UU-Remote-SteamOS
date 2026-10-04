#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv)
{
    if (argc != 2 || !LoadLibraryA(argv[1])) return 2;
    HDC screen = GetDC(NULL), memory = CreateCompatibleDC(screen);
    BITMAPINFO info = {0};
    info.bmiHeader.biSize = sizeof(info.bmiHeader);
    info.bmiHeader.biWidth = 3840;
    info.bmiHeader.biHeight = -2160;
    info.bmiHeader.biPlanes = 1;
    info.bmiHeader.biBitCount = 32;
    void *pixels = NULL;
    HBITMAP bitmap = CreateDIBSection(memory, &info, DIB_RGB_COLORS, &pixels, NULL, 0);
    if (!bitmap || !pixels) return 3;
    HGDIOBJ old = SelectObject(memory, bitmap);
    LARGE_INTEGER frequency, before, after;
    QueryPerformanceFrequency(&frequency);
    union { FARPROC address; BOOL (WINAPI *blit)(HDC,int,int,int,int,HDC,int,int,DWORD); } method;
    method.address = GetProcAddress(GetModuleHandleA("gdi32.dll"), "BitBlt");
    double samples[12];
    for (unsigned round = 0; round < 12; round++) {
        QueryPerformanceCounter(&before);
        if (!(round % 2 ? method.blit(memory, 0, 0, 3840, 2160, screen, 0, 0, SRCCOPY)
                         : BitBlt(memory, 0, 0, 3840, 2160, screen, 0, 0, SRCCOPY))) return 4;
        QueryPerformanceCounter(&after);
        samples[round] = 1000.0 * (after.QuadPart - before.QuadPart) / frequency.QuadPart;
    }
    unsigned char *data = pixels;
    for (size_t i = 0; i < (size_t)3840 * 2160; i++)
        if (data[i * 4] != 29 || data[i * 4 + 1] != 61 || data[i * 4 + 2] != 193) return 5;
    printf("{\"pixels\":\"PASS\",\"width\":3840,\"height\":2160,\"consumer_copy_ms\":[");
    for (unsigned i = 0; i < 12; i++) printf("%s%.4f", i ? "," : "", samples[i]);
    puts("],\"scope\":\"synthetic SHM to Wine GDI; no UU encoding/controller latency\"}");
    SelectObject(memory, old);
    DeleteObject(bitmap);
    DeleteDC(memory);
    ReleaseDC(NULL, screen);
    return 0;
}
