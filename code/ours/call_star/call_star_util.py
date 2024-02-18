import ast,os,sys
import copy
import traceback

import util_rewrite

code_dir = "/".join(os.path.abspath(__file__).split("/")[:-2]) + "/"
print("code path: ",code_dir)
sys.path.append(code_dir)
import chatgpt_util,random
import openai, tiktoken,ast,util
import extract_function_call,extract_value_subscript_from_args_call,call_star_instr




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
def abstract_consecutive(samples,abstract_value="iterable_zj"):
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
        tmp_list = extract_function_call.get_call_2(method_code)

        for bool_node in tmp_list:
            arg_list=extract_consecutive_subscript_node.extract_consecutive_subscripts(bool_node)
            # value_str_list = sorted(value_list)
            # value_str_list=sorted([ast.unparse(value) for value in value_list])
            for arg_seq in arg_list:
                    value=ast.unparse(arg_seq[0].value)
            # extract_subscript.subscripts = []
            # extract_subscript.find_subscripts(bool_node)
            # # print(">>>>>loop: ",ast.unparse(bool_node))
            # vars = extract_loop_var_name.extract_iterated_variables(bool_node)
            # for var in vars:
            #
            #     # print(">>>>>var: ", var,vars,extract_subscript.subscripts)
            #     elements_list = set([])
            #     for sub in extract_subscript.subscripts:
            #         if determine_subscript_name.is_subscript_var_name(sub,var):
            #             elements_list.add(ast.unparse(sub))
            #     elements_list=sorted(elements_list)
            #     if elements_list:
            #         # print("elements_list: ",elements_list)
                    me_code = ", ".join([ast.unparse(arg) for arg in arg_seq])
                    abstract_me_code=util_rewrite.replace(value,abstract_value,me_code)
                    print("abstract_me_code: ",abstract_me_code,other)
                    reponse_list.append([abstract_me_code,value,abstract_value,me_code, old_code, *other, ast.unparse(bool_node),arg_seq, new_code, method_code])

    return reponse_list


def abstract(samples,abstract_value="iterable_zj"):
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
        tmp_list = extract_function_call.get_call_2(method_code)

        for bool_node in tmp_list:
            value_list=extract_value_subscript_from_args_call.get_value(bool_node)
            value_str_list = sorted(value_list)
            # value_str_list=sorted([ast.unparse(value) for value in value_list])
            for value in value_str_list:
            # extract_subscript.subscripts = []
            # extract_subscript.find_subscripts(bool_node)
            # # print(">>>>>loop: ",ast.unparse(bool_node))
            # vars = extract_loop_var_name.extract_iterated_variables(bool_node)
            # for var in vars:
            #
            #     # print(">>>>>var: ", var,vars,extract_subscript.subscripts)
            #     elements_list = set([])
            #     for sub in extract_subscript.subscripts:
            #         if determine_subscript_name.is_subscript_var_name(sub,var):
            #             elements_list.add(ast.unparse(sub))
            #     elements_list=sorted(elements_list)
            #     if elements_list:
            #         # print("elements_list: ",elements_list)
                    me_code = ast.unparse(bool_node)
                    abstract_me_code=util_rewrite.replace(value,abstract_value,me_code)
                    print("abstract_me_code: ",abstract_me_code)
                    reponse_list.append([abstract_me_code,value,abstract_value,me_code, old_code, *other, new_code, method_code])

    return reponse_list
