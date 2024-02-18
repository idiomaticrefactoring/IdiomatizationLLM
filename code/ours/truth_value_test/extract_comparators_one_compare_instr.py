import os,sys
import struct
import traceback
code_dir = "/".join(os.path.abspath(__file__).split("/")[:-2]) + "/"
print("code path: ",code_dir)
sys.path.append(code_dir)
import chatgpt_util,random
import openai, tiktoken,ast,util
import ast
import truth_test_util
if __name__ == '__main__':
    user_instr = '''
For the following comparison operation Python code, you extract comparison values.

Python code:
{{code}}
'''
    examples = [['''
For the following comparison operation Python code, you extract comparison values.

Python code:
a % b == 0
''',
'''
v1: a % b
v2: 0
''']

]

    idiom = "truth value testing"
    idiom = "_".join(idiom.split(" "))
    save_complicated_code_dir_root = util.data_root + "chatgpt/NonIdiomatic/"
    # save_complicated_code_dir_root = util.data_root + "NonIdiomatic/find_code_snippets/"
    save_complicated_code_dir = save_complicated_code_dir_root + "sample_methods/"

    samples = util.load_pkl(save_complicated_code_dir, "sample_methods_" + idiom)

    # random.seed(2023)
    # samples = random.sample(samples, 30)
    reponse_list = truth_test_util.get_response_compare(user_instr, examples, samples[:],
                                                sys_msg="You are a helpful assistant.")
    # util.save_pkl(save_complicated_code_dir_root + "chain_comparison_bool_compare/",
    #               "abstract_one_compare_instr",
    #               reponse_list)
    # util.save_pkl(save_complicated_code_dir_root+ idiom + "/",
    #               "extract_comparators_one_compare_instr",
    #               reponse_list)

    util.save_pkl(save_complicated_code_dir_root + idiom + "/",
                  "extract_comparators_one_compare_instr_all",
                  reponse_list)