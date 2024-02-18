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
'''
import ast

def get_for(code):
    """
    extract all For AST nodes

    Parameters
    ----------
    code : string
        a Python code
    Returns
    -------
    result : set
          all For AST nodes
    """
    result = set()
    tree = ast.parse(code)
    for node in ast.walk(tree):
        if isinstance(node, ast.For):
            result.add(node)
    return result


This code uses the `ast` module to parse the given Python code into an abstract syntax tree (AST). It then walks through the tree and adds any `ast.For` nodes it finds to a set. Finally, it returns the set of all `ast.For` nodes.
'''
def instr_1():
    real_instruction = '''
How to extract blocks consisting of several consecutive assignment statements from the a given Python code. Each block whose each statement does not exist in the assigned variables of all statements before this statement.

for example, for the Python code:
event_type = 'ROOT'
event_data = 'example data'
event_module = ''
source_event = ''
evt = SpiderFootEvent(event_type, event_data, event_module, source_event)
result = module.handleEvent(evt)
x = 1
y = 2
z = x + y
a = 'hello'
b = 'world'
c = a + ' ' + b

all consecutive assign nodes:
[[event_type = 'ROOT', event_data = 'example data', event_module = '', source_event = ''],
[x = 1, y = 2],
[a = 'hello', b = 'world']
]
    '''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
def extract_assignment_blocks(code):
    blocks = []
    current_block = []
    assigned_vars = set()

    # Parse the code into an AST
    tree = ast.parse(code)

    # Traverse the AST and extract the assignment statements
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            # Check if all the assigned variables are not used before
            if all(var.id not in assigned_vars for var in node.targets):
                current_block.append(node)
                assigned_vars.update(var.id for var in node.targets)
            else:
                # End the current block and start a new one
                if current_block:
                    blocks.append(current_block)
                    current_block = []
                assigned_vars.clear()

    # Add the last block if it exists
    if current_block:
        blocks.append(current_block)

    # Convert the blocks to a list of lists of assignment statements
    for block in blocks:
        print([ast.unparse(stmt).strip() for stmt in block])
    # return [[ast.unparse(stmt).strip() for stmt in block] for block in blocks]
def extract_block(code):
    # Parse the code into an AST
    tree = ast.parse(code)

    # Initialize variables to keep track of the current block and all blocks
    current_block = []
    all_blocks = []

    # Define a helper function to check if a variable is assigned in a given node
    def is_assigned(node, var):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == var:
                    return True
        return False

    # Traverse the AST and extract the consecutive assignment statements
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            if not current_block or all(
                    is_assigned(prev_node, target.id) for prev_node in current_block for target in node.targets):
                current_block.append(node)
            else:
                all_blocks.append(current_block)
                current_block = [node]

    # Add the last block to the list of all blocks
    if current_block:
        all_blocks.append(current_block)

    # Print the resulting blocks
    for block in all_blocks:
        print([ast.unparse(node).strip() for node in block])
def extract_assignment_blocks_2(code):
    blocks = []
    assigned_vars = set()
    for node in ast.walk(ast.parse(code)):
        if isinstance(node, ast.Assign):
            if all(var.id in assigned_vars for var in node.targets):
                # All variables in this assignment have already been assigned
                # in previous statements, so this is not a new block
                continue
            assigned_vars.update(var.id for var in node.targets)
            block = [ast.unparse(node)]
            while True:
                next_node = next(ast.walk(node), None)
                if not isinstance(next_node, ast.Assign):
                    break
                if all(var.id in assigned_vars for var in next_node.targets):
                    # All variables in this assignment have already been assigned
                    # in previous statements, so this is not part of the current block
                    break
                assigned_vars.update(var.id for var in next_node.targets)
                block.append(ast.unparse(next_node))
                node = next_node
            blocks.append(block)
    return blocks
if __name__ == '__main__':
    # instr_1()
    code = """
event_type = 'ROOT'
event_data = 'example data'
event_module = ''
source_event = ''
evt = SpiderFootEvent(event_type, event_data, event_module, source_event)
result = module.handleEvent(evt)

x = 1
y = 2
z = x + y

a = 'hello'
b = 'world'
c = a + ' ' + b
    """
    blocks = extract_assignment_blocks(code)
    print(blocks)
    # extract_block(code)
    # blocks = extract_assignment_blocks(code)
    # print(blocks)
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
