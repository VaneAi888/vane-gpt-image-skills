import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INSTALLER = ROOT / "scripts" / "install_skills.py"


class InstallationTests(unittest.TestCase):
    def run_installer(self, destination, *args):
        return subprocess.run(
            [sys.executable, str(INSTALLER), *args, "--destination", str(destination)],
            capture_output=True,
            text=True,
        )

    def test_install_both_and_required_assets(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "skills"
            result = self.run_installer(target, "--all")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((target / "vane-portrait-gif-stickers/SKILL.md").is_file())
            self.assertTrue((target / "vane-portrait-gif-stickers/scripts/export_frames.py").is_file())
            self.assertTrue((target / "vane-portrait-gif-stickers/references/frame-manifest.md").is_file())
            self.assertTrue((target / "vane-pixel-visuals/SKILL.md").is_file())
            self.assertTrue((target / "vane-pixel-visuals/assets/article-scenes.png").is_file())
            self.assertTrue((target / "vane-pixel-visuals/assets/pixel-avatar.png").is_file())
            self.assertFalse((target / "vane-portrait-gif-stickers/.git").exists())
            self.assertFalse((target / "vane-portrait-gif-stickers/skills").exists())

    def test_existing_skill_is_preserved_and_all_does_not_partially_install(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "skills"
            existing = target / "vane-pixel-visuals"
            existing.mkdir(parents=True)
            (existing / "SKILL.md").write_text("保留原内容", encoding="utf-8")
            result = self.run_installer(target, "--all")
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual((existing / "SKILL.md").read_text(encoding="utf-8"), "保留原内容")
            self.assertFalse((target / "vane-portrait-gif-stickers").exists())

    def test_install_one_and_leave_other_alone(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "skills"
            result = self.run_installer(target, "--skill", "vane-pixel-visuals")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((target / "vane-pixel-visuals/agents/openai.yaml").is_file())
            self.assertFalse((target / "vane-portrait-gif-stickers").exists())

    def test_install_stickers_alone(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "skills"
            result = self.run_installer(target, "--skill", "vane-portrait-gif-stickers")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((target / "vane-portrait-gif-stickers/scripts/export_frames.py").is_file())
            self.assertFalse((target / "vane-pixel-visuals").exists())


if __name__ == "__main__":
    unittest.main()
