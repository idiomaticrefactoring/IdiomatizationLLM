import ast,os,sys
import copy
import traceback
code_dir = "/".join(os.path.abspath(__file__).split("/")[:-2]) + "/"
print("code path: ",code_dir)
sys.path.append(code_dir)
import chatgpt_util,random
import openai, tiktoken,ast,util
import extract_for,extract_loop_var_name,extract_subscript,determine_subscript_name
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



def whether_same_new_code(bool_code, new_code):
    try:
        if ast.unparse(ast.parse(bool_code))==ast.unparse(ast.parse(new_code)):
            return 1
    except:
        traceback.print_exc()
    return 0
def get_each_repsonse(code,user_instr,examples,sys_msg="You are a helpful assistant."):
    real_instruction = user_instr.replace("{{code}}", code)
    print(">>>>>>>>real_instruction: ",real_instruction)
    msg = chatgpt_util.format_message_2(real_instruction, examples=examples, sys_msg=sys_msg)
    # print(">>>>>>>>msg: ",msg)
    response=chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>response: ",response)
    return msg, response['choices'][0]['message']["content"]

def extract_new_Python_code(response_content):
    try:
        answer_list=response_content.split("\n")
        for answer in answer_list:
            if "New Python code" in answer or "New Python" in answer:
                python_code = answer.split(":")[-1].strip()
                return python_code
    except:
        traceback.print_exc()
        pass
    return "Do not have Python code!"

def get_response(user_instr, examples, samples, sys_msg="You are a helpful assistant."):
    reponse_list = []
    method_code_list=[]
    for ind_sampl, sample_method in enumerate(samples):
        for code in sample_method:
            # repo_name, old_path, file_html, class_name,me_name, old_list, new_tree,\
            #     old_code,new_code, method_code=code
            # break
            *other, old_list, new_tree, \
            old_code, new_code, method_code = code
            # print("method_code: ", method_code)
            method_code_list.append([*other, old_list, new_tree,old_code, new_code, method_code])
            break
    for *other, old_list, new_tree,old_code, new_code, method_code in method_code_list:
            tmp_list = extract_for.get_for(method_code)
            for bool_node in tmp_list:
                me_code = ast.unparse(bool_node)

                # other.append(new_code)
                # other.append(method_code)
                real_instruction = user_instr.replace("{{code}}", me_code)

                # real_instruction=real_instruction+4000*'abc'
                print(">>>>>>>>>>Instr: ", real_instruction)
                # continue
                msg = chatgpt_util.format_message_2(real_instruction, examples=examples, sys_msg=sys_msg)
                # print(">>>>>>>>>>each msg: ", msg)
                num_tokes = chatgpt_util.num_tokens_from_messages(msg)
                # print("len of msg: ",chatgpt_util.num_tokens_from_messages(msg))
                # if chatgpt_util.num_tokens_from_messages(msg)>=chatgpt_util.MAX_TOKENS:
                #     response
                try:
                    response = chatgpt_util.chatGPT_result(msg)
                    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
                    reponse_list.append([me_code, old_code, *other, new_code, method_code])
                    reponse_list[-1].extend([[msg, num_tokes], response])
                except:
                    traceback.print_exc()
                    reponse_list.append([me_code, old_code, *other, new_code, method_code])
                    reponse_list[-1].extend([[msg, num_tokes], traceback.format_exc()])
            # break
    # '''
    return reponse_list

