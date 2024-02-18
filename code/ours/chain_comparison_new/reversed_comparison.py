import os,sys
import struct
import traceback
code_dir = "/".join(os.path.abspath(__file__).split("/")[:-2]) + "/"
print("code path: ",code_dir)
sys.path.append(code_dir)
import chatgpt_util,random
import openai, tiktoken,ast,util
import ast
import extract_boolop_and
import chain_comparison_util,chain_compare_instr


def extract_new_Python_code(response):
    answer_list = response.split("\n")
    if "Yes" in answer_list[0]:
        for e in answer_list[1:]:

            if "New Python Code" in e:
                python_code = e.split(":")[-1].strip()
                if "can be rewritten as" in python_code:
                    python_code = python_code.split("can be rewritten as")[-1].strip()
                return python_code
    return None


def extract_comparison(response):
    comparison_1 = None
    comparison_2 = None
    same_comparator = None
    answer_list = response.split("\n")
    if "Yes" in answer_list[0]:
        for e in answer_list[1:]:

            if "one comparison operation" in e:
                if comparison_1:
                    comparison_2 = e.split(":")[-1].strip()
                else:
                    comparison_1 = e.split(":")[-1].strip()
            else:
                flag_compar = chain_comparison_util.extract_answer_same_comparison(e)
                if flag_compar:
                    same_comparator = flag_compar
        return 1, comparison_1, comparison_2, same_comparator
    return None, None, None, None


def has_substring(string_1, string_2):
    return string_1 in string_2


def check_substring(comparison_1, comparison_2, same_comparator):
    total_string = comparison_1 + " and " + comparison_2
    substring = same_comparator + " and " + same_comparator
    if has_substring(substring, total_string):
        return total_string
    return None


def extract_abstract_info(response):
    new_python_code=None
    dict_map = dict()
    e = response.split("\n")
    # print("response: ",response)
    for i in e:
        i=i.strip()
        if "Python code" in i or "Python Code" in i:
            new_python_code=i.split(":")[-1].strip()
            compare_list=new_python_code.split(" and ")
            return new_python_code,compare_list[0].strip(),compare_list[1].strip(),dict_map
        elif not i.startswith("symbols") and i:
            print("i: ",i)
            real_var,abstract_v = i.split(":")[0], ":".join(i.split(":")[1:])
            dict_map[abstract_v] = real_var
    return new_python_code, None, None, None
def get_compare_node(code):
    for e in ast.walk(ast.parse(code)):
        if isinstance(e,ast.Compare):
            return e