import extract_consecutive_subscript_node
def extract_consecutive(samples,abstract_value="iterable_zj"):
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
        tmp_list = extract_function_call.get_call_2(method_code)

        for bool_node in tmp_list:
            me_code = ast.unparse(bool_node)
            subscript_seq=extract_consecutive_subscript_node.extract_consecutive_subscripts(bool_node)
            for seq in subscript_seq:
                reponse_list.append(
                    [seq,me_code, old_code, *other, new_code, method_code])

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
        tmp_list = extract_function_call.get_call_2(method_code)

        for bool_node in tmp_list:
            value_list=extract_value_subscript_from_args_call.get_value(bool_node)
            value_str_list=sorted([ast.unparse(value) for value in value_list])
            for value in value_str_list:
            # extract_subscript.subscripts = []
            # extract_subscript.find_subscripts(bool_node)
            # # print(">>>>>loop: ",ast.unparse(bool_node))
            # vars = extract_loop_var_name.extract_iterated_variables(bool_node)
            # for var in vars:
            #
            #     # print(">>>>>var: ", var,vars,extract_subscript.subscripts)
            #     elements_list = set([])
            #     for sub in extract_subscript.subscripts:
            #         if determine_subscript_name.is_subscript_var_name(sub,var):
            #             elements_list.add(ast.unparse(sub))
            #     elements_list=sorted(elements_list)
            #     if elements_list:
            #         # print("elements_list: ",elements_list)
                    me_code = ast.unparse(bool_node)

                    # other.append(new_code)
                    # other.append(method_code)
                    real_instruction = user_instr.replace("{{code}}", me_code)
                    real_instruction = real_instruction.replace("{{value}}", value)


                    # real_instruction=real_instruction+4000*'abc'
                    print(">>>>>>>>>>Instr: ", real_instruction)
                    # continue
                    msg = chatgpt_util.format_message_2(real_instruction, examples=examples, sys_msg=sys_msg)
                    print(">>>>>>>>>>new code: ", new_code)
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
def get_response_abstract_same_subscript_value(user_instr, examples, samples, sys_msg="You are a helpful assistant."):
    reponse_list = []
    # reponse_list.append(
    #     [abstract_me_code, value, abstract_value, me_code,  , *other, ast.unparse(bool_node), arg_seq, new_code,
    #      method_code])
    #me_code is call
    # reponse_list.append([abstract_me_code, value, abstract_value, me_code, old_code, *other, new_code, method_code])

    # abstract_same_value_all
    for i,e in enumerate(samples[0]):
        print("ind, e: ",i,e)
    for abstract_me_code,value,abstract_value,*other,bool_node,arg_seq, new_code, method_code in samples:

                print(">>>>other: ", other)

                real_instruction = user_instr.replace("{{code}}",
                                                      abstract_me_code)
                real_instruction = real_instruction.replace("{{value}}", abstract_value)

                # real_instruction=real_instruction+4000*'abc'
                print(">>>>>>>>>>Instr: ", real_instruction)
                # continue
                msg = chatgpt_util.format_message_2(real_instruction, examples=examples, sys_msg=sys_msg)
                print(">>>>>>>>>>new code: ", new_code)
                num_tokes = chatgpt_util.num_tokens_from_messages(msg)
                # print("len of msg: ",chatgpt_util.num_tokens_from_messages(msg))
                # if chatgpt_util.num_tokens_from_messages(msg)>=chatgpt_util.MAX_TOKENS:
                #     response
                try:
                    response = chatgpt_util.chatGPT_result(msg)
                    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
                    reponse_list.append([abstract_me_code,value,abstract_value,*other, new_code, method_code])
                    reponse_list[-1].extend([[msg, num_tokes], response])
                except:
                    traceback.print_exc()
                    reponse_list.append([abstract_me_code,value,abstract_value,*other, new_code, method_code])
                    reponse_list[-1].extend([[msg, num_tokes], traceback.format_exc()])
        # break
    # '''
    return reponse_list

def get_response_abstract(user_instr, examples, samples, sys_msg="You are a helpful assistant."):
    reponse_list = []
    for abstract_me_code,value,abstract_value,*other, new_code, method_code in samples:


                real_instruction = user_instr.replace("{{code}}",
                                                      ", ".join([ast.unparse(arg) for arg in bool_node.args]))
                real_instruction = real_instruction.replace("{{value}}", abstract_value)

                # real_instruction=real_instruction+4000*'abc'
                print(">>>>>>>>>>Instr: ", real_instruction)
                # continue
                msg = chatgpt_util.format_message_2(real_instruction, examples=examples, sys_msg=sys_msg)
                print(">>>>>>>>>>new code: ", new_code)
                num_tokes = chatgpt_util.num_tokens_from_messages(msg)
                # print("len of msg: ",chatgpt_util.num_tokens_from_messages(msg))
                # if chatgpt_util.num_tokens_from_messages(msg)>=chatgpt_util.MAX_TOKENS:
                #     response
                try:
                    response = chatgpt_util.chatGPT_result(msg)
                    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
                    reponse_list.append([abstract_me_code,value,abstract_value,*other, new_code, method_code])
                    reponse_list[-1].extend([[msg, num_tokes], response])
                except:
                    traceback.print_exc()
                    reponse_list.append([abstract_me_code,value,abstract_value,*other, new_code, method_code])
                    reponse_list[-1].extend([[msg, num_tokes], traceback.format_exc()])
        # break
    # '''
    return reponse_list
def get_response_4(user_instr, examples, samples, sys_msg="You are a helpful assistant."):
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
        tmp_list = extract_function_call.get_call_2(method_code)

        for bool_node in tmp_list:
            value_list=extract_value_subscript_from_args_call.get_value(bool_node)
            # value_str_list=sorted([ast.unparse(value) for value in value_list])
            value_str_list=sorted(value_list)
            for value in value_str_list:

                    me_code = ast.unparse(bool_node)

                    # other.append(new_code)
                    # other.append(method_code)
                    real_instruction = user_instr.replace("{{code}}", ", ".join([ast.unparse(arg) for arg in bool_node.args]))
                    real_instruction = real_instruction.replace("{{value}}", value)


                    # real_instruction=real_instruction+4000*'abc'
                    print(">>>>>>>>>>Instr: ", real_instruction)
                    # continue
                    msg = chatgpt_util.format_message_2(real_instruction, examples=examples, sys_msg=sys_msg)
                    print(">>>>>>>>>>new code: ", new_code)
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
def parse_elements(content):
    eles_list=[]
    content_list=content.split("\n")
    for content in content_list:
        if "sequence" in content:
            eles=":".join(content.split(":")[1:])
            # remove only one element
            if "," not in eles:
                continue
            # get some answerAnswer: Yes
            # Information:
            # sequence 1: color[0], color[1], color[2], color[3] (the entire sequence is an arithmetic sequence with a common difference of 1)
            if eles.endswith(")"):
                eles_ind = eles[::-1].index('(')
                eles=eles[::-1][eles_ind+1:]
            eles_list.append(eles)
    return eles_list
