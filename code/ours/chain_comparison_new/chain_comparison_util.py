import ast,os,sys
import chain_comparison_util,traceback
import util_rewrite

code_dir = "/".join(os.path.abspath(__file__).split("/")[:-2]) + "/"
print("code path: ",code_dir)
sys.path.append(code_dir)
import chatgpt_util,random
import openai, tiktoken,ast,util
import extract_boolop_and,chain_compare_instr
def parse_answer(response):
    e = response.split("\n")
    flag = 0
    # if "Yes" in e[0]:
    #     flag=1
    for i in e:
        if "Yes" in i:
            flag = 1
        if i.startswith("the same comparison comparator: ") or "same comparison" in i or "Same comparison" in i:
            same_comparator = i.split(":")[-1].strip()
            return flag, same_comparator
    return flag, None

def extract_answer_same_comparison(response):
    if response.startswith("the same comparison comparator: ") or "same comparison" in response or "Same comparison" in response:
        same_comparator = response.split(":")[-1].strip()
        return same_comparator
    return None



def whether_two_compare_same_comparator(bool_code, response):
    flag, same_comparator = parse_answer(response)
    print("flag: ", flag, same_comparator)
    for node in ast.walk(ast.parse(bool_code)):
        if isinstance(node, ast.BoolOp):
            print(node)
            comparators = [[ast.unparse(com) for com in e.comparators] + [ast.unparse(e.left)] for e in node.values if
                           isinstance(e, ast.Compare)]
            for ind, cm in enumerate(comparators):
                for cm2 in comparators[ind + 1:]:
                    same_ele = set(cm) & set(cm2)

                    same_ele = {str(e) for e in same_ele}

                    if same_ele:
                        if flag and same_comparator in same_ele:
                            return 1
                        if not flag:
                            return 0
    if flag == 0:
        return 1

    return 0
def get_each_repsonse(code,user_instr,examples,sys_msg="You are a helpful assistant."):
    real_instruction = user_instr.replace("{{code}}", code)
    print(">>>>>>>>real_instruction: ",real_instruction)
    msg = chatgpt_util.format_message_2(real_instruction, examples=examples, sys_msg=sys_msg)
    # print(">>>>>>>>msg: ",msg)
    response=chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>response: ",response['choices'][0]['message']["content"])
    return msg, response['choices'][0]['message']["content"]



def get_response(user_instr,examples,samples,sys_msg="You are a helpful assistant.",values=None):
    reponse_list=[]
    count=-1
    for ind_sampl, sample_method in enumerate(samples):
        for code in sample_method:
            # repo_name, old_path, file_html, class_name,me_name, old_list, new_tree,\
            #     old_code,new_code, method_code=code
            # break
            *other, old_list, new_tree, \
            old_code, new_code, method_code = code
            # print("method_code: ",method_code)
            bool_code_list=extract_boolop_and.get_BoolOp_And(method_code)
            for bool_node in bool_code_list:
                count+=1
                #[15+i for i in range(0,20)]+
                # if count not in [62,162,163,183,194,206,223,235,242,245,247,254,259,261,274,308,363,364,385,394,465,493,507,539,557,571,588]:
                #     continue

                me_code=ast.unparse(bool_node)
                # other.append(new_code)
                # other.append(method_code)

                real_instruction=user_instr.replace("{{code}}", me_code)
                real_instruction = real_instruction.replace("{{AST}}", ast.dump(bool_node))

                if values:
                    values_list=[ast.unparse(value) for value in bool_node.values]
                    values_str="\n".join(values_list)
                    real_instruction = real_instruction.replace("{{value}}", values_str)

                # real_instruction=real_instruction+4000*'abc'
                print(">>>>>>>>>>Instr: ", real_instruction)

                msg=chatgpt_util.format_message_2(real_instruction, examples=examples, sys_msg=sys_msg)
                # print(">>>>>>>>>>each msg: ", msg)
                num_tokes=chatgpt_util.num_tokens_from_messages(msg)
                # print("len of msg: ",chatgpt_util.num_tokens_from_messages(msg))
                # if chatgpt_util.num_tokens_from_messages(msg)>=chatgpt_util.MAX_TOKENS:
                #     response
                try:
                    response=chatgpt_util.chatGPT_result(msg)
                    print(">>>>>>>>>>each response:\n", response)
                    reponse_list.append([me_code, old_code, *other,new_code,method_code])
                    reponse_list[-1].extend([[msg,num_tokes],response])
                except:
                    traceback.print_exc()
                    reponse_list.append([me_code, old_code, *other,new_code,method_code])
                    reponse_list[-1].extend([[msg,num_tokes],traceback.format_exc()])
    return reponse_list
    # util.save_pkl(save_complicated_code_dir_root + "chain_comparison_bool_compare/",
    #                           "comparison_find_from_boolop_and_3_examples",
    #                           reponse_list)
