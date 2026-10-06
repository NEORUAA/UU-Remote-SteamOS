# Native capture experiments on the common Plus base

The tested desktop reference uses legacy input, an RDP video relay and four
canvas sizes ending at 4K. This is distinct from [fresh-install defaults](architecture.md#defaults-and-supported-branches).
The CPU and GPU adapters are optional developer prototypes. Their intended
comparison shares a verified Plus UU, terminal, clipboard and input base;
only the capture producer and adapter should differ. Such a matched real
controller comparison has not yet been completed. Wine 11.0 stays installed.

The CPU producer and capture adapter are adapted from the MIT-licensed uur
sources in `vendor/uur-native-cpu`. The producer negotiates Portal-authorized
PipeWire frames in CPU memory and publishes a three-slot shared file. The
capture-only DLL replaces screen BitBlt/StretchBlt data and makes DXGI capture
fall back to that GDI path. It installs no SendInput hook. When several buffers
are pending, the producer keeps the latest one to avoid processing old frames.

The GPU producer and interop backend are the separate AGPL-3.0 component in
`vendor/uuway-gpu-component`; its source receipts and full license are bundled.
Its intended path imports DMA-BUF into Vulkan, performs GPU copies into a DXVK
D3D11 capture texture, and supplies DXGI duplication frames to UU. The same MIT
capture adapter is built with a GPU selector that calls the independent
component's endpoint constructor. No whole UUWay application, input layer,
installer, Wine build or Mutter replacement is used. These are GPU copies, so
this is not a zero-copy claim. The runtime must prove DMA-BUF negotiation and
the actual UU encoder path separately.

## Local commands

Development headers and pinned Wine/DXVK/NVENC inputs are extracted under
`build/native-deps`; the build scripts install no system or live prefix files.

```sh
scripts/build-native-cpu.sh
scripts/build-native-gpu.sh
/usr/bin/python3 scripts/test-native-cpu.py
/usr/bin/python3 scripts/test-native-gpu.py
```

`scripts/uu-native-video.py` prepares one private prefix from the installed Plus
base. That prefix contains account state and must stay private. Both backend commands can reuse it, but an existing lab is not evidence that
it still matches the installed source. Validate the common runtime files and
installed digest, and prepare a fresh private base after source changes.
Preparing the lab does not start UU or request screen sharing.

```sh
/usr/bin/python3 scripts/uu-native-video.py prepare \
  --lab "$HOME/.local/state/uu-remote-native-lab"
```

The following runs request sharing the selected physical monitor via the Portal
and then attach a native capture DLL to the private Plus UU process. They are
experimental runs, not verified deployment commands. The committed short-run interface is a
developer tool: its duration is not an accepted controller-ready measurement
window. Coordinate the controller
and stop the live bridge during the private UU comparison, since the cloned
account/device state must not compete with the live instance. Restore the live
bridge after the comparison. Use the same physical monitor, 4K mode and short
scroll/window-drag sequence for each run.

```sh
/usr/bin/python3 scripts/uu-native-video.py run --backend cpu \
  --lab "$HOME/.local/state/uu-remote-native-lab" --seconds 12
/usr/bin/python3 scripts/uu-native-video.py run --backend gpu \
  --lab "$HOME/.local/state/uu-remote-native-lab" --seconds 12
```

The supervisor stops only its owned process groups and Wine prefix. It writes
logs in the private lab and closes its own Portal session. It does not alter the
production video setting or replace system Wine. Actual reconnection, capture
and encoder acceptance are still required before either native backend can be
recommended as a production option.

## Current evidence

The CPU probe verifies every RGB pixel of a 3840×2160 synthetic shared-memory
frame through the Wine GDI boundary, including imported and dynamically looked
up BitBlt calls. Its copy timings measure that local consumer operation only.

The GPU probe verifies Wine 11/DXVK 3.1 shared-texture interop on the RTX 5000 Ada,
an exact Vulkan/CUDA device UUID match, persistent H.264 and HEVC NVENC sessions,
changing frames and caller-state preservation. Decoding both bitstreams confirms
five 3840×2160 frames per codec. This is a synthetic hardware proof; it does not
prove a live Portal DMA-BUF frame reaches UU or lower Mac latency.

Portal CreateSession and SelectSources work on this host's ScreenCast v5. The
session was closed without Start or a sharing dialog. A real monitor consent,
CPU and GPU stream negotiation, native adapter attachment to UU and a short
controller comparison remain pending. Private development receipts are not public deployment artifacts.

A useful comparison must bind the lab to the same completed Plus baseline,
start its measurement only after the real controller connects, use identical
monitor/canvas/motion settings, and confirm restoration of the reference bridge.
The existing local probes and short-run commands do not establish this full
sequence. No FPS, latency percentage or production readiness is claimed.