def get_whether_slice_response_abstract(user_instr, examples, samples, sys_msg="You are a helpful assistant."):
    reponse_list = []
    for abstract_me_code, value, abstract_value, *other,response in samples:
        content = response["choices"][0]["message"]["content"]
        element_str_lisr = parse_elements(content)
        for e in ast.walk(ast.parse(abstract_me_code)):
            if isinstance(e,ast.Call):
                bool_node=e
                break
        arg_seq=", ".join([ast.unparse(arg) for arg in bool_node.args])

        for ele_str in element_str_lisr:
                ele_str = ele_str.strip()
                if ele_str not in arg_seq:
                    print("come here: ",ele_str, ">>>>",arg_seq,">>>>",ele_str in arg_seq)
                    continue

                # other.append(new_code)
                # other.append(method_code)
                real_instruction = user_instr.replace("{{var}}", abstract_value)
                real_instruction = real_instruction.replace("{{elements}}", ele_str)

                # real_instruction=real_instruction+4000*'abc'
                print(">>>>>>>>>>Instr: ", real_instruction)
                # continue
                msg = chatgpt_util.format_message_2(real_instruction, examples=examples, sys_msg=sys_msg)
                # print(">>>>>>>>>>new code: ", new_code)
                num_tokes = chatgpt_util.num_tokens_from_messages(msg)
                # print("len of msg: ",chatgpt_util.num_tokens_from_messages(msg))
                # if chatgpt_util.num_tokens_from_messages(msg)>=chatgpt_util.MAX_TOKENS:
                #     response
                try:
                    response = chatgpt_util.chatGPT_result(msg)
                    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
                    reponse_list.append([ele_str,abstract_me_code, value, abstract_value,arg_seq, *other])
                    reponse_list[-1].extend([[msg, num_tokes], response])
                except:
                    traceback.print_exc()
                    reponse_list.append([ele_str,abstract_me_code, value, abstract_value,arg_seq, *other])
                    reponse_list[-1].extend([[msg, num_tokes], traceback.format_exc()])
    return reponse_list

def get_whether_slice_response_abstract_same_subscript(user_instr, examples, samples, sys_msg="You are a helpful assistant."):
    reponse_list = []
    # reponse_list.append([abstract_me_code, value, abstract_value, *other, new_code, method_code])
    # for ind, e in enumerate(samples[0]):
    #     print(">>>other: ", ind, e)
    for abstract_me_code, value, abstract_value,*other,response in samples:

        content = response["choices"][0]["message"]["content"]
        element_str_lisr = parse_elements(content)
        # for e in ast.walk(ast.parse(abstract_me_code)):
        #     if isinstance(e,ast.Call):
        #         bool_node=e
        #         break
        # arg_seq=", ".join([ast.unparse(arg) for arg in bool_node.args])

        for ele_str in element_str_lisr:
                #iterable_zj[g1], iterable_zj[g2]# if "iterable_zj[1], iterable_zj[1]" not in ele_str:#iterable_zj[0], iterable_zj[1], iterable_zj[0] #iterable_zj[0], iterable_zj[-1], iterable_zj[0] #iterable_zj[1], iterable_zj[2], iterable_zj[0]
                if "iterable_zj[-11:11], iterable_zj[:]" not in ele_str:
                    continue
                # ele_str = ele_str.strip()
                # if ele_str not in arg_seq:
                #     print("come here: ",ele_str, ">>>>",arg_seq,">>>>",ele_str in arg_seq)
                #     continue

                # other.append(new_code)
                # other.append(method_code)
                real_instruction = user_instr.replace("{{var}}", abstract_value)
                real_instruction = real_instruction.replace("{{elements}}", ele_str)

                # real_instruction=real_instruction+4000*'abc'
                print(">>>>>>>>>>Instr: ", real_instruction)
                # continue
                msg = chatgpt_util.format_message_2(real_instruction, examples=examples, sys_msg=sys_msg)
                # print(">>>>>>>>>>new code: ", new_code)
                num_tokes = chatgpt_util.num_tokens_from_messages(msg)
                # print("len of msg: ",chatgpt_util.num_tokens_from_messages(msg))
                # if chatgpt_util.num_tokens_from_messages(msg)>=chatgpt_util.MAX_TOKENS:
                #     response
                try:
                    response = chatgpt_util.chatGPT_result(msg)
                    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
                    reponse_list.append([ele_str,abstract_me_code, value, abstract_value, *other])
                    for k,o_e in enumerate(other):
                        print("k,o_e: ",k,o_e)
                    reponse_list[-1].extend([[msg, num_tokes], response])
                except:
                    traceback.print_exc()
                    reponse_list.append([ele_str,abstract_me_code, value, abstract_value, *other])
                    reponse_list[-1].extend([[msg, num_tokes], traceback.format_exc()])
    return reponse_list
