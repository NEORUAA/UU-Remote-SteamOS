#!/usr/bin/env bash
set -Eeuo pipefail
repo_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
headers="${UURB_PIPEWIRE_HEADERS:-$repo_dir/build/native-deps/sysroot/usr/include}"
stage="${1:-$repo_dir/build/native-cpu}"
mkdir -p "$stage"
gcc -std=gnu11 -O2 -Wall -Wextra -Werror \
    -isystem "$headers/pipewire-0.3" -isystem "$headers/spa-0.2" \
    -o "$stage/plus-pw-cpu" "$repo_dir/vendor/uur-native-cpu/capture/uur-pw-capture.c" \
    -l:libpipewire-0.3.so.0
x86_64-w64-mingw32-gcc -std=c11 -O2 -Wall -Wextra -Werror \
    -Wl,--no-insert-timestamp -shared -o "$stage/plus-cpu-capture.dll" \
    "$repo_dir/vendor/uur-native-cpu/hook/plus-cpu-capture.c" -lgdi32 -luser32 -lkernel32
printf 'Built isolated CPU producer and capture-only Plus adapter in %s\n' "$stage"
