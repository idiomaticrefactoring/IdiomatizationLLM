import os, sys
import struct
import traceback

code_dir = "/".join(os.path.abspath(__file__).split("/")[:-2]) + "/"
print("code path: ", code_dir)
sys.path.append(code_dir)
import chatgpt_util, random
import openai, tiktoken, ast, util, dict_util
import ast

if __name__ == '__main__':
    '''
    Variable unpacking in for statements in Python is a way to assign values to multiple variables at once from an iterable object such as a list, tuple, or dictionary. It allows you to iterate over the iterable and assign each value to a separate variable in a single line of code. 
    '''
    user_instr = '''
Extract the path through statement A from the following Python code.

Python code:
{{code}}

statement A:
{{for_code}}
'''
    user_instr = '''
Find the initialization statement of {{var}} whose format is similar to "{{var}} = {}" or "{{var}} = dict()" that arrives block A from the following Python code
Extract path that arrives block A from the following Python code.

Python code:
{{code}}
    '''
    examples = [['''
Extract path that arrives block A from the following Python code.

Python code:
def force_fp32_wrapper(old_func):

    @functools.wraps(old_func)
    def new_func(*args, **kwargs):
        if not isinstance(args[0], torch.nn.Module):
            raise TypeError('@force_fp32 can only be used to decorate the method of nn.Module')
        if not (hasattr(args[0], 'fp16_enabled') and args[0].fp16_enabled):
            return old_func(*args, **kwargs)
        args_info = getfullargspec(old_func)
        args_to_cast = args_info.args if apply_to is None else apply_to
        new_args = []
        if args_to_cast:
            arg_names = args_info.args[:len(args)]
        else:
            arg_names = args_info.args[:len(args)]
            A
    ''',
'''
path that arrives block A is as follows:
if not isinstance(args[0], torch.nn.Module):
    raise TypeError('@force_fp32 can only be used to decorate the method of nn.Module')
if not (hasattr(args[0], 'fp16_enabled') and args[0].fp16_enabled):
    return old_func(*args, **kwargs)
args_info = getfullargspec(old_func)
args_to_cast = args_info.args if apply_to is None else apply_to
new_args = []
else:
    arg_names = args_info.args[:len(args)]
    A
'''
    ]
]

    idiom = "dict_comprehension"
    save_complicated_code_dir_root = util.data_root + "chatgpt/NonIdiomatic/"
    # save_complicated_code_dir_root = util.data_root + "NonIdiomatic/find_code_snippets/"
    save_complicated_code_dir = save_complicated_code_dir_root + "sample_methods/"

    samples = util.load_pkl(save_complicated_code_dir, "sample_methods_" + idiom)

    # random.seed(2023)
    #
    # samples = random.sample(samples, 70)
    file_name = "find_for_stmt_other_info"  # "extract_arithmetic_seq_from_arguments_instr3_all"  # "whether_can_var_unpack_for_subscript_stmt_instr_explain_4_new"




    # '''
    reponse_list = dict_util.get_response_path_one_stmt(user_instr, examples, samples[:],
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
