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
fast_approx = True
input_tensor.requires_grad = True
''',
'''
symbols:
zj1: fast_approx
zj2: input_tensor.requires_grad


New Python Code: 
zj1 = True
zj2 = True
'''],
['''
For the following Python code, you use only one symbol zj to represent assigned targets of assignment statements. Please do not change other code.

Python code:
self.result.tracks[0].AR['v1']['DBCRC'] = None
self.result.tracks[0].AR['v1']['DBConfidence'] = None
''',
'''
symbols:
zj1: self.result.tracks[0].AR['v1']['DBCRC']
zj2: self.result.tracks[0].AR['v1']['DBConfidence']

New Python Code: 
zj1 = None
zj2 = None
''']
]
    idiom = "chained_assignment"
    save_complicated_code_dir_root = util.data_root + "chatgpt/NonIdiomatic/"
    # save_complicated_code_dir_root = util.data_root + "NonIdiomatic/find_code_snippets/"
    save_complicated_code_dir = save_complicated_code_dir_root + "sample_methods/"

    samples = util.load_pkl(save_complicated_code_dir_root, "methods_sample_10000")  # methods_sample
    sample_code_list = ass_same_value_util.extract_module(samples)
    # random.seed(2023)
    # samples = random.sample(sample_code_list, 324)
    # extract_module(samples)
    # '''
    reponse_list = ass_same_value_util.get_response_directly_refactor(user_instr, examples, sample_code_list,
                                                                      sys_msg="You are a helpful assistant.")
    file_name="abstract_ass_tar"
    util.save_pkl(save_complicated_code_dir_root + idiom + "/",
                  file_name,
                  reponse_list)
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