def get_response_no_repeat(user_instr,examples,samples,sys_msg="You are a helpful assistant.",values=None):
    reponse_list=[]
    count=-1
    method_list=[]
    for ind_sampl, sample_method in enumerate(samples):
        for code in sample_method:
            # repo_name, old_path, file_html, class_name,me_name, old_list, new_tree,\
            #     old_code,new_code, method_code=code
            # break
            *other, old_list, new_tree, \
            old_code, new_code, method_code = code
            method_list.append([ *other, old_list, new_tree,old_code, new_code, method_code])
            break
    for  *other, old_list, new_tree,old_code, new_code, method_code in method_list:
            # print("method_code: ",method_code)
            bool_code_list=extract_boolop_and.get_BoolOp_And(method_code)
            for bool_node in bool_code_list:
                count+=1
                #[15+i for i in range(0,20)]+
                # if count not in [62,162,163,183,194,206,223,235,242,245,247,254,259,261,274,308,363,364,385,394,465,493,507,539,557,571,588]:
                #     continue

                me_code=ast.unparse(bool_node)
                if "output_spatial_sizes[0] % shape[1] == 0" not in me_code:#mode == 'UPSAMPLE_MODE' and output_spatial_sizes[0] % shape[1] == 0 and (output_spatial_sizes[1] % shape[2] == 0) i % 1000000 == 0 iter % save_interval == 0 iter % log_iters == 0 i % 1000000 == 0 and i > 0 site['type'] == 'sample' site['type'] == 'plate' nums[j] > previousSmallestNum  key.find('filename') < 0 nums[j] > previousSmallestNum
                    continue
                # other.append(new_code)
                # other.append(method_code)

                real_instruction=user_instr.replace("{{code}}", me_code)
                real_instruction = real_instruction.replace("{{AST}}", ast.dump(bool_node))

                if values:
                    values_list=[ast.unparse(value) for value in bool_node.values]
                    values_str="\n".join(values_list)
                    real_instruction = real_instruction.replace("{{value}}", values_str)

                # real_instruction=real_instruction+4000*'abc'
                print(">>>>>>>>>>Instr: ", real_instruction)

                msg=chatgpt_util.format_message_2(real_instruction, examples=examples, sys_msg=sys_msg)
                # print(">>>>>>>>>>each msg: ", msg)
                num_tokes=chatgpt_util.num_tokens_from_messages(msg)
                # print("len of msg: ",chatgpt_util.num_tokens_from_messages(msg))
                # if chatgpt_util.num_tokens_from_messages(msg)>=chatgpt_util.MAX_TOKENS:
                #     response
                try:
                    response=chatgpt_util.chatGPT_result(msg)
                    print(">>>>>>>>>>each response:\n", response)
                    reponse_list.append([me_code, old_code, *other,new_code,method_code])
                    reponse_list[-1].extend([[msg,num_tokes],response])
                except:
                    traceback.print_exc()
                    reponse_list.append([me_code, old_code, *other,new_code,method_code])
                    reponse_list[-1].extend([[msg,num_tokes],traceback.format_exc()])
    return reponse_list


