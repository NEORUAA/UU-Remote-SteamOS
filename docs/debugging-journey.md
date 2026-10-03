[English](debugging-journey.md) · [中文（简体）](i18n/zh-Hans/debugging-journey.md)

[← English home](../README.md)

# Troubleshooting approach

Start with the component that matches the reported symptom. Keep detailed
incident records, private screenshots and raw logs outside the public source.
This guide describes reusable checks rather than a history of individual hosts.

## Separate the display paths

The desktop relay and the local UU management window are different views.
Confirm which window and desktop a screenshot shows before diagnosing a black
frame. Use [architecture](architecture.md) to locate the display path, and
[troubleshooting](troubleshooting.md) for the corresponding commands.

## Check input delivery

UU accepting a request, the broker accepting events and an application receiving
text are separate results. Check focus and the intended application. Physical
keys, phone text and paste require separate checks; see
[keyboard compatibility](mobile-keyboard-parity-handoff.md).

Change one setting at a time and retain the previous value. Do not mask a lost
input path with repeated text injection or a global delay. Follow
[XRDP recovery](xrdp-and-keyboard-recovery.md) when that session is affected.

## Distinguish source from installed files

Editing source or successfully compiling it does not update a running helper.
Use the installer or [runtime-only refresh](runtime-only-refresh.md), then run
`./scripts/verify.sh --quick`. A failed identity check is a reason to inspect
the installation, not a reason to disable validation.

## Restore service before changing the product

Use `uu-remote status` and private service logs to distinguish an inactive
service from an unavailable desktop or failed connection. See
[clean-exit recovery](clean-exit-recovery.md) for service lifecycle behavior.
Retain the working account, relay route and rollback material during diagnosis.

Public conclusions should describe the affected component, relevant versions
and the change that fixed it. Omit host identities, account/device IDs, raw
input, network topology and completed incident transcripts.
