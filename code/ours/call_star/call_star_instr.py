import os,sys
import struct
import traceback
code_dir = "/".join(os.path.abspath(__file__).split("/")[:-2]) + "/"
print("code path: ",code_dir)
sys.path.append(code_dir)
import chatgpt_util,random
import openai, tiktoken,ast,util
import ast
def is_subscript_node(code):
    try:
        node = ast.parse(code).body[0].value
        return isinstance(node, ast.Subscript)
    except:
        return False
def instr_is_subscript():
    real_instruction = '''
Write Python code to check whether a given code is a subscript AST node
for the given code a[-11:-9] + a[:1], it is not a subscript node
for the given code a[-11:-9], it is a subscript node
'''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
def func(a,b):

    print("come here: ",a,b)
if __name__ == '__main__':

    # instr_is_subscript()
    a=[1]
    b=[2]
    func(*a+b)
    pass