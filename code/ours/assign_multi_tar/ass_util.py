import ast,os,sys
import copy
import traceback

import util_rewrite

code_dir = "/".join(os.path.abspath(__file__).split("/")[:-2]) + "/"
print("code path: ",code_dir)
sys.path.append(code_dir)
import chatgpt_util,random
import openai, tiktoken,ast,util
import code_extract_multi_ass,code_blocks_no_depedency

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
            tmp_list = code_extract_multi_ass.extract_all_consecutive_ass(method_code)

            for bool_node in tmp_list:
                if len(bool_node)<2:
                    continue
                consecutive_code_list= code_extract_multi_ass.extract_two_consecutive_ass(ast.unparse(bool_node))
                for consecutive_code in consecutive_code_list:
                    # print(">>>>>>>>>>bool_node: ",bool_node)
                    me_code = "\n".join([ast.unparse(assign).strip() for assign in consecutive_code])
                    me_code = "\n".join(
                        [f"stmt{i + 1}: " + e for i, e in enumerate(me_code.split("\n"))])

                    # me_code=ast.unparse(bool_node)
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
                        reponse_list.append([me_code, old_code, ast.unparse(bool_node), *other, new_code, method_code])
                        reponse_list[-1].extend([[msg, num_tokes], response])
                    except:
                        traceback.print_exc()
                        reponse_list.append([me_code, old_code,ast.unparse(bool_node), *other, new_code, method_code])
                        reponse_list[-1].extend([[msg, num_tokes], traceback.format_exc()])
                # break
        # '''
        return reponse_list


def get_response_instr_from_blocks(user_instr, examples, samples, sys_msg="You are a helpful assistant."):
    reponse_list = []
    method_code_list = []
    for ind_sampl, sample_method in enumerate(samples):
        for code in sample_method:
            # repo_name, old_path, file_html, class_name,me_name, old_list, new_tree,\
            #     old_code,new_code, method_code=code
            # break
            *other, old_list, new_tree, \
            old_code, new_code, method_code = code
            # print(">>>>method_code: ", method_code)
            # print(">>>>old_list: ", old_list)
            # print(">>>>old_code: ", old_code)
            # print(">>>>new_code: ", new_code)

            method_code_list.append([*other, old_list, new_tree, old_code, new_code, method_code])
            break
        # break
    print("len of method_code_list: ",len(method_code_list))
    count=0
    for *other, old_list, new_tree, old_code, new_code, method_code in method_code_list:
        tmp_list = code_extract_multi_ass.extract_all_consecutive_ass(method_code)
        # count += len(tmp_list)
        for bool_node in tmp_list:
            print("refer whole code: ",ast.unparse(bool_node))
            block_list = code_blocks_no_depedency.get_blocks_no_depdend(ast.unparse(bool_node))
            count += len(block_list)

            for me_code in block_list:
                print("me_code: ", me_code)

                # count+=1
                # continue

            # if len(bool_node) < 2:
            #     continue
            # consecutive_code_list = code_extract_multi_ass.extract_two_consecutive_ass(ast.unparse(bool_node))
            # for consecutive_code in consecutive_code_list:
                # print(">>>>>>>>>>bool_node: ",bool_node)
                # me_code = "\n".join([ast.unparse(assign).strip() for assign in block_code])
                # me_code = "\n".join(
                #     [f"stmt{i + 1}: " + e for i, e in enumerate(me_code.split("\n"))])

                # me_code=ast.unparse(bool_node)
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
                    reponse_list.append([me_code, old_code, ast.unparse(bool_node), *other, new_code, method_code])
                    reponse_list[-1].extend([[msg, num_tokes], response])
                except:
                    traceback.print_exc()
                    reponse_list.append([me_code, old_code, ast.unparse(bool_node), *other, new_code, method_code])
                    reponse_list[-1].extend([[msg, num_tokes], traceback.format_exc()])
            # break
    # '''
    print("count: ",count)
    return reponse_list

