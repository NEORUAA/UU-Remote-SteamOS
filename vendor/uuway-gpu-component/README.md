# Optional native GPU component

This is a source subset from the fixed upstream commit in `SOURCE.json`, under
the bundled GNU AGPL version 3. Its source and license must accompany this
component, including any changes. It is an independently built optional
PipeWire/Vulkan/CUDA capture worker and DXGI interop plugin for the Plus bridge.
The Plus terminal, clipboard, input and RDP implementation stays in the common
base. No upstream installer, whole application, settings service, Wine build,
Mutter build or input/clipboard implementation is included.

The intended path is Portal-authorized DMA-BUF → Vulkan texture → CUDA GPU copy
→ DXVK D3D11 capture texture → UU's existing capture and encoder. This path uses
GPU copies; it must not be described as zero-copy or CPU-free until runtime
evidence establishes the negotiated buffer type and GPU interop success. It
does not replace the stable RDP default. Sources compile through
`scripts/build-native-gpu.sh`; external development inputs stay in
`build/native-deps`, and live Wine files are not changed by the build.

Wine server protocol 930, Wine 11.0 and DXVK 3.1 are explicit compatibility
constraints of this component. Successful compilation does not establish a
working UU video connection, native DMA-BUF negotiation, GPU synchronization,
hardware encoding, or lower controller latency.
