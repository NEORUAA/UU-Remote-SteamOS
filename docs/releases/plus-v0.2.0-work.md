# UU Remote Ubuntu Plus 0.2.0-work

Updated 2026-10-06. This development source follows tagged Plus 0.1.0; it does
not create a new release tag. See the [illustrated update](../updates/2026-10-06.md)
for real-session results and the remaining checks.

## Terminal session

`UURB_TERMINAL_SESSION_MODE=persistent` attaches UU terminal windows to the
same independent `main` tmux workspace. Closing a controller connection or
reaching transport EOF detaches the client while preserving the shell, working
directory and jobs. `exit` or Ctrl-D still closes the shell. Fresh sessions
remain the install default. A bridge service restart, logout or reboot is
outside this persistence guarantee.

The terminal proxy preserves raw terminal bytes through the ConPTY compatibility
path and uses a local authenticated broker. Session mode is carried by the
handoff; recovery targets only the owned UU MUX. A real Mac close/reopen cycle
on the current source retained the shell, directory and background job.
Ordinary input, Ctrl-C, resize and clear passed. Rapid batch input remains
unresolved. Configuration and shared-workspace behavior are described in the
[terminal guide](../native-ubuntu-terminal.md#keep-the-terminal-across-reconnects-opt-in).

## Clipboard images and text

The native owner handles UTF-8 text and image exchange, preserving original PNG
bytes alongside Win32 DIBV5/DIB offers. It accepts common 24/32-bit DIB and
DIBV5, and prefers an original DIB over a stale synthesized Wine V5 cache.
While the extended companion is active, RDP CLIPRDR is disabled to avoid two
clipboard authorities overwriting new copies. If the native companion is
unavailable at startup, the original RDP clipboard remains available.

Local isolated checks validate exact media bytes and bitmap pixels. They do
not establish every real controller path. A historical Ubuntu → Mac sample
passed; newer reverse-image freshness and color acceptance remains pending.
A failed 24-bit trial was reverted. Do not treat the historical result as
current complete bidirectional image acceptance.

The [optional Mac helper](../macos-clipboard-compat.md) adds TIFF to ordinary
PNG copies while preserving their original bytes. Its settings UI and normal
PNG controller path passed historical checks. The reference helper is currently
**not running**, with its saved preference still enabled. This companion is
separate from the official Mac UU application.

## Incoming multi-file copy

Incoming CF_HDROP and OLE FileGroupDescriptorW lists are supported, with
FileContents provided as IStream or HGlobal. Files arrive in 64 KiB chunks under
`~/.local/share/uu-remote/clipboard-files/copy-*/`. Linux `text/uri-list` and
GNOME copied-file formats are published only after the whole batch completes.
Copies use new staging directories; duplicate names receive numeric suffixes.
Completed files can be pasted into a file manager and remain staged until
manually removed. Outgoing files and directory copies are not implemented.
Limits are **64 MiB per file, 64 files and 256 MiB per copy**; images are limited
to 16 million decoded pixels.

The non-focusing **UU 文件接收** window reports the current filename, i/N and
actual file/batch bytes. Unknown totals stay indeterminate. Completion is shown
for five seconds; failure remains visible until dismissed. An interrupted
transfer removes the unfinished batch. A new native Ubuntu copy cancels that
batch and keeps the new clipboard selection. Counters measure bytes received
by the bridge; UU's earlier delayed-file fetching exposes no byte counter.
Metadata is written to `~/.local/state/uu-remote-bridge/clipboard-transfer.json`.

A real Mac → Ubuntu transfer delivered **two files totaling 2,228,224 bytes**
with both source SHA-256 hashes matching and actual progress displayed.
Focused probes separately cover partial transfers, unknown totals, native-copy
cancellation and stale completion rejection. Those probes do not imply that
every interruption case has been repeated through a real Mac controller.

The helper uses system Python, python3-xlib, python3-pil, python3-gi and
GTK 3 introspection. Upgrade and rollback snapshots include it. Clipboard
status records direction, dimensions or file size and hashes, rather than text
or image contents. `native-to-wine-prepared` denotes source preparation;
controller acceptance needs a separate observation.

## Experimental capture and focus

Optional [native CPU and GPU capture](../native-video-backends.md) have local
synthetic checks. The CPU adaptation is MIT; the independent GPU component is
AGPL-3.0 with source and licensing receipts included. Neither is installed by
default. A matched Portal → UU → Mac comparison remains pending, so no real
controller FPS or latency gain is claimed.

Management windows retain independent capture. Dual-controller focus loss is
unresolved. Recent focus/public-input trial candidates are excluded from this
source update; the rejected public-input trial was rolled back. The tested
reference remains legacy input, RDP and four canvas sizes ending at 4K.
[New-install defaults](../architecture.md#defaults-and-supported-branches)
remain a separate configuration choice.

## Build and acceptance scope

Reference real-session checks used Ubuntu 26.04 / GNOME 50, Wine 11 and Windows
UU 4.42.0.2770 with Mac UU. The Ubuntu 24.04 installer target is retained; it
did not receive a new end-to-end check in this update. Other controller/platform
combinations require their own acceptance.

FreeRDP's thirteen PE products retain their verified hashes and pinned build
recipe. Existing outputs are reused through the normal source-build verification
path; this update is not a new cold FreeRDP build. Upstream release notes and
the published Plus 0.1.0 tag remain historical records.
