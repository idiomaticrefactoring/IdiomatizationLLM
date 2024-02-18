import os,sys
import traceback
code_dir = "/".join(os.path.abspath(__file__).split("/")[:-2]) + "/"
print("code path: ",code_dir)
sys.path.append(code_dir)
import chatgpt_util,random
import openai, tiktoken,ast,util
import ast
import extract_boolop_and
#For the following Python code, for each comparison operation, you only use one symbol v to abstract all comparison operands no matter the comparison operand is a complicated or simple experssion. And the same comparison operands must be represented by the same symbol. Please do not change other code.
#For the following Python code, for each comparison operation, regardless of whether the comparison operand is a simple or complex expression, only one symbol v is simply used to represent each comparison operand. And the same comparison operands must be represented by the same symbol. Please do not change other code.
#For the following Python code, for each comparison operation, regardless of whether the comparison operand is a simple or complex expression, simply use only one symbol v to simplify each comparison operand. And the same comparison operands must be represented by the same symbol. Please do not change other code.
#Abstract_boolop_4_no_explain_add_new.py
user_instr='''
For the following Python code, for each comparison operation, you only use one identifier v to simplify each comparison operand regardless of whether the comparison operand is a simple or complex expression. And the same comparison operands must be represented by the same symbol. Please do not change other code.

Python code:
{{code}}

all comparison operands:
{{operand}}'''
examples=[
[
'''
For the following Python code, for each comparison operation, you only use one identifier v to simplify each comparison operand regardless of whether the comparison operand is a simple or complex expression. And the same comparison operands must be represented by the same symbol. Please do not change other code.

Python code:
a > 1 and d % e == 1

all comparison operands:
a
1
d % e
1
''',
'''
symbols:
a: v1
1: v2
d + e: v3

New Python code: v1 > v2 and v3 == v2
'''
]]
# ,[
# '''
# For the following Python code, for each comparison operation, you extract all comparison operands and only use one identifier v to simplify each comparison operand regardless of whether the comparison operand is a simple or complex expression. And the same comparison operands must be represented by the same symbol. Please do not change other code.
#
# Python code:
# (iter % save_interval == 0 or iter == iters) and local_rank == 0
#
# all comparison operands:
# iter
# save_interval
# local_rank
# 0''','''
# symbols:
# iter % save_interval: v1
# 0: v2
# iter: v3
# iters: v4
# local_rank: v5
#
# New Python code: (v1 == v2 or v3 == v4) and v5 == v2'''
# ]
'''
lab is not None and len(label_batcher) == 0 and (len(data_batcher) > 0)
v1 is not v2 and v4 == v5 and (v7 > v8)

l_type == 'CNAME' and rdtype != 'CNAME'
v1 == v2 and v3 != v4

in_size[0] % 8 == 0 and in_size[1] % 8 == 0
v1 % v2 == 0 and v3 % v2 == 0

os.getuid() == 0 and selinux.is_selinux_enabled() != 0
v1 == v2 and v3 != v4

'''
'''
l_type == 'CNAME' and rdtype != 'CNAME'
v1 == v2 and v3 != v4

in_size[0] % 8 == 0 and in_size[1] % 8 == 0
v1 % v2 == 0 and v3 % v2 == 0

os.getuid() == 0 and selinux.is_selinux_enabled() != 0
v1 == v2 and v3 != v4

word_lens[i][j] == 0 and j != 0
v1[v2][v3] == v4 and v3 != v4

'''
'''
max_episode_steps is None and self.env.spec is not None
v1 is v2 and v3 is not None

mode == 'UPSAMPLE_MODE' and output_spatial_sizes[0] % shape[1] == 0 and (output_spatial_sizes[1] % shape[2] == 0)
v1 == v2 and v3 % v4 == v5 and (v6 % v7 == v5)

CompareBigEndian(s_val, [0]) > 0 and CompareBigEndian(s_val, max_mod_half_order) <= 0
v1 > v2 and v1 <= CompareBigEndian(s_val, v3)

lab is not None and len(label_batcher) == 0 and (len(data_batcher) > 0)
v1 is not v2 and v4 == v7 and (v6 > v7)

l_type == 'CNAME' and rdtype != 'CNAME'
v1 == v2 and v3 != v4

in_size[0] % 8 == 0 and in_size[1] % 8 == 0
v1 % v2 == 0 and v3 % v2 == 0

os.getuid() == 0 and selinux.is_selinux_enabled() != 0
v1 == v2 and v3 != v4

word_lens[i][j] == 0 and j != 0
v1[v2][v3] == v4 and v3 != v4
'''
'''
l_type == 'CNAME' and rdtype != 'CNAME'
v1 == v2 and v3 != v4

in_size[0] % 8 == 0 and in_size[1] % 8 == 0
v1 % v2 == 0 and v3 % v2 == 0

len(err_msg) > 0 and rank == 0
v1 > v2 and v3 == v4

os.getuid() == 0 and selinux.is_selinux_enabled() != 0
v1 == v2 and v3 != v4

word_lens[i][j] == 0 and j != 0
v1 == v2 and v3 != v4

'''
#     [
# '''
# We give you a Python code whose AST is BoolOp, you represent the expression with the symbol v and do not change other code, and the same expression is represented with the same symbol.
#
# Python code:
# e.b[0] == a and c[e] > 1 and d.e[i] < f and a.e.c in g
# ''',
# '''
# symbols:
# v1: e.b[0]
# v2: a
# v3: c[e]
# v4: 1
# v5: d.e[i]
# v6: f
# v7: a.e.c
# v8: g
#
# New Python code: v1 == v2 and v3 > v4 and v5 < v6 and v7 in v8
# '''
# ]


