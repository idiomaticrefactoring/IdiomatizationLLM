import ast,os,sys
import copy
import time
import traceback

import util_rewrite

code_dir = "/".join(os.path.abspath(__file__).split("/")[:-2]) + "/"
print("code path: ",code_dir)
sys.path.append(code_dir)
import chatgpt_util,random
import openai, tiktoken,ast,util
import loop_else_code_instr,loop_else_code_instr_node

def get_response_instr(user_instr, examples, samples, sys_msg="You are a helpful assistant."):
    reponse_list = []
    method_code_list = []
    for ind_sampl, sample_method in enumerate(samples):
        for code in sample_method:
            # repo_name, old_path, file_html, class_name,me_name, old_list, new_tree,\
            #     old_code,new_code, method_code=code
            # break
            # samples_csv = [[repo, file_html, me_name, me_code, ast.unparse(ass_node) + "\n" + ast.unparse(for_node),
            #                 ast.unparse(new_node), str(remove_ass_flag)] for (
            #                repo, file_path, file_html, class_name, me_name, for_node, ass_node, remove_ass_flag,
            #                new_node, me_code) in samples]
            # for ind, e in enumerate(code):
            #     print("ind>> ",ind, e)
            # print("code: ",code)
            *other, (ass_node_old, for_node_old, if_node,remove_ass_flag, break_list), for_node_old, total_old_code, new_code, method_code = code
            # print(">>>>ass_node_old: ", ass_node_old)

            '''
            print(">>>>for_node: ", for_node_old)
            print(">>>>remove_ass_flag: ", remove_ass_flag)
            print(">>>>ass_node: ", total_old_code)
            # print(">>>>method_code: ", method_code)
            print(">>>>new_node: ", new_code)
            '''
            # print(">>>>me_code: ", new_loop_me_code)
            # print(">>>>remove_ass_flag: ", remove_ass_flag)
            method_code_list.append([*other, for_node_old, ast.unparse(ass_node_old),total_old_code, new_code, method_code])
            break
        # break
    # return
    for *other, for_node_old, ass_code,total_old_code, new_code, me_code in method_code_list:
        tmp_list = loop_else_code_instr.whole_code_pair_for_if(ast.unparse(ast.parse(me_code)))
        print(">>>>>>>>>>tmp_list: ", tmp_list)

        for bool_node in tmp_list:
                bool_node_str="\n".join(bool_node)
                real_instruction = user_instr.replace("{{code}}",bool_node_str )

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
                    print("new code: ",new_code)
                    reponse_list.append([bool_node_str, ass_code,*other, new_code, me_code])
                    reponse_list[-1].extend([[msg, num_tokes], response])
                except:
                    traceback.print_exc()
                    reponse_list.append([bool_node_str,ass_code, *other, new_code, me_code])
                    reponse_list[-1].extend([[msg, num_tokes], traceback.format_exc()])
            # break
    # '''
    return reponse_list

def get_response_instr_if_statement(user_instr, examples, samples, sys_msg="You are a helpful assistant."):
    reponse_list = []
    method_code_list = []
    for ind_sampl, sample_method in enumerate(samples):
        for code in sample_method:
            # repo_name, old_path, file_html, class_name,me_name, old_list, new_tree,\
            #     old_code,new_code, method_code=code
            # break
            # samples_csv = [[repo, file_html, me_name, me_code, ast.unparse(ass_node) + "\n" + ast.unparse(for_node),
            #                 ast.unparse(new_node), str(remove_ass_flag)] for (
            #                repo, file_path, file_html, class_name, me_name, for_node, ass_node, remove_ass_flag,
            #                new_node, me_code) in samples]
            # for ind, e in enumerate(code):
            #     print("ind>> ",ind, e)
            # print("code: ",code)
            *other, (ass_node_old, for_node_old, if_node,remove_ass_flag, break_list), for_node_old, total_old_code, new_code, method_code = code
            # print(">>>>ass_node_old: ", ass_node_old)

            '''
            print(">>>>for_node: ", for_node_old)
            print(">>>>remove_ass_flag: ", remove_ass_flag)
            print(">>>>ass_node: ", total_old_code)
            # print(">>>>method_code: ", method_code)
            print(">>>>new_node: ", new_code)
            '''
            # print(">>>>me_code: ", new_loop_me_code)
            # print(">>>>remove_ass_flag: ", remove_ass_flag)
            method_code_list.append([*other, for_node_old, ast.unparse(ass_node_old),total_old_code, new_code, method_code])
            break
        # break
    # return
    for *other, for_node_old, ass_code,total_old_code, new_code, me_code in method_code_list:
        tmp_list = loop_else_code_instr.whole_code_pair_for_if(ast.unparse(ast.parse(me_code)))
        # print(">>>>>>>>>>tmp_list: ", tmp_list)

        for bool_node in tmp_list:
                bool_node_str=bool_node[1]
                real_instruction = user_instr.replace("{{code}}",bool_node_str )

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
                    # print("new code: ",new_code)
                    # reponse_list.append([bool_node_str, ass_code,*other, new_code, me_code])

                    reponse_list.append([bool_node,bool_node_str, ass_code,*other, new_code, me_code])
                    reponse_list[-1].extend([[msg, num_tokes], response])
                except:
                    traceback.print_exc()
                    reponse_list.append([bool_node,bool_node_str,ass_code, *other, new_code, me_code])
                    reponse_list[-1].extend([[msg, num_tokes], traceback.format_exc()])

    return reponse_list
def get_response_instr_if_statement_add_new_information(user_instr, examples, samples, sys_msg="You are a helpful assistant."):
    reponse_list = []
    method_code_list = []
    for ind_sampl, sample_method in enumerate(samples):
        for code in sample_method:
            # repo_name, old_path, file_html, class_name,me_name, old_list, new_tree,\
            #     old_code,new_code, method_code=code
            # break
            # samples_csv = [[repo, file_html, me_name, me_code, ast.unparse(ass_node) + "\n" + ast.unparse(for_node),
            #                 ast.unparse(new_node), str(remove_ass_flag)] for (
            #                repo, file_path, file_html, class_name, me_name, for_node, ass_node, remove_ass_flag,
            #                new_node, me_code) in samples]
            # for ind, e in enumerate(code):
            #     print("ind>> ",ind, e)
            # print("code: ",code)
            *other, (ass_node_old, for_node_old, if_node,remove_ass_flag, break_list), for_node_old, total_old_code, new_code, method_code = code
            # print(">>>>ass_node_old: ", ass_node_old)

            '''
            print(">>>>for_node: ", for_node_old)
            print(">>>>remove_ass_flag: ", remove_ass_flag)
            print(">>>>ass_node: ", total_old_code)
            # print(">>>>method_code: ", method_code)
            print(">>>>new_node: ", new_code)
            '''
            # print(">>>>me_code: ", new_loop_me_code)
            # print(">>>>remove_ass_flag: ", remove_ass_flag)
            method_code_list.append([*other, for_node_old, ast.unparse(ass_node_old),total_old_code, new_code, method_code])
            break
        # break
    # return
    for *other, for_node_old, ass_code,total_old_code, new_code, me_code in method_code_list:
        tmp_list = loop_else_code_instr_node.whole_code_pair_get_break_list_for_if(ast.unparse(ast.parse(me_code)))
        print(">>>>>>>>>>tmp_list: ", tmp_list)

        for loop_str,if_str, break_list,has_used_var_in_if, assign_in_block_of_break in tmp_list:
                old_if_str,old_loop_str=loop_str,if_str
                bool_node_str=if_str

                def get_name_nodes(tree):
                    name_nodes = []
                    for node in ast.walk(tree):
                        if isinstance(node, ast.Name):
                            name_nodes.append(node)
                    return name_nodes
                symbol_name_if_map=dict()
                var_in_if_list=[]
                for e in ast.walk(ast.parse(if_str)):
                    if isinstance(e,ast.If):
                        var_in_if_list =[ast.unparse(e) for e in  list(set(get_name_nodes(e.test)))]
                        for ind, var in enumerate(var_in_if_list):
                            symbol='flag_'+str(ind)
                            loop_str=loop_str.replace(var,symbol)
                            if_str=if_str.replace(var,symbol)
                            symbol_name_if_map[symbol]=var
                        break
                real_instruction = user_instr.replace("{{code}}",if_str )

                # real_instruction=real_instruction+4000*'abc'
                print(">>>>>>>>>>Instr: ", real_instruction)
                continue
                msg = chatgpt_util.format_message_2(real_instruction, examples=examples, sys_msg=sys_msg)
                # print(">>>>>>>>>>each msg: ", msg)
                num_tokes = chatgpt_util.num_tokens_from_messages(msg)
                # print("len of msg: ",chatgpt_util.num_tokens_from_messages(msg))
                # if chatgpt_util.num_tokens_from_messages(msg)>=chatgpt_util.MAX_TOKENS:
                #     response
                try:
                    response = chatgpt_util.chatGPT_result(msg)
                    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
                    print("new code: ",new_code)
                    # reponse_list.append([bool_node_str, ass_code,*other, new_code, me_code])

                    reponse_list.append([loop_str+"\n"+if_str, loop_str, if_str, has_used_var_in_if, assign_in_block_of_break, ass_code, *other, new_code, me_code])
                    reponse_list[-1].extend([[msg, num_tokes], response])
                except:
                    traceback.print_exc()
                    reponse_list.append([loop_str+"\n"+if_str,bool_node_str,ass_code, *other, new_code, me_code])
                    reponse_list[-1].extend([[msg, num_tokes], traceback.format_exc()])

    return reponse_list
