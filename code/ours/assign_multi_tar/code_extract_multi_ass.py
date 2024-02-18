'''
Extract all consecutive assign nodes from a given Python code in Python
'''

import os,sys
import struct
import traceback
code_dir = "/".join(os.path.abspath(__file__).split("/")[:-2]) + "/"
print("code path: ",code_dir)
sys.path.append(code_dir)
import chatgpt_util,random
import openai, tiktoken,ast,util
import ast
def instr_0():
    real_instruction = '''
Extract all consecutive assign statements from a given Python code in Python
for example, for the Python code:
a = 1
b = 2
for k in e:
    pass
c = 3


all consecutive assign nodes:
[[a = 1, b = 2], [c = 3]]
    '''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])

def instr_1():
    real_instruction = '''
Extract all two consecutive assign nodes from a given Python code in Python
for example, for the Python code:
a = 1
b = 2
c = 3


all consecutive assign nodes:
[[a = 1, b = 2], [b = 2, c = 3]]
    '''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])

def instr_2():
    real_instruction = '''
Extract all consecutive statements from a given Python code in Python
for example, for the Python code:
a = 1
b = 2
c = 3


all consecutive statements:
[[a = 1, b = 2], [b = 2, c = 3],
[a = 1, b = 2, c = 3]]
    '''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])

def instr_conse_stmt():
    real_instruction = '''
find all consecutive Assign nodes in the same block from a given Python code in Python
for example, for the Python code:
a = 1
b = 2
for i in e:
    if l:
        w=1
        b=1
    else:
        k=2
        c=1
c = 3

all consecutive Assign nodes:
a = 1
b = 2,
w=1
b=1,
k=2
c=1,
c = 3
'''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
'''
Group all consecutive assignment statements from a given Python code in Python
for example, for the Python code:
a = 1
b = 2
for i in e:
    if l:
        w=1
        b=1
    else:
        k=2
        c=1
c = 3


all code snippets whose statements are assignment statements:
a = 1
b = 2,
w=1
b=1,
k=2
c=1,
c = 3
'''
def group_consecutive_assignments(code):
        assignments = []
        current_group = []
        lines = code.split('\n')
        for line in lines:
            if '=' in line:
                current_group.append(line.strip())
            elif current_group:
                assignments.append(current_group)
                current_group = []
        if current_group:
            assignments.append(current_group)
        return assignments
def add_next_stmt(current_code,given_code):

    # Split the given code into lines
    given_lines = given_code.split("\n")
    print("given_lines: ",given_lines)
    # Get the last line of the current code
    current_lines = current_code.split("\n")
    last_line = current_lines[-1]
    print("current_lines: ",current_lines)

    # Find the index of the last line in the given code
    last_line_index = given_lines.index(last_line)

    # Add the next line to the current code
    next_line = given_lines[last_line_index + 1]
    new_code = current_code + "\n" + next_line

    print("new_code: ",new_code)
    return new_code
def instr_3():
    real_instruction = '''
Write Python code to get a new Python code by adding a next statement to current Python code from a given Python code
for example, 
current Python code:
a = 1
b = 2

the given Python code:
a = 1
b = 2
c = 3
d=4


the new Python code:
a = 1
b = 2
c = 3
    '''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
def extract_all_consecutive_ass(code):
    # Parse the code into an AST
    tree = ast.parse(code)

    # Initialize variables
    assign_nodes = []
    current_assigns = []

    # Traverse the AST and extract assign statements
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            current_assigns.append(node)
        else:
            if current_assigns:
                assign_nodes.append(current_assigns)
                current_assigns = []

    # Add the last set of assign statements if any
    if current_assigns:
        assign_nodes.append(current_assigns)

    # Print the result
    # for assigns in assign_nodes:
    #     print([ast.unparse(assign).strip() for assign in assigns])
    return assign_nodes
    # print(assign_nodes)
def extract_two_consecutive_ass(code):
    tree = ast.parse(code)

    consecutive_assigns = []
    prev_assign = None

    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            if prev_assign is not None:
                consecutive_assigns.append([prev_assign, node])
            prev_assign = node
    return consecutive_assigns

