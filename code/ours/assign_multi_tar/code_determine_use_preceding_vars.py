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

def instr_1():
    real_instruction = '''
Write Python code to determine whether an assignment statement uses the variable names of a set.
'''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
def get_all_Name_from_target(code):
    tree = ast.parse(code)
    name_nodes = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    name_nodes.add(target.id)
    return name_nodes
def get_all_Name_from_target_2(code):
    tree = ast.parse(code)

    # Define a function to recursively search for Name nodes in the AST
    def find_names(node):
        if isinstance(node, ast.Name):
            return {node.id}
        elif isinstance(node, ast.Attribute):
            return find_names(node.value)
        elif isinstance(node, ast.Subscript):
            return find_names(node.value)
        elif isinstance(node, ast.Tuple):
            names = set()
            for elt in node.elts:
                names |= find_names(elt)
            return names
        elif isinstance(node, ast.List):
            names = set()
            for elt in node.elts:
                names |= find_names(elt)
            return names
        elif isinstance(node, ast.Dict):
            names = set()
            for key, value in zip(node.keys, node.values):
                names |= find_names(key)
                names |= find_names(value)
            return names
        else:
            names = set()
            for child in ast.iter_child_nodes(node):
                names |= find_names(child)
            return names

    # Find all Name nodes in the targets of assignment statements
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                names |= find_names(target)

    print(names)
    return names
def instr_name_from_targets():
    real_instruction = '''
Write Python code to find all Name AST nodes of targets of assignment statements of a given Python code.

for example, for the Python code:
a.imag = 9
res = a.execute().fetch()
c, d[0] = d

targets of assignment statements are: a.imag, res, c, d[0]
so all Name AST nodes of targets of assignment statements are: {a, res, c, d}
'''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
def instr_name_all_targets():
    real_instruction = '''
How to know the number of elements and extract elements's nodes of an Tuple AST node in Python

for examples, 
for the tuple x, y, all elements are x, y, so the number is 2
for the tuple  ((a, b[0]), w.c), c, all elements are c, b[0], a, w.c, so the number is 4
'''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
def instr_targets_2():
    real_instruction = '''
How to extract targets AST node of all assignment statements of a given Python code in Python
for example, for the Python code:
x, y=a
((a, b[0]), w.c), c =d

targets AST node
[x, y,
((a, b[0]), w.c), c]
'''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])

def instr_name():
    real_instruction = '''
Write Python code to get all Name AST nodes from a given Python code.
'''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
def instr_targets():
    real_instruction = '''
Write Python code to get all targets of assignment statements from a given Python code.
for example, for the Python code:
a.imag = 9
res = a.execute().fetch()

the targets are [a.imag, res]
'''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
def instr_4():
    real_instruction = '''
Write Python code to get all variables of targets of assignment statements of a given Python code.

for example, for the Python code:
a.imag = 9
res = a.execute().fetch()

the targets are: a.imag, res
so variables are: {a, res}
'''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
def instr_var_intersect():
    real_instruction = '''
Write Python code to determine whether a variable set intersects with another variable set
'''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])

def instr_3():
    real_instruction = '''
Write Python code to determine whether the variable set of an assignment statement intersects with a variable set

for example, 
for the assignment statment: res = a.execute().fetch(), its variable set is {res, a}, a variable set: {a, 9}
the assignment contains one variable a in the set {a, 9}
'''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
def instr_5():
    real_instruction = '''
Write Python code to determine whether an assignment statement uses elements of a variable set

for example, 
for the assignment statment: res = a.execute().fetch(),a variable set: {a, 9}
the assignment contains one variable a in the set {a, 9}
'''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])

def extract_consecutive_ass(code):
    tree = ast.parse(code)

    consecutive_assigns = []
    prev_assign = None

    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            if prev_assign is not None:
                consecutive_assigns.append([prev_assign, node])
            prev_assign = node
    return consecutive_assigns
def check_variable_intersection(assignment_set, variable_set):
    return bool(assignment_set.intersection(variable_set))
def get_names(code):
    tree = ast.parse(code)

    names = [node.id for node in ast.walk(tree) if isinstance(node, ast.Name)]
    return set(names)
def get_names_from_targets(code):
    tree = ast.parse(code)

    # Define a function to recursively find all Name nodes in the AST
    def find_names(node):
        if isinstance(node, ast.Name):
            return {node.id}
        elif isinstance(node, ast.Attribute):
            return find_names(node.value)
        elif isinstance(node, ast.Subscript):
            return find_names(node.value)
        elif isinstance(node, ast.Tuple):
            names = set()
            for elt in node.elts:
                names |= find_names(elt)
            return names
        else:
            names = set()
            for child in ast.iter_child_nodes(node):
                names |= find_names(child)
            return names

    # Find all Name nodes of targets of assignment statements
    targets = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                targets |= find_names(target)
    return targets
