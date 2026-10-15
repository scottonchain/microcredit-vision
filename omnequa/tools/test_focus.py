"""Synthetic source-contract controls, not rendered keyboard/browser tests."""
import importlib.util
from pathlib import Path
import unittest

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('omnequa_check',HERE/'check.py')
check=importlib.util.module_from_spec(spec)
spec.loader.exec_module(check)
CSS=(HERE.parent/'assets/style.css').read_text()


class FocusSourceTests(unittest.TestCase):
    def rejected(self,css):
        self.assertTrue(check.focus_contrast_errors(css))

    def test_current_light_and_dark_surfaces(self):
        self.assertEqual(check.focus_contrast_errors(CSS),[])

    def test_historical_amber_focus(self):
        historical=CSS.replace('--focus:var(--ink);','').replace(
            'solid var(--focus)','solid var(--amber)').replace(
            '.cta,.intro-strip{--focus:var(--white)}','')
        self.rejected(historical)

    def test_amber_focus_token_regression(self):
        self.rejected(CSS.replace('--focus:var(--ink);','--focus:var(--amber);'))

    def test_dark_override_removed(self):
        self.rejected(CSS.replace('.cta,.intro-strip{--focus:var(--white)}',''))

    def test_ink_on_dark_surface(self):
        self.rejected(CSS.replace('.cta,.intro-strip{--focus:var(--white)}',
                                  '.cta,.intro-strip{--focus:var(--ink)}'))

    def test_teal_on_dark_surface(self):
        self.rejected(CSS.replace('.cta,.intro-strip{--focus:var(--white)}',
                                  '.cta,.intro-strip{--focus:var(--teal)}'))

    def test_transparent_outline(self):
        self.rejected(CSS.replace('3px solid var(--focus)','3px solid transparent'))

    def test_zero_width_outline(self):
        self.rejected(CSS.replace('3px solid var(--focus)','0 solid var(--focus)'))

    def test_input_outline_not_covered_by_link_rule(self):
        self.rejected(CSS.replace('input:focus,textarea:focus{outline:3px solid var(--focus)',
                                  'input:focus,textarea:focus{outline:none'))

    def test_changed_light_surface_is_measured(self):
        self.rejected(CSS.replace('.hero-note{background:#e6eadf',
                                  '.hero-note{background:#213c34'))

    def test_changed_dark_surface_is_measured(self):
        self.rejected(CSS.replace('.cta{padding:60px 10%;background:var(--teal)',
                                  '.cta{padding:60px 10%;background:var(--white)'))

    def test_unsupported_color_requires_review(self):
        self.rejected(CSS.replace('--ink:#213c34;','--ink:rgba(33,60,52,1);'))

    def test_later_outline_override(self):
        self.rejected(CSS+'a:focus-visible{outline:none}')

    def test_later_dark_token_override(self):
        self.rejected(CSS+'.cta{--focus:var(--ink)}')

    def test_forced_color_override_requires_review(self):
        self.rejected(CSS+'a:focus-visible{forced-color-adjust:none}')

    def test_outline_color_override_requires_review(self):
        self.rejected(CSS+'a:focus-visible{outline-color:transparent}')


if __name__=='__main__':unittest.main()
