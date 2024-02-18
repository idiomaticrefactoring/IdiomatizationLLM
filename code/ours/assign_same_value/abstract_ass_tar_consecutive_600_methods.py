import os, sys
import struct
import traceback

code_dir = "/".join(os.path.abspath(__file__).split("/")[:-2]) + "/"
print("code path: ", code_dir)
sys.path.append(code_dir)
import chatgpt_util, random
import openai, tiktoken, ast, util
import ast
import ass_same_value_util

if __name__ == '__main__':
    '''
    Variable unpacking in for statements in Python is a way to assign values to multiple variables at once from an iterable object such as a list, tuple, or dictionary. It allows you to iterate over the iterable and assign each value to a separate variable in a single line of code. 
    '''
    user_instr = '''
For the following Python code, you use only one symbol zj to represent assigned targets of assignment statements. Please do not change other code.

Python code:
{{code}}
'''
    examples = [
['''
For the following Python code, you use only one symbol zj to represent assigned targets of assignment statements. Please do not change other code.

Python code:
info.supportsACL = True
info.supportsExtendedMotion = True
info.supportsSharedQueue = True
info.supportsSystemPairing = True
''',
'''
symbols:
zj1: info.supportsACL
zj2: info.supportsExtendedMotion
zj3: info.supportsSharedQueue
zj4: info.supportsSystemPairing

New Python Code: 
zj1 = True
zj2 = True
zj3 = True
zj4 = True
'''],
['''
For the following Python code, you use only one symbol zj to represent assigned targets of assignment statements. Please do not change other code.

Python code:
message_input_model['spelling_suggestions'] = False
message_input_model['spelling_auto_correct'] = False
''',
'''
symbols:
zj1: message_input_model['spelling_suggestions']
zj2: message_input_model['spelling_auto_correct']

New Python Code: 
zj1 = False
zj2 = False
''']
]
    idiom = "chained_assignment"
    save_complicated_code_dir_root = util.data_root + "chatgpt/NonIdiomatic/"
    # save_complicated_code_dir_root = util.data_root + "NonIdiomatic/find_code_snippets/"
    save_complicated_code_dir = save_complicated_code_dir_root + "sample_methods/"

    # samples = util.load_pkl(save_complicated_code_dir_root, "methods_sample_10000")  # methods_sample
    # sample_code_list = ass_same_value_util.extract_module_consecutive_ass(samples)

    file_name = "new_idiom_methods_600"
    samples = util.load_pkl(save_complicated_code_dir_root, file_name)  # methods_sample

    # file_name = "extract_arithmetic_seq_from_abstract_same_subscript_value_arguments_instr7_all_2_sample"  # "extract_arithmetic_seq_from_arguments_instr3_all"  # "whether_can_var_unpack_for_subscript_stmt_instr_explain_4_new"
    sample_code_list = ass_same_value_util.extract_module_consecutive_ass_from_methods(samples)

    # random.seed(2023)
    # samples = random.sample(sample_code_list, 324)
    # extract_module(samples)
    # '''
    # reponse_list = ass_same_value_util.get_response_directly_refactor(user_instr, examples, sample_code_list,
    #                                                                   sys_msg="You are a helpful assistant.")
    # file_name="abstract_ass_tar_consecutive"
    # util.save_pkl(save_complicated_code_dir_root + idiom + "/",
    #               file_name,
    #               reponse_list)
    '''
    samples = util.load_pkl(save_complicated_code_dir_root + idiom + "/", file_name)

    csv_res_list=call_star_util.save_csv(samples, [None for e in samples])
    util.save_csv(
        save_complicated_code_dir_root + idiom + "/" + file_name+".csv",
        csv_res_list,
        ["repo_name", "file_path", "file_html", "class_name", "me_name", "me_code", "old_code", "new_code", "bool_code",
         "chatGPT_code", "if_correct", "reversed_code", "non_replace_var_refactored_code", "refactored_code", "acc",
         "instruction", "sys_msg", "exam_msg", "user_msg"])
    '''
