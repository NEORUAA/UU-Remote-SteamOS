# UU Remote Ubuntu Plus 0.2.0-work

This working version adds native terminal session persistence, bidirectional
bitmap clipboard, and incoming single-file clipboard to the existing Plus
bridge. It retains the legacy input route, RDP desktop relay, four resolution
choices ending at 4K, Wine 11.0 and the audited UU 4.42 runtime.

## Terminal session

`UURB_TERMINAL_SESSION_MODE=persistent` attaches terminal windows to the same
`main` tmux workspace. Closing a controller connection or reaching transport
EOF detaches the client while preserving the shell, working directory and jobs.
Typing `exit` or Ctrl-D still closes the shell. The install default is `fresh`;
the current test host enables `persistent`. A full bridge service restart,
logout or reboot is outside this persistence guarantee.

## Clipboard

The native owner publishes `image/png` and accepts PNG, common 24/32-bit DIB,
and DIBV5 from Wine. Native PNG copies are converted to Win32 DIBV5 and DIB for
the controller. UTF-8 text also travels in both directions through this native
owner. While the extended companion is active, RDP CLIPRDR is disabled so the
same image does not return through a second clipboard channel and overwrite a
new controller copy. RDP still carries desktop video and physical input; if
the native companion is unavailable at startup, its original clipboard remains
enabled.

Incoming files support exactly one CF_HDROP file or one OLE
FileGroupDescriptorW with FileContents supplied as IStream or HGlobal. A
complete file is staged in `~/.local/share/uu-remote/clipboard-files/copy-*/`;
only then are `text/uri-list` and GNOME's copied-file format published. A new
directory for each copy prevents duplicate names from overwriting prior files.
Users can paste the file into a file manager. Staged files remain until manually
removed; remove them after pasting or when those clipboard references are no
longer needed. Directory copies, multiple files and outgoing file transfer are
not implemented. Payloads are limited to 64 MiB and images to 16 million pixels.

The helper requires system Python with python3-xlib and python3-pil. Upgrade and
rollback snapshots include the helper. Clipboard metadata in
`~/.local/state/uu-remote-bridge/clipboard-status.json` records direction,
dimensions or file size and hashes; it does not record text or image contents.
`native-to-wine-prepared` means the native image was prepared for transport;
controller acceptance requires a separate observation.

## Validation and deployment

The isolated Wine/Xvfb probe verifies different exact bitmap pixels in both
directions, CF_HDROP and OLE IStream file contents, Linux URI publication,
same-image copying after foreign text, duplicate names, partial transfers and
invalid file names. The authenticated terminal probe verifies reattachment to
the same shell, preserved working directory/jobs, EOF detach, resizing, removed
transport credentials and unchanged fresh mode.

These probes do not establish a real Mac controller result. The local deployment
receipt records that acceptance separately, alongside installed file hashes,
saved settings and an exact rollback command. FreeRDP's thirteen PE products
are reused only after checking their fixed hashes and build recipe through the
normal source-build reuse path; this is not a new cold build.

The upstream `docs/releases/v0.2.0.md` and published `v0.1.0` tag remain historical
records. `0.2.0-work` is a local working version pending controller acceptance.
