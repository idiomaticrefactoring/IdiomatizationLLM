import os, sys
import struct
import traceback

code_dir = "/".join(os.path.abspath(__file__).split("/")[:-2]) + "/"
print("code path: ", code_dir)
sys.path.append(code_dir)
import chatgpt_util, random
import openai, tiktoken, ast, util
import ast,copy
import for_else_util,loop_else_code_instr_node,util_rewrite
from loop_else_code_instr_node import indent_code,unindent_code
def get_acc(samples,new_python_code_list):
    offset=0#-2
    reponse_list=[]
    ground_truth_list=[]
    for ind_sampl, sample_method in enumerate(samples):
        for code in sample_method:
            repo_name, old_path, file_html, class_name,me_name, (ass_node_old, for_node_old, if_node,remove_ass_flag, break_list), for_node_new_else, total_old_code, new_code, method_code = code
            # print("for_node_new_else: ",ast.unparse(for_node_new_else))
            # print("for_node_old: ",ast.unparse(for_node_old))
            # print("if_node: ",ast.unparse(if_node))

            # repo_name, old_path, file_html, class_name,me_name, old_list, new_tree,\
            #     old_code,new_code, method_code=code
            # break
            *other, old_list, new_tree, \
            old_code, new_code, method_code = code
            try:
                ele = [repo_name, old_path, file_html, class_name, me_name, method_code,ast.unparse(ast.parse(ast.unparse(for_node_old)+"\n"+ast.unparse(if_node))), ast.unparse(ast.parse(for_node_new_else))]
            except:
                continue
            ground_truth_list.append(ele)
            # print("new_code:\n",ast.unparse(old_list[0][-2]),new_code)
    #         for i,e in enumerate(ele):
    #             print("i,e: ",i,e)
    #         break
    #     # if ind_sampl>2:
    #     break
    print("len of ground_truth_list: ",len(ground_truth_list))
    # return 0

    # ground_copy_truth_list = ground_truth_list
    ground_copy_truth_list=copy.deepcopy(ground_truth_list)
    ground_copy_truth_list=[e[offset:] for e in ground_copy_truth_list]
    predict_res=[]
    acc=0
    pre=0
    now_list=[]
    print("len of new_python_code_list: ",len(new_python_code_list))

    for ind, sample in enumerate(new_python_code_list):
        # print("sample: ",sample)
        # for i,s in enumerate(sample):
        #     print("i,sample: ",i,s)
        # return 0
        repo_name, old_path, file_html, class_name, me_name, method_code,old_code,refactor_code,*other=sample
        # reponse_list.append([ele_str, abstract_me_code, value, abstract_value, *other])
        # reponse_list.append([0, "Cannot refactor", element_str, slice_str, method_code, me_code, *other])
        # if not flag_can_refactor:
        #     continue
        # print("refactor_code: ",refactor_code)
        # flag_can_refactor, refactor_code,element_seq_str, slice_str,method_code,me_code,_,_,repo_name, old_path, file_html, class_name,me_name,*other = sample
        # bool_code, old_code, repo_name, old_path, file_html, class_name,me_name,*other, new_code, method_code, info, response = sample
        old_refactor_code=refactor_code
        # if flag_can_refactor:
        #     try:
        #         refactor_code = ast.unparse(ast.parse(slice_str))
        #         print("me_code,refactor_code:\n",me_code,refactor_code)
        #     except:
        #         refactor_code =traceback.print_exc()
        if ind==11:
            print(">>>>come here to check: ",old_code,refactor_code)
        try:
            e=[repo_name, old_path, file_html, class_name,me_name,method_code,
               ast.unparse(ast.parse(old_code)),
               ast.unparse(ast.parse(refactor_code))]
        except:
            print("old_code, refactor_code: ",old_code,"\n**********\n",refactor_code)
            print(other)
            traceback.print_exc()
            continue
        # print("predict ele: ", e)

        # predict_res.append(e)
        ground_pre_list=[e[offset:-1] for e in ground_copy_truth_list]
        if e in ground_copy_truth_list:
                index = ground_copy_truth_list.index(e)
                now_list.append(index)
                 # e[-1]=old_refactor_code
                if ind == 11:
                    print("correct ground_copy_truth_list[index][-1]: ", ground_copy_truth_list[index][-1])
                e.append(ground_copy_truth_list[index][-1])
                e.append(1)
                ground_copy_truth_list.pop(index)
                acc+=1
                pre+=1

        elif e[:-1] in ground_pre_list:
            # e[-1] = old_refactor_code
            index=ground_pre_list.index(e[:-1])
            now_list.append(index)
            if ind==11:
                print("ground_copy_truth_list[index][-1]: ",ground_copy_truth_list[index][-1])
            e.append(ground_copy_truth_list[index][-1])
            e.append(0)
            ground_copy_truth_list.pop(index)
        else:
            # continue
            e[-1] = old_refactor_code
            e.append("Cannot refactor")
            e.append(-1)
            # continue
            # acc += 1
        e.extend(other)
        predict_res.append(e )

    predict_res.append(["NOFOUND"])

    for ind,e in enumerate(ground_copy_truth_list):
            predict_res.append(e+[0])
    print("acc: ",acc,len(predict_res),acc/len(ground_truth_list))
    print("precision: ",pre,len(predict_res),pre/len(ground_truth_list))

    return predict_res

