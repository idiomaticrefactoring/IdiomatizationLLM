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
            repo_name, old_path, file_html, class_name, me_name, old_list, new_tree, \
            old_code, new_code, method_code = code
            # print("for_node_new_else: ",ast.unparse(for_node_new_else))
            # print("for_node_old: ",ast.unparse(for_node_old))
            # print("if_node: ",ast.unparse(if_node))

            # repo_name, old_path, file_html, class_name,me_name, old_list, new_tree,\
            #     old_code,new_code, method_code=code
            # break
            *other, old_list, new_tree, \
            old_code, new_code, method_code = code
            try:
                ele = [repo_name, old_path, file_html, class_name, me_name, method_code,ast.unparse(ast.parse(old_code)), ast.unparse(ast.parse(new_code))]
            except:
                continue
            ground_truth_list.append(ele)
    return ground_truth_list
def get_eva_p_r(ground_truth_list,new_python_code_list):
    # repo_name, old_path, file_html, class_name, me_name, method_code, old_code, refactor_code, *other = sample
    no_found_wrong = 0
    find_wrong=0
    refactor_wrong = 0
    ground_copy_truth_list=copy.deepcopy(ground_truth_list)
    ground_pre_list = [e[:-1] for e in ground_copy_truth_list]
    ground_pre_list_copy=copy.deepcopy(ground_pre_list)

    for ind, e in enumerate(new_python_code_list):
        # if "t >= 0.0 and v <= 0.0 >= u" not in e[-1]:
        #     continue
        if e[:-1] in ground_pre_list:
            indices = [i for i, x in enumerate(ground_pre_list) if x == e[:-1]]
            for index in indices:
                # index = ground_pre_list.index(e[:-1])
                copy_index=[i for i, x in enumerate(ground_pre_list_copy) if x == e[:-1]]
                gd_refactor_code=[]
                for i_copy in copy_index:
                    gd_refactor_code.extend( ground_copy_truth_list[i_copy][-1])
                # gd_refactor_code = ground_copy_truth_list[index][-1]
                # gd_refactor_code = ground_copy_truth_list[ground_pre_list_copy.index(e[:-1])][-1]

                for ind_res,res1 in enumerate(gd_refactor_code):
                    # print("res1: ", ind_res,res1)
                    if res1.strip() == e[-1].strip():
                        break
                else:
                    continue
                    # print(gd_refactor_code)
                    # print("e[-1]: ",e[-2],e[-1])
                    # refactor_wrong += 1
                break
            else:
                refactor_wrong += 1
                print(">>>come here: ", e[6],"\n",e[7])
            ground_pre_list.pop(index)
        else:
            # print(">>>come here: ",e[:-1])
            # print("refactor code: ",e[-1])
            # for k_i,k in enumerate(e[:]):
            #     print("k: ",k_i,k)
            #     print("j: ", k_i,ground_copy_truth_list[0][k_i])
            find_wrong += 1
    no_found_wrong = len(ground_pre_list)
    # for code_e in ground_pre_list:
    #     # print("code_e: ",code_e)
    #     for i,e in enumerate(code_e):
    #         print("i,e: ", i,e)

    print(find_wrong,refactor_wrong, no_found_wrong)
if __name__ == '__main__':
    idiom = "chain comparison"
    idiom = "_".join(idiom.split(" "))

    save_complicated_code_dir_root = util.data_root + "chatgpt/NonIdiomatic/"
    # save_complicated_code_dir_root = util.data_root + "NonIdiomatic/find_code_snippets/"
    save_complicated_code_dir = save_complicated_code_dir_root + "sample_methods/"
    file_name="which_statement_will_execute_4_improve_2_all_new_get_acc_new_add_continue_instr3_add_new_found_new.csv"
    save_file_name="rewrite_instr_from_code_generation"
    method_code_list = []
    samples = util.load_pkl(save_complicated_code_dir, "sample_methods_" + idiom)

    for ind_sampl, sample_method in enumerate(samples):
        for code in sample_method:
            *other, old_list, new_tree, \
            old_code, new_code, method_code = code
            method_code_list.append([*other, old_list, new_tree, old_code, new_code, method_code])
            break

    # util.save_pkl(save_complicated_code_dir_root + idiom + "/",
    #               "chatgpt_refactor_new_python_code_list",
    #               reponse_list)
    # util.save_pkl(save_complicated_code_dir_root + idiom + "/",
    #               "ridiom_truth_test",
    #               reponse_list)
# reponse_list.append([me_code, old_code, *other, real_compare_value.strip(), method_code])
#     util.save_pkl(save_complicated_code_dir_root + idiom + "/", "truth_test_bench_new",res)
    all_res = util.load_pkl(save_complicated_code_dir_root + idiom + "/", "chain_compare_bench_new")
    ridiom_code_list = util.load_pkl(save_complicated_code_dir_root + idiom + "/", "ridiom_res_"+idiom)
    new_all_code_list = util.load_pkl(save_complicated_code_dir_root + idiom + "/", "gpt_res_"+idiom)
    for ind,e in enumerate(new_all_code_list[0]):
        print("ind,e: ",ind,e)
    # ridiom_code_list=get_ridiom_res(ridiom_res)
    file_name="gpt_result_"+idiom
    # file_name="gpt_result_fine_tune_"+idiom
    # new_python_code_list=util.load_pkl(save_complicated_code_dir_root + idiom + "/","gpt_result_"+idiom)
    new_python_code_list=[e[:8] for e in new_all_code_list]
    print("len: ",len(method_code_list),len(all_res),len(ridiom_code_list),len(new_python_code_list))
    # for e in all_res:
    #     # print("e[-1]: ",e[-1])
    #     try:
    #         e[-1]=[ast.unparse(ast.parse(k)) for k in e[-1] ]
    #     except:
    #         continue
        # e[-2] = ast.unparse(ast.parse(e[-2]))
        # e[-3] = ast.unparse(ast.parse(e[-3]))
    # get_eva_p_r(all_res, new_python_code_list)
    get_eva_p_r(all_res, ridiom_code_list)

    # benchmarks = []


