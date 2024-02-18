import os,sys
import struct
import traceback
code_dir = "/".join(os.path.abspath(__file__).split("/")[:-2]) + "/"
print("code path: ",code_dir)
sys.path.append(code_dir)
import chatgpt_util,random
import openai, tiktoken,ast,util
import ast
import truth_test_util,whether_is_member_EmptySet,truth_test_instr,util_rewrite
def extract_new_Python_code(answer):
    if "New Python Code" in answer:
        python_code = answer.split(":")[-1].strip()
        return python_code
    return None
def extract_map(response):
    str_map = ""
    e = response.split("\n")
    for i in e:
        if i.startswith("v"):
            str_map += i + "\n"
    return str_map
def extract_values(response):
    values_list = []
    e = response.split("\n")
    for i in e:
        if i.startswith("v"):
            values_list.append(i.split(":")[-1].strip())
    return values_list
import extract_test_boolop,extract_compare_from_test_boolop
if __name__ == '__main__':


    idiom = "truth value testing"
    idiom = "_".join(idiom.split(" "))
    save_complicated_code_dir_root = util.data_root + "chatgpt/NonIdiomatic/"
    # save_complicated_code_dir_root = util.data_root + "NonIdiomatic/find_code_snippets/"
    save_complicated_code_dir = save_complicated_code_dir_root + "sample_methods/"

    samples = util.load_pkl(save_complicated_code_dir, "sample_methods_" + idiom)
    save_file_name="rewrite_instr_from_code_generation"
    reponse_list = []
    method_code_list = []
    for ind_sampl, sample_method in enumerate(samples):
        for code in sample_method:
            # repo_name, old_path, file_html, class_name,me_name, old_list, new_tree,\
            #     old_code,new_code, method_code=code
            # break
            *other, old_list, new_tree, \
            old_code, new_code, method_code = code
            # print("method_code: ", method_code)
            method_code_list.append([*other, old_list, new_tree, old_code, new_code, method_code])
            break
    for *other, old_list, new_tree, old_code, new_code, method_code in method_code_list:
        bool_code_list = extract_test_boolop.get_BoolOp_test(method_code)

        # '''
        tmp_list = []
        for bool_code in bool_code_list:
            comp_list = extract_compare_from_test_boolop.get_compare(ast.unparse(bool_code))
            tmp_list.extend(comp_list)
        for bool_node in tmp_list:
            real_compare_value=None
            me_code = ast.unparse(bool_node)
            # if "0 == query.Bool()._min_should_match" not in me_code:
            #     continue
            left_value,right_value=truth_test_instr.get_values(bool_node)
            flag_is = whether_is_member_EmptySet.is_member(left_value)
            if flag_is:
                real_compare_value=right_value
            flag_is = whether_is_member_EmptySet.is_member(right_value)
            if flag_is:
                real_compare_value=left_value
            print(">>>>>>>real_compare_value: ",real_compare_value)
            if real_compare_value is not None:
                # new_code, method_code
                ops=truth_test_instr.check_comparison_operator(me_code)
                if ops=="==":
                    real_compare_value = util_rewrite.join(["not",real_compare_value]," ")
                reponse_list.append([me_code,old_code,*other,real_compare_value.strip(),method_code])
            else:
                flag_is = whether_is_member_EmptySet.is_member_True(left_value)
                if flag_is:
                    real_compare_value = right_value
                flag_is = whether_is_member_EmptySet.is_member_True(right_value)
                if flag_is:
                    real_compare_value = left_value
                ops = truth_test_instr.check_comparison_operator(me_code)
                if real_compare_value is not None:
                    if ops == "!=":
                        real_compare_value = util_rewrite.join(["not", real_compare_value], " ")
                        reponse_list.append([me_code, old_code, *other, real_compare_value.strip(), method_code])

                # print(">>>>>>>>:",me_code,real_compare_value)

    util.save_pkl(save_complicated_code_dir_root+idiom+"/",
                  save_file_name,
                  reponse_list)
    all_code_list = util.load_pkl(save_complicated_code_dir_root + idiom + "/",
                                  save_file_name)
    print("final refactor_code: ", all_code_list[124])


    print("final refactor_code: ", all_code_list[124])
    # '''
    refactor_code_list = [e[-2] for e in all_code_list]


    csv_res_list,chatgpt_refactor_new_python_code_list,ground_truth_list = truth_test_util.get_acc_from_all_code_generation(samples, all_code_list, refactor_code_list)
    csv_file_name = save_file_name+".csv"  # "rewrite_instr_replace_with_real_var_all.csv"#"rewrite_instr_replace_with_real_var.csv"
    print("len: ",len(samples))
    util.save_csv(
        save_complicated_code_dir_root + idiom + "/" + csv_file_name,
        csv_res_list,
        ["repo_name", "file_path", "file_html", "class_name", "me_name", "me_code", "old_code", "new_code", "bool_code",
         "chatGPT_code", "if_correct", "reversed_code", "non_replace_var_refactored_code", "refactored_code", "acc",
         "instruction", "sys_msg", "exam_msg", "user_msg"])
    util.save_pkl(save_complicated_code_dir_root + idiom + "/",
                  "get_acc_res",
                  csv_res_list)
    util.save_pkl(save_complicated_code_dir_root + idiom+"/",
                  "chatgpt_refactor_new_python_code_list",
                  chatgpt_refactor_new_python_code_list)
    util.save_pkl(save_complicated_code_dir_root + idiom+"/",
                  "ridiom_truth_test",
                  ground_truth_list)
    # util.save_pkl(save_complicated_code_dir_root + "chain_comparison_bool_compare/",
    #               "rewrite_compare_emptySet_instr",
    #               reponse_list)
    # util.save_pkl(save_complicated_code_dir_root + "chain_comparison_bool_compare/",
    #               "rewrite_compare_emptySet_instr",
    #               reponse_list)

    
    # refactor_file_name="rewrite_compare_emptySet_instr"
    # refactor_code_list = util.load_pkl(save_complicated_code_dir_root + "chain_comparison_bool_compare/",
    #                                      refactor_file_name)
    # refactor_code_list=[e[1] for e in refactor_code_list]
    # print("refactor_code_list: ",refactor_code_list[:10])
    # csv_res_list = truth_test_util.save_csv(
    #                                        new_python_code_list,refactor_code_list)
    #
    # print("csv_res_list: ", len(csv_res_list))
    # '''

    # find_comparison_from_abstract_boolop_value_2_example_multi_binary_operation_new_2

    # csv_res_list = merge_all_info(csv_res_list, refactored_code_list, reversed_python_code_list)
    # print("len csv_res_list: ", len(csv_res_list))

    # sample_csv=chain_comparison_util.save_csv(save_complicated_code_dir_root,"reversed_comparison_by_knowledge_from_abstract",csv_file_name)
    #
    # res=[sample+responses_list[ind] for ind,sample in enumerate(sample_csv)]
    #
    # csv_file_name="refactored_code_abstract_find_same_operand_reversed_replace_abstract.csv"
    # csv_file_name="refactored_code_abstract_find_same_operand_reversed_replace_abstract_new_3.csv"
    '''
    csv_file_name = "replace_abstract_instr5_with_real_var.csv"

    util.save_csv(
        save_complicated_code_dir_root + idiom+"/" + csv_file_name,
        csv_res_list,
        ["repo_name", "file_path", "file_html", "class_name", "me_name", "me_code", "old_code", "new_code", "bool_code",
         "chatGPT_code", "YesorNo_emptyset" "if_correct", "acc",
         "instruction", "sys_msg", "exam_msg", "user_msg"])
    '''