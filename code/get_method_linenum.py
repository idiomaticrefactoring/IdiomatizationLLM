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
    save_complicated_code_dir_root = util.data_root + "chatgpt/NonIdiomatic/"
    # save_complicated_code_dir_root = util.data_root + "NonIdiomatic/find_code_snippets/"
    save_complicated_code_dir = save_complicated_code_dir_root + "sample_methods/"
    idiom = "chain_comparison"
    idiom = "set_comprehension"

    file_name = idiom + "_methods"

    samples = util.load_pkl(save_complicated_code_dir_root, file_name)  # methods_sample
    line_num=0
    node_max=0
    for k in samples:
        *other, node=k
        if "in_roles.add(" in node:
            print("node: ",node)
        # print(node)
        line_num=max(len(node.split("\n")),line_num)
        # break
        if line_num==len(node.split("\n")):
            node_max=node
    # print(line_num)
    # print(node_max)