idiom = "chain comparison"
idiom = "_".join(idiom.split(" "))
save_complicated_code_dir_root = util.data_root + "chatgpt/NonIdiomatic/"
# save_complicated_code_dir_root = util.data_root + "NonIdiomatic/find_code_snippets/"
save_complicated_code_dir=save_complicated_code_dir_root+"sample_methods/"

samples = util.load_pkl(save_complicated_code_dir, "sample_methods_" + idiom)
save_file_name="abstract_same_operand_instr"#"abstract_boolop_value_instr_no_explain"

import chain_comparison_util
# '''
# reponse_list=chain_comparison_util.get_response(user_instr,examples,samples[:],sys_msg="You are a helpful assistant.")
reponse_list=chain_comparison_util.get_response_no_repeat_abstract(user_instr,examples,samples[:],sys_msg="You are a helpful assistant.")

# util.save_pkl(save_complicated_code_dir_root + "chain_comparison_bool_compare/",
#                           "abstract_boolop_value_1_example_special_example",
#                           reponse_list)
util.save_pkl(save_complicated_code_dir_root + idiom+"/",
              save_file_name,
                          reponse_list)
# '''

samples = util.load_pkl(save_complicated_code_dir_root+ idiom+"/", save_file_name)
for sample in samples:


    bool_code, old_code, repo_name, old_path, file_html, class_name, me_name, *other, new_code, method_code, real_comparison_1, real_comparison_2, msg2msg, response = sample
    if "name[-2:] != '__'" not in bool_code:
        continue
    print("bool_code: ", bool_code,real_comparison_1, real_comparison_2,)

    # print("comparison_1,comparison_2: ",real_comparison_1,real_comparison_2)
    # if not ("not in" in real_comparison_1  or "not in" in real_comparison_2):
    #     continue
    # if not ("is" in real_comparison_1  or "is" in real_comparison_2):
    #     continue
    # v3 > v2

    response = response["choices"][0]["message"]["content"]
    print("response: ",response)


'''
reponse_list=chain_comparison_util.get_response(user_instr,examples,samples[:],sys_msg="You are a helpful assistant.")
util.save_pkl(save_complicated_code_dir_root + "chain_comparison_bool_compare/",
                          "abstract_boolop_value_2_example_multi_binary_operation_new_2",
                          reponse_list)
# util.save_pkl(save_complicated_code_dir_root + "chain_comparison_bool_compare/",
#                           "abstract_boolop_value_2_example_multi_binary_operation",
#                           reponse_list)
# samples = util.load_pkl(save_complicated_code_dir_root+ "chain_comparison_bool_compare/", "abstract_boolop_value_2_example_multi_binary_operation")
# print("sample 2: ",samples[1])
# print("len: ",len(samples))

csv_file_name="abstract_boolop_value_2_example_multi_binary_operation_new_2.csv"
csv_res=chain_comparison_util.save_csv(save_complicated_code_dir_root,"abstract_boolop_value_2_example_multi_binary_operation_new_2",csv_file_name)
util.save_csv(
        save_complicated_code_dir_root + "chain_comparison_bool_compare/" + csv_file_name,
        csv_res,
        ["repo_name", "file_path", "file_html", "class_name", "me_name", "me_code", "old_code", "new_code", "bool_code",
         "chatGPT_code", "if_correct",
         "instruction", "sys_msg", "exam_msg", "user_msg"])
'''
