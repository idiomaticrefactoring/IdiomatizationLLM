import os, sys
import struct
import traceback

import util_rewrite

code_dir = "/".join(os.path.abspath(__file__).split("/")[:-2]) + "/"
print("code path: ", code_dir)
sys.path.append(code_dir)
import chatgpt_util, random, chat_gpt_ast_util
import openai, tiktoken, ast, util, util_rewrite,baseline_util
import ast,copy
def get_eva_p_r(ground_truth_list,new_python_code_list):
    # repo_name, old_path, file_html, class_name, me_name, method_code, old_code, refactor_code, *other = sample
    no_found_wrong = 0
    p_r_res=[]
    find_wrong=0
    refactor_wrong = 0
    correct=0
    # for e in ground_truth_list:
    #     e[-1]=ast.unparse(ast.parse(e[-1]))
    #     e[-2] = ast.unparse(ast.parse(e[-2]))
    # ground_truth_list=[ for e in ground_truth_list]
    ground_copy_truth_list=copy.deepcopy(ground_truth_list)
    ground_copy_truth_list_2=copy.deepcopy(ground_truth_list)

    ground_pre_list = [e[:-1] for e in ground_copy_truth_list]
    ground_pre_list_copy=copy.deepcopy(ground_pre_list)

    for ind, e in enumerate(new_python_code_list):
        # if "t >= 0.0 and v <= 0.0 >= u" not in e[-1]:
        #     continue
        if e[:-1] in ground_pre_list:
            all_refac_code=[]
            indices = [i for i, x in enumerate(ground_pre_list) if x == e[:-1]]
            for index in indices:
                # index = ground_pre_list.index(e[:-1])
                copy_index=[i for i, x in enumerate(ground_pre_list_copy) if x == e[:-1]]
                gd_refactor_code=[]
                for i_copy in copy_index:
                    gd_refactor_code.extend( ground_copy_truth_list[i_copy][-1])
                    all_refac_code.extend(ground_copy_truth_list[i_copy][-1])
                # gd_refactor_code = ground_copy_truth_list[index][-1]
                # gd_refactor_code = ground_copy_truth_list[ground_pre_list_copy.index(e[:-1])][-1]

                for ind_res,res1 in enumerate(gd_refactor_code):
                    # print("res1: ", ind_res,res1)
                    if res1.strip() == e[-1].strip():
                        ground_pre_list.pop(index)
                        ground_copy_truth_list_2.pop(index)
                        p_r_res.append(e+[res1]+[1])
                        correct+=1
                        break
                else:
                    continue
                    # print(gd_refactor_code)
                    # print("e[-1]: ",e[-2],e[-1])
                    # refactor_wrong += 1
                break
            else:
                p_r_res.append(e + [all_refac_code]+[-1])
                refactor_wrong += 1
        else:
            p_r_res.append(e + ['find_wrong'] + [2])
            # print(">>>come here: ",e[-2])
            # print("refactor code: ",e[-1])
            # for k_i,k in enumerate(e[:]):
            #     print("k: ",k_i,k)
            #     print("j: ", k_i,ground_copy_truth_list[0][k_i])
            find_wrong += 1
    no_found_wrong = len(ground_pre_list)
    for code_e in ground_copy_truth_list_2:
        p_r_res.append(code_e + ['no_found',0])

        # print("code_e: ",code_e)
    #     for i,e in enumerate(code_e):
    #         print("i,e: ", i,e)

    print("correct,find_wrong,refactor_wrong, no_found_wrong:",correct,find_wrong,refactor_wrong, no_found_wrong,len(ground_copy_truth_list),len(ground_copy_truth_list_2))
    return  p_r_res

