import os, sys
import struct
import traceback

code_dir = "/".join(os.path.abspath(__file__).split("/")[:-2]) + "/"
print("code path: ", code_dir)
sys.path.append(code_dir)
import chatgpt_util, random
import openai, tiktoken, ast, util
import ast,copy
def get_ridiom_res(samples):
    offset=0#-2
    reponse_list=[]
    ground_truth_list=[]
    for ind_sampl, sample_method in enumerate(samples):
        for code in sample_method:
            repo_name, old_path, file_html, class_name,me_name, (ass_node_old, for_node_old, if_node,remove_ass_flag, break_list), for_node_new_else, total_old_code, new_code, method_code = code
            # print("for_node_new_else: ",ast.unparse(for_node_new_else))
            # print("for_node_old: ",ast.unparse(for_node_old))
            # print("if_node: ",ast.unparse(if_node))

            # repo_name, old_path, file_html, class_name,me_name, old_list, new_tree,\
            #     old_code,new_code, method_code=code
            # break
            *other, old_list, new_tree, \
            old_code, new_code, method_code = code
            try:
                ele = [repo_name, old_path, file_html, class_name, me_name, method_code,ast.unparse(ast.parse(ast.unparse(for_node_old)+"\n"+ast.unparse(if_node))), ast.unparse(ast.parse(for_node_new_else))]
            except:
                continue
            ground_truth_list.append(ele)
    return ground_truth_list
def get_eva_p_r(ground_truth_list,new_python_code_list):
    new_python_code_list=[e[:8] for e in new_python_code_list]

    predict_res=[]
    # repo_name, old_path, file_html, class_name, me_name, method_code, old_code, refactor_code, *other = sample
    no_found_wrong = 0
    find_wrong=0
    refactor_wrong = 0
    ground_copy_truth_list=copy.deepcopy(ground_truth_list)
    for ind,e in enumerate(ground_copy_truth_list):
        ground_copy_truth_list[ind][-3]=ast.unparse(ast.parse(ground_copy_truth_list[ind][-3]))

    for ind, e in enumerate(new_python_code_list):
        new_python_code_list[ind][-3]=ast.unparse(ast.parse(new_python_code_list[ind][-3]))

    ground_pre_list = [e[:-1] for e in ground_copy_truth_list]


    ground_pre_list_copy=copy.deepcopy(ground_pre_list)

    for ind, e in enumerate(new_python_code_list):
        # print("res1: ", ind, e,e)
        if e[:-1] in ground_pre_list:
            index = ground_pre_list.index(e[:-1])
            gd_refactor_code = ground_copy_truth_list[ground_pre_list_copy.index(e[:-1])][-1]
            # print(gd_refactor_code)
            # predict_res.append(e)


            for ind_res,res1 in enumerate(gd_refactor_code):
                # print("res1: ", ind,ind_res,res1,e[-1])
                if res1.strip() == e[-1].strip():
                    e.append(gd_refactor_code)
                    e.append(1)
                    break
            else:
                # print("e[-1]: ",e[-1])
                refactor_wrong += 1
                e.append(gd_refactor_code)
                e.append(0)

            ground_pre_list.pop(index)
        else:
            e.append("Cannot refactor")
            e.append(2)
            print(">>>come here")
            # for k_i,k in enumerate(e[:-1]):
            #     print("k: ",k_i,k)
            # print("j: ", k_i,ground_copy_truth_list[0][k_i])
            find_wrong += 1
        predict_res.append(e)


    no_found_wrong = len(ground_pre_list)
    predict_res.append(["NOFOUND"])

    for ind, e in enumerate(ground_pre_list):
        predict_res.append(e + [0])
    print(find_wrong,refactor_wrong, no_found_wrong)
    return predict_res
if __name__ == '__main__':
    idiom = "list_comprehension"
    save_complicated_code_dir_root = util.data_root + "chatgpt/NonIdiomatic/"
    # save_complicated_code_dir_root = util.data_root + "NonIdiomatic/find_code_snippets/"
    save_complicated_code_dir = save_complicated_code_dir_root + "sample_methods/"
    file_name="which_statement_will_execute_4_improve_2_all_new_get_acc_new_add_continue_instr3_add_new_found_new.csv"
    # util.save_pkl(save_complicated_code_dir_root + idiom + "/", "ridiom_set_comprehension", ground_truth_list)
    # util.save_pkl(save_complicated_code_dir_root + idiom + "/", "gpt_result_set_comprehension", format_new_python_list)
    # util.save_pkl(save_complicated_code_dir_root + idiom + "/", "set_comprehension_bench",res)
    # util.save_pkl(save_complicated_code_dir_root + idiom + "/", "set_comprehension_bench",res)
    # util.save_pkl(save_complicated_code_dir_root + idiom + "/", "ridiom_set_comprehension", ground_truth_list)
    # util.save_pkl(save_complicated_code_dir_root + idiom + "/", "gpt_result_set_comprehension", format_new_python_list)

    # util.save_pkl(save_complicated_code_dir_root + idiom + "/", "ridiom_set_comprehension", ground_truth_list)
    # util.save_pkl(save_complicated_code_dir_root + idiom + "/", "gpt_result_set_comprehension", format_new_python_list)

    all_res = util.load_pkl(save_complicated_code_dir_root + idiom + "/", "set_comprehension_bench")
    # ridiom_res = util.load_pkl(save_complicated_code_dir, "sample_methods_" + idiom)
    ridiom_code_list=util.load_pkl(save_complicated_code_dir_root + idiom + "/", "ridiom_" + idiom)
    # file_name="gpt_result_"+idiom
    # file_name="gpt_result_fine_tune_"+idiom
    # "gpt_result_from_def_stmt"
    file_name="gpt_result_from_def_stmt_sample"#"gpt_result_from_def_stmt"
    file_name="gpt_result_from_def_stmt_from_abstract_var_all"
    file_name="gpt_result_from_def_stmt_from_abstract_var_all_add_examp"
    file_name="gpt_result_from_def_stmt_from_abstract_var_all_add_examp_new"
    file_name="gpt_result_from_def_stmt_from_abstract_var_all_add_examp_new_filter_for"
    file_name="gpt_result_from_def_stmt_from_abstract_var_all_add_examp_new_filter_for"

    new_python_code_list=util.load_pkl(save_complicated_code_dir_root + idiom + "/",file_name)
    # new_python_code_list=util.load_pkl(save_complicated_code_dir_root + idiom + "/","gpt_result_"+idiom)
    new_python_code_list=[e[:8] for e in new_python_code_list]
    print("len of new_python_code_list:",len(new_python_code_list))
    print("len of new_python_code_list: ",len(new_python_code_list[0]))
    print("len of all_res: ",len(all_res))


    for ind,e in enumerate(new_python_code_list[29]):
        print("ind,e: ", ind,e)

    csv_res_list=get_eva_p_r(all_res, new_python_code_list)
    get_eva_p_r(all_res, ridiom_code_list)
    # acc_file_name="gpt_result_from_def_stmt_acc.csv"
    acc_file_name=file_name+"_acc.csv"#gpt_result_from_def_stmt_acc_all.csv"

    # util.save_csv(
    #     save_complicated_code_dir_root + idiom + "/" + acc_file_name,
    #     csv_res_list,
    #     ["repo_name", "file_path", "file_html", "class_name", "me_name", "me_code", "old_code", "chatGPT_code",
    #      "element_str",
    #      "slice_str", "truth_code"])
    # benchmarks = []