def get_response_5(previous_list,user_instr, examples, samples, sys_msg="You are a helpful assistant."):
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
    count=0
    for *other, old_list, new_tree, old_code, new_code, method_code in method_code_list:
        tmp_list = extract_function_call.get_call_2(method_code)

        for bool_node in tmp_list:
            value_list=extract_value_subscript_from_args_call.get_value(bool_node)
            # value_str_list=sorted([ast.unparse(value) for value in value_list])
            value_str_list=sorted(value_list)
            for value in value_str_list:
                *other,response=previous_list[count]
                count += 1
                content=response["choices"][0]["message"]["content"]
                element_str_lisr=parse_elements(content)
                for ele_str in element_str_lisr:
                    me_code = ast.unparse(bool_node)
                    ele_str=ele_str.strip()
                    # other.append(new_code)
                    # other.append(method_code)
                    real_instruction = user_instr.replace("{{var}}", value)
                    real_instruction = real_instruction.replace("{{elements}}", ele_str)


                    # real_instruction=real_instruction+4000*'abc'
                    print(">>>>>>>>>>Instr: ", real_instruction)
                    # continue
                    msg = chatgpt_util.format_message_2(real_instruction, examples=examples, sys_msg=sys_msg)
                    print(">>>>>>>>>>new code: ", new_code)
                    num_tokes = chatgpt_util.num_tokens_from_messages(msg)
                    # print("len of msg: ",chatgpt_util.num_tokens_from_messages(msg))
                    # if chatgpt_util.num_tokens_from_messages(msg)>=chatgpt_util.MAX_TOKENS:
                    #     response
                    try:
                        response = chatgpt_util.chatGPT_result(msg)
                        print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
                        reponse_list.append([me_code, old_code, *other, new_code, method_code,ele_str])
                        reponse_list[-1].extend([[msg, num_tokes], response])
                    except:
                        traceback.print_exc()
                        reponse_list.append([me_code, old_code, *other, new_code, method_code,ele_str])
                        reponse_list[-1].extend([[msg, num_tokes], traceback.format_exc()])
        # break
    # '''
    return reponse_list
def parse_slice(content):
    slice=None
    content_list = content.split("\n")
    for content in content_list:
        if "No" in content:
            return 0,slice
        if "Information" in content:
            slice=(":".join(content.split(":")[1:])).strip()

            return 1, slice
    return 0,slice
def get_response_6(previous_list):
    reponse_list = []
    # reponse_list.append([me_code, old_code, *other, new_code, method_code, ele_str])

    import util_rewrite
    for me_code, old_code, *other, new_code, method_code,element_str,_,response in previous_list:
        flag_refactor,slice_str=parse_slice(response["choices"][0]["message"]["content"])
        print(">>>>>flag_refactor,slice_str: ",flag_refactor,"'",element_str,"'","***",slice_str)
        element_str=element_str.strip()
        if flag_refactor:
            print(">>>>>old code: ",me_code,',', element_str )# element_str[0]==' ',',',',',  element_str[-1],',',element_str in me_code,"rpt[0], rpt[1], rpt[2]" in me_code,"rpt[0], rpt[1], rpt[2]"==element_str,',',"rpt[0], rpt[1], rpt[2]",',',element_str,',',len("rpt[0], rpt[1], rpt[2]"),len(element_str))

            slice_str = "*" + slice_str
            me_code_new = util_rewrite.replace_first_occur(element_str, slice_str, me_code)
            if me_code_new ==me_code:
                print("Cannot refactor: ", me_code)
                reponse_list.append([0, "Cannot refactor", element_str, slice_str, method_code,me_code, *other])
            else:
                print(">>>>>new refactored code: ",me_code)

                reponse_list.append([flag_refactor, me_code_new, element_str, slice_str, method_code,me_code, *other])
        else:
            print("Cannot refactor: ", me_code,flag_refactor,element_str, slice_str)

            reponse_list.append([flag_refactor, "Cannot refactor", element_str, slice_str, method_code,me_code, *other])


    return reponse_list