def get_response_instr_from_blocks_2(user_instr, examples, samples, sys_msg="You are a helpful assistant."):
    reponse_list = []
    method_code_list = []
    for ind_sampl, sample_method in enumerate(samples):
        for code in sample_method:
            # repo_name, old_path, file_html, class_name,me_name, old_list, new_tree,\
            #     old_code,new_code, method_code=code
            # break
            *other, old_list, new_tree, \
            old_code, new_code, method_code = code
            # print(">>>>method_code: ", method_code)
            # print(">>>>old_list: ", old_list)
            # print(">>>>old_code: ", old_code)
            # print(">>>>new_code: ", new_code)

            method_code_list.append([*other, old_list, new_tree, old_code, new_code, method_code])
            break
        # break
    print("len of method_code_list: ",len(method_code_list))
    count=0
    for *other, old_list, new_tree, old_code, new_code, method_code in method_code_list:
        standard_method_code=ast.unparse(ast.parse(method_code))
        tmp_list = code_extract_multi_ass.find_consecutive_assign_nodes(standard_method_code)
        # count += len(tmp_list)
        for bool_node_lisr in tmp_list:
            bool_node="\n".join([ast.unparse(e) for e in bool_node_lisr])
            # bool_node_str="\n".join(bool_node_lisr)
            print("refer whole code: ",bool_node)
            block_list = code_blocks_no_depedency.get_blocks_no_depdend_2(bool_node)
            count += len(block_list)

            for me_code in block_list:
                print("me_code: ", me_code)

                # count+=1
                # continue

            # if len(bool_node) < 2:
            #     continue
            # consecutive_code_list = code_extract_multi_ass.extract_two_consecutive_ass(ast.unparse(bool_node))
            # for consecutive_code in consecutive_code_list:
                # print(">>>>>>>>>>bool_node: ",bool_node)
                # me_code = "\n".join([ast.unparse(assign).strip() for assign in block_code])
                # me_code = "\n".join(
                #     [f"stmt{i + 1}: " + e for i, e in enumerate(me_code.split("\n"))])

                # me_code=ast.unparse(bool_node)
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
                    reponse_list.append([me_code, old_code, bool_node, *other, new_code, method_code])
                    reponse_list[-1].extend([[msg, num_tokes], response])
                except:
                    traceback.print_exc()
                    reponse_list.append([me_code, old_code, bool_node, *other, new_code, method_code])
                    reponse_list[-1].extend([[msg, num_tokes], traceback.format_exc()])
            # break
    # '''
    print("count: ",count)
    return reponse_list

def get_response_instr_from_blocks_3(user_instr, examples, samples, sys_msg="You are a helpful assistant."):
    reponse_list = []
    method_code_list = []
    for ind_sampl, sample_method in enumerate(samples):
        for code in sample_method:
            # repo_name, old_path, file_html, class_name,me_name, old_list, new_tree,\
            #     old_code,new_code, method_code=code
            # break
            *other, old_list, new_tree, \
            old_code, new_code, method_code = code
            # print(">>>>method_code: ", method_code)
            # print(">>>>old_list: ", old_list)
            # print(">>>>old_code: ", old_code)
            # print(">>>>new_code: ", new_code)

            method_code_list.append([*other, old_list, new_tree, old_code, new_code, method_code])
            break
        # break
    print("len of method_code_list: ",len(method_code_list))
    count=0
    for *other, old_list, new_tree, old_code, new_code, method_code in method_code_list:
        standard_method_code=ast.unparse(ast.parse(method_code))
        tmp_list = code_extract_multi_ass.find_consecutive_assign_nodes(standard_method_code)
        # count += len(tmp_list)
        for bool_node_lisr in tmp_list:
            bool_node="\n".join([ast.unparse(e) for e in bool_node_lisr])
            # bool_node_str="\n".join(bool_node_lisr)
            print("refer whole code: ",bool_node)
            block_list = code_blocks_no_depedency.get_blocks_no_depdend_3(bool_node)
            count += len(block_list)

            for me_code in block_list:
                print("me_code: ", me_code)
                # continue
                # count+=1
                # continue

            # if len(bool_node) < 2:
            #     continue
            # consecutive_code_list = code_extract_multi_ass.extract_two_consecutive_ass(ast.unparse(bool_node))
            # for consecutive_code in consecutive_code_list:
                # print(">>>>>>>>>>bool_node: ",bool_node)
                # me_code = "\n".join([ast.unparse(assign).strip() for assign in block_code])
                # me_code = "\n".join(
                #     [f"stmt{i + 1}: " + e for i, e in enumerate(me_code.split("\n"))])

                # me_code=ast.unparse(bool_node)
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
                    reponse_list.append([me_code, old_code, bool_node, *other, new_code, method_code])
                    reponse_list[-1].extend([[msg, num_tokes], response])
                except:
                    traceback.print_exc()
                    reponse_list.append([me_code, old_code, bool_node, *other, new_code, method_code])
                    reponse_list[-1].extend([[msg, num_tokes], traceback.format_exc()])
            # break
    # '''
    print("count: ",count)
    return reponse_list
