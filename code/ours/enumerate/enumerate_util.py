import ast,os,sys
import copy
import traceback

import util_rewrite

code_dir = "/".join(os.path.abspath(__file__).split("/")[:-2]) + "/"
print("code path: ",code_dir)
sys.path.append(code_dir)
import chatgpt_util,random
import openai, tiktoken,ast,util,chat_gpt_ast_util
# import code_extract_for,code_extract_for_determine_has_add_func


def get_response_directly_refactor_with_specify_stmt_sample_method(user_instr, examples, samples,
                                                     sys_msg="You are a helpful assistant."):
    count=0
    reponse_list = []
    method_code_list = []
    one_other = []
    for ind_sampl, sample_method in enumerate(samples):
        method_code_list.append(sample_method)

    for *other, method_code in method_code_list:
        # if "do_setup$1697" not in other:
        #     continue
        # print(other[2:])

        method_code=ast.unparse(ast.parse(method_code))
        tree=ast.parse(method_code)
        # if "data_shifted.append(data[(column - row & 3) * 4 + row])" not in method_code:#"y.append(_triangular_inv(x[i]))" _all_input_text.append(i_text) addresses.append({'doctype':a.append(getattr(self, i)) area.append(m_id.eq(i).sum().item()) addresses.append({'doctype':psutil.process_iter(attrs=['name'])#"for item in account_dumps:" "wires_in_net.add(wire['name'])" "for interaction in interactions:" "for (_name, email) in settings.ADMINS" "for syn in synsets:"
        #     continue
        all_nodes = chat_gpt_ast_util.get_for_2(tree)
        for node in all_nodes:
            flag_enumerate=chat_gpt_ast_util.is_enumerate_for(node)
            if flag_enumerate:
                continue
            print("code:\n",ast.unparse(node))
            # stmt = chat_gpt_ast_util.extract_function_call_stmt_from_tree(tree, node)
            # if isinstance(stmt,ast.With):
            #     continue
            # body = chat_gpt_ast_util.find_parent_node(stmt, tree)
            # print("body: ",body,body.body)
            # body_code=chat_gpt_ast_util.extract_code_from_line(ast.unparse(body), 2)
            # body_code=body.body
            # open_code=chat_gpt_ast_util.extract_code_from_line(ast.unparse(ast.parse(body))[1:], node.lineno-body.body[0].lineno+1)
            #
            real_instruction = user_instr.replace("{{code}}",ast.unparse(node))
            count+=1
            '''
            print(">>>>>>>>>>real_instruction: ", real_instruction)

            msg = chatgpt_util.format_message_2(real_instruction, examples=examples, sys_msg=sys_msg)
            # print(">>>>>>>>>>each msg: ", msg)
            # num_tokes = chatgpt_util.num_tokens_from_messages(msg)
            # print("len of msg: ",chatgpt_util.num_tokens_from_messages(msg))
            # if chatgpt_util.num_tokens_from_messages(msg)>=chatgpt_util.MAX_TOKENS:
            #     response
            # if 1:
            try:
                response = chatgpt_util.chatGPT_result(msg)
                print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
                content = response["choices"][0]["message"]["content"]
                reponse_list.append(
                    [])
                reponse_list[-1].extend([[msg], response])
                # return
            except:
                traceback.print_exc()
                reponse_list.append([])
                reponse_list[-1].extend([[msg], traceback.format_exc()])
            '''
    print("count: ",count)
    return reponse_list


