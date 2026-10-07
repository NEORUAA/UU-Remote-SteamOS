#!/usr/bin/env bash
set -Eeuo pipefail
unset CFLAGS CPPFLAGS LDFLAGS CPATH C_INCLUDE_PATH LIBRARY_PATH CXXFLAGS \
    OBJC_INCLUDE_PATH COMPILER_PATH GCC_EXEC_PREFIX ASFLAGS
export SOURCE_DATE_EPOCH="${SOURCE_DATE_EPOCH:-1}"
repo_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
output_dir="${1:-$repo_dir/build/compat}"
cc="${MINGW_CC:-x86_64-w64-mingw32-gcc}"
pe_strip="${MINGW_STRIP:-x86_64-w64-mingw32-strip}"
host_cc="${HOST_CC:-gcc}"
host_strip="${HOST_STRIP:-strip}"
for tool in "$cc" "$pe_strip" "$host_cc" "$host_strip"; do
    command -v "$tool" >/dev/null || { printf 'Missing build tool: %s\n' "$tool" >&2; exit 1; }
done
common=(-std=c11 -O2 -Wall -Wextra -Werror)
pe_link=(-Wl,--no-insert-timestamp)
mkdir -p "$output_dir"
# All SteamOS input goes to the native desktop relay, including Windows input.
"$cc" "${common[@]}" "${pe_link[@]}" -DUURB_FORCE_INPUT_BROKER=1 -shared \
    -o "$output_dir/uu-input-bridge.dll" "$repo_dir/src/uu_input_bridge_legacy.c" \
    "$repo_dir/src/uurb_ready.c" -luser32
"$cc" "${common[@]}" "${pe_link[@]}" -shared \
    -o "$output_dir/uu-cursor-guard.dll" "$repo_dir/src/uu_cursor_guard.c" -luser32 -lgdi32
"$cc" "${common[@]}" "${pe_link[@]}" -municode -mwindows \
    -o "$output_dir/uu-input-broker.exe" "$repo_dir/src/uu_input_broker.c" \
    "$repo_dir/src/uurb_rdp_backend.c" "$repo_dir/src/uurb_ready.c" \
    "$repo_dir/src/full-input.c" -luser32 -lws2_32
"$cc" "${common[@]}" "${pe_link[@]}" -municode \
    -o "$output_dir/uu-injector.exe" "$repo_dir/src/uu_injector.c"
"$cc" "${common[@]}" "${pe_link[@]}" -mwindows \
    -o "$output_dir/uu-healthd-stub.exe" "$repo_dir/src/winlogon.c"
"$pe_strip" "$output_dir/uu-input-bridge.dll" "$output_dir/uu-cursor-guard.dll" \
    "$output_dir/uu-input-broker.exe" "$output_dir/uu-injector.exe" "$output_dir/uu-healthd-stub.exe"
cp "$output_dir/uu-healthd-stub.exe" "$output_dir/winlogon.exe"
"$host_cc" "${common[@]}" -o "$output_dir/uu-x11-input" "$repo_dir/src/uu_x11_input.c" -ldl
"$host_cc" "${common[@]}" -fPIC -shared -o "$output_dir/uu-krdp-input-auth.so" \
    "$repo_dir/src/uu_krdp_input_auth.c" -ldl -pthread
"$host_strip" "$output_dir/uu-x11-input" "$output_dir/uu-krdp-input-auth.so"
printf 'SteamOS compatibility tools built in %s\n' "$output_dir"
