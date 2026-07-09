"""Tests for index_entries.py."""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

import index_entries  # noqa: E402


def test_summarize_extracts_heading_and_first_paragraph(tmp_path):
    entry = tmp_path / "2026-01-01.md"
    entry.write_text("# 2026-01-01\n\nThis is the first paragraph.\n\nSecond paragraph.\n")

    heading, summary = index_entries.summarize(entry)

    assert heading == "2026-01-01"
    assert summary == "This is the first paragraph."


def test_summarize_truncates_long_paragraphs(tmp_path):
    entry = tmp_path / "long.md"
    long_para = "word " * 100
    entry.write_text(f"# long\n\n{long_para}\n")

    _, summary = index_entries.summarize(entry)

    assert len(summary) <= 160
    assert summary.endswith("...")


def test_summarize_falls_back_to_filename_without_heading(tmp_path):
    entry = tmp_path / "no-heading.md"
    entry.write_text("Just some text, no markdown heading.\n")

    heading, _ = index_entries.summarize(entry)

    assert heading == "no-heading"
