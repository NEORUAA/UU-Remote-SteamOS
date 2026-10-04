#!/usr/bin/env bash
# Builds the separately licensed GPU component; installs no live runtime files.
set -Eeuo pipefail
repo_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
component="$repo_dir/vendor/uuway-gpu-component/src"
deps="$repo_dir/build/native-deps"
stage="${1:-$repo_dir/build/native-gpu}"
headers="$deps/sysroot/usr/include"
cuda="$deps/cuda-runtime/nvidia/cuda_runtime/include"
nvenc="$deps/nv-codec-headers/include"
wine_headers=( -I "$deps/wine-dev/usr/include/wine" -I "$deps/wine-dev/usr/include/wine/wine/windows" )
common=( -std=gnu11 -O2 -Wall -Wextra -Werror )
[[ "$(/opt/wine-stable/bin/wine --version)" == wine-11.0 ]]
mkdir -p "$stage/cursor-shaders"
for shader in vert frag; do
    LD_LIBRARY_PATH="$deps/sysroot/usr/lib/x86_64-linux-gnu" \
        "$deps/sysroot/usr/bin/glslangValidator" -V --target-env vulkan1.0 \
        --vn "uurb_cursor_${shader}_spv" "$component/shaders/native_cursor.$shader" \
        -o "$stage/cursor-shaders/native_cursor_${shader}.h"
done
gcc "${common[@]}" -isystem "$headers/pipewire-0.3" -isystem "$headers/spa-0.2" \
    -I "$headers" -I "$cuda" -I "$nvenc" -I "$stage/cursor-shaders" \
    "$component/uu_pipewire_native_probe.c" "$component/native_vk_dmabuf_import.c" \
    "$component/native_vk_capture_encode.c" "$component/native_cuda_encode_session.c" \
    "$component/native_gpu_frame_channel.c" "$component/native_cursor_metadata.c" \
    "$component/native_vk_cursor_composite.c" -o "$stage/plus-pw-gpu" \
    -l:libpipewire-0.3.so.0 -l:libvulkan.so.1 -lcuda -ldl -pthread
for source in native_cuda_frame_copy native_gpu_frame_channel; do
    gcc "${common[@]}" -fPIC -I "$cuda" -c "$component/$source.c" -o "$stage/$source.o"
done
gcc "${common[@]}" -fPIC -I "$deps/wine-11/include" \
    -c "$component/native_wine11_gpu_fd.c" -o "$stage/native_wine11_gpu_fd.o"
/opt/wine-stable/bin/winegcc -m64 -shared "${common[@]}" "${wine_headers[@]}" \
    -I "$headers" -o "$stage/uurb-dxgi-capture.dll" "$component/uu_dxgi_duplication.spec" \
    "$component/uu_dxgi_duplication.c" "$component/uu_d3d11_capture_texture.c" \
    "$stage/native_cuda_frame_copy.o" "$stage/native_gpu_frame_channel.o" "$stage/native_wine11_gpu_fd.o" \
    -ld3d11 -ldxgi -ldxguid -luuid -lntdll -lvulkan-1 -lcuda
x86_64-w64-mingw32-gcc "${common[@]}" -shared -Wl,--no-insert-timestamp \
    -o "$stage/uurb-dxgi-capture-loader.dll" "$component/uu_dxgi_duplication_loader.c"
x86_64-w64-mingw32-gcc "${common[@]}" -shared -Wl,--no-insert-timestamp -DUURB_NATIVE_GPU \
    -o "$stage/plus-gpu-capture.dll" "$repo_dir/vendor/uur-native-cpu/hook/plus-cpu-capture.c" \
    -lgdi32 -luser32 -lkernel32
x86_64-w64-mingw32-gcc "${common[@]}" -I "$nvenc" -Wl,--no-insert-timestamp \
    -o "$stage/plus-dxgi-consumer-probe.exe" "$component/uu_dxgi_capture_probe.c" \
    -ld3d11 -ldxgi -ldxguid -luuid
for source in native_cuda_encode_session native_cuda_encode_probe; do
    gcc "${common[@]}" -fPIC -I "$cuda" -I "$nvenc" \
        -c "$component/$source.c" -o "$stage/$source.o"
done
gcc "${common[@]}" -fPIC -I "$nvenc" \
    -c "$component/../tests/probes/nvenc_symbol_collision.c" -o "$stage/nvenc_symbol_collision.o"
/opt/wine-stable/bin/winegcc -m64 "${common[@]}" "${wine_headers[@]}" \
    -I "$headers" -I "$nvenc" -o "$stage/plus-gpu-interop-probe.exe" \
    "$component/uu_gpu_interop_probe.c" "$component/uu_d3d11_frame_adapter.c" \
    "$component/uu_d3d11_encode_session.c" "$stage/native_cuda_encode_session.o" \
    "$stage/native_cuda_encode_probe.o" "$stage/native_wine11_gpu_fd.o" \
    "$stage/nvenc_symbol_collision.o" \
    -ld3d11 -ld3dcompiler -ldxgi -ldxguid -luuid -lntdll -lvulkan-1 -ldl -lcuda -pthread
printf 'Built optional AGPL GPU capture/interop component in %s\n' "$stage"