def get_response_2(user_instr, examples, samples, sys_msg="You are a helpful assistant."):
    reponse_list = []
    method_code_list = []
    for ind_sampl, sample_method in enumerate(samples):
        for code in sample_method:
            # repo_name, old_path, file_html, class_name,me_name, old_list, new_tree,\
            #     old_code,new_code, method_code=code
            # break
            *other, old_list, new_tree, \
            old_code, new_code, method_code = code
            # print("method_code: ", method_code)
            method_code_list.append([*other, old_list, new_tree, old_code, new_code, method_code])
            break
    for *other, old_list, new_tree, old_code, new_code, method_code in method_code_list:
        tmp_list = extract_for.get_for(method_code)
        for bool_node in tmp_list:
            vars=extract_loop_var_name.extract_iterated_variables(bool_node)
            vars=['"'+var+'"' for var in vars]
            me_code = ast.unparse(bool_node)

            # other.append(new_code)
            # other.append(method_code)
            real_instruction = user_instr.replace("{{code}}", me_code)
            real_instruction = real_instruction.replace("{{var}}", " and ".join(vars))

            # real_instruction=real_instruction+4000*'abc'
            print(">>>>>>>>>>Instr: ", real_instruction)
            # continue
            msg = chatgpt_util.format_message_2(real_instruction, examples=examples, sys_msg=sys_msg)
            # print(">>>>>>>>>>each msg: ", msg)
            num_tokes = chatgpt_util.num_tokens_from_messages(msg)
            # print("len of msg: ",chatgpt_util.num_tokens_from_messages(msg))
            # if chatgpt_util.num_tokens_from_messages(msg)>=chatgpt_util.MAX_TOKENS:
            #     response
            try:
                response = chatgpt_util.chatGPT_result(msg)
                print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
                reponse_list.append([me_code, old_code, *other, new_code, method_code])
                reponse_list[-1].extend([[msg, num_tokes], response])
            except:
                traceback.print_exc()
                reponse_list.append([me_code, old_code, *other, new_code, method_code])
                reponse_list[-1].extend([[msg, num_tokes], traceback.format_exc()])
        # break
    # '''
    return reponse_list

def get_response_3(user_instr, examples, samples, sys_msg="You are a helpful assistant."):
    reponse_list = []
    method_code_list = []
    for ind_sampl, sample_method in enumerate(samples):
        for code in sample_method:
            # repo_name, old_path, file_html, class_name,me_name, old_list, new_tree,\
            #     old_code,new_code, method_code=code
            # break
            *other, old_list, new_tree, \
            old_code, new_code, method_code = code
            # print("method_code: ", method_code)
            method_code_list.append([*other, old_list, new_tree, old_code, new_code, method_code])
            break
    for *other, old_list, new_tree, old_code, new_code, method_code in method_code_list:
        tmp_list = extract_for.get_for(method_code)

        for bool_node in tmp_list:
            extract_subscript.subscripts = []
            extract_subscript.find_subscripts(bool_node)
            # print(">>>>>loop: ",ast.unparse(bool_node))
            vars = extract_loop_var_name.extract_iterated_variables(bool_node)
            for var in vars:

                # print(">>>>>var: ", var,vars,extract_subscript.subscripts)
                elements_list = set([])
                for sub in extract_subscript.subscripts:
                    if determine_subscript_name.is_subscript_var_name(sub,var):
                        elements_list.add(ast.unparse(sub))
                elements_list=sorted(elements_list)
                if elements_list:
                    # print("elements_list: ",elements_list)
                    me_code = ast.unparse(bool_node)

                    # other.append(new_code)
                    # other.append(method_code)
                    real_instruction = user_instr.replace("{{code}}", me_code)
                    real_instruction = real_instruction.replace("{{var}}", var)
                    real_instruction = real_instruction.replace("{{element}}", "\n".join(elements_list))

                    # real_instruction=real_instruction+4000*'abc'
                    print(">>>>>>>>>>Instr: ", real_instruction)
                    # continue
                    msg = chatgpt_util.format_message_2(real_instruction, examples=examples, sys_msg=sys_msg)
                    # print(">>>>>>>>>>each msg: ", msg)
                    num_tokes = chatgpt_util.num_tokens_from_messages(msg)
                    # print("len of msg: ",chatgpt_util.num_tokens_from_messages(msg))
                    # if chatgpt_util.num_tokens_from_messages(msg)>=chatgpt_util.MAX_TOKENS:
                    #     response
                    try:
                        response = chatgpt_util.chatGPT_result(msg)
                        print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
                        reponse_list.append([me_code, old_code, *other, new_code, method_code])
                        reponse_list[-1].extend([[msg, num_tokes], response])
                    except:
                        traceback.print_exc()
                        reponse_list.append([me_code, old_code, *other, new_code, method_code])
                        reponse_list[-1].extend([[msg, num_tokes], traceback.format_exc()])
        # break
    # '''
    return reponse_list
    # util.save_pkl(save_complicated_code_dir_root + "chain_comparison_bool_compare/",
    #                           "comparison_find_from_boolop_and_3_examples",
    #                           reponse_list)

