# JSON Practice
![CI](https://github.com/Arcticmo0n/json-practice/actions/workflows/ci.yml/badge.svg)

Тренировка JSON: синтаксис, схемы, JSONL, трансформации.

## Структура
- [`01_basics/`](01_basics) - валидный и невалидные JSON, правила синтаксиса
- [`02_api_response/`](02_api_response) - ответ API + JSON Schema
- [`03_config/`](03_config) - конфиг приложения + схема
- [`04_jsonl/`](04_jsonl) - JSONL: одна запись на строку
- [`05_transform/`](05_transform) - вход -> выход: преобразование JSON

## Справочник
- [JSON Cheatsheet](JSON_CHEATSHEET.md) - все о JSON: типы, правила, Python, JSONL, Schema

## Запуск
```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
python -m pytest
```

## Инструменты
- `pytest` - тесты
- `ruff` - линтер
- `mypy` - проверка типов
- `jsonschema` - валидация по схеме
- `pre-commit` - хуки перед коммитом (ruff, mypy)

Конфиг - в [`pyproject.toml`](pyproject.toml).

## Прогресс
| #  | Тема         | Статус |
|----|--------------|--------|
| 01 | Basics       | ✅     |
| 02 | API Response | ✅     |
| 03 | Config       | 🚧     |
| 04 | JSONL        | ⬜     |
| 05 | Transform    | ⬜     |

