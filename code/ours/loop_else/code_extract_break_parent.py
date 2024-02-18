import os,sys
import struct
import traceback
code_dir = "/".join(os.path.abspath(__file__).split("/")[:-2]) + "/"
print("code path: ",code_dir)
sys.path.append(code_dir)
import chatgpt_util,random
import openai, tiktoken,ast,util
import ast

def whole_code_pair_get_break_list_for_if(code):
    new_pairs=[]
    break_parent_list=[]
    tree = ast.parse(code)
    if_set = get_if_nodes(tree)
    loop_set = get_for_loops_without_else(tree)
    pairs = get_pairs_loop_if(loop_set, if_set)
    '''
    conditions:
    1. the same parent of loop_node and if_node
    2. loop_node has the break statement


    3. get assignment statements of variables of if_node.test
    4. get whether the variables of if_node.test is used after the if_node
    '''
    for loop_node, if_node in pairs:
        parent_loop = find_parent_node(loop_node, tree)
        paren_if = find_parent_node(if_node, tree)
        if parent_loop != paren_if:
            continue
        break_list = get_breaks_from_for(loop_node)
        if not break_list:
            continue
        for break_node in break_list:
            parent_break = find_parent_node(break_node, tree)
            break_parent_list.append(parent_break)

        vars = list(set(get_name_nodes(if_node.test)))
        if (len(vars)) != 1:
            continue
        var_name = ast.unparse(vars[0])
        has_used = is_variable_used_after_node(tree, if_node, var_name)

        ass_in_for_list = []
        for break_node in break_list:
            parent_break = find_parent_node(break_node, tree)
            break_parent_list.append(parent_break)
            ass_in_for = get_last_assign_node(parent_break, var_name)
            if ass_in_for:
                ass_in_for_list.append(ass_in_for)
        ass_in_for_list = sorted(list({ass for ass in ass_in_for_list}))

        new_pairs.append((loop_node, if_node, break_parent_list,has_used, ass_in_for_list))

    return new_pairs