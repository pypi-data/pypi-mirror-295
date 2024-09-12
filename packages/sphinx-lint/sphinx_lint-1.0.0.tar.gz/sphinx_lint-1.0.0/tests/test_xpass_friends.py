"""This test needs `download-more-tests.sh`.

This is useful to avoid a sphinx-lint release to break many CIs.
"""

import shlex
from pathlib import Path

import pytest

from sphinxlint.cli import main

FIXTURE_DIR = Path(__file__).resolve().parent / "fixtures"


@pytest.mark.parametrize(
    "file",
    [str(f) for f in (FIXTURE_DIR / "friends").iterdir() if f.name != ".DS_Store"]
    if (FIXTURE_DIR / "friends").is_dir()
    else [],
)
def test_sphinxlint_friend_projects_shall_pass(file, capsys):
    flags = (Path(file) / "flags").read_text(encoding="UTF-8")
    has_errors = main(["sphinxlint.py", file] + shlex.split(flags))
    out, err = capsys.readouterr()
    assert err == ""
    assert out == "No problems found.\n"
    assert not has_errors
