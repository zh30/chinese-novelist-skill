import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
MARKDOWN_FILES = [ROOT / "SKILL.md", ROOT / "README.md"]


class SkillDocsTests(unittest.TestCase):
    def test_skill_and_readme_reference_opening_and_ending_guides(self):
        required = {"references/opening-design.md", "references/ending-design.md"}

        combined = "\n".join(path.read_text(encoding="utf-8") for path in MARKDOWN_FILES)

        for rel_path in required:
            self.assertIn(rel_path, combined)

    def test_local_markdown_links_resolve(self):
        pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")

        for path in ROOT.rglob("*.md"):
            content = path.read_text(encoding="utf-8")
            for target in pattern.findall(content):
                if target.startswith("http://") or target.startswith("https://") or target.startswith("#"):
                    continue
                resolved = (path.parent / target).resolve()
                self.assertTrue(
                    resolved.exists(),
                    msg=f"{path.relative_to(ROOT)} has broken link: {target}",
                )


if __name__ == "__main__":
    unittest.main()
