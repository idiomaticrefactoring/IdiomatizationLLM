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
#whether_slice_for_abstract_same_subscript_value_arithmetic_seq_all_3_assume_iterable_all_all.py
if __name__ == '__main__':
    '''
    Variable unpacking in for statements in Python is a way to assign values to multiple variables at once from an iterable object such as a list, tuple, or dictionary. It allows you to iterate over the iterable and assign each value to a separate variable in a single line of code. 
    '''
    user_instr = '''
Assume "{{var}}" is an iterable such as a list or tuple, you use the slice operator [:] to slice "{{var}}"  to get the elements {{elements}} in Python 

response format:
Answer: You respond with Yes or No for whether can slice an iterable "{{var}}".
Information: If your answer is Yes, you give the sliced "{{var}}". Otherwise, you respond with None. Please explain it.
'''
    examples = [['''
Assume "a" is an iterable such as a list or tuple, you use the slice operator [:] to slice "a" to get elements "a[0]", "a[1]" in Python 

response format:
Answer: You respond with Yes or No for whether can slice an iterable "{{var}}".
Information: If your answer is Yes, you give the sliced "{{var}}". Otherwise, you respond with None. Please explain it.
''',
'''
Answer: Yes
Information: a[:2]
'''],
['''
Assume "a" is an iterable such as a list or tuple, you use the slice operator [:] to slice "a" to get elements "a[0]", "a[2]" in Python 

response format:
Answer: You respond with Yes or No for whether can slice an iterable "{{var}}".
Information: If your answer is Yes, you give the sliced "{{var}}". Otherwise, you respond with None. Please explain it.
''',
'''
Answer: Yes
Information: a[:4:2]
'''],
['''
Assume "a" is an iterable such as a list or tuple, you use the slice operator [:] to slice "a" to get elements "a[1]", "a[3]" in Python 

response format:
Answer: You respond with Yes or No for whether can slice an iterable "{{var}}".
Information: If your answer is Yes, you give the sliced "{{var}}". Otherwise, you respond with None. Please explain it.
''',
'''
Answer: Yes
Information: a[1:6:2]
'''],
['''
Assume "a" is an iterable such as a list or tuple, you use the slice operator [:] to slice "a" to get elements "a[2]", "a[1]" in Python 

response format:
Answer: You respond with Yes or No for whether can slice an iterable "{{var}}".
Information: If your answer is Yes, you give the sliced "{{var}}". Otherwise, you respond with None. Please explain it.
''',
'''
Answer: Yes
Information: a[2:0:-1]
'''],
['''
Assume "a" is an iterable such as a list or tuple, you use the slice operator [:] to slice "a" to get the elements "a[i]", "a[i+1]" in Python 

response format:
Answer: You respond with Yes or No for whether can slice an iterable "{{var}}".
Information: If your answer is Yes, you give the sliced "{{var}}". Otherwise, you respond with None. Please explain it.
''',
'''
Answer: Yes
Information: a[i:i+2]
'''],
['''
Assume "a" is an iterable such as a list or tuple, you use the slice operator [:] to slice "a" to get elements "a[0]", "a[0]" in Python 

response format:
Answer: You respond with Yes or No for whether can slice an iterable "{{var}}".
Information: If your answer is Yes, you give the sliced "{{var}}". Otherwise, you respond with None. Please explain it.
''',
'''
Answer: No
Information: None
'''],
['''
Assume "a" is an iterable such as a list or tuple, you use the slice operator [:] to slice "a" to get elements "a[:]", "a['key']" in Python 

response format:
Answer: You respond with Yes or No for whether can slice an iterable "{{var}}".
Information: If your answer is Yes, you give the sliced "{{var}}". Otherwise, you respond with None. Please explain it.
''',
'''
Answer: No
Information: None
''']

]
    '''
    73 Assume "iterable_zj" is an iterable such as a list or tuple, you use the slice operator [:] to slice "iterable_zj"  to get the elements  iterable_zj[0], iterable_zj[2] in Python 

 Answer: Yes
Information: iterable_zj[::2]

115 Assume "iterable_zj" is an iterable such as a list or tuple, you use the slice operator [:] to slice "iterable_zj"  to get the elements  iterable_zj[2], iterable_zj[1], iterable_zj[3] in Python 
 Answer: Yes
Information: iterable_zj[1:4][::-1]

79 Assume "iterable_zj" is an iterable such as a list or tuple, you use the slice operator [:] to slice "iterable_zj"  to get the elements  iterable_zj[-11:11], iterable_zj[:] in Python 
 Answer: Yes
Information: iterable_zj[-11:11], iterable_zj[:]

80 Assume "iterable_zj" is an iterable such as a list or tuple, you use the slice operator [:] to slice "iterable_zj"  to get the elements  iterable_zj[-11:-9], iterable_zj[:1] in Python 
Information: iterable_zj[-11:-9] + iterable_zj[:1]

81 Assume "iterable_zj" is an iterable such as a list or tuple, you use the slice operator [:] to slice "iterable_zj"  to get the elements  iterable_zj[-1], iterable_zj[9] in Python 
 Answer: Yes
Information: iterable_zj[-1], iterable_zj[9]

82 Assume "iterable_zj" is an iterable such as a list or tuple, you use the slice operator [:] to slice "iterable_zj"  to get the elements  iterable_zj[0::-1], iterable_zj[0:-11:-1] in Python 
 Answer: Yes
Information: iterable_zj[0::-1] will give all the elements of iterable_zj in reverse order starting from the first element. iterable_zj[0:-11:-1] will give the first 10 elements of iterable_zj in reverse order.

93 Assume "iterable_zj" is an iterable such as a list or tuple, you use the slice operator [:] to slice "iterable_zj"  to get the elements  iterable_zj['season'], iterable_zj['episode'] in Python 
 Answer: No
Information: It is not possible to slice an iterable using dictionary keys. Slicing is only possible using integer indices or slices.

74 Assume "iterable_zj" is an iterable such as a list or tuple, you use the slice operator [:] to slice "iterable_zj"  to get the elements  iterable_zj[0], iterable_zj[0] in Python 
 Answer: No
Information: None

75 Assume "iterable_zj" is an iterable such as a list or tuple, you use the slice operator [:] to slice "iterable_zj"  to get the elements  iterable_zj[:, [1, 2, 3]], iterable_zj[:, [1, 2, 3]] in Python 
 Answer: No
Information: The slice operator [:] cannot be used to slice a multi-dimensional iterable like "iterable_zj". Instead, you can use indexing to access specific elements or ranges of elements in each dimension of the iterable. For example, to get the elements iterable_zj[:, [1, 2, 3]], iterable_zj[:, [1, 2, 3]], you can use numpy indexing like this: `iterable_zj[:, [1, 2, 3]]`.

    '''

    idiom = "call_star"
    save_complicated_code_dir_root = util.data_root + "chatgpt/NonIdiomatic/"
    # save_complicated_code_dir_root = util.data_root + "NonIdiomatic/find_code_snippets/"
    save_complicated_code_dir = save_complicated_code_dir_root + "sample_methods/"

    samples = util.load_pkl(save_complicated_code_dir, "sample_methods_" + idiom)

    # random.seed(2023)
    # samples = random.sample(samples, 50)
    file_name = "extract_arithmetic_seq_from_abstract_same_subscript_value_arguments_instr7_all"
    # file_name = "extract_arithmetic_seq_from_abstract_same_subscript_value_arguments_instr7_all_2_sample"#"extract_arithmetic_seq_from_abstract_same_subscript_value_arguments_instr7_all"#"extract_arithmetic_seq_from_abstract_same_subscript_value_arguments_instr7_all"#"extract_arithmetic_seq_from_abstract_value_arguments_instr7_all"#"extract_arithmetic_seq_from_abstract_value_arguments_instr7_50"#"extract_arithmetic_seq_from_abstract_value_arguments_instr5_50"#"extract_arithmetic_seq_from_abstract_value_arguments_instr3"#"extract_arithmetic_seq_from_abstract_value_arguments_instr3"  # "whether_can_var_unpack_for_subscript_stmt_instr_explain_4_new"
    samples = util.load_pkl(save_complicated_code_dir_root + idiom + "/", file_name)
    print("samples: ",len(samples))
    # '''
    reponse_list = call_star_util.get_whether_slice_response_abstract_same_subscript(user_instr, examples, samples,
                                                        sys_msg="You are a helpful assistant.")

    file_name = "whether_slice_for_abstract_same_subscript_value_arithmetic_seq_all_3_assume_iterable_all_all"  # "whether_can_var_unpack_for_subscript_stmt_instr_explain_4_new"
    # file_name = "whether_slice_for_abstract_same_subscript_value_arithmetic_seq_all_3_assume_iterable_all_all_2_sample"  # "whether_can_var_unpack_for_subscript_stmt_instr_explain_4_new"

    # util.save_pkl(save_complicated_code_dir_root + "chain_comparison_bool_compare/",
    #               "abstract_one_compare_instr",
    #               reponse_list)
    # util.save_pkl(save_complicated_code_dir_root+ idiom + "/",
    #               "extract_comparators_one_compare_instr",
    #               reponse_list)

    # util.save_pkl(save_complicated_code_dir_root + idiom + "/",
    #               file_name,
    #               reponse_list)

    # '''
    '''
    samples = util.load_pkl(save_complicated_code_dir_root + idiom + "/", file_name)

    csv_res_list = call_star_util.save_csv(samples, [None for e in samples])
    util.save_csv(
        save_complicated_code_dir_root + idiom + "/" + file_name + ".csv",
        csv_res_list,
        ["repo_name", "file_path", "file_html", "class_name", "me_name", "me_code", "old_code", "new_code", "bool_code",
         "chatGPT_code", "if_correct", "reversed_code", "non_replace_var_refactored_code", "refactored_code", "acc",
         "instruction", "sys_msg", "exam_msg", "user_msg"])
    '''

