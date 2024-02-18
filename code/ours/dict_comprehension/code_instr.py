'''
How to determine whether a For AST node contains append function call in Python
'''

import os, sys
import struct
import traceback

code_dir = "/".join(os.path.abspath(__file__).split("/")[:-2]) + "/"
print("code path: ", code_dir)
sys.path.append(code_dir)
import chatgpt_util, random
import openai, tiktoken, ast, util
import ast


def instr_1():
    real_instruction = '''
python extract path through a statement from a given Python code how to describe the instruction
    '''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])



if __name__ == '__main__':
    # instr_1()
    code = '''
for i in a:
    if b:
        c[0].truadd(i)    
        add(i)  
        d.add(9)  
    '''
    code = '''
for i in a:
    if b:
        a.b[i]=b
        '''
    instr_1()

    import ast


    def extract_path(tree, target_lineno, target_col_offset):
        path = []

        def traverse(node):
            if isinstance(node, ast.stmt):
                path.append((node.lineno, node.col_offset))
            for child in ast.iter_child_nodes(node):
                if hasattr(child, 'lineno') and child.lineno == target_lineno and child.col_offset == target_col_offset:
                    path.append((child.lineno, child.col_offset))
                    return True
                elif traverse(child):
                    return True
            if path:
                path.pop()
            return False

        traverse(tree)
        return path


    def main():
        code = """
def foo():
    a = 1
    b = 2
    if a > 0:
        c = a + b
    else:
        c = a - b
    return c
        """

        tree = ast.parse(code)

        target_lineno = 6  # Line number of the statement you want to track
        target_col_offset = 8  # Column offset of the statement you want to track

        path = extract_path(tree, target_lineno, target_col_offset)
        for lineno, col_offset in path:
            print(f"Line {lineno}, Column {col_offset}")


    main()

