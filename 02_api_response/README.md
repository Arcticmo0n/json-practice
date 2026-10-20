# 02. API Response
О чем речь: реалистичный ответ API + валидация через JSON Schema.

## Файлы

| Файл            | Что                                             |
|-----------------|-------------------------------------------------|
| `response.json` | Ответ API: `status`, `pagination`, `users[]`    |
| `schema.json`   | JSON Schema (draft 2020-12) для `response.json` |
| `test_api.py`   | Парсинг + `jsonschema.validate`                 |
## Что проверяем
1. `response.json` **проходит** валидацию по `schema.json`.
2. Невалидный пользователь (`id: 0`, пустое имя, плохой email, `active: "yes"`) -> `ValidationError`.
3. Отсутствие обязательного поля (`pagination.total`) -> `ValidationError`.

## Нюанс: `format: email`
`json.schema` **не проверяет** `format: email` по умолчанию (это "annotation", не "assertion").
Чтобы проверять - нужен `FormatChecker`:

```python
from jsonschema import FormatChecker

jsonschema.validate(instance=response, schema=schema, format_checker=FormatChecker())
```
