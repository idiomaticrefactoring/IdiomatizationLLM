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
        if e[:-1] in ground_pre_list:
            index = ground_pre_list.index(e[:-1])
            gd_refactor_code = ground_copy_truth_list[ground_pre_list_copy.index(e[:-1])][-1]
            # print(gd_refactor_code)

            for ind_res,res1 in enumerate(gd_refactor_code):
                # print("res1: ", ind_res,res1)
                if res1.strip() == e[-1].strip():
                    break
            else:
                # print("e[-1]: ",e[-1])
                refactor_wrong += 1
            ground_pre_list.pop(index)
        else:
            print(">>>find_wrong: ", e[6], "\n", e[7])

            # print(">>>come here: ",e[-2])
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
    idiom = "loop_else"
    idiom = "truth value testing"
    idiom = "_".join(idiom.split(" "))
    save_complicated_code_dir_root = util.data_root + "chatgpt/NonIdiomatic/"
    # save_complicated_code_dir_root = util.data_root + "NonIdiomatic/find_code_snippets/"
    save_complicated_code_dir = save_complicated_code_dir_root + "sample_methods/"

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
    all_res = util.load_pkl(save_complicated_code_dir_root + idiom + "/", "truth_test_bench_new")
    ridiom_code_list = util.load_pkl(save_complicated_code_dir_root + idiom + "/", "ridiom_truth_test")
    new_all_code_list = util.load_pkl(save_complicated_code_dir_root + idiom + "/", "chatgpt_refactor_new_python_code_list")
    for ind,e in enumerate(new_all_code_list[0]):
        print("ind,e: ",ind,e)
    # ridiom_code_list=get_ridiom_res(ridiom_res)
    file_name="gpt_result_"+idiom
    # file_name="gpt_result_fine_tune_"+idiom
    # new_python_code_list=util.load_pkl(save_complicated_code_dir_root + idiom + "/","gpt_result_"+idiom)
    new_python_code_list=[e[:8] for e in new_all_code_list]
    print("len: ",len(method_code_list),len(all_res),len(ridiom_code_list),len(new_python_code_list))
    for e in all_res:
        # print("e[-1]: ",e[-1])
        e[-1]=[ast.unparse(ast.parse(k)) for k in e[-1] ]
        # e[-2] = ast.unparse(ast.parse(e[-2]))
        # e[-3] = ast.unparse(ast.parse(e[-3]))
    # get_eva_p_r(all_res, new_python_code_list)
    get_eva_p_r(all_res, ridiom_code_list)

    # benchmarks = []


