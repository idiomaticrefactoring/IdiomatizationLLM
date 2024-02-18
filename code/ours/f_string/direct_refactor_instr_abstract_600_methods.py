import os, sys
import struct
import traceback

import util_rewrite

code_dir = "/".join(os.path.abspath(__file__).split("/")[:-2]) + "/"
print("code path: ", code_dir)
sys.path.append(code_dir)
import chatgpt_util, random, chat_gpt_ast_util
import openai, tiktoken, ast, util, util_rewrite
import ast, fstring_util


if __name__ == '__main__':

    user_instr = '''
Refactor the following Python code with fstring. Do not refactor other part of code.

Python code:
{{code}}

response format:
Answer: You respond with Yes or No for whether the code can be refactored with fstring.
Information: If your answer is Yes, you give the refactored code. Otherwise, you respond with None. 
'''
    examples = [
['''
Refactor the following Python code with fstring. Do not refactor other part of code.

Python code:
print("The quick brown %s jumped over the lazy sleeping %s" % (e_zj_1, e_zj_2))

response format:
Answer: You respond with Yes or No for whether the code can be refactored with iterable unpacking into one assignment statement that assign a slicing sequence: "input_shape" to multiple variables.
Information: If your answer is Yes, you give the refactored code. Otherwise, you respond with None. 
''',
'''
Answer: Yes
Information:
print(f"The quick brown {e_zj_1} jumped over the lazy sleeping {e_zj_2}")
''']]#Explanation:
# the object "inputs" is not a sequence type object, but rather a dictionary. Hence, it cannot be unpacked to elements.


    idiom = "with_stmt"
    idiom = "list_comprehension"
    idiom = "set_comprehension"
    idiom = "dict_comprehension"
    idiom = "chained_assignment"
    idiom = "unpack_assignment"
    idiom = "fstring"

    save_complicated_code_dir_root = util.data_root + "chatgpt/NonIdiomatic/"
    # save_complicated_code_dir_root = util.data_root + "NonIdiomatic/find_code_snippets/"
    save_complicated_code_dir = save_complicated_code_dir_root + "sample_methods/"


    sample_code_list = util.load_pkl(save_complicated_code_dir_root + idiom + "/",
                      "abstract_samples_fstring_600_methods")  # methods_sample

    # file_name = "extract_arithmetic_seq_from_abstract_same_subscript_value_arguments_instr7_all_2_sample"  # "extract_arithmetic_seq_from_arguments_instr3_all"  # "whether_can_var_unpack_for_subscript_stmt_instr_explain_4_new"
    # sample_code_list = fstring_util.extract_module(samples)
    # random.seed(2023)
    # samples = random.sample(sample_code_list, 324)
    # extract_module(samples)
    # '''
    reponse_list = fstring_util.get_response_directly_refactor(user_instr, examples, sample_code_list,
                                                     sys_msg="You are a helpful assistant.")
    #
    # reponse_list = set_util.get_response_directly_refactor(user_instr, examples, samples[:],
    #                                                     sys_msg="You are a helpful assistant.")
    # # util.save_pkl(save_complicated_code_dir_root + "chain_comparison_bool_compare/",
    #               "abstract_one_compare_instr",
    #               reponse_list)
    # util.save_pkl(save_complicated_code_dir_root+ idiom + "/",
    #               "extract_comparators_one_compare_instr",
    #               reponse_list)
    file_name="direct_refactor_fstring_from_abstract_600_methods"#"direct_refactor_with_stmt_instr_sample_methods"
    util.save_pkl(save_complicated_code_dir_root + idiom + "/",
                  file_name,
                  reponse_list)
    '''
    file_name="direct_refactor_fstring_from_abstract"#"direct_refactor_with_stmt_instr_sample_methods"
    csv_res = []
    samples = util.load_pkl(save_complicated_code_dir_root + idiom + "/", file_name)
    for ind, sample in enumerate(samples):
        # for i, s in enumerate(sample):
        #     print("i,sample: ", i, s)
        repo_name, file_html, old_path, class_name, method_code, for_code, symbols_map,abstract_code_node,_, response = sample
        # print(">>>>class_name:",repo_name, old_path, file_html, "xx",class_name,"tt")
        content = response["choices"][0]["message"]["content"]
        # print("content: ",content)
        # method_code=ast.unparse(ast.parse(method_code))

        flag_ref, refactored_code = fstring_util.parse_refactor_code(content)
        if flag_ref:
            print("refactored_code: ",refactored_code)
            for key in sorted(list(symbols_map.keys()))[::-1]:
                value=symbols_map[key]
                refactored_code=util_rewrite.replace(key,value,refactored_code)
            print("new refactored_code: ",refactored_code)

            # if "for i in range(num_types):" in refactored_code:
            #     print(">>>Come here: ", content)
            csv_res.append(
                [repo_name, file_html, old_path, class_name, ast.unparse(method_code), ast.unparse(for_code), refactored_code,1])
            # print(">>>>for_code:",for_code)
            # print(">>>>response:",response)
            # print(">>>>refactored_code:",flag_ref,refactored_code)
            # break
        # else:
        #     csv_res.append([repo_name, file_html,old_path, class_name, ast.unparse(method_code),ast.unparse(for_code),refactored_code,0])

        # reponse_list.append(
        #     [*other, for_code])
        # reponse_list[-1].extend([[msg], response])
        # new_code, method_code, _, response = sample
    print("len of samples: ", len(csv_res))
    # util.save_csv(
    #     save_complicated_code_dir_root + idiom + "/" + file_name + "_new.csv",
    #     csv_res,
    #     ["repo_name", "file_path", "file_html", "class_name", "me_code", "old_code", "new_code", "bool_code",
    #      "chatGPT_code", "if_correct", "reversed_code", "non_replace_var_refactored_code", "refactored_code", "acc",
    #      "instruction", "sys_msg", "exam_msg", "user_msg"])
    file_name="gpt_fstring_res"#"direct_refactor_with_stmt_instr_sample_methods"

    util.save_pkl(save_complicated_code_dir_root + idiom + "/",
                  file_name,
                  csv_res)
    '''