def get_response_instr_abstract_break_block(user_instr, examples, samples, sys_msg="You are a helpful assistant."):
    reponse_list = []
    method_code_list = []
    for ind_sampl, sample_method in enumerate(samples):
        for code in sample_method:
            # repo_name, old_path, file_html, class_name,me_name, old_list, new_tree,\
            #     old_code,new_code, method_code=code
            # break
            # samples_csv = [[repo, file_html, me_name, me_code, ast.unparse(ass_node) + "\n" + ast.unparse(for_node),
            #                 ast.unparse(new_node), str(remove_ass_flag)] for (
            #                repo, file_path, file_html, class_name, me_name, for_node, ass_node, remove_ass_flag,
            #                new_node, me_code) in samples]
            # for ind, e in enumerate(code):
            #     print("ind>> ",ind, e)
            # print("code: ",code)
            *other, (ass_node_old, for_node_old, if_node,remove_ass_flag, break_list), for_node_old, total_old_code, new_code, method_code = code
            # print(">>>>ass_node_old: ", ass_node_old)

            '''
            print(">>>>for_node: ", for_node_old)
            print(">>>>remove_ass_flag: ", remove_ass_flag)
            print(">>>>ass_node: ", total_old_code)
            # print(">>>>method_code: ", method_code)
            print(">>>>new_node: ", new_code)
            '''
            # print(">>>>me_code: ", new_loop_me_code)
            # print(">>>>remove_ass_flag: ", remove_ass_flag)
            method_code_list.append([*other, for_node_old, ast.unparse(ass_node_old),total_old_code, new_code, method_code])
            break
        # break
    # return
    for *other, for_node_old, ass_code,total_old_code, new_code, me_code in method_code_list:
        tmp_list = loop_else_code_instr_node.whole_code_pair_get_break_list_for_if(ast.unparse(ast.parse(me_code)))
        print(">>>>>>>>>>tmp_list: ", tmp_list)
        # new_pairs.append((loop_node, if_node, break_parent_list,has_used, ass_in_for_list))

        for loop_node,if_node, break_parent_list,has_used_var_in_if, assign_in_block_of_break in tmp_list:
                loop_str, if_str=ast.unparse(loop_node),ast.unparse(if_node)
                # print(">>>find code: ",loop_str,if_str)
                total_code=["for e in e_list:"]
                print(">>>len of break_parent_list: ",len(break_parent_list))
                for break_node in break_parent_list:
                    # print("parent of break code: ",ast.unparse(break_node))
                    total_code+=["    "+line for ind, line in enumerate(ast.unparse(break_node).split("\n")) ]
                total_replace_for_code="\n".join(total_code)
                # print("total_replace_for_code: ",total_replace_for_code)
                # continue
                # for ass in assign_in_block_of_break:
                #     print(">>>>>>ass code: ",ast.unparse(ass))

                # print(">>>>>>ass code: ", ast.unparse(ass))
                real_instruction = user_instr.replace("{{code}}",if_str )

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
                    print("new code: ",new_code)
                    # reponse_list.append([bool_node_str, ass_code,*other, new_code, me_code])

                    reponse_list.append([loop_str+"\n"+if_str,total_replace_for_code, loop_node,if_node, break_parent_list,has_used_var_in_if, assign_in_block_of_break, ass_code, *other, new_code, me_code])
                    reponse_list[-1].extend([[msg, num_tokes], response])
                except:
                    traceback.print_exc()
                    reponse_list.append([loop_str+"\n"+if_str,total_replace_for_code,loop_node,if_node, break_parent_list,has_used_var_in_if, assign_in_block_of_break, ass_code, *other, new_code, me_code])
                    reponse_list[-1].extend([[msg, num_tokes], traceback.format_exc()])

    return reponse_list

def get_response_instr_abstract_break_block_1(user_instr, examples, samples, sys_msg="You are a helpful assistant."):
    reponse_list = []
    method_code_list = []
    for ind_sampl, sample_method in enumerate(samples):
        for code in sample_method:
            # repo_name, old_path, file_html, class_name,me_name, old_list, new_tree,\
            #     old_code,new_code, method_code=code
            # break
            # samples_csv = [[repo, file_html, me_name, me_code, ast.unparse(ass_node) + "\n" + ast.unparse(for_node),
            #                 ast.unparse(new_node), str(remove_ass_flag)] for (
            #                repo, file_path, file_html, class_name, me_name, for_node, ass_node, remove_ass_flag,
            #                new_node, me_code) in samples]
            # for ind, e in enumerate(code):
            #     print("ind>> ",ind, e)
            # print("code: ",code)
            *other, (ass_node_old, for_node_old, if_node,remove_ass_flag, break_list), for_node_old, total_old_code, new_code, method_code = code
            # print(">>>>ass_node_old: ", ass_node_old)

            '''
            print(">>>>for_node: ", for_node_old)
            print(">>>>remove_ass_flag: ", remove_ass_flag)
            print(">>>>ass_node: ", total_old_code)
            # print(">>>>method_code: ", method_code)
            print(">>>>new_node: ", new_code)
            '''
            # print(">>>>me_code: ", new_loop_me_code)
            # print(">>>>remove_ass_flag: ", remove_ass_flag)
            method_code_list.append([*other, for_node_old, ast.unparse(ass_node_old),total_old_code, new_code, method_code])
            break
        # break
    # return
    for *other, for_node_old, ass_code,total_old_code, new_code, me_code in method_code_list:
        tmp_list = loop_else_code_instr_node.whole_code_pair_get_break_list_for_if(ast.unparse(ast.parse(me_code)))
        print(">>>>>>>>>>tmp_list: ", tmp_list)
        # new_pairs.append((loop_node, if_node, break_parent_list,has_used, ass_in_for_list))

        for loop_node,if_node, break_parent_list,has_used_var_in_if, assign_in_block_of_break in tmp_list:
                loop_str, if_str=ast.unparse(loop_node),ast.unparse(if_node)
                # print(">>>find code: ",ast.unparse(ast.parse(me_code)))
                total_code=["for e in e_list:"]
                # print(">>>len of break_parent_list: ",len(break_parent_list))
                for break_node in break_parent_list:
                    # print("parent of break code: ",ast.unparse(break_node))
                    total_code+=["    "+line for ind, line in enumerate(ast.unparse(break_node).split("\n")) ]
                total_replace_for_code="\n".join(total_code)
                print("has_used_var_in_if: ",has_used_var_in_if)
                # print("total_replace_for_code: ",total_replace_for_code)
                # continue
                # for ass in assign_in_block_of_break:
                #     print(">>>>>>ass code: ",ast.unparse(ass))

                # print(">>>>>>ass code: ", ast.unparse(ass))
                if_str='''
if isRelation:
    if len(set(x_values)) == 1 or len(set(y_values)) == 1:
        continue
    (x_fields, x_attribute) = attributeValues_headers[i]
    (y_fields, y_attribute) = attributeValues_headers[j]
    if len(x_fields) == 1 and len(y_fields) == 1 and (x_fields[0].id == y_fields[0].id):
        continue
    relation_type = self._findRelationType(x_attribute, y_attribute, x_fields, y_fields)
    if relation_type == self.REL_UNKNOWN:
        continue
    if relation_type == self.REL_DATA and len(set(x_fields).intersection(set(y_fields))) > 0:
        continue
    if relation_type == self.REL_SIZE:
        if x_attribute == self.ATTR_VALUE:
            if len(x_fields) > 1:
                continue
        elif y_attribute == self.ATTR_VALUE:
            if len(y_fields) > 1:
                continue
    if relation_type == self.REL_EQUALITY:
        if x_attribute == self.ATTR_VALUE:
            if len(x_fields) > 1:
                continue
        elif y_attribute == self.ATTR_VALUE:
            if len(y_fields) > 1:
                continue
    self._logger.debug("Relation found between '" + str(x_fields) + ':' + x_attribute + "' and '" + str(y_fields) + ':' + y_attribute + "'")
    id_relation = str(uuid.uuid4())
    results.append({'id': id_relation, 'relation_type': relation_type, 'x_fields': x_fields, 'x_attribute': x_attribute, 'y_fields': y_fields, 'y_attribute': y_attribute})'''
                '''
if not is_custom:
    if name == 'bias' and (not (is_norm or is_dcn_module)):
        param_group['lr'] = self.base_lr * bias_lr_mult
    if prefix.find('conv_offset') != -1 and is_dcn_module and isinstance(module, torch.nn.Conv2d):
        param_group['lr'] = self.base_lr * dcn_offset_lr_mult
    if self.base_wd is not None:
        if is_norm:
            param_group['weight_decay'] = self.base_wd * norm_decay_mult
        elif is_dwconv:
            param_group['weight_decay'] = self.base_wd * dwconv_decay_mult
        elif name == 'bias' and (not is_dcn_module):
            param_group['weight_decay'] = self.base_wd * bias_decay_mult               
                '''
                real_instruction = user_instr.replace("{{code}}",if_str )

                # real_instruction=real_instruction+4000*'abc'
                print(">>>>>>>>>>Instr: ", real_instruction)
                # continue
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
                    print("new code: ",new_code)
                    # reponse_list.append([bool_node_str, ass_code,*other, new_code, me_code])
                    return
                    reponse_list.append([loop_str+"\n"+if_str,total_replace_for_code, loop_node,if_node, break_parent_list,has_used_var_in_if, assign_in_block_of_break, ass_code, *other, new_code, me_code])
                    reponse_list[-1].extend([[msg, num_tokes], response])
                except:
                    traceback.print_exc()
                    reponse_list.append([loop_str+"\n"+if_str,total_replace_for_code,loop_node,if_node, break_parent_list,has_used_var_in_if, assign_in_block_of_break, ass_code, *other, new_code, me_code])
                    reponse_list[-1].extend([[msg, num_tokes], traceback.format_exc()])

    return reponse_list
