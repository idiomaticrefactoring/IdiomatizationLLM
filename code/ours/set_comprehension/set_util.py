import ast,os,sys
import copy
import traceback

import util_rewrite

code_dir = "/".join(os.path.abspath(__file__).split("/")[:-2]) + "/"
print("code path: ",code_dir)
sys.path.append(code_dir)
import chatgpt_util,random
import openai, tiktoken,ast,util,chat_gpt_ast_util
import code_extract_for,code_extract_for_determine_has_add_func
def parse_refactor_code(content):

    content_list=content.split("\n")
    for content in content_list:
        if "Answer: No" in content:
            return 0,None
    return 1, content_list[-1].strip()
def get_response_instr(user_instr, examples, samples, sys_msg="You are a helpful assistant."):
        reponse_list = []
        method_code_list = []
        for ind_sampl, sample_method in enumerate(samples):
            for code in sample_method:
                # repo_name, old_path, file_html, class_name,me_name, old_list, new_tree,\
                #     old_code,new_code, method_code=code
                # break
                *other, old_list, new_tree, \
                old_code, new_code, method_code = code
                print(">>>>method_code: ", method_code)
                print(">>>>old_list: ", old_list)
                print(">>>>old_code: ", old_code)
                print(">>>>new_code: ", new_code)

                method_code_list.append([*other, old_list, new_tree, old_code, new_code, method_code])
                break
            # break
        for *other, old_list, new_tree, old_code, new_code, method_code in method_code_list:
            tmp_list = code_extract_for.get_for_2(method_code)

            for bool_node in tmp_list:
                whether_append=code_extract_for_determine_has_append_func.contains_append(bool_node)
                if not whether_append:
                    continue
                me_code=ast.unparse(bool_node)
                real_instruction = user_instr.replace("{{code}}", ast.unparse(bool_node))

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
def get_response_directly_refactor(user_instr, examples, samples, sys_msg="You are a helpful assistant."):
        reponse_list = []
        method_code_list = []
        one_other=[]
        for ind_sampl, sample_method in enumerate(samples):
            for code in sample_method:
                # repo_name, old_path, file_html, class_name,me_name, old_list, new_tree,\
                #     old_code,new_code, method_code=code
                # break
                *other, old_list, new_tree, \
                old_code, new_code, method_code = code
                # if other in one_other:
                #     continue
                # one_other.append(other)
                # print(">>>>method_code: ", method_code)
                # print(">>>>old_list: ", old_list)
                # print(">>>>old_code: ", old_code)
                # print(">>>>new_code: ", new_code)

                method_code_list.append([*other, old_list, new_tree, old_code, new_code, method_code])
                break
            # break
        for *other, old_list, new_tree, old_code, new_code, method_code in method_code_list:
            # if "do_setup$1697" not in other:
            #     continue
            # print(other[2:])
            # if "for include in line.split()[1:]:" not in method_code:
            #     continue
            tmp_list = code_extract_for.get_for_2(method_code)
            all_me_code=[]
            print("tmp_list: ",len(tmp_list))
            for bool_node in tmp_list:
                whether_append = code_extract_for_determine_has_add_func.if_has_add(bool_node)
                if not whether_append:
                    continue
                me_code=ast.unparse(bool_node)
                real_instruction = user_instr.replace("{{code}}", ast.unparse(bool_node))

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
                    content = response["choices"][0]["message"]["content"]
                    flag_can_refactor, refactor_code = parse_refactor_code(content)
                    if flag_can_refactor:
                        for e in all_me_code:
                            # print(">>>>e: ",e)
                            for node in ast.walk(ast.parse(e)):
                                if isinstance(node, ast.For):
                                    # print(">>>>node: ", ast.unparse(node))
                                    if ast.unparse(bool_node) ==ast.unparse(node) and ast.unparse(bool_node)!=e:
                                    # if refactor_code in e and refactor_code!=e:
                                    #     print(">>> come here")
                                        break
                            else:
                                continue
                            break
                        else:
                            all_me_code.append(ast.unparse(bool_node))
                            # continue
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