def get_combination(code):
    tree = ast.parse(code)

    statements = []
    for i, node in enumerate(tree.body):
        if isinstance(node, ast.Assign):
            statement = [node]
            j = i + 1
            while j < len(tree.body) and isinstance(tree.body[j], ast.Assign):
                statement.append(tree.body[j])
                j += 1
            statements.append(statement)

    consecutive_statements = []
    for statement in statements:
        consecutive_statements.append([ast.unparse(node).strip() for node in statement])

    print(consecutive_statements)
'''
find all consecutive Assign nodes whose line number is consecutive from a given Python code in Python
for example, for the Python code:
a = 1
b = 2
for i in e:
    if l:
        w=1
        b=1
    else:
        k=2
        c=1
c = 3


all code snippets whose statements are assignment statements:
a = 1
b = 2,
w=1
b=1,
k=2
c=1,
c = 3
'''
def find_consecutive_assign_nodes(code_str):
        import ast

        # Parse the code string into an AST
        tree = ast.parse(code_str)

        # Initialize variables to keep track of consecutive Assign nodes
        prev_lineno = None
        assign_nodes = []
        consecutive_assign_nodes = []

        # Traverse the AST and find all Assign nodes
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                assign_nodes.append(node)

        # Iterate over the Assign nodes and find consecutive ones
        for node in assign_nodes:
            if prev_lineno is None or node.lineno == prev_lineno + 1:
                consecutive_assign_nodes.append(node)
            else:
                # If the current node is not consecutive, yield the previous consecutive ones
                if len(consecutive_assign_nodes) > 1:
                    yield consecutive_assign_nodes
                consecutive_assign_nodes = [node]
            prev_lineno = node.lineno

        # Yield any remaining consecutive Assign nodes
        if len(consecutive_assign_nodes) > 1:
            yield consecutive_assign_nodes
