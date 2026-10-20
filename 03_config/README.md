# 03. Config

Что тренируем: реалистичный конфиг приложения + JSON Schema.

## Файлы

| Файл                     | Что                                              |
|--------------------------|--------------------------------------------------|
| `app_config.json`        | Конфиг: `app`, `database`, `logging`, `features` |
| `app_config.schema.json` | JSON Schema (draft 2020-12)                      |
| `test_config.py`         | Валидация + негативные кейсы                     |

## Что проверяем

1. `app_config.json` **проходит** валидацию.
2. Невалидный **порт** (`70000`) → `ValidationError` (`maximum: 65535`).
3. Невалидный **log level** (`TRACE`) → `ValidationError` (`enum`).
4. Невалидная **версия** (`v1.0`) → `ValidationError` (`pattern`).
5. Отсутствие обязательной **секции** (`database`) → `ValidationError` (`required`).

## Запуск

```bash
python -m pytest 03_config -v
```
