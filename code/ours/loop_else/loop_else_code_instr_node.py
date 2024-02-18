import os,sys
import struct
import traceback
code_dir = "/".join(os.path.abspath(__file__).split("/")[:-2]) + "/"
print("code path: ",code_dir)
sys.path.append(code_dir)
import chatgpt_util,random
import openai, tiktoken,ast,util
import ast

def instr_1():
    real_instruction = '''
Write Python code to get all for statements
'''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])

def instr_2():
    real_instruction = '''
Write Python code to get all blocks consisting of a For statement and an If statement where the start line number of If statement is equal to the end line number of For statement + 1 from a given Python code.
'''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
def instr_code_pairs_improve():
    real_instruction = '''
We give you two sets: a set of loop nodes (loop_set) and a set of If nodes (if_set), write Python code to get all pairs that the end line number of loop statement from for_set plus 1 is equal to the start line number of the If statement from if_set.  
    '''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
def get_pairs_loop_if(loop_set, if_set):
    pairs = []
    for loop_node in loop_set:
        for if_node in if_set:
            if loop_node.end_lineno + 1 == if_node.lineno:
                pairs.append((loop_node, if_node))
    return pairs
def instr_code_pairs():
    real_instruction = '''
We give you two sets: a set of For nodes (for_set) and a set of If nodes (if_set), write Python code to get all pairs that the start line number of the If statement from if_set is equal to the end line number of For statement from for_set plus 1
    '''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
def get_pairs(for_set, if_set):
    pairs = []
    for for_node in for_set:
        for if_node in if_set:
            if if_node.lineno == for_node.end_lineno + 1:
                pairs.append((for_node, if_node))
    return pairs
def instr_for_code():
    real_instruction = '''
Write Python code to return a list of For nodes of a given Python code.  
    '''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])

def get_for_nodes(code):
    tree = ast.parse(code)
    for_nodes = [node for node in ast.walk(tree) if isinstance(node, ast.For)]
    return for_nodes
    '''
    for_nodes = get_for_nodes(code)
    print(for_nodes)
    '''

def instr_if_code():
    real_instruction = '''
Write Python code to return a list of If nodes from a given AST tree.  
    '''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
# def get_if_nodes(code):
#     tree = ast.parse(code)
#     if_nodes = [node for node in ast.walk(tree) if isinstance(node, ast.If)]
#     return if_nodes
def get_if_nodes(tree):
    if_nodes = []
    for node in ast.walk(tree):
        if isinstance(node, ast.If):
            if_nodes.append(node)
    return if_nodes
def instr_while_code():
    real_instruction = '''
Write Python code to return a list of while statements from a given AST tree.  
    '''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])

def get_while_statements(tree):
    while_statements = []
    for node in ast.walk(tree):
        if isinstance(node, ast.While):
            while_statements.append(node)
    return while_statements
def instr_while_code_without_else():
    real_instruction = '''
Write Python code to return a list of while statements without else of a given AST tree.  
    '''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])

def get_while_statements_without_else(tree):
    while_statements = []
    for node in ast.walk(tree):
        if isinstance(node, ast.While):
            if not node.orelse:
                while_statements.append(node)
    return while_statements

def instr_for_code_without_else():
    real_instruction = '''
Write Python code to return a list of for statements without else of a given AST tree.  
    '''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])

def get_for_loops_without_else(tree):
    for_loops = []
    for node in ast.walk(tree):
        if isinstance(node, ast.For):
            if not node.orelse:
                for_loops.append(node)
    return for_loops
def instr_get_break_from_for_code():
    real_instruction = '''
Write Python code to get all break statements from a given For node. If child nodes of the For node have For or While node, do not check their child nodes. otherwise, check their child nodes. 
'''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])

def instr_replace_node():
    real_instruction = '''
Write Python code to replace a code snippets with a new code snippets from a given code. 
'''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
def get_breaks_from_for(node):
    breaks = []
    for child in ast.iter_child_nodes(node):
        if isinstance(child, ast.For) or isinstance(child, ast.While):
            continue
        elif isinstance(child, ast.Break):
            breaks.append(child)
        else:
            breaks.extend(get_breaks_from_for(child))
    return breaks
