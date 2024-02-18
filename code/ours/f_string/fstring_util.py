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
def parse_abstract_code(content):
    content_list=content.split("New Python code:")
    if len(content_list)==1:
        content_list = content.split("New Python Code:")

    symbols_list=content_list[0].strip().split("\n")
    symbols_map=dict()
    for i in symbols_list:
        if i.startswith("e_zj"):
            key=i.split(":")[0]
            value=":".join(i.split(":")[1:]).strip()
            symbols_map[key]=value

    content = content_list[-1]
    return content.strip(),symbols_map
def get_response_directly_refactor(user_instr, examples, samples,
                                                     sys_msg="You are a helpful assistant."):
    count=0
    reponse_list = []
    # method_code_list = []
    # one_other = []
    # for ind_sampl, sample_method in enumerate(samples):
    #     method_code_list.append(sample_method)

    for *other, node in samples:

        if 1:
            code=ast.unparse(node)
            # if "tabRepayment Schedule" not in code:#fmt % (full_tag, tag_prefix) thumbnail:%s can't open (%s) %04x Can't read --exclude-file: svg width=
            #     continue
            # code="section.PointerToRawData % e_zj_1"
            # code="'UPDATE `tabRepayment Schedule`\n\t\t\tSET is_accrued = 1 where name in (%s)' % zj1"
            # code="'UPDATE `tabRepayment Schedule`\n\t\t\tSET is_accrued = 1 where name in (%s)' % zj1, zj2"
            real_instruction = user_instr.replace("{{code}}",code)

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
                    [*other,node])
                reponse_list[-1].extend([[msg], response])
                # return
            except:
                traceback.print_exc()
                reponse_list.append([*other,node])
                reponse_list[-1].extend([[msg], traceback.format_exc()])
            # break
            # '''
    print("count: ",count)
    return reponse_list
def extract_module(samples):
    all_codes=[]
    count=0
    reponse_list = []
    method_code_list = []
    one_other = []
    for ind_sampl, sample_method in enumerate(samples):
        method_code_list.append(sample_method)
        if ind_sampl>=3000:
            break

    for *other, method_code in method_code_list:
        # if "do_setup$1697" not in other:
        #     continue
        # print(other[2:])

        method_code=ast.parse(method_code)
        # tree=ast.parse(method_code)
        # if "data_shifted.append(data[(column - row & 3) * 4 + row])" not in method_code:#"y.append(_triangular_inv(x[i]))" _all_input_text.append(i_text) addresses.append({'doctype':a.append(getattr(self, i)) area.append(m_id.eq(i).sum().item()) addresses.append({'doctype':psutil.process_iter(attrs=['name'])#"for item in account_dumps:" "wires_in_net.add(wire['name'])" "for interaction in interactions:" "for (_name, email) in settings.ADMINS" "for syn in synsets:"
        #     continue
        all_nodes = chat_gpt_ast_util.extract_old_formatted_strings_new(method_code)
        for node in all_nodes:
                count += 1
                all_codes.append([*other,method_code,node])
                # print("code:\n", "\n".join([ast.unparse(e) for e in ass_list]))
                # break
    print("count: ",count)
    return all_codes
def extract_module_new(method_code_list):
    all_codes=[]
    count=0
    # reponse_list = []
    # method_code_list = []
    # one_other = []
    # for ind_sampl, sample_method in enumerate(samples):
    #     method_code_list.append(sample_method)
    #     if ind_sampl>=3000:
    #         break

    for *other, method_code in method_code_list:
        # if "do_setup$1697" not in other:
        #     continue
        # print(other[2:])

        method_code=ast.parse(method_code)
        # tree=ast.parse(method_code)
        # if "data_shifted.append(data[(column - row & 3) * 4 + row])" not in method_code:#"y.append(_triangular_inv(x[i]))" _all_input_text.append(i_text) addresses.append({'doctype':a.append(getattr(self, i)) area.append(m_id.eq(i).sum().item()) addresses.append({'doctype':psutil.process_iter(attrs=['name'])#"for item in account_dumps:" "wires_in_net.add(wire['name'])" "for interaction in interactions:" "for (_name, email) in settings.ADMINS" "for syn in synsets:"
        #     continue
        all_nodes = chat_gpt_ast_util.extract_old_formatted_strings_new(method_code)
        for node in all_nodes:
                count += 1
                all_codes.append([*other,method_code,node])
                # print("code:\n", "\n".join([ast.unparse(e) for e in ass_list]))
                # break
    print("count: ",count)
    return all_codes
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