def get_response_abstract_for_block_execute_improve(user_instr, examples, samples, sys_msg="You are a helpful assistant."):
    reponse_list = []
    method_code_list = []
    for ind_sampl, sample_method in enumerate(samples):
        for code in sample_method:
            # repo_name, old_path, file_html, class_name,me_name, old_list, new_tree,\
            #     old_code,new_code, method_code=code
            # break
            # samples_csv = [[repo, file_html, me_name, me_code, ast.unparse(ass_node) + "\n" + ast.unparse(for_node),
            #                 ast.unparse(new_node), str(remove_ass_flag)] for (
            #                repo, file_path, file_html, class_name, me_name, for_node, ass_node, remove_ass_flag,
            #                new_node, me_code) in samples]
            # for ind, e in enumerate(code):
            #     print("ind>> ",ind, e)
            # print("code: ",code)
            *other, (ass_node_old, for_node_old, if_node,remove_ass_flag, break_list), for_node_old, total_old_code, new_code, method_code = code
            # print(">>>>ass_node_old: ", ass_node_old)

            '''
            print(">>>>for_node: ", for_node_old)
            print(">>>>remove_ass_flag: ", remove_ass_flag)
            print(">>>>ass_node: ", total_old_code)
            # print(">>>>method_code: ", method_code)
            print(">>>>new_node: ", new_code)
            '''
            # print(">>>>me_code: ", new_loop_me_code)
            # print(">>>>remove_ass_flag: ", remove_ass_flag)
            method_code_list.append([*other, for_node_old, ast.unparse(ass_node_old),total_old_code, new_code, method_code])
            break
        # break
    # return
    for *other, for_node_old, ass_code,total_old_code, new_code, me_code in method_code_list:
        code=ast.unparse(ast.parse(me_code))
        tmp_list = loop_else_code_instr_node.whole_code_pair_get_break_list_for_if_improve(code)
        print(">>>>>>>>>>tmp_list: ", tmp_list)
        # new_pairs.append((loop_node, if_node, break_parent_list,has_used, ass_in_for_list))

        for loop_node,if_node, break_parent_list,has_used_var_in_if, assign_in_block_of_break in tmp_list:
                loop_str, if_str=ast.unparse(loop_node),ast.unparse(if_node)
                # print(">>>find code: ",ast.unparse(ast.parse(me_code)))
                first_line_list=loop_else_code_instr_node.extract_unindent_lines(ast.unparse(if_node))
                blocks_list=loop_else_code_instr_node.extract_blocks(ast.unparse(if_node))
                if_first=first_line_list[0]+"\n    "+"zj1"


                total_code=["for e in e_list:"]
                # print(">>>len of break_parent_list: ",len(break_parent_list))
                for break_parent_node,assign_node in zip(break_parent_list,assign_in_block_of_break):
                    # print("parent of break code: ",ast.unparse(break_node))
                    if assign_node:
                        total_code.append( loop_else_code_instr_node.indent_code("\n".join([ast.unparse(assign_node), "break"])))
                    else:

                        total_code.append(loop_else_code_instr_node.indent_code(ast.unparse(break_parent_node)))
                total_replace_for_code="\n".join(total_code)
                print("has_used_var_in_if: ",has_used_var_in_if)
                code=total_replace_for_code + "\n" + if_first
#                 code='''
# for e in e_list:
#     check = True
#     break
# if check:
#     zj1'''
                real_instruction = user_instr.replace("{{code}}", code)

                # real_instruction=real_instruction+4000*'abc'
                print(">>>>>>>>>>Instr: ", real_instruction)
                # continue
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
                    # print("new code: ",new_code)
                    # reponse_list.append([bool_node_str, ass_code,*other, new_code, me_code])
                    # return
                    reponse_list.append([loop_str+"\n"+if_str,total_replace_for_code,first_line_list,blocks_list, loop_node,if_node, break_parent_list,has_used_var_in_if, assign_in_block_of_break, ass_code, *other, new_code, me_code])
                    reponse_list[-1].extend([[msg, num_tokes], response])
                except:
                    traceback.print_exc()
                    reponse_list.append([loop_str+"\n"+if_str,total_replace_for_code,first_line_list,blocks_list,loop_node,if_node, break_parent_list,has_used_var_in_if, assign_in_block_of_break, ass_code, *other, new_code, me_code])
                    reponse_list[-1].extend([[msg, num_tokes], traceback.format_exc()])

    return reponse_list
def get_response_abstract_for_block_execute(user_instr, examples, samples, sys_msg="You are a helpful assistant."):
    reponse_list = []
    method_code_list = []
    for ind_sampl, sample_method in enumerate(samples):
        for code in sample_method:
            # repo_name, old_path, file_html, class_name,me_name, old_list, new_tree,\
            #     old_code,new_code, method_code=code
            # break
            # samples_csv = [[repo, file_html, me_name, me_code, ast.unparse(ass_node) + "\n" + ast.unparse(for_node),
            #                 ast.unparse(new_node), str(remove_ass_flag)] for (
            #                repo, file_path, file_html, class_name, me_name, for_node, ass_node, remove_ass_flag,
            #                new_node, me_code) in samples]
            # for ind, e in enumerate(code):
            #     print("ind>> ",ind, e)
            # print("code: ",code)
            *other, (ass_node_old, for_node_old, if_node,remove_ass_flag, break_list), for_node_old, total_old_code, new_code, method_code = code
            # print(">>>>ass_node_old: ", ass_node_old)

            '''
            print(">>>>for_node: ", for_node_old)
            print(">>>>remove_ass_flag: ", remove_ass_flag)
            print(">>>>ass_node: ", total_old_code)
            # print(">>>>method_code: ", method_code)
            print(">>>>new_node: ", new_code)
            '''
            # print(">>>>me_code: ", new_loop_me_code)
            # print(">>>>remove_ass_flag: ", remove_ass_flag)
            method_code_list.append([*other, for_node_old, ast.unparse(ass_node_old),total_old_code, new_code, method_code])
            break
        # break
    # return
    for *other, for_node_old, ass_code,total_old_code, new_code, me_code in method_code_list:
        code=ast.unparse(ast.parse(me_code))
        tmp_list = loop_else_code_instr_node.whole_code_pair_get_break_list_for_if(code)
        print(">>>>>>>>>>tmp_list: ", tmp_list)
        # new_pairs.append((loop_node, if_node, break_parent_list,has_used, ass_in_for_list))

        for loop_node,if_node, break_parent_list,has_used_var_in_if, assign_in_block_of_break in tmp_list:
                loop_str, if_str=ast.unparse(loop_node),ast.unparse(if_node)
                # print(">>>find code: ",ast.unparse(ast.parse(me_code)))
                first_line_list=loop_else_code_instr_node.extract_unindent_lines(ast.unparse(if_node))
                blocks_list=loop_else_code_instr_node.extract_blocks(ast.unparse(if_node))
                if_first=first_line_list[0]+"\n    "+"zj1"


                total_code=["for e in e_list:"]
                # print(">>>len of break_parent_list: ",len(break_parent_list))
                for break_node in break_parent_list:
                    # print("parent of break code: ",ast.unparse(break_node))
                    total_code+=["    "+line for ind, line in enumerate(ast.unparse(break_node).split("\n")) ]
                total_replace_for_code="\n".join(total_code)
                print("has_used_var_in_if: ",has_used_var_in_if)
                code=total_replace_for_code + "\n" + if_first
