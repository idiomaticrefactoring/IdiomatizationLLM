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
We give you a code template, you write Python code to extract all For AST nodes from a given Python code.
def get_for(code):
    """
    Extract all For AST nodes.

    Parameters
    ----------
    code : string
        a Python code
    Returns
    -------
    result : set
          all For AST nodes
    """
'''
import ast

def get_for(code):
    """
    Extract all For AST nodes.

    Parameters
    ----------
    code : string
        a Python code
    Returns
    -------
    result : set
          all For AST nodes
    """
    tree = ast.parse(code)
    result = []
    for node in ast.walk(tree):
        if isinstance(node, ast.For):
            if node not in result:
                result.append(node)
    return result
if __name__ == '__main__':
    save_complicated_code_dir_root = util.data_root + "chatgpt/NonIdiomatic/"
    save_complicated_code_dir=save_complicated_code_dir_root+"sample_methods/"
    idiom="for multi targets"
    idiom = "_".join(idiom.split(" "))
    samples = util.load_pkl(save_complicated_code_dir, "sample_methods_" + idiom)
    for ind_sampl, sample_method in enumerate(samples):
        for code in sample_method:
            get_for(code)