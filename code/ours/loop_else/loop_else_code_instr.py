import os,sys
import struct
import traceback
code_dir = "/".join(os.path.abspath(__file__).split("/")[:-2]) + "/"
print("code path: ",code_dir)
sys.path.append(code_dir)
import chatgpt_util,random
import openai, tiktoken,ast,util
import ast
'''
code
snippets
that
consist
of
two
adjacent
blocks: the
For
block and the
If
block
that
the
next
block
of
the
For
block is the
If
block.
for example, for the Python code:
    Assign_stmt_1: viewer = None
For_stmt_1
for v in potential_viewers:
    viewer = shutil.which(v)
    if viewer:
        break

If_stmt_1:
if not viewer:
    raise Exception("Cannot find an image viewer")

Assign_stmt2: subprocess.run([viewer] + paths)

For_stmt_2:
for REG_LINK in REG_LINKS:
    link = REG_LINK + service.lower()
    xml = link_test(link)
    if xml:
        break
If_stmt_2:
if xml is None:
    return None

we
represent
them:
Assign_stmt_1
For_stmt_1
If_stmt_1
Assign_stmt2
For_stmt_2
If_stmt_2

there
are
two
code
snippets,
the
first
code
snippet:
For_stmt_1
If_stmt_1

the
second
snippet:
For_stmt_2
If_stmt_2
'''
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
Write Python code to return a list of If nodes of a given Python code.  
    '''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
def get_if_nodes(code):
    tree = ast.parse(code)
    if_nodes = [node for node in ast.walk(tree) if isinstance(node, ast.If)]
    return if_nodes

def instr_while_code():
    real_instruction = '''
Write Python code to return a list of while statements of a given Python code.  
    '''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])

def get_while_statements(code):
    while_statements = []
    tree = ast.parse(code)
    for node in ast.walk(tree):
        if isinstance(node, ast.While):
            while_statements.append(node)
    return while_statements
def instr_while_code_without_else():
    real_instruction = '''
Write Python code to return a list of while statements without else of a given Python code.  
    '''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])

def get_while_statements_no_else(code):
    tree = ast.parse(code)

    while_loops = []

    for node in ast.walk(tree):
        if isinstance(node, ast.While):
            if not node.orelse:
                while_loops.append(node)
    return while_loops
def instr_get_break_from_for_code():
    real_instruction = '''
Write Python code to get all break statements from a given For node. If child nodes of the For node have For or While node, do not check their child nodes. otherwise, check their child nodes. 
'''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])

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
def instr_for_code_without_else():
    real_instruction = '''
Write Python code to return a list of for statements without else of a given Python code.  
    '''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])

def get_while_statements_no_else(code):
    tree = ast.parse(code)

    while_loops = []

    for node in ast.walk(tree):
        if isinstance(node, ast.While):
            if not node.orelse:
                while_loops.append(node)
    return while_loops


def get_for_loops_without_else(code):
    """
    Returns a list of for loops without else statements in the given code.
    """
    # Parse the code into an abstract syntax tree
    tree = ast.parse(code)

    # Initialize an empty list to store the for loops without else
    for_loops = []

    # Traverse the abstract syntax tree and find all for loops without else
    for node in ast.walk(tree):
        if isinstance(node, ast.For):
            if not node.orelse:
                for_loops.append(node)

    # Return the list of for loops without else
    return for_loops
def instr_whether_same_block():

    real_instruction = '''
Write Python code to get the parent node of a give node from an AST tree.
'''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
def instr_find_parent():

    real_instruction = '''
Write Python code to get the parent node of a give node from a Python code.
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
    if_set=get_if_nodes(code)
    loop_set=get_for_loops_without_else(code)
    loop_set=[e for e in loop_set if has_break_in_for(e)]
    pairs=get_pairs_loop_if(loop_set, if_set)
    pairs = keep_same_parent(pairs)
    new_pairs=[]
    for loop_node, if_node in pairs:
        break_list = get_break_from_loop(loop_node)
        vars=get_name_from_if(if_node)
        if(len(vars))>1:
            continue
        ass_in_for_list=get_ass_node_from_for(vars)
        has_used=whether_use_var_after_if_code(if_node,code,vars)
        new_pairs.append((loop_node, if_node, has_used, ass_in_for_list))
    pairs_str_list=[(ast.unparse(loop_node),ast.unparse(if_node)) for loop_node, if_node in pairs]
    return pairs_str_list
def whole_code_pair_while_if(code):
    if_set=get_if_nodes(code)
    loop_set=get_while_statements_no_else(code)
    loop_set=[e for e in loop_set if has_break_in_for(e)]
    pairs=get_pairs_loop_if(loop_set, if_set)
    pairs_str_list=[(ast.unparse(loop_node),ast.unparse(if_node)) for loop_node, if_node in pairs]
    return pairs_str_list
'''
Write Python code to get all Name AST nodes after a given line number from a given Python code.
'''
def get_names_after_line(code, line_number):
    tree = ast.parse(code)
    names = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and node.lineno > line_number:
            names.append(node.id)
    return names
'''
Write Python code to get all Name AST nodes from a given Python code.
'''
def get_names(code):
    tree = ast.parse(code)

    names = [node.id for node in ast.walk(tree) if isinstance(node, ast.Name)]
    return set(names)

if __name__ == '__main__':
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
    instr_find_parent()
    source_code = """
for i in range(10):
    if i == 5:
        break
    print(i)
    """
    tree = ast.parse(source_code)
    for node in ast.walk(tree):
        if isinstance(node, ast.If):
            parent_node = find_parent_node(node, tree)
            print("parent_node: ",parent_node)

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

    code='''

      
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
    code = """
a = 1
b = 2
for k in e:
    w=e
    k.e, u=1, 3
    pass
c = 3
"""
