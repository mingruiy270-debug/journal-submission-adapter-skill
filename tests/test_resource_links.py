import re
import unittest
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]


class ResourceLinkTests(unittest.TestCase):
    def test_bundled_markdown_resource_links_resolve(self):
        documents = [ROOT / "README.md", *ROOT.glob("docs/*.md"), *ROOT.glob("tests/*.md"),
                     *ROOT.glob("skills/journal-submission-adapter/**/*.md")]
        checked = 0
        for document in documents:
            for target in re.findall(r"\]\(([^)]+)\)", document.read_text(encoding="utf-8")):
                if urlsplit(target).scheme or target.startswith("#"):
                    continue
                path = (document.parent / unquote(target.split("#", 1)[0])).resolve()
                with self.subTest(document=document.name, target=target):
                    self.assertTrue(path.is_relative_to(ROOT))
                    self.assertTrue(path.is_file(), f"Missing bundled resource: {target}")
                checked += 1
        self.assertGreater(checked, 0)


if __name__ == "__main__":
    unittest.main()
