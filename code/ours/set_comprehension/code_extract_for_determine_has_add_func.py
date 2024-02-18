'''
How to determine whether a For AST node contains append function call in Python
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
def instr_last_line():
    real_instruction = '''
Extract the last line of code and determine whether it is a function call statement.

for example, for the following Python code
for i in a:
    if b:
        a.add(i)  

the last line is: a.add(i), and it is a function call
    '''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
def instr_3():
    real_instruction = '''
Write Python code to check whether the whole Python code is a function call in Python

for example, for the following Python code
a.add(i)

it is a function call

for another example, for the following Python code
a= func(i)

it is an assignment statement and is not a function call
    '''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
def is_function_call_2(code):
    try:
        parsed = ast.parse(code)
        if isinstance(parsed.body[0], ast.Expr) and isinstance(parsed.body[0].value, ast.Call):
            return True
        else:
            return False
    except:
        return False
def is_function_call(code):
    try:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                return True
        return False
    except SyntaxError:
        return False
def instr_2():
    real_instruction = '''
Write Python code to extract the last line of code

for example, for the following Python code
for i in a:
    if b:
        a.add(i)  

the last line is: a.add(i)
    '''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
def get_last_line(code):
    last_line = code.strip().split('\n')[-1].strip()
    return last_line
def get_last_function_call(node):
    last_call = None
    for child in ast.iter_child_nodes(node):
        if isinstance(child, ast.Expr) and isinstance(child.value, ast.Call):
            last_call = child.value
    return last_call
def last_line_is_call(tree):
    # Traverse the AST to find the last node
    last_node = None
    for node in ast.walk(tree):
        if hasattr(node, 'lineno') and node.lineno > ast.increment_lineno(tree, -1):
            last_node = node
    # Check if the last node is a function call
    if isinstance(last_node, ast.Expr) and isinstance(last_node.value, ast.Call):
        return last_node
    else:
        None

def instr_fun_name_is_given_string():
    real_instruction = '''
Write Python code to determine whether the function name of a given function call node is a given string, if it is you also extract its corresponding object in Python

for example, for the function call: a.c.add(i), a given string is add
its function name of function call is add, so the function name of the function call is add. And the object is "a.c"
    '''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])

def extract_function_object(code, function_name):
    tree=ast.parse(code)
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if node.func.attr == function_name:
                obj = ast.unparse(node.func.value).strip()
                return obj, node.func.attr
    return None, None

def is_function_name(node, name):
    if isinstance(node, ast.Call):
        if isinstance(node.func, ast.Name):
            return node.func.id == name
        elif isinstance(node.func, ast.Attribute):
            return node.func.attr == name
    return False

def instr_1():

    real_instruction = '''
How to determine whether a given AST node contains a given string function call  in Python

for example, for the following Python code, a given string is add
for i in a:
    if b:
        a.add(i)  
        
it contains add function call
    '''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])

class FunctionCallVisitor(ast.NodeVisitor):
    def __init__(self, function_name):
        self.function_name = function_name
        self.found = False

    def visit_Call(self, node):
        if isinstance(node.func, ast.Attribute) and node.func.attr == self.function_name:
            self.found = True

        self.generic_visit(node)

def if_has_add(tree,name="add"):
    visitor = FunctionCallVisitor(name)
    visitor.visit(tree)
    return visitor.found


def instr_def_stmt():
    real_instruction = '''
Find the def that reach a stmt graph[u].add(v) of the following Python code.

Python code:
graph = {}
for u in self.complete:
    graph[u] = set()
    for v in self.complete[u]:
        if u != v:  # ignore self-loop
            graph[u].add(v)

response format:
Answer: You respond with Yes or No for whether there is a def statement that reach a node of a given Python code.
Information: If your answer is Yes, you give the def statement. Otherwise, you respond with None. Please explain it.
    '''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])

def instr_code_before_line():
    real_instruction = '''
Write Python code to extract code before a given line number including the line number from a given Python code in Python
'''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
def extract_code_before_line_number(code, line_number):
    lines = code.split('\n')
    if line_number > len(lines):
        return code
    else:
        return '\n'.join(lines[:line_number])
if __name__ == '__main__':
    # instr_1()
    # instr_2()
    instr_3()
    # instr_code_before_line()
    # instr_3()
    # instr_def_stmt()
    # instr_fun_name_is_given_string()
    code='''
for i in a:
    if b:
        c[0].truadd(i)    
        add(i)  
        d.add(9)  
    '''
    code = '''
for i in a:
    for j in b:
        if b:
            w
            c.add(i)
        '''
    code1 = "a.add(i)"
    code2 = "a = func(i)"
    print(is_function_call_2(code1))
    print(is_function_call_2(code2))

    # for node in ast.walk(ast.parse(code)):
    #     if isinstance(node,ast.For):
    #         print(if_has_add(node,name="add"))
    # print(contains_match(code))
    # idiom = "call_star"
    # save_complicated_code_dir_root = util.data_root + "chatgpt/NonIdiomatic/"
    # # save_complicated_code_dir_root = util.data_root + "NonIdiomatic/find_code_snippets/"
    # save_complicated_code_dir = save_complicated_code_dir_root + "sample_methods/"
    #
    # samples = util.load_pkl(save_complicated_code_dir, "sample_methods_" + idiom)
    #
    # # extract_consecutive_subscripts(node)
    # # random.seed(2023)
    # # samples = random.sample(samples, 30)
    # file_name="abstract_same_value_all"#"whether_can_var_unpack_for_subscript_stmt_instr_explain_4_new"
    # reponse_list = call_star_util.abstract_consecutive(samples)
    # util.save_pkl(save_complicated_code_dir_root + idiom + "/",
    #               file_name,
    #               reponse_list)
