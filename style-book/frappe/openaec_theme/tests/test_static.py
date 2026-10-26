import ast
import pathlib
import unittest

APP = pathlib.Path(__file__).resolve().parents[1] / "openaec_theme"


class StaticChecks(unittest.TestCase):
    def test_hooks_verwijzen_naar_bestaande_assets(self):
        tree = ast.parse((APP / "hooks.py").read_text(encoding="utf-8"))
        values = {
            t.id: ast.literal_eval(node.value)
            for node in tree.body if isinstance(node, ast.Assign)
            for t in node.targets if isinstance(t, ast.Name)
        }
        self.assertEqual(values["app_name"], "openaec_theme")
        for url in values["app_include_css"] + [values["app_logo_url"]]:
            rel = url.removeprefix("/assets/openaec_theme/")
            self.assertTrue((APP / "public" / rel).is_file(), url)

    def test_versie_en_fonts(self):
        self.assertIn('__version__ = "', (APP / "__init__.py").read_text(encoding="utf-8"))
        fonts = APP / "public" / "fonts"
        self.assertTrue(any(fonts.glob("*.ttf")))
        self.assertTrue(any(fonts.glob("OFL-*.txt")))


if __name__ == "__main__":
    unittest.main()
