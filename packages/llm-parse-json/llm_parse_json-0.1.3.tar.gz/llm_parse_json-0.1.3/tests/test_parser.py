from llm_parse_json import parse_json

json_str = '{"name": "John",\n "age": 30, "city": "\\nNew \nYork", "address": {"street": "123 Main St", "zip": "10001"}}'
print(parse_json(json_str))

json_array_str = '[{"\\nname": "\nJohn"}, {"name": "Jane"}]'
print(parse_json(json_array_str))