def get_response_no_repeat_abstract(user_instr,examples,samples,sys_msg="You are a helpful assistant.",values=None):
    reponse_list=[]
    count=-1
    method_list=[]
    for ind_sampl, sample_method in enumerate(samples):
        for code in sample_method:
            # repo_name, old_path, file_html, class_name,me_name, old_list, new_tree,\
            #     old_code,new_code, method_code=code
            # break
            *other, old_list, new_tree, \
            old_code, new_code, method_code = code
            method_list.append([ *other, old_list, new_tree,old_code, new_code, method_code])
            break
    for  *other, old_list, new_tree,old_code, new_code, method_code in method_list:
            # print("method_code: ",method_code)
            bool_code_list=extract_boolop_and.get_BoolOp_And(method_code)
            for bool_node in bool_code_list:
                count+=1
                #[15+i for i in range(0,20)]+
                # if count not in [62,162,163,183,194,206,223,235,242,245,247,254,259,261,274,308,363,364,385,394,465,493,507,539,557,571,588]:
                #     continue

                me_code=ast.unparse(bool_node)
                # if "top_k != 'all' and boxes.shape[0] > top_k" not in me_code:#iprot._fast_decode is not None len(lower) == 1 self.Margins <= xPos <= wm nums[j] > previousSmallestNum site['args'][1] is not None min(masked_gaussian.shape) > 0 mode == 'UPSAMPLE_MODE' and output_spatial_sizes[0] % shape[1] == 0 and (output_spatial_sizes[1] % shape[2] == 0) i % 1000000 == 0 iter % save_interval == 0 iter % log_iters == 0 i % 1000000 == 0 and i > 0 site['type'] == 'sample' site['type'] == 'plate' nums[j] > previousSmallestNum  key.find('filename') < 0 nums[j] > previousSmallestNum
                #     continue
                # print("come here: ",me_code)
                # other.append(new_code)
                # other.append(method_code)
                compare_list=chain_compare_instr.extract_compare_nodes(bool_node.values)
                # print(compare_list)
                combinations=chain_compare_instr.get_combinations(compare_list)
                # print(combinations)
                real_list=[]
                for e1, e2 in combinations:
                    # print(e1, e2)
                    operands_1= [ast.unparse(e) for e in chain_compare_instr.get_compare_operands(e1)]
                    operands_2=[ast.unparse(e) for e in chain_compare_instr.get_compare_operands(e2)]
                    if chain_compare_instr.has_common_elements(operands_1,operands_2):
                        real_list.append([e1, e2])
                for e1,e2 in real_list:
                    e1_str=ast.unparse(e1)
                    e2_str=ast.unparse(e2)
                    real_instruction = user_instr.replace("{{code}}", util_rewrite.join([e1_str,e2_str]," and "))
                    operand_list=[e for com in [e1,e2] if chain_compare_instr.get_compare_operands(com) for e in chain_compare_instr.get_compare_operands(com)]
                    operand_str="\n".join([ast.unparse(oper) for oper in operand_list])
                    real_instruction = real_instruction.replace("{{operand}}", operand_str)
                #
                # print(real_list)
                # continue
                # compare_list=chain_compare_instr.get_compare_nodes(bool_node)
                # operand_list=[e for com in compare_list if chain_compare_instr.get_compare_operands(com) for e in chain_compare_instr.get_compare_operands(com)]
                # operand_str="\n".join([ast.unparse(oper) for oper in operand_list])
                # real_instruction=user_instr.replace("{{code}}", me_code)
                # real_instruction = real_instruction.replace("{{AST}}", ast.dump(bool_node))
                # real_instruction = real_instruction.replace("{{operand}}", operand_str)

                # if values:
                #     values_list=[ast.unparse(value) for value in bool_node.values]
                #     values_str="\n".join(values_list)
                #     real_instruction = real_instruction.replace("{{value}}", values_str)

                # real_instruction=real_instruction+4000*'abc'
                    print(">>>>>>>>>>Instr: ", real_instruction)

                    msg=chatgpt_util.format_message_2(real_instruction, examples=examples, sys_msg=sys_msg)
                    # print(">>>>>>>>>>each msg: ", msg)
                    num_tokes=chatgpt_util.num_tokens_from_messages(msg)
                    # print("len of msg: ",chatgpt_util.num_tokens_from_messages(msg))
                    # if chatgpt_util.num_tokens_from_messages(msg)>=chatgpt_util.MAX_TOKENS:
                    #     response
                    try:
                        response=chatgpt_util.chatGPT_result(msg)
                        print(">>>>>>>>>>each response:\n", response)
                        reponse_list.append([me_code, old_code, *other,new_code,method_code,e1_str,e2_str])
                        reponse_list[-1].extend([[msg,num_tokes],response])
                    except:
                        traceback.print_exc()
                        reponse_list.append([me_code, old_code, *other,new_code,method_code,e1_str,e2_str])
                        reponse_list[-1].extend([[msg,num_tokes],traceback.format_exc()])
    return reponse_list
