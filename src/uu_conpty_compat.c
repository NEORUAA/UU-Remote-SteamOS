#define _WIN32_WINNT 0x0A00
#include <windows.h>
HRESULT WINAPI uurb_create(COORD size,HANDLE input,HANDLE output,DWORD flags,HPCON *pc)
{
    /* Cursor inheritance breaks Wine 11 console handles; retain other UU flags. */
    return CreatePseudoConsole(size,input,output,flags & ~PSEUDOCONSOLE_INHERIT_CURSOR,pc);
}
HRESULT WINAPI uurb_resize(HPCON pc,COORD size){return ResizePseudoConsole(pc,size);}
void WINAPI uurb_close(HPCON pc){ClosePseudoConsole(pc);}