def get_response_abstract_target(user_instr, examples, samples, sys_msg="You are a helpful assistant."):
    reponse_list = []
    method_code_list = []
    for ind_sampl, sample_method in enumerate(samples):
        for code in sample_method:
            # repo_name, old_path, file_html, class_name,me_name, old_list, new_tree,\
            #     old_code,new_code, method_code=code
            # break
            *other, old_list, new_tree, \
            old_code, new_code, method_code = code
            # print("method_code: ", method_code)
            method_code_list.append([*other, old_list, new_tree, old_code, new_code, method_code])
            break
    for *other, old_list, new_tree, old_code, new_code, method_code in method_code_list:
        tmp_list = extract_for.get_for(method_code)

        for bool_node in tmp_list:
            extract_subscript.subscripts = []
            extract_subscript.find_subscripts(bool_node)
            # print(">>>>>loop: ",ast.unparse(bool_node))
            vars = extract_loop_var_name.extract_iterated_variables(bool_node)
            for var in vars:

                # print(">>>>>var: ", var,vars,extract_subscript.subscripts)
                elements_list = set([])
                for sub in extract_subscript.subscripts:
                    if determine_subscript_name.is_subscript_var_name(sub,var):
                        elements_list.add(ast.unparse(sub))
                elements_list=sorted(elements_list)
                if elements_list:

                    # print("elements_list: ",elements_list)
                    me_code = ast.unparse(bool_node)
                    abstract_var="e"
                    # if "call_args[0][1]" not in elements_list:#item[2] hseq[0][0] inputs[0][:inputs[0].index('(')] i[0][::-1] "xxx[0]" "fig_temp['data']" item[0] edge[0] b[4] thing[1] hseq[0][0] l2[uv_layer] script['id']
                    #     continue
                    element_str="\n".join(elements_list)

                    element_str= element_str.replace(var, abstract_var)

                    # print("element_str: ", element_str)
                    # return None
                    # other.append(new_code)
                    # other.append(method_code)
                    real_instruction = user_instr.replace("{{code}}", me_code)
                    real_instruction = real_instruction.replace("{{var}}", abstract_var)
                    real_instruction = real_instruction.replace("{{element}}", element_str)

                    # real_instruction=real_instruction+4000*'abc'
                    print(">>>>>>>>>>Instr: ", real_instruction)
                    # continue
                    msg = chatgpt_util.format_message_2(real_instruction, examples=examples, sys_msg=sys_msg)
                    # print(">>>>>>>>>>each msg: ", msg)
                    num_tokes = chatgpt_util.num_tokens_from_messages(msg)
                    # print("len of msg: ",chatgpt_util.num_tokens_from_messages(msg))
                    # if chatgpt_util.num_tokens_from_messages(msg)>=chatgpt_util.MAX_TOKENS:
                    #     response
                    try:
                        response = chatgpt_util.chatGPT_result(msg)
                        print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
                        reponse_list.append([me_code, old_code, *other, new_code, method_code,var,abstract_var])
                        reponse_list[-1].extend([[msg, num_tokes], response])
                        # return
                    except:
                        traceback.print_exc()
                        reponse_list.append([me_code, old_code, *other, new_code, method_code,var,abstract_var])
                        reponse_list[-1].extend([[msg, num_tokes], traceback.format_exc()])
        # break
    # '''
    return reponse_list