def save_csv(save_complicated_code_dir_root,sample_file_name,csv_file_name=None):
    # samples = util.load_pkl(save_complicated_code_dir_root + "chain_comparison_bool_compare/",
    #                         "comparison_find_from_boolop_and_3_examples")
    samples = util.load_pkl(save_complicated_code_dir_root + "chain_comparison_bool_compare/",
                            sample_file_name)
    #

    samples_csv = []
    for ind_sam, sample in enumerate(samples):
        try:
            bool_code, old_code, repo_name, old_path, file_html, class_name, me_name, *other, new_code, method_code, msg, response = sample
            # print("sample[-1]: ", sample[-1])
            # print("sample[-2]: ", sample[-2])
            msg = msg if isinstance(msg, list) else response[0]
            # print("all msg: ", msg)

            sys_msg, exam_msg, user_msg = chatgpt_util.get_sys_examp_user(msg[0])
            # print("bool_code:\n ", bool_code)
            # print("method_code:\n ", method_code)
            # print("response:\n ", response)

            # print("other: ",other)

            if_correct = 0
            try:
                sample[-1] = sample[-1]["choices"][0]["message"]["content"]

                # print(" sample[-1]: ", sample[-1])
                if_correct = chain_comparison_util.whether_two_compare_same_comparator(bool_code, sample[-1])
                # print("if_correct: ", if_correct)
                # a = ast.literal_eval(sample[-1])
                # a=jsonify(sample[-1])
                # a=json.loads(samples[-1])
                # sample[-1]="\n###########\n".join(a)
            except:
                pass
            real_instruction = user_msg#user_instr.replace("{{code}}", sample[0])
            ele = [repo_name, old_path, file_html, class_name, me_name, method_code, old_code, new_code, bool_code,
                   sample[-1], if_correct, real_instruction, sys_msg, exam_msg, user_msg]
        except:
            traceback.print_exc()
            # print("sample: ", len(sample))
            ele = [repo_name, old_path, file_html, class_name, me_name, method_code, old_code, new_code, bool_code,
                   sample[-1], if_correct, real_instruction, sys_msg, exam_msg, user_msg]
            # break
        samples_csv.append(ele)
    # util.save_csv(
    # save_complicated_code_dir_root + "chain_comparison_bool_compare/"+"comparison_same_operand_3_examples.csv",
    #                             samples_csv,
    #                             ["repo_name", "file_path","file_html", "class_name","me_name", "me_code", "old_code", "new_code", "bool_code", "chatGPT_code","if_correct",
    #                              "instruction"])
    # util.save_csv(
    #     save_complicated_code_dir_root + "chain_comparison_bool_compare/" + "comparison_same_operand_add_correct_3_examples.csv",
    #     samples_csv,
    #     ["repo_name", "file_path", "file_html", "class_name", "me_name", "me_code", "old_code", "new_code", "bool_code",
    #      "chatGPT_code", "if_correct",
    #      "instruction", "sys_msg", "exam_msg", "user_msg"])

    # util.save_csv(
    #     save_complicated_code_dir_root + "chain_comparison_bool_compare/" + csv_file_name,
    #     samples_csv,
    #     ["repo_name", "file_path", "file_html", "class_name", "me_name", "me_code", "old_code", "new_code", "bool_code",
    #      "chatGPT_code", "if_correct",
    #      "instruction", "sys_msg", "exam_msg", "user_msg"])
    return samples_csv