import os
import ast

def extract_request_args_get_params(filepath):
    with open(filepath, "r") as file:
        tree = ast.parse(file.read(), filename=filepath)

    params = []

    class RequestArgsGetVisitor(ast.NodeVisitor):
        def visit_Call(self, node):
            if isinstance(node.func, ast.Attribute):
                if (isinstance(node.func.value, ast.Attribute) and 
                    node.func.value.attr == 'args' and 
                    node.func.attr == 'get' and 
                    len(node.args) > 0 and 
                    isinstance(node.args[0], ast.Str)):
                    params.append(node.args[0].s)
            self.generic_visit(node)

    RequestArgsGetVisitor().visit(tree)
    return params

def search_directory_for_params(directory):
    all_params = set()
    for root, dirs, files in os.walk(directory):
        # Exclude .git directory
        if '.git' in dirs:
            dirs.remove('.git')
        for file in files:
            if file.endswith(".py") and file != "extract_params.py":
                filepath = os.path.join(root, file)
                params = extract_request_args_get_params(filepath)
                all_params.update(params)
    return all_params

def main():
    codebase_directory = "."  # Current directory
    params = search_directory_for_params(codebase_directory)
    
    with open("extracted_keywords.txt", "w") as output_file:
        for param in sorted(params):
            output_file.write(f"{param}\n")
    
    print("Extraction complete. Keywords have been written to extracted_keywords.txt.")

if __name__ == "__main__":
    main()

#Usage:
# python3 extract_params.py
