import os,sys
import traceback
code_dir = "/".join(os.path.abspath(__file__).split("/")[:-2]) + "/"
print("code path: ",code_dir)
sys.path.append(code_dir)
import chatgpt_util,random
import openai, tiktoken,ast,util
import ast
user_str='''
Write Python code to get all BoolOp AST nodes and AST node whose attribute test of type ast.expr  for a given Python code.
'''
#Write Python code to extract all BoolOp AST nodes and AST nodes with a test attribute of type ast.expr from a given Python code.
# user_instr='''
# We give you a code template, you write Python code to extract all BoolOp AST nodes and AST nodes with a test attribute of type ast.expr from a given Python code.
# def get_BoolOp_test(code):
#     """
#     Extract all BoolOp AST nodes and AST nodes with a test attribute of type ast.expr from a given Python code.
#
#     Parameters
#     ----------
#     code : string
#         a Python code
#     Returns
#     -------
#     result : list
#          all BoolOp AST nodes and AST nodes with a test attribute of type ast.expr
#     """
# '''
user_instr='''
We give you a code template, you write Python code to find all comparison operations whose comparison operator can only be "==" or "!=" from a given Python code. 

def get_compare(code):
    """
    find all comparison operations whose comparison operator can only be "==" or "!="

    Parameters
    ----------
    code : string
        a Python code
    Returns
    -------
    result : list
          all comparison operations whose comparison operator can only be "==" or "!="
    """
'''

answer_instr='''
One possible implementation of the `get_compare` function is:

```python
import ast

def get_compare(code):
    """
    find all comparison operations whose comparison operator can only be "==" or "!="

    Parameters
    ----------
    code : string
        a Python code
    Returns
    -------
    result : list
          all comparison operations whose comparison operator can only be "==" or "!="
    """
    class CompareVisitor(ast.NodeVisitor):
        def __init__(self):
            self.result = []

        def visit_Compare(self, node):
            if len(node.ops) == 1:
                op = node.ops[0]
                if isinstance(op, ast.Eq) or isinstance(op, ast.NotEq):
                    self.result.append(node)

    tree = ast.parse(code)
    visitor = CompareVisitor()
    visitor.visit(tree)
    return visitor.result
```

This implementation uses the `ast` module to parse the input code into an abstract syntax tree (AST), and then traverses the tree using a custom `CompareVisitor` class that extends the `ast.NodeVisitor` base class. The `CompareVisitor` class overrides the `visit_Compare` method to check if the comparison operation has only one operator, and if that operator is either `ast.Eq` (for `==`) or `ast.NotEq` (for `!=`). If the condition is satisfied, the comparison node is added to the `result` list.

To use this function, simply call it with a string containing the Python code to analyze, like this:

```python
code = """
x = 1
y = 2
if x == y:
    print("x equals y")
if x != y:
    print("x is not equal to y")
if x < y:
    print("x is less than y")
"""
result = get_compare(code)
print(result)
```

This will output:

```
[<_ast.Compare object at 0x7f9c5c1d7d90>, <_ast.Compare object at 0x7f9c5c1d7e10>]
```

which indicates that the two comparison operations `x == y` and `x != y` were found in the code.
'''

import ast

import ast

def get_compare(code):
    """
    find all comparison operations whose comparison operator can only be "==" or "!="

    Parameters
    ----------
    code : string
        a Python code
    Returns
    -------
    result : list
          all comparison operations whose comparison operator can only be "==" or "!="
    """
    class CompareVisitor(ast.NodeVisitor):
        def __init__(self):
            self.result = []

        def visit_Compare(self, node):
            if len(node.ops) == 1:
                op = node.ops[0]
                if isinstance(op, ast.Eq) or isinstance(op, ast.NotEq):
                    self.result.append(node)

    tree = ast.parse(code)
    visitor = CompareVisitor()
    visitor.visit(tree)
    return visitor.result

if __name__ == '__main__':
    code='''
x = 1
y = 2
if x == y or (func(a and b==0)):
    print("x equals y")
if x != y:
    print("x is not equal to y")
if x < y:
    print("x is less than y")    
'''
    result=get_compare(code)
    for e in result:
        print("code: ",ast.unparse(e))