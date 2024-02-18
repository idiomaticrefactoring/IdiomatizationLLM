import os, sys
import struct
import traceback

import util_rewrite

code_dir = "/".join(os.path.abspath(__file__).split("/")[:-2]) + "/"
print("code path: ", code_dir)
sys.path.append(code_dir)
import chatgpt_util, random
import openai, tiktoken, ast, util,util_rewrite
import ast,code_extract_for_determine_has_add_func
from  set_comprehension import set_util

if __name__ == '__main__':
    '''
    direct_refactor_set_comprehension_instr_add_one_example_instr3_2_real_examp_from_def_stmt_abstract_var_all_add_example_filter_for_from_code_gen.py
    Variable unpacking in for statements in Python is a way to assign values to multiple variables at once from an iterable object such as a list, tuple, or dictionary. It allows you to iterate over the iterable and assign each value to a separate variable in a single line of code. 
    '''
    user_instr = '''
Refactor the following Python code with set comprehension in Python as much as possible. Do not refactor other part of code.

Python code:
{{code}}

response format:
Answer: You respond with Yes or No for whether the code can be refactored with set comprehension.
Information: If your answer is Yes, you give the refactored code. Otherwise, you respond with None. Please explain it.
'''
    examples = [
['''
Refactor the following Python code with set comprehension in Python as much as possible. Do not refactor other part of code.

Python code:
for word in words:
    zj.add(word)
        
response format:
Answer: You respond with Yes or No for whether the code can be refactored with set comprehension.
Information: If your answer is Yes, you give the refactored code. Otherwise, you respond with None. Please explain it.
''',
'''
Answer: Yes
Information:
zj = {word for word in words}
'''],
['''
Refactor the following Python code with set comprehension in Python as much as possible. Do not refactor other part of code.

Python code:
for (num, (entry_title, media_kind, download_text)) in enumerate(re.findall('(?s)<p[^>]+class="infotext"[^>]*>\\s*(?:<a[^>]+>)?\\s*<strong>(.+?)</strong>.*?</p>.*?%s' % DOWNLOAD_REGEX, webpage), 1):
    zj.add({'id': '%s-%d' % (display_id, num), 'title': '%s' % entry_title, 'formats': self._extract_formats(download_text, media_kind)})

response format:
Answer: You respond with Yes or No for whether the code can be refactored with set comprehension.
Information: If your answer is Yes, you give the refactored code. Otherwise, you respond with None. Please explain it.
''',
'''
Answer: Yes
Information:
zj = {{'id': '%s-%d' % (display_id, num), 'title': '%s' % entry_title, 'formats': self._extract_formats(download_text, media_kind)} for (num, (entry_title, media_kind, download_text)) in enumerate(re.findall('(?s)<p[^>]+class="infotext"[^>]*>\\s*(?:<a[^>]+>)?\\s*<strong>(.+?)</strong>.*?</p>.*?%s' % DOWNLOAD_REGEX, webpage), 1)}
'''],
['''
Refactor the following Python code with set comprehension in Python as much as possible. Do not refactor other part of code.

Python code:
for line in f:
    if line.startswith('include '):
        for include in line.split()[1:]:
            zj.add(include)
        
response format:
Answer: You respond with Yes or No for whether the code can be refactored with set comprehension.
Information: If your answer is Yes, you give the refactored code. Otherwise, you respond with None. Please explain it.
''',
'''
Answer: Yes
Information:
zj = {include for line in f if line.startswith('include ') for include in line.split()[1:]}
'''],
['''
Refactor the following Python code with set comprehension in Python as much as possible. Do not refactor other part of code.

Python code:
for (index, (first, second)) in enumerate(zip(x_shape[0:-2], self.dx.shape[0:-2])):
    if first != second:
        zj.add(index)
    else:
        zj.add(index+1)
        
response format:
Answer: You respond with Yes or No for whether the code can be refactored with set comprehension.
Information: If your answer is Yes, you give the refactored code. Otherwise, you respond with None. Please explain it.
''',
'''
Answer: Yes
Information:
zj = {index if first != second else index+1 for (index, (first, second)) in enumerate(zip(x_shape[0:-2], self.dx.shape[0:-2])) if first != second}
''']

]

    idiom = "set_comprehension"
    save_complicated_code_dir_root = util.data_root + "chatgpt/NonIdiomatic/"
    # save_complicated_code_dir_root = util.data_root + "NonIdiomatic/find_code_snippets/"
    save_complicated_code_dir = save_complicated_code_dir_root + "sample_methods/"

    samples = util.load_pkl(save_complicated_code_dir, "sample_methods_" + idiom)

    random.seed(2023)

    samples = random.sample(samples, 70)
    file_name = "direct_refactor_set_comprehension_instr_add_one_example_instr3_2_real_examp"  # "extract_arithmetic_seq_from_arguments_instr3_all"  # "whether_can_var_unpack_for_subscript_stmt_instr_explain_4_new"
    file_name = "find_def_stmt_for_a_node"  # "extract_arithmetic_seq_from_arguments_instr3_all"  # "whether_can_var_unpack_for_subscript_stmt_instr_explain_4_new"
    file_name ="find_def_stmt_for_a_node_all"
    file_name ="find_def_stmt_for_a_node_all_filter_for"
    file_name = "find_def_stmt_for_a_node_all_filter_for"  # "extract_arithmetic_seq_from_arguments_instr3_all"  # "whether_can_var_unpack_for_subscript_stmt_instr_explain_4_new"
    file_name = "find_def_stmt_for_a_node_all_filter_for_from_code"  # "extract_arithmetic_seq_from_arguments_instr3_all"  # "whether_can_var_unpack_for_subscript_stmt_instr_explain_4_new"

    samples = util.load_pkl(save_complicated_code_dir_root + idiom + "/",file_name)
    print("len of samples: ",len(samples))

    # file_name = "extract_arithmetic_seq_from_abstract_same_subscript_value_arguments_instr7_all_2_sample"  # "extract_arithmetic_seq_from_arguments_instr3_all"  # "whether_can_var_unpack_for_subscript_stmt_instr_explain_4_new"


    reponse_list = set_util.get_response_directly_refactor_from_def_stmt_abstract_obj_filter_for_from_code(user_instr, examples, samples,
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
    file_name="direct_refactor_set_comprehension_from_def_stmt_code_gen"
    # util.save_pkl(save_complicated_code_dir_root + idiom + "/",
    #               file_name,
    #               reponse_list)
    '''

    file_name="direct_refactor_set_comprehension_from_def_stmt_code_gen"

    reponse_list=[]

    samples = util.load_pkl(save_complicated_code_dir_root + idiom + "/",file_name)
    print("len of samples: ",len(samples))
    w=0
    except_error = 0

    for ind,sample in enumerate(samples):
        if ind==0:
            for ind_e,e in enumerate(sample):
                print("ind_e,e: ",ind_e,e)
       # abstract_me_code,me_code, old_code, ass_flag, ass_stmt,flag_use, object_var, *other])

        abstract_me_code,me_code,old_code,ass_stmt,flag_use, object_var, repo_name,old_path, file_html, class_name,me_name,new_code,method_code,_,response=sample

        if not object_var:
            w+=1
            continue

        # print("old_path: ",old_path)
        # repo_name=old_path.split("/")[8].strip()
        # print("repo_name: ",repo_name)
        #
        # break
        content = response["choices"][0]["message"]["content"]
        flag_can_refactor, refactor_code=set_util.parse_refactor_code(content)
        try:
            if flag_can_refactor:
                refactor_code = util_rewrite.replace("zj", object_var, refactor_code)
                if flag_use:
                    refactor_code=util_rewrite.replace_first_occur(object_var+" ",object_var+" |",refactor_code)
                # print("refactor_code: ", refactor_code, me_code)
                e = [repo_name, old_path, file_html, class_name, me_name, method_code, me_code, ast.unparse(ast.parse(refactor_code)),ass_stmt,content]

                reponse_list.append(e)
            else:
                print("Content: ",content,abstract_me_code)
        except:
            except_error+=1

    util.save_pkl(save_complicated_code_dir_root + idiom + "/",
                  "gpt_result_from_def_stmt_from_abstract_var_all_add_examp_new_filter_for_from_code_gen",
                  reponse_list)
    print("no obj var: ",w,except_error)
    print("len of reponse_list: ",len(reponse_list))
    '''
    # '''
    # '''
    # samples = util.load_pkl(save_complicated_code_dir_root + idiom + "/", file_name)
    #
    # csv_res_list=call_star_util.save_csv(samples, [None for e in samples])
    # util.save_csv(
    #     save_complicated_code_dir_root + idiom + "/" + file_name+".csv",
    #     csv_res_list,
    #     ["repo_name", "file_path", "file_html", "class_name", "me_name", "me_code", "old_code", "new_code", "bool_code",
    #      "chatGPT_code", "if_correct", "reversed_code", "non_replace_var_refactored_code", "refactored_code", "acc",
    #      "instruction", "sys_msg", "exam_msg", "user_msg"])
    # '''