def instr_for_code_with_break():
    real_instruction = '''
Write Python code to determine whether a given For node contains break statement. If child nodes of the For node have For or While node, do not check their child nodes. otherwise, check their child nodes. 
    '''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
def has_break_in_for(node):
    """
    Check if a given For node contains a break statement.
    """
    for child in ast.iter_child_nodes(node):
        if isinstance(child, (ast.For, ast.While)):
            # If child node is a loop, skip its child nodes
            continue
        elif isinstance(child, ast.Break):
            return True
        elif isinstance(child, ast.AST):
            # Recursively check child nodes
            if has_break_in_for(child):
                return True
    return False

def instr_find_parent():

    real_instruction = '''
Write Python code to get the parent node of a give node from a AST tree.
'''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
def find_parent_node(node, parent):
    for child in ast.iter_child_nodes(parent):
        if child == node:
            return parent
        else:
            result = find_parent_node(node, child)
            if result is not None:
                return result
    return None
def instr_split_if_statement_3():
    """
    Returns a list of assignment statements whose assigned variable is a given variable in a given for node.
    """
    real_instruction = '''
Write Python code to extract lines that each line of code that is not indented

for example, for the following Python code:
if a:
    a=1
    if b:
        c=1
else:
    print(e)

the first line:
if a:
the second line:
else:
'''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
def instr_unindent_each_line():
    """
    Returns a list of assignment statements whose assigned variable is a given variable in a given for node.
    """
    real_instruction = '''
Write Python code to unindent each line of a given code
'''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
def unindent_code(code):
    # Split the code into lines
    lines = code.split('\n')

    # Find the minimum indentation level
    min_indent = float('inf')
    for line in lines:
        stripped_line = line.lstrip()
        if stripped_line and stripped_line[0] != '#':
            indent = len(line) - len(stripped_line)
            min_indent = min(min_indent, indent)

    # Remove the minimum indentation level from each line
    unindented_lines = []
    for line in lines:
        unindented_lines.append(line[min_indent:])

    # Join the unindented lines and return the result
    return '\n'.join(unindented_lines)
def instr_indent_each_line():
    """
    Returns a list of assignment statements whose assigned variable is a given variable in a given for node.
    """
    real_instruction = '''
Write Python code to indent each line of a given code
'''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
def indent_code(code, spaces=4):
    indented_code = ""
    for line in code.split("\n"):
        indented_code += " " * spaces + line + "\n"
    return indented_code
def extract_unindent_lines(code):
    non_indented_lines = []
    for line in code.split('\n'):
        if not line.startswith(' '):
            non_indented_lines.append(line)
    return non_indented_lines

def extract_blocks(code):
    print(">>code: ",code)
    blocks = []
    current_block = []
    for line in code.split('\n'):
        if line.strip() == '':
            continue
        if line.startswith(' ') or line.startswith('\t'):
            current_block.append(line)
        else:
            if current_block:
                print("current_block: ",current_block)
                blocks.append('\n'.join(current_block))
                current_block = []

    if current_block:
        blocks.append('\n'.join(current_block))
    return blocks
def instr_split_if_statement_2():

    real_instruction = '''
Write Python code to extract blocks by dividing a given code according to each line of code that is not indented

for example, for the following Python code:
if a:
    a=1
    if b:
        c=1
else:
    print(e)

the first block:
a=1
if b:
    c=1
the second block:
print(e)
'''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
def get_blocks_divide_if(code):
    blocks = []
    current_block = []
    for line in code.split('\n'):
        if line.strip() == '':
            continue
        if line[0] != ' ':
            if current_block:
                blocks.append((' '.join(current_block[0].split()), '\n'.join(current_block[1:])))
                current_block = []
            current_block.append(line)
        else:
            current_block.append(line)
    if current_block:
        blocks.append((' '.join(current_block[0].split()), '\n'.join(current_block[1:])))
    return blocks