def get_response_directly_refactor_from_def_stmt_abstract_obj(user_instr, examples, samples, sys_msg="You are a helpful assistant."):
    reponse_list = []
    method_code_list = []
    one_other = []

    for me_code, old_code,object_var, *other, _,response in samples:
            content = response["choices"][0]["message"]["content"]
            ass_flag,ass_stmt=parse_for_code(content)
            # if "for plugin_func in plugin_store.values()" in me_code:
            #     print("come here: ",content)
            #     print("code: ",me_code)
            #

            if not ass_flag:
                continue

            if ass_stmt in me_code:
                continue
            last_line = code_extract_for_determine_has_add_func.get_last_line(me_code)
            object_var, fun_name = code_extract_for_determine_has_add_func.extract_function_object(last_line, 'add')
            # print("object_var: ",object_var)
            # if "for plugin_func in plugin_store.values()" not in me_code:
            #     # print("come here: ")
            #     continue

            if not object_var:
                continue

            abstract_me_code=util_rewrite.replace(object_var,"zj",me_code)
            # if "for plugin_func in plugin_store.values()" not in abstract_me_code:
            #     continue
    #         abstract_me_code='''for line in f:
    # if line.startswith('include '):
    #     for include in line.split()[1:]:
    #         zj.add(include)
    #         '''
            real_instruction = user_instr.replace("{{code}}", abstract_me_code)

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
                # return
                # flag_can_refactor, refactor_code = parse_refactor_code(content)
                # if flag_can_refactor:
                reponse_list.append([abstract_me_code,me_code, old_code, ass_flag, ass_stmt, *other])
                reponse_list[-1].extend([[msg, num_tokes], response])
            # else:
                #     continue

            except:
                traceback.print_exc()
                reponse_list.append([abstract_me_code,me_code, old_code,ass_flag,ass_stmt, *other])
                reponse_list[-1].extend([[msg, num_tokes], traceback.format_exc()])
        # break
    # '''

    return reponse_list

def get_response_directly_refactor_from_def_stmt_abstract_obj_filter_for_from_code(user_instr, examples, samples, sys_msg="You are a helpful assistant."):
    reponse_list = []
    method_code_list = []
    one_other = []
    # reponse_list.append([me_code, old_code, flag_use, object_var, ass_flag, ass_stmt, *other, new_code, method_code])
    # reponse_list.append([abstract_me_code, me_code, old_code, ass_flag, ass_stmt, flag_use, object_var, *other])
    # reponse_list.append([me_code, old_code, flag_use, object_var, ass_flag, ass_stmt, *other, new_code, method_code])
    # reponse_list.append(
    #     [info[0], old_code, *info[1:], *other, new_code, method_code])
    # return ast.unparse(bool_node), ass_stmt, object_var, flag_use, last_line

    for me_code, old_code, ass_stmt,object_var,flag_use,  last_line,  *other in samples:
            if "for u in urls_result:" not in me_code:#for (peer_id, mode) in zip(self.ordered_peer_ids, self.modes): for u in urls_result: for item in account_dumps:
                continue
            # print("response: ", response)

            # content = response["choices"][0]["message"]["content"]
            # ass_flag,ass_stmt=parse_for_code(content)
            # if "for im in goldChunkAry:" not in me_code:#for v in self.complete[u]: "psutil.process_iter(attrs=['name'])" "not_seen2d.add((hsize, wsize))"
            #
            #     continue
            # print("come here: ", content)
            # print("code: ", me_code,ass_flag,ass_stmt)
            #

            # if not ass_flag:
            #     continue

            if ass_stmt in me_code:
                continue
            # last_line = code_extract_for_determine_has_add_func.get_last_line(me_code)
            # object_var, fun_name = code_extract_for_determine_has_add_func.extract_function_object(last_line, 'add')
            # # print("object_var: ",object_var)
            # if "for plugin_func in plugin_store.values()" not in me_code:
            #     # print("come here: ")
            #     continue

            if not object_var:
                continue

            abstract_me_code=util_rewrite.replace(object_var,"zj",me_code)
            # if "for plugin_func in plugin_store.values()" not in abstract_me_code:
            #     continue
    #         abstract_me_code='''for line in f:
    # if line.startswith('include '):
    #     for include in line.split()[1:]:
    #         zj.add(include)
    #         '''
            real_instruction = user_instr.replace("{{code}}", abstract_me_code)

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
                # return
                # flag_can_refactor, refactor_code = parse_refactor_code(content)
                # if flag_can_refactor:
                reponse_list.append([abstract_me_code,me_code, old_code, ass_stmt,flag_use, object_var, *other])
                reponse_list[-1].extend([[msg, num_tokes], response])
            # else:
                #     continue

            except:
                traceback.print_exc()
                reponse_list.append([abstract_me_code,me_code, old_code,ass_stmt,flag_use, object_var, *other])
                reponse_list[-1].extend([[msg, num_tokes], traceback.format_exc()])
            # break
    # '''

    return reponse_list