def func_eval(idiom,samples,all_res):
    length_is_larger=0
    csv_res = []
    for ind, sample in enumerate(samples):
        # for i, s in enumerate(sample):
        #     print("i,sample: ", i, s)
        # break
        if "fstring" in idiom:
            repo_name, file_html,old_path, class_name, method_code,_, response = sample
            me_name=""
        else:
            repo_name, file_html,old_path, class_name, me_name, method_code,_, response = sample

        # print(">>>>class_name:",repo_name, old_path, file_html, "xx",class_name,"tt",me_name,"method_code",method_code)
        # print(">>>>>>>>content: ",response)
        try:
            content = response["choices"][0]["message"]["content"]
        except:
            length_is_larger+=1
            continue
        # print(">>>>>>>>content: ",content)
        # method_code=ast.unparse(ast.parse(method_code))

        flag_ref, refactored_code_list = baseline_util.parse_refactor_code(content)
        if flag_ref:
            for old_code,new_code in refactored_code_list:
                if "comprehension" in idiom:
                    ass,for_code=old_code.split("\n")[0],"\n".join(old_code.split("\n")[1:])
                    if "= []" in ass:
                        old_code=for_code.strip()
                if "else" in idiom:
                    ass, for_code = old_code.split("\n")[0], "\n".join(old_code.split("\n")[1:])
                    if "= " in old_code:
                        old_code = for_code.strip()
                if "truth" in idiom:
                    if old_code.startswith("if "):
                        old_code=old_code[3:]
                        if old_code.endswith(":"):
                            old_code =old_code[:-1]
                            new_code = new_code[3:-1]
                        else:
                            new_code = new_code[3:]

                print("refactored_code: ", old_code,"\n>>>>>\n",new_code)
                try:
                    csv_res.append(
                        [repo_name, file_html, old_path, class_name, me_name,ast.unparse(ast.parse(method_code)), old_code,
                         ast.unparse(ast.parse(new_code)), 1])
                except:
                    csv_res.append(
                        [repo_name, file_html, old_path, class_name, me_name, ast.unparse(ast.parse(method_code)),
                         old_code,
                         new_code, 1])
            # print(">>>>for_code:",for_code)
            # print(">>>>response:",response)
            # print(">>>>refactored_code:",flag_ref,refactored_code)
            # break
        # else:
        #     csv_res.append([repo_name, file_html, old_path, class_name, ast.unparse(ast.parse(method_code)),content,
        #                     refactored_code_list, 0])

        # reponse_list.append(
        #     [*other, for_code])
        # reponse_list[-1].extend([[msg], response])
        # new_code, method_code, _, response = sample
    print("len of csv_res,length_is_larger: ", len(csv_res),length_is_larger)
    # util.save_csv(
    #     save_complicated_code_dir_root + idiom + "/" + file_name + "_new.csv",
    #     csv_res,
    #     ["repo_name", "file_path", "file_html", "class_name", "me_code", "old_code", "new_code", "bool_code",
    #      "chatGPT_code", "if_correct", "reversed_code", "non_replace_var_refactored_code", "refactored_code", "acc",
    #      "instruction", "sys_msg", "exam_msg", "user_msg"])

    # file_name = "gpt_fstring_res"  # "direct_refactor_with_stmt_instr_sample_methods"
    #
    util.save_pkl(save_complicated_code_dir_root+ "baseline/",
                  "gpt_res_direct_"+idiom,
                  csv_res)

    for res in all_res:
        # print(">>>res: ",res[5])
        try:
            res[5] = ast.unparse(ast.parse(res[5]))
        except:
            pass
        # try:
        #     res[5]=ast.unparse(ast.parse(res[5]))
        # except:
        #     pass
        # print(">>>res: ",res[5])
        try:
            res[6] = ast.unparse(ast.parse(res[6]))
        except:
            pass
        for ind, e in enumerate(res[-1]):
            try:
                res[-1][ind] = ast.unparse(ast.parse(e))
            except:
                traceback.print_exc()
                pass
        # for ind,e in enumerate(res):
        #     print(">>>>>ind,e: ",ind,e)
        # break
    csv_res=[e[:-1] for e in csv_res]
    for res in csv_res:
        try:
            res[5]=ast.unparse(ast.parse(res[5]))
        except:
            pass
        try:
            res[6] = ast.unparse(ast.parse(res[6]))
        except:
            pass
        try:
            res[7] = ast.unparse(ast.parse(res[7]))
        except:
            pass


        # for ind,e in enumerate(res):
        #     print(">>>>>ind,e: ",ind,e)
        # break
    p_r_res=get_eva_p_r(all_res,csv_res)
    file_name="p_r_res_"+idiom
    util.save_csv(
            save_complicated_code_dir_root + "baseline/"+ file_name + "_new.csv",
            p_r_res,
            ["repo_name", "file_path", "file_html", "class_name", "me_name","me_code", "old_code", "new_code", "gd_truth_code",
             "acc"])
    print("len of each ele: ",len(all_res),len(csv_res),len(all_res[0]),len(csv_res[0]))

