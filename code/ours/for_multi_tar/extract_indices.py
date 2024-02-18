import ast
'''
# Example code with a Subscript node
code = "my_list[0][1]"

# Parse the code into an AST
tree = ast.parse(code)

# Find the Subscript node
subscript_node = next(node for node in ast.walk(tree) if isinstance(node, ast.Subscript))

# Extract the indices of the Subscript node
indices = [ast.unparse(index) for index in subscript_node.slice]

print(indices)  # Output: [0, 1]
'''
'''
import ast

# Define a sample code snippet
code = "my_list[0][1][2:3]"

# Parse the code into an AST
tree = ast.parse(code)

# Define a function to recursively search for Subscript nodes
def find_subscripts(node, indices):
    if isinstance(node, ast.Subscript):
        indices.append(node.slice.value)
        find_subscripts(node.value, indices)


# Find all Subscript nodes in the AST and extract their indices
subscripts = []
for node in ast.walk(tree):
    find_subscripts(node, subscripts)

# Print the indices of the Subscript node
print(subscripts)
'''

import ast

# Example code with a Subscript node
code = "my_list[0][1][2]"

# Parse the code into an AST
tree = ast.parse(code)

# Define a visitor class to find all Subscript nodes
class SubscriptVisitor(ast.NodeVisitor):
    def __init__(self):
        self.subscripts = []

    def visit_Subscript(self, node):
        self.subscripts.append(node)
        self.generic_visit(node)

# Find all Subscript nodes in the AST
visitor = SubscriptVisitor()
visitor.visit(tree)

# Extract all indices of the first Subscript node
subscript_node = visitor.subscripts[0]
indices = [index for index in subscript_node.slice.elts]

print(indices)  # Output: [0, 1, 2]