def get_response_directly_refactor_from_extract_module(user_instr, examples, samples,
                                                     sys_msg="You are a helpful assistant."):
    count=0
    reponse_list = []
    # method_code_list = []
    # one_other = []
    # for ind_sampl, sample_method in enumerate(samples):
    #     method_code_list.append(sample_method)

    for *other, for_code,for_node in samples:
        # # if "do_setup$1697" not in other:
        # #     continue
        # # print(other[2:])
        #
        # method_code=ast.unparse(ast.parse(method_code))
        # tree=ast.parse(method_code)
        # # if "data_shifted.append(data[(column - row & 3) * 4 + row])" not in method_code:#"y.append(_triangular_inv(x[i]))" _all_input_text.append(i_text) addresses.append({'doctype':a.append(getattr(self, i)) area.append(m_id.eq(i).sum().item()) addresses.append({'doctype':psutil.process_iter(attrs=['name'])#"for item in account_dumps:" "wires_in_net.add(wire['name'])" "for interaction in interactions:" "for (_name, email) in settings.ADMINS" "for syn in synsets:"
        # #     continue
        # all_nodes = chat_gpt_ast_util.get_for_2(tree)
        # for node in all_nodes:
        #     flag_enumerate=chat_gpt_ast_util.is_enumerate_for(node)
        #     if flag_enumerate:
        #         continue
        #     print("code:\n",ast.unparse(node))
        if 1:
            # stmt = chat_gpt_ast_util.extract_function_call_stmt_from_tree(tree, node)
            # if isinstance(stmt,ast.With):
            #     continue
            # body = chat_gpt_ast_util.find_parent_node(stmt, tree)
            # print("body: ",body,body.body)
            # body_code=chat_gpt_ast_util.extract_code_from_line(ast.unparse(body), 2)
            # body_code=body.body
            # open_code=chat_gpt_ast_util.extract_code_from_line(ast.unparse(ast.parse(body))[1:], node.lineno-body.body[0].lineno+1)
            #
            # print("for_code: ",for_code)
            real_instruction = user_instr.replace("{{code}}",for_code)
            count+=1
            # '''
            print(">>>>>>>>>>real_instruction: ", real_instruction)

            msg = chatgpt_util.format_message_2(real_instruction, examples=examples, sys_msg=sys_msg)
            # print(">>>>>>>>>>each msg: ", msg)
            # num_tokes = chatgpt_util.num_tokens_from_messages(msg)
            # print("len of msg: ",chatgpt_util.num_tokens_from_messages(msg))
            # if chatgpt_util.num_tokens_from_messages(msg)>=chatgpt_util.MAX_TOKENS:
            #     response
            # if 1:
            try:
                response = chatgpt_util.chatGPT_result(msg)
                print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
                content = response["choices"][0]["message"]["content"]
                reponse_list.append(
                    [*other,for_code])
                reponse_list[-1].extend([[msg], response])
                # return
            except:
                traceback.print_exc()
                reponse_list.append([*other,for_code])
                reponse_list[-1].extend([[msg], traceback.format_exc()])
            # break
            # '''
    print("count: ",count)
    return reponse_list

def parse_refactor_code(content):
    try:
        answer_list = content.split("Information:")
        content_list = content.split("\n")
        for content in content_list:
            if "Answer: No" in content:
                return 0, answer_list[-1].strip()
            else:
                return 1,  answer_list[-1].strip()
    except:
        traceback.print_exc()
        pass
    return 0, None