def get_rewrite(previous_list):
    reponse_list = []
    # reponse_list.append([me_code, old_code, *other, new_code, method_code, ele_str])
    # reponse_list.append([ele_str, abstract_me_code, value, abstract_value, *other])
    # import util_rewrite
    for ind, e in enumerate(previous_list[0]):
        print("ind,e: ",ind,e)
    reponse_list.append([ele_str, abstract_me_code, value, abstract_value, *other])

    for element_str, abstract_me_code, value, abstract_value,arg_seq,me_code, old_code, *other, new_code, method_code,_,_,response in previous_list:
        flag_refactor,slice_str=parse_slice(response["choices"][0]["message"]["content"])
        print(">>>>>flag_refactor,slice_str: ",flag_refactor,"'",element_str,"'","***",slice_str)
        print(">>>>>>>method_code: ",method_code)
        element_str=element_str.strip()
        if flag_refactor:
            print(">>>>>old code: ",old_code,',',me_code,',', element_str )# element_str[0]==' ',',',',',  element_str[-1],',',element_str in me_code,"rpt[0], rpt[1], rpt[2]" in me_code,"rpt[0], rpt[1], rpt[2]"==element_str,',',"rpt[0], rpt[1], rpt[2]",',',element_str,',',len("rpt[0], rpt[1], rpt[2]"),len(element_str))

            slice_str = "*" + slice_str
            me_code_new_1 = util_rewrite.replace_first_occur(element_str, slice_str, abstract_me_code)
            me_code_new = util_rewrite.replace(abstract_value, value, me_code_new_1)
            slice_str=util_rewrite.replace(abstract_value, value, slice_str)
            try:
                me_code_new = ast.unparse(ast.parse(me_code_new))
            except:
                me_code_new = me_code_new
            if me_code_new ==me_code:
                print("is 1 Cannot refactor: ", me_code)
                reponse_list.append([0, "Cannot refactor", element_str, slice_str, method_code,me_code, *other])
            else:
                print(">>>>>new refactored code: ",me_code_new)

                reponse_list.append([flag_refactor, me_code_new, element_str, slice_str, method_code,me_code, *other])
        else:
            print("Cannot refactor: ", me_code)

            reponse_list.append([flag_refactor, "Cannot refactor", element_str, slice_str, method_code,me_code, *other])


    return reponse_list