if __name__ == '__main__':
    # instr_0()
    # instr_1()
    # instr_2()
    # instr_3()
    code = """
a = 1
b = 2
for k in e:
    w=e
    k.e, u=1, 3
    pass
c = 3
    """
    current_code='''
a = 1
b = 2
c = 3
d=4
'''
    given_code='''
a = 1
b = 2
c = 3
d=4    
'''
    import re
    # instr_conse_stmt()
    code = """
a = 1
b = 2
for i in e:
    if l:
        x_train = tf.ones([batch_size * steps_per_epoch, 28, 28, 1], dtype=tf.float32)
        
        b=1
        #hello
    else:
        k=2
        c=1
    try:
        w.e, c=1
        d=2
    except:
        ee=2
c = 3
    """
    print("code: ",ast.unparse(ast.parse(code)))

    import ast


    def extract_assignments(code_str):
        assignments = []
        for node in ast.walk(ast.parse(code_str)):
            if isinstance(node, ast.Assign):
                assignments.append(node)
        snippets = []
        current_snippet = []
        for node in ast.walk(ast.parse(code_str)):
            if node in assignments:
                current_snippet.append(ast.unparse(node).strip())
            elif current_snippet:
                snippets.append(current_snippet)
                current_snippet = []
        if current_snippet:
            snippets.append(current_snippet)
        return snippets


    # snippets = extract_assignments(code)
    # print(snippets)


    def find_consecutive_assign_nodes(code_str):
        import ast

        # Parse the code string into an AST
        tree = ast.parse(code_str)

        # Initialize variables to keep track of consecutive Assign nodes
        prev_lineno = None
        assign_nodes = []
        consecutive_assign_nodes = []

        # Traverse the AST and find all Assign nodes
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                assign_nodes.append(node)

        # Iterate over the Assign nodes and find consecutive ones
        for node in assign_nodes:
            if prev_lineno is None or node.lineno == prev_lineno + 1:
                consecutive_assign_nodes.append(node)
            else:
                # If the current node is not consecutive, yield the previous consecutive ones
                if len(consecutive_assign_nodes) > 1:
                    yield consecutive_assign_nodes
                consecutive_assign_nodes = [node]
            prev_lineno = node.lineno

        # Yield any remaining consecutive Assign nodes
        if len(consecutive_assign_nodes) > 1:
            yield consecutive_assign_nodes


    for consecutive_assign_nodes in find_consecutive_assign_nodes(code):
        print([ast.unparse(node).strip() for node in consecutive_assign_nodes])

    tree = ast.parse(code)

    consecutive_assigns = []
    current_assigns = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            current_assigns.append(node)
        else:
            if len(current_assigns) > 1:
                consecutive_assigns.append(current_assigns)
            current_assigns = []

    if len(current_assigns) > 1:
        consecutive_assigns.append(current_assigns)

    for assigns in consecutive_assigns:
        print(', '.join([ast.unparse(a).strip() for a in assigns]))


    def find_consecutive_assigns(code):
        # Parse the code into an abstract syntax tree
        tree = ast.parse(code)

        # Initialize variables to keep track of the current block and consecutive assigns
        current_block = []
        consecutive_assigns = []

        # Define a helper function to process a node and its children recursively
        def process_node(node):
            nonlocal current_block, consecutive_assigns

            # If the node is an Assign node, add it to the current block
            if isinstance(node, ast.Assign):
                current_block.append(node)

            # If the node is a control flow statement, process its children in a new block
            elif isinstance(node, (ast.If, ast.For, ast.While)):
                # Process the body of the control flow statement in a new block
                previous_block = current_block
                current_block = []
                for child_node in node.body:
                    process_node(child_node)
                # If there were consecutive assigns in the new block, add them to the list
                if len(current_block) > 1:
                    consecutive_assigns.extend(current_block)
                # Reset the current block to the previous block
                current_block = previous_block

            # If the node is any other type of statement, process its children in the same block
            else:
                for child_node in ast.iter_child_nodes(node):
                    process_node(child_node)

        # Traverse the tree and process each node
        for node in tree.body:
            process_node(node)

        # Return the list of consecutive assigns
        return consecutive_assigns


    consecutive_assigns = find_consecutive_assigns(code)
    for assign in consecutive_assigns:
        print(ast.unparse(assign))
    # def find_consecutive_assignments(code_str):
    #     tree = ast.parse(code_str)
    #     assignments = []
    #     current_assignments = []
    #     for node in ast.walk(tree):
    #         if isinstance(node, ast.Assign):
    #             current_assignments.append(node)
    #         else:
    #             if len(current_assignments) > 1:
    #                 assignments.append(current_assignments)
    #             current_assignments = []
    #     if len(current_assignments) > 1:
    #         assignments.append(current_assignments)
    #     return assignments



    # Parse the code into an AST
    # tree = ast.parse(code)
    # assignments = find_consecutive_assignments(code)
    #
    # for assignment_group in assignments:
    #     print([ast.unparse(assignment).strip() for assignment in assignment_group])
    #
    # # Define a helper function to check if a node is an Assign node
    def is_assign(node):
        return isinstance(node, ast.Assign)




    # def group_consecutive_assignments(code):
    #     assignments = []
    #     current_group = []
    #     lines = code.split('\n')
    #     for line in lines:
    #         if '=' in line:
    #             current_group.append(line.strip())
    #         elif current_group:
    #             assignments.append(current_group)
    #             current_group = []
    #     if current_group:
    #         assignments.append(current_group)
    #     return assignments
    #
    #
    # assignments = group_consecutive_assignments(code)
    # print(assignments)
    # print(extract_all_consecutive_ass(code))
    # add_next_stmt(current_code.strip(), given_code.strip())
    '''
    tree = ast.parse(code)

    consecutive_assigns = []
    prev_assign = None

    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            if prev_assign is not None:
                consecutive_assigns.append([prev_assign, node])
            prev_assign = node

    print(consecutive_assigns)
    '''
    # extract_2()
    # extract_consecu_ass()
    # idiom = "call_star"
    # save_complicated_code_dir_root = util.data_root + "chatgpt/NonIdiomatic/"
    # # save_complicated_code_dir_root = util.data_root + "NonIdiomatic/find_code_snippets/"
    # save_complicated_code_dir = save_complicated_code_dir_root + "sample_methods/"
    #
    # samples = util.load_pkl(save_complicated_code_dir, "sample_methods_" + idiom)
    #
    # # extract_consecutive_subscripts(node)
    # # random.seed(2023)
    # # samples = random.sample(samples, 30)
    # file_name="abstract_same_value_all"#"whether_can_var_unpack_for_subscript_stmt_instr_explain_4_new"
    # reponse_list = call_star_util.abstract_consecutive(samples)
    # util.save_pkl(save_complicated_code_dir_root + idiom + "/",
    #               file_name,
    #               reponse_list)