def get_response_instr_from_abstract_blocks(user_instr, examples, samples, sys_msg="You are a helpful assistant."):
    reponse_list = []
    # reponse_list.append([abstract_me_code, value, abstract_value, *other, new_code, method_code])
    # for ind, e in enumerate(samples[0]):
    #     print(">>>other: ", ind, e)
    for me_code, old_code, whole_ass_code, *other, new_code, method_code, _, response in samples:

        content = response["choices"][0]["message"]["content"]
        abstract_code, symbols_map = parse_abstract_code(content)
        real_instruction = user_instr.replace("{{code}}", abstract_code)
        msg = chatgpt_util.format_message_2(real_instruction, examples=examples, sys_msg=sys_msg)
        print(">>>>>>>>>>real_instruction: ", real_instruction)
        num_tokes = chatgpt_util.num_tokens_from_messages(msg)
        # print("len of msg: ",chatgpt_util.num_tokens_from_messages(msg))
        # if chatgpt_util.num_tokens_from_messages(msg)>=chatgpt_util.MAX_TOKENS:
        #     response
        try:
            response = chatgpt_util.chatGPT_result(msg)
            print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
            reponse_list.append([abstract_code, symbols_map, me_code, old_code, *other, new_code, method_code])
            reponse_list[-1].extend([[msg, num_tokes], response])
        except:
            traceback.print_exc()
            reponse_list.append([abstract_code, symbols_map, me_code, old_code, *other, new_code, method_code])
            reponse_list[-1].extend([[msg, num_tokes], traceback.format_exc()])
    return reponse_list
def get_response_instr_from_abstract_blocks_2(user_instr, examples, samples, sys_msg="You are a helpful assistant."):
    reponse_list = []
    # reponse_list.append([abstract_me_code, value, abstract_value, *other, new_code, method_code])
    # for ind, e in enumerate(samples[0]):
    #     print(">>>other: ", ind, e)
    for me_code, old_code, whole_ass_code, *other, new_code, method_code, _, response in samples:
        if "slice2[axis] = slice(None, -1)" not in me_code:#self.tokenizer = tokenizer labels = utils.get_batch_label(dataset, idx) self.tokenizer = tokenizer self._fn = None slice2[axis] = slice(None, -1) doc = self._download_xml(self.fc0 = layers.fc(
            continue
        # if "slice2[axis] = slice(None, -1)" not in me_code:#doc = self._download_xml( num_classes = 10 self.fc0 = layers.fc(
        #     continue
        content = response["choices"][0]["message"]["content"]
        print(">> previous content: ",content)
        abstract_code, symbols_map = parse_abstract_code_2(content)
        print("abstract_code: ",abstract_code)
        real_instruction = user_instr.replace("{{code}}", abstract_code)
        msg = chatgpt_util.format_message_2(real_instruction, examples=examples, sys_msg=sys_msg)
        print(">>>>>>>>>>real_instruction: ", real_instruction)
        num_tokes = chatgpt_util.num_tokens_from_messages(msg)
        # print("len of msg: ",chatgpt_util.num_tokens_from_messages(msg))
        # if chatgpt_util.num_tokens_from_messages(msg)>=chatgpt_util.MAX_TOKENS:
        #     response
        try:
            response = chatgpt_util.chatGPT_result(msg)
            print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
            reponse_list.append([abstract_code, symbols_map, me_code, old_code, *other, new_code, method_code])
            reponse_list[-1].extend([[msg, num_tokes], response])
        except:
            traceback.print_exc()
            reponse_list.append([abstract_code, symbols_map, me_code, old_code, *other, new_code, method_code])
            reponse_list[-1].extend([[msg, num_tokes], traceback.format_exc()])
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
def parse_abstract_code(content):
    content_list=content.split("New Python code:")
    if len(content_list)==1:
        content_list = content.split("New Python Code:")

    symbols_list=content_list[0].strip().split("\n")
    symbols_map=dict()
    for i in symbols_list:
        if i.startswith("v"):
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
def get_response_instr_direct(user_instr, examples, samples, sys_msg="You are a helpful assistant."):
    reponse_list = []
    method_code_list = []
    for ind_sampl, sample_method in enumerate(samples):
        for code in sample_method:
            # repo_name, old_path, file_html, class_name,me_name, old_list, new_tree,\
            #     old_code,new_code, method_code=code
            # break
            *other, old_list, new_tree, \
            old_code, new_code, method_code = code
            # print(">>>>method_code: ", method_code)
            # print(">>>>old_list: ", old_list)
            # print(">>>>old_code: ", old_code)
            # print(">>>>new_code: ", new_code)

            method_code_list.append([*other, old_list, new_tree, old_code, new_code, method_code])
            break
        # break
    print("len of method_code_list: ",len(method_code_list))
    count = 0
    for *other, old_list, new_tree, old_code, new_code, method_code in method_code_list:
        standard_method_code = ast.unparse(ast.parse(method_code))
        tmp_list = code_extract_multi_ass.find_consecutive_assign_nodes(standard_method_code)
        # count += len(tmp_list)
        for bool_node_lisr in tmp_list:
            bool_node = "\n".join([ast.unparse(e) for e in bool_node_lisr])
            # bool_node_str="\n".join(bool_node_lisr)
            print("refer whole code: ", bool_node)
            block_list = code_blocks_no_depedency.get_blocks_no_depdend_2(bool_node)
            count += len(block_list)

            for me_code in block_list:
                print("me_code: ", me_code)

                # count+=1
                # continue

                # if len(bool_node) < 2:
                #     continue
                # consecutive_code_list = code_extract_multi_ass.extract_two_consecutive_ass(ast.unparse(bool_node))
                # for consecutive_code in consecutive_code_list:
                # print(">>>>>>>>>>bool_node: ",bool_node)
                # me_code = "\n".join([ast.unparse(assign).strip() for assign in block_code])
                # me_code = "\n".join(
                #     [f"stmt{i + 1}: " + e for i, e in enumerate(me_code.split("\n"))])

                # me_code=ast.unparse(bool_node)
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
                    reponse_list.append([me_code, old_code, bool_node, *other, new_code, method_code])
                    reponse_list[-1].extend([[msg, num_tokes], response])
                except:
                    traceback.print_exc()
                    reponse_list.append([me_code, old_code, bool_node, *other, new_code, method_code])
                    reponse_list[-1].extend([[msg, num_tokes], traceback.format_exc()])
            # break
    # '''
    print("count: ", count)