def get_rewrite_same_subscript_value(previous_list):
    reponse_list = []
    # reponse_list.append([me_code, old_code, *other, new_code, method_code, ele_str])
    # reponse_list.append([ele_str, abstract_me_code, value, abstract_value, *other])
    # import util_rewrite
    for ind, e in enumerate(previous_list[0]):
        print("ind,e: ",ind,e)

    # reponse_list.append(
    #     [abstract_me_code, value, abstract_value, me_code, old_code, *other, ast.unparse(bool_node), arg_seq, new_code,
    #      method_code])

    # reponse_list.append([ele_str, abstract_me_code, value, abstract_value, *other])
    # reponse_list[-1].extend([[msg, num_tokes], response])
    #
    # reponse_list.append([ele_str, abstract_me_code, value, abstract_value, *other])
    # reponse_list.append([ele_str, abstract_me_code, value, abstract_value, *other])
    #
    # reponse_list.append(
    #     [abstract_me_code, value, abstract_value, me_code, old_code, *other, ast.unparse(bool_node), arg_seq, new_code,
    #      method_code])
    # reponse_list.append([abstract_me_code, value, abstract_value, me_code, old_code, *other, new_code, method_code])
    # reponse_list.append([abstract_me_code, value, abstract_value, *other, new_code, method_code])
    # reponse_list.append([ele_str, abstract_me_code, value, abstract_value, *other])
    #reponse_list.append([abstract_me_code, value, abstract_value, me_code, old_code, *other, new_code, method_code])

    for element_str, abstract_me_code, value, abstract_value,me_code, old_code, *other, new_code, method_code,_,_,response in previous_list:
        flag_refactor,slice_str=parse_slice(response["choices"][0]["message"]["content"])
        print(">>>>>flag_refactor,slice_str: ",flag_refactor,"'",element_str,"'","***",slice_str)
        # print(">>>>>>>method_code: ",method_code)
        # slice_str=slice_str.strip()
        element_str=element_str.strip()
        if flag_refactor and slice_str:
            element_str_list=element_str.split(", ")
            element_str_list=[ast.unparse(ast.parse(e)) for e in element_str_list]
            element_str=(", ").join(element_str_list)
            print(">>>>>old code: ",old_code,',',me_code,',', element_str,abstract_me_code )# element_str[0]==' ',',',',',  element_str[-1],',',element_str in me_code,"rpt[0], rpt[1], rpt[2]" in me_code,"rpt[0], rpt[1], rpt[2]"==element_str,',',"rpt[0], rpt[1], rpt[2]",',',element_str,',',len("rpt[0], rpt[1], rpt[2]"),len(element_str))
            element_str_new= util_rewrite.replace(abstract_value,value, element_str)
            print(">>>>>element_str_new: ",element_str_new)
            # if "mn2_info[15], mn2_info[16], mn2_info[17]" not in element_str_new:
            #     continue

            try:
                flag_subscript=call_star_instr.is_subscript_node(slice_str)
                slice_str = "*" + slice_str if flag_subscript else "*(" + slice_str+")"
                print(">>>slice_str: ", element_str, element_str_new, slice_str)
                me_code_new_1 = util_rewrite.replace_first_occur(element_str, slice_str, abstract_me_code)
                print(">>>abstract_me_code: ", element_str, me_code, abstract_me_code, me_code_new_1, slice_str)

                # me_code_new = util_rewrite.replace(abstract_value, value, me_code_new_1)
                slice_str = util_rewrite.replace(abstract_value, value, slice_str)
                # me_code_new = ast.unparse(ast.parse(me_code_new))
                print(">>>slice_str: ", slice_str)

                me_code_new = ast.unparse(ast.parse(slice_str))
                print(">>>me_code_new: ", me_code_new)

            except:
                me_code_new = me_code_new
                continue
            print(">>>abstract_me_code: ",element_str,me_code,abstract_me_code,me_code_new_1)

            if me_code_new ==element_str_new:
                print("is 1 Cannot refactor: ", me_code,*other)
                pass
                # reponse_list.append([0, "Cannot refactor", element_str, me_code_new, method_code,element_str_new, *other])
            else:
                print(">>>>>new refactored code: ",me_code_new,*other)

                reponse_list.append([flag_refactor, me_code_new, element_str, slice_str, method_code,element_str_new, *other])
                # print("element_str, slice_str,me_code: ",element_str, slice_str,me_code)
                # for k,o_k in enumerate(other):
                #     print("k,o_k: ",k,o_k )
        else:
            continue
            # print("Cannot refactor: ", me_code,*other)
            #
            # reponse_list.append([flag_refactor, "Cannot refactor", element_str, slice_str, method_code,me_code, *other])


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
        flag_can_refactor, refactor_code, element_str, slice_str, method_code, bool_code, repo_name, old_path, file_html, class_name,me_name,*other=sample

        # flag_can_refactor, refactor_code, new_code,bool_code,method_code,repo_name, old_path, file_html, class_name,me_name,*other = sample
        # bool_code, old_code, repo_name, old_path, file_html, class_name,me_name,*other, new_code, method_code, info, response = sample

        # if flag_can_refactor:
        #     refactor_code = rewrite_for(refactor_code)
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
            ele = [repo_name, old_path, file_html, class_name, me_name, method_code, ast.unparse(ast.parse(ast.unparse(old_list[0][-2]))), new_code]
            ground_truth_list.append(ele)
            # print("new_code:\n",ast.unparse(old_list[0][-2]),new_code)
        #     break
        # if ind_sampl>2:
        #     break
    print("len of ground_truth_list: ",len(ground_truth_list))
    # ground_copy_truth_list = ground_truth_list
    ground_copy_truth_list=copy.deepcopy(ground_truth_list)
    ground_copy_truth_list=[e[offset:] for e in ground_copy_truth_list]
    predict_res=[]
    acc=0
    pre=0
    now_list=[]
    for ind, sample in enumerate(new_python_code_list):

        # reponse_list.append([flag_refactor, me_code, element_str, slice_str, method_code, me_code, *other])
    # reponse_list.append([flag_refactor, me_code_new, element_str, slice_str, method_code, me_code, *other])
    #     flag_refactor, "Cannot refactor", element_str, slice_str, method_code, me_code, *other])
        flag_can_refactor, refactor_code, element_str, slice_str, method_code, me_code, repo_name, old_path, file_html, class_name,me_name,*other=sample

        # flag_can_refactor, refactor_code,element_seq_str, slice_str,method_code,me_code,_,_,repo_name, old_path, file_html, class_name,me_name,*other = sample
        # bool_code, old_code, repo_name, old_path, file_html, class_name,me_name,*other, new_code, method_code, info, response = sample
        old_refactor_code=refactor_code
        if flag_can_refactor:
            try:
                refactor_code = ast.unparse(ast.parse(slice_str))
                print("me_code,refactor_code:\n",me_code,refactor_code)
            except:
                refactor_code =traceback.print_exc()

        e=[repo_name, old_path, file_html, class_name,me_name,method_code,me_code,refactor_code]
        print("predict ele: ", e)
        print("sample: ",sample)

        # predict_res.append(e)
        ground_pre_list=[e[offset:-1] for e in ground_copy_truth_list]
        if e in ground_copy_truth_list:
                index = ground_copy_truth_list.index(e)
                now_list.append(index)
                e[-1]=old_refactor_code
                e.extend([element_str, slice_str])
                e.append(ground_copy_truth_list[index][-1])
                e.append(1)
                ground_copy_truth_list.pop(index)
                acc+=1
                pre+=1

        elif e[:-1] in ground_pre_list:
            e[-1] = old_refactor_code
            index=ground_pre_list.index(e[:-1])
            now_list.append(index)
            e.extend([element_str, slice_str])
            e.append(ground_copy_truth_list[index][-1])
            e.append(0)
            ground_copy_truth_list.pop(index)
        else:
            continue
            e[-1] = old_refactor_code
            e.extend([element_str, slice_str])
            e.append("Cannot refactor")
            e.append(1)
            acc += 1
        predict_res.append(e + other)

    predict_res.append(["NOFOUND"])

    for ind,e in enumerate(ground_copy_truth_list):
            predict_res.append(e+[0])
    print("acc: ",acc,len(predict_res),acc/len(ground_truth_list))
    print("precision: ",pre,len(predict_res),pre/len(ground_truth_list))

    return predict_res