import ast
class Rewrite(ast.NodeTransformer):
    def visit_Name(self, node):
        return ast.Name(id='data', ctx=ast.Load())
def rewrite_for(new_code):
    try:
        for e in ast.walk(ast.parse(new_code)):
            if isinstance(e, ast.For):
                e.target = Rewrite().visit(e.target)
                return ast.unparse(e.target)
    except:
        return new_code

def rewrite_ass(new_code):
    try:
        for e in ast.walk(ast.parse(new_code)):
            if isinstance(e, ast.Assign):
                e=ast.parse(ast.unparse(e).split("=")[0])
                e = Rewrite().visit(e)
                print(">>> Assign ast.unparse(e): ",ast.unparse(e))
                return ast.unparse(e)
    except:
        traceback.print_exc()
        return new_code
def get_acc(samples,new_python_code_list,refactor_code_list,whether_emptyset_list=None):
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
            print("new_code:\n ",new_code)
            new_code=new_code.split("\n")[0]
            new_code+="\n    pass"
            ele[-1] =rewrite_for(new_code)


        #     break
        # if ind_sampl>2:
        #     break
    # ground_copy_truth_list = ground_truth_list
    ground_copy_truth_list=copy.deepcopy(ground_truth_list)
    ground_copy_truth_list=[e[offset:] for e in ground_copy_truth_list]
    predict_res=[]
    acc=0
    pre=0
    for ind, sample in enumerate(new_python_code_list):
        flag_can_refactor, refactor_code, new_code,bool_code,method_code,repo_name, old_path, file_html, class_name,me_name,*other = sample
        # bool_code, old_code, repo_name, old_path, file_html, class_name,me_name,*other, new_code, method_code, info, response = sample

        if flag_can_refactor:
            refactor_code = rewrite_for(refactor_code)
        e=[repo_name, old_path, file_html, class_name,me_name,method_code,bool_code,refactor_code]
        # print("predict ele: ", e)

        # predict_res.append(e)
        ground_pre_list=[e[offset:-1] for e in ground_copy_truth_list]
        if e in ground_copy_truth_list:
                index = ground_copy_truth_list.index(e)
                e.append(ground_copy_truth_list[index][-1])
                e.append(1)
                ground_copy_truth_list.pop(index)
                acc+=1
                pre+=1

        elif e[:-1] in ground_pre_list:


            index=ground_pre_list.index(e[:-1])
            e.append(ground_copy_truth_list[index][-1])
            e.append(0)
            ground_copy_truth_list.pop(index)
        else:
            e.append("Cannot refactor")
            e.append(1)
            acc += 1
        predict_res.append(e + other)


    print("acc: ",acc,len(new_python_code_list),acc/len(new_python_code_list))
    print("precision: ",pre,len(ground_truth_list),pre/len(ground_truth_list))

    return predict_res