def get_break_parent_new(break_parent,exe_bk_blk):
    break_parent_new=break_parent
    break_parent_line = break_parent.split("\n")
    for line in break_parent_line:
        if "break" in line:
            prefix = line.index("break") * " "
            # break_parent_str=ast.unparse(break_parent)

            real_str=exe_bk_blk
            # print("real_str: \n",real_str)
            # print("prefix: ",len(prefix))
            '''
            real_str_list = real_str.split("\n")
            
            prefix_real = []
            for i in real_str_list[0]:
                if i == " ":
                    prefix_real.append(" ")
                else:
                    break
            # print("len of prefix_real: ",len(prefix_real))
            if len(real_str_list) > 1:
                prefix_real = []
                for i in real_str_list[1]:
                    if i == " ":
                        prefix_real.append(" ")
                    else:
                        break
                # print("len of prefix_real_2: ", len(prefix_real))
            '''
            real_str_list = [prefix + e for e in real_str.split("\n")]
            real_str_list.append(prefix + "break")
            break_parent_new = util_rewrite.replace(prefix + "break", "\n".join(real_str_list), break_parent_new)
            print(">>>>break_parent: ",break_parent_new)
    return break_parent_new
'''
For a given set of string, get a new set of string by removing elements that belong to other element from the set.
'''
def remove_substrings(strings):
    result = set(strings)
    for s in strings:
        for t in strings:
            if s != t and s in t:
                result.discard(s)
                break
    return result
def parse_break_stmt(content):
    print("content: ",content)
    try:
        content_list=content.strip().split("\n")
        first,second=":".join(content_list[0].split(":")[1:]).strip(), ":".join(content_list[1].split(":")[1:]).strip()
        return  first if first!="None" else None,second if second!="None" else None
    except:
        print("content: ",content)
        traceback.print_exc()
        return None, None

