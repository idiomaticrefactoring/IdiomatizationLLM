import os,sys
import struct
import traceback
code_dir = "/".join(os.path.abspath(__file__).split("/")[:-2]) + "/"
print("code path: ",code_dir)
sys.path.append(code_dir)
import chatgpt_util,random
import openai, tiktoken,ast,util
import ast
import for_multi_tar_util
if __name__ == '__main__':
    '''
    Variable unpacking in for statements in Python is a way to assign values to multiple variables at once from an iterable object such as a list, tuple, or dictionary. It allows you to iterate over the iterable and assign each value to a separate variable in a single line of code. 
    '''
    user_instr = '''
You determine whether the iterable object "{{var}}" can be unpacked to assign the following unpacked elements? You answer based on the required response format. Please explain your answer.

unpacked elements:
{{element}}

response format:
Answer: You respond with Yes or No for whether the following iterable object can be unpacked to to assign the following unpacked elements.
Iterable Unpacking: If your answer is Yes, you give the Python code to unpacking the iterable object. Otherwise, you respond with None. Please explain it.
'''
    examples = [['''
You determine whether the iterable object "e" can be unpacked to assign the following unpacked elements? You answer based on the required response format. Please explain your answer.

unpacked elements:
e[1]
    
response format:
Answer: You respond with Yes or No for whether the following iterable object can be unpacked to to assign the following unpacked elements.
Iterable Unpacking: If your answer is Yes, you give the Python code to unpacking the iterable object. Otherwise, you respond with None. Please explain it.
''',
'''
Answer: Yes
Iterable Unpacking: e_0, e_1, *e_remaining = e
variable mapping:
e_1: e[1]
'''],
['''
You determine whether the iterable object "e" can be unpacked to assign the following unpacked elements? You answer based on the required response format. Please explain your answer.

unpacked elements:
e[0]
e[1]
e[1][1]
    
response format:
Answer: You respond with Yes or No for whether the following iterable object can be unpacked to to assign the following unpacked elements.
Iterable Unpacking: If your answer is Yes, you give the Python code to unpacking the iterable object. Otherwise, you respond with None. Please explain it.
''',
'''
Answer: Yes
Iterable Unpacking: e_0, e_1, *e_remaining = e
variable mapping:
e_0: e[0]
e_1: e[1]
e_1[1]: e[1][1]
'''],
['''
You determine whether the iterable object "e" can be unpacked to assign the following unpacked elements? You answer based on the required response format. Please explain your answer.

unpacked elements:
e[0]
e[1][1]
    
response format:
Answer: You respond with Yes or No for whether the following iterable object can be unpacked to to assign the following unpacked elements.
Iterable Unpacking: If your answer is Yes, you give the Python code to unpacking the iterable object. Otherwise, you respond with None. Please explain it.
''',
'''
Answer: Yes
Iterable Unpacking: e_0, (e_1_0, e_1_1, *e_1_remaining), *e_remaining = e
variable mapping:
e_0: e[0]
e_1_1: e[1][1]
'''],
['''
You determine whether the iterable object "e" can be unpacked to assign the following unpacked elements? You answer based on the required response format. Please explain your answer.

unpacked elements:
e[i]
e[1]
e['key']

response format:
Answer: You respond with Yes or No for whether the following iterable object can be unpacked to to assign the following unpacked elements.
Iterable Unpacking: If your answer is Yes, you give the Python code to unpacking the iterable object. Otherwise, you respond with None. Please explain it.
''',
'''
Answer: No
Iterable Unpacking: None
Explanation: The given the indices of unpacked element e[i], e['key'] are i and 'key' that are not int constants. Therefore, the iterable object "e" cannot be unpacked using the iterable unpacking syntax as it is not a sequence type like a list or tuple. Hence, the answer is No and the iterable unpacking code is not applicable in this case.
''']

]


    idiom = "for multi targets"
    idiom = "_".join(idiom.split(" "))
    save_complicated_code_dir_root = util.data_root + "chatgpt/NonIdiomatic/"
    # save_complicated_code_dir_root = util.data_root + "NonIdiomatic/find_code_snippets/"
    save_complicated_code_dir = save_complicated_code_dir_root + "sample_methods/"

    samples = util.load_pkl(save_complicated_code_dir, "sample_methods_" + idiom)


    # random.seed(2023)
    # samples = random.sample(samples, 30)
    file_name="whether_can_var_unpack_for_subscript_stmt_instr_explain_4_new_all_2"#"whether_can_var_unpack_for_subscript_stmt_instr_explain_4_new"
    # '''
    reponse_list = for_multi_tar_util.get_response_3(user_instr, examples, samples[:],
                                                sys_msg="You are a helpful assistant.")
    # util.save_pkl(save_complicated_code_dir_root + "chain_comparison_bool_compare/",
    #               "abstract_one_compare_instr",
    #               reponse_list)
    # util.save_pkl(save_complicated_code_dir_root+ idiom + "/",
    #               "extract_comparators_one_compare_instr",
    #               reponse_list)
    # '''
    util.save_pkl(save_complicated_code_dir_root + idiom + "/",
                  file_name,
                  reponse_list)
    
    samples = util.load_pkl(save_complicated_code_dir_root + idiom + "/", file_name)

    csv_res_list=for_multi_tar_util.save_csv(samples, [None for e in samples])
    util.save_csv(
        save_complicated_code_dir_root + idiom + "/" + file_name+".csv",
        csv_res_list,
        ["repo_name", "file_path", "file_html", "class_name", "me_name", "me_code", "old_code", "new_code", "bool_code",
         "chatGPT_code", "if_correct", "reversed_code", "non_replace_var_refactored_code", "refactored_code", "acc",
         "instruction", "sys_msg", "exam_msg", "user_msg"])
    # '''
