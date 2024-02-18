import copy
import os,sys
import struct
import traceback

import util_rewrite

code_dir = "/".join(os.path.abspath(__file__).split("/")[:-2]) + "/"
print("code path: ",code_dir)
sys.path.append(code_dir)
import chatgpt_util,random
import openai, tiktoken,ast,util
import ast
import extract_boolop_and
import chain_comparison_util,chain_compare_instr
def get_acc(samples,new_python_code_list,whether_emptyset_list=None):
    offset=0#-2
    ground_truth_list=[]
    for ind_sampl, sample_method in enumerate(samples):
        for code in sample_method:
            repo_name, old_path, file_html, class_name,me_name, old_list, new_tree,\
                old_code,new_code, method_code=code
            # break
            *other, old_list, new_tree, \
            old_code, new_code, method_code = code
            ele = [repo_name, old_path, file_html, class_name, me_name, method_code, old_code, new_code]
            ground_truth_list.append(ele)
            # print("ele: ",ele)

    ground_copy_truth_list=copy.deepcopy(ground_truth_list)
    ground_copy_truth_list=[e[offset:] for e in ground_copy_truth_list]
    predict_res=[]
    acc=0
    pre=0
    chat_gpt_res=[]
    for ind, e in enumerate(new_python_code_list):
        chat_gpt_res.append(e)
        # bool_code, old_code, repo_name, old_path, file_html, class_name,me_name,*other, new_code, method_code, info, response = sample
        # response_content = sample[-1]["choices"][0]["message"]["content"]
        #
        # refactor_code=refactor_code_list[ind]
        # print("refactor_code: ",ind,bool_code,refactor_code)
        # e=[repo_name, old_path, file_html, class_name,me_name,method_code,bool_code,refactor_code]
        ground_pre_list=[e[offset:-1] for e in ground_copy_truth_list]
        if e in ground_copy_truth_list:
                index = ground_copy_truth_list.index(e)
                e.append(ground_copy_truth_list[index][-1])
                e.append(1)
                ground_copy_truth_list.pop(index)
                acc+=1
                pre+=1

        elif e[:-1] in ground_pre_list:
            print("wrongly refactor")
            index=ground_pre_list.index(e[:-1])
            e.append(ground_copy_truth_list[index][-1])
            print(ground_copy_truth_list[index][-1])
            e.append(0)
            ground_copy_truth_list.pop(index)
        else:
            print("cannot refactor")
            e.append("Cannot refactor")
            e.append(2)
            acc += 1
        if whether_emptyset_list :
            predict_res.append(e+[whether_emptyset_list[ind][1]])
        else:
            predict_res.append(e)
    # for e in ground_copy_truth_list:
    #     print(">>>>>>>>unfound: ",e[:4])
    #     print(">>>>>>>>unfound: ",e[-2:])
    predict_res.append(["NOFOUND"])

    for ind, e in enumerate(ground_copy_truth_list):
        predict_res.append(e + [0])
        # print(e[6:])
    print("acc: ",acc,len(new_python_code_list),acc/len(new_python_code_list))
    print("precision: ",pre,len(ground_truth_list),pre/len(ground_truth_list))

    return predict_res,ground_truth_list,chat_gpt_res
