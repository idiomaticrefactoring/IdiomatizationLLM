import os, sys
import struct
import traceback

code_dir = "/".join(os.path.abspath(__file__).split("/")[:-2]) + "/"
print("code path: ", code_dir)
sys.path.append(code_dir)
import chatgpt_util, random
import openai, tiktoken, ast, util
import ast,copy

if __name__ == '__main__':
    idiom = "dict_comprehension"
    # util.save_csv(
    #     save_complicated_code_dir_root + idiom + "/" + acc_file_name,
    #     csv_res_list,
    #     ["repo_name", "file_path", "file_html", "class_name", "me_name", "me_code", "old_code", "chatGPT_code",
    #      "element_str",
    #      "slice_str", "truth_code"])
    save_complicated_code_dir_root = util.data_root + "chatgpt/NonIdiomatic/"
    # save_complicated_code_dir_root = util.data_root + "NonIdiomatic/find_code_snippets/"
    save_complicated_code_dir = save_complicated_code_dir_root + "sample_methods/"
    # file_name="which_statement_will_execute_4_improve_2_all_new_get_acc_new_add_continue_instr3_add_new_found_new.csv"
    file_name = "direct_refactor_set_comprehension_instr_add_one_example_instr3_2_real_examp_all"  # "extract_arithmetic_seq_from_arguments_instr3_all"  # "whether_can_var_unpack_for_subscript_stmt_instr_explain_4_new"
    # file_name = "direct_refactor_set_comprehension_instr_add_one_example_instr3_2_real_examp_all"  # "extract_arithmetic_seq_from_arguments_instr3_all"  # "whether_can_var_unpack_for_subscript_stmt_instr_explain_4_new"
    file_name = "gpt_result_from_def_stmt_from_abstract_var_all_add_examp_new_filter_for_improve_list_comprehension_get_acc_add_info_add_no_in.csv"
    file_name = "gpt_result_from_def_stmt_from_abstract_var_all_add_examp_new_filter_for_improve_all_" + idiom
    file_name = file_name + "_get_acc_add_info_add_no_in.csv"  # "rewrite_instr_replace_with_real_var_all.csv"#"rewrite_instr_replace_with_real_var.csv"
    file_name = "gpt_result_refactor_newdict_comprehension_get_acc_add_info_add_no_in.csv"
    # file_name = file_name + "_get_acc_add_info.csv"  # "rewrite_instr_replace_with_real_var_all.csv"#"rewrite_instr_replace_with_real_var.csv"

    benchmarks = []
    all_res = util.load_csv(save_complicated_code_dir_root + idiom + "/" + file_name)

    # repo_name, old_path, file_html, class_name, me_name, method_code, old_code, refactor_code, *other = sample
    flag=0
    res=[]
    count = 0
    count_error = 0
    parse_error=0
    for ind_e,e in enumerate(all_res[:]):
        # if ind_e==0:
        #     continue
        if ind_e==0:
            print("e: ",e)
            continue
        repo_name, old_path, file_html, class_name, me_name, method_code, old_code, chat_gpt_code, ridiom_code, acc, chatgpt_acc, ridiom_acc, real_acc, *other=e
        # print("method_code: ",ind_e,method_code)
        try:
            method_code=ast.unparse(ast.parse(method_code))
            old_code=ast.unparse(ast.parse(old_code))
        except:
            parse_error+=1
            continue
        chat_gpt_code, ridiom_code=ast.unparse(ast.parse(chat_gpt_code)),ast.unparse(ast.parse(ridiom_code)) if "Cannot refactor" not in ridiom_code else ridiom_code
        # if "for init_lr_g in init_lr_g_l:" not in old_code:
        #     continue
        print("old_code: ",old_code)
        print("chatgpt_code: ",chat_gpt_code)
        print("ridiom_codee: ", ridiom_code)
        if "FOUND" in repo_name:
            flag=1
            continue
        if not me_name:
            continue

        acc,real_acc,chatgpt_acc,ridiom_acc=int(acc) if acc.isdigit() else None,int(real_acc) if real_acc.isdigit() else None, int(chatgpt_acc) if chatgpt_acc.isdigit() else None,int(ridiom_acc) if ridiom_acc.isdigit() else None

        if not flag:
            # print("acc: ",acc==1,acc=='1',len(e),e[9])
            if acc==1:
                if real_acc==0:
                    continue
                count+=1
                res.append([repo_name, old_path, file_html, class_name, me_name, method_code, old_code,[chat_gpt_code]])
            elif chatgpt_acc==1:
                # if ridiom_acc!=1:
                #     res.append([repo_name, old_path, file_html, class_name, me_name, method_code, old_code,[chat_gpt_code]])
                # else:
                count_error+=1
                res.append([repo_name, old_path, file_html, class_name, me_name, method_code, old_code,[chat_gpt_code,ridiom_code]])

            elif ridiom_acc==1:
                res.append([repo_name, old_path, file_html, class_name, me_name, method_code, old_code,
                            [ridiom_code]])
            # else:
            #     res.append([repo_name, old_path, file_html, class_name, me_name, method_code, old_code,
            #                 [ridiom_code]])
        else:
            res.append([repo_name, old_path, file_html, class_name, me_name, method_code, old_code,
                        [chat_gpt_code]])
    print("len of benchmark: ",len(res))
    print("error: ",count_error,count,parse_error)
    print("last one: ",res[-1])
    # util.save_pkl(save_complicated_code_dir_root + idiom + "/", "dict_comprehension_bench",res)
    # util.save_pkl(save_complicated_code_dir_root + idiom + "/", "dict_comprehension_bench_new", res)
    util.save_pkl(save_complicated_code_dir_root + idiom + "/", "dict_comprehension_bench_new_2",res)