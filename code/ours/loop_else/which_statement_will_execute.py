import os, sys
import struct
import traceback

code_dir = "/".join(os.path.abspath(__file__).split("/")[:-2]) + "/"
print("code path: ", code_dir)
sys.path.append(code_dir)
import chatgpt_util, random
import openai, tiktoken, ast, util
import ast
import for_else_util

if __name__ == '__main__':
    '''
    which_statement_will_execute_4_improve_2_all_new_fine_tune.py
    Variable unpacking in for statements in Python is a way to assign values to multiple variables at once from an iterable object such as a list, tuple, or dictionary. It allows you to iterate over the iterable and assign each value to a separate variable in a single line of code. 
    '''
    user_instr = '''Determine whether zj1 statement is executed if the break statement is executed or if the break statement is not executed.

Python code:
{{code}}

Response Format:
break statement is executed:Respond with zj1 if it is executed when the break statement is executed. Otherwise, respond with None.
break statement is not executed:Respond with with zj1 if it is is executed if the break statement is not executed. Otherwise, respond with None.
'''
    examples = [
['''Determine whether zj1 statement is executed if the break statement is executed or if the break statement is not executed.

Python code:
for var1 in var2:
    if var3:
        var4 = True
        break
if var4:
    zj1
    
Response Format:
break statement is executed:Respond with zj1 if it is executed when the break statement is executed. Otherwise, respond with None.
break statement is not executed:Respond with with zj1 if it is is executed if the break statement is not executed. Otherwise, respond with None.
'''
,
'''break statement is executed:zj1
break statement is not executed:None'''],
['''Determine whether zj1 statement is executed if the break statement is executed or if the break statement is not executed.

Python code:
for var1 in var2:
    var4 = False
    break
if var4:
    zj1

Response Format:
break statement is executed:Respond with zj1 if it is executed when the break statement is executed. Otherwise, respond with None.
break statement is not executed:Respond with with zj1 if it is is executed if the break statement is not executed. Otherwise, respond with None.
'''
,
'''break statement is executed:None
break statement is not executed:zj1
'''],
['''Determine whether zj1 statement is executed if the break statement is executed or if the break statement is not executed.

Python code:
for var1 in var2:
    var4 = False
    break
if var4:
    zj1

Response Format:
break statement is executed:Respond with zj1 if it is executed when the break statement is executed. Otherwise, respond with None.
break statement is not executed:Respond with with zj1 if it is is executed if the break statement is not executed. Otherwise, respond with None.
'''
,
'''
break statement is executed:None
break statement is not executed:zj1
'''],
['''Determine whether zj1 statement is executed if the break statement is executed or if the break statement is not executed.

Python code:
for var1 in var2:
    var5
    var6 = True
    break
if not var6:
    zj1

Response Format:
break statement is executed:Respond with zj1 if it is executed when the break statement is executed. Otherwise, respond with None.
break statement is not executed:Respond with with zj1 if it is is executed if the break statement is not executed. Otherwise, respond with None.
'''
,
'''break statement is executed:None
break statement is not executed:zj1
'''],
['''Determine whether zj1 statement is executed if the break statement is executed or if the break statement is not executed.

Python code:
for var1 in var2:
    if var3:
        break
if not var3:
    zj1

Response Format:
break statement is executed:Respond with zj1 if it is executed when the break statement is executed. Otherwise, respond with None.
break statement is not executed:Respond with with zj1 if it is is executed if the break statement is not executed. Otherwise, respond with None.
'''
,
'''break statement is executed:None
break statement is not executed:zj1
''']

]
#     ['''Determine which statement called zj will be executed if the break statement is executed and which statement called zj will be executed if the break statement is not executed.
#
# Python code:
# for var1 in var2:
#     var3 = True
#     break
# if var3 == False:
#     zj1
#
# Response Format:
# break statement is executed:Respond which statement called zj after the break statement is executed. You respond None if there is no statement called zj that will be executed after the break statement is executed
# break statement is not executed:Respond which statement called zj after the break statement is not executed. You respond None if there is no statement called zj that will be executed after the break statement is not executed
# '''
# ,
# '''
# break statement is executed:None
# break statement is not executed:zj1
# '''],
# ['''Determine which statement called zj will be executed if the break statement is executed and which statement called zj will be executed if the break statement is not executed.
#
# Python code:
# for var1 in var2:
#     if var5:
#         break
# if var5 == False:
#     zj1
# else:
#     zj2
#
# Response Format:
# break statement is executed:Respond which statement called zj after the break statement is executed. You respond None if there is no statement called zj that will be executed after the break statement is executed
# break statement is not executed:Respond which statement called zj after the break statement is not executed. You respond None if there is no statement called zj that will be executed after the break statement is not executed
# '''
# ,
# '''break statement is executed:zj2
# break statement is not executed:zj1'''],
    idiom = "loop_else"
    save_complicated_code_dir_root = util.data_root + "chatgpt/NonIdiomatic/"
    # save_complicated_code_dir_root = util.data_root + "NonIdiomatic/find_code_snippets/"
    save_complicated_code_dir = save_complicated_code_dir_root + "sample_methods/"

    samples = util.load_pkl(save_complicated_code_dir, "sample_methods_" + idiom)

    # random.seed(2023)
    #
    # samples = random.sample(samples, 50)

    # file_name = "abstract_total_code_split_if_for_abstract"
    file_name = "abstract_total_code_split_if_for_abstract_3_2"  # "extract_arithmetic_seq_from_arguments_instr3_all"  # "whether_can_var_unpack_for_subscript_stmt_instr_explain_4_new"
    file_name = "abstract_total_code_split_if_for_abstract_2_improve_50"
    file_name = "abstract_total_code_split_if_for_abstract_2_improve_all"
    file_name = "abstract_total_code_split_if_for_abstract_2_improve_new_all"
    file_name = "abstract_total_code_split_if_for_abstract_2_improve_new_all_fine_tune"  # "extract_arithmetic_seq_from_arguments_instr3_all"  # "whether_can_var_unpack_for_subscript_stmt_instr_explain_4_new"

    samples = util.load_pkl(save_complicated_code_dir_root + idiom + "/", file_name)

    # file_name = "abstract_ass_values_instr2_all"#"abstract_ass_values_instr2"#"direct_refactor_from_blocks_no_dependinstr"  # "extract_arithmetic_seq_from_arguments_instr3_all"  # "whether_can_var_unpack_for_subscript_stmt_instr_explain_4_new"
    # file_name = "abstract_ass_values_instr2"#"direct_refactor_from_blocks_no_dependinstr"  # "extract_arithmetic_seq_from_arguments_instr3_all"  # "whether_can_var_unpack_for_subscript_stmt_instr_explain_4_new"
    #
    # # file_name = "extract_arithmetic_seq_from_abstract_same_subscript_value_arguments_instr7_all_2_sample"  # "extract_arithmetic_seq_from_arguments_instr3_all"  # "whether_can_var_unpack_for_subscript_stmt_instr_explain_4_new"
    # samples = util.load_pkl(save_complicated_code_dir_root + idiom + "/", file_name)
    # print("len of samples: ",len(samples))
    # '''
    reponse_list = for_else_util.get_response_which_block_execute(user_instr, examples, samples[:],
                                                                                      sys_msg="You are a helpful assistant.")
    # util.save_pkl(save_complicated_code_dir_root + "chain_comparison_bool_compare/",
    #               "abstract_one_compare_instr",
    #               reponse_list)
    # util.save_pkl(save_complicated_code_dir_root+ idiom + "/",
    #               "extract_comparators_one_compare_instr",
    #               reponse_list)
    # file_name = "direct_refactor_from_blocks_no_dependinstr_all"  # "extract_arithmetic_seq_from_arguments_instr3_all"  # "whether_can_var_unpack_for_subscript_stmt_instr_explain_4_new"
    file_name = "which_statement_will_execute_2"  # "extract_arithmetic_seq_from_arguments_instr3_all"  # "whether_can_var_unpack_for_subscript_stmt_instr_explain_4_new"
    file_name = "which_statement_will_execute_4_all"  # "extract_arithmetic_seq_from_arguments_instr3_all"  # "whether_can_var_unpack_for_subscript_stmt_instr_explain_4_new"
    file_name = "which_statement_will_execute_4_improve_all_new"  # "extract_arithmetic_seq_from_arguments_instr3_all"  # "whether_can_var_unpack_for_subscript_stmt_instr_explain_4_new"
    file_name = "which_statement_will_execute_4_improve_2_all_new_fine_tune"  # "extract_arithmetic_seq_from_arguments_instr3_all"  # "whether_can_var_unpack_for_subscript_stmt_instr_explain_4_new"

    util.save_pkl(save_complicated_code_dir_root + idiom + "/",
                  file_name,
                  reponse_list)

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