def get_new_code(loop_node,break_parent_list,block2,else_str,assign_in_block_of_break):
    print(">>>>bloc2: ",block2)
    loop_new = ast.unparse(loop_node)
    break_parent_str_list = [ast.unparse(break_parent) for break_parent in break_parent_list]
    # break_parent_str_list=remove_substrings(break_parent_str_list)
    # break_parent_new = None
    break_parent_list = sorted(break_parent_list, key=lambda i: len(ast.unparse(i)), reverse=True)
    for ind,break_parent_node in enumerate(break_parent_list):
        prefix_break_parent = (break_parent_node.col_offset - loop_node.col_offset) * " "
        break_parent = ast.unparse(break_parent_node)
        break_parent_new = break_parent
        print("break_parent_new: ", break_parent_new)
        if not has_used_var_in_if:
            print("assign_in_block_of_break: ", assign_in_block_of_break)
            print("remove the assign")
            if assign_in_block_of_break[ind]:
                break_parent_new = util_rewrite.replace(ast.unparse(assign_in_block_of_break[ind]), "", break_parent_new)
        print("break_parent_new: ", break_parent_new)
        print("block2: ",block2)
        if block2:
            break_parent_new = get_break_parent_new(break_parent_new, block2)
        # break_parent_new=get_break_parent_new(break_parent)

        print("break_parent_new: ",break_parent_new)

        break_parent_new = "\n".join([prefix_break_parent + e for e in break_parent_new.split("\n")])
        old_break_parent = "\n".join([prefix_break_parent + e for e in break_parent.split("\n")])
        print("break_parent: ", old_break_parent)
        print("break_parent_new: ", break_parent_new)
        loop_new = util_rewrite.replace(old_break_parent, break_parent_new, loop_new)
        # print("loop_old: \n", ast.unparse(loop_node))
        print("loop_new: \n", loop_new)
    return loop_new+"\n"+else_str