def get_response_directly_refactor_from_replace_abstract(user_instr, examples, samples,
                                                     sys_msg="You are a helpful assistant."):
    count=0
    reponse_list = []
    # method_code_list = []
    # one_other = []
    # for ind_sampl, sample_method in enumerate(samples):
    #     method_code_list.append(sample_method)
    # all_codes.append([*other, method_code, ast.unparse(node), node,
    #                   [["enumerate(" + ast.unparse(node.itr) + ")", ast.unparse(node.iter)],
    #                    [tar_new, ast.unparse(node.target)]], ast.unparse(abstract_for_code), abstract_for_code])

    for *other, ((_,enumer_obj),_),for_code,for_node in samples:
        # # if "do_setup$1697" not in other:
        # #     continue
        # # print(other[2:])
        #
        # method_code=ast.unparse(ast.parse(method_code))
        # tree=ast.parse(method_code)
        # # if "data_shifted.append(data[(column - row & 3) * 4 + row])" not in method_code:#"y.append(_triangular_inv(x[i]))" _all_input_text.append(i_text) addresses.append({'doctype':a.append(getattr(self, i)) area.append(m_id.eq(i).sum().item()) addresses.append({'doctype':psutil.process_iter(attrs=['name'])#"for item in account_dumps:" "wires_in_net.add(wire['name'])" "for interaction in interactions:" "for (_name, email) in settings.ADMINS" "for syn in synsets:"
        # #     continue
        # all_nodes = chat_gpt_ast_util.get_for_2(tree)
        # for node in all_nodes:
        #     flag_enumerate=chat_gpt_ast_util.is_enumerate_for(node)
        #     if flag_enumerate:
        #         continue
        #     print("code:\n",ast.unparse(node))
        if 1:
            # if "for i in arg[1:]:" not in for_code:#for project in projects_data: for i in range(len(x_1d)): for ksize in kernel_size: for n in arange(minN, maxN + 1): for (pathname, dirname, content, meta) in self.allfiles(): for record in [rec1, rec2]: for i in range(len(x)) for d in args:
            #     continue
            # stmt = chat_gpt_ast_util.extract_function_call_stmt_from_tree(tree, node)
            # if isinstance(stmt,ast.With):
            #     continue
            # body = chat_gpt_ast_util.find_parent_node(stmt, tree)
            # print("body: ",body,body.body)
            # body_code=chat_gpt_ast_util.extract_code_from_line(ast.unparse(body), 2)
            # body_code=body.body
            # open_code=chat_gpt_ast_util.extract_code_from_line(ast.unparse(ast.parse(body))[1:], node.lineno-body.body[0].lineno+1)
            #
            # print("for_code: ",for_code)
            # return
            # if "zip(names, init_params):" not in for_code:
            #     continue
            stmt=chat_gpt_ast_util.get_first_line(for_code)
            real_instruction = user_instr.replace("{{code}}",for_code)
            real_instruction = real_instruction.replace("{{stmt}}",enumer_obj)

            count+=1
            # '''
            print(">>>>>>>>>>real_instruction: ", real_instruction)

            msg = chatgpt_util.format_message_2(real_instruction, examples=examples, sys_msg=sys_msg)
            # print(">>>>>>>>>>each msg: ", msg)
            # num_tokes = chatgpt_util.num_tokens_from_messages(msg)
            # print("len of msg: ",chatgpt_util.num_tokens_from_messages(msg))
            # if chatgpt_util.num_tokens_from_messages(msg)>=chatgpt_util.MAX_TOKENS:
            #     response
            # if 1:
            try:
                response = chatgpt_util.chatGPT_result(msg)
                print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
                content = response["choices"][0]["message"]["content"]
                reponse_list.append(
                    [*other,((_,enumer_obj),_),for_code])
                reponse_list[-1].extend([[msg], response])
                # return
            except:
                traceback.print_exc()
                reponse_list.append([*other,((_,enumer_obj),_),for_code])
                reponse_list[-1].extend([[msg], traceback.format_exc()])
            # break
            # '''
    print("count: ",count)
    return reponse_list
def get_response_directly_refactor_from_extract_module_with_for_stmt(user_instr, examples, samples,
                                                     sys_msg="You are a helpful assistant."):
    count=0
    reponse_list = []
    # method_code_list = []
    # one_other = []
    # for ind_sampl, sample_method in enumerate(samples):
    #     method_code_list.append(sample_method)

    for *other, for_code,for_node in samples:
        # # if "do_setup$1697" not in other:
        # #     continue
        # # print(other[2:])
        #
        # method_code=ast.unparse(ast.parse(method_code))
        # tree=ast.parse(method_code)
        # # if "data_shifted.append(data[(column - row & 3) * 4 + row])" not in method_code:#"y.append(_triangular_inv(x[i]))" _all_input_text.append(i_text) addresses.append({'doctype':a.append(getattr(self, i)) area.append(m_id.eq(i).sum().item()) addresses.append({'doctype':psutil.process_iter(attrs=['name'])#"for item in account_dumps:" "wires_in_net.add(wire['name'])" "for interaction in interactions:" "for (_name, email) in settings.ADMINS" "for syn in synsets:"
        # #     continue
        # all_nodes = chat_gpt_ast_util.get_for_2(tree)
        # for node in all_nodes:
        #     flag_enumerate=chat_gpt_ast_util.is_enumerate_for(node)
        #     if flag_enumerate:
        #         continue
        #     print("code:\n",ast.unparse(node))
        if 1:
            if "for i in arg[1:]:" not in for_code:#for project in projects_data: for i in range(len(x_1d)): for ksize in kernel_size: for n in arange(minN, maxN + 1): for (pathname, dirname, content, meta) in self.allfiles(): for record in [rec1, rec2]: for i in range(len(x)) for d in args:
                continue
            # stmt = chat_gpt_ast_util.extract_function_call_stmt_from_tree(tree, node)
            # if isinstance(stmt,ast.With):
            #     continue
            # body = chat_gpt_ast_util.find_parent_node(stmt, tree)
            # print("body: ",body,body.body)
            # body_code=chat_gpt_ast_util.extract_code_from_line(ast.unparse(body), 2)
            # body_code=body.body
            # open_code=chat_gpt_ast_util.extract_code_from_line(ast.unparse(ast.parse(body))[1:], node.lineno-body.body[0].lineno+1)
            #
            # print("for_code: ",for_code)
            # return
            # if "zip(names, init_params):" not in for_code:
            #     continue
            stmt=chat_gpt_ast_util.get_first_line(for_code)
            real_instruction = user_instr.replace("{{code}}",for_code)
            real_instruction = real_instruction.replace("{{stmt}}",stmt)

            count+=1
            # '''
            print(">>>>>>>>>>real_instruction: ", real_instruction)

            msg = chatgpt_util.format_message_2(real_instruction, examples=examples, sys_msg=sys_msg)
            # print(">>>>>>>>>>each msg: ", msg)
            # num_tokes = chatgpt_util.num_tokens_from_messages(msg)
            # print("len of msg: ",chatgpt_util.num_tokens_from_messages(msg))
            # if chatgpt_util.num_tokens_from_messages(msg)>=chatgpt_util.MAX_TOKENS:
            #     response
            # if 1:
            try:
                response = chatgpt_util.chatGPT_result(msg)
                print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
                content = response["choices"][0]["message"]["content"]
                reponse_list.append(
                    [*other,for_code])
                reponse_list[-1].extend([[msg], response])
                # return
            except:
                traceback.print_exc()
                reponse_list.append([*other,for_code])
                reponse_list[-1].extend([[msg], traceback.format_exc()])
            # break
            # '''
    print("count: ",count)
    return reponse_list