def get_response_directly_refactor_from_def_stmt_abstract_obj_filter_for(user_instr, examples, samples, sys_msg="You are a helpful assistant."):
    reponse_list = []
    method_code_list = []
    one_other = []
    # reponse_list.append([me_code, old_code, flag_use, object_var, ass_flag, ass_stmt, *other, new_code, method_code])
    # reponse_list.append([abstract_me_code, me_code, old_code, ass_flag, ass_stmt, flag_use, object_var, *other])
    # reponse_list.append([me_code, old_code, flag_use, object_var, ass_flag, ass_stmt, *other, new_code, method_code])

    for me_code, old_code, flag_use, object_var, ass_flag, ass_stmt, *other, _,response in samples:
            # if "for item in account_dumps:" not in me_code:
            #     continue
            # print("response: ", response)

            # content = response["choices"][0]["message"]["content"]
            # ass_flag,ass_stmt=parse_for_code(content)
            if "for im in goldChunkAry:" not in me_code:#for v in self.complete[u]: "psutil.process_iter(attrs=['name'])" "not_seen2d.add((hsize, wsize))"

                continue
            # print("come here: ", content)
            # print("code: ", me_code,ass_flag,ass_stmt)
            #

            if not ass_flag:
                continue

            if ass_stmt in me_code:
                continue
            # last_line = code_extract_for_determine_has_add_func.get_last_line(me_code)
            # object_var, fun_name = code_extract_for_determine_has_add_func.extract_function_object(last_line, 'add')
            # # print("object_var: ",object_var)
            # if "for plugin_func in plugin_store.values()" not in me_code:
            #     # print("come here: ")
            #     continue

            if not object_var:
                continue

            abstract_me_code=util_rewrite.replace(object_var,"zj",me_code)
            # if "for plugin_func in plugin_store.values()" not in abstract_me_code:
            #     continue
    #         abstract_me_code='''for line in f:
    # if line.startswith('include '):
    #     for include in line.split()[1:]:
    #         zj.add(include)
    #         '''
            real_instruction = user_instr.replace("{{code}}", abstract_me_code)

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
                # return
                # flag_can_refactor, refactor_code = parse_refactor_code(content)
                # if flag_can_refactor:
                reponse_list.append([abstract_me_code,me_code, old_code, ass_flag, ass_stmt,flag_use, object_var, *other])
                reponse_list[-1].extend([[msg, num_tokes], response])
            # else:
                #     continue

            except:
                traceback.print_exc()
                reponse_list.append([abstract_me_code,me_code, old_code,ass_flag,ass_stmt,flag_use, object_var, *other])
                reponse_list[-1].extend([[msg, num_tokes], traceback.format_exc()])
            # break
    # '''

    return reponse_list

def get_response_directly_refactor_from_def_stmt(user_instr, examples, samples, sys_msg="You are a helpful assistant."):
    reponse_list = []
    method_code_list = []
    one_other = []

    for me_code, old_code, *other, _,response in samples:
            content = response["choices"][0]["message"]["content"]
            ass_flag,ass_stmt=parse_for_code(content)

            if not ass_flag:
                continue

            if ass_stmt in me_code:
                continue

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
                flag_can_refactor, refactor_code = parse_refactor_code(content)
                if flag_can_refactor:
                    reponse_list.append([me_code, old_code, ass_flag, ass_stmt, *other])
                    reponse_list[-1].extend([[msg, num_tokes], response])
                else:
                    continue

            except:
                traceback.print_exc()
                reponse_list.append([me_code, old_code,ass_flag,ass_stmt, *other])
                reponse_list[-1].extend([[msg, num_tokes], traceback.format_exc()])
        # break
    # '''

    return reponse_list

def parse_for_code(content):
    # print("content: ",content)
    content_list = content.split("Information:")
    flag=1 if "Yes" in content_list[0] else 0
    return flag,content_list[1].strip() if len(content_list)>1 else None
