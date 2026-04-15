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

        # Template files contain placeholder links that only resolve at runtime
        # (e.g. progress-dashboard-template.md links to 00-大纲.md which
        # only exists inside novels/ directories)
        TEMPLATE_LINKS = {
            '00-大纲.md', '01-人物档案.md', '02-世界观与伏笔.md',
            '03-悬念追踪表.md',
        }

        for path in ROOT.rglob("*.md"):
            # Skip historical design docs (their links don't resolve from docs/plans/)
            if 'docs/plans' in str(path):
                continue
            content = path.read_text(encoding="utf-8")
            for target in pattern.findall(content):
                if target.startswith("http://") or target.startswith("https://") or target.startswith("#"):
                    continue
                # Template placeholder links only resolve at runtime in novels/ directories
                if target in TEMPLATE_LINKS:
                    continue
                if '___' in target or target.startswith('第'):
                    continue
                resolved = (path.parent / target).resolve()
                self.assertTrue(
                    resolved.exists(),
                    msg=f"{path.relative_to(ROOT)} has broken link: {target}",
                )


if __name__ == "__main__":
    unittest.main()
