import ast

class DataExtractor:
    def __init__(self, script_path):
        self.script_path = script_path

    def extract_data(self):
        data = {}
        with open(self.script_path, "r") as file:
            tree = ast.parse(file.read(), filename=self.script_path)
            for node in ast.walk(tree):
                if isinstance(node, ast.Assign):
                    if isinstance(node.targets[0], ast.Name):
                        key = node.targets[0].id
                        value = ast.literal_eval(node.value)
                        data[key] = value
        return data
