from __future__ import annotations

import pytest

from src.rag.chunking import chunk_text


def test_explicit_zero_overlap_is_honored():
    chunks = chunk_text("abcdef", chunk_size=2, overlap=0)
    assert [c.text for c in chunks] == ["ab", "cd", "ef"]


def test_overlap_produces_sliding_window():
    chunks = chunk_text("abcdef", chunk_size=3, overlap=1)
    assert [c.text for c in chunks] == ["abc", "cde", "ef"]


def test_overlap_equal_to_size_raises():
    with pytest.raises(ValueError):
        chunk_text("abcdef", chunk_size=2, overlap=2)


def test_overlap_greater_than_size_raises():
    with pytest.raises(ValueError):
        chunk_text("abcdef", chunk_size=2, overlap=5)
