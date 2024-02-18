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
    idiom = "assign_multiple_targets"
    save_complicated_code_dir_root = util.data_root + "chatgpt/NonIdiomatic/"
    # save_complicated_code_dir_root = util.data_root + "NonIdiomatic/find_code_snippets/"
    save_complicated_code_dir = save_complicated_code_dir_root + "sample_methods/"
    file_name="direct_refactor_from_blocks_no_dependinstr_improve_depdend_4_4_examp_all_get_acc"

    # save_complicated_code_dir_root + idiom + "/" + csv_file_name,
    benchmarks = []
    all_res = util.load_csv(save_complicated_code_dir_root + idiom + "/" +"utf_8_ass.csv")
    # util.save_pkl(save_complicated_code_dir_root + idiom + "/",
    #               "get_acc_res",
    #               csv_res_list)
    csv_res_list_pkl = util.load_pkl(save_complicated_code_dir_root + idiom + "/", file_name)

    # repo_name, old_path, file_html, class_name, me_name, method_code, old_code, refactor_code, *other = sample
    flag=0
    res=[]
    for ind_e,e in enumerate(all_res):
        if ind_e==0:
            continue
        # print("len(e): ",len(e))
        # print("e: ",e)
        # for ind_k,k in enumerate(e):
        #     print("k",ind_k,k)

        repo_name, old_path, file_html, class_name, me_name, method_code, old_code, chat_gpt_code,abstract_code, ridiom_code, acc, chatgpt_acc,ridiom_acc,real_acc,*other=e
        if "FOUND" in repo_name:
            flag=1
            continue
        try:
            repo_name, old_path, file_html, class_name, me_name, method_code, old_code, chat_gpt_code, abstract_code,ridiom_code,*other=csv_res_list_pkl[ind_e-1]
        except:
            repo_name, old_path, file_html, class_name, me_name, method_code, old_code, ridiom_code,*other=csv_res_list_pkl[ind_e-1]
        # if "t >= 0.0 and v <= 0.0 >= u" not in chat_gpt_code:
        #     continue
        # ridiom_acc, real_acc='1','1'

        # if not me_name:
        #     continue
        # if "for x in range(TEST_TIMEOUT)" in old_code:
        #     print(acc,real_acc,chatgpt_acc,ridiom_acc)

        acc,real_acc,chatgpt_acc,ridiom_acc=int(acc) if acc.isdigit() else int(acc) if acc=="-1" else None,int(real_acc) if real_acc.isdigit() else None, int(chatgpt_acc) if chatgpt_acc.isdigit() else None,int(ridiom_acc) if ridiom_acc.isdigit() else None
        # if "for event_item in user_dict[" in old_code:#for x in range(TEST_TIMEOUT)
        #     print(acc,real_acc,chatgpt_acc,ridiom_acc)
        if not flag:
            print("acc,real_acc,chatgpt_acc,ridiom_acc: ", ind_e, acc, chatgpt_acc, ridiom_acc, real_acc, ridiom_code)

            # print("acc: ",acc==1,acc=='1',len(e),e[9])
            if acc==1:
                # if real_acc==0:
                #     continue
                # if "for event_item in user_dict[" in old_code:
                #     print("come here")
                res.append([repo_name, old_path, file_html, class_name, me_name, method_code, old_code,[chat_gpt_code,ridiom_code]])
            elif acc==-1:
                if chatgpt_acc == 1:
                    res.append([repo_name, old_path, file_html, class_name, me_name, method_code, old_code,[chat_gpt_code]])
                elif ridiom_acc == 0 and chatgpt_acc == 0 and real_acc == 1:
                        res.append([repo_name, old_path, file_html, class_name, me_name, method_code, old_code,
                                    ["it can be refactored"]])

            elif acc==0:
                if ridiom_acc == 0 and chatgpt_acc == 0 and real_acc == 1:
                    res.append([repo_name, old_path, file_html, class_name, me_name, method_code, old_code,
                                ["it can be refactored"]])
                elif chatgpt_acc==None:
                    print("come herechatgpt_acc==None: ", ind_e, acc, real_acc, chatgpt_acc, ridiom_acc)
                    res.append([repo_name, old_path, file_html, class_name, me_name, method_code, old_code,
                                [ridiom_code]])
                elif chatgpt_acc==1:
                    res.append([repo_name, old_path, file_html, class_name, me_name, method_code, old_code,[chat_gpt_code,ridiom_code]])
                elif ridiom_acc==1:
                    res.append([repo_name, old_path, file_html, class_name, me_name, method_code, old_code,[chat_gpt_code]])
                # elif ridiom_acc == 0 and chatgpt_acc == 0 and real_acc == 1:
                #     res.append([repo_name, old_path, file_html, class_name, me_name, method_code, old_code,
                #                 ["it can be refactored"]])
            # elif chatgpt_acc==1:
            #     if ridiom_acc==0:
            #         # print("come here ridiom_acc==0: ", ridiom_acc)
            #
            #         res.append([repo_name, old_path, file_html, class_name, me_name, method_code, old_code,[chat_gpt_code]])
            #     else:
            #         res.append([repo_name, old_path, file_html, class_name, me_name, method_code, old_code,[chat_gpt_code,ridiom_code]])
            # elif chatgpt_acc==0 and ridiom_acc!=0:
            #     res.append([repo_name, old_path, file_html, class_name, me_name, method_code, old_code,
            #                 [ridiom_code]])
            # elif ridiom_acc==0 and chatgpt_acc==0 and real_acc==1:
            #     res.append([repo_name, old_path, file_html, class_name, me_name, method_code, old_code,
            #                 ["it can be refactored"]])
            else:
                print("come here: ",ind_e,acc,real_acc,chatgpt_acc,ridiom_acc)
        else:
            print("acc,real_acc,chatgpt_acc,ridiom_acc: ", ind_e, acc, chatgpt_acc, ridiom_acc, real_acc, ridiom_code)

            pass
            res.append([repo_name, old_path, file_html, class_name, me_name, method_code, old_code,
                        [chat_gpt_code]])
    print("len of benchmark: ",len(csv_res_list_pkl),len(res))
    # util.save_pkl(save_complicated_code_dir_root + idiom + "/", "loop_else_bench",res)
    util.save_pkl(save_complicated_code_dir_root + idiom + "/", "ass_multi_tar_bench_new",res)