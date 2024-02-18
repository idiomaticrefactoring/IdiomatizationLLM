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
#abstract_ass_values_instr4_improve_depend_all.py
if __name__ == '__main__':
    '''
    Variable unpacking in for statements in Python is a way to assign values to multiple variables at once from an iterable object such as a list, tuple, or dictionary. It allows you to iterate over the iterable and assign each value to a separate variable in a single line of code. 
    '''
    user_instr = '''
For the following Python code, you use only one symbol zj to represent values of assignment statements. Please do not change other code.

Python code:
{{code}}
'''
    examples = [
['''
For the following Python code, you use only one symbol zj to represent values of assignment statements. Please do not change other code.

Python code:
count = stages[stage_num - 2]
ch_out = self.stage_filters[stage_num - 2]
is_first = False if stage_num != 2 else True
dcn_v2 = True if stage_num in self.dcn_v2_stages else False
num_filters1 = self.num_filters1[stage_num - 2]
num_filters2 = self.num_filters2[stage_num - 2]
nonlocal_mod = 1000
''',
'''
symbols:
zj1: stages[stage_num - 2]
zj2: self.stage_filters[stage_num - 2]
zj3: False if stage_num != 2 else True
zj4: True if stage_num in self.dcn_v2_stages else False
zj5: self.num_filters1[stage_num - 2]
zj6: self.num_filters2[stage_num - 2]
zj7: 1000

New Python Code: 
count = zj1
ch_out = zj2
is_first = zj3
dcn_v2 = zj4
num_filters1 = zj5
num_filters2 = zj6
nonlocal_mod = zj7
'''],
['''
For the following Python code, you use only one symbol zj to represent values of assignment statements. Please do not change other code.

Python code:
predictions[t] = best_guess.item()
x = torch.tensor([best_guess.item()], dtype=torch.float).to(device)
''',
'''
symbols:
zj1: best_guess.item()
zj2: torch.tensor([best_guess.item()], dtype=torch.float).to(device)

New Python Code: 
predictions[t] = zj1
x = zj2
''']
]
    # ,
    # ['''
    # For the following Python code, you use only one symbol v to represent assigned variables of assignment statements. And then replace the variable with the corresponding symbol of the Python code. Please do not change other code.
    #
    # Python code:
    # a_data = np.array([1 + 2j, 3 + 4j, 5 + 6j])
    # a = tensor(a_data, chunk_size=2)
    # res = a.imag.execute().fetch()
    # expected = a_data.imag
    # ''',
    #  '''
    #  symbols:
    #  v1: a_data
    #  v2: a
    #  v3: res
    #  v4: expected
    #
    #  New Python code:
    #  v1 = np.array([1 + 2j, 3 + 4j, 5 + 6j])
    #  v2 = tensor(v3, chunk_size=2)
    #  v3 = v2.imag.execute().fetch()
    #  v4 = v1.imag
    #  '''],
    # ['''
    # For the following Python code, you use only one symbol v to represent assigned variables of assignment statements. And then replace the variable with the corresponding symbol of the Python code. Please do not change other code.
    #
    # Python code:
    # a.imag = 9
    # res = a.execute().fetch()
    # expected = a_data.copy()
    # expected.imag = 9
    # ''',
    #  '''
    #  symbols:
    #  v1: a
    #  v2: res
    #  v3: expected
    #
    #  New Python code:
    #  v1.imag = 9
    #  v2 = v1.execute().fetch()
    #  v3 = a_data.copy()
    #  v3.imag = 9
    #  ''']
    idiom = "assign_multiple_targets"
    save_complicated_code_dir_root = util.data_root + "chatgpt/NonIdiomatic/"
    # save_complicated_code_dir_root = util.data_root + "NonIdiomatic/find_code_snippets/"
    save_complicated_code_dir = save_complicated_code_dir_root + "sample_methods/"

    samples = util.load_pkl(save_complicated_code_dir, "sample_methods_" + idiom)

    # random.seed(2023)
    #
    # samples = random.sample(samples, 30)
    file_name = "abstract_ass_values_instr4_improve_depend_all"  # "extract_arithmetic_seq_from_arguments_instr3_all"  # "whether_can_var_unpack_for_subscript_stmt_instr_explain_4_new"
    # file_name = "extract_arithmetic_seq_from_abstract_same_subscript_value_arguments_instr7_all_2_sample"  # "extract_arithmetic_seq_from_arguments_instr3_all"  # "whether_can_var_unpack_for_subscript_stmt_instr_explain_4_new"

    # '''
    reponse_list = ass_util.get_response_instr_from_blocks_3(user_instr, examples, samples[:],
                                                        sys_msg="You are a helpful assistant.")
    # util.save_pkl(save_complicated_code_dir_root + "chain_comparison_bool_compare/",
    #               "abstract_one_compare_instr",
    #               reponse_list)
    # util.save_pkl(save_complicated_code_dir_root+ idiom + "/",
    #               "extract_comparators_one_compare_instr",
    #               reponse_list)

    util.save_pkl(save_complicated_code_dir_root + idiom + "/",
                  file_name,
                  reponse_list)
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
