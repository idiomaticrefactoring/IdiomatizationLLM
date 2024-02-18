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
#abstract_total_code_modify_example_split_if_for_abstract_2_improve_new_fine_tune.py
if __name__ == '__main__':
    '''
    Variable unpacking in for statements in Python is a way to assign values to multiple variables at once from an iterable object such as a list, tuple, or dictionary. It allows you to iterate over the iterable and assign each value to a separate variable in a single line of code. 
    '''
    user_instr = '''For the following Python code, you use only one symbol var to represent the expression of the following Python code. Please do not change other code.

Python code:
{{code}}'''
    examples = [
['''For the following Python code, you use only one symbol var to represent the expression of the following Python code. Please do not change other code.

Python code:
for e in e_list:
    if xml:
        break
if xml is None:
    zj1
'''
,
'''symbols:
var1:e
var2:e_list
var3:xml

New Python code:
for var1 in var2:
    if var3:
        break
if var3 is None:
    zj1'''],
['''For the following Python code, you use only one symbol var to represent the expression of the following Python code. Please do not change other code.

Python code:
for e in e_list:
    found = True
    break
if not found:
    zj1
''',
'''symbols:
var1:e
var2:e_list
var3:found

New Python code:
for var1 in var2:
    var3=True
    break
if not var5:
    zj1'''],
['''
For the following Python code, you use only one symbol var to represent the expression of the following Python code. Please do not change other code.

Python code:
for e in e_list:
    is_det = True
    break
if is_det == False:
    zj1
'''
,
'''symbols:
var1:e
var2:e_list
var3:is_det

New Python code:
for var1 in var2:
    var3 = True
    break
if var3 == False:
    zj1''']

]
    '''
    >>>>>>>>>>Instr:  For the following Python code, you use only one symbol var to represent the expression of the following Python code. Please do not change other code.

Python code:
for e in e_list:
    try:
        config_file = open(path)
    except IOError as e:
        if e.errno == errno.ENOENT:
            continue
        else:
            raise
    else:
        file_loaded = True
        break
if not file_loaded:
    zj1
>>>>>>>>>>each response:
 symbols:
var1:e
var2:e_list
var3:config_file = open(path)
var4:if e.errno == errno.ENOENT:
            continue
        else:
            raise
var5:file_loaded

New Python code:
for var1 in var2:
    try:
        var3
    except IOError as var1:
        var4
    else:
        var5 = True
        break
if not var5:
    zj1
    >>>>>>>>>>real_instruction:  For the following Python code, you use only one symbol var to represent the expression of the following Python code. Please do not change other code.

Python code:
for e in e_list:
    if os.path.exists(path):
        poster = path
        self.log.info('Local artwork detected, using %s.' % path)
        break
if poster:
    zj1
>>>>>>>>>>each response:
 symbols:
var1:e
var2:e_list
var3:os.path.exists(path)
var4:poster = path
        self.log.info('Local artwork detected, using %s.' % path)
var5:poster

New Python code:
for var1 in var2:
    if var3:
        var4
        var5 = path
        break
if var5:
    zj1
>>>>>>>>>>Instr:  For the following Python code, you use only one symbol var to represent the expression of the following Python code. Please do not change other code.

Python code:
for e in e_list:
    if modif.short_name.startswith(sub):
        triple = [modif.short_name.lstrip(sub), modif.short_name, modif.name]
        tiny[sub].append(triple)
        done = True
        break
if done:
    zj1
else:
    zj2
>>>>>>>>>>each response:
 symbols:
var1:e
var2:e_list
var3:modif.short_name.startswith(sub)
var4:triple = [modif.short_name.lstrip(sub), modif.short_name, modif.name]
        tiny[sub].append(triple)
var5:done
var6:done = False
var7:for fo in exclude_in_others:
        if modif.short_name.startswith(fo) or modif.short_name.startswith('ID'):
            false_others = True
    if false_others:
        false_others = False
    else:
        tiny['other'].append([modif.short_name, modif.short_name, modif.name])

New Python code:
for var1 in var2:
    if var3:
        var4
        var5 = True
        break
if var5:
    var5 = False
else:
    for fo in exclude_in_others:
        if var1.startswith(fo) or var1.startswith('ID'):
            var6 = True
    if var6:
        var6 = False
    else:
        tiny['other'].append([var1, var1, modif.name])
    for e in e_list:
    if existing_iface['ip_address'] == new_iface['ip']:
        exists = True
        break
    if 'ip' in new_iface:
        if existing_iface['ip_address'] == new_iface['ip']:
            exists = True
            break
    else:
        exists = True
        break
if not exists:
    zj1
    '''
    '''
    for e in e_list:
    if os.path.exists(path):
        poster = path
        self.log.info('Local artwork detected, using %s.' % path)
        break
if not poster:
    zj1

symbols:
var1:e
var2:e_list
var3:poster
var4:os.path.exists(path)
var5:poster = path
        self.log.info('Local artwork detected, using %s.' % path)

New Python code:
for var1 in var2:
    if var3:
        break
    if var4:
        var5
        break
if not var3:
    zj1
    '''
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
    idiom = "loop_else"
    save_complicated_code_dir_root = util.data_root + "chatgpt/NonIdiomatic/"
    # save_complicated_code_dir_root = util.data_root + "NonIdiomatic/find_code_snippets/"
    save_complicated_code_dir = save_complicated_code_dir_root + "sample_methods/"

    samples = util.load_pkl(save_complicated_code_dir, "sample_methods_" + idiom)

    # random.seed(2023)
    #
    # samples = random.sample(samples, 50)
    # file_name = "abstract_code_loop_else_total_code"
    # file_name = "abstract_code_loop_else_if_code"  # "extract_arithmetic_seq_from_arguments_instr3_all"  # "whether_can_var_unpack_for_subscript_stmt_instr_explain_4_new"
    # file_name = "abstract_code_loop_else_if_code_abstract_code_instr3"
    # samples = util.load_pkl(save_complicated_code_dir_root + idiom + "/", file_name)
    # print("len of samples: ",len(samples))
    # for e in samples:
    #     print(e)
    # file_name = "abstract_code_loop_else_total_code"
    # samples = util.load_pkl(save_complicated_code_dir_root + idiom + "/", file_name)

    # file_name = "abstract_ass_values_instr2_all"#"abstract_ass_values_instr2"#"direct_refactor_from_blocks_no_dependinstr"  # "extract_arithmetic_seq_from_arguments_instr3_all"  # "whether_can_var_unpack_for_subscript_stmt_instr_explain_4_new"
    # file_name = "abstract_ass_values_instr2"#"direct_refactor_from_blocks_no_dependinstr"  # "extract_arithmetic_seq_from_arguments_instr3_all"  # "whether_can_var_unpack_for_subscript_stmt_instr_explain_4_new"
    #
    # # file_name = "extract_arithmetic_seq_from_abstract_same_subscript_value_arguments_instr7_all_2_sample"  # "extract_arithmetic_seq_from_arguments_instr3_all"  # "whether_can_var_unpack_for_subscript_stmt_instr_explain_4_new"
    # samples = util.load_pkl(save_complicated_code_dir_root + idiom + "/", file_name)
    # print("len of samples: ",len(samples))
    # '''

    reponse_list = for_else_util.get_response_abstract_for_block_execute_improve(user_instr, examples, samples[:],
                                                                                    sys_msg="You are a helpful assistant.")
    # util.save_pkl(save_complicated_code_dir_root + "chain_comparison_bool_compare/",
    #               "abstract_one_compare_instr",
    #               reponse_list)
    # util.save_pkl(save_complicated_code_dir_root+ idiom + "/",
    #               "extract_comparators_one_compare_instr",
    #               reponse_list)
    # file_name = "direct_refactor_from_blocks_no_dependinstr_all"  # "extract_arithmetic_seq_from_arguments_instr3_all"  # "whether_can_var_unpack_for_subscript_stmt_instr_explain_4_new"
    file_name = "abstract_total_code_split_if_for_abstract"  # "extract_arithmetic_seq_from_arguments_instr3_all"  # "whether_can_var_unpack_for_subscript_stmt_instr_explain_4_new"
    file_name = "abstract_total_code_split_if_for_abstract_2_improve_new_all_fine_tune"  # "extract_arithmetic_seq_from_arguments_instr3_all"  # "whether_can_var_unpack_for_subscript_stmt_instr_explain_4_new"

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
