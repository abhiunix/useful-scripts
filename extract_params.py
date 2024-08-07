import os
import ast
import re

def extract_keywords(filepath):
    with open(filepath, "r") as file:
        tree = ast.parse(file.read(), filename=filepath)

    params = []

    class KeywordVisitor(ast.NodeVisitor):
        def visit_Call(self, node):
            if isinstance(node.func, ast.Attribute):
                if (isinstance(node.func.value, ast.Attribute) and 
                    node.func.value.attr == 'args' and 
                    node.func.attr == 'get' and 
                    len(node.args) > 0 and 
                    isinstance(node.args[0], ast.Str)):
                    params.append(node.args[0].s)
            self.generic_visit(node)
        
        def visit_Assign(self, node):
            if isinstance(node.targets[0], ast.Name):
                if isinstance(node.value, ast.Str):
                    params.append(node.targets[0].id)
                elif isinstance(node.value, ast.List):
                    for element in node.value.elts:
                        if isinstance(element, ast.Str):
                            params.append(element.s)
                elif isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                    params.extend(extract_sql_keywords(node.value.value))
            self.generic_visit(node)

        def visit_Constant(self, node):
            if isinstance(node.value, str):
                params.extend(extract_sql_keywords(node.value))
            self.generic_visit(node)

    KeywordVisitor().visit(tree)
    return params

def extract_sql_keywords(sql_query):
    # Regular expression to find column names
    column_regex = re.compile(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b')
    keywords = column_regex.findall(sql_query)
    
    # Removing SQL keywords and duplicates
    sql_keywords = set([
        "select", "from", "where", "join", "on", "and", "or", "group", "by", "order", "having",
        "union", "all", "as", "case", "when", "then", "else", "end", "left", "right", "inner",
        "outer", "cross", "full", "natural", "distinct", "with", "insert", "into", "update",
        "delete", "values", "create", "table", "primary", "key", "foreign", "references",
        "drop", "alter", "add", "constraint", "index", "view", "procedure", "function", "trigger",
        "replace", "declare", "set", "exec", "execute", "if", "exists", "null", "not", "between",
        "in", "like", "is", "true", "false", "limit", "offset", "fetch", "for", "while", "loop",
        "iterate", "repeat", "until", "leave", "elseif", "open", "close", "cursor", "fetch",
        "return"
    ])

    return [keyword for keyword in keywords if keyword.lower() not in sql_keywords]

def search_directory_for_keywords(directory):
    all_params = set()
    for root, dirs, files in os.walk(directory):
        # Exclude .git directory
        if '.git' in dirs:
            dirs.remove('.git')
        for file in files:
            if file.endswith(".py") and file != "extract_params.py":
                filepath = os.path.join(root, file)
                params = extract_keywords(filepath)
                all_params.update(params)
    return all_params

def clean_keywords_file(filepath):
    with open(filepath, "r") as file:
        keywords = file.readlines()
    
    cleaned_keywords = sorted(set(keyword.strip().replace('`', '') for keyword in keywords))

    with open(filepath, "w") as file:
        for keyword in cleaned_keywords:
            file.write(f"{keyword}\n")

def main():
    codebase_directory = "."  # Current directory
    params = search_directory_for_keywords(codebase_directory)
    
    unique_sorted_params = sorted(set(params))
    
    with open("extracted_keywords.txt", "w") as output_file:
        for param in unique_sorted_params:
            output_file.write(f"{param}\n")
    
    clean_keywords_file("extracted_keywords.txt")
    
    print("Extraction and cleaning complete. Keywords have been written to extracted_keywords.txt.")

if __name__ == "__main__":
    main()

#Usage:
# python3 extract_params.py
# It will extract the possible keywords from all the files and folders from the current directory.