def get_response_from_previous_response_instr(user_instr, examples, samples, sys_msg="You are a helpful assistant."):
    reponse_list = []
    # reponse_list.append([abstract_me_code, value, abstract_value, *other, new_code, method_code])
    # for ind, e in enumerate(samples[0]):
    #     print(">>>other: ", ind, e)
    for me_code, old_code, *other, new_code, method_code, _, response in samples:

        content = response["choices"][0]["message"]["content"]
        abstract_code,symbols_map = parse_abstract_code(content)
        real_instruction = user_instr.replace("{{code}}", abstract_code)
        msg = chatgpt_util.format_message_2(real_instruction, examples=examples, sys_msg=sys_msg)
        print(">>>>>>>>>>real_instruction: ", real_instruction)
        num_tokes = chatgpt_util.num_tokens_from_messages(msg)
        # print("len of msg: ",chatgpt_util.num_tokens_from_messages(msg))
        # if chatgpt_util.num_tokens_from_messages(msg)>=chatgpt_util.MAX_TOKENS:
        #     response
        try:
            response = chatgpt_util.chatGPT_result(msg)
            print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
            reponse_list.append([abstract_code, symbols_map, me_code, old_code, *other, new_code, method_code])
            reponse_list[-1].extend([[msg, num_tokes], response])
        except:
            traceback.print_exc()
            reponse_list.append([abstract_code, symbols_map, me_code, old_code, *other, new_code, method_code])
            reponse_list[-1].extend([[msg, num_tokes], traceback.format_exc()])
    return reponse_list
def get_response_from_previous_response_instr_line_no(user_instr, examples, samples, sys_msg="You are a helpful assistant."):
    reponse_list = []
    # reponse_list.append([abstract_me_code, value, abstract_value, *other, new_code, method_code])
    # for ind, e in enumerate(samples[0]):
    #     print(">>>other: ", ind, e)
    for me_code, old_code, *other, new_code, method_code, _, response in samples:

        content = response["choices"][0]["message"]["content"]
        abstract_code,symbols_map = parse_abstract_code(content)
        abstract_code_lineno="\n".join([f"stmt{i+1}: "+e for i,e in enumerate(abstract_code.split("\n"))])
        real_instruction = user_instr.replace("{{code}}", abstract_code_lineno)
        msg = chatgpt_util.format_message_2(real_instruction, examples=examples, sys_msg=sys_msg)
        print(">>>>>>>>>>real_instruction: ", real_instruction)
        num_tokes = chatgpt_util.num_tokens_from_messages(msg)
        # print("len of msg: ",chatgpt_util.num_tokens_from_messages(msg))
        # if chatgpt_util.num_tokens_from_messages(msg)>=chatgpt_util.MAX_TOKENS:
        #     response
        try:
            response = chatgpt_util.chatGPT_result(msg)
            print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
            reponse_list.append([abstract_code, symbols_map, me_code, old_code, *other, new_code, method_code])
            reponse_list[-1].extend([[msg, num_tokes], response])
        except:
            traceback.print_exc()
            reponse_list.append([abstract_code, symbols_map, me_code, old_code, *other, new_code, method_code])
            reponse_list[-1].extend([[msg, num_tokes], traceback.format_exc()])
    return reponse_list