def get_acc_3(samples,new_python_code_list,refactor_code_list,whether_emptyset_list=None):
    offset=0#-2
    ground_truth_list=[]
    for ind_sampl, sample_method in enumerate(samples):
        for code in sample_method:
            repo_name, old_path, file_html, class_name,me_name, old_list, new_tree,\
                old_code,new_code, method_code=code
            # break
            *other, old_list, new_tree, \
            old_code, new_code, method_code = code
            ele = [repo_name, old_path, file_html, class_name, me_name, method_code, ast.unparse(ast.parse(ast.unparse(old_list[0][-2]))), new_code]
            ground_truth_list.append(ele)
            # print("new_code:\n",ast.unparse(old_list[0][-2]),new_code)
        #     break
        # if ind_sampl>2:
        #     break
    print("len of ground_truth_list: ",len(ground_truth_list))
    # ground_copy_truth_list = ground_truth_list
    ground_copy_truth_list=copy.deepcopy(ground_truth_list)
    ground_copy_truth_list=[e[offset:] for e in ground_copy_truth_list]
    predict_res=[]
    acc=0
    pre=0
    now_list=[]
    for ind, sample in enumerate(new_python_code_list):
        # for i,s in enumerate(sample):
        #     print("i,sample: ",i,s)
        # flag_refactor, me_code_new, element_str, slice_str, method_code, me_code, *other])

        # reponse_list.append([me_code, old_code, *other, new_code, method_code, ele_str])
        # reponse_list.append([flag_refactor, me_code_new, element_str, slice_str, method_code, me_code, *other])

        # reponse_list.append([flag_refactor, me_code, element_str, slice_str, method_code, me_code, *other])
    # reponse_list.append([flag_refactor, me_code_new, element_str, slice_str, method_code, me_code, *other])
    #     flag_refactor, "Cannot refactor", element_str, slice_str, method_code, me_code, *other])
    #     flag_can_refactor, refactor_code, element_str, slice_str, method_code, arg_str,ele_str,bool_code,*other, repo_name, old_path, file_html, class_name,me_name=sample
    #     ele_str, abstract_me_code, value, abstract_value, arg_seq, *other
        flag_can_refactor, refactor_code, element_str, slice_str, method_code, me_code, repo_name, old_path, file_html, class_name,me_name,*other=sample
        # reponse_list.append([ele_str, abstract_me_code, value, abstract_value, *other])

        # flag_can_refactor, refactor_code,element_seq_str, slice_str,method_code,me_code,_,_,repo_name, old_path, file_html, class_name,me_name,*other = sample
        # bool_code, old_code, repo_name, old_path, file_html, class_name,me_name,*other, new_code, method_code, info, response = sample
        old_refactor_code=refactor_code
        if flag_can_refactor:
            try:
                refactor_code = ast.unparse(ast.parse(slice_str))
                print("me_code,refactor_code:\n",me_code,refactor_code)
            except:
                refactor_code =traceback.print_exc()

        e=[repo_name, old_path, file_html, class_name,me_name,method_code,me_code,refactor_code]
        # print("predict ele: ", e)

        # predict_res.append(e)
        ground_pre_list=[e[offset:-1] for e in ground_copy_truth_list]
        if e in ground_copy_truth_list:
                index = ground_copy_truth_list.index(e)
                now_list.append(index)
                e[-1]=old_refactor_code
                e.extend([element_str, slice_str])
                e.append(ground_copy_truth_list[index][-1])
                e.append(1)
                ground_copy_truth_list.pop(index)
                acc+=1
                pre+=1

        elif e[:-1] in ground_pre_list:
            e[-1] = old_refactor_code
            index=ground_pre_list.index(e[:-1])
            now_list.append(index)
            e.extend([element_str, slice_str])
            e.append(ground_copy_truth_list[index][-1])
            e.append(0)
            ground_copy_truth_list.pop(index)
        else:
            continue
            e[-1] = old_refactor_code
            e.extend([element_str, slice_str])
            e.append("Cannot refactor")
            e.append(1)
            acc += 1
        predict_res.append(e + other)

    predict_res.append(["NOFOUND"])

    for ind,e in enumerate(ground_copy_truth_list):
            predict_res.append(e+[0])
    print("acc: ",acc,len(predict_res),acc/len(ground_truth_list))
    print("precision: ",pre,len(predict_res),pre/len(ground_truth_list))

    return predict_res