def func_eval_new_idiom(idiom,samples,all_res):
    length_is_larger=0
    csv_res = []
    for ind, sample in enumerate(samples):
        # for i, s in enumerate(sample):
        #     print("i,sample: ", i, s)
        # break
        # if "fstring" in idiom:
        repo_name, file_html,old_path, class_name, method_code,_, response = sample
        # else:
        #     repo_name, file_html,old_path, class_name, me_name, method_code,_, response = sample

        # print(">>>>class_name:",repo_name, old_path, file_html, "xx",class_name,"tt",me_name,"method_code",method_code)
        # print(">>>>>>>>content: ",response)
        try:
            content = response["choices"][0]["message"]["content"]
        except:
            length_is_larger+=1
            continue
        # print(">>>>>>>>content: ",content)
        # method_code=ast.unparse(ast.parse(method_code))

        flag_ref, refactored_code_list = baseline_util.parse_refactor_code(content)
        if flag_ref:
            for old_code,new_code in refactored_code_list:
                if "comprehension" in idiom:
                    ass,for_code=old_code.split("\n")[0],"\n".join(old_code.split("\n")[1:])
                    if "= []" in ass:
                        old_code=for_code.strip()
                if "else" in idiom:
                    ass, for_code = old_code.split("\n")[0], "\n".join(old_code.split("\n")[1:])
                    if "= " in old_code:
                        old_code = for_code.strip()
                if "truth" in idiom:
                    if old_code.startswith("if "):
                        old_code=old_code[3:]
                        if old_code.endswith(":"):
                            old_code =old_code[:-1]
                            new_code = new_code[3:-1]
                        else:
                            new_code = new_code[3:]

                print("refactored_code: ", old_code,"\n>>>>>\n",new_code)
                try:
                    csv_res.append(
                        [repo_name, file_html, old_path, class_name,ast.unparse(ast.parse(method_code)), old_code,
                         ast.unparse(ast.parse(new_code)), 1])
                except:
                    csv_res.append(
                        [repo_name, file_html, old_path, class_name, ast.unparse(ast.parse(method_code)),
                         old_code,
                         new_code, 1])
            # print(">>>>for_code:",for_code)
            # print(">>>>response:",response)
            # print(">>>>refactored_code:",flag_ref,refactored_code)
            # break
        # else:
        #     csv_res.append([repo_name, file_html, old_path, class_name, ast.unparse(ast.parse(method_code)),content,
        #                     refactored_code_list, 0])

        # reponse_list.append(
        #     [*other, for_code])
        # reponse_list[-1].extend([[msg], response])
        # new_code, method_code, _, response = sample
    print("len of csv_res,length_is_larger: ", len(csv_res),length_is_larger)
    # util.save_csv(
    #     save_complicated_code_dir_root + idiom + "/" + file_name + "_new.csv",
    #     csv_res,
    #     ["repo_name", "file_path", "file_html", "class_name", "me_code", "old_code", "new_code", "bool_code",
    #      "chatGPT_code", "if_correct", "reversed_code", "non_replace_var_refactored_code", "refactored_code", "acc",
    #      "instruction", "sys_msg", "exam_msg", "user_msg"])

    # file_name = "gpt_fstring_res"  # "direct_refactor_with_stmt_instr_sample_methods"
    #
    # util.save_pkl(save_complicated_code_dir_root+ "baseline/",
    #               "gpt_res_direct_"+idiom,
    #               csv_res)

    for res in all_res:
        # print(">>>res: ",res[5])
        try:
            res[4] = ast.unparse(ast.parse(res[4]))
        except:
            pass
        # try:
        #     res[5]=ast.unparse(ast.parse(res[5]))
        # except:
        #     pass
        # print(">>>res: ",res[5])
        try:
            res[5] = ast.unparse(ast.parse(res[5]))
        except:
            pass
        try:
            res[-1] =[ast.unparse(ast.parse(res[-1]))]
        except:
            res[-1] = [res[-1]]
        # print("res[-1]: ",[ast.unparse(ast.parse(res[-1]))])
        # for ind, e in enumerate(res[-1]):
        #     try:
        #         res[-1][ind] = ast.unparse(ast.parse(e))
        #     except:
        #         traceback.print_exc()
        #         pass
        # for ind,e in enumerate(res):
        #     print(">>>>>ind,e: ",ind,e)
        # break
    csv_res=[e[:-1] for e in csv_res]
    for res in csv_res:
        try:
            res[4]=ast.unparse(ast.parse(res[4]))
        except:
            pass
        try:
            res[5] = ast.unparse(ast.parse(res[5]))
        except:
            pass
        try:
            res[6] = ast.unparse(ast.parse(res[6]))
        except:
            pass


        # for ind,e in enumerate(res):
        #     print(">>>>>ind,e: ",ind,e)
        # break
    p_r_res=get_eva_p_r(all_res,csv_res)
    file_name="p_r_res_"+idiom
    util.save_csv(
            save_complicated_code_dir_root + "baseline/"+ file_name + "_new.csv",
            p_r_res,
            ["repo_name", "file_path", "file_html", "class_name", "me_name","me_code", "old_code", "new_code", "gd_truth_code",
             "acc"])
    print("len of each ele: ",len(all_res),len(csv_res),len(all_res[0]),len(csv_res[0]))