#                 code='''
# for var1 in var2::
#     if var3:
#         break
# if var3 is None:
#     zj1
#                 '''
                real_instruction = user_instr.replace("{{code}}", code)

                # real_instruction=real_instruction+4000*'abc'
                print(">>>>>>>>>>Instr: ", real_instruction)
                # continue
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
                    # print("new code: ",new_code)
                    # reponse_list.append([bool_node_str, ass_code,*other, new_code, me_code])
                    # return
                    reponse_list.append([loop_str+"\n"+if_str,total_replace_for_code,first_line_list,blocks_list, loop_node,if_node, break_parent_list,has_used_var_in_if, assign_in_block_of_break, ass_code, *other, new_code, me_code])
                    reponse_list[-1].extend([[msg, num_tokes], response])
                except:
                    traceback.print_exc()
                    reponse_list.append([loop_str+"\n"+if_str,total_replace_for_code,first_line_list,blocks_list,loop_node,if_node, break_parent_list,has_used_var_in_if, assign_in_block_of_break, ass_code, *other, new_code, me_code])
                    reponse_list[-1].extend([[msg, num_tokes], traceback.format_exc()])

    return reponse_list
def get_response_which_block_execute(user_instr, examples, samples, sys_msg="You are a helpful assistant."):
    # reponse_list.append(
    #     [loop_str + "\n" + if_str, total_replace_for_code, first_line_list, blocks_list, loop_node, if_node,
    #      break_parent_list, has_used_var_in_if, assign_in_block_of_break, ass_code, *other, new_code, me_code])
        reponse_list=[]
        for total_old_code, total_replace_for_code,first_line_list, blocks_list,loop_node, if_node, \
         break_parent_list, has_used_var_in_if, assign_in_block_of_break, ass_code, *other, new_code, me_code,_,response in samples:
                loop_str, if_str=ast.unparse(loop_node),ast.unparse(if_node)
                content = response["choices"][0]["message"]["content"]

                # print(">>>find code: ",ast.unparse(ast.parse(me_code)))
                abstract_code, symbols_map = parse_abstract_for_code(content)

#                 abstract_code='''for var1 in var2:
#     if var3:
#         var4 = True
#         break
# if var4 is False:
#     zj1
#                 '''
                real_instruction = user_instr.replace("{{code}}", abstract_code)

                # real_instruction=real_instruction+4000*'abc'
                print(">>>>>>>>>>Instr: ", real_instruction)
                # continue
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
                    print("new code: ",new_code)
                    # reponse_list.append([bool_node_str, ass_code,*other, new_code, me_code])
                    # return
                    reponse_list.append([abstract_code, symbols_map,loop_str+"\n"+if_str,total_replace_for_code,first_line_list,blocks_list, loop_node,if_node, break_parent_list,has_used_var_in_if, assign_in_block_of_break, ass_code, *other, new_code, me_code])
                    reponse_list[-1].extend([[msg, num_tokes], response])
                except:
                    traceback.print_exc()
                    reponse_list.append([abstract_code, symbols_map,loop_str+"\n"+if_str,total_replace_for_code,first_line_list,blocks_list,loop_node,if_node, break_parent_list,has_used_var_in_if, assign_in_block_of_break, ass_code, *other, new_code, me_code])
                    reponse_list[-1].extend([[msg, num_tokes], traceback.format_exc()])

        return reponse_list
def get_response_instr_abstract_for_and_if_block(user_instr, examples, samples, sys_msg="You are a helpful assistant."):
    reponse_list = []
    method_code_list = []
    for ind_sampl, sample_method in enumerate(samples):
        for code in sample_method:
            # repo_name, old_path, file_html, class_name,me_name, old_list, new_tree,\
            #     old_code,new_code, method_code=code
            # break
            # samples_csv = [[repo, file_html, me_name, me_code, ast.unparse(ass_node) + "\n" + ast.unparse(for_node),
            #                 ast.unparse(new_node), str(remove_ass_flag)] for (
            #                repo, file_path, file_html, class_name, me_name, for_node, ass_node, remove_ass_flag,
            #                new_node, me_code) in samples]
            # for ind, e in enumerate(code):
            #     print("ind>> ",ind, e)
            # print("code: ",code)
            *other, (ass_node_old, for_node_old, if_node,remove_ass_flag, break_list), for_node_old, total_old_code, new_code, method_code = code
            # print(">>>>ass_node_old: ", ass_node_old)

            '''
            print(">>>>for_node: ", for_node_old)
            print(">>>>remove_ass_flag: ", remove_ass_flag)
            print(">>>>ass_node: ", total_old_code)
            # print(">>>>method_code: ", method_code)
            print(">>>>new_node: ", new_code)
            '''
            # print(">>>>me_code: ", new_loop_me_code)
            # print(">>>>remove_ass_flag: ", remove_ass_flag)
            method_code_list.append([*other, for_node_old, ast.unparse(ass_node_old),total_old_code, new_code, method_code])
            break
        # break
    # return
    for *other, for_node_old, ass_code,total_old_code, new_code, me_code in method_code_list:
        tmp_list = loop_else_code_instr_node.whole_code_pair_get_break_list_for_if(ast.unparse(ast.parse(me_code)))
        print(">>>>>>>>>>tmp_list: ", tmp_list)
        # new_pairs.append((loop_node, if_node, break_parent_list,has_used, ass_in_for_list))

        for loop_node,if_node, break_parent_list,has_used_var_in_if, assign_in_block_of_break in tmp_list:
                loop_str, if_str=ast.unparse(loop_node),ast.unparse(if_node)
                # print(">>>find code: ",loop_str,if_str)
                total_code=["for e in e_list:"]
                print(">>>len of break_parent_list: ",len(break_parent_list))
                for break_node in break_parent_list:
                    # print("parent of break code: ",ast.unparse(break_node))
                    total_code+=["    "+line for ind, line in enumerate(ast.unparse(break_node).split("\n")) ]
                total_replace_for_code="\n".join(total_code)+"\n"+if_str
                print("total_replace_for_code: ",total_replace_for_code)

                # continue
                # for ass in assign_in_block_of_break:
                #     print(">>>>>>ass code: ",ast.unparse(ass))


                real_instruction = user_instr.replace("{{code}}",total_replace_for_code )

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
                    # print("new code: ",new_code)
                    # reponse_list.append([bool_node_str, ass_code,*other, new_code, me_code])

                    reponse_list.append([loop_str+"\n"+if_str,total_replace_for_code, loop_str, if_str, has_used_var_in_if, assign_in_block_of_break, ass_code, *other, new_code, me_code])
                    reponse_list[-1].extend([[msg, num_tokes], response])
                except:
                    traceback.print_exc()
                    reponse_list.append([loop_str+"\n"+if_str,total_replace_for_code,loop_str, if_str, has_used_var_in_if, assign_in_block_of_break, ass_code, *other, new_code, me_code])
                    reponse_list[-1].extend([[msg, num_tokes], traceback.format_exc()])

    return reponse_list
def get_response_instr_while(user_instr, examples, samples, sys_msg="You are a helpful assistant."):
    reponse_list = []
    method_code_list = []
    for ind_sampl, sample_method in enumerate(samples):
        for code in sample_method:
            # repo_name, old_path, file_html, class_name,me_name, old_list, new_tree,\
            #     old_code,new_code, method_code=code
            # break
            # samples_csv = [[repo, file_html, me_name, me_code, ast.unparse(ass_node) + "\n" + ast.unparse(for_node),
            #                 ast.unparse(new_node), str(remove_ass_flag)] for (
            #                repo, file_path, file_html, class_name, me_name, for_node, ass_node, remove_ass_flag,
            #                new_node, me_code) in samples]
            # for ind, e in enumerate(code):
            #     print("ind>> ",ind, e)
            # print("code: ",code)
            *other, (ass_node_old, for_node_old, if_node,remove_ass_flag, break_list), for_node_old, total_old_code, new_code, method_code = code
            # print(">>>>ass_node_old: ", ass_node_old)

            '''
            print(">>>>for_node: ", for_node_old)
            print(">>>>remove_ass_flag: ", remove_ass_flag)
            print(">>>>ass_node: ", total_old_code)
            # print(">>>>method_code: ", method_code)
            print(">>>>new_node: ", new_code)
            '''
            # print(">>>>me_code: ", new_loop_me_code)
            # print(">>>>remove_ass_flag: ", remove_ass_flag)
            method_code_list.append([*other, for_node_old, ast.unparse(ass_node_old),total_old_code, new_code, method_code])
            break
        # break
    # return
    for *other, for_node_old, ass_code,total_old_code, new_code, me_code in method_code_list:
        tmp_list = loop_else_code_instr.whole_code_pair_while_if(ast.unparse(ast.parse(me_code)))
        print(">>>>>>>>>>tmp_list: ", tmp_list)

        for bool_node in tmp_list:
                bool_node_str="\n".join(bool_node)
                real_instruction = user_instr.replace("{{code}}",bool_node_str )

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
                    print("new code: ",new_code)
                    reponse_list.append([bool_node_str, ass_code,*other, new_code, me_code])
                    reponse_list[-1].extend([[msg, num_tokes], response])
                except:
                    traceback.print_exc()
                    reponse_list.append([bool_node_str,ass_code, *other, new_code, me_code])
                    reponse_list[-1].extend([[msg, num_tokes], traceback.format_exc()])
            # break
    # '''
    return reponse_list
