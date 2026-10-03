[English](quality-guide.md) · [العربية](i18n/ar/quality-guide.md) · [Deutsch](i18n/de/quality-guide.md) · [Español](i18n/es/quality-guide.md) · [Français](i18n/fr/quality-guide.md) · [日本語](i18n/ja/quality-guide.md) · [한국어](i18n/ko/quality-guide.md) · [Русский](i18n/ru/quality-guide.md) · [Tiếng Việt](i18n/vi/quality-guide.md) · [简体中文](i18n/zh-Hans/quality-guide.md) · [繁體中文](i18n/zh-Hant/quality-guide.md)

[Home](../README.md)

# Quality, resolution and frame rate

Choose the canvas on Ubuntu, then adjust streaming quality on the controlling computer or phone. Canvas size, compression quality, requested FPS and bitrate ceiling are separate controls.

## Canvas selection

Open **UU Remote 画质与分辨率** in the GNOME application list, or run:

```bash
uu-remote quality gui
uu-remote quality list
uu-remote quality status
uu-remote quality apply 2160p
uu-remote quality guide
```

![Ubuntu canvas selector with four presets](images/quality-presets.png)

| Preset | Canvas | Use |
| --- | --- | --- |
| `720p` | 1280 × 720 | Small screens or limited connections |
| `1080p` | 1920 × 1080 | Everyday use; first-install default |
| `1440p` | 2560 × 1440 | More workspace with fewer pixels than 4K |
| `2160p` | 3840 × 2160 | Fine text and a complete 4K workspace |

Reinstalling preserves your saved choice. Smart sizing fits the whole source desktop into the canvas and maps pointer coordinates with the same geometry. Source resolution and aspect ratio affect the result; the canvas does not resize the physical GNOME desktop. Capture can still process the full source image.

The selector distinguishes **saved startup / requested RDP size** from **current canvas**. Changing the saved size briefly reconnects UU. Reapplying the saved preset restores the live canvas on the supported RDP path without restarting the relay; the selector verifies the resulting size. A rollback timer starts before a change and restores the previous configuration if the bridge cannot become ready. Wait for recovery to finish before another change.

Fixed presets use `--follow-desktop-resolution off`, the installation default. If following was enabled, turn it off with that installer option before applying presets. See [installation](../README.md) and `./install.sh --help`.

The tested 4K source looked worse when enlarged to 5K, without additional detail. Regular choices therefore stop at 4K. Nominal 60 Hz display modes describe the virtual display, while actual streaming FPS depends on the complete connection.

## Controller quality and FPS

On a computer, open **控制中心 → 画质**; on a phone, open **操作 → 显示**. True Color is also selected on the controller where available.

![Example native UU quality and FPS menu](images/uu-native-quality-menu.png)

This menu example is from Ubuntu controlling a Mac. Available quality, FPS and color choices depend on the devices and codec. Quality changes compression and detail; requested FPS sets UU's target update rate. True Color can improve colored text and edges. If UU reports a device-performance limit, select an available quality level. Compare the same text and moving scene for clarity and responsiveness.

See NetEase's [FPS and Super Screen guide](https://uuyc.163.com/help/superscreen.html), [True Color guide](https://uuyc.163.com/features/color/) and [compatibility notes](https://uuyc.163.com/help/20241216/40221_1200122.html). Wine Super Screen / virtual-display support and 144 FPS remain untested here. [Performance notes](performance-evidence.md) describe controller measurements.

## Bitrate ceiling

```bash
uu-remote quality bitrate 20
uu-remote quality bitrate 0
```

`20` requests a **20 Mbps ceiling** through UU's CLI; `0` removes it. This sets neither a target bitrate nor FPS or canvas size. Preset changes preserve the bitrate setting. A tight ceiling can soften moving scenes, so compare on your connection.

## Cursor and desktop actions

The optional cursor guard is off on a fresh install. For an oversized pointer:

```bash
./install.sh --skip-packages --skip-account-login --cursor-guard on --cursor-size 24
```

`--cursor-size auto` follows the desktop cursor size; fixed values range from 24 to 128 pixels. GNOME and application cursor settings remain independent. The Dock uses your GNOME settings. Android's show-desktop and all-windows actions are mapped to GNOME's desktop and overview; actual Android-button testing is pending.

## Management window and recovery

`uu-remote open` opens the separate management viewer. To enlarge it:

```bash
UURB_WINDOW_SCALE=2 ./install.sh --skip-packages --skip-account-login
```

Supported scales are `1` (default), `1.5`, `2` and `3`. This affects the viewer, not Wine DPI or desktop resolution. Manager clipboard exchange is disabled; desktop copy/paste uses the relay.

```bash
uu-remote status
uu-remote quality status
uu-remote network
uu-remote logs
```

Failed relay components restart through the user service, which can cause a short reconnect. Preset rollback restores settings; runtime deployment uses its own recovery procedure. See [troubleshooting](troubleshooting.md) and [source build](source-build.md).

The main workflow is another UU device controlling Ubuntu. Ubuntu's Wine client controlling another computer has separate quality limits. Physical-monitor off/on and virtual outputs are pending on this host; see [Ubuntu 26.04 notes](ubuntu-26.04-port.md). The phone → ToDesk → Mac → UU chain still has a repeated-text issue; direct phone and Mac text input work.
