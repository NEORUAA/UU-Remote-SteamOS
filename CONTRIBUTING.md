[English](CONTRIBUTING.md) · [العربية](i18n/CONTRIBUTING.ar.md) · [Deutsch](i18n/CONTRIBUTING.de.md) · [Español](i18n/CONTRIBUTING.es.md) · [Français](i18n/CONTRIBUTING.fr.md) · [日本語](i18n/CONTRIBUTING.ja.md) · [한국어](i18n/CONTRIBUTING.ko.md) · [Русский](i18n/CONTRIBUTING.ru.md) · [Tiếng Việt](i18n/CONTRIBUTING.vi.md) · [简体中文](i18n/CONTRIBUTING.zh-Hans.md) · [繁體中文](i18n/CONTRIBUTING.zh-Hant.md)

[English · UU Remote Ubuntu Plus](README.md)

# Contributing to UU Remote Ubuntu Plus

Plus builds on [Lachlan Chen's MIT-licensed bridge](https://github.com/lachlanchen/uu-remote-ubuntu-bridge).
Preserve the original copyright notice, upstream technical history and license.
Contributions should be small, reproducible and clear about which host and
control direction they actually validate.

This project modifies version-locked behavior in proprietary software. A
new hash requires a new reverse-engineering review, not a routine dependency
bump. Never bypass approved manifests, full hashes or runtime checks to make
an installation appear successful.

## Start with the right scope

Use the [compatibility report form](https://github.com/llmir/uu-remote-ubuntu-plus/issues/new?template=compatibility.yml) for
sanitized bug reports and compatibility requests. Include Ubuntu, GNOME,
Wine and UU versions, bridge resolution/relay route, steps and observed
behavior. Distinguish these workflows:

- another UU device controlling Ubuntu as host;
- the local Ubuntu UU login/management window;
- Ubuntu's Wine UU client controlling another machine.

A successful result on one path does not validate the others. Report measured
inner-relay updates separately from actual controller FPS. Preserve a working
reconnect/recovery route when testing a live remote host.

## Portable development dependencies

Use an Ubuntu development environment and the distro Python 3. Native build
and isolated tests need GCC, MinGW-w64, Wine development tools and X11
utilities. A minimal source-test setup is:

```bash
sudo apt-get update
sudo apt-get install --no-install-recommends \
  build-essential binutils gcc-mingw-w64-x86-64-win32 \
  wine wine64 wine64-tools \
  xvfb x11-utils x11-xserver-utils xclip xcompmgr
```

The installed bridge additionally needs the dependencies declared by
`install.sh`; let the installer manage them on a supported host. These source
packages alone are not a complete production installation. For WineHQ builds,
`build-compat.sh` normally uses `/opt/wine-stable/bin/winegcc`; when testing a
distro Wine toolchain, select the actual compiler explicitly:

```bash
WINEGCC="$(command -v winegcc)" ./scripts/build-compat.sh
```

Use `MINGW_CC`, `MINGW_STRIP`, `HOST_CC` and `HOST_STRIP` only when selecting
an alternate available toolchain. Do not bake a maintainer's absolute paths
into production scripts. Isolated tests should create their own temporary
Wine prefixes/Xvfb displays and must not drive the logged-in user's desktop.

## Check source changes

Run source checks before requesting review:

```bash
while IFS= read -r file; do
  bash -n "$file" || exit
done < <(
  find . -type f \( -name '*.sh' \
    -o -path './scripts/uu-remote' \
    -o -path './scripts/uu-remote-bridge' \
    -o -path './scripts/uu-remote-console' \) \
    -not -path './build/*' -not -path './.git/*' -print
)
python3 -m compileall -q scripts tests
python3 -m unittest discover -s tests -v
./scripts/build-compat.sh
git diff --check
```

Use the distro Python explicitly if your shell defaults to a separate Conda
or virtual environment. Some tests need Wine, Xvfb or systemd; report skipped
capability tests rather than counting them as successful execution. Use
`UURB_TEST_SYSTEMD=1` only in an environment with a usable user-service bus.
The build uses strict C warning checks; keep them enabled.

For docs-only changes, run the documentation tests and inspect any rendered
images. Avoid adding test assertions whose only purpose is locking promotional
copy. Functional runtime, manifest and recovery checks must remain intact.

## Edit the technical illustrations

The data-flow and porting scenes combine PNG artwork with editable SVG labels
and routes in `docs/images/`. English and Simplified Chinese use the same layout.
Edit the corresponding `*-en.svg` and `*-zh-Hans.svg` files, then rebuild the
PNGs and looping GIFs with Node.js and Sharp:

```bash
npm install --no-save --package-lock=false sharp
node scripts/render-doc-graphics.cjs
```

The renderer embeds the local artwork while rendering, so the PNGs and GIFs
display directly in GitHub. Each GIF has 80 frames at 60 ms per frame (4.8 seconds per loop). The SVG
files keep their local artwork references for editing.

## Validate the installed runtime

After changing any runtime script or native component, install the new source
and run the existing verifier on an authorized supported test host:

```bash
./install.sh --skip-packages --skip-account-login
./scripts/verify.sh --quick
./uninstall.sh --dry-run
```

This can briefly disconnect UU. Arm an independent tested recovery mechanism
before experimental deployments, and keep a known working configuration.
The quality-preset rollback timer covers preset changes; it is not a safety
net for arbitrary runtime replacement. The source/runtime digest deliberately
fails after changes until the installer has refreshed the runtime.

For a lifecycle, capture, input or product-version change, also run the full
runtime verifier and perform visible controller acceptance. The full verifier
includes the 270-second stability interval. Do not weaken checks, skip them
silently or replace meaningful tests with stubs.

Terminate only the dedicated prefix with `scripts/stop-wine-prefix`, supplying
its prefix and wineserver path. Do not use broad `pkill wine` commands that
can stop unrelated applications.

## New UU releases

Follow [the upstream audit workflow](docs/upstream-maintenance.md). A release
contribution needs:

- an approved manifest with installer, original server, patched server and
  health-monitor SHA-256 identities;
- semantic rationale for every equal-length edit and updated relevant
  imports/landmarks;
- disposable patch/verify/byte-identical restore evidence;
- cold start, real controller mouse/keyboard, reconnect/restart and full
  stability results;
- verified uninstall restoration and login-preservation acceptance where
  promotion is requested.

Do not include NetEase executables, proprietary disassembly dumps, Wine
account state or raw private audit logs. Keep local evidence under ignored
`build/audits/`. A newly changed official installer hash is a reason to stop
and audit, never a reason to disable verification.

## Privacy and publication hygiene

Before committing, review `git status`, `git diff --cached` and the exact file
list. Never force-add ignored artifacts. In particular, exclude:

- `build/`, generated binaries, caches and Wine prefixes;
- `.omc/` operational state, private recovery snapshots and conversation logs
  (the explicitly allowed project skill directory is a separate source case);
- `docs/handoff-codex.md`, which is a private operator handoff;
- account/device identifiers, credentials, tokens, private hostnames or IP
  addresses, typed/clipboard content and raw production logs.

Documentation screenshots must be actual, explicitly sanitized captures.
Inspect the complete image and metadata; do not publish a desktop merely
because its central window looks harmless. Diagrams must be labeled as
illustrations rather than presented as performance or runtime evidence.

## Patch quality and review

Keep hooks narrow and return real API result/error shapes. Bound cross-process
requests before reading payloads. Do not log key codes, Unicode values,
pointer coordinates or clipboard data. Preserve authentication, TLS checks,
manifest approval, account state, user-level operation and reversible removal.

Ask for an independent review with the concrete problem, resulting behavior,
tests actually run and remaining limitations. Avoid claiming complete support
for a controller, codec, frame rate or headless configuration that was not
measured. See [the quality guide](docs/quality-guide.md) and
[port validation notes](docs/ubuntu-26.04-port.md) for current boundaries.
