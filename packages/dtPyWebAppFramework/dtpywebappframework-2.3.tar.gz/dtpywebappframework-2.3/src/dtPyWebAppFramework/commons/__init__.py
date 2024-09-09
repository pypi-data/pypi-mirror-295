import os
import importlib
import inspect
import re


def find_base_app_class(root_path):
    # regular expression to find class definitions
    class_regex = re.compile(r'^class\s+(\w+)\(BaseApp\):')

    results = []

    # starting at the current directory
    for root, dirs, files in os.walk(root_path):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    for line_no, line in enumerate(f, start=1):
                        match = class_regex.match(line)
                        if match:
                            return file_path, match.group(1)

    return None