def parse_abstract_for_code(content):
    content_list = content.split("New Python code:")
    if len(content_list) == 1:
        content_list = content.split("New Python Code:")

    symbols_list = content_list[0].strip().split("\n")
    symbols_map = dict()
    pre_value_list = []
    key = ""
    for i in symbols_list:
        if i.startswith("symbol"):
            continue
        if i.startswith("var"):
            if pre_value_list:
                symbols_map[key] = "\n".join(pre_value_list)
            pre_value_list = []
            key = i.split(":")[0]
            pre_value_list.append(":".join(i.split(":")[1:]))
            symbols_map[key] = pre_value_list
        else:
            pre_value_list.append(i)
    if key:
        symbols_map[key] = "\n".join(pre_value_list)

    content = content_list[-1]
    return content.strip(), symbols_map

def parse_abstract_code(content):
    content_list = content.split("New Python code:")
    if len(content_list) == 1:
        content_list = content.split("New Python Code:")

    symbols_list = content_list[0].strip().split("\n")
    symbols_map = dict()
    pre_value_list=[]
    key=""
    len_prefix=0
    for i in symbols_list:
        if i.startswith("symbol"):
            continue
        if i.startswith("zj"):
            if pre_value_list:
                symbols_map[key] = "\n".join(pre_value_list)
            pre_value_list=[]
            key = i.split(":")[0]
            pre_value_list.append(":".join(i.split(":")[1:]))
            symbols_map[key] = pre_value_list
        else:
            if not pre_value_list:
                prefix_len=[]
                for e in i:
                    if e:
                        break
                    prefix_len.append(e)
                len_prefix=len(prefix_len)

            pre_value_list.append(i[len_prefix:])
    if key:
        symbols_map[key] = "\n".join(pre_value_list)




    content = content_list[-1]

    return content.strip(), symbols_map
def get_response_instr_from_abstract(user_instr, examples, samples, sys_msg="You are a helpful assistant."):
    reponse_list = []
    # reponse_list.append([abstract_me_code, value, abstract_value, *other, new_code, method_code])
    # for ind, e in enumerate(samples[0]):
    #     print(">>>other: ", ind, e)
    for me_code_list, abstract_if_code, whole_ass_code, *other, new_code, method_code, _, response in samples:

        content = response["choices"][0]["message"]["content"]
        abstract_code, symbols_map = parse_abstract_code(content)
        print("abstract_code: ",abstract_code)
        abstract_code=me_code_list[0]+"\n"+abstract_code
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
            reponse_list.append([abstract_code, symbols_map, "\n".join(me_code_list), *other, new_code, method_code])
            reponse_list[-1].extend([[msg, num_tokes], response])
        except:
            traceback.print_exc()
            reponse_list.append([abstract_code, symbols_map, "\n".join(me_code_list), *other, new_code, method_code])
            reponse_list[-1].extend([[msg, num_tokes], traceback.format_exc()])
    return reponse_list

def get_response_instr_from_abstract_loop(user_instr, examples, samples, sys_msg="You are a helpful assistant."):
    reponse_list = []
    # reponse_list.append([abstract_me_code, value, abstract_value, *other, new_code, method_code])
    # for ind, e in enumerate(samples[0]):
    #     print(">>>other: ", ind, e)
    # reponse_list.append(
    #     [loop_str + "\n" + if_str, loop_str, if_str, has_used_var_in_if, assign_in_block_of_break, ass_code, *other,
    #      new_code, me_code])

    for total_old_code, loop_str, if_str, has_used_var_in_if, assign_in_block_of_break, ass_code, *other, new_code, method_code, _, response in samples:

        content = response["choices"][0]["message"]["content"]
        abstract_if_code, symbols_map = parse_abstract_code(content)

        # print("abstract_code: ",abstract_if_code)
        # abstract_code=loop_str+"\n"+abstract_code
        real_instruction = user_instr.replace("{{code}}", loop_str)

        msg = chatgpt_util.format_message_2(real_instruction, examples=examples, sys_msg=sys_msg)
        print(">>>>>>>>>>real_instruction: ", real_instruction)
        num_tokes = chatgpt_util.num_tokens_from_messages(msg)
        # print("len of msg: ",chatgpt_util.num_tokens_from_messages(msg))
        # if chatgpt_util.num_tokens_from_messages(msg)>=chatgpt_util.MAX_TOKENS:
        #     response
        try:
            response = chatgpt_util.chatGPT_result(msg)
            print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
            reponse_list.append([abstract_if_code, symbols_map, total_old_code, loop_str, if_str, has_used_var_in_if, assign_in_block_of_break, ass_code, *other, new_code, method_code])
            # reponse_list.append([abstract_code, symbols_map, "\n".join(me_code_list), *other, new_code, method_code])
            reponse_list[-1].extend([[msg, num_tokes], response])
        except:
            traceback.print_exc()
            reponse_list.append([abstract_if_code, symbols_map, total_old_code, loop_str, if_str, has_used_var_in_if, assign_in_block_of_break, ass_code, *other, new_code, method_code])
            reponse_list[-1].extend([[msg, num_tokes], traceback.format_exc()])
    return reponse_list

def get_response_instr_from_abstract_add_whether_remove_ass(user_instr, examples, samples, sys_msg="You are a helpful assistant."):
    reponse_list = []
    # reponse_list.append([abstract_me_code, value, abstract_value, *other, new_code, method_code])
    # for ind, e in enumerate(samples[0]):
    #     print(">>>other: ", ind, e)
    # reponse_list.append(
    #     [loop_str + "\n" + if_str, loop_str, if_str, has_used_var_in_if, assign_in_block_of_break, ass_code, *other,
    #      new_code, me_code])

    for total_old_code, loop_str, if_str, has_used_var_in_if, assign_in_block_of_break, ass_code, *other, new_code, method_code, _, response in samples:

        content = response["choices"][0]["message"]["content"]
        abstract_code, symbols_map = parse_abstract_code(content)

        note_if_remove_ass=f"Note: Keep {assign_in_block_of_break}" if assign_in_block_of_break else ''
        print("abstract_code: ",abstract_code)
        abstract_code=loop_str+"\n"+abstract_code
        real_instruction = user_instr.replace("{{code}}", abstract_code)
        real_instruction = real_instruction.replace("{{note_if_remove_ass}}", note_if_remove_ass)
        real_instruction = real_instruction.replace(f"zj", "zj=zj+")

        msg = chatgpt_util.format_message_2(real_instruction, examples=examples, sys_msg=sys_msg)
        print(">>>>>>>>>>real_instruction: ", real_instruction)
        num_tokes = chatgpt_util.num_tokens_from_messages(msg)
        # print("len of msg: ",chatgpt_util.num_tokens_from_messages(msg))
        # if chatgpt_util.num_tokens_from_messages(msg)>=chatgpt_util.MAX_TOKENS:
        #     response
        try:
            response = chatgpt_util.chatGPT_result(msg)
            print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
            reponse_list.append([abstract_code, symbols_map, total_old_code, loop_str, if_str, has_used_var_in_if, assign_in_block_of_break, ass_code, *other, new_code, method_code])
            # reponse_list.append([abstract_code, symbols_map, "\n".join(me_code_list), *other, new_code, method_code])
            reponse_list[-1].extend([[msg, num_tokes], response])
        except:
            traceback.print_exc()
            reponse_list.append([abstract_code, symbols_map, total_old_code, loop_str, if_str, has_used_var_in_if, assign_in_block_of_break, ass_code, *other, new_code, method_code])
            reponse_list[-1].extend([[msg, num_tokes], traceback.format_exc()])
    return reponse_list