def get_response_find_def_stmt_improve(samples):
    reponse_list = []
    method_code_list = []
    one_other = []
    for ind_sampl, sample_method in enumerate(samples):
        for code in sample_method:
            *other, old_list, new_tree, \
            old_code, new_code, method_code = code
            method_code_list.append([*other, old_list, new_tree, old_code, new_code, method_code])
            break
        # break
    for *other, old_list, new_tree, old_code, new_code, method_code in method_code_list:
        # if "do_setup$1697" not in other:
        #     continue
        # print(other[2:])
        # if "for c in datasets[d]:" not in method_code:#for element in difference: attention_mask.append([int(input_idfor txi in tx['inputs']: for include in line.split()[1:]:" "not_seen2d.add((hsize, wsize))"
        #     continue
        method_code=ast.unparse(ast.parse(method_code))
        tree=ast.parse(method_code)
        # if "data_shifted.append(data[(column - row & 3) * 4 + row])" not in method_code:#"y.append(_triangular_inv(x[i]))" _all_input_text.append(i_text) addresses.append({'doctype':a.append(getattr(self, i)) area.append(m_id.eq(i).sum().item()) addresses.append({'doctype':psutil.process_iter(attrs=['name'])#"for item in account_dumps:" "wires_in_net.add(wire['name'])" "for interaction in interactions:" "for (_name, email) in settings.ADMINS" "for syn in synsets:"
        #     continue
        tmp_list = chat_gpt_ast_util.get_for_2(tree)
        # print("tmp_list: ", len(tmp_list))
        new_bool_node_list=[]
        correspond_var_dict=dict()
        # print("method_code:\n",method_code)
        for bool_node in tmp_list:
            code = ast.unparse(bool_node)
            if "for u in urls_result:" not in code:
                continue

            # if "for (iid, extra) in enumerate(extra_data):" not in code:#for day_bucket in day_buckets:
            #     continue
            # if "result[size_key] = {}" not in code:
            #     continue
            # if "for attribute_key in QINGCLOUD_SIZES[zone][size_key]:" not in code:
            #     continue
            last_line = chat_gpt_ast_util.get_last_line(code)
            is_function_call = chat_gpt_ast_util.is_function_call_2(last_line)

            if is_function_call:

                object_var, fun_name = chat_gpt_ast_util.extract_function_object(last_line, 'add')
                # object_var = chat_gpt_ast_util.extract_subscript_value(last_line)
                if not object_var:
                    continue
                # print("last_line: ",last_line)
                def get_info(tree,bool_node,object_var):
                    parent_node = chat_gpt_ast_util.find_parent_node(bool_node, tree)
                    while parent_node and parent_node != tree:
                        previous_code = ast.unparse(parent_node)
                        ass_stmt = object_var + " = set()" if object_var + " = set()" in previous_code and object_var + " = set()" not in ast.unparse(bool_node) else None
                        ass_flag = 1 if ass_stmt else 0
                        if ass_flag:
                            line_numbers = chat_gpt_ast_util.get_line_number(previous_code, ass_stmt)

                            flag_use = chat_gpt_ast_util.check_object_usage(previous_code, line_numbers[0] + 1,
                                                                            bool_node.lineno-parent_node.lineno, object_var)
                            # print("previous_code ",object_var,parent_node.end_lineno,line_numbers,line_numbers[0] + 1,bool_node.lineno,parent_node.lineno,bool_node.lineno-parent_node.lineno, previous_code)
                            # print("ast.unparse(bool_node): ",ast.unparse(bool_node))
                            # print("ass_stmt ",flag_use, ass_stmt)
                            return ast.unparse(bool_node),ass_stmt,object_var, flag_use,last_line
                            # new_bool_node_list.append([bool_node, last_line, object_var])
                            # break
                        if isinstance(parent_node, (ast.For, ast.While)):
                            return None
                        parent_node = chat_gpt_ast_util.find_parent_node(parent_node, tree)

                print(">>>>>>>bool_node: ", ast.unparse(bool_node))
                print(">>>>>>>object_var: ",object_var)
                info=get_info(tree,bool_node,object_var)
                print(">>>>>>>info: ",info)
                if info:
                    new_bool_node_list.append(info)
                    reponse_list.append(
                        [info[0], old_code, *info[1:], *other, new_code, method_code])

    return reponse_list
