[English](performance-evidence.md) · [العربية](i18n/ar/performance-evidence.md) · [Deutsch](i18n/de/performance-evidence.md) · [Español](i18n/es/performance-evidence.md) · [Français](i18n/fr/performance-evidence.md) · [日本語](i18n/ja/performance-evidence.md) · [한국어](i18n/ko/performance-evidence.md) · [Русский](i18n/ru/performance-evidence.md) · [Tiếng Việt](i18n/vi/performance-evidence.md) · [简体中文](i18n/zh-Hans/performance-evidence.md) · [繁體中文](i18n/zh-Hant/performance-evidence.md)

[Home](../README.md)

# Experience and performance

![Chinese input, clipboard and management-window improvements](images/experience-refinements-en.png)

[Editable SVG](images/experience-refinements-en.svg)

![Pixel areas and choices for four canvases](images/canvas-pixel-scale-en.png)

[Editable SVG](images/canvas-pixel-scale-en.svg)

Choose a canvas for your screen and connection. Plus offers 720p, 1080p, 1440p and 4K; UU's quality, requested FPS and bitrate ceiling remain separate controls.

## Current development status · 2026-10-06

Persistent terminal reattachment and incoming two-file copies have real Mac
acceptance. Current image synchronization and dual-controller focus are still
open. Native CPU/GPU results are local synthetic checks; no matched real Mac
latency or FPS benefit has been measured. See the [illustrated update](updates/2026-10-06.md).
The earlier everyday feedback below does not replace these current boundaries.

## Improvements in everyday use

Recent refinements focus on Chinese input, text paste and window handling.

| Scene | Context | Earlier experience | Improved experience |
| --- | --- | --- | --- |
| Phone Chinese | Earlier Plus phone input | Some text submitted from the phone did not reach the desktop correctly | Chinese text submitted over a direct phone connection reaches the Ubuntu desktop correctly |
| Copy/paste | Earlier Plus text relay | Pasting could still insert older text after a new copy | Newly copied text refreshes for desktop paste; ordinary computer text copy/paste works |
| UU settings/popups | Earlier Plus management view | Management windows could overlap the desktop image or leave focus in the wrong place | Settings stay separate from the desktop image; dual-controller focus loss remains unresolved |
| Clarity/canvas | Plus canvas experiment | Enlarging the tested 4K source added no detail and looked worse | Four presets show the complete desktop and restore the saved size; 4K is the useful maximum for the tested source |
| Reconnect | Mac UU client update | The Mac UU update called for checking everyday desktop use | Reconnect, direct Chinese input and text paste continue to work after the update; the 4K experience feels similar |

The [comparison](upstream-comparison.md) separates the upstream foundation, newer-version compatibility, Plus additions and repairs during Plus use.

![Upstream foundations, Plus changes and design expectations](images/uu-plus-evolution-en.png)

[Editable SVG](images/uu-plus-evolution-en.svg)

**Design expectation:** timely text refresh can reduce repeated paste attempts; focus restoration during controller switching still needs verification. A smaller canvas supplies fewer pixels per frame; visible responsiveness also depends on capture, encoding, network and controller display.

## Canvas pixels and selection

| Canvas | Pixels per frame | Relative to 1080p |
| --- | ---: | ---: |
| 1280 × 720 | 921,600 | 0.44× |
| 1920 × 1080 | 2,073,600 | 1.00× |
| 2560 × 1440 | 3,686,400 | 1.78× |
| 3840 × 2160 | 8,294,400 | 4.00× |

These are pixel-area ratios. Capture may process the full source desktop; compression, motion and network conditions affect actual load. Smart sizing fits the complete desktop without changing the physical resolution.

| Control | Use |
| --- | --- |
| Ubuntu canvas | Relay image size; start at 1080p, choose 4K for fine text/workspace |
| Controller quality/FPS/True Color | Compression, requested updates and supported color mode |
| `uu-remote quality bitrate 20` | 20 Mbps ceiling; `0` removes it. Tight limits can soften motion |

See [quality settings](quality-guide.md) for menus, commands and recovery.

## Source-build cost

A complete clean-source build, including bootstrap and checks, produced:

| Item | Observed result |
| --- | --- |
| Elapsed time | 699.851 s, about 11 min 40 s |
| Resource limits | Two-core-equivalent CPU quota; 4 GiB memory ceiling |
| Reported peak memory | About 1.8 GB, rounded service-manager reading |
| Reported swap | 0 bytes |
| Output | 13 Windows runtime binaries |
| Reproducibility | Fixed inputs produced identical binary bytes across source/output directories |

The normal source entry uses normalized paths and explicit configuration. Downloads and compiler availability affect build time on a new machine. Verified output can be reused; see [source build](source-build.md).

## Environments and matched measurement

| Environment | Ubuntu | GNOME | Windows UU |
| --- | --- | --- | --- |
| Upstream reference | 24.04 | 46 | 4.33.0.8907 |
| Plus local observations | 26.04 | 50 | 4.42.0.2770 |

Existing records contain no matched fixed-upstream-versus-Plus controller FPS or input-to-visible-screen latency measurement. Relay timing and CPU-quota experiments are component measurements.

Fix host/controller versions, source resolution, application, network, UU quality, requested FPS and bitrate. Run the pinned upstream and Plus in separate disposable environments, accounting for upstream's 24.04 installer boundary. Time a defined input action until the visible controller response; count visible controller updates in a repeatable moving scene. Repeat runs, report their spread and text clarity, and retain the measurement method with the results.