def get_acc_2(samples,new_python_code_list,refactor_code_list,whether_emptyset_list=None):
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
            print("new_code:\n ",new_code)
            new_code=new_code.split("\n")[0]
            new_code+="\n    pass"
            ele[-1] =rewrite_for(new_code)
            print("ele[-1]:\n ",ele[-1])



        #     break
        # if ind_sampl>2:
        #     break
    # ground_copy_truth_list = ground_truth_list
    ground_copy_truth_list=copy.deepcopy(ground_truth_list)
    ground_copy_truth_list=[e[offset:] for e in ground_copy_truth_list]
    predict_res=[]
    acc=0
    pre=0
    for ind, sample in enumerate(new_python_code_list):
        flag_can_refactor, refactor_code, new_code,bool_code,method_code,repo_name, old_path, file_html, class_name,me_name,*other = sample
        # bool_code, old_code, repo_name, old_path, file_html, class_name,me_name,*other, new_code, method_code, info, response = sample
        old_refactor_code=refactor_code
        if flag_can_refactor:
            print("old refactor_code:\n ",refactor_code)
            refactor_code = rewrite_ass(refactor_code.split("\n")[1].strip())
            print("refactor_code:\n ",refactor_code)

        e=[repo_name, old_path, file_html, class_name,me_name,method_code,bool_code,refactor_code]
        # print("predict ele: ", e)

        # predict_res.append(e)
        ground_pre_list=[e[offset:-1] for e in ground_copy_truth_list]
        if e in ground_copy_truth_list:
                index = ground_copy_truth_list.index(e)
                e[-1]=old_refactor_code
                e.append(ground_copy_truth_list[index][-1])
                e.append(1)
                ground_copy_truth_list.pop(index)
                acc+=1
                pre+=1

        elif e[:-1] in ground_pre_list:

            e[-1] = old_refactor_code
            index=ground_pre_list.index(e[:-1])
            e.append(ground_copy_truth_list[index][-1])
            e.append(0)
            ground_copy_truth_list.pop(index)
        else:
            e[-1] = old_refactor_code
            e.append("Cannot refactor")
            e.append(1)
            acc += 1
        predict_res.append(e + other)


    print("acc: ",acc,len(new_python_code_list),acc/len(new_python_code_list))
    print("precision: ",pre,len(ground_truth_list),pre/len(ground_truth_list))

    return predict_res

def get_acc_3(samples,new_python_code_list,refactor_code_list,whether_emptyset_list=None):
    offset=0#-2
    ground_truth_list=[]
    real_ground_truth_list=[]
    for ind_sampl, sample_method in enumerate(samples):
        for code in sample_method:
            repo_name, old_path, file_html, class_name,me_name, old_list, new_tree,\
                old_code,new_code, method_code=code
            # break
            *other, old_list, new_tree, \
            old_code, new_code, method_code = code
            ele = [repo_name, old_path, file_html, class_name, me_name, method_code, old_code, new_code]
            ele.append(new_code)
            try:
                new_code = ast.unparse(ast.parse(new_code))
            except:
                new_code = new_code
            real_ground_truth_list.append([repo_name, old_path, file_html, class_name, me_name, method_code, old_code, new_code])
            print("new_code:\n ",new_code)
            new_code=new_code.split("\n")[0]
            new_code+="\n    pass"
            ele[-2] =rewrite_for(new_code)
            ground_truth_list.append(ele)

            # print("ele[-1]:\n ",ele[-1])
            print("ele[-2]:\n ",ele[-2])




        #     break
        # if ind_sampl>2:
        #     break
    # ground_copy_truth_list = ground_truth_list
    ground_copy_truth_list=copy.deepcopy(ground_truth_list)
    ground_copy_truth_list=[e[offset:-1] for e in ground_copy_truth_list]

    ground_copy_truth_list_2 = copy.deepcopy(ground_truth_list)
    # ground_copy_truth_list_2 = [e[offset:-1] for e in ground_copy_truth_list]
    predict_res=[]
    chatgpt_refactor_list=[]
    acc=0
    pre=0
    for ind, sample in enumerate(new_python_code_list):
        flag_can_refactor, refactor_code, new_code,bool_code,method_code,repo_name, old_path, file_html, class_name,me_name,*other = sample
        # bool_code, old_code, repo_name, old_path, file_html, class_name,me_name,*other, new_code, method_code, info, response = sample
        old_refactor_code=refactor_code
        try:
            old_refactor_code = ast.unparse(ast.parse(old_refactor_code))
        except:
            old_refactor_code = old_refactor_code
        if flag_can_refactor:

            print("old refactor_code:\n ",refactor_code)
            refactor_code = rewrite_ass(refactor_code.split("\n")[1].strip())
            print("refactor_code:\n ",refactor_code)
        # else:
        #     continue

        e=[repo_name, old_path, file_html, class_name,me_name,method_code,bool_code,refactor_code]
        chatgpt_refactor_list.append([repo_name, old_path, file_html, class_name,me_name,method_code,bool_code,old_refactor_code])
        # print("predict ele: ", e)

        # predict_res.append(e)
        ground_pre_list=[e[offset:-1] for e in ground_copy_truth_list]
        if e in ground_copy_truth_list:
                index = ground_copy_truth_list.index(e)
                e[-1]=old_refactor_code
                e.append(ground_copy_truth_list_2[index][-2])
                e.append(ground_copy_truth_list_2[index][-1])
                e.append(1)
                ground_copy_truth_list.pop(index)
                ground_copy_truth_list_2.pop(index)
                acc+=1
                pre+=1

        elif e[:-1] in ground_pre_list:

            e[-1] = old_refactor_code
            index=ground_pre_list.index(e[:-1])
            e.append(ground_copy_truth_list_2[index][-2])
            e.append(ground_copy_truth_list_2[index][-1])

            e.append(0)
            ground_copy_truth_list.pop(index)
            ground_copy_truth_list_2.pop(index)
        else:
            e[-1] = old_refactor_code
            e.append("Cannot refactor")
            e.append("Cannot refactor")

            e.append(2)
            acc += 1
        predict_res.append(e + other)


    print("acc: ",acc,len(new_python_code_list),acc/len(new_python_code_list))
    print("precision: ",pre,len(ground_truth_list),pre/len(ground_truth_list))

    return predict_res,real_ground_truth_list,chatgpt_refactor_list


