# UU Remote Ubuntu Plus 0.2.0-work

This working version adds native terminal session persistence, bidirectional
bitmap clipboard, and incoming multi-file clipboard to the existing Plus
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
Bitmap reads retain the owner's DIB publication order: a synthesized Wine V5
cache must not take priority over a newly rendered original DIB.

Incoming files support CF_HDROP and OLE FileGroupDescriptorW lists, with
FileContents supplied as IStream or HGlobal. Files are received in 64 KiB
chunks into `~/.local/share/uu-remote/clipboard-files/copy-*/`; only after the
entire batch is complete are `text/uri-list` and GNOME's copied-file format
published. A new directory for each copy prevents overwriting prior files;
duplicate names within a batch receive a numeric suffix.
Users can paste the file into a file manager. Staged files remain until manually
removed; remove them after pasting or when those clipboard references are no
longer needed. Directory copies and outgoing file transfer are not implemented.
Each file is limited to 64 MiB, with up to 64 files and 256 MiB per copy. Images
remain limited to 16 million pixels.

A non-focusing **UU 文件接收** window shows the current filename and i/N,
actual received/total bytes and percentages for the file and batch. Unknown
totals stay indeterminate. Completion is displayed for five seconds; failure
remains visible until dismissed. Interrupted copies remove the entire unfinished
batch and leave the prior clipboard available. A new copy in a native Ubuntu
application also cancels the batch and keeps the new clipboard selection.
Counters measure bytes received
by this bridge; UU's earlier fetching of a delayed file does not expose a byte
count. Local progress metadata is saved in
`~/.local/state/uu-remote-bridge/clipboard-transfer.json`.

The helper requires system Python with python3-xlib, python3-pil, python3-gi and
gir1.2-gtk-3.0. Upgrade and
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

On the current host, terminal reattachment and an incoming single file passed
their acceptance checks. A distinct 43×29 Ubuntu image also reached the Mac
with identical RGB pixels. Ordinary PNG-only Mac copies did not produce a
Windows image offer. A distinct Mac TIFF-only 47×31 image then reached Ubuntu
and an actual Wayland GTK consumer with identical RGB pixels. A second 53×37
Mac source advertised TIFF first alongside its original PNG; Ubuntu again
received identical RGB pixels. The original PNG need not be removed.

The [optional Mac compatibility helper](../macos-clipboard-compat.md) preserves
pure PNG bytes and adds TIFF automatically, with an enable/disable menu switch.
Its first version compiled on the actual Mac. A settings window has since been
added for GUI enabling; that revision and its ordinary Preview-copy path await
Mac acceptance. The previous one-way RDP experiment
was rolled back and is not part of this repair. The 19 isolated clipboard checks
pass, including actual multi-file bytes, unknown totals and disconnect cleanup.
A focused real X-selection probe also verifies that a native copy cancels an
unfinished batch, removes its staged files, rejects a stale END and preserves
the new native text. The initial multi-file version is installed with 27
readiness checks passing; two review corrections await the next serial update
and a real Mac two-file check. CPU/GPU prototypes still await actual Portal-to-UU integration and
controller latency comparison.

The upstream `docs/releases/v0.2.0.md` and published `v0.1.0` tag remain historical
records. `0.2.0-work` is a local working version pending controller acceptance.
