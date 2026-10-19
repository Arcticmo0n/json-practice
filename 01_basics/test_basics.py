"""Тесты для 01_basics: валидный и невалидные JSON."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

BASE = Path(__file__).parent


def test_valid_json_parses() -> None:
    data = json.loads((BASE / "valid.json").read_text(encoding="utf-8"))
    assert data["name"] == "Arcticmo0n"
    assert data["age"] == 30
    assert data["tags"] == ["dev", "python"]
    assert data["address"]["zip"] is None


def _reject_constant(value: str) -> None:
    raise ValueError(f"Non-standard JSON constant: {value}")


@pytest.mark.parametrize(
    "filename",
    [
        "invalid_trailing_comma.json",
        "invalid_single_quotes.json",
        "invalid_nan.json"
    ],
)
def test_invalid_json_raises(filename: str) -> None:
    with pytest.raises((json.JSONDecodeError, ValueError)):
        json.loads(
            (BASE / filename).read_text(encoding="utf-8"),
            parse_constant=_reject_constant
        )
