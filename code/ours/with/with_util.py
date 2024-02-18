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
def get_response_directly_refactor(user_instr, examples, samples,
                                                     sys_msg="You are a helpful assistant."):

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

        method_code=ast.unparse(ast.parse(method_code))
        tree=ast.parse(method_code)
        # if "data_shifted.append(data[(column - row & 3) * 4 + row])" not in method_code:#"y.append(_triangular_inv(x[i]))" _all_input_text.append(i_text) addresses.append({'doctype':a.append(getattr(self, i)) area.append(m_id.eq(i).sum().item()) addresses.append({'doctype':psutil.process_iter(attrs=['name'])#"for item in account_dumps:" "wires_in_net.add(wire['name'])" "for interaction in interactions:" "for (_name, email) in settings.ADMINS" "for syn in synsets:"
        #     continue
        all_nodes = chat_gpt_ast_util.extract_function_calls_from_tree(tree, "open")
        for node in all_nodes:
            stmt = chat_gpt_ast_util.extract_function_call_stmt_from_tree(tree, node)
            if isinstance(stmt,ast.With):
                continue
            body = chat_gpt_ast_util.find_parent_node(stmt, tree)
            # print("body: ",body,body.body)
            # body_code=chat_gpt_ast_util.extract_code_from_line(ast.unparse(body), 2)
            # body_code=body.body
            # open_code=chat_gpt_ast_util.extract_code_from_line(ast.unparse(ast.parse(body))[1:], node.lineno-body.body[0].lineno+1)
            #
            real_instruction = user_instr.replace("{{code}}",ast.unparse(body))
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


    return reponse_list


def get_response_directly_refactor_with_specify_stmt(user_instr, examples, samples,
                                                     sys_msg="You are a helpful assistant."):

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

        method_code=ast.unparse(ast.parse(method_code))
        tree=ast.parse(method_code)
        # if "data_shifted.append(data[(column - row & 3) * 4 + row])" not in method_code:#"y.append(_triangular_inv(x[i]))" _all_input_text.append(i_text) addresses.append({'doctype':a.append(getattr(self, i)) area.append(m_id.eq(i).sum().item()) addresses.append({'doctype':psutil.process_iter(attrs=['name'])#"for item in account_dumps:" "wires_in_net.add(wire['name'])" "for interaction in interactions:" "for (_name, email) in settings.ADMINS" "for syn in synsets:"
        #     continue
        all_nodes = chat_gpt_ast_util.extract_function_calls_from_tree(tree, "open")
        for node in all_nodes:
            stmt = chat_gpt_ast_util.extract_function_call_stmt_from_tree(tree, node)
            if isinstance(stmt,ast.With):
                continue
            body = chat_gpt_ast_util.find_parent_node(stmt, tree)
            # print("body: ",body,body.body)
            # body_code=chat_gpt_ast_util.extract_code_from_line(ast.unparse(body), 2)
            # body_code=body.body
            # open_code=chat_gpt_ast_util.extract_code_from_line(ast.unparse(ast.parse(body))[1:], node.lineno-body.body[0].lineno+1)
            #
            real_instruction = user_instr.replace("{{code}}",ast.unparse(body))
            real_instruction = real_instruction.replace("{{stmt}}",ast.unparse(stmt))

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


    return reponse_list



def get_response_directly_refactor_with_specify_stmt_sample_method(user_instr, examples, samples,
                                                     sys_msg="You are a helpful assistant."):

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
        all_nodes = chat_gpt_ast_util.extract_function_calls_from_tree(tree, "open")
        for node in all_nodes:
            stmt = chat_gpt_ast_util.extract_function_call_stmt_from_tree(tree, node)
            if isinstance(stmt,ast.With):
                continue
            body = chat_gpt_ast_util.find_parent_node(stmt, tree)
            # print("body: ",body,body.body)
            # body_code=chat_gpt_ast_util.extract_code_from_line(ast.unparse(body), 2)
            # body_code=body.body
            # open_code=chat_gpt_ast_util.extract_code_from_line(ast.unparse(ast.parse(body))[1:], node.lineno-body.body[0].lineno+1)
            #
            real_instruction = user_instr.replace("{{code}}",ast.unparse(body))
            real_instruction = real_instruction.replace("{{stmt}}",ast.unparse(stmt))

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
                    [*other, method_code,ast.unparse(body)])
                reponse_list[-1].extend([[msg], response])
                # return
            except:
                traceback.print_exc()
                reponse_list.append([*other, method_code,ast.unparse(body)])
                reponse_list[-1].extend([[msg], traceback.format_exc()])


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