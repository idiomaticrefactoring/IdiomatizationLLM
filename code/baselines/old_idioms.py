import os, sys
import struct
import traceback

import util_rewrite

code_dir = "/".join(os.path.abspath(__file__).split("/")[:-2]) + "/"
print("code path: ", code_dir)
sys.path.append(code_dir)
import chatgpt_util, random, chat_gpt_ast_util
import openai, tiktoken, ast, util, util_rewrite
import ast
if __name__ == '__main__':
    idiom = "list_comprehension"
    idiom = "dict_comprehension"
    idiom = "set_comprehension"
    idiom = "loop_else"
    idiom = "chain_comparison"
    idiom = "truth value testing"
    idiom = "_".join(idiom.split(" "))
    idiom = "call_star"
    idiom = "assign_multiple_targets"
    idiom = "for multi targets"
    idiom = "_".join(idiom.split(" "))
    save_complicated_code_dir_root = util.data_root + "chatgpt/NonIdiomatic/"
    # save_complicated_code_dir_root = util.data_root + "NonIdiomatic/find_code_snippets/"
    save_complicated_code_dir = save_complicated_code_dir_root + "sample_methods/"

    samples = util.load_pkl(save_complicated_code_dir, "sample_methods_" + idiom)
    method_code_list=[]
    for ind_sampl, sample_method in enumerate(samples):
        for code in sample_method:
            *other, old_list, new_tree, \
            old_code, new_code, method_code = code
            method_code_list.append([*other, method_code])

            # method_code_list.append([*other, old_list, new_tree, old_code, new_code, method_code])
            print("*other: ",*other)
            print("old_code: ", old_code)
            print("new_code: ", new_code)
            break

    file_name = idiom+"_methods"
    util.save_pkl(save_complicated_code_dir_root,
                  file_name,
                  method_code_list)
    print("len of methods: ",len(method_code_list))