if __name__ == '__main__':
    # instr_1()
    # instr_2()
    # instr_3()
    # instr_2()
    # instr_name()
    # instr_targets()
    # instr_name_from_targets()
    # instr_5()
    # instr_4()
    code = """
a = 1
b = 2
c = 3
d=a
    """
    # instr_name_all_targets()
    instr_targets_2()
    # instr_var_intersect()
    import ast

    code = """
a.imag = 9
res = a.execute().fetch()
    """
    # code = """
    # ((c,self.a), w), e = d
    # self.c = b
    # """
    '''
    # Parse the code into an abstract syntax tree (AST)
    tree = ast.parse(code)


    # Define a function to recursively traverse the AST and find all assigned data
    def find_assigned_data(node):
        assigned_data = []
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    assigned_data.append(target.id)
                elif isinstance(target, ast.Tuple):
                    assigned_data.extend(find_assigned_data(target))
        elif isinstance(node, ast.AugAssign):
            if isinstance(node.target, ast.Name):
                assigned_data.append(node.target.id)
        elif isinstance(node, ast.For):
            assigned_data.extend(find_assigned_data(node.target))
        elif isinstance(node, ast.With):
            assigned_data.extend(find_assigned_data(node.optional_vars))
        elif isinstance(node, ast.FunctionDef):
            for arg in node.args.args:
                assigned_data.append(arg.arg)
        elif isinstance(node, ast.ClassDef):
            pass
        elif isinstance(node, ast.If):
            assigned_data.extend(find_assigned_data(node.test))
        elif isinstance(node, ast.While):
            assigned_data.extend(find_assigned_data(node.test))
        elif isinstance(node, ast.Try):
            for handler in node.handlers:
                assigned_data.extend(find_assigned_data(handler))
        elif isinstance(node, ast.ExceptHandler):
            if node.name:
                assigned_data.append(node.name)
        elif isinstance(node, ast.WithItem):
            assigned_data.extend(find_assigned_data(node.context_expr))
        elif isinstance(node, ast.Global):
            assigned_data.extend(node.names)
        elif isinstance(node, ast.Nonlocal):
            assigned_data.extend(node.names)
        elif isinstance(node, ast.Expr):
            pass
        elif isinstance(node, ast.Pass):
            pass
        elif isinstance(node, ast.Break):
            pass
        elif isinstance(node, ast.Continue):
            pass
        elif isinstance(node, ast.Return):
            pass
        elif isinstance(node, ast.Delete):
            pass
        elif isinstance(node, ast.Assert):
            pass
        elif isinstance(node, ast.Import):
            pass
        elif isinstance(node, ast.ImportFrom):
            pass
        elif isinstance(node, ast.alias):
            pass
        elif isinstance(node, ast.Raise):
            pass
        elif isinstance(node, ast.TryFinally):
            pass
        elif isinstance(node, ast.TryExcept):
            pass
        elif isinstance(node, ast.arguments):
            pass
        elif isinstance(node, ast.arg):
            pass
        elif isinstance(node, ast.Name):
            pass
        elif isinstance(node, ast.Num):
            pass
        elif isinstance(node, ast.Str):
            pass
        elif isinstance(node, ast.Bytes):
            pass
        elif isinstance(node, ast.List):
            for item in node.elts:
                assigned_data.extend(find_assigned_data(item))
        elif isinstance(node, ast.Tuple):
            for item in node.elts:
                assigned_data.extend(find_assigned_data(item))
        elif isinstance(node, ast.Set):
            for item in node.elts:
                assigned_data.extend(find_assigned_data(item))
        elif isinstance(node, ast.Dict):
            for key, value in zip(node.keys, node.values):
                assigned_data.extend(find_assigned_data(key))
                assigned_data.extend(find_assigned_data(value))
        elif isinstance(node, ast.Ellipsis):
            pass
        elif isinstance(node, ast.Slice):
            pass
        elif isinstance(node, ast.ExtSlice):
            pass
        elif isinstance(node, ast.Index):
            pass
        else:
            raise ValueError(f"Unknown node type: {type(node)}")
        return assigned_data


    # Traverse the AST and find all assigned data
    assigned_data = []
    for node in ast.walk(tree):
        assigned_data.extend(find_assigned_data(node))

    # Print the assigned data
    print(assigned_data)
    '''
    # result=get_all_Name_from_target(code)
    # print("result: ",result)
    # Parse the code into an AST

    # print(has_data_dependency(code))  # True
    #
    # code1 = "x = 1\ny = x + 2"
    # code2 = "x = 1\ny = x\nz = y"
    #
    # print(has_data_dependency(code1))  # True
    # print(has_data_dependency(code2))  # False
    # flag=has_data_dependency(code)
    # print("flag: ",flag)
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