def get_response_instr_from_abstract_total_code_change(user_instr, examples, samples, sys_msg="You are a helpful assistant."):
    reponse_list = []
    # reponse_list.append([abstract_me_code, value, abstract_value, *other, new_code, method_code])
    # for ind, e in enumerate(samples[0]):
    #     print(">>>other: ", ind, e)
    # reponse_list.append(
    #     [loop_str + "\n" + if_str, loop_str, if_str, has_used_var_in_if, assign_in_block_of_break, ass_code, *other,
    #      new_code, me_code])
    # reponse_list.append(
    #     [loop_str + "\n" + if_str, total_replace_for_code, loop_str, if_str, break_parent_list, has_used_var_in_if,
    #      assign_in_block_of_break, ass_code, *other, new_code, me_code])

    # reponse_list.append([loop_str + "\n" + if_str, total_replace_for_code, loop_str, if_str, has_used_var_in_if,
    #                      assign_in_block_of_break, ass_code, *other, new_code, me_code])
    for total_old_code, total_replace_for_code,loop_node,if_node,break_parent_list,  has_used_var_in_if, assign_in_block_of_break, ass_code, *other, new_code, method_code, _, response in samples:

        content = response["choices"][0]["message"]["content"]
        abstract_code, symbols_map = parse_abstract_code(content)
        print("symbols_map: ",symbols_map)
        # for sym in symbols_map:
        #     print("sym: ",sym)
        #     print(symbols_map[sym])
        # continue
        # symbol_name_if_map = dict()
        #
        # def get_name_nodes(tree):
        #     name_nodes = []
        #     for node in ast.walk(tree):
        #         if isinstance(node, ast.Name):
        #             name_nodes.append(node)
        #     return name_nodes
        # var_in_if_list = []
        # for e in ast.walk(ast.parse(if_str)):
        #     if isinstance(e, ast.If):
        #         var_in_if_list = [ast.unparse(e) for e in list(set(get_name_nodes(e.test)))]
        #         for ind, var in enumerate(var_in_if_list):
        #             symbol = 'flag_' + str(ind)
        #             loop_str = loop_str.replace(var, symbol)
        #             if_str = if_str.replace(var, symbol)
        #             symbol_name_if_map[symbol] = var
        #         break
        # assigned_var=",".join(var_in_if_list) if has_used_var_in_if else 'zj'
        # note_if_remove_ass=f"Note: Keep {assign_in_block_of_break}" if assign_in_block_of_break else ''
        abstract_code=total_replace_for_code+"\n"+abstract_code
        print("abstract_code: ",abstract_code)

        real_instruction = user_instr.replace("{{code}}", abstract_code)
        # real_instruction = real_instruction.replace("{{note_if_remove_ass}}", note_if_remove_ass)
        # real_instruction = real_instruction.replace(f"zj", f"zj={assigned_var},")

        msg = chatgpt_util.format_message_2(real_instruction, examples=examples, sys_msg=sys_msg)
        print(">>>>>>>>>>real_instruction: ", real_instruction)
        # continue
        num_tokes = chatgpt_util.num_tokens_from_messages(msg)
        # print("len of msg: ",chatgpt_util.num_tokens_from_messages(msg))
        # if chatgpt_util.num_tokens_from_messages(msg)>=chatgpt_util.MAX_TOKENS:
        #     response
        try:
            response = chatgpt_util.chatGPT_result(msg)
            print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
            reponse_list.append([abstract_code, symbols_map, total_old_code, loop_node,if_node,break_parent_list, has_used_var_in_if, assign_in_block_of_break, ass_code, *other, new_code, method_code])
            # reponse_list.append([abstract_code, symbols_map, "\n".join(me_code_list), *other, new_code, method_code])
            reponse_list[-1].extend([[msg, num_tokes], response])
        except:
            traceback.print_exc()
            reponse_list.append([abstract_code, symbols_map, total_old_code, loop_node,if_node,break_parent_list, has_used_var_in_if, assign_in_block_of_break, ass_code, *other, new_code, method_code])
            reponse_list[-1].extend([[msg, num_tokes], traceback.format_exc()])
    return reponse_list
def get_response_instr_refactor_from_abstract_for_and_if(user_instr, examples, samples, sys_msg="You are a helpful assistant."):
    reponse_list = []
    # reponse_list.append([abstract_me_code, value, abstract_value, *other, new_code, method_code])
    # for ind, e in enumerate(samples[0]):
    #     print(">>>other: ", ind, e)
    # reponse_list.append(
    #     [loop_str + "\n" + if_str, loop_str, if_str, has_used_var_in_if, assign_in_block_of_break, ass_code, *other,
    #      new_code, me_code])
    # reponse_list.append([loop_str + "\n" + if_str, total_replace_for_code, loop_str, if_str, has_used_var_in_if,
    #                      assign_in_block_of_break, ass_code, *other, new_code, me_code])


    for abstract_if_code,symbols_map_if,total_old_code, loop_str,if_str, has_used_var_in_if, assign_in_block_of_break, ass_code, *other, new_code, method_code, _, response in samples:

        content = response["choices"][0]["message"]["content"]
        abstract_code, symbols_map = parse_abstract_for_code(content)
        # symbol_name_if_map = dict()
        #
        # def get_name_nodes(tree):
        #     name_nodes = []
        #     for node in ast.walk(tree):
        #         if isinstance(node, ast.Name):
        #             name_nodes.append(node)
        #     return name_nodes
        # var_in_if_list = []
        # for e in ast.walk(ast.parse(if_str)):
        #     if isinstance(e, ast.If):
        #         var_in_if_list = [ast.unparse(e) for e in list(set(get_name_nodes(e.test)))]
        #         for ind, var in enumerate(var_in_if_list):
        #             symbol = 'flag_' + str(ind)
        #             loop_str = loop_str.replace(var, symbol)
        #             if_str = if_str.replace(var, symbol)
        #             symbol_name_if_map[symbol] = var
        #         break
        # assigned_var=",".join(var_in_if_list) if has_used_var_in_if else 'zj'
        # note_if_remove_ass=f"Note: Keep {assign_in_block_of_break}" if assign_in_block_of_break else ''
        # abstract_code=total_replace_for_code+"\n"+abstract_code
        abstract_code='''
for var1 in var2:
    if var3:
        var4
        var5 = True
        break
if var6 is False:
    zj1        
        '''
        '''
for var1 in var2:
    if var3:
        var4 = True
        break
if not var4:
    zj1      
        '''


        '''
for var1 in var2:
        if var5:
            break
if var6:
    zj1
else:
    zj2        
        '''
        '''
for var1 in var2:
        if var5:
            break
if var5 == False:
    zj1
else:
    zj2        
        '''
        '''
for var1 in var2:
        var5 = path
        break
if not var5:
    zj1
else:
    zj2        
        '''
        print("abstract_code: ",abstract_code)

        real_instruction = user_instr.replace("{{code}}", abstract_code)
        # real_instruction = real_instruction.replace("{{note_if_remove_ass}}", note_if_remove_ass)
        # real_instruction = real_instruction.replace(f"zj", f"zj={assigned_var},")

        msg = chatgpt_util.format_message_2(real_instruction, examples=examples, sys_msg=sys_msg)
        print(">>>>>>>>>>real_instruction: ", real_instruction)
        num_tokes = chatgpt_util.num_tokens_from_messages(msg)
        # print("len of msg: ",chatgpt_util.num_tokens_from_messages(msg))
        # if chatgpt_util.num_tokens_from_messages(msg)>=chatgpt_util.MAX_TOKENS:
        #     response
        try:
            response = chatgpt_util.chatGPT_result(msg)
            print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
            reponse_list.append([abstract_code, symbols_map, abstract_if_code,symbols_map_if,total_old_code, loop_str, if_str, has_used_var_in_if, assign_in_block_of_break, ass_code, *other, new_code, method_code])
            # reponse_list.append([abstract_code, symbols_map, "\n".join(me_code_list), *other, new_code, method_code])
            reponse_list[-1].extend([[msg, num_tokes], response])
            return
        except:
            traceback.print_exc()
            reponse_list.append([abstract_code, symbols_map, abstract_if_code,symbols_map_if,total_old_code, loop_str, if_str, has_used_var_in_if, assign_in_block_of_break, ass_code, *other, new_code, method_code])
            reponse_list[-1].extend([[msg, num_tokes], traceback.format_exc()])
        break
    return reponse_list

# def get_response_instr_refactor_from_abstract_for_and_if_which_block_executed(user_instr, examples, samples, sys_msg="You are a helpful assistant."):
def get_response_instr_refactor_from_abstract_for_and_if_which_block_executed(user_instr, examples, samples,
                                                         sys_msg="You are a helpful assistant."):
    reponse_list = []
    # reponse_list.append([abstract_me_code, value, abstract_value, *other, new_code, method_code])
    # for ind, e in enumerate(samples[0]):
    #     print(">>>other: ", ind, e)
    # reponse_list.append(
    #     [loop_str + "\n" + if_str, loop_str, if_str, has_used_var_in_if, assign_in_block_of_break, ass_code, *other,
    #      new_code, me_code])
    # reponse_list.append([loop_str + "\n" + if_str, total_replace_for_code, loop_str, if_str, has_used_var_in_if,
    #                      assign_in_block_of_break, ass_code, *other, new_code, me_code])

    for abstract_if_code, symbols_map_if, total_old_code, loop_str, if_str, has_used_var_in_if, assign_in_block_of_break, ass_code, *other, new_code, method_code, _, response in samples:

        content = response["choices"][0]["message"]["content"]
        abstract_code, symbols_map = parse_abstract_for_code(content)
        # symbol_name_if_map = dict()
        #
        # def get_name_nodes(tree):
        #     name_nodes = []
        #     for node in ast.walk(tree):
        #         if isinstance(node, ast.Name):
        #             name_nodes.append(node)
        #     return name_nodes
        # var_in_if_list = []
        # for e in ast.walk(ast.parse(if_str)):
        #     if isinstance(e, ast.If):
        #         var_in_if_list = [ast.unparse(e) for e in list(set(get_name_nodes(e.test)))]
        #         for ind, var in enumerate(var_in_if_list):
        #             symbol = 'flag_' + str(ind)
        #             loop_str = loop_str.replace(var, symbol)
        #             if_str = if_str.replace(var, symbol)
        #             symbol_name_if_map[symbol] = var
        #         break
        # assigned_var=",".join(var_in_if_list) if has_used_var_in_if else 'zj'
        # note_if_remove_ass=f"Note: Keep {assign_in_block_of_break}" if assign_in_block_of_break else ''
        # abstract_code=total_replace_for_code+"\n"+abstract_code
