import json
import re

def _escape_special_chars_in_json_value(json_str):
    """
    将 JSON 字符串中的值中的特殊字符转义。
    """
    in_string = False
    escaped_str = []
    for char in json_str:
        if char == '"':
            in_string = not in_string
        if in_string:
            if char == '\n':
                escaped_str.append('\\n')
            elif char == '\t':
                escaped_str.append('\\t')
            elif char == '\r':
                escaped_str.append('\\r')
            elif char == '\\':
                escaped_str.append('\\\\')
            else:
                escaped_str.append(char)
        else:
            escaped_str.append(char)
    return ''.join(escaped_str)

def _preprocess_json_string(json_str):
    """
    预处理 JSON 字符串，首先转义值中的特殊字符，然后移除键值对间多余的空白字符。
    """
    # 首先转义 JSON 值中的特殊��符
    json_str = _escape_special_chars_in_json_value(json_str)

    # 移除键值对之间的多余空白字符（例如换行符、制表符等）
    json_str = re.sub(r'(?<=:|,)\s+', '', json_str)

    return json_str


def parse_json(json_str):
    """
    解析 JSON 字符串，根据其格式选择使用解析对象或数组的方法。
    """
    # 预处理 JSON 字符串
    json_str = _preprocess_json_string(json_str)

    json_str = json_str.strip()

    if not json_str:
        raise ValueError("EMPTY JSON")

    # 查找第一个对象或数组的起始位置
    first_brace_index = json_str.find('{')
    first_bracket_index = json_str.find('[')

    if first_brace_index == -1 and first_bracket_index == -1:
        raise ValueError("Invalid JSON input")

    # 根据起始符号决定是对象还是数组
    if first_brace_index != -1 and (first_bracket_index == -1 or first_brace_index < first_bracket_index):
        return _parse_object(json_str)
    else:
        return _parse_array(json_str)


def _parse_object(json_str):
    """
    使用栈解析 JSON 对象字符串。
    """
    stack = []
    for i, char in enumerate(json_str):
        if char == '{':
            stack.append(i)
        elif char == '}':
            start_index = stack.pop()
            if not stack:
                data = json_str[start_index:i + 1].strip()
                if not data:
                    raise ValueError("EMPTY JSON")
                return json.loads(data)
    raise ValueError("Invalid JSON input")


def _parse_array(json_str):
    """
    使用栈解析 JSON 数组字符串。
    """
    stack = []
    for i, char in enumerate(json_str):
        if char == '[':
            stack.append(i)
        elif char == ']':
            start_index = stack.pop()
            if not stack:
                data = json_str[start_index:i + 1].strip()
                if not data:
                    raise ValueError("EMPTY JSON")
                return json.loads(data)
    raise ValueError("Invalid JSON input")