if __name__ == '__main__':
    save_complicated_code_dir_root = util.data_root + "chatgpt/NonIdiomatic/"
    idiom = "assign_multiple_targets"
    file_name = "baseline"+idiom
    gd_file_name="ass_multi_tar_bench_new"

    idiom = "list_comprehension"
    file_name = "baseline_list_comprehension"
    gd_file_name="list_comprehension_bench_from_code_gen"

    idiom = "loop_else"
    file_name = "baseline"+idiom
    gd_file_name="loop_else_bench_new"
    # all_res = util.load_pkl(save_complicated_code_dir_root + idiom + "/", "loop_else_bench_new")
    idiom = "chain_comparison"
    file_name = "baseline_"+idiom
    gd_file_name="chain_compare_bench_new"

    idiom = "truth value testing"
    idiom = "_".join(idiom.split(" "))
    file_name = "baseline"+idiom
    gd_file_name="truth_test_bench_new"

    idiom = "call_star"
    file_name = "baseline_"+idiom
    gd_file_name="call_star_bench_new"

    idiom = "for multi targets"
    idiom = "_".join(idiom.split(" "))
    file_name = "baseline"+idiom
    gd_file_name="for_multi_tar_bench_new"
    samples = util.load_pkl(save_complicated_code_dir_root + "baseline/", file_name)  # methods_sample
    print("samples: ", len(samples), len(samples[0]), samples[0])
    all_res = util.load_pkl(save_complicated_code_dir_root + idiom + "/", gd_file_name)
    # func_eval(idiom, samples, all_res)

    idiom = "fstring"
    file_name = "baseline_fstring_stmt"
    gd_file_name="gpt_fstring_res"#"direct_refactor_with_stmt_instr_sample_methods"
    csv_file_name="p_r_res_" + idiom
    res=[]
    all_res = util.load_csv(save_complicated_code_dir_root + idiom + "/" + csv_file_name+".csv")
    for ind_e,e in enumerate(all_res):
        # if ind_e==0:
        #     continue
        print("len(e): ",len(e))
        print("e: ",e)
        for ind_k,k in enumerate(e):
            print("k",ind_k,k)

        repo_name, old_path, file_html, class_name, method_code, old_code, baseline_code, ourmethod_code, acc, baseline_acc,ourmethod_acc, real_acc,*other=e
        # repo_name, old_path, file_html, class_name, me_name, method_code, old_code, chat_gpt_code, ridiom_code,*other=csv_res_list_pkl[ind_e-1]
        # ridiom_acc, real_acc='1','1'
        # if "FOUND" in repo_name:
        #     flag=1
        # if not me_name:
        #     continue
        # if "for x in range(TEST_TIMEOUT)" in old_code:
        #     print(acc,real_acc,chatgpt_acc,ridiom_acc)

        acc,baseline_acc,ourmethod_acc,real_acc=int(acc) if acc.isdigit() else None,int(baseline_acc) if baseline_acc.isdigit() else None, int(ourmethod_acc) if ourmethod_acc.isdigit() else None,int(real_acc) if real_acc.isdigit() else None
        # if "for event_item in user_dict[" in old_code:#for x in range(TEST_TIMEOUT)
        #     print(acc,real_acc,chatgpt_acc,ridiom_acc)
        if acc==1:
            if real_acc==0:
                continue
            if baseline_acc==0:
                res.append([repo_name, old_path, file_html, class_name,method_code, old_code,[chat_gpt_code]])

            elif ourmethod_acc==0:
                res.append([repo_name, old_path, file_html, class_name, method_code, old_code,[chat_gpt_code]])

            else:
                res.append([repo_name, old_path, file_html, class_name, method_code, old_code,[chat_gpt_code]])



        # if not flag:
        #     # print("acc: ",acc==1,acc=='1',len(e),e[9])
        #     if acc==1:
        #         if real_acc==0:
        #             continue
        #         if "for event_item in user_dict[" in old_code:
        #             print("come here")
        #         res.append([repo_name, old_path, file_html, class_name, me_name, method_code, old_code,[chat_gpt_code]])
        #     elif chatgpt_acc==1:
        #         if ridiom_acc!=1:
        #             res.append([repo_name, old_path, file_html, class_name, me_name, method_code, old_code,[chat_gpt_code]])
        #         else:
        #             res.append([repo_name, old_path, file_html, class_name, me_name, method_code, old_code,[chat_gpt_code,ridiom_code]])
        #
        #     # elif ridiom_acc==1:
        #     #     res.append([repo_name, old_path, file_html, class_name, me_name, method_code, old_code,
        #     #                 [ridiom_code]])
        # else:
        #     pass
            # res.append([repo_name, old_path, file_html, class_name, me_name, method_code, old_code,
            #             [chat_gpt_code]])
    print("len of benchmark: ",len(res))
    # util.save_pkl(save_complicated_code_dir_root + idiom + "/", "loop_else_bench",res)
    util.save_pkl(save_complicated_code_dir_root + idiom + "/", "truth_test_bench_new",res)
    # idiom = "enumerate"
    # file_name = "baseline_enumerate_stmt_with_for_stmt"
    # gd_file_name="our_method_res_"+idiom
    # samples = util.load_pkl(save_complicated_code_dir_root+ "baseline/", file_name)  # methods_sample
    # print("samples: ",len(samples),len(samples[0]),samples[0])
    # all_res = util.load_pkl(save_complicated_code_dir_root + idiom + "/", gd_file_name)
    #
    # if idiom=="fstring":
    #     all_res=[e[:-1] for e in all_res]
    # print("all_res: ",len(all_res),len(all_res[0]),all_res[0])
    # func_eval_new_idiom(idiom, samples, all_res)
    # # print("one example: ",all_res[0][5:])
    #


