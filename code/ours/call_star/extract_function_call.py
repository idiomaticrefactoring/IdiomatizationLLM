'''
How to get all Call AST nodes from a given Python code.'''

'''
To get all Call AST nodes from a given Python code, you can use the `ast` module in Python. Here's an example code snippet:

```python
import ast

code = """
def foo():
    print("Hello, world!")
    
foo()
"""

tree = ast.parse(code)

calls = [node for node in ast.walk(tree) if isinstance(node, ast.Call)]

for call in calls:
    print(call)
```

In this example, we define a simple Python function `foo` that prints a message to the console, and then call it. We use the `ast.parse` function to parse the code into an AST (Abstract Syntax Tree) object, and then use the `ast.walk` function to traverse the tree and find all `ast.Call` nodes. Finally, we print out each `ast.Call` node that we found.

This code will output:

```
Call(func=Name(id='print', ctx=Load()), args=[Str(s='Hello, world!')], keywords=[])
Call(func=Name(id='foo', ctx=Load()), args=[], keywords=[])
```

As you can see, we found two `ast.Call` nodes: one for the `print` function call inside `foo`, and one for the `foo` function call itself.
'''

'''
We give you a code template, you write Python code to extract all Call AST nodes from a given Python code. 
def get_for(code):
    """
    extract all Call AST nodes 

    Parameters
    ----------
    code : string
        a Python code
    Returns
    -------
    result : list
          all Call AST nodes, please do not have the same element more than once
    """
'''
'''
We give you a code template, you write Python code to extract all Call AST nodes from a given Python code. 
def get_call(code):
    """
    extract all Call AST nodes 

    Parameters
    ----------
    code : string
        a Python code
    Returns
    -------
    result : set 
          all Call AST nodes
    """
'''
import ast

def get_call(code):
    """
    extract all Call AST nodes

    Parameters
    ----------
    code : string
        a Python code
    Returns
    -------
    result : set
          all Call AST nodes
    """
    result = set()
    tree = ast.parse(code)
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            result.add(node)
    return result

def get_call_2(code):
    """
    extract all Call AST nodes

    Parameters
    ----------
    code : string
        a Python code
    Returns
    -------
    result : set
          all Call AST nodes
    """
    result = []
    tree = ast.parse(code)
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if node not in result:
                result.append(node)
    return result