def get_response_from_previous_response_instr_line_no_ass_vars(user_instr, examples, samples, sys_msg="You are a helpful assistant."):
    reponse_list = []
    # reponse_list.append([abstract_me_code, value, abstract_value, *other, new_code, method_code])
    # for ind, e in enumerate(samples[0]):
    #     print(">>>other: ", ind, e)
    for me_code, old_code, *other, new_code, method_code, _, response in samples:

        content = response["choices"][0]["message"]["content"]
        abstract_code,symbols_map = parse_abstract_code(content)
        abstract_code_lineno="\n".join([f"stmt{i+1}: "+e for i,e in enumerate(abstract_code.split("\n"))])
        assign_vars = []
        count=0
        for e in ast.walk(ast.parse(abstract_code)):
            if isinstance(e,ast.Assign):
                for e2 in ast.walk(e):
                    if isinstance(e2, ast.Name):
                        count+=1
                        assign_vars.append(f"stmt{count}: "+ast.unparse(e2))
                        break
        real_instruction = user_instr.replace("{{code}}", abstract_code_lineno)
        real_instruction = real_instruction.replace("{{ass_var}}", "\n".join(assign_vars))

        msg = chatgpt_util.format_message_2(real_instruction, examples=examples, sys_msg=sys_msg)
        print(">>>>>>>>>>real_instruction: ", real_instruction)
        num_tokes = chatgpt_util.num_tokens_from_messages(msg)
        # print("len of msg: ",chatgpt_util.num_tokens_from_messages(msg))
        # if chatgpt_util.num_tokens_from_messages(msg)>=chatgpt_util.MAX_TOKENS:
        #     response
        try:
            response = chatgpt_util.chatGPT_result(msg)
            print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
            reponse_list.append([abstract_code, symbols_map, me_code, old_code, *other, new_code, method_code])
            reponse_list[-1].extend([[msg, num_tokes], response])
        except:
            traceback.print_exc()
            reponse_list.append([abstract_code, symbols_map, me_code, old_code, *other, new_code, method_code])
            reponse_list[-1].extend([[msg, num_tokes], traceback.format_exc()])
    return reponse_list
def get_response_from_previous_response_instr_line_no_dependency(user_instr, examples, samples, sys_msg="You are a helpful assistant."):
    reponse_list = []
    # reponse_list.append([abstract_me_code, value, abstract_value, *other, new_code, method_code])
    # for ind, e in enumerate(samples[0]):
    #     print(">>>other: ", ind, e)
    for abstract_code, symbols_map,me_code, old_code, *other, new_code, method_code, _, response in samples:

        content = response["choices"][0]["message"]["content"]
        dependency = parse_dependency(content)
        abstract_code_lineno="\n".join([f"stmt{i+1}: "+e for i,e in enumerate(abstract_code.split("\n"))])
        real_instruction = user_instr.replace("{{code}}", abstract_code_lineno)
        real_instruction = real_instruction.replace("{{dependency}}", dependency)

        msg = chatgpt_util.format_message_2(real_instruction, examples=examples, sys_msg=sys_msg)
        print(">>>>>>>>>>real_instruction: ", real_instruction)
        num_tokes = chatgpt_util.num_tokens_from_messages(msg)
        # print("len of msg: ",chatgpt_util.num_tokens_from_messages(msg))
        # if chatgpt_util.num_tokens_from_messages(msg)>=chatgpt_util.MAX_TOKENS:
        #     response
        try:
            response = chatgpt_util.chatGPT_result(msg)
            print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
            reponse_list.append([abstract_code, symbols_map, me_code, old_code, *other, new_code, method_code])
            reponse_list[-1].extend([[msg, num_tokes], response])
        except:
            traceback.print_exc()
            reponse_list.append([abstract_code, symbols_map, me_code, old_code, *other, new_code, method_code])
            reponse_list[-1].extend([[msg, num_tokes], traceback.format_exc()])
    return reponse_list
