"""
Tests for reflect.py. Run with:

    python3 -m pytest tests/ -v
"""

import datetime
import importlib
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))


def test_refuses_to_overwrite_existing_entry(tmp_path, monkeypatch):
    import reflect

    importlib.reload(reflect)
    monkeypatch.setattr(reflect, "ENTRIES_DIR", tmp_path)

    today = datetime.date.today().isoformat()
    existing = tmp_path / f"{today}.md"
    existing.write_text("already here")

    result = reflect.main()

    assert result == 1
    assert existing.read_text() == "already here"  # untouched


def test_creates_entry_with_todays_date(tmp_path, monkeypatch):
    import reflect

    importlib.reload(reflect)
    monkeypatch.setattr(reflect, "ENTRIES_DIR", tmp_path)

    result = reflect.main()
    today = datetime.date.today().isoformat()
    expected = tmp_path / f"{today}.md"

    assert result == 0
    assert expected.exists()
    assert today in expected.read_text()


def test_template_has_expected_sections(tmp_path, monkeypatch):
    import reflect

    importlib.reload(reflect)
    monkeypatch.setattr(reflect, "ENTRIES_DIR", tmp_path)

    reflect.main()
    today = datetime.date.today().isoformat()
    content = (tmp_path / f"{today}.md").read_text()

    assert "## What prompted this entry" in content
    assert "## What I actually think" in content
    assert "## What's still unresolved" in content
