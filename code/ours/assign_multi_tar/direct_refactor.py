import os, sys
import struct
import traceback

code_dir = "/".join(os.path.abspath(__file__).split("/")[:-2]) + "/"
print("code path: ", code_dir)
sys.path.append(code_dir)
import chatgpt_util, random
import openai, tiktoken, ast, util
import ast
import ass_util
#direct_refactor_from_blocks_no_dependinstr_improve_depdend_4_4_examp.py
if __name__ == '__main__':
    '''
    Variable unpacking in for statements in Python is a way to assign values to multiple variables at once from an iterable object such as a list, tuple, or dictionary. It allows you to iterate over the iterable and assign each value to a separate variable in a single line of code. 
    '''
    user_instr = '''
Refactor the following Python code consisting of multiple assignment statements with one assign statement to assign multiple variables.

Python code:
{{code}}

response format:
Answer: You respond with Yes or No for whether the code can be refactored with one assign statement.
New Python Code: If your answer is Yes, you give the refactored code. Otherwise, you respond with None.
'''
    examples = [
['''
Refactor the following Python code consisting of multiple assignment statements with one assign statement to assign multiple variables.

Python code:
event_type = zj1
event_data = zj2
event_module = zj3
source_event = zj4

response format:
Answer: You respond with Yes or No for whether the code can be refactored with one assign statement.
New Python Code: If your answer is Yes, you give the refactored code. Otherwise, you respond with None.
''',
'''
Answer: Yes
New Python Code: event_type, event_data, event_module, source_event = zj1, zj2, zj3, zj4
'''],
['''
Refactor the following Python code consisting of multiple assignment statements with one assign statement to assign multiple variables.

Python code:
ret['result'] = zj1
ret['comment'] = zj2

response format:
Answer: You respond with Yes or No for whether the code can be refactored with one assign statement.
New Python Code: If your answer is Yes, you give the refactored code. Otherwise, you respond with None.
''',
'''
Answer: Yes
New Python Code: ret['result'], ret['comment']= zj1, zj2
'''],
['''
Refactor the following Python code consisting of multiple assignment statements with one assign statement to assign multiple variables.

Python code:
weight_attribute.input_type = zj1
weight_attribute.value_required = zj2

response format:
Answer: You respond with Yes or No for whether the code can be refactored with one assign statement.
New Python Code: If your answer is Yes, you give the refactored code. Otherwise, you respond with None.
''',
'''
Answer: Yes
New Python Code: weight_attribute.input_type, weight_attribute.value_required= zj1, zj2
'''],
['''
Refactor the following Python code consisting of multiple assignment statements with one assign statement to assign multiple variables.

Python code:
contents = zj1
lines = zj2

response format:
Answer: You respond with Yes or No for whether the code can be refactored with one assign statement.
New Python Code: If your answer is Yes, you give the refactored code. Otherwise, you respond with None.
''',
'''
Answer: Yes
New Python Code: contents, lines= zj1, zj2
''']
]
#     ,
# ['''
# Refactor the following Python consisting of multiple assignments with one assign statement to assign multiple variables.
#
# Python code:
# cache0 = self.caches[0]
# cache1 = self.caches[1]
#
# response format:
# Answer: You respond with Yes or No for whether the code can be refactored with list comprehension.
# New Python Code: If your answer is Yes, you give the refactored code. Otherwise, you respond with None. Please explain it.
# ''',
# '''
# Answer: Yes
# New Python Code:
# cache0 , cache1  = self.caches[0], self.caches[1]
# ''']
    idiom = "assign_multiple_targets"
    save_complicated_code_dir_root = util.data_root + "chatgpt/NonIdiomatic/"
    # save_complicated_code_dir_root = util.data_root + "NonIdiomatic/find_code_snippets/"
    save_complicated_code_dir = save_complicated_code_dir_root + "sample_methods/"

    samples = util.load_pkl(save_complicated_code_dir, "sample_methods_" + idiom)

    # random.seed(2023)

    # samples = random.sample(samples, 30)
    file_name = "abstract_ass_values_instr2_all"#"abstract_ass_values_instr2"#"direct_refactor_from_blocks_no_dependinstr"  # "extract_arithmetic_seq_from_arguments_instr3_all"  # "whether_can_var_unpack_for_subscript_stmt_instr_explain_4_new"
    file_name = "abstract_ass_values_instr2_improve_depend"#"direct_refactor_from_blocks_no_dependinstr"  # "extract_arithmetic_seq_from_arguments_instr3_all"  # "whether_can_var_unpack_for_subscript_stmt_instr_explain_4_new"
    file_name = "abstract_ass_values_instr3_improve_depend_all"#"abstract_ass_values_instr3_improve_depend"
    file_name = "abstract_ass_values_instr4_improve_depend"
    file_name = "abstract_ass_values_instr4_improve_depend_all"
    # file_name = "extract_arithmetic_seq_from_abstract_same_subscript_value_arguments_instr7_all_2_sample"  # "extract_arithmetic_seq_from_arguments_instr3_all"  # "whether_can_var_unpack_for_subscript_stmt_instr_explain_4_new"
    samples = util.load_pkl(save_complicated_code_dir_root + idiom + "/", file_name)
    print("len of samples: ",len(samples))
    # '''
    reponse_list = ass_util.get_response_instr_from_abstract_blocks_2(user_instr, examples, samples[:],
                                                        sys_msg="You are a helpful assistant.")
    # util.save_pkl(save_complicated_code_dir_root + "chain_comparison_bool_compare/",
    #               "abstract_one_compare_instr",
    #               reponse_list)
    # util.save_pkl(save_complicated_code_dir_root+ idiom + "/",
    #               "extract_comparators_one_compare_instr",
    #               reponse_list)
    # file_name = "direct_refactor_from_blocks_no_dependinstr_all"  # "extract_arithmetic_seq_from_arguments_instr3_all"  # "whether_can_var_unpack_for_subscript_stmt_instr_explain_4_new"
    file_name = "direct_refactor_from_blocks_no_dependinstr_improve_depdend_4_4_examp"  # "extract_arithmetic_seq_from_arguments_instr3_all"  # "whether_can_var_unpack_for_subscript_stmt_instr_explain_4_new"
    file_name = "direct_refactor_from_blocks_no_dependinstr_improve_depdend_4_4_examp_all"  # "extract_arithmetic_seq_from_arguments_instr3_all"  # "whether_can_var_unpack_for_subscript_stmt_instr_explain_4_new"

    # util.save_pkl(save_complicated_code_dir_root + idiom + "/",
    #               file_name,
    #               reponse_list)
    # '''
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
