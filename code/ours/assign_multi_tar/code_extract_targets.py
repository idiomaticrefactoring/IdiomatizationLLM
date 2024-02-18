'''
Extract all consecutive assign nodes from a given Python code in Python
'''

import os,sys
import struct
import traceback
code_dir = "/".join(os.path.abspath(__file__).split("/")[:-2]) + "/"
print("code path: ",code_dir)
sys.path.append(code_dir)
import chatgpt_util,random
import openai, tiktoken,ast,util
import ast

def instr_1():
    real_instruction = '''
Write Python code to determine whether an assignment statement uses the variable names of a set.
'''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
def get_all_Name_from_target(code):
    tree = ast.parse(code)
    name_nodes = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    name_nodes.add(target.id)
    return name_nodes
def get_all_Name_from_target_2(code):
    tree = ast.parse(code)

    # Define a function to recursively search for Name nodes in the AST
    def find_names(node):
        if isinstance(node, ast.Name):
            return {node.id}
        elif isinstance(node, ast.Attribute):
            return find_names(node.value)
        elif isinstance(node, ast.Subscript):
            return find_names(node.value)
        elif isinstance(node, ast.Tuple):
            names = set()
            for elt in node.elts:
                names |= find_names(elt)
            return names
        elif isinstance(node, ast.List):
            names = set()
            for elt in node.elts:
                names |= find_names(elt)
            return names
        elif isinstance(node, ast.Dict):
            names = set()
            for key, value in zip(node.keys, node.values):
                names |= find_names(key)
                names |= find_names(value)
            return names
        else:
            names = set()
            for child in ast.iter_child_nodes(node):
                names |= find_names(child)
            return names

    # Find all Name nodes in the targets of assignment statements
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                names |= find_names(target)

    print(names)
    return names
def instr_name_from_targets():
    real_instruction = '''
Write Python code to find all Name AST nodes of targets of assignment statements of a given Python code.

for example, for the Python code:
a.imag = 9
res = a.execute().fetch()
c, d[0] = d

targets of assignment statements are: a.imag, res, c, d[0]
so all Name AST nodes of targets of assignment statements are: {a, res, c, d}
'''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])

def instr_name():
    real_instruction = '''
Write Python code to get all Name AST nodes from a given Python code.
'''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
def instr_targets():
    real_instruction = '''
Write Python code to get all targets of assignment statements from a given Python code.
for example, for the Python code:
a.imag = 9
res = a.execute().fetch()

the targets are [a.imag, res]
'''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
def instr_4():
    real_instruction = '''
Write Python code to get all variables of targets of assignment statements of a given Python code.

for example, for the Python code:
a.imag = 9
res = a.execute().fetch()

the targets are: a.imag, res
so variables are: {a, res}
'''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
def instr_var_intersect():
    real_instruction = '''
Write Python code to determine whether a variable set intersects with another variable set
'''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])

def instr_3():
    real_instruction = '''
Write Python code to determine whether the variable set of an assignment statement intersects with a variable set

for example, 
for the assignment statment: res = a.execute().fetch(), its variable set is {res, a}, a variable set: {a, 9}
the assignment contains one variable a in the set {a, 9}
'''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
def instr_5():
    real_instruction = '''
Write Python code to find all Name AST nodes of value of an assignment statement of a given Python code.
'''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])



if __name__ == '__main__':
    # instr_1()
    # instr_2()
    # instr_3()
    # instr_2()
    # instr_name()
    # instr_targets()
    # instr_name_from_targets()
    # instr_5()
    # instr_4()
    instr_5()
    code = """
a = 1
b = 2
c = 3
d=a
    """


    code = """
a.imag = 9
res = a.execute().fetch()
c, d =a
    """
    # Parse the code into an abstract syntax tree (AST)
    tree = ast.parse(code)


    # Define a visitor class to extract the targets of assignment statements
    class AssignmentVisitor(ast.NodeVisitor):
        def __init__(self):
            self.targets = []

        def visit_Assign(self, node):
            for target in node.targets:
                self.targets.append(ast.dump(target))


    # Visit the AST with the AssignmentVisitor
    visitor = AssignmentVisitor()
    visitor.visit(tree)

    # Print the targets of assignment statements
    print(visitor.targets)
