# Copyright (C) 2024 Bellande Algorithm Model Research Innovation Center, Ronaldson Bellande

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

#!/usr/bin/env python3

import re
from typing import Dict, List, Union, Any

class Bellande_Format:
    def parse_bellande(self, file_path: str) -> str:
        with open(file_path, 'r') as file:
            lines = file.readlines()
        parsed_data = self.parse_lines(lines)
        return self.to_string_representation(parsed_data)

    def parse_lines(self, lines: List[str]) -> Union[Dict, List]:
        result = {}
        current_key = None
        current_list = None
        indent_stack = [(-1, result)]

        for line in lines:
            stripped = line.strip()
            if not stripped or stripped.startswith('#'):
                continue

            indent = len(line) - len(line.lstrip())

            while indent_stack and indent <= indent_stack[-1][0]:
                popped = indent_stack.pop()
                if isinstance(popped[1], list):
                    current_list = None

            if ':' in stripped:
                key, value = map(str.strip, stripped.split(':', 1))
                current_key = key
                if value:
                    result[key] = self.parse_value(value)
                else:
                    result[key] = []
                    current_list = result[key]
                    indent_stack.append((indent, current_list))
            elif stripped.startswith('-'):
                value = stripped[1:].strip()
                parsed_value = self.parse_value(value)
                if current_list is not None:
                    current_list.append(parsed_value)
                else:
                    if not result:  # If result is empty, start a root-level list
                        result = [parsed_value]
                        current_list = result
                        indent_stack = [(-1, result)]
                    else:
                        result[current_key] = [parsed_value]
                        current_list = result[current_key]
                        indent_stack.append((indent, current_list))

        return result

    def parse_value(self, value: str) -> Union[str, int, float, bool, None]:
        if value.lower() == 'true':
            return True
        elif value.lower() == 'false':
            return False
        elif value.lower() == 'null':
            return None
        elif value.startswith('"') and value.endswith('"'):
            return value[1:-1]
        elif re.match(r'^-?\d+$', value):
            return int(value)
        elif re.match(r'^-?\d*\.\d+$', value):
            return float(value)
        else:
            return value

    def to_string_representation(self, data: Any) -> str:
        if isinstance(data, dict):
            items = [f'"{k}": {self.to_string_representation(v)}' for k, v in data.items()]
            return '{' + ', '.join(items) + '}'
        elif isinstance(data, list):
            items = [self.to_string_representation(item) for item in data]
            return '[' + ', '.join(items) + ']'
        elif isinstance(data, str):
            return f'"{data}"'
        elif isinstance(data, (int, float)):
            return str(data)
        elif data is None:
            return 'null'
        elif isinstance(data, bool):
            return str(data).lower()
        else:
            return str(data)

    def write_bellande(self, data: Any, file_path: str):
        with open(file_path, 'w') as file:
            file.write(self.to_bellande_string(data))
    
    def to_bellande_string(self, data: Any, indent: int = 0) -> str:
        if isinstance(data, dict):
            lines = []
            for key, value in data.items():
                if isinstance(value, (dict, list)):
                    lines.append(f"{' ' * indent}{key}:")
                    lines.append(self.to_bellande_string(value, indent + 2))
                else:
                    lines.append(f"{' ' * indent}{key}: {self.format_value(value)}")
            return '\n'.join(lines)
        elif isinstance(data, list):
            lines = []
            for item in data:
                if isinstance(item, dict):
                    dict_lines = self.to_bellande_string(item, indent + 2).split('\n')
                    lines.append(f"{' ' * indent}- {dict_lines[0]}")
                    lines.extend(dict_lines[1:])
                else:
                    lines.append(f"{' ' * indent}- {self.format_value(item)}")
            return '\n'.join(lines)
        else:
            return f"{' ' * indent}{self.format_value(data)}"

    def format_value(self, value: Any) -> str:
        if isinstance(value, str):
            if ' ' in value or ':' in value or value.lower() in ['true', 'false', 'null']:
                return f'"{value}"'
            return value
        elif isinstance(value, bool):
            return str(value).lower()
        elif value is None:
            return 'null'
        else:
            return str(value)