def get_response_directly_refactor_from_extract_module_with_for_stmt_simplify(user_instr, examples, samples,
                                                     sys_msg="You are a helpful assistant."):
    count=0
    reponse_list = []
    # method_code_list = []
    # one_other = []
    # for ind_sampl, sample_method in enumerate(samples):
    #     method_code_list.append(sample_method)

    for *other, for_code,for_node in samples:
        # # if "do_setup$1697" not in other:
        # #     continue
        # # print(other[2:])
        #
        # method_code=ast.unparse(ast.parse(method_code))
        # tree=ast.parse(method_code)
        # # if "data_shifted.append(data[(column - row & 3) * 4 + row])" not in method_code:#"y.append(_triangular_inv(x[i]))" _all_input_text.append(i_text) addresses.append({'doctype':a.append(getattr(self, i)) area.append(m_id.eq(i).sum().item()) addresses.append({'doctype':psutil.process_iter(attrs=['name'])#"for item in account_dumps:" "wires_in_net.add(wire['name'])" "for interaction in interactions:" "for (_name, email) in settings.ADMINS" "for syn in synsets:"
        # #     continue
        # all_nodes = chat_gpt_ast_util.get_for_2(tree)
        # for node in all_nodes:
        #     flag_enumerate=chat_gpt_ast_util.is_enumerate_for(node)
        #     if flag_enumerate:
        #         continue
        #     print("code:\n",ast.unparse(node))
        if 1:
            if "for i in arg[1:]:" not in for_code:#for project in projects_data: for i in range(len(x_1d)): for ksize in kernel_size: for n in arange(minN, maxN + 1): for (pathname, dirname, content, meta) in self.allfiles(): for record in [rec1, rec2]: for i in range(len(x)) for d in args:
                continue
            # stmt = chat_gpt_ast_util.extract_function_call_stmt_from_tree(tree, node)
            # if isinstance(stmt,ast.With):
            #     continue
            # body = chat_gpt_ast_util.find_parent_node(stmt, tree)
            # print("body: ",body,body.body)
            # body_code=chat_gpt_ast_util.extract_code_from_line(ast.unparse(body), 2)
            # body_code=body.body
            # open_code=chat_gpt_ast_util.extract_code_from_line(ast.unparse(ast.parse(body))[1:], node.lineno-body.body[0].lineno+1)
            #
            # print("for_code: ",for_code)
            # return
            # if "zip(names, init_params):" not in for_code:
            #     continue
            stmt=chat_gpt_ast_util.get_first_line(for_code)
            real_instruction = user_instr.replace("{{code}}",for_code)
            real_instruction = real_instruction.replace("{{stmt}}",stmt)

            count+=1
            # '''
            print(">>>>>>>>>>real_instruction: ", real_instruction)

            msg = chatgpt_util.format_message_2(real_instruction, examples=examples, sys_msg=sys_msg)
            # print(">>>>>>>>>>each msg: ", msg)
            # num_tokes = chatgpt_util.num_tokens_from_messages(msg)
            # print("len of msg: ",chatgpt_util.num_tokens_from_messages(msg))
            # if chatgpt_util.num_tokens_from_messages(msg)>=chatgpt_util.MAX_TOKENS:
            #     response
            # if 1:
            try:
                response = chatgpt_util.chatGPT_result(msg)
                print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
                content = response["choices"][0]["message"]["content"]
                reponse_list.append(
                    [*other,for_code])
                reponse_list[-1].extend([[msg], response])
                # return
            except:
                traceback.print_exc()
                reponse_list.append([*other,for_code])
                reponse_list[-1].extend([[msg], traceback.format_exc()])
            # break
            # '''
    print("count: ",count)
    return reponse_list


