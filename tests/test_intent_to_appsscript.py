import io
import unittest
from pathlib import Path

SKILL_TESTS = Path(__file__).resolve().parent.parent / "skills" / "intent-to-appsscript" / "tests"


def test_skill_unit_tests_pass():
    """The skill carries its own unittest suite; run it as part of the repository's tests."""
    suite = unittest.defaultTestLoader.discover(str(SKILL_TESTS), top_level_dir=str(SKILL_TESTS))
    result = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0).run(suite)
    assert result.testsRun >= 70 and result.wasSuccessful(), result.failures + result.errors