def get_response_from_previous_response_instr_line_no_dependency_instr_9(user_instr, examples, samples, sys_msg="You are a helpful assistant."):
    reponse_list = []
    # reponse_list.append([abstract_me_code, value, abstract_value, *other, new_code, method_code])
    # for ind, e in enumerate(samples[0]):
    #     print(">>>other: ", ind, e)
    for abstract_code, symbols_map,me_code, old_code, *other, new_code, method_code, _, response in samples:

        content = response["choices"][0]["message"]["content"]
        dependency = parse_dependency_2(content)
        abstract_code_lineno="\n".join([f"stmt{i+1}: "+e for i,e in enumerate(abstract_code.split("\n"))])
        real_instruction = user_instr.replace("{{code}}", abstract_code_lineno)
        real_instruction = real_instruction.replace("{{dependency}}", dependency)

        msg = chatgpt_util.format_message_2(real_instruction, examples=examples, sys_msg=sys_msg)
        print(">>>>>>>>>>real_instruction: ", real_instruction)
        num_tokes = chatgpt_util.num_tokens_from_messages(msg)
        # print("len of msg: ",chatgpt_util.num_tokens_from_messages(msg))
        # if chatgpt_util.num_tokens_from_messages(msg)>=chatgpt_util.MAX_TOKENS:
        #     response
        try:
            response = chatgpt_util.chatGPT_result(msg)
            print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
            reponse_list.append([abstract_code, symbols_map, me_code, old_code, *other, new_code, method_code])
            reponse_list[-1].extend([[msg, num_tokes], response])
        except:
            traceback.print_exc()
            reponse_list.append([abstract_code, symbols_map, me_code, old_code, *other, new_code, method_code])
            reponse_list[-1].extend([[msg, num_tokes], traceback.format_exc()])
    return reponse_list
def get_response_from_previous_response_instr_line_no_dependency_instr_10(user_instr, examples, samples, sys_msg="You are a helpful assistant."):
    reponse_list = []
    # reponse_list.append([abstract_me_code, value, abstract_value, *other, new_code, method_code])
    # for ind, e in enumerate(samples[0]):
    #     print(">>>other: ", ind, e)
    for abstract_code, symbols_map,me_code, old_code, *other, new_code, method_code, _, response in samples:

        content = response["choices"][0]["message"]["content"]
        dependency = parse_dependency_3(content)
        abstract_code_lineno="\n".join([f"stmt{i+1}: "+e for i,e in enumerate(abstract_code.split("\n"))])
        real_instruction = user_instr.replace("{{code}}", abstract_code_lineno)
        real_instruction = real_instruction.replace("{{dependency}}", dependency)

        msg = chatgpt_util.format_message_2(real_instruction, examples=examples, sys_msg=sys_msg)
        print(">>>>>>>>>>real_instruction: ", real_instruction)
        num_tokes = chatgpt_util.num_tokens_from_messages(msg)
        # print("len of msg: ",chatgpt_util.num_tokens_from_messages(msg))
        # if chatgpt_util.num_tokens_from_messages(msg)>=chatgpt_util.MAX_TOKENS:
        #     response
        try:
            response = chatgpt_util.chatGPT_result(msg)
            print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
            reponse_list.append([abstract_code, symbols_map, me_code, old_code, *other, new_code, method_code])
            reponse_list[-1].extend([[msg, num_tokes], response])
        except:
            traceback.print_exc()
            reponse_list.append([abstract_code, symbols_map, me_code, old_code, *other, new_code, method_code])
            reponse_list[-1].extend([[msg, num_tokes], traceback.format_exc()])
    return reponse_list
def get_response_from_previous_response_instr_line_no_dependency_instr_12(user_instr, examples, samples, sys_msg="You are a helpful assistant."):
    reponse_list = []
    # reponse_list.append([abstract_me_code, value, abstract_value, *other, new_code, method_code])
    # for ind, e in enumerate(samples[0]):
    #     print(">>>other: ", ind, e)
    for abstract_code, symbols_map,me_code, old_code, *other, new_code, method_code, _, response in samples:

        content = response["choices"][0]["message"]["content"]
        dependency = parse_dependency_4(content)
        abstract_code_lineno="\n".join([f"stmt{i+1}: "+e for i,e in enumerate(abstract_code.split("\n"))])
        real_instruction = user_instr.replace("{{code}}", abstract_code_lineno)
        real_instruction = real_instruction.replace("{{dependency}}", dependency)

        msg = chatgpt_util.format_message_2(real_instruction, examples=examples, sys_msg=sys_msg)
        print(">>>>>>>>>>real_instruction: ", real_instruction)
        num_tokes = chatgpt_util.num_tokens_from_messages(msg)
        # print("len of msg: ",chatgpt_util.num_tokens_from_messages(msg))
        # if chatgpt_util.num_tokens_from_messages(msg)>=chatgpt_util.MAX_TOKENS:
        #     response
        try:
            response = chatgpt_util.chatGPT_result(msg)
            print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
            reponse_list.append([abstract_code, symbols_map, me_code, old_code, *other, new_code, method_code])
            reponse_list[-1].extend([[msg, num_tokes], response])
        except:
            traceback.print_exc()
            reponse_list.append([abstract_code, symbols_map, me_code, old_code, *other, new_code, method_code])
            reponse_list[-1].extend([[msg, num_tokes], traceback.format_exc()])
    return reponse_list