def get_response_find_def_stmt_filter(user_instr, examples, samples, sys_msg="You are a helpful assistant."):
    reponse_list = []
    method_code_list = []
    one_other = []
    for ind_sampl, sample_method in enumerate(samples):
        for code in sample_method:
            *other, old_list, new_tree, \
            old_code, new_code, method_code = code
            method_code_list.append([*other, old_list, new_tree, old_code, new_code, method_code])
            break
        # break
    for *other, old_list, new_tree, old_code, new_code, method_code in method_code_list:
        # if "do_setup$1697" not in other:
        #     continue
        # print(other[2:])
        # if "for txi in tx['inputs']:" not in method_code:#for include in line.split()[1:]:" "not_seen2d.add((hsize, wsize))"
        #     continue
        method_code=ast.unparse(ast.parse(method_code))
        tree=ast.parse(method_code)
        if "psutil.process_iter(attrs=['name'])" not in method_code:#"for item in account_dumps:" "wires_in_net.add(wire['name'])" "for interaction in interactions:" "for (_name, email) in settings.ADMINS" "for syn in synsets:"
            continue
        tmp_list = chat_gpt_ast_util.get_for_2(tree)
        print("tmp_list: ", len(tmp_list))
        new_bool_node_list=[]
        correspond_var_dict=dict()
        for bool_node in tmp_list:
            code = ast.unparse(bool_node)
            last_line = chat_gpt_ast_util.get_last_line(code)
            is_function_call = chat_gpt_ast_util.is_function_call_2(last_line)
            if is_function_call:
                object_var, fun_name = code_extract_for_determine_has_add_func.extract_function_object(last_line, 'add')
                if object_var:
                    new_bool_node_list.append([bool_node,last_line,object_var])
                    correspond_var_dict[bool_node]=object_var
        print("len of new_new_bool_node_list: ",len(new_bool_node_list))
        # for e,w,s in new_bool_node_list:
        #     print("code: ",ast.unparse(e),w,s)
        new_new_bool_node_list=[]
        for bool_node,last_line,object_var in new_bool_node_list:
            for other_bool_node,other_last_line,other_object_var in new_bool_node_list:
                if other_bool_node == bool_node:
                    continue
                parent_node = chat_gpt_ast_util.find_parent_node(bool_node, tree)
                while parent_node and parent_node != tree:
                        # print("parent node: ",ast.unparse(parent_node),ast.unparse(other_bool_node))
                        if ast.unparse(parent_node) == ast.unparse(other_bool_node) and object_var==other_object_var:
                            break
                        parent_node = chat_gpt_ast_util.find_parent_node(parent_node, tree)

                else:
                        continue
                break
            else:
                new_new_bool_node_list.append((bool_node,last_line,object_var))
        print("len of new_new_bool_node_list: ",len(new_new_bool_node_list))
        for e,w,s in new_new_bool_node_list:
            print("code: ",ast.unparse(e),w)
        # return

        for bool_node,last_line,object_var in new_new_bool_node_list:
            previous_code=code_extract_for_determine_has_add_func.extract_code_before_line_number(method_code,bool_node.end_lineno)

            me_code = ast.unparse(bool_node)
            real_instruction = user_instr.replace("{{code}}",previous_code)
            real_instruction = real_instruction.replace("{{given_node}}", last_line)
            real_instruction = real_instruction.replace("{{var}}", object_var)

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
                content = response["choices"][0]["message"]["content"]
                ass_flag, ass_stmt = parse_for_code(content)
                # print("previous_code: ",previous_code)
                # print("ass_stmt: ",ass_stmt)
                line_numbers=chat_gpt_ast_util.get_line_number(previous_code, ass_stmt)
                print("ass_stmt: ",line_numbers,object_var,bool_node.lineno,ass_stmt,previous_code,content)

                flag_use=chat_gpt_ast_util.check_object_usage(previous_code,line_numbers[0]+1,bool_node.lineno,object_var)
                print("flag_use: ",flag_use)
                # return
                flag_can_refactor, refactor_code = parse_refactor_code(content)
                # if flag_can_refactor:
                #     for e in all_me_code:
                #         # print(">>>>e: ",e)
                #         for node in ast.walk(ast.parse(e)):
                #             if isinstance(node, ast.For):
                #                 # print(">>>>node: ", ast.unparse(node))
                #                 if ast.unparse(bool_node) == ast.unparse(node) and ast.unparse(bool_node) != e:
                #                     # if refactor_code in e and refactor_code!=e:
                #                     #     print(">>> come here")
                #                     break
                #         else:
                #             continue
                #         break
                #     else:
                #         all_me_code.append(ast.unparse(bool_node))
                        # continue
                reponse_list.append([me_code, old_code,flag_use,object_var,ass_flag, ass_stmt, *other, new_code, method_code])
                reponse_list[-1].extend([[msg, num_tokes], response])
                # return
            except:
                traceback.print_exc()
                reponse_list.append([me_code, old_code,flag_use,object_var,ass_flag, ass_stmt, *other, new_code, method_code])
                reponse_list[-1].extend([[msg, num_tokes], traceback.format_exc()])
        # break
    # '''

    return reponse_list

