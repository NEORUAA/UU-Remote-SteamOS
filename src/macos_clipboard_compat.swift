import AppKit

// UU's Windows clipboard maps TIFF to DIB, but a PNG-only Mac source can be
// ignored before any Windows format is offered. This helper adds a TIFF flavor.
@MainActor
final class ClipboardCompat: NSObject, NSApplicationDelegate {
    private let defaults = UserDefaults.standard
    private let preference = "imageCompatibilityEnabled"
    private var enabled = false
    private var seenChange = -1
    private var timer: Timer?
    private var statusItem: NSStatusItem!
    private let toggleItem = NSMenuItem(title: "Enable PNG compatibility", action: nil, keyEquivalent: "")
    private let resultItem = NSMenuItem(title: "Waiting for a PNG image", action: nil, keyEquivalent: "")
    private let maxBytes = 64 * 1024 * 1024
    private let maxPixels = 16_000_000
    private let nonImageTypes: Set<String> = [
        "public.file-url", "NSFilenamesPboardType", "com.apple.pasteboard.promised-file-url",
        "public.utf8-plain-text", "public.utf16-plain-text", "public.plain-text",
        "NSStringPboardType", "public.url", "public.html", "public.rtf", "com.apple.flat-rtfd"
    ]

    func applicationDidFinishLaunching(_ notification: Notification) {
        if CommandLine.arguments.contains("--enable") { defaults.set(true, forKey: preference) }
        if CommandLine.arguments.contains("--disable") { defaults.set(false, forKey: preference) }
        enabled = defaults.bool(forKey: preference)
        statusItem = NSStatusBar.system.statusItem(withLength: NSStatusItem.variableLength)
        statusItem.button?.title = "UU Clip"
        let menu = NSMenu()
        toggleItem.target = self
        toggleItem.action = #selector(toggle)
        menu.addItem(toggleItem)
        resultItem.isEnabled = false
        menu.addItem(resultItem)
        menu.addItem(.separator())
        let quit = NSMenuItem(title: "Quit", action: #selector(quitHelper), keyEquivalent: "q")
        quit.target = self
        menu.addItem(quit)
        statusItem.menu = menu
        updateToggle()
        timer = Timer.scheduledTimer(timeInterval: 0.15, target: self,
                                    selector: #selector(poll), userInfo: nil, repeats: true)
    }

    private func updateToggle() {
        toggleItem.state = enabled ? .on : .off
        statusItem.button?.toolTip = enabled ? "UU PNG clipboard compatibility enabled" : "UU PNG clipboard compatibility disabled"
    }

    @objc private func toggle() {
        enabled.toggle()
        defaults.set(enabled, forKey: preference)
        seenChange = -1
        updateToggle()
    }

    @objc private func quitHelper() { NSApp.terminate(nil) }

    @objc private func poll() {
        guard enabled, NSWorkspace.shared.runningApplications.contains(where: {
            $0.executableURL?.lastPathComponent == "UURemote" || $0.localizedName == "UU远程"
        }) else { return }
        let board = NSPasteboard.general
        let change = board.changeCount
        guard change != seenChange else { return }
        seenChange = change
        guard let items = board.pasteboardItems, items.count == 1 else { return }
        let source = items[0]
        guard !source.types.contains(where: { nonImageTypes.contains($0.rawValue) }),
              source.types.contains(.png), !source.types.contains(.tiff) else { return }
        guard let png = source.data(forType: .png), png.count <= maxBytes,
              let image = NSBitmapImageRep(data: png), image.pixelsWide > 0,
              image.pixelsHigh > 0, image.pixelsWide <= maxPixels / image.pixelsHigh,
              let tiff = image.representation(using: .tiff, properties: [:]),
              tiff.count <= maxBytes else {
            resultItem.title = "Image unavailable or exceeds bridge limits"
            return
        }
        // Do not replace a newer user copy made while decoding the image.
        guard board.changeCount == change else { return }
        let replacement = NSPasteboardItem()
        replacement.setData(tiff, forType: .tiff)
        replacement.setData(png, forType: .png)
        board.clearContents()
        if board.writeObjects([replacement]) {
            resultItem.title = "Added TIFF: \(image.pixelsWide)×\(image.pixelsHigh)"
        } else {
            board.setData(png, forType: .png)
            resultItem.title = "Clipboard write failed"
        }
        seenChange = board.changeCount
    }
}

@main
struct Main {
    @MainActor static func main() {
        let app = NSApplication.shared
        let helper = ClipboardCompat()
        app.delegate = helper
        app.setActivationPolicy(.accessory)
        withExtendedLifetime(helper) { app.run() }
    }
}
