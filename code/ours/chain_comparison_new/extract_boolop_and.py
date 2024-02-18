# def get_BoolOp_And(code):
#     """
#     Get all BoolOp AST node whose op is "And"
#
#     Parameters
#     ----------
#     code : string
#         a Python code
#     Returns
#     -------
#     result : list
#         all BoolOp AST nodes whose op is "And"
#     """
#

'''
We give you a code template, you write Python code to get all BoolOp AST node whose op is "And"

def get_BoolOp_And(code):
    """
    Get all BoolOp AST node whose op is "And"

    Parameters
    ----------
    code : string
        a Python code
    Returns
    -------
    result : list
        all BoolOp AST nodes whose op is "And"
    """
'''
import os,sys
import traceback
code_dir = "/".join(os.path.abspath(__file__).split("/")[:-2]) + "/"
print("code path: ",code_dir)
sys.path.append(code_dir)
import chatgpt_util,random
import openai, tiktoken,ast,util
# import ast
#
# def get_BoolOp_And(code):
#     """
#     Get all BoolOp AST node whose op is "And"
#
#     Parameters
#     ----------
#     code : string
#         a Python code
#     Returns
#     -------
#     result : list
#         all BoolOp AST nodes whose op is "And"
#     """
#     tree = ast.parse(code)
#     result = []
#     for node in ast.walk(tree):
#         if isinstance(node, ast.BoolOp) and isinstance(node.op, ast.And):
#             result.append(node)
#     return result

import ast

def get_BoolOp_And(code):
    """
    Get all BoolOp AST node whose op is "And"

    Parameters
    ----------
    code : string
        a Python code
    Returns
    -------
    result : set
        all BoolOp AST nodes whose op is "And"
    """
    tree = ast.parse(code)
    result = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.BoolOp) and isinstance(node.op, ast.And):
            result.add(node)
    return result
if __name__ == '__main__':
    save_complicated_code_dir_root = util.data_root + "chatgpt/NonIdiomatic/"
    save_complicated_code_dir=save_complicated_code_dir_root+"sample_methods/"
    idiom = "chain comparison"
    idiom = "_".join(idiom.split(" "))
    samples = util.load_pkl(save_complicated_code_dir, "sample_methods_" + idiom)
    for ind_sampl, sample_method in enumerate(samples):
        for code in sample_method:
            get_BoolOp_And(code)