def get_response_find_def_stmt(user_instr, examples, samples, sys_msg="You are a helpful assistant."):
    reponse_list = []
    method_code_list = []
    one_other = []
    for ind_sampl, sample_method in enumerate(samples):
        for code in sample_method:
            *other, old_list, new_tree, \
            old_code, new_code, method_code = code
            method_code_list.append([*other, old_list, new_tree, old_code, new_code, method_code])
            break
        # break
    for *other, old_list, new_tree, old_code, new_code, method_code in method_code_list:
        # if "do_setup$1697" not in other:
        #     continue
        # print(other[2:])
        # if "for include in line.split()[1:]:" not in method_code:
        #     continue
        method_code=ast.unparse(ast.parse(method_code))
        tmp_list = code_extract_for.get_for_2(method_code)
        all_me_code = []
        print("tmp_list: ", len(tmp_list))
        for bool_node in tmp_list:

            previous_code=code_extract_for_determine_has_add_func.extract_code_before_line_number(method_code,bool_node.end_lineno)
            code=ast.unparse(bool_node)
            # if "urls.add(u)" in code and "data.append(d)" not in code:
            #     print("come here: ")
            # if "urls.add(u)" not in code or "data.append(d)" in code:
            #     continue
            last_line = code_extract_for_determine_has_add_func.get_last_line(code)
            is_function_call=code_extract_for_determine_has_add_func.is_function_call(last_line)
            if is_function_call:
                object_var, fun_name=code_extract_for_determine_has_add_func.extract_function_object(code, 'add')
                if not object_var:
                    continue
            else:
                continue
            me_code = ast.unparse(bool_node)
            real_instruction = user_instr.replace("{{code}}",previous_code)
            real_instruction = real_instruction.replace("{{given_node}}", last_line)
            real_instruction = real_instruction.replace("{{var}}", object_var)

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
                content = response["choices"][0]["message"]["content"]
                flag_can_refactor, refactor_code = parse_refactor_code(content)
                # if flag_can_refactor:
                #     for e in all_me_code:
                #         # print(">>>>e: ",e)
                #         for node in ast.walk(ast.parse(e)):
                #             if isinstance(node, ast.For):
                #                 # print(">>>>node: ", ast.unparse(node))
                #                 if ast.unparse(bool_node) == ast.unparse(node) and ast.unparse(bool_node) != e:
                #                     # if refactor_code in e and refactor_code!=e:
                #                     #     print(">>> come here")
                #                     break
                #         else:
                #             continue
                #         break
                #     else:
                #         all_me_code.append(ast.unparse(bool_node))
                        # continue
                print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
                reponse_list.append([me_code, old_code,object_var, *other, new_code, method_code])
                reponse_list[-1].extend([[msg, num_tokes], response])
                # return
            except:
                traceback.print_exc()
                reponse_list.append([me_code, old_code,object_var, *other, new_code, method_code])
                reponse_list[-1].extend([[msg, num_tokes], traceback.format_exc()])
        # break
    # '''

    return reponse_list