def get_acc_4(samples,new_python_code_list,refactor_code_list,whether_emptyset_list=None):
    offset=0#-2
    reponse_list=[]
    ground_truth_list=[]
    for ind_sampl, sample_method in enumerate(samples):
        for code in sample_method:
            repo_name, old_path, file_html, class_name,me_name, old_list, new_tree,\
                old_code,new_code, method_code=code
            # break
            *other, old_list, new_tree, \
            old_code, new_code, method_code = code
            ele = [repo_name, old_path, file_html, class_name, me_name, method_code,old_code, new_code]
            ground_truth_list.append(ele)
            # print("old_code: ",old_code)
            # return None
            # print("new_code:\n",ast.unparse(old_list[0][-2]),new_code)
        #     break
        # if ind_sampl>2:
        #     break
    print("len of ground_truth_list: ",len(ground_truth_list))
    # ground_copy_truth_list = ground_truth_list
    ground_copy_truth_list=copy.deepcopy(ground_truth_list)
    ground_copy_truth_list=[e[offset:] for e in ground_copy_truth_list]
    chatgpt_code_list=[]
    predict_res=[]
    acc=0
    pre=0
    now_list=[]
    cannot_refactor_other_list=[]
    for ind, sample in enumerate(new_python_code_list):
        # print("sample: ",sample)
        # for i,s in enumerate(sample):
        #     print("i,sample: ",i,s)

        # reponse_list.append([me_code, old_code, *other, new_code, method_code, ele_str])
        # reponse_list.append([flag_refactor, me_code_new, element_str, slice_str, method_code, me_code, *other])

        # reponse_list.append([flag_refactor, me_code, element_str, slice_str, method_code, me_code, *other])
    # reponse_list.append([flag_refactor, me_code_new, element_str, slice_str, method_code, me_code, *other])
    #     flag_refactor, "Cannot refactor", element_str, slice_str, method_code, me_code, *other])
    #     flag_can_refactor, refactor_code, element_str, slice_str, method_code, arg_str,ele_str,bool_code,*other, repo_name, old_path, file_html, class_name,me_name=sample
    #     ele_str, abstract_me_code, value, abstract_value, arg_seq, *other
    #     reponse_list.append([flag_refactor, me_code_new, element_str, slice_str, method_code, me_code, *other])
    #     reponse_list.append([flag_refactor, me_code_new, element_str, slice_str, method_code, me_code, *other])

        flag_can_refactor, refactor_code, element_str, slice_str, method_code, me_code, repo_name, old_path, file_html, class_name,me_name,*other=sample
        # reponse_list.append([ele_str, abstract_me_code, value, abstract_value, *other])
        # reponse_list.append([0, "Cannot refactor", element_str, slice_str, method_code, me_code, *other])

        # flag_can_refactor, refactor_code,element_seq_str, slice_str,method_code,me_code,_,_,repo_name, old_path, file_html, class_name,me_name,*other = sample
        # bool_code, old_code, repo_name, old_path, file_html, class_name,me_name,*other, new_code, method_code, info, response = sample

        old_refactor_code=refactor_code
        # if flag_can_refactor:
        #     try:
        #         refactor_code = ast.unparse(ast.parse(slice_str))
        #         print("me_code,refactor_code:\n",me_code,refactor_code)
        #     except:
        #         refactor_code =traceback.print_exc()

        e=[repo_name, old_path, file_html, class_name,me_name,method_code,me_code,refactor_code]
        if flag_can_refactor and refactor_code:
            chatgpt_code_list.append(e)
        # print("predict ele: ", e)

        # predict_res.append(e)
        ground_pre_list=[e[offset:-1] for e in ground_copy_truth_list]
        if e in ground_copy_truth_list:
                index = ground_copy_truth_list.index(e)
                now_list.append(index)
                e[-1]=old_refactor_code
                e.extend([element_str, slice_str])
                e.append(ground_copy_truth_list[index][-1])
                e.append(1)
                ground_copy_truth_list.pop(index)
                acc+=1
                pre+=1

        elif e[:-1] in ground_pre_list:
            e[-1] = old_refactor_code
            index=ground_pre_list.index(e[:-1])
            now_list.append(index)
            e.extend([element_str, slice_str])
            e.append(ground_copy_truth_list[index][-1])
            e.append(0)
            ground_copy_truth_list.pop(index)
        else:

            e[-1] = old_refactor_code
            e.extend([element_str, slice_str])
            e.append("Cannot refactor")
            e.append(2)
            cannot_refactor_other_list.append(e+other)
            continue
            acc += 1

        predict_res.append(e + other)
    # cannot_refactor_other_list.append
    predict_res.extend(cannot_refactor_other_list)
    predict_res.append(["NOFOUND"])

    for ind,e in enumerate(ground_copy_truth_list):
            predict_res.append(e+[0])
    print("acc: ",acc,len(predict_res),acc/len(ground_truth_list))
    print("precision: ",pre,len(predict_res),pre/len(ground_truth_list))

    return predict_res,chatgpt_code_list,ground_truth_list
def save_csv(samples,refactor_code_list):
    # samples = util.load_pkl(save_complicated_code_dir_root + "chain_comparison_bool_compare/",
    #                         "comparison_find_from_boolop_and_3_examples")

    #

    samples_csv = []
    for ind_sam, sample in enumerate(samples):
        # print("sample: ",sample)
        try:
            # bool_code, old_code, repo_name, old_path, file_html, class_name, me_name, *other, new_code, method_code, info, response = sample

            bool_code, old_code, repo_name, old_path, file_html, class_name, me_name, *other, new_code, method_code, msg, response = sample
            # print("sample[-1]: ", sample[-1])
            # print("sample[-2]: ", sample[-2])
            msg = msg if isinstance(msg, list) else response[0]
            # print("all msg: ", msg)

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