# Mac PNG clipboard compatibility

The current UU 4.42 Windows image mapping accepts Mac TIFF as Win32 DIB.
In the real controller check, PNG-only copies produced no Windows image offer,
while a distinct TIFF-only image reached native Ubuntu and a Wayland GTK reader
with identical RGB pixels. A second, distinct 53×37 source advertised TIFF first
and its original PNG alongside it; native Ubuntu received identical RGB pixels.
The PNG source was correctly copied and read by Mac
UU. This narrows the observed failure to image-format compatibility before the
native Ubuntu reader; it is not a claim about every UU release or controller.

The optional Mac helper provides an automatic TIFF representation for a pure
PNG clipboard image. It preserves the original PNG bytes. It acts only while
UU is running, skips text, file/URL, rich-text and multiple-item copies, and does
not change UU settings. Other application-specific image flavors are replaced
by the PNG and TIFF representations. Both the converted payload and the
original PNG are limited to 64 MiB, with at most 16 million decoded pixels.

Build it on the Mac with the existing Xcode command-line tools:

```sh
scripts/build-macos-clipboard-compat.sh
open "build/macos/UU Clipboard Compat.app"
```

The menu bar's **UU Clip** menu has an **Enable PNG compatibility** switch.
The first launch also shows **UU 图片兼容设置**, with a checkbox to enable it.
The menu's **设置…** item and reopening the app show that window again. Closing
the window keeps the helper running; **Quit** exits it. It starts disabled until
enabled and remembers that choice. For the authorized
controller verification, `open -a "build/macos/UU Clipboard Compat.app" --args
--enable` enables it on launch. It stays local and records no clipboard body,
file contents or network data. Disabling or quitting stops future conversions.
No login item is installed by the build script.

## Acceptance and current state · 2026-10-06

The settings UI compiled on the actual Mac, and an ordinary PNG copy passed
with the automatic helper: its TIFF offer reached UU and native Ubuntu with
matching image pixels. That is historical acceptance with this local companion,
not a guarantee for all official Mac UU versions or image-copy sources.

The reference helper is currently **not running**. Its saved
`imageCompatibilityEnabled` preference remains enabled; not running and a
saved disabled preference are different states. No launch or preference change
was made for this documentation update. Current reverse Ubuntu → Mac freshness
and color acceptance is still pending. See the [development update](updates/2026-10-06.md).

For a later incoming check, use a distinct Mac PNG, verify that the running
helper adds TIFF, observe the new Windows image offer and compare the actual
native GTK pixels. A previously passing sample does not establish a new result.
