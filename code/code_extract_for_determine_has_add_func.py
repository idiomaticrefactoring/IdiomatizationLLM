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

def instr_1():

    real_instruction = '''
Write Python code to determine whether a given AST node has an assign statement whose assigned data is a subscript node in Python

for example, for the following Python code, a given string is add
for i in a:
    if b:
        a.b[i]=b
        
it contains an assign statement: a.b[i]=b, its assigned data is a subscript node: a.b[i] in Python
    '''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])

def has_subscript_assign(node):
    if isinstance(node, ast.Assign):
        for target in node.targets:
            if isinstance(target, ast.Subscript):
                return True
    return False

def if_assign_subscript(tree):
    for node in ast.walk(tree):
        if has_subscript_assign(node):
            return True
    return False
class AssignVisitor(ast.NodeVisitor):
    def visit_Assign(self, node):
        # Check if the assigned data is a subscript node
        if isinstance(node.targets[0], ast.Subscript):
            return True


if __name__ == '__main__':
    # instr_1()
    code='''
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
    for node in ast.walk(ast.parse(code)):
        if isinstance(node,ast.For):
            print(if_assign_subscript(node))
            print(if_assign_subscript(node))

            '''
            # Define a visitor class to traverse the AST
            class AssignVisitor(ast.NodeVisitor):
                def visit_Assign(self, node):
                    # Check if the assigned data is a subscript node
                    if isinstance(node.targets[0], ast.Subscript):
                        print("Found assign statement with subscript node:", node.targets[0])
                        return True

            # Traverse the AST with the visitor
            visitor = AssignVisitor()
            print(visitor.visit(node))
            '''
            # print(if_has_add(node,name="add"))
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
