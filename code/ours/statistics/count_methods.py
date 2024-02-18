import os, sys
import struct
import traceback

code_dir = "/".join(os.path.abspath(__file__).split("/")[:-2]) + "/"
print("code path: ", code_dir)
sys.path.append(code_dir)
import chatgpt_util, random
import openai, tiktoken, ast, util
import ast,copy
if __name__ == '__main__':
    idiom = "dict_comprehension"
    save_complicated_code_dir_root = util.data_root + "chatgpt/NonIdiomatic/"
    save_complicated_code_dir = save_complicated_code_dir_root + "sample_methods/"
    method_code_list=[]
    for file_path in os.listdir(save_complicated_code_dir):
        print("file+path: ",file_path)
        if file_path.endswith(".pkl"):
            samples = util.load_pkl(save_complicated_code_dir, file_path[:-4])
            for ind_sampl, sample_method in enumerate(samples):
                for code in sample_method:
                    repo_name,file_path,*other, method_code = code
                    print("repo_name,file_path: ",repo_name,file_path)
                    if [repo_name, file_path, method_code] not in method_code_list:
                        method_code_list.append([repo_name,file_path, method_code])
                    break
    print("method_code_list: ",len(method_code_list))

