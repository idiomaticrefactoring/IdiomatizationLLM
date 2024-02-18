import os, sys
import struct
import traceback

import util_rewrite

code_dir = "/".join(os.path.abspath(__file__).split("/")[:-2]) + "/"
print("code path: ", code_dir)
sys.path.append(code_dir)
import chatgpt_util, random
import openai, tiktoken, ast, util,util_rewrite
import ast,with_util

if __name__ == '__main__':

    user_instr = '''
Refactor the following Python code with statement {{stmt}} with With statement in Python as much as possible. Do not refactor other part of code.

Python code:
{{code}}

response format:
Answer: You respond with Yes or No for whether the code can be refactored with With statement.
Information: If your answer is Yes, you give the refactored code. Otherwise, you respond with None. 
'''
    examples = [
['''
Refactor the following Python code with statement open(os.path.join(parent, filename), 'r') in Python as much as possible. Do not refactor other part of code.

Python code:
line = img_path
fin_anno = open(os.path.join(parent, filename), 'r')
bbox_list = []
for (i, anno) in enumerate(fin_anno):
    if i == 0:
        continue
if len(bbox_list) == 0:
    line += ',0,0'
    fout.write(line + '\n')
else:
    fout.write(line + '\n')     
      
response format:
Answer: You respond with Yes or No for whether the code can be refactored with With statement.
Information: If your answer is Yes, you give the refactored code. Otherwise, you respond with None. 
''',
'''
Answer: Yes
Information:
line = img_path
with open(os.path.join(parent, filename), 'r') as fin_anno:
    bbox_list = []
    for (i, anno) in enumerate(fin_anno):
        if i == 0:
            continue
    if len(bbox_list) == 0:
        line += ',0,0'
        fout.write(line + '\n')
    else:
        fout.write(line + '\n') 
'''],
['''
Refactor the following Python code with statement open("dev/conda-recipe/meta.yaml", "r").read() in Python as much as possible. Do not refactor other part of code.

Python code:
if char_map_dict is None:
    char_map_dict = json.load(open(FLAGS.char_map_json_file, 'r'))

response format:
Answer: You respond with Yes or No for whether the code can be refactored with With statement.
Information: If your answer is Yes, you give the refactored code. Otherwise, you respond with None. 
''',
'''
Answer: Yes
Information:
if char_map_dict is None:
    with open(FLAGS.char_map_json_file, 'r') as f:
        char_map_dict = json.load(f)
''']

]

    idiom = "with_stmt"
    # idiom = "list_comprehension"
    # idiom = "set_comprehension"
    # idiom = "dict_comprehension"

    save_complicated_code_dir_root = util.data_root + "chatgpt/NonIdiomatic/"
    # save_complicated_code_dir_root = util.data_root + "NonIdiomatic/find_code_snippets/"
    save_complicated_code_dir = save_complicated_code_dir_root + "sample_methods/"
    file_name = "new_idiom_methods_600"
    samples = util.load_pkl(save_complicated_code_dir_root, file_name)  # methods_sample

    # samples = util.load_pkl(save_complicated_code_dir_root, "methods_sample_10000" )#methods_sample
    #
    # random.seed(2023)
    #
    # samples = random.sample(samples, 70)
    # file_name = "direct_refactor_set_comprehension_instr_add_one_example_instr3_2_real_examp"  # "extract_arithmetic_seq_from_arguments_instr3_all"  # "whether_can_var_unpack_for_subscript_stmt_instr_explain_4_new"
    # file_name = "find_def_stmt_for_a_node"  # "extract_arithmetic_seq_from_arguments_instr3_all"  # "whether_can_var_unpack_for_subscript_stmt_instr_explain_4_new"
    # file_name ="find_def_stmt_for_a_node_all"
    # file_name ="find_def_stmt_for_a_node_all_filter_for"
    # file_name = "find_def_stmt_for_a_node_all_filter_for"  # "extract_arithmetic_seq_from_arguments_instr3_all"  # "whether_can_var_unpack_for_subscript_stmt_instr_explain_4_new"
    # file_name = "find_def_stmt_for_a_node_all_filter_for_improve"
    # file_name = "find_def_stmt_for_a_node_all_filter_for_improve_3"
    # samples = util.load_pkl(save_complicated_code_dir_root + idiom + "/",file_name)
    # print("len of samples: ",len(samples))

    # file_name = "extract_arithmetic_seq_from_abstract_same_subscript_value_arguments_instr7_all_2_sample"  # "extract_arithmetic_seq_from_arguments_instr3_all"  # "whether_can_var_unpack_for_subscript_stmt_instr_explain_4_new"

    '''
    reponse_list = with_util.get_response_directly_refactor_with_specify_stmt_sample_method(user_instr, examples, samples,
                                                     sys_msg="You are a helpful assistant.")
    
    #
    # reponse_list = set_util.get_response_directly_refactor(user_instr, examples, samples[:],
    #                                                     sys_msg="You are a helpful assistant.")
    # # util.save_pkl(save_complicated_code_dir_root + "chain_comparison_bool_compare/",
    #               "abstract_one_compare_instr",
    #               reponse_list)
    # util.save_pkl(save_complicated_code_dir_root+ idiom + "/",
    #               "extract_comparators_one_compare_instr",
    #               reponse_list)
    file_name="direct_refactor_with_stmt_instr_sample_methods_10000"#"direct_refactor_with_stmt_instr_sample_methods"
    util.save_pkl(save_complicated_code_dir_root + idiom + "/",
                  file_name,
                  reponse_list)
    '''
    file_name="direct_refactor_with_stmt_instr_sample_methods_10000"#"direct_refactor_with_stmt_instr_sample_methods"

    samples = util.load_pkl(save_complicated_code_dir_root + idiom + "/",file_name)
    print("len of samples: ",len(samples))
    csv_res=[]

    for ind, sample in enumerate(samples):
        # for k,e in enumerate(sample):
        #     print("k,e: ",k,e)
        repo_name, file_html,old_path, class_name, method_code,for_code, _, response =sample
        # print(">>>>class_name:",repo_name, old_path, file_html, "xx",class_name,"tt")
        method_code=ast.unparse(ast.parse(method_code))
        content = response["choices"][0]["message"]["content"]
        flag_ref,refactored_code=with_util.parse_refactor_code(content)
        if flag_ref:
            if "for i in range(num_types):" in refactored_code:
                print(">>>Come here: ",content)
            csv_res.append([repo_name, file_html,old_path, class_name, method_code,for_code,refactored_code,1])
            # print(">>>>for_code:",for_code)
            # print(">>>>response:",response)
            # print(">>>>refactored_code:",flag_ref,refactored_code)
            # break
        else:
            csv_res.append([repo_name, file_html,old_path, class_name, method_code,for_code,refactored_code,0])


        # reponse_list.append(
        #     [*other, for_code])
        # reponse_list[-1].extend([[msg], response])
        # new_code, method_code, _, response = sample
    print("len of samples: ",len(csv_res))
    file_name = "gpt_with_res_sample_methods"
    idiom = "with_stmt"
    util.save_pkl(save_complicated_code_dir_root + idiom + "/",
                  file_name,
                  csv_res)

    util.save_csv(
        save_complicated_code_dir_root+ idiom+ "/" + file_name + ".csv",
        csv_res,
        ["repo_name", "file_path", "file_html", "class_name", "me_code", "old_code", "new_code", "bool_code",
         "chatGPT_code", "if_correct", "reversed_code", "non_replace_var_refactored_code", "refactored_code", "acc",
         "instruction", "sys_msg", "exam_msg", "user_msg"])