def get_response_find_def_stmt_add_info(user_instr, examples, samples, sys_msg="You are a helpful assistant."):
    reponse_list = []
    method_code_list = []
    one_other = []
    for ind_sampl, sample_method in enumerate(samples):
        for code in sample_method:
            *other, old_list, new_tree, \
            old_code, new_code, method_code = code
            method_code_list.append([*other, old_list, new_tree, old_code, new_code, method_code])
            break
        # break
    for *other, old_list, new_tree, old_code, new_code, method_code in method_code_list:
        # if "do_setup$1697" not in other:
        #     continue
        # print(other[2:])
        # if "for include in line.split()[1:]:" not in method_code:
        #     continue
        method_code=ast.unparse(ast.parse(method_code))
        tmp_list = code_extract_for.get_for_2(method_code)
        all_me_code = []
        print("tmp_list: ", len(tmp_list))
        for bool_node in tmp_list:
            previous_code=code_extract_for_determine_has_add_func.extract_code_before_line_number(method_code,bool_node.end_lineno)
            code=ast.unparse(bool_node)
            last_line = code_extract_for_determine_has_add_func.get_last_line(code)
            is_function_call=code_extract_for_determine_has_add_func.is_function_call(last_line)
            if is_function_call:
                object_var, fun_name=code_extract_for_determine_has_add_func.extract_function_object(code, 'add')
                if not object_var:
                    continue
            else:
                continue
            me_code = ast.unparse(bool_node)
            real_instruction = user_instr.replace("{{code}}",previous_code)
            real_instruction = real_instruction.replace("{{given_node}}", last_line)
            real_instruction = real_instruction.replace("{{var}}", object_var)

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
                content = response["choices"][0]["message"]["content"]
                flag_can_refactor, refactor_code = parse_refactor_code(content)
                if flag_can_refactor:
                    for e in all_me_code:
                        # print(">>>>e: ",e)
                        for node in ast.walk(ast.parse(e)):
                            if isinstance(node, ast.For):
                                # print(">>>>node: ", ast.unparse(node))
                                if ast.unparse(bool_node) == ast.unparse(node) and ast.unparse(bool_node) != e:
                                    # if refactor_code in e and refactor_code!=e:
                                    #     print(">>> come here")
                                    break
                        else:
                            continue
                        break
                    else:
                        all_me_code.append(ast.unparse(bool_node))
                        # continue
                        print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
                        reponse_list.append([me_code, old_code,object_var, *other, new_code, method_code])
                        reponse_list[-1].extend([[msg, num_tokes], response])

            except:
                traceback.print_exc()
                reponse_list.append([me_code, old_code, object_var,*other, new_code, method_code])
                reponse_list[-1].extend([[msg, num_tokes], traceback.format_exc()])
        # break
    # '''

    return reponse_list
def get_acc_5(samples,new_python_code_list,refactor_code_list=None,whether_emptyset_list=None):
    offset=0#-2
    reponse_list=[]
    ground_truth_list=[]
    for ind_sampl, sample_method in enumerate(samples):
        for code in sample_method:
            repo_name, old_path, file_html, class_name,me_name, old_list, new_tree,\
                old_code,new_code, method_code=code


            # break
            old_for_code=ast.unparse(old_list[0])
            *other, old_list, new_tree, \
            old_code, new_code, method_code = code
            print("old_for_code: ",old_for_code)
            ele = [repo_name, old_path, file_html, class_name, me_name, ast.unparse(ast.parse(method_code)),ast.unparse(ast.parse(old_for_code)), ast.unparse(ast.parse(new_code))]
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
    format_new_python_list=[]
    for i, s in enumerate(new_python_code_list[0]):
        print("i,sample: ", i, s)

    for ind, sample in enumerate(new_python_code_list):
        # print("sample: ",sample)
        # e = [repo_name, old_path, file_html, class_name, me_name, method_code, me_code,
        #      ast.unparse(ast.parse(refactor_code)), ass_stmt, content]

        # break
        # e = [repo_name, old_path, file_html, class_name, me_name, method_code, me_code,
        #      ast.unparse(ast.parse(refactor_code)), ass_stmt, content]

        repo_name, old_path, file_html, class_name, me_name, method_code,me_code,refactor_code,*other=sample
        # me_code,old_code,repo_name, old_path, file_html, class_name,me_name,new_code,method_code,_,response=sample
        # print(">>>>me_code: ",me_code,response )
        # try:
        #     response= sample[-1]
        #     content = response["choices"][0]["message"]["content"]
        # except:
        #     continue
        # reponse_list.append([me_code, old_code, *other, new_code, method_code])
        # reponse_list[-1].extend([[msg, num_tokes], response])

        # flag_can_refactor, refactor_code=parse_refactor_code(content)
        # if not flag_can_refactor:
        #     continue


        # print(">>>>>>refactor_code: ", refactor_code)

        e=[repo_name, old_path, file_html, class_name,me_name,method_code,me_code,refactor_code]
        # print("predict ele: ", e)
        format_new_python_list.append(e)

        # predict_res.append(e)
        ground_pre_list=[e[offset:-1] for e in ground_copy_truth_list]
        if e in ground_copy_truth_list:
                index = ground_copy_truth_list.index(e)
                now_list.append(index)
                # e[-1]=old_refactor_code
                # e.extend([element_str, slice_str])
                e.append(ground_copy_truth_list[index][-1])
                e.append(1)
                ground_copy_truth_list.pop(index)
                acc+=1
                pre+=1

        elif e[:-1] in ground_pre_list:
            # print(">>>>>>>>old code:",e[-2],content)
            # e[-1] = old_refactor_code
            index=ground_pre_list.index(e[:-1])
            now_list.append(index)
            # e.extend([element_str, slice_str])
            e.append(ground_copy_truth_list[index][-1])
            print(">>>>>>>>refactor error!",ground_copy_truth_list[index][-1])

            e.append(0)
            ground_copy_truth_list.pop(index)
        else:
            # continue
            # e[-1] = old_refactor_code
            # e.extend([element_str, slice_str])
            e.append("Cannot refactor")
            e.append(-1)
            acc += 1
        predict_res.append(e + other)

    predict_res.append(["NOFOUND"])

    for ind,e in enumerate(ground_copy_truth_list):
            predict_res.append(e+[0])
    print("acc: ",acc,len(predict_res),acc/len(ground_truth_list))
    print("precision: ",pre,len(predict_res),pre/len(ground_truth_list))

    return predict_res,ground_truth_list,format_new_python_list

