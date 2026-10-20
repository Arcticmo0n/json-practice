"""Тесты для 03_config: валидация конфига приложения."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import jsonschema
import pytest

BASE = Path(__file__).parent


def _load(name: str) -> dict[str, Any]:
    text = (BASE / name).read_text(encoding="utf-8")
    data: dict[str, Any] = json.loads(text)
    return data


def test_config_matches_schema() -> None:
    config = _load("app_config.json")
    schema = _load("app_config.schema.json")
    jsonschema.validate(instance=config, schema=schema)


def test_invalid_port_raises() -> None:
    config = _load("app_config.json")
    schema = _load("app_config.schema.json")
    config["database"]["port"] = 70000  # > 65535
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=config, schema=schema)


def test_invalid_log_level_raises() -> None:
    config = _load("app_config.json")
    schema = _load("app_config.schema.json")
    config["logging"]["level"] = "TRACE"  # не в enum
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=config, schema=schema)


def test_invalid_version_pattern_raises() -> None:
    config = _load("app_config.json")
    schema = _load("app_config.schema.json")
    config["app"]["version"] = "v1.0"  # не semver
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=config, schema=schema)


def test_missing_required_section_raises() -> None:
    config = _load("app_config.json")
    schema = _load("app_config.schema.json")
    del config["database"]  # обязательный блок
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=config, schema=schema)