def get_response_from_previous_response_instr_line_no_dependency_instr_14(user_instr, examples, samples, sys_msg="You are a helpful assistant."):
    reponse_list = []
    # reponse_list.append([abstract_me_code, value, abstract_value, *other, new_code, method_code])
    # for ind, e in enumerate(samples[0]):
    #     print(">>>other: ", ind, e)
    for abstract_code, symbols_map,me_code, old_code, *other, new_code, method_code, _, response in samples:

        content = response["choices"][0]["message"]["content"]
        dependency = parse_dependency_5(content)
        abstract_code_lineno="\n".join([f"stmt{i+1}: "+e for i,e in enumerate(abstract_code.split("\n"))])
        real_instruction = user_instr.replace("{{code}}", abstract_code_lineno)
        real_instruction = real_instruction.replace("{{dependency}}", dependency)

        msg = chatgpt_util.format_message_2(real_instruction, examples=examples, sys_msg=sys_msg)
        print(">>>>>>>>>>real_instruction: ", real_instruction)
        num_tokes = chatgpt_util.num_tokens_from_messages(msg)
        # print("len of msg: ",chatgpt_util.num_tokens_from_messages(msg))
        # if chatgpt_util.num_tokens_from_messages(msg)>=chatgpt_util.MAX_TOKENS:
        #     response
        try:
            response = chatgpt_util.chatGPT_result(msg)
            print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
            reponse_list.append([abstract_code, symbols_map, me_code, old_code, *other, new_code, method_code])
            reponse_list[-1].extend([[msg, num_tokes], response])
        except:
            traceback.print_exc()
            reponse_list.append([abstract_code, symbols_map, me_code, old_code, *other, new_code, method_code])
            reponse_list[-1].extend([[msg, num_tokes], traceback.format_exc()])
    return reponse_list
def get_response_from_previous_response_instr_line_no_dependency_iter(user_instr, examples, samples, sys_msg="You are a helpful assistant."):
    reponse_list = []
    # reponse_list.append([abstract_me_code, value, abstract_value, *other, new_code, method_code])
    # for ind, e in enumerate(samples[0]):
    #     print(">>>other: ", ind, e)
    for abstract_code, symbols_map,me_code, old_code, *other, new_code, method_code, _, response in samples:

        content = response["choices"][0]["message"]["content"]
        dependency = content.strip()
        abstract_code_lineno="\n".join([f"stmt{i+1}: "+e for i,e in enumerate(abstract_code.split("\n"))])
        real_instruction = user_instr.replace("{{code}}", abstract_code_lineno)
        real_instruction = real_instruction.replace("{{dependency}}", dependency)

        msg = chatgpt_util.format_message_2(real_instruction, examples=examples, sys_msg=sys_msg)
        print(">>>>>>>>>>real_instruction: ", real_instruction)
        num_tokes = chatgpt_util.num_tokens_from_messages(msg)
        # print("len of msg: ",chatgpt_util.num_tokens_from_messages(msg))
        # if chatgpt_util.num_tokens_from_messages(msg)>=chatgpt_util.MAX_TOKENS:
        #     response
        try:
            response = chatgpt_util.chatGPT_result(msg)
            print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
            reponse_list.append([abstract_code, symbols_map, me_code, old_code, *other, new_code, method_code])
            reponse_list[-1].extend([[msg, num_tokes], response])
        except:
            traceback.print_exc()
            reponse_list.append([abstract_code, symbols_map, me_code, old_code, *other, new_code, method_code])
            reponse_list[-1].extend([[msg, num_tokes], traceback.format_exc()])
    return reponse_list
