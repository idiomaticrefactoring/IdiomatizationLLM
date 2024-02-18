'''
We give you a code template, you write Python code to extract all values of Subscript AST nodes from arguments of a Call AST node.
def get_value(node):
    """
    extract all values of  Subscript AST nodes from arguments of a Call AST node

    Parameters
    ----------
    node : AST
        a Call AST node
    Returns
    -------
    result : set
          all values of  Subscript AST nodes
    """
'''
import ast
def get_value(node):
    result = set()
    if isinstance(node, ast.Call):
        for arg in node.args:
            if isinstance(arg, ast.Subscript):
                result.add(ast.unparse(arg.value))
    return result
