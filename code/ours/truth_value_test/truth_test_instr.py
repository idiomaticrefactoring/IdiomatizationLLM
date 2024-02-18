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
    #Write Python code to get comparison values for a given Compare node

    real_instruction = '''
Write Python code to return comparison values for a given Compare node
for example,
for the code a==0,
comparison values are a,0
for the code self.a!=func(c)
comparison values are self.a,func(c)
'''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
def get_values(compare_node):
    # Get the left and right values of the comparison
    # Get the left and right values of the comparison
    left_value = ast.unparse(compare_node.left).strip()
    right_value = ast.unparse(compare_node.comparators[0]).strip()

    # Return the comparison values
    return left_value, right_value
def instr_2():
    real_instruction = '''
Write Python code to return comparison operators for a given comparison expression
for example,
for the code a==0,
comparison operators are ==
for the code self.a!=func(c)
comparison operators are !=
'''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
def instr_3():
    real_instruction = '''
Write Python code to check whether the comparison operator is == or != for a given comparison operation. If they are return the corresponding comparison operator.
for the comparison operation a==0,
the comparison operators are ==
for the comparison operation self.a!=func(c)
the comparison operators are !=
'''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
def check_comparison_operator(operation):
    if "==" in operation:
        return "=="
    elif "!=" in operation:
        return "!="
    else:
        return None
def get_comparison_operator(expression):
    operators = ['==', '!=', '<', '>', '<=', '>=', 'in', 'not in', 'is', 'is not']
    for operator in operators:
        if operator in expression:
            return operator
    return None
def join_string_instr():
    real_instruction = '''
Write Python code to join given several strings using given string
for example,
for the given several strings: "not", "world", "hello", the given string is " "
the new string is "not world hello"
'''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])

def is_len_instr():
    real_instruction = '''
Write Python code to determine whether the given Python code is a call function whose name is len, if it is, please also return its argument
for example,
for the given Python code: len(a+b), it is a call function function whose name is len, and its argument is a+b.
'''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])

def find_len_arg(code):
    tree = ast.parse(code)
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'len':
            arg = node.args[0]
            return arg
    return None


def is_len_call(code):
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return False

    if not isinstance(tree, ast.Module):
        return False

    if len(tree.body) != 1:
        return False

    expr = tree.body[0]
    if not isinstance(expr, ast.Expr):
        return False

    if not isinstance(expr.value, ast.Call):
        return False

    func = expr.value.func
    if not isinstance(func, ast.Name):
        return False

    if func.id != 'len':
        return False

    arg = expr.value.args[0]
    return arg

def remove_starts_with():
    real_instruction = '''
Write Python code to check whether a given string starts with a given substring. If it is, remove the given substring
for example,
for the given string: not len(a+b), a given substring is "not "
the given string starts with "not ", so the new string len(a+b)
'''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
def remove_starts_substring(string,substring):
    if string.startswith(substring):
        new_string = string[len(substring):]
        return new_string
    return string
if __name__ == '__main__':
    # instr_1()
    # instr_2()
    # instr_3()
    # join_string_instr()
    # is_len_instr()
    # is_len_instr()
    remove_starts_with()
    compare_node = ast.parse("x > y").body[0].value
    print("compare_node: ",compare_node)
    # result = eval(compile(ast.Expression(compare_node), '', 'eval'))
    left_value,right_value=get_values(compare_node)
    # print(result)
    print(left_value,right_value)
    ops=get_comparison_operator("x > y")
    print(ops)
    strings = ["not", "world", "hello"]
    delimiter = " "
    code = 'len(a+b)'
    # code = 'len(a+b)/2'
    # code = 'len(a+b) + len(c)'
    # arg = find_len_arg(code)
    arg = is_len_call(code)
    if arg:
        print(f"The argument of len() is {ast.unparse(arg)}")
    else:
        print("The code is not a call to len()")
    new_string = delimiter.join(strings)

    print(new_string)
    pass