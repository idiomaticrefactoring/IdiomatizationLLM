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
if __name__ == '__main__':
    user_instr='''
We give you a Python code whose AST is BoolOp, you determine whether its values exist two comparison operations that have the same comparison operand. You answer based on the required response format.

the comparison operators of comparison operation are: 
"<" , ">",  "==",  ">=",  "<=",  "!=",  "is",  "is not",  "in",  "not in"

Python code:
{{code}}

response format:
Answer: You respond with Yes or No
Information: If your answer is Yes, you give the two comparison operations and the same comparison operand. Otherwise, you respond with None. Please explain your answer.
'''
    #v1 is not v2 and v3 > v1
    #v1 is v2 and v3 is not None
    #v1 == v2 and v3 % v4 == 0 and v5 % v6 == 0
    #v1 is not v2 and v1 < v3
    #v1 is not v2 and isinstance(v1, v3) and (v1 > v4)
    #v1 in v2 and v3 == v4 and (v1 != v5) and (v6 == v7)
    #v1 % v2 == v3 and v1 != v3
    #v1 is not v2 and v1 < v3
    #v1 % v2 == 0 and v3 % v2 == 0   v2

    # v1 is not v2 and v1 != v3 can
    #v1 is not v2 and v3 >= v1
    #v1 is not v2 and v3 is not v2
    #v1[v2][v3] == v4 and v3 != v4
    #v1 == v2 and v3 != v4
    #v1 > v2 and v3 == v2
    #v1 is v2 and type(v3) is v2
    examples =[]
    examples=[['''
We give you a Python code whose AST is BoolOp, you determine whether its values exist two comparison operations that have the same comparison operand. You answer based on the required response format.

the comparison operators of comparison operation are:
"<" , ">",  "==",  ">=",  "<=",  "!=",  "is",  "is not",  "in",  "not in"

Python code:
a>1 and and x>5 and a<10 and (a or b)

response format:
Answer: You respond with Yes or No
Information: If your answer is Yes, you give the two comparison operations and the same comparison operand. Otherwise, you respond with None. Please explain your answer.
''','''
Answer: Yes
Information:
one comparison operation: a>1
one comparison operation: a<10
the same comparison comparator: a
''']]

    idiom = "chain comparison"
    idiom = "_".join(idiom.split(" "))
    save_complicated_code_dir_root = util.data_root + "chatgpt/NonIdiomatic/"
    # save_complicated_code_dir_root = util.data_root + "NonIdiomatic/find_code_snippets/"
    save_complicated_code_dir=save_complicated_code_dir_root+"sample_methods/"

    samples = util.load_pkl(save_complicated_code_dir, "sample_methods_" + idiom)

    import chain_comparison_util
    # chain_comparison_util.save_csv(save_complicated_code_dir_root,"comparison_find_from_boolop_and","comparison_same_operand_add_correct.csv")
    # samples = util.load_pkl(save_complicated_code_dir_root + "chain_comparison_bool_compare/", "abstract_boolop_value_2_example_multi_binary_operation")


    # samples = util.load_pkl(save_complicated_code_dir_root + "chain_comparison_bool_compare/", "abstract_boolop_value_2_example_multi_binary_operation_new_2")
    # samples = util.load_pkl(save_complicated_code_dir_root + "chain_comparison_bool_compare/", "abstract_boolop_value_1_example_special_example")
    abstract_file_name="abstract_boolop_value_instr_no_explain_no_repeat"#"abstract_boolop_value_instr_no_explain"
    samples = util.load_pkl(save_complicated_code_dir_root + idiom+"/",abstract_file_name )
    save_file_name="find_comparison_add_kg_from_abstract_instr_5_no_repeat"#"find_comparison_add_kg_from_abstract_instr_5"
    abstract_code_list=[]
    reponse_list = []
    for sample in samples[62:64]:
        # print("sample: ",sample)
        # bool_code, old_code, repo_name, old_path, file_html, class_name, me_name, *other, new_code, method_code, msg, response = sample
        bool_code, old_code,*other,  new_code, method_code,info,response=sample
        try:
            sample[-1] = sample[-1]["choices"][0]["message"]["content"]
            for e in sample[-1].split("\n"):
                if "Python code" in e:
                    sample[-1]=sample[-1].split(":")[-1]
        except:
            sample[-1]="Do not have the abstract Python!"
        me_code=sample[-1]
        real_instruction = user_instr.replace("{{code}}", me_code)
        print("real_instruction: ",real_instruction)
        print("abstract_code: ",sample[-1])
        msg = chatgpt_util.format_message_2(real_instruction, examples=examples, sys_msg="You are a helpful assistant.")
        # print(">>>>>>>>>>each msg: ", msg)
        num_tokes = chatgpt_util.num_tokens_from_messages(msg)
        # print("len of msg: ",chatgpt_util.num_tokens_from_messages(msg))
        # if chatgpt_util.num_tokens_from_messages(msg)>=chatgpt_util.MAX_TOKENS:
        #     response
        try:
            response = chatgpt_util.chatGPT_result(msg)
            print(">>>>>>>>>>each response:\n", response)
            reponse_list.append([me_code, old_code, *other, new_code, method_code])
            reponse_list[-1].extend([[msg, num_tokes], response])
        except:
            traceback.print_exc()
            reponse_list.append([me_code, old_code, *other, new_code, method_code])
            reponse_list[-1].extend([[msg, num_tokes], traceback.format_exc()])
        abstract_code_list.append(sample[-1].strip())
    # util.save_pkl(save_complicated_code_dir_root + idiom+"/"
    #               ,save_file_name,
    #               reponse_list)
    # samples = util.load_pkl(save_complicated_code_dir, "sample_methods_" + idiom)
    # def get_response(user_instr,examples,samples,sys_msg="You are a helpful assistant.",values=None,abstract_code_list=abstract_code_list):
    #     reponse_list=[]
    #     count=0
    #     for ind_sampl, sample_method in enumerate(samples):
    #         for code in sample_method:
    #             # repo_name, old_path, file_html, class_name,me_name, old_list, new_tree,\
    #             #     old_code,new_code, method_code=code
    #             # break
    #             *other, old_list, new_tree, \
    #             old_code, new_code, method_code = code
    #             # print("method_code: ",method_code)
    #             bool_code_list=extract_boolop_and.get_BoolOp_And(method_code)
    #             for bool_node in bool_code_list:
    #                 me_code=ast.unparse(bool_node)
    #                 if abstract_code_list:
    #                     me_code=abstract_code_list[count]
    #                     # for e_node in ast.walk(ast.parse(me_code)):
    #                     #     if isinstance(e_node,ast.BoolOp):
    #                     #         bool_node=e_node
    #                     #         break
    #                 count+=1
    #
    #
    #                 real_instruction=user_instr.replace("{{code}}", me_code)
    #                 # real_instruction = real_instruction.replace("{{AST}}", ast.dump(bool_node))
    #
    #                 if values:
    #                     values_list=[ast.unparse(value) for value in bool_node.values]
    #                     values_str="\n".join(values_list)
    #                     real_instruction = real_instruction.replace("{{value}}", values_str)
    #
    #                 # real_instruction=real_instruction+4000*'abc'
    #                 print(">>>>>>>>>>Instr: ", real_instruction)
    #
    #                 msg=chatgpt_util.format_message_2(real_instruction, examples=examples, sys_msg=sys_msg)
    #                 # print(">>>>>>>>>>each msg: ", msg)
    #                 num_tokes=chatgpt_util.num_tokens_from_messages(msg)
    #                 # print("len of msg: ",chatgpt_util.num_tokens_from_messages(msg))
    #                 # if chatgpt_util.num_tokens_from_messages(msg)>=chatgpt_util.MAX_TOKENS:
    #                 #     response
    #                 try:
    #                     response=chatgpt_util.chatGPT_result(msg)
    #                     print(">>>>>>>>>>each response:\n", response)
    #                     reponse_list.append([me_code, old_code, *other,new_code,method_code])
    #                     reponse_list[-1].extend([[msg,num_tokes],response])
    #                 except:
    #                     traceback.print_exc()
    #                     reponse_list.append([me_code, old_code, *other,new_code,method_code])
    #                     reponse_list[-1].extend([[msg,num_tokes],traceback.format_exc()])
    #     return reponse_list

    # reponse_list=get_response(user_instr,examples,samples[:],sys_msg="You are a helpful assistant.",values=None,abstract_code_list=abstract_code_list)
    # util.save_pkl(save_complicated_code_dir_root + "chain_comparison_bool_compare/",
    #                           "find_comparison_from_abstract_boolop_value_2_example_multi_binary_operation",
    #                           reponse_list)
    # util.save_pkl(save_complicated_code_dir_root + "chain_comparison_bool_compare/",
    #               "find_comparison_from_abstract_boolop_value_2_example_multi_binary_operation_new_2",
    #               reponse_list)
    # chain_comparison_util.save_csv(save_complicated_code_dir_root,"find_comparison_from_abstract_boolop_value_2_example_multi_binary_operation_new_2","find_comparison_from_abstract_boolop_value_2_example_multi_binary_operation_new_2.csv")
    # chain_comparison_util.save_csv(save_complicated_code_dir_root,"comparison_find_from_boolop_and_3_examples","find_comparison_from_abstract_1_example.csv")
    # util.save_pkl(save_complicated_code_dir_root + "chain_comparison_bool_compare/",
    #                                         "find_comparison_from_abstract_boolop_value_1_example_part_example",
    #                                         reponse_list)
    # util.save_pkl(save_complicated_code_dir_root + "chain_comparison_bool_compare/",
    #                                         "find_comparison_from_abstract_boolop_value_3_example_part_example",
    #                                         reponse_list)
    # samples = util.load_pkl(save_complicated_code_dir_root+ "chain_comparison_bool_compare/", "find_comparison_from_abstract_boolop_value_1_example_part_example")
    # print("len: ",len(samples))
    # samples = util.load_pkl(save_complicated_code_dir_root+ "chain_comparison_bool_compare/", "comparison_find_from_boolop_and")
    # #
    #
    # samples_csv=[]
    # for ind_sam,sample in enumerate(samples):
    #     try:
    #         bool_code, old_code, repo_name, old_path, file_html, class_name, me_name,*other,new_code,method_code,msg,response=sample
    #         print("bool_code:\n ",bool_code)
    #         print("method_code:\n ", method_code)
    #         print("response:\n ", response)
    #         # print("other: ",other)
    #
    #
    #
    #         if_correct=0
    #         try:
    #             sample[-1]=sample[-1]["choices"][0]["message"]["content"]
    #
    #             print(" sample[-1]: ",sample[-1])
    #             if_correct=chain_comparison_util.whether_two_compare_same_comparator(bool_code, sample[-1])
    #             print("if_correct: ", if_correct)
    #             # a = ast.literal_eval(sample[-1])
    #             # a=jsonify(sample[-1])
    #             # a=json.loads(samples[-1])
    #             # sample[-1]="\n###########\n".join(a)
    #         except:
    #             pass
    #         real_instruction = user_instr.replace("{{code}}", sample[0])
    #         ele=[repo_name, old_path, file_html, class_name, me_name,method_code,old_code,new_code,bool_code,sample[-1],if_correct,real_instruction]
    #     except:
    #         traceback.print_exc()
    #         print("sample: ",len(sample))
    #         ele=[repo_name, old_path, file_html, class_name, me_name,method_code,old_code,new_code,bool_code,sample[-1],if_correct,real_instruction]
    #         break
    #     samples_csv.append(ele)
    # # util.save_csv(
    # # save_complicated_code_dir_root + "chain_comparison_bool_compare/"+"comparison_same_operand.csv",
    # #                             samples_csv,
    # #                             ["repo_name", "file_path","file_html", "class_name","me_name", "me_code", "old_code", "new_code", "bool_code", "chatGPT_code","if_correct",
    # #                              "instruction"])
    # util.save_csv(
    # save_complicated_code_dir_root + "chain_comparison_bool_compare/"+"comparison_same_operand_add_correct.csv",
    #                             samples_csv,
    #                             ["repo_name", "file_path","file_html", "class_name","me_name", "me_code", "old_code", "new_code", "bool_code", "chatGPT_code","if_correct",
    #                              "instruction"])
    #