def symbol_mapping_fun(code):
    lines = code.split('\n')
    mapping = ''
    indent_level = 0
    for line in lines:
        if line.strip() == '':
            continue
        if line.startswith(' ' * indent_level):
            mapping += line[indent_level:] + '\n'
        else:
            indent_level = len(line) - len(line.lstrip())
            mapping += line + '\n'
    return mapping
def instr_split_if_statement():

    real_instruction = '''
Write Python code to return a list of blocks and symbol mapping by using symbol zj to represent blocks by dividing the code based on each line of code that is not indented.
for example, for the following Python code:
if a:
    a=1
    if b:
        c=1
else:
    print(e)
 
a list of blocks:
if a:
    zj1
,    
else:
    zj2
    
the symbol mapping is:
zj1:
a=1
if b:
    c=1

zj2:
print(e)
'''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
def divide_code(code):
        # Split the code into lines
        lines = code.split('\n')

        # Initialize the symbol mapping and the new code
        symbol_mapping = {}
        new_code = ''

        # Initialize the current block level and the current block code
        current_block_level = 0
        current_block_code = ''

        # Iterate over each line of code
        for line in lines:
            # If the line is not indented
            if not line.startswith(' '):
                # If there is a current block code, add it to the symbol mapping
                if current_block_code:
                    symbol_mapping[f'zj{len(symbol_mapping) + 1}'] = current_block_code
                    new_code += f'zj{len(symbol_mapping)}\n'
                    current_block_code = ''

                # Add the current line to the new code
                new_code += f'{line}\n'

                # Reset the current block level
                current_block_level = 0
            else:
                # If the current block level is zero, set it to the indentation level of the current line
                if current_block_level == 0:
                    current_block_level = len(line) - len(line.lstrip())

                # Add the current line to the current block code
                current_block_code += f'{line}\n'

        # If there is a current block code, add it to the symbol mapping
        if current_block_code:
            symbol_mapping[f'zj{len(symbol_mapping) + 1}'] = current_block_code
            new_code += f'zj{len(symbol_mapping)}\n'

        # Return the new code and the symbol mapping
        return new_code, symbol_mapping
def get_blocks(code):
    blocks = []
    symbol_mapping = {}
    current_block = ""
    current_symbol = ""
    for line in code.split("\n"):
        if line.strip() == "":
            continue
        if line.startswith(" "):
            current_block += line + "\n"
        else:
            if current_block != "":
                blocks.append(current_block.strip())
                symbol_mapping[current_symbol] = current_block.strip()
                current_block = ""
            current_symbol = "zj" + str(len(symbol_mapping) + 1)
            current_block += line + "\n"
    if current_block != "":
        blocks.append(current_block.strip())
        symbol_mapping[current_symbol] = current_block.strip()
    return blocks, symbol_mapping
def instr_assignment_statements_from_for_stmt():
    """
    Returns a list of assignment statements whose assigned variable is a given variable in a given for node.
    """
    real_instruction = '''
Write Python code to return a list of assignment statements whose assigned variable is a given variable in a given for node.
'''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
def whole_code_pair_for_if(code):
    if_set=get_if_nodes(code)
    loop_set=get_for_loops_without_else(code)
    loop_set=[e for e in loop_set if has_break_in_for(e)]
    pairs=get_pairs_loop_if(loop_set, if_set)
    pairs_str_list=[(ast.unparse(loop_node),ast.unparse(if_node)) for loop_node, if_node in pairs]
    return pairs_str_list
