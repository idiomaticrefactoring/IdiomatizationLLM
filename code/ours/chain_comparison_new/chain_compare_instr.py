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
    #Write Python code to get comparison values for a given Compare node

    real_instruction = '''
Write Python code to map all comparison operands of each comparison operation from a given Bool Node whose op is "And" into one symbol v. And the same comparison operands must be represented by the same symbol. 

for example, 
a given Bool Node is as follows:
a > 1 and c.b is None and a < d + e < c.b[0] + d and d is not None and (c.func(x) or e.b[0] == 1) and d % e > 1

the variable mappings is: 
v1: a
v2: 1
v3: c.b
v4: None
v5: d + e
v6: c.b[0] + d
v7: d
v8: c.func(x)
v9: e.b[0]
v10: d % e

New Python code is:
v1 > v2 and v3 is v4 and v1 < v5 < v6 and v7 is not v4 and (v8 or v9 == v2) and v10 > v2
'''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])

def instr_2():
    #Write Python code to get comparison values for a given Compare node

    real_instruction = '''
Write Python code to extract all two comparison operations from its values that have the same comparison operand from a given Python code whose AST is BoolOp, .

for example, 
a given Python code:
a > 1 and c.b is None and a < d + e < c.b[0] + d and d is not None and (c.func(x) or e.b[0] == 1) and d % e > 1

all two comparison operations and the same comparison operand:
a > 1, a < d + e < c.b[0] + d, 1
c.b is None, d is not None, None
a > 1, d % e > 1, 1
'''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
def instr_3():
    #Write Python code to get comparison values for a given Compare node

    real_instruction = '''
Write Python code to extract comparison nodes from a given AST node set.

for example, 
a given AST node set:
a > 1
c.b is None
a < d + e < c.b[0] + d
(b or c and d)

comparison nodes:
a > 1
c.b is None
a < d + e < c.b[0] + d
'''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])

def extract_comparison_nodes(node_set):
    comparison_nodes = []
    for node in node_set:
        if isinstance(node, ast.Compare):
            comparison_nodes.append(node)
    return comparison_nodes

def instr_4():
    #Write Python code to get comparison values for a given Compare node

    real_instruction = '''
Write Python code to find two comparison nodes that have the same comparison value from a given comparison node set exist. If it has, you give all possibles consisting of the two comparison nodes and the same comparison value.

for example, 
a given comparison node set:
a > 1
c.b is None
a < b < d
w is not None

all possibles:
two comparison nodes: 
a > 1 
a < b < d

the same comparison value: a

two comparison nodes: 
c.b is None
w is not None

the same comparison value: None
'''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])

#a Python code whose AST is BoolOp, you determine whether its values exist two comparison operations that have the same comparison operand.
def get_values(compare_node):
    # Get the left and right values of the comparison
    # Get the left and right values of the comparison
    left_value = ast.unparse(compare_node.left).strip()
    right_value = ast.unparse(compare_node.comparators[0]).strip()

    # Return the comparison values
    return left_value, right_value
def instr_same_operand_for_two_compare():
    #Write Python code to get comparison values for a given Compare node

    real_instruction = '''
Write Python code to check if compare operands of two given compare AST nodes intersect in Python. 

for example, for the given two compare AST nodes: 
c.b is None
w is not None

their all compare operands are respectively:
c.b, None
w, None

So they intersect, the same compare operand is None
'''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])

def instr_get_operands():
    #Write Python code to get comparison values for a given Compare node

    real_instruction = '''
Write Python code to get all compare operands for a given compare AST node.

for example, for the given compare AST node: 
c.b is None

the compare operands are: c.b, None

for another example, for the given compare AST node: 
w is not None

the compare operands are: w, None
'''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
def get_compare_operands(node):
    if isinstance(node, ast.Compare):
        operands = [node.left] + node.comparators
        return operands
    else:
        return None
def instr_get_operands_from_given_code():
    #Write Python code to get comparison values for a given Compare node

    real_instruction = '''
Write Python code to get all compare nodes for a given BoolOp node.

for example, for the BoolOp node: 
a > 1 and c.b is None and a < d + e < c.b[0] + d and d is not None and (c.func(x) or e.b[0] == 1) and d % e > 1

all compare nodes are:
a > 1
c.b is None
a < d + e < c.b[0] + d
d is not None
e.b[0] == 1
d % e > 1
'''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
# Function to get all compare nodes for a given BoolOp node
def instr_get_compare_from_given_code():
    #Write Python code to get comparison values for a given Compare node

    real_instruction = '''
Write Python code to extract list from a given AST node set whose each element is Compare AST node.

for example, a given node set are:
a > 1
c.b is None
a < d + e < c.b[0] + d
d is not None
(c.func(x) or e.b[0] == 1)
d % e > 1
(c or b and e)

since (c.func(x) or e.b[0] == 1), (c or b and e) are not compare nodes, so we remove them. Among the set, the list are:
a > 1
c.b is None
a < d + e < c.b[0] + d
d is not None
d % e > 1
'''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
def extract_compare_nodes(node_set):
    compare_nodes = []
    for node in node_set:
        if isinstance(node, ast.Compare):
            compare_nodes.append(node)
    return compare_nodes

def instr_has_the_same_element():
    #Write Python code to get comparison values for a given Compare node

    real_instruction = '''
Write Python code to check if two lists have common elements in Python
'''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
def has_common_elements(list1,list2):
    common_elements = set(list1).intersection(set(list2))
    return list(common_elements)
    # if common_elements:
    #     return 1
    # else:
    #     return 0
def instr_extract_combinations():
    #Write Python code to get comparison values for a given Compare node

    real_instruction = '''
Write Python code to extract all combinations consisting of two different elements in a given set in Python
'''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
import itertools
def get_combinations(my_set):

    combinations = list(itertools.combinations(my_set, 2))
    return combinations
def get_compare_nodes(node):
    if isinstance(node, ast.BoolOp):
        compare_nodes = []
        for value in node.values:
            compare_nodes.extend(get_compare_nodes(value))
        return compare_nodes
    elif isinstance(node, ast.Compare):
        return [node]
    else:
        return []
def instr_compare_satisfy_one_condition():
    #Write Python code to get comparison values for a given Compare node

    real_instruction = '''
Write Python code to find all two elements of a given compare AST node set whose comparison operands intersect.
'''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
if __name__ == '__main__':
    # instr_1()
    # instr_2()
    # instr_3()
    # instr_4()
    # instr_same_operand_for_two_compare()
    # instr_compare_satisfy_one_condition()
    # instr_get_operands_from_given_code()
    # instr_get_compare_from_given_code()
    # instr_has_the_same_element()
    # instr_extract_combinations()
    # instr_get_operands()
    # instr_3()
    # join_string_instr()
    # is_len_instr()
    # is_len_instr()
    # instr_1()
    print(get_combinations([1,2,3]))
    # compare_node = ast.parse("x > y").body[0].value
    # print("compare_node: ",compare_node)
    # # result = eval(compile(ast.Expression(compare_node), '', 'eval'))
    # left_value,right_value=get_values(compare_node)
    # # print(result)
    # print(left_value,right_value)