#         abstract_code = '''
# for var1 in var2:
#     if var3:
#         var4 = True
#         break
# if not var4:
#     zj1
#         '''
#         '''
# for var1 in var2:
#     if var3:
#         var4
#         var5 = True
#         break
# if var5 is False:
#     var6
# else:
#     var7
#         '''
#
#         '''
# for var1 in var2:
#         if var5:
#             break
# if var6:
#     zj1
# else:
#     zj2
#         '''
#         '''
# for var1 in var2:
#         if var5:
#             break
# if var5 == False:
#     zj1
# else:
#     zj2
#         '''
#         '''
# for var1 in var2:
#         var5 = path
#         break
# if not var5:
#     zj1
# else:
#     zj2
#         '''
        # print("abstract_code: ", abstract_code)
        abstract_code_list=abstract_code.split("\n")
        for_code=[]
        if_code=[]
        for line in abstract_code_list:
            if line.startswith("if"):
                if_code.append(line)
            else:
                if if_code:
                    if_code.append(line)
                else:
                    for_code.append(line)

        abstract_if_code="\n".join(if_code)
        abstract_for_code="\n".join(for_code)

        print("abstract_for_code: ", abstract_for_code)
        print("abstract_if_code: ", abstract_if_code)


        real_instruction = user_instr.replace("{{for_code}}", abstract_for_code)
        real_instruction = real_instruction.replace("{{if_code}}", abstract_if_code)

        # real_instruction = real_instruction.replace("{{note_if_remove_ass}}", note_if_remove_ass)
        # real_instruction = real_instruction.replace(f"zj", f"zj={assigned_var},")

        msg = chatgpt_util.format_message_2(real_instruction, examples=examples, sys_msg=sys_msg)
        print(">>>>>>>>>>real_instruction: ", real_instruction)
        num_tokes = chatgpt_util.num_tokens_from_messages(msg)
        # print("len of msg: ",chatgpt_util.num_tokens_from_messages(msg))
        # if chatgpt_util.num_tokens_from_messages(msg)>=chatgpt_util.MAX_TOKENS:
        #     response
        try:
            response = chatgpt_util.chatGPT_result(msg)
            print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
            reponse_list.append(
                [abstract_code, symbols_map, abstract_if_code, symbols_map_if, total_old_code, loop_str, if_str,
                 has_used_var_in_if, assign_in_block_of_break, ass_code, *other, new_code, method_code])
            # reponse_list.append([abstract_code, symbols_map, "\n".join(me_code_list), *other, new_code, method_code])
            reponse_list[-1].extend([[msg, num_tokes], response])
        except:
            traceback.print_exc()
            reponse_list.append(
                [abstract_code, symbols_map, abstract_if_code, symbols_map_if, total_old_code, loop_str, if_str,
                 has_used_var_in_if, assign_in_block_of_break, ass_code, *other, new_code, method_code])
            reponse_list[-1].extend([[msg, num_tokes], traceback.format_exc()])
        # break
    return reponse_list
def get_response_instr_refactor_from_abstract_for_and_if_which_block_executed_2(user_instr, examples, samples,
                                                         sys_msg="You are a helpful assistant."):
    reponse_list = []
    # reponse_list.append([abstract_me_code, value, abstract_value, *other, new_code, method_code])
    # for ind, e in enumerate(samples[0]):
    #     print(">>>other: ", ind, e)
    # reponse_list.append(
    #     [loop_str + "\n" + if_str, loop_str, if_str, has_used_var_in_if, assign_in_block_of_break, ass_code, *other,
    #      new_code, me_code])
    # reponse_list.append([loop_str + "\n" + if_str, total_replace_for_code, loop_str, if_str, has_used_var_in_if,
    #                      assign_in_block_of_break, ass_code, *other, new_code, me_code])
    # reponse_list.append(
    #     [abstract_code, symbols_map, total_old_code, loop_str, if_str, break_parent_list, has_used_var_in_if,
    #      assign_in_block_of_break, ass_code, *other, new_code, method_code])

    for abstract_if_code, symbols_map_if, total_old_code, loop_node, if_node,break_parent_list, has_used_var_in_if, assign_in_block_of_break, ass_code, *other, new_code, method_code, _, response in samples:

        content = response["choices"][0]["message"]["content"]
        abstract_code, symbols_map = parse_abstract_for_code(content)
        # for key in symbols_map:
        #     print("key: ",key)
        #     print(symbols_map[key])
        # print("symbols_map")
        # continue
        abstract_code='''
for var1 in var2:
    if var3:
        var4
        var5 = True
        break
if var6 is False:
    zj1
'''
        real_instruction = user_instr.replace("{{code}}", abstract_code)
        # real_instruction = real_instruction.replace("{{if_code}}", abstract_if_code)

        # real_instruction = real_instruction.replace("{{note_if_remove_ass}}", note_if_remove_ass)
        # real_instruction = real_instruction.replace(f"zj", f"zj={assigned_var},")

        msg = chatgpt_util.format_message_2(real_instruction, examples=examples, sys_msg=sys_msg)
        print(">>>>>>>>>>real_instruction: ", real_instruction)
        num_tokes = chatgpt_util.num_tokens_from_messages(msg)
        # print("len of msg: ",chatgpt_util.num_tokens_from_messages(msg))
        # if chatgpt_util.num_tokens_from_messages(msg)>=chatgpt_util.MAX_TOKENS:
        #     response
        try:
            response = chatgpt_util.chatGPT_result(msg)
            print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
            time.sleep(10)
            return
            reponse_list.append(
                [abstract_code, symbols_map, abstract_if_code, symbols_map_if, total_old_code, loop_node, if_node,break_parent_list,
                 has_used_var_in_if, assign_in_block_of_break, ass_code, *other, new_code, method_code])
            # reponse_list.append([abstract_code, symbols_map, "\n".join(me_code_list), *other, new_code, method_code])
            reponse_list[-1].extend([[msg, num_tokes], response])
        except:
            traceback.print_exc()
            reponse_list.append(
                [abstract_code, symbols_map, abstract_if_code, symbols_map_if, total_old_code, loop_node, if_node,break_parent_list,
                 has_used_var_in_if, assign_in_block_of_break, ass_code, *other, new_code, method_code])
            reponse_list[-1].extend([[msg, num_tokes], traceback.format_exc()])
        # break
    return reponse_list
def get_response_instr_from_abstract_add_whether_remove_ass(user_instr, examples, samples, sys_msg="You are a helpful assistant."):
    reponse_list = []
    # reponse_list.append([abstract_me_code, value, abstract_value, *other, new_code, method_code])
    # for ind, e in enumerate(samples[0]):
    #     print(">>>other: ", ind, e)
    # reponse_list.append(
    #     [loop_str + "\n" + if_str, loop_str, if_str, has_used_var_in_if, assign_in_block_of_break, ass_code, *other,
    #      new_code, me_code])

    for total_old_code, loop_str, if_str, has_used_var_in_if, assign_in_block_of_break, ass_code, *other, new_code, method_code, _, response in samples:

        content = response["choices"][0]["message"]["content"]
        abstract_code, symbols_map = parse_abstract_code(content)
        symbol_name_if_map = dict()

        def get_name_nodes(tree):
            name_nodes = []
            for node in ast.walk(tree):
                if isinstance(node, ast.Name):
                    name_nodes.append(node)
            return name_nodes
        var_in_if_list = []
        for e in ast.walk(ast.parse(if_str)):
            if isinstance(e, ast.If):
                var_in_if_list = [ast.unparse(e) for e in list(set(get_name_nodes(e.test)))]
                for ind, var in enumerate(var_in_if_list):
                    symbol = 'flag_' + str(ind)
                    loop_str = loop_str.replace(var, symbol)
                    if_str = if_str.replace(var, symbol)
                    symbol_name_if_map[symbol] = var
                break
        assigned_var=",".join(var_in_if_list) if has_used_var_in_if else 'zj'
        note_if_remove_ass=f"Note: Keep {assign_in_block_of_break}" if assign_in_block_of_break else ''
        print("abstract_code: ",abstract_code)
        abstract_code=loop_str+"\n"+abstract_code
        real_instruction = user_instr.replace("{{code}}", abstract_code)
        # real_instruction = real_instruction.replace("{{note_if_remove_ass}}", note_if_remove_ass)
        real_instruction = real_instruction.replace(f"zj", f"zj={assigned_var},")

        msg = chatgpt_util.format_message_2(real_instruction, examples=examples, sys_msg=sys_msg)
        print(">>>>>>>>>>real_instruction: ", real_instruction)
        num_tokes = chatgpt_util.num_tokens_from_messages(msg)
        # print("len of msg: ",chatgpt_util.num_tokens_from_messages(msg))
        # if chatgpt_util.num_tokens_from_messages(msg)>=chatgpt_util.MAX_TOKENS:
        #     response
        try:
            response = chatgpt_util.chatGPT_result(msg)
            print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
            reponse_list.append([abstract_code, symbols_map, total_old_code, loop_str, if_str, has_used_var_in_if, assign_in_block_of_break, ass_code, *other, new_code, method_code])
            # reponse_list.append([abstract_code, symbols_map, "\n".join(me_code_list), *other, new_code, method_code])
            reponse_list[-1].extend([[msg, num_tokes], response])
        except:
            traceback.print_exc()
            reponse_list.append([abstract_code, symbols_map, total_old_code, loop_str, if_str, has_used_var_in_if, assign_in_block_of_break, ass_code, *other, new_code, method_code])
            reponse_list[-1].extend([[msg, num_tokes], traceback.format_exc()])
    return reponse_list