def whole_code_pair_same_parent_for_if(code):
    tree=ast.parse(code)
    if_set=get_if_nodes(tree)
    loop_set=get_for_loops_without_else(tree)
    pairs=get_pairs_loop_if(loop_set, if_set)
    new_pairs=[]
    '''
    conditions:
    1. the same parent of loop_node and if_node
    2. loop_node has the break statement
    
    
    3. get assignment statements of variables of if_node.test
    4. get whether the variables of if_node.test is used after the if_node
    '''
    #
    for loop_node, if_node in pairs:
        parent_loop=find_parent_node(loop_node)
        paren_if=find_parent_node(if_node)
        if parent_loop!=paren_if:
            continue
        break_list = get_breaks_from_for(loop_node)
        if not break_list:
            continue
        vars = list(set(get_name_nodes(if_node.test)))
        if (len(vars)) != 1:
            continue
        var_name=ast.unparse(vars[0])
        has_used = is_variable_used_after_node(tree, node, var_name)

        ass_in_for_list=[]
        for break_node in break_list:
            parent_break = find_parent_node(break_node)
            ass_in_for = get_last_assign_node(parent_break, var_name)
            if ass_in_for:
                ass_in_for_list.append(ass_in_for)
        ass_in_for_list_str=sorted(list({ast.unparse(ass) for ass in ass_in_for_list}))

        new_pairs.append((ast.unparse(loop_node), ast.unparse(if_node), has_used, ass_in_for_list_str))
    pairs_str_list=[(ast.unparse(loop_node),ast.unparse(if_node)) for loop_node, if_node in pairs]
    return pairs_str_list

def filter_pairs(pairs,tree):
    new_pairs = []
    '''
    conditions:
    1. the same parent of loop_node and if_node
    2. loop_node has the break statement


    3. get assignment statements of variables of if_node.test
    4. get whether the variables of if_node.test is used after the if_node
    '''
    #
    for loop_node, if_node in pairs:
        parent_loop = find_parent_node(loop_node,tree)
        paren_if = find_parent_node(if_node,tree)
        if parent_loop != paren_if:
            continue
        break_list = get_breaks_from_for(loop_node)
        if not break_list:
            continue
        vars = list(set(get_name_nodes(if_node.test)))
        if (len(vars)) != 1:
            continue
        var_name = ast.unparse(vars[0])
        has_used = is_variable_used_after_node(tree, if_node, var_name)

        ass_in_for_list = []
        for break_node in break_list:
            parent_break = find_parent_node(break_node,tree)
            ass_in_for = get_last_assign_node(parent_break, var_name)
            if ass_in_for:
                ass_in_for_list.append(ass_in_for)
        ass_in_for_list_str = sorted(list({ast.unparse(ass) for ass in ass_in_for_list}))

        new_pairs.append((ast.unparse(loop_node), ast.unparse(if_node), has_used, ass_in_for_list_str))
    # pairs_str_list = [(ast.unparse(loop_node), ast.unparse(if_node)) for loop_node, if_node in pairs]
    return new_pairs

def filter_pairs_2(pairs,tree):
    new_pairs = []
    '''
    conditions:
    1. the same parent of loop_node and if_node
    2. loop_node has the break statement


    3. get assignment statements of variables of if_node.test
    4. get whether the variables of if_node.test is used after the if_node
    '''
    #
    for loop_node, if_node in pairs:
        parent_loop = find_parent_node(loop_node)
        paren_if = find_parent_node(if_node)
        if parent_loop != paren_if:
            continue
        break_list = get_breaks_from_for(loop_node)
        if not break_list:
            continue
        vars = list(set(get_name_nodes(if_node.test)))
        has_used=0

        for var in vars:
            var_name = ast.unparse(var)
            if is_variable_used_after_node(tree, node, var_name):
                has_used=1
                break


        ass_in_for_list = []
        for var in vars:
            var_name = ast.unparse(var)
            for break_node in break_list:
                parent_break = find_parent_node(break_node)
                ass_in_for = get_last_assign_node(parent_break, var_name)
                ass_in_for_list.append(ass_in_for)
        ass_in_for_list_str = sorted(list({ast.unparse(ass) for ass in ass_in_for_list}))

        new_pairs.append((ast.unparse(loop_node), ast.unparse(if_node), has_used, ass_in_for_list_str))
    pairs_str_list = [(ast.unparse(loop_node), ast.unparse(if_node)) for loop_node, if_node in pairs]
    return pairs_str_list
def whole_code_pair_same_parent_for_if(code):
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
    return filter_pairs(pairs,tree)

