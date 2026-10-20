"""Тесты для 02_api_response: парсинг и валидация по схеме."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import jsonschema
import pytest

BASE = Path(__file__).parent


def _load(name: str) -> dict[str, Any]:
    data: dict[str, Any] = json.loads((BASE / name).read_text(encoding="utf-8"))
    return data


def test_response_matches_schema() -> None:
    response = _load("response.json")
    schema = _load("schema.json")
    jsonschema.validate(instance=response, schema=schema)


def test_invalid_user_raises() -> None:
    schema = _load("schema.json")
    bad = {
        "status": "ok",
        "pagination": {"page": 1, "per_page": 2, "total": 3},
        "users": [
            {
                "id": 0,  # minimum: 1
                "name": "",  # minLength: 1
                "email": "not-an-email",  # format: email
                "roles": [],  # ok (enum не нарушен)
                "active": "yes",  # ожидается type boolean (true/false)
            }
        ],
    }
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=bad, schema=schema)


def test_missing_required_field_raises() -> None:
    schema = _load("schema.json")
    bad = {
        "status": "ok",
        "pagination": {"page": 1, "per_page": 2},  # нет total
        "users": [],
    }
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=bad, schema=schema)
