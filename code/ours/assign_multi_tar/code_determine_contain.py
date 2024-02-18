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
For a given set of string, get a new set of string by removing elements that belong to other element from the set.
    '''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
def extract_consecutive_ass(code):
    tree = ast.parse(code)

    consecutive_assigns = []
    prev_assign = None

    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            if prev_assign is not None:
                consecutive_assigns.append([prev_assign, node])
            prev_assign = node
    return consecutive_assigns
def remove_substrings(strings):
        result = set(strings)
        for s in strings:
            for t in strings:
                if s != t and s in t:
                    result.discard(s)
                    break
        return result
if __name__ == '__main__':
    # instr_1()
    code = """
a = 1
b = 2
c = 3
d=4
    """





    strings = {'hello', 'world', 'hell', 'he', 'llo'}
    strings = {'hello\n a=1\n b=1', 'a=1\n b=1', 'c=2 \n d=2'}

    new_strings = remove_substrings(strings)
    print(new_strings)
    # extract_2()
    # extract_consecu_ass()
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