def whole_code_pair_get_break_list_for_if(code):
    new_pairs=[]
    break_ass_pairs=[]
    tree = ast.parse(code)
    if_set = get_if_nodes(tree)
    loop_set = get_for_loops_without_else(tree)
    while_set = get_while_statements_without_else(tree)
    loop_set.extend(while_set)
    pairs = get_pairs_loop_if(loop_set, if_set)
    '''
    conditions:
    1. the same parent of loop_node and if_node
    2. loop_node has the break statement

    3. get assignment statements of variables of if_node.test
    4. get whether the variables of if_node.test is used after the if_node
    '''
    for loop_node, if_node in pairs:
        break_parent_list = []
        parent_loop = find_parent_node(loop_node, tree)
        paren_if = find_parent_node(if_node, tree)
        if parent_loop != paren_if:
            continue
        break_list = get_breaks_from_for(loop_node)
        if not break_list:
            continue
        # for break_node in break_list:
        #     parent_break = find_parent_node(break_node, tree)
        #     break_parent_list.append(parent_break)

        vars = list(set(get_name_nodes(if_node.test)))
        if (len(vars)) != 1:
            continue
        var_name = ast.unparse(vars[0])
        has_used = is_variable_used_after_node(tree, if_node, var_name)
        print("len of break_list: ",len(break_list))
        ass_in_for_list = []
        for break_node in break_list:
            parent_break = find_parent_node(break_node, tree)
            break_parent_list.append(parent_break)
            ass_in_for=get_last_assign_node(tree, var_name, break_node.lineno)
            # ass_in_for = get_last_assign_node(parent_break, var_name)
            if ass_in_for:
                ass_in_for_list.append(ass_in_for)
                break_ass_pairs.append((ass_in_for))
            else:
                break_ass_pairs.append((parent_break))

        ass_in_for_list = list({ass for ass in ass_in_for_list})

        new_pairs.append((loop_node, if_node, break_parent_list,has_used, ass_in_for_list))

    return new_pairs

def whole_code_pair_get_break_list_for_if_improve(code):
    new_pairs=[]
    break_ass_pairs=[]
    tree = ast.parse(code)
    if_set = get_if_nodes(tree)
    loop_set = get_for_loops_without_else(tree)
    while_set = get_while_statements_without_else(tree)
    loop_set.extend(while_set)
    pairs = get_pairs_loop_if(loop_set, if_set)
    '''
    conditions:
    1. the same parent of loop_node and if_node
    2. loop_node has the break statement

    3. get assignment statements of variables of if_node.test
    4. get whether the variables of if_node.test is used after the if_node
    '''
    for loop_node, if_node in pairs:
        break_parent_list = []
        parent_loop = find_parent_node(loop_node, tree)
        paren_if = find_parent_node(if_node, tree)
        if parent_loop != paren_if:
            continue
        break_list = get_breaks_from_for(loop_node)
        if not break_list:
            continue
        # for break_node in break_list:
        #     parent_break = find_parent_node(break_node, tree)
        #     break_parent_list.append(parent_break)

        vars = list(set(get_name_nodes(if_node.test)))
        if (len(vars)) != 1:
            continue
        var_name = ast.unparse(vars[0])
        has_used = is_variable_used_after_node(tree, if_node, var_name)
        print("len of break_list: ",len(break_list))
        ass_in_for_list = []
        for break_node in break_list:
            parent_break = find_parent_node(break_node, tree)
            break_parent_list.append(parent_break)
            ass_in_for=get_last_assign_node_before_line(parent_break, var_name, break_node.lineno)
            # ass_in_for = get_last_assign_node(parent_break, var_name)
            if ass_in_for:
                ass_in_for_list.append(ass_in_for)
                break_ass_pairs.append((ass_in_for))
            else:
                ass_in_for_list.append(None)
                break_ass_pairs.append((parent_break))

        # ass_in_for_list = list({ass for ass in ass_in_for_list})

        new_pairs.append((loop_node, if_node, break_parent_list,has_used, ass_in_for_list))

    return new_pairs

def whole_code_pair_while_if(code):
    if_set=get_if_nodes(code)
    loop_set=get_while_statements_no_else(code)
    loop_set=[e for e in loop_set if has_break_in_for(e)]
    pairs=get_pairs_loop_if(loop_set, if_set)
    pairs_str_list=[(ast.unparse(loop_node),ast.unparse(if_node)) for loop_node, if_node in pairs]
    return pairs_str_list
