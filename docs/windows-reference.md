[English](windows-reference.md) · [简体中文](i18n/zh-Hans/windows-reference.md)

[Home](../README.md)

# Windows reference comparison

Use a Windows installation of the same UU version to compare the host service, input devices and controller behavior with Wine.

## Installed layout

Find the installation through the Windows service's `PathName`. The following layout uses a generic example directory:

```text
C:\path\to\GameViewer
C:\path\to\GameViewer\bin\GameViewerService.exe --service
C:\path\to\GameViewer\bin\drivers\gvInput\gvinput.sys
C:\path\to\GameViewer\bin\drivers\gvInput\gvinputmf.sys
```

On Windows, `GameViewerService` and the `gvinput` drivers provide the kernel HID path. Device Manager and UU logs identify `ROOT\HIDCLASS` and `HID\GVINPUT` devices, including a keyboard collection. Wine uses the bridge's user-mode input path instead.

## Safe inspection commands

In PowerShell, inspect the service and read its executable path. Replace the example directory below with the installation root found in `PathName`:

```powershell
Get-Service GameViewerService
Get-CimInstance Win32_Service -Filter "Name='GameViewerService'" |
  Select-Object Name, State, PathName
$installRoot = 'C:\path\to\GameViewer'
Get-ChildItem (Join-Path $installRoot 'bin\drivers\gvInput')
Get-PnpDevice | Where-Object InstanceId -Match 'GVINPUT'
```

UU logs are under the installation's `log\server`, `log\service` and `log\client` directories. Compare the relevant service and input status; remove account and device data before sharing excerpts.

## End-to-end controller test

Use the Windows UU application to open the Ubuntu device. Confirm the live desktop, mouse clicks, a fresh terminal, keyboard shortcuts and text input. Disconnect and reconnect once, then check that the same desktop remains usable. Observe the service over a longer session alongside the controller behavior.

## Repository and installed files

The repository contains the bridge's user-mode implementation. Windows `gvinput` drivers, certificates, NetEase binaries and account state remain with their respective installations.