def get_response_instr_from_abstract_add_whether_remove_ass(user_instr, examples, samples, sys_msg="You are a helpful assistant."):
    reponse_list = []
    # reponse_list.append([abstract_me_code, value, abstract_value, *other, new_code, method_code])
    # for ind, e in enumerate(samples[0]):
    #     print(">>>other: ", ind, e)
    # reponse_list.append(
    #     [loop_str + "\n" + if_str, loop_str, if_str, has_used_var_in_if, assign_in_block_of_break, ass_code, *other,
    #      new_code, me_code])

    for total_old_code, loop_str, if_str, has_used_var_in_if, assign_in_block_of_break, ass_code, *other, new_code, method_code, _, response in samples:

        content = response["choices"][0]["message"]["content"]
        abstract_code, symbols_map = parse_abstract_code(content)
        symbol_name_if_map = dict()

        def get_name_nodes(tree):
            name_nodes = []
            for node in ast.walk(tree):
                if isinstance(node, ast.Name):
                    name_nodes.append(node)
            return name_nodes
        var_in_if_list = []
        for e in ast.walk(ast.parse(if_str)):
            if isinstance(e, ast.If):
                var_in_if_list = [ast.unparse(e) for e in list(set(get_name_nodes(e.test)))]
                for ind, var in enumerate(var_in_if_list):
                    symbol = 'flag_' + str(ind)
                    loop_str = loop_str.replace(var, symbol)
                    if_str = if_str.replace(var, symbol)
                    symbol_name_if_map[symbol] = var
                break
        assigned_var=",".join(var_in_if_list) if has_used_var_in_if else 'zj'
        note_if_remove_ass=f"Note: Keep {assign_in_block_of_break}" if assign_in_block_of_break else ''
        print("abstract_code: ",abstract_code)
        abstract_code=loop_str+"\n"+abstract_code
        real_instruction = user_instr.replace("{{code}}", abstract_code)
        # real_instruction = real_instruction.replace("{{note_if_remove_ass}}", note_if_remove_ass)
        real_instruction = real_instruction.replace(f"zj", f"zj={assigned_var},")

        msg = chatgpt_util.format_message_2(real_instruction, examples=examples, sys_msg=sys_msg)
        print(">>>>>>>>>>real_instruction: ", real_instruction)
        num_tokes = chatgpt_util.num_tokens_from_messages(msg)
        # print("len of msg: ",chatgpt_util.num_tokens_from_messages(msg))
        # if chatgpt_util.num_tokens_from_messages(msg)>=chatgpt_util.MAX_TOKENS:
        #     response
        try:
            response = chatgpt_util.chatGPT_result(msg)
            print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
            reponse_list.append([abstract_code, symbols_map, total_old_code, loop_str, if_str, has_used_var_in_if, assign_in_block_of_break, ass_code, *other, new_code, method_code])
            # reponse_list.append([abstract_code, symbols_map, "\n".join(me_code_list), *other, new_code, method_code])
            reponse_list[-1].extend([[msg, num_tokes], response])
        except:
            traceback.print_exc()
            reponse_list.append([abstract_code, symbols_map, total_old_code, loop_str, if_str, has_used_var_in_if, assign_in_block_of_break, ass_code, *other, new_code, method_code])
            reponse_list[-1].extend([[msg, num_tokes], traceback.format_exc()])
    return reponse_list

def get_response_instr_for_ass_node_from_abstract(user_instr, examples, samples, sys_msg="You are a helpful assistant."):
    reponse_list = []
    # reponse_list.append([abstract_me_code, value, abstract_value, *other, new_code, method_code])
    # for ind, e in enumerate(samples[0]):
    #     print(">>>other: ", ind, e)
    for me_code_list, if_body_code, whole_ass_code, *other, new_code, method_code, _, response in samples:

        content = response["choices"][0]["message"]["content"]
        abstract_code, symbols_map = parse_abstract_code(content)
        print("abstract_code: ",abstract_code,if_body_code)
        # abstract_code=me_code_list[0]+"\n"+abstract_code
        real_instruction = user_instr.replace("{{loop_code}}", me_code_list[0])
        real_instruction = real_instruction.replace("{{if_code}}", abstract_code)

        msg = chatgpt_util.format_message_2(real_instruction, examples=examples, sys_msg=sys_msg)
        print(">>>>>>>>>>real_instruction: ", real_instruction)
        num_tokes = chatgpt_util.num_tokens_from_messages(msg)
        # print("len of msg: ",chatgpt_util.num_tokens_from_messages(msg))
        # if chatgpt_util.num_tokens_from_messages(msg)>=chatgpt_util.MAX_TOKENS:
        #     response
        try:
            response = chatgpt_util.chatGPT_result(msg)
            print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
            reponse_list.append([abstract_code, symbols_map, "\n".join(me_code_list), *other, new_code, method_code])
            reponse_list[-1].extend([[msg, num_tokes], response])
        except:
            traceback.print_exc()
            reponse_list.append([abstract_code, symbols_map, "\n".join(me_code_list), *other, new_code, method_code])
            reponse_list[-1].extend([[msg, num_tokes], traceback.format_exc()])
    return reponse_list

def get_response_instr_for_and_while(user_instr, examples, samples, sys_msg="You are a helpful assistant."):
    reponse_list = []
    method_code_list = []
    for ind_sampl, sample_method in enumerate(samples):
        for code in sample_method:
            # repo_name, old_path, file_html, class_name,me_name, old_list, new_tree,\
            #     old_code,new_code, method_code=code
            # break
            # samples_csv = [[repo, file_html, me_name, me_code, ast.unparse(ass_node) + "\n" + ast.unparse(for_node),
            #                 ast.unparse(new_node), str(remove_ass_flag)] for (
            #                repo, file_path, file_html, class_name, me_name, for_node, ass_node, remove_ass_flag,
            #                new_node, me_code) in samples]
            # for ind, e in enumerate(code):
            #     print("ind>> ",ind, e)
            # print("code: ",code)
            *other, (ass_node_old, for_node_old, if_node,remove_ass_flag, break_list), for_node_old, total_old_code, new_code, method_code = code
            # print(">>>>ass_node_old: ", ass_node_old)

            '''
            print(">>>>for_node: ", for_node_old)
            print(">>>>remove_ass_flag: ", remove_ass_flag)
            print(">>>>ass_node: ", total_old_code)
            # print(">>>>method_code: ", method_code)
            print(">>>>new_node: ", new_code)
            '''
            # print(">>>>me_code: ", new_loop_me_code)
            # print(">>>>remove_ass_flag: ", remove_ass_flag)
            method_code_list.append([*other, for_node_old, ast.unparse(ass_node_old),total_old_code, new_code, method_code])
            break
        # break
    # return
    for *other, for_node_old, ass_code,total_old_code, new_code, me_code in method_code_list:
        tmp_list = loop_else_code_instr.whole_code_pair_for_if(me_code)
        tmp_list += loop_else_code_instr.whole_code_pair_while_if(me_code)

        print(">>>>>>>>>>tmp_list: ", tmp_list)

        for bool_node in tmp_list:
                bool_node_str="\n".join(bool_node)
                real_instruction = user_instr.replace("{{code}}",bool_node_str )

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
                    print("new code: ",new_code)
                    reponse_list.append([bool_node_str, ass_code,*other, new_code, me_code])
                    reponse_list[-1].extend([[msg, num_tokes], response])
                except:
                    traceback.print_exc()
                    reponse_list.append([bool_node_str,ass_code, *other, new_code, me_code])
                    reponse_list[-1].extend([[msg, num_tokes], traceback.format_exc()])
            # break
    # '''
    return reponse_list

def parse_code(content):
    content_list=content.split("New Python code:")
    if len(content_list)==1:
        content_list = content.split("New Python Code:")

    if "No" in content_list[0]:
        return 0, None
    content = content_list[-1].strip()
    return 1,content