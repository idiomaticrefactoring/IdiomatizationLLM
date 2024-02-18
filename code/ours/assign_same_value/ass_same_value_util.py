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
    count=0
    reponse_list = []
    # method_code_list = []
    # one_other = []
    # for ind_sampl, sample_method in enumerate(samples):
    #     method_code_list.append(sample_method)

    for *other, ass_code in samples:
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
            real_instruction = user_instr.replace("{{code}}","\n".join(ass_code))

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
                    [*other,ass_code])
                reponse_list[-1].extend([[msg], response])
                # return
            except:
                traceback.print_exc()
                reponse_list.append([*other,ass_code])
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
def extract_module(samples):
    all_codes=[]
    count=0
    reponse_list = []
    method_code_list = []
    one_other = []
    for ind_sampl, sample_method in enumerate(samples):
        method_code_list.append(sample_method)
        # if ind_sampl>=9000:
        #     break

    for *other, method_code in method_code_list:
        # if "do_setup$1697" not in other:
        #     continue
        # print(other[2:])

        method_code=ast.unparse(ast.parse(method_code))
        # tree=ast.parse(method_code)
        # if "data_shifted.append(data[(column - row & 3) * 4 + row])" not in method_code:#"y.append(_triangular_inv(x[i]))" _all_input_text.append(i_text) addresses.append({'doctype':a.append(getattr(self, i)) area.append(m_id.eq(i).sum().item()) addresses.append({'doctype':psutil.process_iter(attrs=['name'])#"for item in account_dumps:" "wires_in_net.add(wire['name'])" "for interaction in interactions:" "for (_name, email) in settings.ADMINS" "for syn in synsets:"
        #     continue
        all_nodes = chat_gpt_ast_util.find_consecutive_assign_nodes(method_code)
        for nodes in all_nodes:
            ass_same_value_nodes=chat_gpt_ast_util.group_assign_nodes(nodes)
            for ass_list in ass_same_value_nodes:
                if len(ass_list)<=1:
                    continue
                count += 1
                all_codes.append([*other,method_code,[ast.unparse(e) for e in ass_list]])
                # print("code:\n", "\n".join([ast.unparse(e) for e in ass_list]))
                # break
    print("count: ",count)
    return all_codes

def extract_module_consecutive_ass(samples):
    all_codes=[]
    count=0
    reponse_list = []
    method_code_list = []
    one_other = []
    for ind_sampl, sample_method in enumerate(samples):
        method_code_list.append(sample_method)
        # if ind_sampl>=9000:
        #     break

    for *other, method_code in method_code_list:
        # if "do_setup$1697" not in other:
        #     continue
        # print(other[2:])

        method_code=ast.unparse(ast.parse(method_code))
        # tree=ast.parse(method_code)
        # if "data_shifted.append(data[(column - row & 3) * 4 + row])" not in method_code:#"y.append(_triangular_inv(x[i]))" _all_input_text.append(i_text) addresses.append({'doctype':a.append(getattr(self, i)) area.append(m_id.eq(i).sum().item()) addresses.append({'doctype':psutil.process_iter(attrs=['name'])#"for item in account_dumps:" "wires_in_net.add(wire['name'])" "for interaction in interactions:" "for (_name, email) in settings.ADMINS" "for syn in synsets:"
        #     continue
        all_nodes = chat_gpt_ast_util.find_consecutive_assign_nodes(method_code)
        for nodes in all_nodes:

            ass_same_value_nodes=chat_gpt_ast_util.group_consecutive_assign_nodes(nodes)
            for ass_list in ass_same_value_nodes:
                if len(ass_list)<=1:
                    continue
                count += 1
                all_codes.append([*other,method_code,[ast.unparse(e) for e in ass_list]])
                # print("code:\n", "\n".join([ast.unparse(e) for e in ass_list]))
                # break
    print("count: ",count)
    return all_codes

def extract_module_consecutive_ass_from_methods(method_code_list):
    all_codes=[]
    count=0
    reponse_list = []
    one_other = []


    for *other, method_code in method_code_list:
        # if "do_setup$1697" not in other:
        #     continue
        # print(other[2:])
        if "def set_missing_values(source, target):" not in method_code:
            continue
        method_code=ast.unparse(ast.parse(method_code))
        # tree=ast.parse(method_code)
        # if "data_shifted.append(data[(column - row & 3) * 4 + row])" not in method_code:#"y.append(_triangular_inv(x[i]))" _all_input_text.append(i_text) addresses.append({'doctype':a.append(getattr(self, i)) area.append(m_id.eq(i).sum().item()) addresses.append({'doctype':psutil.process_iter(attrs=['name'])#"for item in account_dumps:" "wires_in_net.add(wire['name'])" "for interaction in interactions:" "for (_name, email) in settings.ADMINS" "for syn in synsets:"
        #     continue
        all_nodes = chat_gpt_ast_util.find_consecutive_assign_nodes(method_code)
        for nodes in all_nodes:

            ass_same_value_nodes=chat_gpt_ast_util.group_consecutive_assign_nodes(nodes)
            for ass_list in ass_same_value_nodes:
                if len(ass_list)<=1:
                    continue
                count += 1
                # if "target.discount_amount = 0.0" not in [ast.unparse(e) for e in ass_list]:#self._receiver = None
                #     continue
                print([ast.unparse(e) for e in ass_list])
                all_codes.append([*other,method_code,[ast.unparse(e) for e in ass_list]])
                # print("code:\n", "\n".join([ast.unparse(e) for e in ass_list]))
                # break
    print("count: ",count)
    return all_codes
def get_response_refactor_from_abstract(user_instr, examples, samples,
                                                     sys_msg="You are a helpful assistant."):
    count=0
    reponse_list = []


    for *other, ass_code,_,response in samples:

        if 1:
            if "self._receiver = None" not in ass_code:
                continue
            content = response["choices"][0]["message"]["content"]
            abstract_ass_code,symbols_map=parse_abstract_code_2(content)
            real_instruction = user_instr.replace("{{code}}",abstract_ass_code)
            print(" abstract_ass_code,symbols_map: ",symbols_map,abstract_ass_code)
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
                    [*other,ass_code,abstract_ass_code, symbols_map])
                reponse_list[-1].extend([[msg], response])
                # return
            except:
                traceback.print_exc()
                reponse_list.append([*other,ass_code,abstract_ass_code, symbols_map])
                reponse_list[-1].extend([[msg], traceback.format_exc()])
            # break
            # '''
    print("count: ",count)
    return reponse_list


def parse_abstract_code_2(content):
    content_list=content.split("New Python code:")
    if len(content_list)==1:
        content_list = content.split("New Python Code:")

    symbols_list=content_list[0].strip().split("\n")
    symbols_map=dict()
    for i in symbols_list:
        if i.startswith("zj"):
            key=i.split(":")[0]
            value=":".join(i.split(":")[1:]).strip()
            symbols_map[key]=value

    content = content_list[-1]
    return content.strip(),symbols_map

def parse_code(content):
    content_list=content.split("New Python code:")
    if len(content_list)==1:
        content_list = content.split("New Python Code:")

    if "No" in content_list[0]:
        return 0, None
    content = content_list[-1].strip().split("\n")[0].strip()
    return 1,content