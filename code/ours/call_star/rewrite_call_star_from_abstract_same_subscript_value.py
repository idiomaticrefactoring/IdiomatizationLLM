import os,sys
import struct
import traceback
code_dir = "/".join(os.path.abspath(__file__).split("/")[:-2]) + "/"
print("code path: ",code_dir)
sys.path.append(code_dir)
import chatgpt_util,random
import openai, tiktoken,ast,util
import ast,call_star_util
#rewrite_call_star_from_abstract_same_subscript_value_instr7.py
if __name__ == '__main__':
    idiom = "call_star"
    save_complicated_code_dir_root = util.data_root + "chatgpt/NonIdiomatic/"
    # save_complicated_code_dir_root = util.data_root + "NonIdiomatic/find_code_snippets/"
    save_complicated_code_dir = save_complicated_code_dir_root + "sample_methods/"
    samples = util.load_pkl(save_complicated_code_dir, "sample_methods_" + idiom)
    # random.seed(2023)
    # samples = random.sample(samples, 50)
    file_name = "whether_slice_for_abstract_same_subscript_value_arithmetic_seq_all_3_assume_iterable_all_all"
    # file_name = "whether_slice_for_abstract_same_subscript_value_arithmetic_seq_all_3_assume_iterable_all_all_2_sample"#"whether_slice_for_abstract_same_subscript_value_arithmetic_seq_all_3_assume_iterable_all_all"#"whether_slice_for_abstract_value_arithmetic_seq_all_3_assume_iterable_all_all"#"whether_slice_for_abstract_value_arithmetic_seq_all_3_assume_iterable_sample_50"#"whether_slice_for_abstract_value_arithmetic_seq_all_2_assume_iterable_all"#"whether_slice_for_abstract_value_arithmetic_seq_all_2_assume_iterable"  # "whether_slice_for_arithmetic_seq"#"whether_slice_for_arithmetic_seq_all_2"  # "whether_can_var_unpack_for_subscript_stmt_instr_explain_4_new_all"#"whether_can_var_unpack_for_subscript_stmt_instr_explain_4_new"
    slice_list = util.load_pkl(save_complicated_code_dir_root + idiom + "/", file_name)
    file_name = "rewrite_call_star_from_abstract_same_subscript_value_instr7_all_new"#"rewrite_call_star_from_abstract_instr7_all"#"rewrite_call_star_from_abstract_instr7_all_50"#"rewrite_call_star_from_abstract_all"#"rewrite_call_star_from_abstract"#"rewrite_call_star"#


    response_list = call_star_util.get_rewrite_same_subscript_value(slice_list)
    # '''
    # response_list = call_star_util.get_response_6(slice_list)
    file_name = "rewrite_call_star_from_abstract_same_subscript_value_instr7_all_new_add_cannot_refactor_modify_old_code_new_code"#"rewrite_call_star_from_abstract_instr7_all"#"rewrite_call_star_from_abstract_instr7_all_50"#"rewrite_call_star_from_abstract_all"#"rewrite_call_star_from_abstract"#"rewrite_call_star"#
    util.save_pkl(save_complicated_code_dir_root + idiom + "/",
                  file_name,
                  response_list)

    # '''
    # util.save_csv(
    #     save_complicated_code_dir_root + idiom + "/" + file_name + ".csv",
    #     response_list,
    #     ["repo_name", "file_path", "file_html", "class_name", "me_name", "me_code", "old_code", "new_code", "bool_code",
    #      "chatGPT_code", "if_correct", "reversed_code", "non_replace_var_refactored_code", "refactored_code", "acc",
    #      "instruction", "sys_msg", "exam_msg", "user_msg"])
    refactor_code_list = util.load_pkl(save_complicated_code_dir_root + idiom + "/",
                                       file_name)
    # print("final refactor_code: ", refactor_code_list[124])
    
    new_refactor_code_list = [e[1] for e in refactor_code_list]
    #
    csv_res_list,chatgpt_code_list,ground_truth_list = call_star_util.get_acc_4(samples, refactor_code_list, new_refactor_code_list)
    acc_file_name = file_name + "_get_acc.csv"  # "rewrite_instr_replace_with_real_var_all.csv"#"rewrite_instr_replace_with_real_var.csv"
    acc_file_name = file_name + "_get_acc_add_predict.csv"  # "rewrite_instr_replace_with_real_var_all.csv"#"rewrite_instr_replace_with_real_var.csv"
    acc_file_name = file_name + "_get_acc_add_info.csv"  # "rewrite_instr_replace_with_real_var_all.csv"#"rewrite_instr_replace_with_real_var.csv"
    acc_file_name = file_name + "_get_acc_add_info_add_cannot_refactor.csv"  # "rewrite_instr_replace_with_real_var_all.csv"#"rewrite_instr_replace_with_real_var.csv"
    acc_file_name = file_name + "_get_acc_add_info_add_cannot_refactor_new.csv"  # "rewrite_instr_replace_with_real_var_all.csv"#"rewrite_instr_replace_with_real_var.csv"
    util.save_pkl(save_complicated_code_dir_root + idiom + "/",
                  "ridiom_call_star_result",
                  ground_truth_list)

    util.save_pkl(save_complicated_code_dir_root + idiom + "/",
                  "gpt_call_star_result",
                  chatgpt_code_list)
    util.save_pkl(save_complicated_code_dir_root + idiom + "/",
                  "csv_res_list_pkl",
                  csv_res_list)
    print("len: ", len(samples))
    # util.save_csv(
    #     save_complicated_code_dir_root + idiom + "/" + acc_file_name,
    #     csv_res_list,
    #     ["repo_name", "file_path", "file_html", "class_name", "me_name", "me_code", "old_code", "chatGPT_code", "element_str",
    #      "slice_str", "truth_code"])
    # '''