def get_response_directly_refactor_from_extract_module_with_for_stmt_abstract(user_instr, examples, samples,
                                                     sys_msg="You are a helpful assistant."):
    count=0
    reponse_list = []
    # method_code_list = []
    # one_other = []
    # for ind_sampl, sample_method in enumerate(samples):
    #     method_code_list.append(sample_method)

    for *other, for_code,for_node in samples:
        # # if "do_setup$1697" not in other:
        # #     continue
        # # print(other[2:])
        #
        # method_code=ast.unparse(ast.parse(method_code))
        # tree=ast.parse(method_code)
        # # if "data_shifted.append(data[(column - row & 3) * 4 + row])" not in method_code:#"y.append(_triangular_inv(x[i]))" _all_input_text.append(i_text) addresses.append({'doctype':a.append(getattr(self, i)) area.append(m_id.eq(i).sum().item()) addresses.append({'doctype':psutil.process_iter(attrs=['name'])#"for item in account_dumps:" "wires_in_net.add(wire['name'])" "for interaction in interactions:" "for (_name, email) in settings.ADMINS" "for syn in synsets:"
        # #     continue
        # all_nodes = chat_gpt_ast_util.get_for_2(tree)
        # for node in all_nodes:
        #     flag_enumerate=chat_gpt_ast_util.is_enumerate_for(node)
        #     if flag_enumerate:
        #         continue
        #     print("code:\n",ast.unparse(node))
        if 1:
            # if "for i in arg[1:]:" not in for_code:#for project in projects_data: for i in range(len(x_1d)): for ksize in kernel_size: for n in arange(minN, maxN + 1): for (pathname, dirname, content, meta) in self.allfiles(): for record in [rec1, rec2]: for i in range(len(x)) for d in args:
            #     continue
            # stmt = chat_gpt_ast_util.extract_function_call_stmt_from_tree(tree, node)
            # if isinstance(stmt,ast.With):
            #     continue
            # body = chat_gpt_ast_util.find_parent_node(stmt, tree)
            # print("body: ",body,body.body)
            # body_code=chat_gpt_ast_util.extract_code_from_line(ast.unparse(body), 2)
            # body_code=body.body
            # open_code=chat_gpt_ast_util.extract_code_from_line(ast.unparse(ast.parse(body))[1:], node.lineno-body.body[0].lineno+1)
            #
            # print("for_code: ",for_code)
            # return
            # if "zip(names, init_params):" not in for_code:
            #     continue
            abstract_for_code =chat_gpt_ast_util.replace_for_iter(for_node, "zj_list")
            abstract_for_code = ast.unparse(abstract_for_code)
            stmt=chat_gpt_ast_util.get_first_line(abstract_for_code)
            # real_instruction = user_instr.replace("{{code}}",for_code)
            real_instruction = user_instr.replace("{{stmt}}",stmt)

            count+=1
            # '''
            print(">>>>>>>>>>real_instruction: ", real_instruction)

            msg = chatgpt_util.format_message_2(real_instruction, examples=examples, sys_msg=sys_msg)
            # print(">>>>>>>>>>each msg: ", msg)
            # num_tokes = chatgpt_util.num_tokens_from_messages(msg)
            # print("len of msg: ",chatgpt_util.num_tokens_from_messages(msg))
            # if chatgpt_util.num_tokens_from_messages(msg)>=chatgpt_util.MAX_TOKENS:
            #     response
            # if 1:
            try:
                response = chatgpt_util.chatGPT_result(msg)
                print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
                content = response["choices"][0]["message"]["content"]
                reponse_list.append(
                    [*other,abstract_for_code,["zj_list",ast.unparse(for_node.iter)],stmt,for_code])
                reponse_list[-1].extend([[msg], response])
                # return
            except:
                traceback.print_exc()
                reponse_list.append([*other,abstract_for_code,["zj_list",ast.unparse(for_node.iter)],stmt,for_code])
                reponse_list[-1].extend([[msg], traceback.format_exc()])
            # break
            # '''
    print("count: ",count)
    return reponse_list



