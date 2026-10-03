[English](macos-current-desktop.md) · [简体中文](i18n/zh-Hans/macos-current-desktop.md)

[English · UU Remote Ubuntu Plus](../README.md)

# macOS current-desktop access

The bridge already occupies GNOME's desktop-sharing RDP connection. A second
RDP client is not a way to join that same desktop. GNOME remote login creates
a separate session instead.

For authorized access to the existing desktop, use the bridge's local VNC view
through native SSH. The example alias `desktop-host` must be configured for
your own host with verified host keys and SSH key authentication.

## Start the desktop view

On Ubuntu, from the logged-in user's session:

```bash
uu-remote-console relay
```

The helper locates the existing desktop relay and starts its authenticated VNC
view on `127.0.0.1:5922`. It uses the bridge's keyring credential and does not
open a LAN listener. The local VNC authentication file is private; SSH is the
network access boundary.

On the Mac, keep this SSH forward open:

```bash
ssh -N -o ExitOnForwardFailure=yes \
  -L 15922:127.0.0.1:5922 desktop-host
```

Then open Screen Sharing:

```bash
open vnc://127.0.0.1:15922
```

Enter the configured bridge password when requested. Use macOS Keychain only
if retaining that credential on this Mac is appropriate. Do not include the
password, alias or actual host details in a public support record.

## Optional launcher

For a reusable Mac app, edit `scripts/macos-connect.applescript` before compiling
it with `osacompile`. Set its `targetName`, `targetHost`, `sshAlias` and
`rdpUsername` properties to your own authorized target. The shipped values are
examples. Verify the SSH alias and host key before use; keep account-specific
copies and generated apps private.

## Close and diagnose

Closing the viewer ends its desktop interaction; closing SSH removes the
forward. The relay helper exits after the last viewer disconnects.
It does not start another RDP session or stop the desktop bridge.

For a connection failure, confirm the Ubuntu helper is running and the Mac
forward exists. If the view contains a recursive desktop, close any reverse
viewer showing the Mac from Ubuntu. Use GNOME remote login only when a separate
login session is intended. See [SSH setup](ssh-and-port-mapping.md).