def get_response_from_previous_response_instr_line_no_dependency_instr_9(user_instr, examples, samples, sys_msg="You are a helpful assistant."):
    reponse_list = []
    # reponse_list.append([abstract_me_code, value, abstract_value, *other, new_code, method_code])
    # for ind, e in enumerate(samples[0]):
    #     print(">>>other: ", ind, e)
    for abstract_code, symbols_map,me_code, old_code, *other, new_code, method_code, _, response in samples:

        content = response["choices"][0]["message"]["content"]
        dependency = parse_dependency_6(content)
        abstract_code_lineno="\n".join([f"stmt{i+1}: "+e for i,e in enumerate(abstract_code.split("\n"))])
        real_instruction = user_instr.replace("{{code}}", abstract_code_lineno)
        real_instruction = real_instruction.replace("{{dependency}}", dependency)

        msg = chatgpt_util.format_message_2(real_instruction, examples=examples, sys_msg=sys_msg)
        print(">>>>>>>>>>real_instruction: ", real_instruction)
        num_tokes = chatgpt_util.num_tokens_from_messages(msg)
        # print("len of msg: ",chatgpt_util.num_tokens_from_messages(msg))
        # if chatgpt_util.num_tokens_from_messages(msg)>=chatgpt_util.MAX_TOKENS:
        #     response
        try:
            response = chatgpt_util.chatGPT_result(msg)
            print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
            reponse_list.append([abstract_code, symbols_map, me_code, old_code, *other, new_code, method_code])
            reponse_list[-1].extend([[msg, num_tokes], response])
        except:
            traceback.print_exc()
            reponse_list.append([abstract_code, symbols_map, me_code, old_code, *other, new_code, method_code])
            reponse_list[-1].extend([[msg, num_tokes], traceback.format_exc()])
    return reponse_list
def parse_dependency_6(content):
    new_content = []
    content_list = content.split("\n")
    for e in content_list:
        if " None" in e:
            continue
        new_e=util_rewrite.replace_first_occur(":", " uses assigned variable of ", e)
        new_content.append(new_e)
    if not new_content:
        return "The code's statements do not have data dependency "
    return "\n".join(new_content)
def parse_dependency_5(content):
    new_content = []
    content_list = content.split("\n")
    for e in content_list:
        if " None" in e:
            continue
        new_e=util_rewrite.replace_first_occur(":", " data depends on ", e)
        new_content.append(new_e)
    if not new_content:
        return "The code's statements do not have data dependency "
    return "\n".join(new_content)
def parse_dependency_4(content):
    new_content = []
    content_list = content.split("\n")
    for e in content_list:
        if " None" in e:
            continue
        new_e=util_rewrite.replace_first_occur(":", " and ", e)
        new_e=new_e+" are different blocks"
        new_content.append(new_e)
    if not new_content:
        return "None"
    return "\n".join(new_content)
def parse_dependency_3(content):
    new_content = []
    content_list = content.split("\n")
    for e in content_list:
        if " None" in e:
            continue
        new_e=util_rewrite.replace_first_occur(":", " and ", e)
        new_e="separate "+new_e+" into different blocks"
        new_content.append(new_e)
    if not new_content:
        return "None"
    return "\n".join(new_content)
def parse_dependency_2(content):
    new_content = []
    content_list = content.split("\n")
    for e in content_list:
        if " None" in e:
            continue
        new_e=util_rewrite.replace_first_occur(":", " is different from the block of ", e)
        new_e="the block of "+new_e
        new_content.append(new_e)
    if not new_content:
        return "None"
    return "\n".join(new_content)

def parse_dependency(content):
    new_content=[]
    content_list=content.split("\n")
    for e in content_list:
        if " None" in e:
            continue
        new_content.append(util_rewrite.replace_first_occur(":","'s block is different from the block of ",e))
    if not new_content:
        return "None"
    return "\n".join(new_content)
    # return content.strip()
def parse_block(content):
    blk_list=[]
    cur_list=[]

    content_list=content.split("\n")
    for content in content_list:
        if "block" in content:
            if cur_list:
                blk_list.append(cur_list)
            cur_list=[]
        else:
            real_content=content.strip()
            if real_content:
                cur_list.append(real_content)

    return blk_list



# def get_response_directly_refactor(user_instr, examples, samples, sys_msg="You are a helpful assistant."):

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
            continue
            e[-1] = old_refactor_code
            # e.extend([element_str, slice_str])
            # e.append("Cannot refactor")
            e.append(1)
            acc += 1
        predict_res.append(e + other)

    predict_res.append(["NOFOUND"])

    for ind,e in enumerate(ground_copy_truth_list):
            predict_res.append(e+[0])
    print("acc: ",acc,len(predict_res),acc/len(ground_truth_list))
    print("precision: ",pre,len(predict_res),pre/len(ground_truth_list))

    return predict_res