if __name__ == '__main__':
    idiom = "loop_else"
    #rewrite_code_4.py
    save_complicated_code_dir_root = util.data_root + "chatgpt/NonIdiomatic/"
    # save_complicated_code_dir_root = util.data_root + "NonIdiomatic/find_code_snippets/"
    save_complicated_code_dir = save_complicated_code_dir_root + "sample_methods/"

    file_name = "which_statement_will_execute_2"
    file_name = "which_statement_will_execute_2_all"
    file_name = "which_statement_will_execute_2_instr3"
    file_name = "which_statement_will_execute_4"
    file_name = "which_statement_will_execute_4_new"
    file_name = "which_statement_will_execute_5_new"
    file_name ="which_statement_will_execute_4_all"
    # abstract_total_code_split_if_for_abstract_2_improve_50
    # file_name = "which_statement_will_execute_4_improve"  # "extract_arithmetic_seq_from_arguments_instr3_all"  # "whether_can_var_unpack_for_subscript_stmt_instr_explain_4_new"
    file_name = "which_statement_will_execute_4_improve_all"
    file_name = "which_statement_will_execute_4_improve"  # "extract_arithmetic_seq_from_arguments_instr3_all"  # "whether_can_var_unpack_for_subscript_stmt_instr_explain_4_new"
    file_name = "which_statement_will_execute_4_improve_all_new"
    file_name = "which_statement_will_execute_4_improve_2_all_new"  # "extract_arithmetic_seq_from_arguments_instr3_all"  # "whether_can_var_unpack_for_subscript_stmt_instr_explain_4_new"
    file_name = "which_statement_will_execute_4_improve_2_all_new_fine_tune"  # "extract_arithmetic_seq_from_arguments_instr3_all"  # "whether_can_var_unpack_for_subscript_stmt_instr_explain_4_new"

    samples = util.load_pkl(save_complicated_code_dir_root + idiom + "/", file_name)
    print("len of samples: ",len(samples))
    new_python_code_list=[]
    # reponse_list.append(
    #     [abstract_code, symbols_map, abstract_if_code, symbols_map_if, total_old_code, loop_str, if_str,
    #      break_parent_list,
    #      has_used_var_in_if, assign_in_block_of_break, ass_code, *other, new_code, method_code])
    # reponse_list[-1].extend([[msg, num_tokes], traceback.format_exc()])
    # # br
    count=0
    # reponse_list.append(
    #     [loop_str + "\n" + if_str, total_replace_for_code, first_line_list, blocks_list, loop_node, if_node,
    #      break_parent_list, has_used_var_in_if, assign_in_block_of_break, ass_code, *other, new_code, me_code])

    for ind_s,(abstract_for_code, symbols_for_map,abstract_code, total_replace_for_code,first_line_list, blocks_list,loop_node, if_node, \
        break_parent_list, has_used_var_in_if, assign_in_block_of_break, ass_code, *other, new_code, method_code,_,response) in enumerate(samples):
        content = response["choices"][0]["message"]["content"]
        print(">>>>>>>>>>has_used_var_in_if: ", has_used_var_in_if)
        # new_pairs.append((loop_node, if_node, break_parent_list,has_used, ass_in_for_list))

        # print("total_old_code: ",total_old_code)
        # print("loop_str, if_str: ",loop_str, if_str)
        exe_bk_blk,no_exe_bk_blk=parse_break_stmt(content)
        old_code=ast.unparse(loop_node)+"\n"+ast.unparse(if_node)
        print("exe_bk_blk,no_exe_bk_blk: ", exe_bk_blk,no_exe_bk_blk)
        if "if fnmatch.filter([destFile], ptrn)" in ast.unparse(loop_node):
            print(">>>>>come here: ",)

        print("content: ",ast.unparse(if_node),"***\n",content,abstract_for_code)
        if not exe_bk_blk and not no_exe_bk_blk:
            continue
        elif no_exe_bk_blk:
            new_code = ""
            # else_str=get_else_str()
            block_1 = blocks_list[0]
            block2 = None
            if len(blocks_list) > 1:

                if first_line_list[1].startswith("else"):
                    block2 = unindent_code(blocks_list[1])
                else:
                    print("blocks_list: ",blocks_list[1:])
                    # prefix_block2 = "if not" + first_line_list[0][2:]
                    first_line_list[1] = first_line_list[1][2:]
                    block2 = "\n".join(
                        [e1 + "\n" + e2 for e1, e2 in zip(first_line_list[1:], blocks_list[1:])])
                    print("block2: ",block2)
            else_str = "else:\n" + block_1
            new_code=get_new_code(loop_node, break_parent_list, block2, else_str,assign_in_block_of_break)
        else:
            block_2 = unindent_code(blocks_list[0])
            block_1 = None
            if len(blocks_list) > 1:

                if first_line_list[1].startswith("else"):
                    block_1 = blocks_list[1]
                else:
                    # prefix_block2 = "if not" + first_line_list[0][2:]
                    first_line_list[1] = first_line_list[1][2:]
                    block_1 = indent_code("\n".join(
                        [e1 + "\n" + e2 for e1, e2 in zip(first_line_list[1:], blocks_list[1:])]))
            if not block_1:
                continue
            else_str = "else:\n" + block_1
            new_code=get_new_code(loop_node, break_parent_list, block_2, else_str,assign_in_block_of_break)

        print("old_code: ",old_code)
        print("new_code: ",new_code)
        new_python_code_list.append([*other,method_code,ast.unparse(ast.parse(old_code)),ast.unparse(ast.parse(new_code)),abstract_for_code,content])
    # util.save_pkl(save_complicated_code_dir_root + idiom + "/","gpt_result_"+idiom,new_python_code_list)
    util.save_pkl(save_complicated_code_dir_root + idiom + "/","gpt_result_fine_tune_"+idiom,new_python_code_list)

    # '''
    samples = util.load_pkl(save_complicated_code_dir, "sample_methods_" + idiom)

    # random.seed(2023)
    #
    # samples = random.sample(samples, 50)
    csv_res_list=get_acc(samples, new_python_code_list)
    acc_file_name = file_name + "_get_acc_new_add_continue_instr3_add_new_found_new.csv"  # "direct_refactor_from_blocks_no_dependinstr_get_acc.csv"
    acc_file_name = file_name + "_get_acc_new_add_continue_instr3_add_new_found_new.csv"  # "direct_refactor_from_blocks_no_dependinstr_get_acc.csv"

    # util.save_csv(
    #     save_complicated_code_dir_root + idiom + "/" + acc_file_name,
    #     csv_res_list,
    #     ["repo_name", "file_path", "file_html", "class_name", "me_name", "me_code", "old_code", "chatGPT_code",
    #      "element_str",
    #      "slice_str", "truth_code"])



# '''

                # break_parent_line = loop_str.split("\n")
                    # for line in break_parent_line:
                    #     if "break" in line:
                    #         prefix = line.index("break") * " "
                    # loop_str=util_rewrite.replace(break_parent, break_parent_new, loop_str)