def instr_check_names_after_line():
    real_instruction = '''
Write Python code to check whether a given variable is used after a given node from a given AST tree.
'''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
def is_variable_used_after_node(tree, node, variable_name):
    """
    Check whether a given variable is used after a given node from a given AST tree.
    """
    class VariableUsageVisitor(ast.NodeVisitor):
        def __init__(self, node, variable_name):
            self.node = node
            self.variable_name = variable_name
            self.variable_used_after_node = False

        def visit_Name(self, node):
            if node.id == self.variable_name and node.lineno > self.node.lineno:
                self.variable_used_after_node = True

    visitor = VariableUsageVisitor(node, variable_name)
    visitor.visit(tree)
    return visitor.variable_used_after_node
# def is_variable_used_after_start(node, variable):
#     start_line = node.lineno
#     for node in ast.walk(node):
#         if isinstance(node, ast.Name) and node.id == variable and node.lineno > start_line:
#             return True
#     return False
'''
Write Python code to get all Name AST nodes after the line number of a given node from a given AST tree.
'''
def instr_get_names_after_line():
    real_instruction = '''
Write Python code to get all Name AST nodes after the line number of a given node from a given AST tree.
'''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
'''
Write Python code to get all Name AST nodes after the line number of a given node from a given AST tree.
'''
def get_names_after_line(node, tree):
    names = []
    for n in ast.walk(tree):
        if isinstance(n, ast.Name) and n.lineno > node.lineno:
            names.append(n)
    return names
def instr_get_ass_node_from_for_2():
    real_instruction = '''
Write Python code to get the last assign AST node before a line number that assigning values to a given variable from a given AST tree.
'''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])


def get_last_assign_node_before_line(tree, var_name, line_num):
    last_assign_node = None

    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == var_name and node.lineno <= line_num:
                    last_assign_node = node

    return last_assign_node
def instr_get_ass_node_from_for():
    real_instruction = '''
Write Python code to get the last assign AST node that assigning values to a given variable from a given AST tree.
'''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
def get_last_assign_node(tree, var_name):
    last_assign_node = None
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == var_name:
                    last_assign_node = node
    return last_assign_node
def instr_get_names_from_node():

    real_instruction = '''
Write Python code to get all Name AST nodes from a given AST tree.
'''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
def get_name_nodes(tree):
    name_nodes = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            name_nodes.append(node)
    return name_nodes
'''
Write Python code to get all Name AST nodes from a given Python code.
'''
def get_names(code):
    tree = ast.parse(code)

    names = [node.id for node in ast.walk(tree) if isinstance(node, ast.Name)]
    return set(names)

if __name__ == '__main__':
    # instr_if_code()
    # instr_while_code()
    # instr_while_code_without_else()
    # instr_for_code_without_else()
    # instr_get_break_from_for_code()
    # instr_find_parent()
    # instr_get_names_after_line()
    # instr_get_ass_node_from_for()
    # instr_get_names_from_node()
    # instr_check_names_after_line()
    # instr_0()
    # instr_1()
    # instr_2()
    # instr_code_pairs()
    # instr_for_code()
    # instr_if_code()
    # instr_while_code()
    # instr_code_pairs_improve()
    # instr_while_code_without_else()
    # instr_for_code_without_else()
    # instr_for_code_with_break()
    # instr_3()
    # instr_assignment_statements_from_for_stmt()
    # instr_whether_same_block()
    # instr_find_parent()
    # instr_get_names_from_node()
    # instr_replace_node()
    # instr_split_if_statement()
    # instr_split_if_statement()
    # instr_split_if_statement_2()
    # instr_split_if_statement_3()
    # instr_unindent_each_line()
    instr_get_ass_node_from_for_2()
    # instr_indent_each_line()
    source_code = """
for i in range(10):
    
    print(k)
if i == 5:
        j=2
        break  
print(i)  
    """
    tree = ast.parse(source_code)
    for node in ast.walk(tree):
        if isinstance(node, ast.If):
            is_use=is_variable_used_after_node(tree, node, 'j')
            print("is_use: ",is_use)

            # parent_node = find_parent_node(node, tree)
            # print("parent_node: ",parent_node)

    #
    #     tree = ast.parse(source_code)
