#### 1. Что такое JSON
JSON (JavaScript Object Notation) - текстовый формат обмена данными. Легкий, читаемый, независимый от языка. Стандарты: RFC 8259, ECMA-404. Родился из синтаксиса языка JS, использование: АПИ, конфиги, логи, БД (MongoDB, PostgreSQL jsonb), ML-датасеты.

__Ключевая идея__ - JSON описывает значения шести типов, вложенные друг в друга. Все остальное - комбинации.

#### 2. Шесть типов значений
| Тип     | Пример                 | Замечания                                                                                |
|---------|------------------------|------------------------------------------------------------------------------------------|
| object  | {"a": 2, "b": 3}       | Неупорядоченный набор пар ключ -> значение.<br/>Ключ - всегда строка в двойных кавычках. |
| array   | [1, null, "two", true] | Упорядоченный список. Элементы любых типов,<br/>в т.ч. разнородные.                      |
| string  | "hello\nworld"         | Всегда в двойных кавычках. Экранирование:<br/>\" \\ \/ \b \n \f \r \t \uXXXX.            |
| number  | 42, -3.14, 1e10        | Без кавычек. Нет NaN, Infinity, нет<br/>восьмеричных/шестнадцатеричных литералов.        |
| boolean | true, false            | Строго строчные.                                                                         |
| null    | null                   | Единственное пустое значение.                                                            |

Чего нет в JSON: функций, undefined, комментариев, дат (дата-строка), NaN/Infinity, trailing comma, одинарных кавычек, ключей не-строк.

#### 3. Синтаксис: правила
```json
{
  "name": "Arcticmo0n",
  "age": 30,
  "is_active": true,
  "score": 99.5,
  "tags": ["dev", "python"],
  "address": {
    "city": "Moscow",
    "zip": null
  }
}
```
Правила:
- Корень - любое значение (обычно object или array). Строка "hello" - валидный JSON.
- Ключи - только строки в двойных кавычках.
- Пары разделяются запятой, без запятой после последней (trailing comma запрещена).
- Пробелы/переводы строк между токенами игнорируются (кроме внутри строк).
- Кодировка - UTF-8 (по умолчанию; ВОМ не рекомендуется).

#### 4. Валидный vs Невалидный

```json
// невалидно
[
  {
    name:"x", // ключ без кавычек
    'age': 1, // одинарные кавычки
    "n": NaN, // нет NaN
    "list": [1, 2,], // trailing comma
    // комментарий // нет комментариев
  },
  {
    "name": "x",
    "age": 10,
    "list": [1, 2],
    "nothing": null
  }
]
```

#### 5. JSON в Python
Стандартный модуль json
```python
import json

data = {"name": "Arcticmo0n", "tags": ["dev", "python"], "active": True}

# Python -> строка JSON (сериализация)
s = json.dumps(data, ensure_ascii=False, indent=2)

# JSON -> Python (десериализация)
obj = json.loads(s)

# Файлы
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

with open("data.json", encoding="utf-8") as f:
    loaded = json.load(f)
```
Полезные параметры dumps/dump:
- ensure_ascii=False - не экранировать кириллицу.
- indent=2 - pretty-print.
- sort_keys=True - сортировать ключи.
- separators=(",", ":") - компактный вывод
- defauls=str - как сериализовать нестандартные объекты (иначе TypeError)

Маппинг типов Python <-> JSON:

| Python      | JSON       |
|-------------|------------|
| dict        | object     |
| list, tuple | array      |
| int, float  | number     |
| str         | string     |
| True/False  | true/false |
| None        | null       |

Обработка ошибок

```python
import json

try:
    json.loads("{bad.json}")
except json.JSONDecodeError as e:
    print(e.msg, e.pos, e.lineno, e.colno)
```
`json.dumps(float('nan'))` по умолчанию выдаст `NaN` - невалидный json. Отключается `allow_nan=False` (тогда ValueError).
`json.loads` по умолчанию принимает `NaN/Infinity` (расширение Python). Для строгости `parse_constant`.

#### 6. JSON vs Python dict

|                 | JSON                       | dict                |
|-----------------|----------------------------|---------------------|
| Ключи           | только строки              | любой hashable      |
| Кавычки         | только "                   | ' или "             |
| true/false/null | да                         | True/False/None     |
| Комментарии     | нет                        | есть #              |
| trailing comma  | нет                        | да                  |
| NaN/Infinity    | нет                        | да                  |
| Порядок ключей  | не гарантирован стандартом | гарантирован (3.7+) |

#### 7. JSON Lines (JSONL/NDJSON)

"Одна JSON-запись на строку" - для потоков, логов, больших файлов:
```text
{"id": 1, "event": "login"}
{"id": 2, "event": "click"}
{"id": 3, "event": "logout"}
```
- Каждая строка - самостоятельный валидный JSON.
- Можно читать построчно, не загружая весь файл.
- Используется в ML-датасетах, логах, streaming API.

```python
import json

with open("events.jsonl", encoding="utf-8") as f:
    for line in f:
        event = json.loads(line)
```
`JSONL != JSON-массив. [{"a": 1}, {"a": 2}] - это один JSON-массив. {"a": 1}\n{"a": 2} - JSONL`

#### 8. JSON Schema (кратко)
Способ описать и валидировать структуру JSON. Сама схема - тоже JSON.
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "properties": {
    "name": {"type": "string", "minLength": 1},
    "age": {"type":  "integer", "minimum": 0}
  },
  "required": ["name"],
  "additionalProperties": false
}
```
в Python библиотек - jsonschema:
```python
import jsonschema
jsonschema.validate(instance=data, schema=schema)
```
Применение: валидация API-запросов, конфигов, OpenAPI, CI.

##### 9. JSON5, JSONC, YAML - расширения
- JSON5 - комментарии, одинарные кавычки, trailing comma, hex, Infinity/NaN. Конфиги (Babel, VS Code).
- JSONC (JSON with comments) - JSON + комментарии. tsconfig.json, .vscode/settings.json.
- YAML - надмножество JSON (валидный JSON = валидный YAML), но с отступами, якорями, комментариями. Конфиги (Docker Compose, GitHub Actions, Kubernetes). Сложнее парсить, нюансы с типами (yes -> bool).

#### 10. Безопансость и производительность
- eval - никогда. json.loads безопасен; eval/ast.literal_eval для JSON не нужны и опасны.
- Глубина вложенности. Очень глубокий JSON может вызвать RecursionError. Необходимо валидировать вход.
- Огромные файлы. json.load читает все в память. Для больших - ijson(streaming) или JSONL.
- Дубли ключей. Стандарт не запрещает; Python берет последнее значение. Не полагаться на дубли.
- Порядок ключей. Стандартом не гарантирован; не строить логику на порядке.
- Числа 1е400 -> inf в Python; большие int - ok в Python. Для денег/ID - строки или decimal

#### 11. Чек-лист на валидность
- Все ключи и строки - в двойных кавычках.
- Нет trailing comma.
- Нет комментариев.
- true/false/null - строчные, без кавычек.
- Нет NaN, Infinity, undefined.
- Нет одинарных кавычек, нет неэкранированных " внутри строк.
- Корень - одно значение (object/array/строка/число/bool/null).
- Кодировка - UTF-8, без ВОМ.