def get_response_directly_refactor_from_extract_module_with_for_stmt_abstract_complete_code(user_instr, examples, samples,
                                                     sys_msg="You are a helpful assistant."):
    count=0
    reponse_list = []
    # method_code_list = []
    # one_other = []
    # for ind_sampl, sample_method in enumerate(samples):
    #     method_code_list.append(sample_method)

    for *other, for_code,for_node in samples:
        # # if "do_setup$1697" not in other:
        # #     continue
        # # print(other[2:])
        #
        # method_code=ast.unparse(ast.parse(method_code))
        # tree=ast.parse(method_code)
        # # if "data_shifted.append(data[(column - row & 3) * 4 + row])" not in method_code:#"y.append(_triangular_inv(x[i]))" _all_input_text.append(i_text) addresses.append({'doctype':a.append(getattr(self, i)) area.append(m_id.eq(i).sum().item()) addresses.append({'doctype':psutil.process_iter(attrs=['name'])#"for item in account_dumps:" "wires_in_net.add(wire['name'])" "for interaction in interactions:" "for (_name, email) in settings.ADMINS" "for syn in synsets:"
        # #     continue
        # all_nodes = chat_gpt_ast_util.get_for_2(tree)
        # for node in all_nodes:
        #     flag_enumerate=chat_gpt_ast_util.is_enumerate_for(node)
        #     if flag_enumerate:
        #         continue
        #     print("code:\n",ast.unparse(node))
        if 1:
            # if "for i in arg[1:]:" not in for_code:#for project in projects_data: for i in range(len(x_1d)): for ksize in kernel_size: for n in arange(minN, maxN + 1): for (pathname, dirname, content, meta) in self.allfiles(): for record in [rec1, rec2]: for i in range(len(x)) for d in args:
            #     continue
            # stmt = chat_gpt_ast_util.extract_function_call_stmt_from_tree(tree, node)
            # if isinstance(stmt,ast.With):
            #     continue
            # body = chat_gpt_ast_util.find_parent_node(stmt, tree)
            # print("body: ",body,body.body)
            # body_code=chat_gpt_ast_util.extract_code_from_line(ast.unparse(body), 2)
            # body_code=body.body
            # open_code=chat_gpt_ast_util.extract_code_from_line(ast.unparse(ast.parse(body))[1:], node.lineno-body.body[0].lineno+1)
            #
            # print("for_code: ",for_code)
            # return
            # if "zip(names, init_params):" not in for_code:
            #     continue
            abstract_for_code =chat_gpt_ast_util.replace_for_iter(for_node, "zj_list")
            abstract_for_code = ast.unparse(abstract_for_code)
            stmt=chat_gpt_ast_util.get_first_line(abstract_for_code)
            real_instruction = user_instr.replace("{{code}}",abstract_for_code)
            real_instruction = real_instruction.replace("{{stmt}}",stmt)

            count+=1
            # '''
            print(">>>>>>>>>>real_instruction: ", real_instruction)

            msg = chatgpt_util.format_message_2(real_instruction, examples=examples, sys_msg=sys_msg)
            # print(">>>>>>>>>>each msg: ", msg)
            # num_tokes = chatgpt_util.num_tokens_from_messages(msg)
            # print("len of msg: ",chatgpt_util.num_tokens_from_messages(msg))
            # if chatgpt_util.num_tokens_from_messages(msg)>=chatgpt_util.MAX_TOKENS:
            #     response
            # if 1:
            try:
                response = chatgpt_util.chatGPT_result(msg)
                print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
                content = response["choices"][0]["message"]["content"]
                reponse_list.append(
                    [*other,abstract_for_code,["zj_list",ast.unparse(for_node.iter)],stmt,for_code])
                reponse_list[-1].extend([[msg], response])
                # return
            except:
                traceback.print_exc()
                reponse_list.append([*other,abstract_for_code,["zj_list",ast.unparse(for_node.iter)],stmt,for_code])
                reponse_list[-1].extend([[msg], traceback.format_exc()])
            # break
            # '''
    print("count: ",count)
    return reponse_list