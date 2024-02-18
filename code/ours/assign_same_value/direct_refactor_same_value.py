import os, sys
import struct
import traceback

import util_rewrite

code_dir = "/".join(os.path.abspath(__file__).split("/")[:-2]) + "/"
print("code path: ", code_dir)
sys.path.append(code_dir)
import chatgpt_util, random,chat_gpt_ast_util
import openai, tiktoken, ast, util,util_rewrite
import ast,ass_same_value_util
def extract_module(samples):
    all_codes=[]
    count=0
    reponse_list = []
    method_code_list = []
    one_other = []
    for ind_sampl, sample_method in enumerate(samples):
        method_code_list.append(sample_method)
        # if ind_sampl>=9000:
        #     break

    for *other, method_code in method_code_list:
        # if "do_setup$1697" not in other:
        #     continue
        # print(other[2:])

        method_code=ast.unparse(ast.parse(method_code))
        # tree=ast.parse(method_code)
        # if "data_shifted.append(data[(column - row & 3) * 4 + row])" not in method_code:#"y.append(_triangular_inv(x[i]))" _all_input_text.append(i_text) addresses.append({'doctype':a.append(getattr(self, i)) area.append(m_id.eq(i).sum().item()) addresses.append({'doctype':psutil.process_iter(attrs=['name'])#"for item in account_dumps:" "wires_in_net.add(wire['name'])" "for interaction in interactions:" "for (_name, email) in settings.ADMINS" "for syn in synsets:"
        #     continue
        all_nodes = chat_gpt_ast_util.find_consecutive_assign_nodes(method_code)
        for nodes in all_nodes:
            ass_same_value_nodes=chat_gpt_ast_util.group_assign_nodes(nodes)
            for ass_list in ass_same_value_nodes:
                if len(ass_list)<=1:
                    continue
                count += 1
                all_codes.append([*other,method_code,[ast.unparse(e) for e in ass_list]])
                # print("code:\n", "\n".join([ast.unparse(e) for e in ass_list]))
                # break
    print("count: ",count)
    return all_codes
if __name__ == '__main__':

    user_instr = '''
Refactor the following Python code consisting of multiple assignment statements with chained assignment to assign the same value to multiple variables in a single line.

Python code:
{{code}}

response format:
Answer: You respond with Yes or No for whether the code can be refactored with chained assignment.
Information: If your answer is Yes, you give the refactored code. Otherwise, you respond with None. 
'''
    examples = [
['''
Refactor the following Python code consisting of multiple assignment statements with chained assignment to assign the same value to multiple variables in a single line.

Python code:
a=1
b=1
      
response format:
Answer: You respond with Yes or No for whether the code can be refactored with chained assignment.
Information: If your answer is Yes, you give the refactored code. Otherwise, you respond with None. 
''',
'''
Answer: Yes
Information:
a=b=1
''']

]

    idiom = "with_stmt"
    idiom = "list_comprehension"
    idiom = "set_comprehension"
    idiom = "dict_comprehension"
    idiom = "chained_assignment"
    save_complicated_code_dir_root = util.data_root + "chatgpt/NonIdiomatic/"
    # save_complicated_code_dir_root = util.data_root + "NonIdiomatic/find_code_snippets/"
    save_complicated_code_dir = save_complicated_code_dir_root + "sample_methods/"

    samples = util.load_pkl(save_complicated_code_dir_root, "methods_sample_10000" )#methods_sample
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
    sample_code_list=extract_module(samples)
    # random.seed(2023)
    # samples = random.sample(sample_code_list, 324)
    # extract_module(samples)
    '''
    reponse_list = ass_same_value_util.get_response_directly_refactor(user_instr, examples, sample_code_list,
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
    file_name="direct_refactor_chain_ass_same_value"#"direct_refactor_with_stmt_instr_sample_methods"
    util.save_pkl(save_complicated_code_dir_root + idiom + "/",
                  file_name,
                  reponse_list)
    '''
    # '''
    file_name="direct_refactor_chain_ass_same_value"#"direct_refactor_with_stmt_instr_sample_methods"
    csv_res=[]
    samples = util.load_pkl(save_complicated_code_dir_root + idiom + "/",file_name)
    for ind, sample in enumerate(samples):
        repo_name, file_html,old_path, class_name, method_code,for_code, _, response =sample
        # print(">>>>class_name:",repo_name, old_path, file_html, "xx",class_name,"tt")
        content = response["choices"][0]["message"]["content"]
        flag_ref,refactored_code=ass_same_value_util.parse_refactor_code(content)
        if flag_ref:
            if "for i in range(num_types):" in refactored_code:
                print(">>>Come here: ",content)
            csv_res.append([repo_name, file_html,old_path, class_name, method_code,"\n".join(for_code),refactored_code])
            # print(">>>>for_code:",for_code)
            # print(">>>>response:",response)
            # print(">>>>refactored_code:",flag_ref,refactored_code)
            # break
        # else:
        #     csv_res.append([repo_name, file_html,old_path, class_name, method_code,for_code,refactored_code])


        # reponse_list.append(
        #     [*other, for_code])
        # reponse_list[-1].extend([[msg], response])
        # new_code, method_code, _, response = sample
    print("len of samples: ",len(csv_res))
    util.save_csv(
        save_complicated_code_dir_root + idiom + "/" + file_name+"_contain_cannot_refac.csv",
        csv_res,
        ["repo_name", "file_path", "file_html", "class_name", "me_code", "old_code", "new_code", "bool_code",
         "chatGPT_code", "if_correct", "reversed_code", "non_replace_var_refactored_code", "refactored_code", "acc",
         "instruction", "sys_msg", "exam_msg", "user_msg"])
    # '''