def get_response(comparison_list,user_instr,examples):
    offset=0
    responses_list = []#9:12#17:19
    for ind_saple, sample in enumerate(comparison_list):
        bool_code, old_code, repo_name, old_path, file_html, class_name, me_name, *other, new_code, method_code, real_comparison_1, real_comparison_2,msg2msg, response  = sample
        if "0 <= cell[1] < self.grid.shape[-2] and 0 <= cell[0] < self.grid.shape[-1]" not in old_code:
            continue
        # print("comparison_1,comparison_2: ",real_comparison_1,real_comparison_2)
        # if not ("not in" in real_comparison_1  or "not in" in real_comparison_2):
        #     continue
        # if not ("is" in real_comparison_1  or "is" in real_comparison_2):
        #     continue
        #v3 > v2
        try:
            response = response["choices"][0]["message"]["content"]
            new_python_code, comparison_1, comparison_2, dict_map = extract_abstract_info(response)
            # print("dict_map: ",dict_map)
            # return

            # print("previous response: ",response)
            operands_1 = [ast.unparse(e) for e in chain_compare_instr.get_compare_operands(get_compare_node(comparison_1))]
            operands_2 = [ast.unparse(e) for e in chain_compare_instr.get_compare_operands(get_compare_node(comparison_2))]
            same_comparator= chain_compare_instr.has_common_elements(operands_1, operands_2)[0]
            # print("abstract_comparison_1, abstract_comparison_2: ", comparison_1, comparison_2,same_comparator)

            #
            # has_comparaison, comparison_1, comparison_2, same_comparator = extract_comparison(sample[-1])
            if same_comparator:
                flag_total_string = check_substring(comparison_1, comparison_2, same_comparator)
                if flag_total_string:
                    info = f"We do not need to do reverse operations because the python code has contain the substring {same_comparator} and {same_comparator}"
                    print(info, flag_total_string, same_comparator)
                    responses_list.append([dict_map,bool_code,old_code,real_comparison_1,real_comparison_2,comparison_1, comparison_2,repo_name, old_path, file_html, class_name, me_name, method_code, True, flag_total_string, 0, info, None])
                else:
                    new_Python_code_1, new_Python_code_2 = None, None
                    previous_code = []
                    msg1, answer1 = chain_comparison_util.get_each_repsonse(comparison_1, user_instr, examples)
                    new_Python_code_1 = extract_new_Python_code(answer1)
                    flag = 0
                    print(ind_saple, "sample:", ">>>>>>>>>>>>>>>the first reversed operation: ", answer1)
                    if new_Python_code_1:
                        flag_total_string = check_substring(new_Python_code_1, comparison_2, same_comparator)
                        if flag_total_string:
                            flag = 1
                            responses_list.append([dict_map,bool_code,old_code,real_comparison_1,real_comparison_2,comparison_1, comparison_2,repo_name, old_path, file_html, class_name, me_name, method_code,True, flag_total_string, 1, [msg1], [answer1]])
                        print(ind_saple, "sample:", ">>>>>>>>>>>>>>>result total string: ", flag_total_string, flag,new_Python_code_1)

                    if not flag:
                        msg2, answer2 = chain_comparison_util.get_each_repsonse(comparison_2, user_instr, examples)
                        new_Python_code_2 = extract_new_Python_code(answer2)
                        print(ind_saple, "sample:", ">>>>>>>>>>>>>>>the second reversed operation: ", answer2,new_Python_code_2)
                        if new_Python_code_2:
                            flag_total_string = check_substring(comparison_1, new_Python_code_2, same_comparator)
                            if flag_total_string:
                                flag = 1
                                responses_list.append([dict_map,bool_code,old_code,real_comparison_1,real_comparison_2,comparison_1, comparison_2,repo_name, old_path, file_html, class_name, me_name, method_code,True, flag_total_string, 2, [msg2], [answer2]])
                            print(ind_saple, "sample:", ">>>>>>>>>>>>>>>result total string: ", flag_total_string, flag)

                    if not flag:
                        if new_Python_code_1 and new_Python_code_2:
                            new_total_code = new_Python_code_1 + " and " + new_Python_code_2
                        else:
                            new_total_code = (new_Python_code_2 if new_Python_code_2 else comparison_2) + " and " + (
                                new_Python_code_1 if new_Python_code_1 else comparison_1)

                        flag_total_string = has_substring(same_comparator + " and " + same_comparator, new_total_code)
                        if flag_total_string:
                            flag = 1
                            responses_list.append([dict_map,bool_code,old_code,real_comparison_1,real_comparison_2,comparison_1, comparison_2,repo_name, old_path, file_html, class_name, me_name, method_code,True, new_total_code, 3, [msg1, msg2], [answer1, answer2]])
                        print(ind_saple, "sample:",
                              ">>>>>>>>>>>>>>>change the order of comparison operations or merge operation: ",
                              same_comparator + " and " + same_comparator, new_total_code,
                              "satisfied" if flag else "unsatisfied")
                    # if not flag:
                    #     responses_list.append([dict_map,False, new_total_code, 3, [msg1, msg2], [answer1, answer2]])
            else:
                continue
                # info = "We do not use chatgpt to do reverse operations because the python code does not have two comparison operations that have the same comparison operand"
                # responses_list.append([dict_map,0, sample[-1], 3, info, None])
                # print(ind_saple, "sample:", info, sample[-1], bool_code)
                # #
            # for e in sample[-1].split("\n"):
            #     if "Python code" in e:
            #         sample[-1]=sample[-1].split(":")[-1]
        except:
            # sample[-1] = f"Do not get response!{traceback.print_exc()}"
            # print(ind_saple, "sample:", sample[-1])
            # responses_list.append([None, None, None, sample[-1], None])
            continue
    return responses_list