def save_csv(samples,refactor_code_list):
    # samples = util.load_pkl(save_complicated_code_dir_root + "chain_comparison_bool_compare/",
    #                         "comparison_find_from_boolop_and_3_examples")

    #

    samples_csv = []
    for ind_sam, sample in enumerate(samples):
        print("sample: ",sample)
        try:
            # bool_code, old_code, repo_name, old_path, file_html, class_name, me_name, *other, new_code, method_code, info, response = sample

            bool_code, old_code, repo_name, old_path, file_html, class_name, me_name, *other, new_code, method_code, msg, response = sample
            # print("sample[-1]: ", sample[-1])
            # print("sample[-2]: ", sample[-2])
            msg = msg if isinstance(msg, list) else response[0]
            print("all msg: ", msg)

            sys_msg, exam_msg, user_msg = chatgpt_util.get_sys_examp_user(msg[0])
            print("bool_code:\n ", bool_code)
            # print("method_code:\n ", method_code)
            # print("response:\n ", response)
            print("new_code:\n ", new_code)
            if refactor_code_list:
                print("generate refactored code: ",refactor_code_list[ind_sam])

            if_correct = 0
            try:
                sample[-1] = sample[-1]["choices"][0]["message"]["content"]
                if refactor_code_list:
                    print(" sample[-1]: ", sample[-1])
                    if_correct = whether_same_new_code(refactor_code_list[ind_sam], new_code)
                    print("if_correct: ", if_correct)
                else:
                    if_correct=None
                # a = ast.literal_eval(sample[-1])
                # a=jsonify(sample[-1])
                # a=json.loads(samples[-1])
                # sample[-1]="\n###########\n".join(a)
            except:
                pass
            real_instruction = user_msg#user_instr.replace("{{code}}", sample[0])
            ele = [repo_name, old_path, file_html, class_name, me_name, method_code, old_code, new_code, bool_code,
                   sample[-1], refactor_code_list[ind_sam],if_correct, real_instruction, sys_msg, exam_msg, user_msg]
        except:
            traceback.print_exc()
            print("sample: ", len(sample))
            ele = [repo_name, old_path, file_html, class_name, me_name, method_code, old_code, new_code, bool_code,
                   sample[-1],refactor_code_list[ind_sam], if_correct, real_instruction, sys_msg, exam_msg, user_msg]
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