import os, sys
import struct
import traceback

code_dir = "/".join(os.path.abspath(__file__).split("/")[:-2]) + "/"
print("code path: ", code_dir)
sys.path.append(code_dir)
import chatgpt_util, random
import openai, tiktoken, ast, util
import ast
import call_star_util
#extract_arithmetic_seq_from_abstract_same_subscript_value_arguments_instr7_all_all.py
if __name__ == '__main__':
    '''
    Variable unpacking in for statements in Python is a way to assign values to multiple variables at once from an iterable object such as a list, tuple, or dictionary. It allows you to iterate over the iterable and assign each value to a separate variable in a single line of code. 
    '''
    user_instr = '''
Extract consecutive subscript elements whose format is "{{value}}[]" from the following element sequence, and their subscript sequence is an arithmetic sequence.

element sequence:
{{code}}

response format:
Answer: You respond with Yes or No for whether there are consecutive subscript elements whose format is "{{value}}[]" and their subscript sequence sequence is an arithmetic sequence.
Information: If your answer is Yes, you give all sequences that meets the condition, and each sequence is directly from the element sequence. Otherwise, you respond with None. Please explain it.
'''
    examples = [
['''
Extract consecutive subscript elements whose format is "a[]" from the following element sequence, and their subscript sequence is an arithmetic sequence.

element sequence:
a[0], a[1]

response format:
Answer: You respond with Yes or No for whether there are consecutive subscript elements whose format is "a[]" and their subscript sequence sequence is an arithmetic sequence.
Information: If your answer is Yes, you give all sequences that meets the condition, and each sequence is directly from the element sequence. Otherwise, you respond with None. Please explain it.
''',
 '''
 Answer: Yes
 Information:
 sequence 1: a[0], a[1]
 '''],
['''
Extract consecutive subscript elements whose format is "a[]" from the following element sequence, and their subscript sequence is an arithmetic sequence.

element sequence:
a[0], a[2]

response format:
Answer: You respond with Yes or No for whether there are consecutive subscript elements whose format is "a[]" and their subscript sequence sequence is an arithmetic sequence.
Information: If your answer is Yes, you give all sequences that meets the condition, and each sequence is directly from the element sequence. Otherwise, you respond with None. Please explain it.
''',
'''
Answer: Yes
Information:
sequence 1: a[0], a[2]
'''],
['''
Extract consecutive subscript elements whose format is "a[]" from the following element sequence, and their subscript sequence is an arithmetic sequence.

element sequence:
a[0], a[1], a[2], a[3]

response format:
Answer: You respond with Yes or No for whether there are consecutive subscript elements whose format is "a[]" and their subscript sequence sequence is an arithmetic sequence.
Information: If your answer is Yes, you give all sequences that meets the condition, and each sequence is directly from the element sequence. Otherwise, you respond with None. Please explain it.
''',
'''
Answer: Yes
Information:
sequence 1: a[0], a[1], a[2], a[3]
'''],
['''
Extract consecutive subscript elements whose format is "a[]" from the following element sequence, and their subscript sequence is an arithmetic sequence.

element sequence:
a[2], a[3]

response format:
Answer: You respond with Yes or No for whether there are consecutive subscript elements whose format is "a[]" and their subscript sequence sequence is an arithmetic sequence.
Information: If your answer is Yes, you give all sequences that meets the condition, and each sequence is directly from the element sequence. Otherwise, you respond with None. Please explain it.
''',
'''
Answer: Yes
Information:
sequence 1: a[2], a[3]
'''],
['''
Extract consecutive subscript elements whose format is "a[]" from the following element sequence, and their subscript sequence is an arithmetic sequence.

element sequence:
a[0], a[1], a[0]

response format:
Answer: You respond with Yes or No for whether there are consecutive subscript elements whose format is "a[]" and their subscript sequence sequence is an arithmetic sequence.
Information: If your answer is Yes, you give all sequences that meets the condition, and each sequence is directly from the element sequence. Otherwise, you respond with None. Please explain it.
''',
'''
Answer: Yes
Information:
sequence 1: a[0], a[1]
sequence 2: a[1], a[0]
'''],
['''
Extract consecutive subscript elements whose format is "a[]" from the following element sequence, and their subscript sequence is an arithmetic sequence.

element sequence:
a[i], a[i+1]

response format:
Answer: You respond with Yes or No for whether there are consecutive subscript elements whose format is "a[]" and their subscript sequence sequence is an arithmetic sequence.
Information: If your answer is Yes, you give all sequences that meets the condition, and each sequence is directly from the element sequence. Otherwise, you respond with None. Please explain it.
''',
'''
Answer: Yes
Information:
sequence 1: a[i], a[i+1]
'''],
['''
Extract consecutive subscript elements whose format is "a[]" from the following element sequence, and their subscript sequence is an arithmetic sequence.

element sequence:
a[i1], a[i2]

response format:
Answer: You respond with Yes or No for whether there are consecutive subscript elements whose format is "a[]" and their subscript sequence sequence is an arithmetic sequence.
Information: If your answer is Yes, you give all sequences that meets the condition, and each sequence is directly from the element sequence. Otherwise, you respond with None. Please explain it.
''',
'''
Answer: No
Information:
None
''']
]
    '''
    218 iterable_zj[1], iterable_zj[1]
    220 iterable_zj[2], iterable_zj[2]
    221 iterable_zj[0], iterable_zj[0]
    83 iterable_zj[0::-1], iterable_zj[0:-11:-1]
    82 sequence 1: iterable_zj[-1], iterable_zj[9]
    81 sequence 1: iterable_zj[-11:-9], iterable_zj[:1]
    80 iterable_zj[-11:11], iterable_zj[:]
    79 iterable_zj[[1, 3, 5]], iterable_zj[[1, 3, 5]]
    75 iterable_zj[:, 5:2:-1], iterable_zj[:, 5:2:-1]
    94 iterable_zj['season'], iterable_zj['episode']
    
    116 iterable_zj[2], iterable_zj[1], iterable_zj[3]
    sequence 1: iterable_zj[2], iterable_zj[1], iterable_zj[3]
    sequence 2: iterable_zj[3], iterable_zj[1], iterable_zj[2]
    
    243 iterable_zj[1], iterable_zj[0]
     Answer: No
    Information:
    None
    
    element sequence:
iterable_zj[0], iterable_zj[2], iterable_zj[3], iterable_zj[4]
sequence 1: iterable_zj[0], iterable_zj[2], iterable_zj[3], iterable_zj[4]

    iterable_zj[15], iterable_zj[16], iterable_zj[17], iterable_zj[5]
    sequence 1: iterable_zj[15], iterable_zj[16], iterable_zj[17]
    
    
    element sequence:
iterable_zj[5], iterable_zj[4]
sequence 1: iterable_zj[5], iterable_zj[4]
    '''

    idiom = "call_star"
    save_complicated_code_dir_root = util.data_root + "chatgpt/NonIdiomatic/"
    # save_complicated_code_dir_root = util.data_root + "NonIdiomatic/find_code_snippets/"
    save_complicated_code_dir = save_complicated_code_dir_root + "sample_methods/"

    samples = util.load_pkl(save_complicated_code_dir, "sample_methods_" + idiom)

    # random.seed(2023)
    file_name = "abstract_same_value_all"#"abstract_value_all"  # "whether_can_var_unpack_for_subscript_stmt_instr_explain_4_new"
    samples = util.load_pkl(save_complicated_code_dir_root + idiom + "/", file_name)

    # samples = random.sample(samples, 50)
    file_name = "extract_arithmetic_seq_from_abstract_same_subscript_value_arguments_instr7_all"  # "extract_arithmetic_seq_from_arguments_instr3_all"  # "whether_can_var_unpack_for_subscript_stmt_instr_explain_4_new"
    # file_name = "extract_arithmetic_seq_from_abstract_same_subscript_value_arguments_instr7_all_2_sample"  # "extract_arithmetic_seq_from_arguments_instr3_all"  # "whether_can_var_unpack_for_subscript_stmt_instr_explain_4_new"

    # '''
    reponse_list = call_star_util.get_response_abstract_same_subscript_value(user_instr, examples, samples[:],
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