if __name__ == '__main__':
    user_instr='''
Select knowledge from the following knowledge that matches the same comparison operations with the following comparison Python code to respond if the comparison operands of the following comparison Python code can be reversed. You respond based on the required response format.

Python code:
{{code}}

knowledge:
v_1 > v_2 can be reversed as v_2 < v_1
v_1 < v_2 can be reversed as v_2 > v_1
v_1 >= v_2 can be reversed as v_2 <= v_1
v_1 <= v_2 can be reversed as v_2 >= v_1
v_1 == v_2 can be reversed as v_2 == v_1
v_1 != v_2 can be reversed as v_2 != v_1
v_1 is v_2 can be reversed as v_2 is v_1
v_1 is not v_2 can be reversed as v_2 is not v_1
comparison operands of in comparison operation cannot be reversed
comparison operands of not in comparison operation cannot be reversed

response format:
Answer: You respond with Yes or No
New Python Code: If your answer is Yes, you give the new Python code. Otherwise, you respond with None.
'''
    examples=[['''
Select knowledge from the following knowledge that matches the same comparison operations with the following comparison Python code to respond if the comparison operands of the following comparison Python code can be reversed. You respond based on the required response format.

Python code:
v1 != v2

knowledge:
v_1 > v_2 can be reversed as v_2 < v_1
v_1 < v_2 can be reversed as v_2 > v_1
v_1 >= v_2 can be reversed as v_2 <= v_1
v_1 <= v_2 can be reversed as v_2 >= v_1
v_1 == v_2 can be reversed as v_2 == v_1
v_1 != v_2 can be reversed as v_2 != v_1
v_1 is v_2 can be reversed as v_2 is v_1
v_1 is not v_2 can be reversed as v_2 is not v_1
comparison operands of in comparison operation cannot be reversed
comparison operands of not in comparison operation cannot be reversed

response format:
Answer: You respond with Yes or No
New Python Code: If your answer is Yes, you give the new Python code. Otherwise, you respond with None.
''',
'''
Answer: Yes
New Python Code: v2 != v1
'''],['''
Select knowledge from the following knowledge that matches the same comparison operations with the following comparison Python code to respond if the comparison operands of the following comparison Python code can be reversed. You respond based on the required response format.

Python code:
v1 in v2

knowledge:
v_1 > v_2 can be reversed as v_2 < v_1
v_1 < v_2 can be reversed as v_2 > v_1
v_1 >= v_2 can be reversed as v_2 <= v_1
v_1 <= v_2 can be reversed as v_2 >= v_1
v_1 == v_2 can be reversed as v_2 == v_1
v_1 != v_2 can be reversed as v_2 != v_1
v_1 is v_2 can be reversed as v_2 is v_1
v_1 is not v_2 can be reversed as v_2 is not v_1
comparison operands of in comparison operation cannot be reversed
comparison operands of not in comparison operation cannot be reversed

response format:
Answer: You respond with Yes or No
New Python Code: If your answer is Yes, you give the new Python code. Otherwise, you respond with None.
''','''
Answer: No
New Python Code: None'''],['''
Select knowledge from the following knowledge that matches the same comparison operations with the following comparison Python code to respond if the comparison operands of the following comparison Python code can be reversed. You respond based on the required response format.

Python code:
v1 > v2

knowledge:
v_1 > v_2 can be reversed as v_2 < v_1
v_1 < v_2 can be reversed as v_2 > v_1
v_1 >= v_2 can be reversed as v_2 <= v_1
v_1 <= v_2 can be reversed as v_2 >= v_1
v_1 == v_2 can be reversed as v_2 == v_1
v_1 != v_2 can be reversed as v_2 != v_1
v_1 is v_2 can be reversed as v_2 is v_1
v_1 is not v_2 can be reversed as v_2 is not v_1
comparison operands of in comparison operation cannot be reversed
comparison operands of not in comparison operation cannot be reversed

response format:
Answer: You respond with Yes or No
New Python Code: If your answer is Yes, you give the new Python code. Otherwise, you respond with None.
''',
'''
Answer: Yes
New Python Code: v2 < v1
'''],['''
Select knowledge from the following knowledge that matches the same comparison operations with the following comparison Python code to respond if the comparison operands of the following comparison Python code can be reversed. You respond based on the required response format.

Python code:
v1 is not v2

knowledge:
v_1 > v_2 can be reversed as v_2 < v_1
v_1 < v_2 can be reversed as v_2 > v_1
v_1 >= v_2 can be reversed as v_2 <= v_1
v_1 <= v_2 can be reversed as v_2 >= v_1
v_1 == v_2 can be reversed as v_2 == v_1
v_1 != v_2 can be reversed as v_2 != v_1
v_1 is v_2 can be reversed as v_2 is v_1
v_1 is not v_2 can be reversed as v_2 is not v_1
comparison operands of in comparison operation cannot be reversed
comparison operands of not in comparison operation cannot be reversed

response format:
Answer: You respond with Yes or No
New Python Code: If your answer is Yes, you give the new Python code. Otherwise, you respond with None.
''',
'''
Answer: Yes
New Python Code: v2 is not v1
'''],['''
Select knowledge from the following knowledge that matches the same comparison operations with the following comparison Python code to respond if the comparison operands of the following comparison Python code can be reversed. You respond based on the required response format.

Python code:
v1 > v2 > v3

knowledge:
v_1 > v_2 can be reversed as v_2 < v_1
v_1 < v_2 can be reversed as v_2 > v_1
v_1 >= v_2 can be reversed as v_2 <= v_1
v_1 <= v_2 can be reversed as v_2 >= v_1
v_1 == v_2 can be reversed as v_2 == v_1
v_1 != v_2 can be reversed as v_2 != v_1
v_1 is v_2 can be reversed as v_2 is v_1
v_1 is not v_2 can be reversed as v_2 is not v_1
comparison operands of in comparison operation cannot be reversed
comparison operands of not in comparison operation cannot be reversed

response format:
Answer: You respond with Yes or No
New Python Code: If your answer is Yes, you give the new Python code. Otherwise, you respond with None.
''',
'''
Answer: Yes
New Python Code: v3 < v2 < v1
''']
              ]


    idiom = "chain comparison"
    idiom = "_".join(idiom.split(" "))
    save_complicated_code_dir_root = util.data_root + "chatgpt/NonIdiomatic/"
    # save_complicated_code_dir_root = util.data_root + "NonIdiomatic/find_code_snippets/"
    save_complicated_code_dir=save_complicated_code_dir_root+"sample_methods/"
    # find_comparison_from_abstract_boolop_value_2_example_multi_binary_operation_new_2
    # comparison_list = util.load_pkl(save_complicated_code_dir_root+ "chain_comparison_bool_compare/", "find_comparison_from_abstract_boolop_value_2_example_multi_binary_operation")
    #
    find_compare_name="abstract_same_operand_instr"#"find_comparison_add_kg_from_abstract_instr_5_no_repeat"#"find_comparison_add_kg_from_abstract_instr_5"
    # comparison_list = util.load_pkl(save_complicated_code_dir_root+ "chain_comparison_bool_compare/",
    #                 find_compare_name)
    comparison_list = util.load_pkl(save_complicated_code_dir_root +idiom+"/",
                                    find_compare_name)
    save_file_name="reversed_comparison_by_knowledge_from_abstract_find_same_operand_2_improve"
    # comparison_list = util.load_pkl(save_complicated_code_dir_root + "chain_comparison_bool_compare/",
    #                                 "find_comparison_from_abstract_boolop_value_2_example_multi_binary_operation_new_2_change_special_example")

    responses_list=get_response(comparison_list,user_instr,examples)
    '''
    # util.save_pkl(save_complicated_code_dir_root + "chain_comparison_bool_compare/",
    #                           "reversed_comparison_by_knowledge_from_abstract-find-same-operand_part_example",
    #                           responses_list)
    util.save_pkl(save_complicated_code_dir_root + "chain_comparison_bool_compare/",
                  "reversed_comparison_by_knowledge_from_abstract_find_same_operand_2_improve",
                  responses_list)
    
    '''
    samples = util.load_pkl(save_complicated_code_dir_root + "chain_comparison_bool_compare/", save_file_name)
    for sample in samples:
        print("sample: ",sample)
        break
        dict_map, bool_code, old_code, real_comparison_1, real_comparison_2, comparison_1, comparison_2, repo_name, \
        old_path, file_html, class_name, me_name, method_code, flag_can_refactor, flag_total_string, *other,response = sample
        if "0 <= cell[1] < self.grid.shape[-2] and 0 <= cell[0] < self.grid.shape[-1]" not in old_code:
            continue
        # bool_code, old_code, repo_name, old_path, file_html, class_name, me_name, *other, new_code, method_code, real_comparison_1, real_comparison_2, msg2msg, response = sample
        print("bool_code: ", bool_code)
        # print("comparison_1,comparison_2: ",real_comparison_1,real_comparison_2)
        # if not ("not in" in real_comparison_1  or "not in" in real_comparison_2):
        #     continue
        # if not ("is" in real_comparison_1  or "is" in real_comparison_2):
        #     continue
        # v3 > v2

        response = response["choices"][0]["message"]["content"]
        print("response: ", response)
    # save_file_name="reversed_comparison_by_knowledge_from_same_operand_code"#"reversed_comparison_by_knowledge_from_abstract_instr5_find_comparison_kg"#"find_comparison_add_kg_from_abstract_instr_5"

    # util.save_pkl(save_complicated_code_dir_root +idiom+"/",
    #               save_file_name,
    #               responses_list)
    # util.save_pkl(save_complicated_code_dir_root + "chain_comparison_bool_compare/",
    #                           "reversed_comparison_by_knowledge_from_abstract-find-same-operand_new_2",
    #                           responses_list)
    # util.save_pkl(save_complicated_code_dir_root + "chain_comparison_bool_compare/",
    #                           "reversed_comparison_by_knowledge_from_abstract-find-same-operand_modify",
    #                           responses_list)
    # util.save_pkl(save_complicated_code_dir_root + "chain_comparison_bool_compare/",
    #               "reversed_comparison_by_knowledge_from_abstract-find-same-operand_modify_some_special_example",
    #               responses_list)
    # responses_list = util.load_pkl(save_complicated_code_dir_root+ "chain_comparison_bool_compare/", "reversed_comparison_by_knowledge_from_abstract-find-same-operand")

    # csv_file_name="reversed_comparison_by_knowledge_from_abstract.csv"
    # sample_csv=chain_comparison_util.save_csv(save_complicated_code_dir_root,"reversed_comparison_by_knowledge_from_abstract",csv_file_name)
    #
    # res=[sample+responses_list[ind] for ind,sample in enumerate(sample_csv)]
    #
    # util.save_csv(
    #     save_complicated_code_dir_root + "chain_comparison_bool_compare/" + csv_file_name,
    #     sample_csv,
    #     ["repo_name", "file_path", "file_html", "class_name", "me_name", "me_code", "old_code", "new_code", "bool_code",
    #      "chatGPT_code", "if_correct",
    #      "instruction", "sys_msg", "exam_msg", "user_msg"])
