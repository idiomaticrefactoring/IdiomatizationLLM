import os, sys
import struct
import traceback

code_dir = "/".join(os.path.abspath(__file__).split("/")[:-2]) + "/"
print("code path: ", code_dir)
sys.path.append(code_dir)
import chatgpt_util, random
import openai, tiktoken, ast, util,dict_util
import ast

#find_def_stmt_for_a_node_all_filter_contains_for_improve_3_all.py
if __name__ == '__main__':
    '''
    Variable unpacking in for statements in Python is a way to assign values to multiple variables at once from an iterable object such as a list, tuple, or dictionary. It allows you to iterate over the iterable and assign each value to a separate variable in a single line of code. 
    '''
    user_instr = '''
Find the initialization statement of {{var}} whose format is similar to "{{var}} = {}" or "{{var}} = dict()" from the following Python code so that the given statement can be executed without undefined error.

Python code:
{{code}}

a given statement:
{{given_node}}

response format:
Answer: You respond with Yes or No for whether there is a assignment statement whose format is similar to "{{var}} = {}" or "{{var}} = dict()" from the given Python code that can reach the given statement.
Information: If your answer is Yes, you give the assignment statement. Otherwise, you respond with None.
'''
    examples =[
['''Find the initialization statement of table whose format is similar to "table = {}" or "table = dict()" from the following Python code so that the given statement can be executed without undefined error.

Python code:
def captcha_recognize(img_path):
    import pytesseract
    im = Image.open(img_path).convert('L')
    threshold = 200
    table = dict()
    for i in range(256):
        if i < threshold:
            table[i] = 0
                            
a given statement:
table[i] = 0

response format:
Answer: You respond with Yes or No for whether there is a assignment statement whose format is similar to "table = {}" or "table = dict()" from the given Python code that can reach the given statement.
Information: If your answer is Yes, you give the assignment statement. Otherwise, you respond with None.
''',
'''
Answer: Yes
Information:
table = dict()'''],
['''Find the initialization statement of expected_ids is similar to "expected_ids = {}" or "expected_ids = dict()" from the following Python code so that the given statement can be executed without undefined error.

Python code:
def test_ds_describe_directories():
    """Test good and bad invocations of describe_directories()."""
    client = boto3.client('ds', region_name=TEST_REGION)
    ec2_client = boto3.client('ec2', region_name=TEST_REGION)
    def func():
        m_id = masks.transpose(0, 1).softmax(-1)
        if m_id.shape[-1] == 0:
            m_id = torch.zeros((h, w), dtype=torch.long, device=m_id.device)
        else:
            m_id = m_id.argmax(-1).view(h, w)
    expected_ids = dict()
    limit = 10
    for _ in range(limit):
        expected_ids[client]=create_test_directory(client, ec2_client)
                        
a given statement:
expected_ids[client]=create_test_directory(client, ec2_client)

response format:
Answer: You respond with Yes or No for whether there is a assignment statement whose format is similar to "expected_ids = {}" or "expected_ids = dict()" from the given Python code that can reach the given statement.
Information: If your answer is Yes, you give the assignment statement. Otherwise, you respond with None.
''',
'''
Answer: Yes
Information:
expected_ids = dict()'''],
['''Find the initialization statement of addresses whose format is similar to "addresses = {}" or "addresses = dict()" from the following Python code so that the given statement can be executed without undefined error.

Python code:
def get_all_addresses(tx):
    addresses = dict()
    for txi in tx['inputs']:
        addresses[txi]=txi['address']
                            
a given statement:
addresses[txi]=txi['address']

response format:
Answer: You respond with Yes or No for whether there is a assignment statement whose format is similar to "addresses = {}" or "addresses = dict()" from the given Python code that can reach the given statement.
Information: If your answer is Yes, you give the assignment statement. Otherwise, you respond with None.
''',
'''
Answer: Yes
Information:
addresses = dict()''']

]

    idiom = "dict_comprehension"
    save_complicated_code_dir_root = util.data_root + "chatgpt/NonIdiomatic/"
    # save_complicated_code_dir_root = util.data_root + "NonIdiomatic/find_code_snippets/"
    save_complicated_code_dir = save_complicated_code_dir_root + "sample_methods/"

    samples = util.load_pkl(save_complicated_code_dir, "sample_methods_" + idiom)

    # random.seed(2023)

    # samples = random.sample(samples, 70)
    file_name = "find_def_stmt_improve_all_3"  # "extract_arithmetic_seq_from_arguments_instr3_all"  # "whether_can_var_unpack_for_subscript_stmt_instr_explain_4_new"

    # '''
    reponse_list = dict_util.get_response_find_def_stmt_improve(user_instr, examples, samples[:],
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
