from __future__ import annotations

import re
import unittest
from pathlib import Path
from urllib.parse import unquote, urlparse


REPO_DIR = Path(__file__).resolve().parent.parent
MARKDOWN_LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
TRANSLATIONS = {
    "README.ar.md",
    "README.de.md",
    "README.es.md",
    "README.fr.md",
    "README.ja.md",
    "README.ko.md",
    "README.ru.md",
    "README.vi.md",
    "README.zh-Hans.md",
    "README.zh-Hant.md",
}


class DocumentationTests(unittest.TestCase):
    def test_all_local_markdown_links_resolve(self) -> None:
        failures: list[str] = []
        for document in REPO_DIR.rglob("*.md"):
            if any(part in document.parts for part in ("build", ".git", ".omc", "node_modules")):
                continue
            text = document.read_text(encoding="utf-8")
            for raw_target in MARKDOWN_LINK.findall(text):
                target = raw_target.strip().split(maxsplit=1)[0].strip("<>")
                parsed = urlparse(target)
                if parsed.scheme or target.startswith("#"):
                    continue
                relative = re.sub(r":\d+$", "", unquote(parsed.path))
                destination = (document.parent / relative).resolve()
                if not destination.exists():
                    failures.append(
                        f"{document.relative_to(REPO_DIR)} -> {raw_target}"
                    )
        self.assertEqual([], failures)

    def test_language_selectors_link_the_eleven_current_readmes(self) -> None:
        expected = {REPO_DIR / "README.md"}
        expected.update(REPO_DIR / "i18n" / name for name in TRANSLATIONS)
        for document in expected:
            with self.subTest(document=document.name):
                readme = document.read_text(encoding="utf-8")
                selector_targets = {
                    (document.parent / target).resolve()
                    for target in MARKDOWN_LINK.findall(readme.split("</div>", 1)[0])
                    if Path(target).name.startswith("README")
                }
                self.assertEqual(expected, selector_targets)
        actual = {
            path.name for path in (REPO_DIR / "i18n").glob("README.*.md")
        }
        self.assertEqual(TRANSLATIONS, actual)
        languages = sorted(name.removeprefix("README.").removesuffix(".md")
                           for name in TRANSLATIONS)
        for topic in (
            "quality-guide", "source-build", "ubuntu-26.04-port", "architecture",
            "security", "adaptive-keyboard-relays", "reusable-upgrade",
            "automatic-updates", "porting", "upstream-comparison",
            "performance-evidence", "troubleshooting", "support",
        ):
            documents = {REPO_DIR / "docs" / f"{topic}.md"}
            documents.update(REPO_DIR / "docs/i18n" / lang / f"{topic}.md"
                             for lang in languages)
            for document in documents:
                with self.subTest(document=str(document.relative_to(REPO_DIR))):
                    text = document.read_text(encoding="utf-8")
                    navigation = text.split("\n# ", 1)[0]
                    targets = {
                        (document.parent / target).resolve()
                        for target in MARKDOWN_LINK.findall(navigation)
                        if Path(target).name == f"{topic}.md"
                    }
                    self.assertEqual(documents, targets)
                    lang = document.parent.name if "i18n" in document.parts else None
                    home = (REPO_DIR / "i18n" / f"README.{lang}.md"
                            if lang else REPO_DIR / "README.md")
                    self.assertIn(home, {
                        (document.parent / target).resolve()
                        for target in MARKDOWN_LINK.findall(navigation)
                    })
        for topic in ("CONTRIBUTING", "CHANGELOG"):
            documents = {REPO_DIR / f"{topic}.md"}
            documents.update(REPO_DIR / "i18n" / f"{topic}.{lang}.md"
                             for lang in languages)
            for document in documents:
                with self.subTest(document=document.name):
                    navigation = document.read_text(encoding="utf-8").split("\n# ", 1)[0]
                    targets = {
                        (document.parent / target).resolve()
                        for target in MARKDOWN_LINK.findall(navigation)
                        if Path(target).name.startswith(topic)
                    }
                    self.assertEqual(documents, targets)

    def test_current_readmes_identify_the_plus_fork_and_preserve_attribution(self) -> None:
        paths = [REPO_DIR / "README.md"]
        paths.extend(REPO_DIR / "i18n" / name for name in TRANSLATIONS)
        for path in paths:
            with self.subTest(document=path.name):
                text = path.read_text(encoding="utf-8")
                self.assertIn("UU Remote Ubuntu Plus", text)
                self.assertIn("https://github.com/llmir/uu-remote-ubuntu-plus.git", text)
                self.assertIn("https://github.com/lachlanchen/uu-remote-ubuntu-bridge", text)
                self.assertIn("Lachlan Chen", text)
                self.assertIn("MIT", text)
        self.assertIn("Copyright (c) 2026 Lachlan Chen",
                      (REPO_DIR / "LICENSE").read_text(encoding="utf-8"))

    def test_current_readmes_link_quality_and_project_support(self) -> None:
        paths = [REPO_DIR / "README.md"]
        paths.extend(REPO_DIR / "i18n" / name for name in TRANSLATIONS)
        for path in paths:
            with self.subTest(document=path.name):
                text = path.read_text(encoding="utf-8")
                lang = path.stem.removeprefix("README.") if path.parent.name == "i18n" else None
                prefix = f"../docs/i18n/{lang}" if lang else "docs"
                for topic in (
                    "quality-guide", "source-build", "ubuntu-26.04-port", "architecture",
                    "security", "adaptive-keyboard-relays", "reusable-upgrade",
                    "automatic-updates", "porting", "upstream-comparison",
                    "performance-evidence", "troubleshooting", "support",
                ):
                    self.assertIn(f"{prefix}/{topic}.md", text)
                for topic in ("CONTRIBUTING", "CHANGELOG"):
                    self.assertIn(f"{topic}.{lang}.md" if lang else f"{topic}.md", text)
                self.assertIn("uu-remote quality gui", text)
                self.assertIn("4.42.0.2770", text)
                self.assertIn("https://paypal.me/mirmirlin", text)
                self.assertIn("<details>", text)
                support = REPO_DIR / "docs" / (f"i18n/{lang}/support.md" if lang else "support.md")
                support_text = support.read_text(encoding="utf-8")
                for anchor, filename in (
                    ("alipay-cny", "alipay-cny.jpg"),
                    ("alipay-hkd", "alipay-hkd.png"),
                    ("wechat-zh", "wechat-zh.png"),
                    ("wechat-en", "wechat-en.png"),
                ):
                    self.assertIn(f'id="{anchor}"', support_text)
                    self.assertIn(f"images/support/{filename}", support_text)
                    self.assertIn(f"docs/images/support/{filename}", text)
                for previous_support_url in (
                    "https://paypal.me/RongzhouChen",
                    "https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400",
                    "https://chat.lazying.art/donate",
                    "https://github.com/sponsors/lachlanchen",
                ):
                    self.assertNotIn(previous_support_url, text)

    def test_quality_guide_distinguishes_canvas_fps_and_reconnect_limits(self) -> None:
        text = (REPO_DIR / "docs/quality-guide.md").read_text(encoding="utf-8")
        for size in ("1280 × 720", "1920 × 1080", "2560 × 1440", "3840 × 2160"):
            self.assertIn(size, text)
        self.assertIn("briefly reconnects UU", text)
        self.assertIn("rollback timer", text)
        self.assertIn("actual streaming FPS", text)
        self.assertIn("uu-remote quality bitrate 0", text)
        self.assertIn("https://uuyc.163.com/help/superscreen.html", text)

    def test_landing_images_resolve_and_have_accessible_descriptions(self) -> None:
        paths = [REPO_DIR / "README.md"]
        paths.extend(REPO_DIR / "i18n" / name for name in TRANSLATIONS)
        for landing in paths:
            text = landing.read_text(encoding="utf-8")
            for tag in re.findall(r"<img\b([^>]+)>", text):
                attributes = dict(re.findall(r'([\w-]+)="([^"]*)"', tag))
                with self.subTest(document=landing.name, image=attributes.get("src")):
                    self.assertTrue(attributes.get("alt", "").strip())
                    source = attributes["src"]
                    if not urlparse(source).scheme:
                        self.assertTrue((landing.parent / source).is_file())
            linked_images = {}
            for anchor, tag in re.findall(r"<a\b([^>]+)>\s*<img\b([^>]+)>\s*</a>", text):
                link = dict(re.findall(r'([\w-]+)="([^"]*)"', anchor))
                attributes = dict(re.findall(r'([\w-]+)="([^"]*)"', tag))
                linked_images[attributes["src"]] = (link["href"], attributes)
            lang = landing.stem.removeprefix("README.") if landing.parent.name == "i18n" else None
            prefix = "../docs/images/" if lang else "docs/images/"
            logo_href, logo = linked_images[prefix + "uu-plus-logo.png"]
            self.assertEqual("140", logo["width"])
            self.assertEqual(landing, (landing.parent / logo_href).resolve())
            artwork = "zh-Hans" if lang in ("zh-Hans", "zh-Hant") else "en"
            for method, destination in (
                ("paypal", "https://paypal.me/mirmirlin"),
                ("alipay-cny", prefix + "support/alipay-cny.jpg"),
                ("alipay-hkd", prefix + "support/alipay-hkd.png"),
                ("wechat-zh", prefix + "support/wechat-zh.png"),
                ("wechat-en", prefix + "support/wechat-en.png"),
            ):
                href, attributes = linked_images[prefix + f"support-{method}-{artwork}.png"]
                self.assertEqual(destination, href)
                self.assertEqual("160", attributes["width"])

    def test_port_notes_keep_upstream_separate_from_plus_origin(self) -> None:
        text = (REPO_DIR / "docs/ubuntu-26.04-port.md").read_text(encoding="utf-8")
        self.assertIn("git remote add upstream", text)
        self.assertIn("git fetch upstream", text)
        self.assertIn("./scripts/verify.sh --quick", text)
        self.assertIn("preset rollback covers canvas configuration", text)
        self.assertIn("approved manifest", text)
        self.assertNotIn("git merge origin/main", text)

    def test_primary_readmes_use_the_official_windows_uu_download(self) -> None:
        english = (REPO_DIR / "README.md").read_text(encoding="utf-8")
        chinese = (REPO_DIR / "i18n" / "README.zh-Hans.md").read_text(
            encoding="utf-8"
        )
        for text in (english, chinese):
            self.assertGreaterEqual(text.count("https://uuyc.163.com/"), 1)
            self.assertIn("Windows", text)
            self.assertIn("Wine", text)
        self.assertIn("UU retains its own license", english)
        self.assertIn("UU 使用其原有许可证", chinese)

    def test_compatibility_intake_is_public_bilingual_and_privacy_safe(self) -> None:
        form = (
            REPO_DIR / ".github" / "ISSUE_TEMPLATE" / "compatibility.yml"
        ).read_text(encoding="utf-8")
        english = (REPO_DIR / "README.md").read_text(encoding="utf-8")
        chinese = (REPO_DIR / "i18n" / "README.zh-Hans.md").read_text(
            encoding="utf-8"
        )

        route = "issues/new?template=compatibility.yml"
        self.assertIn(route, english)
        self.assertIn(route, chinese)
        self.assertIn("Compatibility report or request / 兼容性反馈或需求", form)
        self.assertIn("Bridge and UU versions / 桥接器与 UU 版本", form)
        self.assertIn("Expected and observed result / 预期与实际结果", form)
        software = form.split("    id: software\n", 1)[1].split("\n  - type:", 1)[0]
        confirmation = form.split("    id: confirmation\n", 1)[1].split("\n  - type:", 1)[0]
        self.assertRegex(software, r"(?m)^    validations:\n      required: true$")
        self.assertRegex(confirmation, r"I removed account/device identifiers and private data\.[^\n]*\n          required: true")
        self.assertIn("我已去掉账号、设备标识和私人数据", form)

    def test_update_guidance_preserves_required_update_controls(self) -> None:
        changelog = (REPO_DIR / "CHANGELOG.md").read_text(encoding="utf-8")
        release = (REPO_DIR / "docs/releases/v0.1.0.md").read_text(
            encoding="utf-8"
        )
        union_release = (REPO_DIR / "docs/releases/v0.2.0.md").read_text(
            encoding="utf-8"
        )
        handoff = (REPO_DIR / "docs/update-handoff.md").read_text(
            encoding="utf-8"
        )
        keyboard_handoff = (
            REPO_DIR / "docs/mobile-keyboard-parity-handoff.md"
        ).read_text(encoding="utf-8")

        self.assertIn("## Upstream 0.1.0 — 2026-07-17", changelog)
        self.assertIn("git checkout v0.1.0", release)
        self.assertIn("--skip-account-login", release)
        self.assertIn("./scripts/verify.sh --quick", release)
        self.assertIn("git checkout 8a68200", release)
        self.assertIn("## Upstream 0.2.0 — 2026-07-18", changelog)
        self.assertIn("git switch --detach v0.2.0", union_release)
        self.assertIn("git switch --detach v0.1.0", union_release)
        self.assertIn("physical-key pacing defaults to `0`", union_release)
        self.assertIn("physical-key routing defaults to `rdp`", union_release)
        self.assertIn("network-interface filtering defaults to `all`", union_release)
        self.assertIn("--keyboard-route x11", union_release)
        self.assertIn("## Source update", handoff)
        self.assertIn("./install.sh --skip-packages --skip-account-login", handoff)
        self.assertIn("./scripts/verify.sh --quick", handoff)
        self.assertIn("abcXYZ123,.!?", handoff)
        self.assertIn("Do not discard a dirty worktree", handoff)
        self.assertIn(
            "https://github.com/lachlanchen/uu-remote-ubuntu-bridge", handoff
        )
        self.assertNotIn("The private repository", handoff)
        self.assertNotIn("repository is private", release.lower())
        self.assertIn("Physical keys", keyboard_handoff)
        self.assertIn("No replay after ambiguity", keyboard_handoff)
        self.assertIn("abcXYZ123,.!?", keyboard_handoff)
        self.assertIn("UURB_TEXT_KEY_DELAY_MS", keyboard_handoff)
        self.assertIn("Do not commit a completed record", keyboard_handoff)

    def test_xrdp_keyboard_recovery_preserves_safe_ordering(self) -> None:
        recovery = (
            REPO_DIR / "docs/xrdp-and-keyboard-recovery.md"
        ).read_text(encoding="utf-8")

        self.assertIn("reset the controller application first", recovery)
        self.assertIn("--physical-key-delay-ms 8", recovery)
        self.assertIn("--physical-key-delay-ms 0", recovery)
        self.assertIn("1620x1080", recovery)
        self.assertIn("subtype:0", recovery)
        self.assertIn("does not prove", recovery)
        self.assertIn("never record a key code", recovery)

    def test_automated_maintenance_contract_preserves_action_boundaries(self) -> None:
        contract = (
            REPO_DIR / "docs/automated-repair-agent-handoff.md"
        ).read_text(encoding="utf-8")

        self.assertIn("assigned repair checkout", contract)
        self.assertIn("No replay after ambiguity", contract)
        self.assertIn("Do not edit the live Wine prefix", contract)
        self.assertIn("outside\nGit", contract)
        self.assertIn("independent review", contract)
        self.assertRegex(
            contract, r"may not approve its own binary\s+interpretation"
        )


if __name__ == "__main__":
    unittest.main()