#rewrite_code_from_reversed_abstract_find_same_operand_2_improve.py
if __name__ == '__main__':
    idiom = "chain comparison"
    idiom = "_".join(idiom.split(" "))
    save_complicated_code_dir_root = util.data_root + "chatgpt/NonIdiomatic/"
    # save_complicated_code_dir_root = util.data_root + "NonIdiomatic/find_code_snippets/"
    save_complicated_code_dir = save_complicated_code_dir_root + "sample_methods/"
    samples = util.load_pkl(save_complicated_code_dir, "sample_methods_" + idiom)

    file_name = "reversed_comparison_by_knowledge_from_abstract_find_same_operand_2_improve"  # "replace_two_comparison_with_replace_code_by_abstract_instr5_no_repeat"
    # "replace_two_comparison_with_replace_code_by_abstract_instr5_reversed_change_one_example"
    # new_python_code_list = util.load_pkl(save_complicated_code_dir_root + idiom + "/",
    #                                      file_name)
    new_python_code_list = util.load_pkl(save_complicated_code_dir_root + "chain_comparison_bool_compare/",
                                         file_name)

    abstract_file_name = "abstract_boolop_value_instr_no_explain_no_repeat"  # "abstract_boolop_value_instr_no_explain"
    abstract_code_list = util.load_pkl(save_complicated_code_dir_root + idiom + "/",
                                       abstract_file_name)
    file_name = "reversed_comparison_by_knowledge_from_abstract_find_same_operand_2_improve"#"reversed_comparison_by_knowledge_from_abstract_instr5_find_comparison_kg"
    # "reversed_comparison_by_knowledge_from_abstract_instr5_find_comparison_kg"#"find_comparison_add_kg_from_abstract_instr_5"
    save_file_name="replace_abstract_instr5_with_real_var_no_repeat_new_instr"#"replace_abstract_instr5_with_real_var_no_repeat"#"replace_abstract_instr5_with_real_var"
    response_list = []
    offset = 0  # 19#49#0#49#10
    for ind, e in enumerate(new_python_code_list[offset:]):
        dict_map, bool_code, old_code, real_comparison_1, real_comparison_2, comparison_1, comparison_2, repo_name,\
             old_path, file_html, class_name, me_name, method_code, flag_can_refactor,flag_total_string, *other=e
        if "y_int < h_img" not in bool_code: #name[-2:] != '__'
            continue

        print("dict_map: ",dict_map)
        # if "i == 1 and (not self._all_tone_three(sub)) and (finals_list[i][0][-1] == '3') and (finals_list[0][-1][-1] == '3')" not in bool_code:
        #     continue
        # print("bool_code: ",bool_code,flag_total_string,flag_can_refactor)
        if flag_can_refactor:
            def get_compare_node(code):
                for e in ast.walk(ast.parse(code)):
                    if isinstance(e, ast.Compare):
                        return e


            operands_1 = [ast.unparse(e) for e in
                          chain_compare_instr.get_compare_operands(get_compare_node(comparison_1))]
            operands_2 = [ast.unparse(e) for e in
                          chain_compare_instr.get_compare_operands(get_compare_node(comparison_2))]
            same_comparator = chain_compare_instr.has_common_elements(operands_1, operands_2)[0].strip()
            new_python_code = util_rewrite.remove("and " + same_comparator, flag_total_string)

            for key in dict_map:
                new_python_code=util_rewrite.replace(key.strip(), dict_map[key].strip(),new_python_code)
            print("new_python_code: ",new_python_code)
            new_bool_code = util_rewrite.remove(real_comparison_1 + " and", bool_code)

            if new_bool_code!=bool_code:
                new_bool_code= util_rewrite.replace_first_occur(real_comparison_2, new_python_code,new_bool_code)
            else:
                new_bool_code = util_rewrite.remove("and " + real_comparison_1, bool_code)

                new_bool_code= util_rewrite.replace_first_occur(real_comparison_2, new_python_code,new_bool_code)


            print("new_bool_code: ",new_bool_code)
            try:
                new_python_code=ast.unparse(ast.parse(new_bool_code.strip()))
            except:
                print("except: new_python_code: ", new_python_code)
                continue
            print(">>>>>new_python_code: ", new_python_code)
            response_list.append([repo_name, old_path, file_html, class_name, me_name,method_code, bool_code, new_python_code])

    save_file_name= "gpt_rewrite_code_new_from_abstract_find_same_operand_code"  # "reversed_comparison_by_knowledge_from_abstract_instr5_find_comparison_kg"#"find_comparison_add_kg_from_abstract_instr_5"
    #"replace_two_comparison_with_replace_code_by_abstract_instr5_reversed_change_one_example"  # "reversed_comparison_by_knowledge_from_abstract_instr5_find_comparison_kg"#"find_comparison_add_kg_from_abstract_instr_5"
    '''
    csv_res,ground_truth_list,chat_gpt_res=get_acc(samples, response_list, whether_emptyset_list=None)
    util.save_pkl(save_complicated_code_dir_root + idiom+"/",
                              save_file_name,
                              csv_res)
    util.save_pkl(save_complicated_code_dir_root + idiom + "/",
                  "ridiom_res_"+idiom,
                  ground_truth_list)
    util.save_pkl(save_complicated_code_dir_root + idiom + "/",
                  "gpt_res_"+idiom,
                  chat_gpt_res)
    '''
    # util.save_pkl(save_complicated_code_dir_root + "chain_comparison_bool_compare/",
    #                           "replace_two_comparison_with_replace_code_by_abstract_reversed",
    #                           response_list)
    # util.save_pkl(save_complicated_code_dir_root + "chain_comparison_bool_compare/",
    #                           "replace_two_comparison_with_replace_code_by_abstract_reversed_new_2",
    #                           response_list)
    # util.save_pkl(save_complicated_code_dir_root + "chain_comparison_bool_compare/",
    #                           "replace_two_comparison_with_replace_code_by_abstract_reversed_new_2_improve_instr_part_example",
    #                           response_list)
    # util.save_pkl(save_complicated_code_dir_root + "chain_comparison_bool_compare/",
    #                           "replace_two_comparison_with_replace_code_by_abstract_reversed_new_2_improve_instr_part_example_3_example_one_example",
    #                           response_list)
    # sample_csv=chain_comparison_util.save_csv(save_complicated_code_dir_root,"reversed_comparison_by_knowledge_from_abstract",csv_file_name)
    #
    # res=[sample+responses_list[ind] for ind,sample in enumerate(sample_csv)]
    #
    # util.save_csv(
    #     save_complicated_code_dir_root + idiom +"/"+ save_file_name+".csv",
    #     csv_res,
    #     ["repo_name", "file_path", "file_html", "class_name", "me_name", "me_code", "old_code", "new_code", "bool_code",
    #      "chatGPT_code", "if_correct",
    #      "instruction", "sys_msg", "exam_msg", "user_msg"])