#     def has_break(node):
#         if isinstance(node, ast.Break):
#             return True
#         elif isinstance(node, ast.For) or isinstance(node, ast.While):
#             return False
#         else:
#             for child in ast.iter_child_nodes(node):
#                 if has_break(child):
#                     return True
#             return False
#
#
#     source_code = """
# for i in range(10):
#     if i == 5:
#         break
#     print(i)
#     """
#
#     tree = ast.parse(source_code)
#     for node in ast.walk(tree):
#         if isinstance(node, ast.For):
#             if has_break(node.body):
#                 print("The for loop contains a break statement.")
#             else:
#                 print("The for loop does not contain a break statement.")

    # def contains_break(stmt):
    #     """
    #     Returns True if the given statement contains a break statement.
    #     """
    #     if isinstance(stmt, ast.For):
    #         # Check if the for loop body contains a break statement
    #         for node in ast.walk(stmt):
    #             if isinstance(node, ast.Break):
    #                 return True
    #             elif isinstance(node, (ast.For, ast.While)):
    #                 # If the body contains another for or while loop, skip it
    #                 continue
    #         return False
    #     else:
    #         return False
    def divide_code(code):
        # Split the code into lines
        lines = code.split('\n')

        # Initialize the symbol mapping and the new code
        symbol_mapping = {}
        new_code = ''

        # Initialize the current block level and the current block code
        current_block_level = 0
        current_block_code = ''

        # Iterate over each line of code
        for line in lines:
            # If the line is not indented
            if not line.startswith(' '):
                # If there is a current block code, add it to the symbol mapping
                if current_block_code:
                    symbol_mapping[f'zj{len(symbol_mapping) + 1}'] = current_block_code
                    new_code += f'zj{len(symbol_mapping)}\n'
                    current_block_code = ''

                # Add the current line to the new code
                new_code += f'{line}\n'

                # Reset the current block level
                current_block_level = 0
            else:
                # If the current block level is zero, set it to the indentation level of the current line
                if current_block_level == 0:
                    current_block_level = len(line) - len(line.lstrip())

                # Add the current line to the current block code
                current_block_code += f'{line}\n'

        # If there is a current block code, add it to the symbol mapping
        if current_block_code:
            symbol_mapping[f'zj{len(symbol_mapping) + 1}'] = current_block_code
            new_code += f'zj{len(symbol_mapping)}\n'

        # Return the new code and the symbol mapping
        return new_code, symbol_mapping
    code='''  if a:
      a=1
      if b:
        c=1
  elif b:
      print(e) 
  else:
      w=w+1
      b=b+2  
'''


    blocks = extract_blocks(code)
    print("***************")
    print(blocks)
    for e in blocks:
        print(e)


    def unindent_code(code):
        # Split the code into lines
        lines = code.split('\n')

        # Find the minimum indentation level
        min_indent = float('inf')
        for line in lines:
            stripped_line = line.lstrip()
            if stripped_line and stripped_line[0] != '#':
                indent = len(line) - len(stripped_line)
                min_indent = min(min_indent, indent)

        # Remove the minimum indentation level from each line
        unindented_lines = []
        for line in lines:
            unindented_lines.append(line[min_indent:])

        # Join the unindented lines and return the result
        return '\n'.join(unindented_lines)


    print(unindent_code(code))

    '''
    def has_break_in_for(node):
        """
        Check if a given For node contains a break statement.
        """
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.For, ast.While)):
                # If child node is a loop, skip its child nodes
                continue
            elif isinstance(child, ast.Break):
                return True
            elif isinstance(child, ast.AST):
                # Recursively check child nodes
                if has_break_in_for(child):
                    return True
        return False
    for node in ast.walk(ast.parse(code)):
        if isinstance(node,ast.For):

            if has_break_in_for(node):
                print("has break")
            else:
                print("no break")
            break
    '''
    code = """
a = 1
b = 2
for k in e:
    w=e
    k.e, u=1, 3
    pass
c = 3
"""