def get_acc_4(samples,new_python_code_list,refactor_code_list=None,whether_emptyset_list=None):
    offset=0#-2
    reponse_list=[]
    ground_truth_list=[]
    for ind_sampl, sample_method in enumerate(samples):
        for code in sample_method:
            repo_name, old_path, file_html, class_name,me_name, old_list, new_tree,\
                old_code,new_code, method_code=code
            # break
            old_for_code=ast.unparse(old_list[0])
            *other, old_list, new_tree, \
            old_code, new_code, method_code = code
            ele = [repo_name, old_path, file_html, class_name, me_name, method_code,old_for_code, new_code]
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
    format_new_python_list=[]
    for i, s in enumerate(new_python_code_list[0]):
        print("i,sample: ", i, s)

    for ind, sample in enumerate(new_python_code_list):
        # print("sample: ",sample)

        # break
        me_code,old_code,repo_name, old_path, file_html, class_name,me_name,new_code,method_code,_,response=sample
        print(">>>>me_code: ",me_code,response )
        try:
            response= sample[-1]
            content = response["choices"][0]["message"]["content"]
        except:
            continue
        # reponse_list.append([me_code, old_code, *other, new_code, method_code])
        # reponse_list[-1].extend([[msg, num_tokes], response])

        flag_can_refactor, refactor_code=parse_refactor_code(content)
        # if not flag_can_refactor:
        #     continue


        print(">>>>>>refactor_code: ", refactor_code)

        e=[repo_name, old_path, file_html, class_name,me_name,method_code,me_code,refactor_code]
        # print("predict ele: ", e)
        format_new_python_list.append(e)

        # predict_res.append(e)
        ground_pre_list=[e[offset:-1] for e in ground_copy_truth_list]
        if e in ground_copy_truth_list:
                index = ground_copy_truth_list.index(e)
                now_list.append(index)
                # e[-1]=old_refactor_code
                # e.extend([element_str, slice_str])
                e.append(ground_copy_truth_list[index][-1])
                e.append(1)
                ground_copy_truth_list.pop(index)
                acc+=1
                pre+=1

        elif e[:-1] in ground_pre_list:
            print(">>>>>>>>old code:",e[-2],content)
            # e[-1] = old_refactor_code
            index=ground_pre_list.index(e[:-1])
            now_list.append(index)
            # e.extend([element_str, slice_str])
            e.append(ground_copy_truth_list[index][-1])
            print(">>>>>>>>refactor error!",ground_copy_truth_list[index][-1])

            e.append(0)
            ground_copy_truth_list.pop(index)
        else:
            # continue
            # e[-1] = old_refactor_code
            # e.extend([element_str, slice_str])
            e.append("Cannot refactor")
            e.append(-1)
            acc += 1
        predict_res.append(e + other)

    predict_res.append(["NOFOUND"])

    for ind,e in enumerate(ground_copy_truth_list):
            predict_res.append(e+[0])
    print("acc: ",acc,len(predict_res),acc/len(ground_truth_list))
    print("precision: ",pre,len(predict_res),pre/len(ground_truth_list))

    return predict_res,ground_truth_list,format_new_python_list