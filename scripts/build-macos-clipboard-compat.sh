#!/usr/bin/env bash
set -euo pipefail
repo_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
if [[ "$(uname -s)" != Darwin ]]; then
    printf '%s\n' 'Build this AppKit helper on the Mac controller.' >&2
    exit 1
fi
output_dir="${1:-$repo_dir/build/macos}"
app="$output_dir/UU Clipboard Compat.app"
mkdir -p "$app/Contents/MacOS"
/usr/bin/xcrun swiftc -parse-as-library -swift-version 5 -O \
    "$repo_dir/src/macos_clipboard_compat.swift" -framework AppKit \
    -o "$app/Contents/MacOS/UUClipboardCompat"
cat >"$app/Contents/Info.plist" <<'PLIST'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
<key>CFBundleIdentifier</key><string>io.llmir.uu-clipboard-compat</string>
<key>CFBundleName</key><string>UU Clipboard Compat</string>
<key>CFBundleExecutable</key><string>UUClipboardCompat</string>
<key>CFBundleVersion</key><string>0.2.0</string>
<key>CFBundlePackageType</key><string>APPL</string>
<key>LSUIElement</key><true/>
<key>LSMinimumSystemVersion</key><string>13.0</string>
</dict></plist>
PLIST
/usr/bin/codesign --force --sign - "$app"
printf '%s\n' "$app"
