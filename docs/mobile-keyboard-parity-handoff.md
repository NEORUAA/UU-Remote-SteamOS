[English](mobile-keyboard-parity-handoff.md) · [简体中文](i18n/zh-Hans/mobile-keyboard-parity-handoff.md)

[English · UU Remote Ubuntu Plus](../README.md)

# Keyboard compatibility checks

Use this guide when one controller or input method behaves differently from
another. Physical keys, the phone keyboard, dictation and clipboard paste can
use different delivery paths; test each separately.

## Settings to record privately

Record the host OS, desktop session, UU and controller versions, keyboard layout
and selected input route. Check `uu-remote quality status` and the saved bridge
configuration without publishing the complete configuration or controller IDs.

`UURB_TEXT_KEY_DELAY_MS` controls phone text pacing. Physical-key delay and
keyboard routing are separate settings. Existing installations retain their
saved values; do not copy another computer's timing profile as a presumed fix.
See [input behavior tracks](release-tracks.md) and
[adaptive keyboard relays](adaptive-keyboard-relays.md).

## Check the actual input methods

Use a disposable text receiver and a nonsensitive sample such as
`abcXYZ123,.!?`. Compare the intended text with the resulting content for:

- computer keyboard typing, modifiers and shortcuts;
- phone English and Chinese keyboards;
- committed dictation and multiline paste;
- ordinary copy/paste in both directions;
- a fresh controller connection and a reconnect.

Observe the intended application and focus before judging a paste failure.
If text arrives in another focused window, correct the test target rather than
attribute the result to the clipboard transport.

A broker accepting an event does not establish that the target application
received it. Keep content-free category, route, result count and error evidence
when diagnosing delivery. Never record key codes, typed text or clipboard
content in public logs. No replay after ambiguity: uncertain delivery must not
be retried automatically.

Change one route or timing setting at a time, retain the previous value and
verify from the real controller. For a stalled XRDP client, follow the ordering
in [XRDP keyboard recovery](xrdp-and-keyboard-recovery.md).

Do not commit a completed record. Public reports should contain versions,
settings and a sanitized symptom description; raw evidence stays private.
