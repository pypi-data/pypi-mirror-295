# llm-parse-json

A simple JSON parsing tool that preprocesses and parses JSON strings.

## Installation

You can install the package via pip:

```bash
pip install llm-parse-json
````

```python
from llm_parse_json import parse_json

json_str = '{"name": "John", "age": 30}'
result = parse_json(json_str)
print(result)
```