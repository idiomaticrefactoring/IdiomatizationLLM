import os, sys
import struct
import traceback

code_dir = "/".join(os.path.abspath(__file__).split("/")[:-2]) + "/"
print("code path: ", code_dir)
sys.path.append(code_dir)
import chatgpt_util, random
import openai, tiktoken, ast, util
import ast
from set_comprehension import set_util

if __name__ == '__main__':
    '''
    Variable unpacking in for statements in Python is a way to assign values to multiple variables at once from an iterable object such as a list, tuple, or dictionary. It allows you to iterate over the iterable and assign each value to a separate variable in a single line of code. 
    '''
    user_instr = '''
Determine the assignment statement of {{var}} that can reach a given statement of the following Python code in Python.

Python code:
{{code}}
                            
a given statement:
{{given_node}}

response format:
Answer: You respond with Yes or No for whether there is a assignment statement that reach a given node of a given Python code.
Information: If your answer is Yes, you give the assignment statement. Otherwise, you respond with None.'''
    examples =[
['''Determine the assignment statement of graph[u] that can reach a given statement of the following Python code in Python.

Python code:
graph = {}
for u in self.complete:
    graph[u] = set()
    for v in self.complete[u]:
        if u != v:  # ignore self-loop
            graph[u].add(v)
        else:
            graph[u] = c
                            
a given statement:
graph[u].add(v)

response format:
Answer: You respond with Yes or No for whether there is a assignment statement that reach a given statement of a given Python code.
Information: If your answer is Yes, you give the assignment statement. Otherwise, you respond with None.
''',
'''
Answer: Yes
Information:
graph[u] = set()'''],
['''Determine the assignment statement of expected_ids that can reach a given statement of the following Python code in Python.

Python code:
def test_ds_describe_directories():
    """Test good and bad invocations of describe_directories()."""
    client = boto3.client('ds', region_name=TEST_REGION)
    ec2_client = boto3.client('ec2', region_name=TEST_REGION)
    expected_ids = set()
    limit = 10
    for _ in range(limit):
        expected_ids.add(create_test_directory(client, ec2_client))
                            
a given statement:
expected_ids.add(create_test_directory(client, ec2_client))

response format:
Answer: You respond with Yes or No for whether there is a assignment statement that reach a given statement of a given Python code.
Information: If your answer is Yes, you give the assignment statement. Otherwise, you respond with None.
''',
'''
Answer: Yes
Information:
expected_ids = set()'''],
['''Determine the assignment statement of addresses that can reach a given statement of the following Python code in Python.

Python code:
def get_all_addresses(tx):
    addresses = set()
    for txi in tx['inputs']:
        addresses.add(txi['address'])
                            
a given statement:
addresses.add(txi['address'])

response format:
Answer: You respond with Yes or No for whether there is a assignment statement that reach a given statement of a given Python code.
Information: If your answer is Yes, you give the assignment statement. Otherwise, you respond with None.
''',
'''
Answer: Yes
Information:
addresses = set()''']

]

    idiom = "set_comprehension"
    save_complicated_code_dir_root = util.data_root + "chatgpt/NonIdiomatic/"
    # save_complicated_code_dir_root = util.data_root + "NonIdiomatic/find_code_snippets/"
    save_complicated_code_dir = save_complicated_code_dir_root + "sample_methods/"

    samples = util.load_pkl(save_complicated_code_dir, "sample_methods_" + idiom)

    # random.seed(2023)
    #
    # samples = random.sample(samples, 70)
    file_name = "find_def_stmt_for_a_node_all_filter_for"  # "extract_arithmetic_seq_from_arguments_instr3_all"  # "whether_can_var_unpack_for_subscript_stmt_instr_explain_4_new"

    # file_name = "extract_arithmetic_seq_from_abstract_same_subscript_value_arguments_instr7_all_2_sample"  # "extract_arithmetic_seq_from_arguments_instr3_all"  # "whether_can_var_unpack_for_subscript_stmt_instr_explain_4_new"

    # '''
    reponse_list = set_util.get_response_find_def_stmt_filter(user_instr, examples, samples[:],
                                                           sys_msg="You are a helpful assistant.")
    # util.save_pkl(save_complicated_code_dir_root + "chain_comparison_bool_compare/",
    #               "abstract_one_compare_instr",
    #               reponse_list)
    # util.save_pkl(save_complicated_code_dir_root+ idiom + "/",
    #               "extract_comparators_one_compare_instr",
    #               reponse_list)

    # util.save_pkl(save_complicated_code_dir_root + idiom + "/",
    #               file_name,
    #               reponse_list)
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
