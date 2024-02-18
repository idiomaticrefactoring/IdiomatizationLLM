import os, sys
import struct
import traceback

code_dir = "/".join(os.path.abspath(__file__).split("/")[:-3]) + "/"
print("code path: ", code_dir)
sys.path.append(code_dir)
import chatgpt_util, random
import openai, tiktoken, ast, util
import ast,copy


if __name__ == '__main__':
    save_complicated_code_dir_root = util.data_root + "chatgpt/NonIdiomatic/"
    file_name="methods_1"#"methods_flat"
    res_list_pkl = util.load_pkl(save_complicated_code_dir_root, file_name)
    repo_list=set([])
    for e in res_list_pkl:
        print(e)
        # for ele in e:
        #     print(ele)
        #     if isinstance(ele,ast.AST):
        #         print("code: ",ast.unparse(ele))
        # repo_list.add(e[0])
        break
    print("len: ",len(res_list_pkl),len(repo_list))
