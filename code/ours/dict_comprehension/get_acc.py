import os,sys
import struct
import traceback
code_dir = "/".join(os.path.abspath(__file__).split("/")[:-2]) + "/"
print("code path: ",code_dir)
sys.path.append(code_dir)
import chatgpt_util,random
import openai, tiktoken,ast,util
import ast
import dict_util
if __name__ == '__main__':
    idiom = "dict_comprehension"
    save_complicated_code_dir_root = util.data_root + "chatgpt/NonIdiomatic/"
    # save_complicated_code_dir_root = util.data_root + "NonIdiomatic/find_code_snippets/"
    save_complicated_code_dir = save_complicated_code_dir_root + "sample_methods/"
    samples = util.load_pkl(save_complicated_code_dir, "sample_methods_" + idiom)

    # random.seed(2023)
    # samples = random.sample(samples, 50)
    # samples = random.sample(samples, 70)
    # samples = random.sample(samples, 70)
    # "gpt_result_from_def_stmt_from_abstract_var_all_add_examp_new_filter_for_improve_" + idiom,

    file_name = "direct_refactor_set_comprehension_instr_add_one_example_instr3_2_real_examp_all"  # "extract_arithmetic_seq_from_arguments_instr3_all"  # "whether_can_var_unpack_for_subscript_stmt_instr_explain_4_new"
    file_name = "direct_refactor_set_comprehension_instr_add_one_example_instr3_2_real_examp_all_new"  # "extract_arithmetic_seq_from_arguments_instr3_all"  # "whether_can_var_unpack_for_subscript_stmt_instr_explain_4_new"
    file_name ="gpt_result_from_def_stmt_from_abstract_var_all_add_examp_new_filter_for_" + idiom
    file_name ="gpt_result_from_def_stmt_from_abstract_var_all_add_examp_new_filter_for_improve_" + idiom
    file_name ="gpt_result_from_def_stmt_from_abstract_var_all_add_examp_new_filter_for_improve_all_" + idiom
    file_name = "direct_refactor_dict_comprehension_improve_new"
    file_name = "gpt_result_refactor_newdict_comprehension"

    # file_name = "whether_slice_for_abstract_same_subscript_value_arithmetic_seq_all_3_assume_iterable_all_all_2_sample"#"whether_slice_for_abstract_same_subscript_value_arithmetic_seq_all_3_assume_iterable_all_all"#"whether_slice_for_abstract_value_arithmetic_seq_all_3_assume_iterable_all_all"#"whether_slice_for_abstract_value_arithmetic_seq_all_3_assume_iterable_sample_50"#"whether_slice_for_abstract_value_arithmetic_seq_all_2_assume_iterable_all"#"whether_slice_for_abstract_value_arithmetic_seq_all_2_assume_iterable"  # "whether_slice_for_arithmetic_seq"#"whether_slice_for_arithmetic_seq_all_2"  # "whether_can_var_unpack_for_subscript_stmt_instr_explain_4_new_all"#"whether_can_var_unpack_for_subscript_stmt_instr_explain_4_new"
    refactor_code_list = util.load_pkl(save_complicated_code_dir_root + idiom + "/",
                                       file_name)
    # print("final refactor_code: ", refactor_code_list[124])
    # return predict_res,ground_truth_list,format_new_python_list
    #
    csv_res_list,ground_truth_list,format_new_python_list = dict_util.get_acc_4(samples, refactor_code_list)
    acc_file_name = file_name + "_get_acc.csv"  # "rewrite_instr_replace_with_real_var_all.csv"#"rewrite_instr_replace_with_real_var.csv"
    acc_file_name = file_name + "_get_acc_add_predict.csv"  # "rewrite_instr_replace_with_real_var_all.csv"#"rewrite_instr_replace_with_real_var.csv"
    acc_file_name = file_name + "_get_acc_add_info.csv"  # "rewrite_instr_replace_with_real_var_all.csv"#"rewrite_instr_replace_with_real_var.csv"
    acc_file_name = file_name + "_get_acc_add_info_add_no_in.csv"  # "rewrite_instr_replace_with_real_var_all.csv"#"rewrite_instr_replace_with_real_var.csv"

    print("len: ", len(samples),len(ground_truth_list),len(format_new_python_list))
    # util.save_pkl(save_complicated_code_dir_root + idiom + "/", "ridiom_dict_comprehension",ground_truth_list)
    # util.save_pkl(save_complicated_code_dir_root + idiom + "/", "gpt_result_dict_comprehension_improve",format_new_python_list)

    # util.save_csv(
    #     save_complicated_code_dir_root + idiom + "/" + acc_file_name,
    #     csv_res_list,
    #     ["repo_name", "file_path", "file_html", "class_name", "me_name", "me_code", "old_code", "chatGPT_code",
    #      "element_str",
    #      "slice_str", "truth_code"])
