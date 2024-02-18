import ast,chatgpt_util
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

def instr_1():
    real_instruction = '''
We give you a code template, you write Python code to extract all For AST nodes from a given Python code.
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

    '''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])

#We give you a code template, you write Python code to extract all For AST nodes from a given Python code.
def get_for_2(tree):
    result=[]
    for node in ast.walk(tree):
        if isinstance(node, ast.For):
            if node not in result:
                result.append(node)
    return result
def instr_for_no_enumerate():
    real_instruction = '''
Write Python code to determine whether a given for node whose iterated object is an enumerate function or not in Python
    '''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])

'''
Write Python code to determine whether a given for node whose iterated object is an enumerate function or not in Python
'''
def is_enumerate_for(node):
    if isinstance(node, ast.For):
        if isinstance(node.iter, ast.Call) and isinstance(node.iter.func, ast.Name) and node.iter.func.id == 'enumerate':
            return True
    return False

def instr_for_determine_func():
    real_instruction = '''
Write Python code to determine whether a given for node whose iterated object is a function call whose function name is a given string  or not in Python
    '''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
def check_for_loop_a_fun_name(node, function_name):
    if isinstance(node, ast.For):
        if isinstance(node.iter, ast.Call):
            if isinstance(node.iter.func, ast.Name) and node.iter.func.id == function_name:
                return True
    return False
def instr_2():
    real_instruction = '''
Write Python code to extract the last line of code

for example, for the following Python code
for i in a:
    if b:
        a.add(i)  

the last line is: a.add(i)
    '''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
def get_last_line(code):
    last_line = code.strip().split('\n')[-1].strip()
    return last_line
def instr_extract_first_line():
    real_instruction = '''
Write Python code to extract the first line of a given Python code

for example, for the following Python code
for i in a:
    if b:
        a.add(i)  

the first line is: for i in a:
    '''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
def get_first_line(code):
    last_line = code.split('\n')[0]
    return last_line
def instr_fun_name_is_given_string():
    real_instruction = '''
Write Python code to determine whether the function name of a given function call node is a given string, if it is you also extract its corresponding object in Python

for example, for the function call: a.c.add(i), a given string is add
its function name of function call is add, so the function name of the function call is add. And the object is "a.c"
    '''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])

def extract_function_object(code, function_name):
    tree=ast.parse(code)
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if node.func.attr == function_name:
                obj = ast.unparse(node.func.value).strip()
                return obj, node.func.attr
    return None, None

def instr_3():
    real_instruction = '''
Write Python code to check whether the whole Python code is a function call in Python

for example, for the following Python code
a.add(i)

it is a function call

for another example, for the following Python code
a= func(i)

it is an assignment statement and is not a function call
    '''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
def is_function_call_2(code):
    try:
        parsed = ast.parse(code)
        if isinstance(parsed.body[0], ast.Expr) and isinstance(parsed.body[0].value, ast.Call):
            return True
        else:
            return False
    except:
        return False
def instr_whether_is_use_var_2():
    real_instruction = '''
Write Python code to check whether the given Python code from a start line to end line has code string of a given node in Python
    '''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
def instr_whether_is_use_var():
    real_instruction = '''
Write Python code to check whether the given Python code from a start line to end line uses a given object in Python
    '''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
def check_object_usage(code, start_line, end_line, obj_name):
    """
    Check whether the given object is used in the given range of lines in the code.
    :param code: The Python code to check.
    :param start_line: The starting line number (inclusive).
    :param end_line: The ending line number (inclusive).
    :param obj_name: The name of the object to check for usage.
    :return: True if the object is used in the given range of lines, False otherwise.
    """
    lines = code.split('\n')
    for i in range(start_line-1, end_line):
        print(">>>>>>>>i, lines[i]: ",lines[i])
        if obj_name in lines[i]:
            return True
    return False
def instr_extract_code_snippets():
    real_instruction = '''
Write Python code to extract code snippets from a start line to end line of a given Python code in Python
    '''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
def extract_code_snippet(code, start_line, end_line):
    lines = code.split('\n')
    snippet = ''
    for i in range(start_line-1, end_line):
        snippet += lines[i] + '\n'
    return snippet
def instr_get_line_number():
    real_instruction = '''
Write Python code to get the line number of a given code in a given Python code in Python
    '''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
def get_line_number(code, target):
    lines = code.split('\n')
    print("len of lines: ",len(lines))
    line_numbers = []
    for i, line in enumerate(lines):
        if target in line:
            line_numbers.append(i+1)
    return line_numbers

def instr_extract_func_specified_name_from_tree():
    real_instruction = '''
Write Python code to extract AST nodes from a given AST tree that belong to function call whose function name is the given string, if it is you also extract the stmt where the function call is located in Python

'''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
def extract_function_calls_from_tree(tree, function_name):
    function_calls = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == function_name:
            function_calls.append(node)
    return function_calls

def extract_function_call_stmt_from_tree(tree, function_call_node):
    for node in ast.walk(tree):
        if isinstance(node, ast.stmt) and node.lineno == function_call_node.lineno:
            return node
    return None
def instr_extract_func_specified_name():
    real_instruction = '''
Write Python code to extract AST nodes from a given Python code that belong to function call whose function name is the given string, if it is you also extract the stmt where the function call is located in Python

'''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
def extract_function_calls(code, function_name):
    tree = ast.parse(code)
    function_calls = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == function_name:
            function_calls.append(node)
    return function_calls

def instr_stmt_fun_call_is_given_string():
    real_instruction = '''
Write Python code to extract the code block whose body from a given Python code that has a function call node whose function name is a given string is located in Python
For example, for the following Python code, the given string of function name is open
def f():
    for k in a_list:
        f=open("a.txt",'r')
the function call node is open("a.txt",'r'), its code body is:   
for k in a_list:
    f=open("a.txt",'r')
'''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])

def instr_fun_name_is_given_string():
    real_instruction = '''
Write Python code to determine whether the function name of a given function call node is a given string, if it is you also extract its corresponding object in Python

for example, for the function call: a.c.add(i), a given string is add
its function name of function call is add, so the function name of the function call is add. And the object is "a.c"
    '''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])

def extract_function_object(code, function_name):
    tree=ast.parse(code)
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if node.func.attr == function_name:
                obj = ast.unparse(node.func.value).strip()
                return obj, node.func.attr
    return None, None

def instr_code_start_line():
    real_instruction = '''
Write Python code to extract code that starts from a given line number including the line number from the body of a given Python AST tree in Python
'''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
def extract_code_from_line(code, start_line):
    lines = code.split('\n')
    extracted_code = ''
    for i, line in enumerate(lines):
        if i + 1 >= start_line:
            extracted_code += f'{i+1}: {line}\n'
    return extracted_code
def instr_code_before_line():
    real_instruction = '''
Write Python code to extract code before a given line number including the line number from a given Python code in Python
'''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
def extract_code_before_line_number(code, line_number):
    lines = code.split('\n')
    if line_number > len(lines):
        return code
    else:
        return '\n'.join(lines[:line_number])

def instr_find_assign():
    real_instruction = '''
Write Python code to extract assignment statement whose a target string (an identifier, attribute reference, subscription or slicing) is a given string in a given Python code

for example, for the given Python code
expected_ids.c = []
limit = 10
for _ in range(limit):
    expected_ids.c.append(create_test_directory(client, ec2_client))
    
a given string is expected_ids.c

the assignment statement is expected_ids.c = [] whose target is expected_ids.c
'''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
def instr_is_assign():
    real_instruction = '''
Write Python code to check whether the whole Python code is a assignment statement in Python

for example, for the following Python code
a[i] =k

it is a assignment statement

for another example, for the following Python code
a.append(func(i=1))

it is a function call and is not a assignment statement
    '''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])

def is_assignment(code):
    try:
        tree = ast.parse(code)
        return isinstance(tree.body[0], ast.Assign)
    except:
        return False

def instr_is_target_subscript_assign():
    real_instruction = '''
Write Python code to determine whether the target of a given assignment statement is a subscript. If the target is a subscript, you also extract its value.

for example, for the assignment statement
a.c[i] =k

the target is a.c[i] whose is a subscript. And its value is a.c.
    '''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])


def extract_subscript_value(assignment_statement):
    """
    Given an assignment statement, determine whether the target is a subscript and extract its value.
    """
    # Parse the assignment statement into an AST
    tree = ast.parse(assignment_statement)

    # Get the target of the assignment
    target = tree.body[0].targets[0]

    # Check if the target is a subscript
    if isinstance(target, ast.Subscript):
        # Extract the value of the subscript
        value = ast.unparse(target.value).strip()
        return value
    else:
        return None
def instr_subscript_value_from_subscript():
    real_instruction = '''
Write Python code to check whether a given Python code is a subscript node. If it is, please also extract value of a subscript.

for example
for the code c[i][j], its value is c[i]
for the code c[i], its value is c
    '''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
def extract_subscript_value_from_whole_code(code):
    """
    Extract the value of a subscript node.
    """
    node = ast.parse(code).body[0].value
    if isinstance(node, ast.Subscript):
        value = ast.unparse(node.value).strip()
        return value
    else:
        return None
def is_function_call_2(code):
    try:
        parsed = ast.parse(code)
        if isinstance(parsed.body[0], ast.Expr) and isinstance(parsed.body[0].value, ast.Call):
            return True
        else:
            return False
    except:
        return False
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
def instr_all_consec_ass():
    real_instruction = '''
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
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])

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

def instr_all_consec_ass_constant():
    real_instruction = '''
For a given list consisting of several Assign AST nodes, write Python code to group all Assign AST nodes where all values of Assign AST nodes of each group are same constant value in Python
for example, for the list:
[a = 1, self.c = w, b = "2", c=1, d="2"]

all groups:
[[a=1, c=1],
[b = "2",d="2"]
]
    '''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])


def group_assign_nodes(assign_nodes):
    from ast import Assign, Constant
    groups = []
    for node in assign_nodes:
        if isinstance(node.value, Constant):
            # Check if there is a group with the same constant value
            for group in groups:
                if all(isinstance(n.value, Constant) and n.value.value == node.value.value for n in group):
                    print("group: ",node.value.value,[n.value.value for n in group],[isinstance(n.value, Constant) and n.value.value == node.value.value for n in group])
                    group.append(node)
                    break
            else:
                # Create a new group
                groups.append([node])
    return groups

def instr_all_ass_constant_consecutive():
    real_instruction = '''
For a given list consisting of several Assign AST nodes, write Python code to group all consecutive Assign AST nodes where all values of each group are constant AST nodes and their values are same in Python
for example, for the list:
[a = 1, self.c = w, b = "2", d="2", c=None, d=None, w=s, f=s]

all consecutive Assign AST nodes:
[[b = "2",d="2"],
[c=None, d=None]
]
    '''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])

def group_consecutive_assign_nodes(assign_nodes):
    groups = []
    current_group = []
    for node in assign_nodes:
        if isinstance(node.value, ast.Constant):
            if not current_group or (current_group and current_group[-1].value.value is node.value.value):
                current_group.append(node)
            else:
                groups.append(current_group)
                current_group = [node]
        else:
            if current_group:
                groups.append(current_group)
                current_group = []
    if current_group:
        groups.append(current_group)
    return [group for group in groups if len(group) > 1]
def group_constant_assignments(assignments):
    groups = []
    current_group = []
    current_value = None

    for assign in assignments:
        if isinstance(assign.value, ast.Constant):
            if current_value is None:
                current_value = assign.value.value
                current_group.append(assign)
            elif assign.value.value is current_value:
                current_group.append(assign)
            else:
                groups.append(current_group)
                current_group = [assign]
                current_value = assign.value.value
        else:
            if current_group:
                groups.append(current_group)
                current_group = []
                current_value = None

    if current_group:
        groups.append(current_group)

    return groups
def find_constant_groups(assign_nodes):
    groups = []
    current_group = []
    current_value = None

    for node in assign_nodes:
        if isinstance(node.value, ast.Constant):
            value = node.value.value
        else:
            value = None

        if value is current_value:
            current_group.append(node)
        else:
            if len(current_group) > 1:
                groups.append(current_group)
            current_group = [node]
            current_value = value

    if len(current_group) > 1:
        groups.append(current_group)

    return groups
# def find_consecutive_assign_nodes(lst):
#     result = []
#     i = 0
#     while i < len(lst):
#         if isinstance(lst[i], ast.Assign):
#             j = i + 1
#             while j < len(lst) and isinstance(lst[j], ast.Assign):
#                 if ast.dump(lst[i].value) == ast.dump(lst[j].value):
#                     j += 1
#                 else:
#                     break
#             if j - i > 1:
#                 result.append(lst[i:j])
#             i = j
#         else:
#             i += 1
#     return result
def instr_all_ass_constant_consecutive_simply():
    real_instruction = '''
For a given list whose each element is a Assign AST nodes, write Python code to extract consecutive Assign AST nodes whose all values are constant AST nodes and constant values are same in Python
for example, for the list:
[a = 1, self.c = w, b = "2", d="2", c=None, d=None, w=s, f=s]

all consecutive Assign AST nodes whose all values are constant AST nodes and constant values are same:
[b = "2",d="2"],
[c=None, d=None]
    '''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
def extract_consecutive_assign_nodes(lst):
    result = []
    temp = []
    for node in lst:
        if isinstance(node, ast.Assign):
            if all(isinstance(value, ast.Constant) for value in node.value) and len(set(value.value for value in node.value)) == 1:
                temp.append(node)
            else:
                if len(temp) > 1:
                    result.append(temp)
                temp = []
        else:
            if len(temp) > 1:
                result.append(temp)
            temp = []
    if len(temp) > 1:
        result.append(temp)
def extract_consecutive_assign_nodes_simplify(lst):
    result = []
    i = 0
    while i < len(lst):
        if isinstance(lst[i], ast.Assign) and isinstance(lst[i].value, ast.Constant):
            constant_value = lst[i].value.value
            j = i + 1
            while j < len(lst) and isinstance(lst[j], ast.Assign) and isinstance(lst[j].value, ast.Constant) and lst[j].value.value is constant_value:
                j += 1
            if j - i > 1:
                result.append(lst[i:j])
            i = j
        else:
            i += 1
    return result

def instr_all_ass_sunscript_simply():
    real_instruction = '''
For a given list whose each element is a Assign AST nodes, write Python code to extract consecutive Assign AST nodes whose all values are Subscript nodes and their values are the same iterable object in Python
for example, for the list:
[a = 1, self.c = w[0], b = w[2], d="2", c=self.a[1], d=self.a[2], e=self.a[3:]]

all consecutive Assign AST nodes whose all values are Subscript nodes and their values are the same iterable object
[self.c = w[0], b = w[2]],
[c=self.a[1], d=self.a[2], e=self.a[3:]]
    '''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])

import astor
def extract_subscript_assignments(assignments):
    result = []
    current_iterable = None
    current_subscript_assignments = []

    for assignment in assignments:
        if isinstance(assignment.value, ast.Subscript):
            if current_iterable is None:
                current_iterable = astor.to_source(assignment.value.value).strip()
                current_subscript_assignments.append(assignment)
            elif astor.to_source(assignment.value.value).strip() == current_iterable:
                current_subscript_assignments.append(assignment)
            else:
                if len(current_subscript_assignments) > 1:
                    result.append(current_subscript_assignments)
                current_iterable = astor.to_source(assignment.value.value).strip()
                current_subscript_assignments = [assignment]
        else:
            if len(current_subscript_assignments) > 1:
                result.append(current_subscript_assignments)
            current_iterable = None
            current_subscript_assignments = []

    if len(current_subscript_assignments) > 1:
        result.append(current_subscript_assignments)

    return result

def instr_find_FormattedValue():
    real_instruction = '''
Write Python function code to extract all old formatted string AST nodes from a given Python tree.

for example, for the given Python tree:
print("The quick brown %s jumped over the lazy sleeping %s" % (animal_one, animal_two))

all old formatted string codes are as follows:
The quick brown %s jumped over the lazy sleeping %s" % (animal_one, animal_two)'''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])

def extract_old_formatted_strings_new(tree):
    old_formatted_strings = []
    for node in ast.walk(tree):
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Mod):
            old_formatted_strings.append(node)
    return old_formatted_strings
'''
Write Python function code to extract all FormattedValue nodes from a given Python code.

for example, for the given Python code:
print("The quick brown %s jumped over the lazy sleeping %s" % (animal_one, animal_two))

all FormattedValue nodes are as follows:
The quick brown %s jumped over the lazy sleeping %s" % (animal_one, animal_two)
    '''
def extract_formatted_values(code):
    formatted_values = []
    tree = ast.parse(code)
    for node in ast.walk(tree):
        if isinstance(node, ast.FormattedValue):
            formatted_values.append(ast.get_source_segment(code, node))
    return formatted_values
'''
Write Python function code to extract all old formatted strings AST nodes from a given Python tree.

for example, for the given Python tree:
print("The quick brown %s jumped over the lazy sleeping %s" % (animal_one, animal_two))

all old formatted strings AST nodes are as follows:
The quick brown %s jumped over the lazy sleeping %s" % (animal_one, animal_two)'''
def extract_old_formatted_strings(tree):
    old_formatted_strings = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'format':
            continue
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Mod):
            old_formatted_strings.append(ast.get_source_segment(tree, node))
    return old_formatted_strings
def extract_formatted_values(tree):
    formatted_values = []

    class FormattedValueVisitor(ast.NodeVisitor):
        def visit_FormattedValue(self, node):
            formatted_values.append(node)

    visitor = FormattedValueVisitor()
    visitor.visit(tree)

    return formatted_values

def instr_replace_iter_for():
    real_instruction = '''
Write Python function code to replace the iter of a given For AST node with a given string in Python.

for example, a given For AST node is:
for i in range(len(S_m)):
    S_m[i] = S_m[i].subs(x, sym.sin(theta) * sym.cos(phi)).subs(y, sym.sin(theta) * sym.sin(phi))
 a given string is "zj_list",
 
so the new code is:
for i in zj_list:
    S_m[i] = S_m[i].subs(x, sym.sin(theta) * sym.cos(phi)).subs(y, sym.sin(theta) * sym.sin(phi))
'''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
def replace_for_iter(node, new_iter):
    if isinstance(node, ast.For):
        node.iter = ast.parse(new_iter).body[0].value
    return node


def instr_replace_target_for():
    real_instruction = '''
Write Python function code to replace a given attribute node of a given For AST node with a given string in Python.

for example, a given For AST node is:
for i,val in enumerate(S_m):
    S_m[i] = S_m[i].subs(x, sym.sin(theta) * sym.cos(phi)).subs(y, sym.sin(theta) * sym.sin(phi))

a given attribute is: "target"

a given string is: "ind, val"

so the new code is:
for ind, val in enumerate(S_m):
    S_m[i] = S_m[i].subs(x, sym.sin(theta) * sym.cos(phi)).subs(y, sym.sin(theta) * sym.sin(phi))
'''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])


def replace_for_iter(node, new_iter):
    if isinstance(node, ast.For):
        node.iter = ast.parse(new_iter).body[0].value
    return node
def replace_for_target(for_node, target, new_target):
    """
    Replace the target of a given For AST node with a given string.

    Args:
        for_node (ast.For): The For AST node to modify.
        target (str): The target to replace.
        new_target (str): The new target to use.

    Returns:
        ast.For: The modified For AST node.
    """
    # Convert the target and new_target strings to AST nodes.
    target_node = ast.parse(target).body[0].value
    new_target_node = ast.parse(new_target).body[0].value

    # Replace the target in the For node with the new target.
    for_node.target = new_target_node

    # Walk the AST and replace any occurrences of the old target with the new target.
    class TargetReplacer(ast.NodeTransformer):
        def visit_Name(self, node):
            if node.id == target_node.id:
                return new_target_node
            return node

    transformer = TargetReplacer()
    new_for_node = transformer.visit(for_node)

    return new_for_node
def instr_extract_call_node():
    real_instruction = '''
Write Python code to extract all Call AST nodes from a given Python code.
    '''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])

if __name__ == '__main__':
    instr_extract_call_node()
    # instr_whether_is_use_var()
    # instr_extract_code_snippets()
    # instr_get_line_number()
    # instr_whether_is_use_var()
    # instr_whether_is_use_var_2()
    # instr_find_assign()
    # instr_is_assign()
    # instr_is_target_subscript_assign()
    # instr_subscript_value_from_subscript()
    # instr_extract_func_specified_name()
    # instr_stmt_fun_call_is_given_string()
    # instr_extract_func_specified_name_from_tree()
    # instr_code_start_line()
    # instr_1()
    # instr_extract_first_line()
    # instr_for_determine_func()
    # instr_all_consec_ass()
    # instr_all_consec_ass_constant()
    # instr_all_consec_ass_constant()
    # instr_all_ass_constant_consecutive()
    # instr_all_ass_constant_consecutive_simply()
    # instr_all_ass_sunscript_simply()
    # instr_find_FormattedValue()
    # instr_replace_iter_for()
    # instr_replace_target_for()
    code_str = """
expected_ids.c = []
limit = 10
for _ in range(limit):
    expected_ids.c.append(create_test_directory(client, ec2_client))
    """
    code='''
c[i]
    '''
    '''
    value = extract_subscript_value_from_whole_code(code)
    print(value)
    def is_assignment(code):
        try:
            tree = ast.parse(code)
            return isinstance(tree.body[0], ast.Assign)
        except:
            return False


    code1 = "a[i] = k"
    code2 = "a.append(func(i=1))"

    print(is_assignment(code1))  # True
    print(is_assignment(code2))  # False

    target_str = "expected_ids.c"
    '''
    code='''
a = 1
self.c = w
b = "2"
c=1
d="2"  
e=5
self.b=5  
self._env_step_counter = 0
self._cam_roll = 0
self.terminated = False
self.debug = False
self.n_contacts = 0
self.n_steps_outside = 0
data = None
downloaded_file = None
data = None
count = False
self._last_progress_updated = 0.0
(seconds, microseconds, type, code, value) = struct.unpack(event_bin_format, data)
c=d
g=d
    '''
    # assign_nodes = []
    # for node in ast.walk(ast.parse(code)):
    #     if isinstance(node,ast.Assign):
    #         assign_nodes.append(node)

    # groups=group_assign_nodes(assign_nodes)
    # groups=find_constant_groups(assign_nodes)
    # groups=find_consecutive_assign_nodes(assign_nodes)
    # groups=group_constant_assignments(assign_nodes)
    # groups=group_consecutive_assign_nodes(assign_nodes)
    # groups=extract_consecutive_assign_nodes(assign_nodes)
    # groups=extract_consecutive_assign_nodes_simplify(assign_nodes)


    # for each in groups:
    #     print(">>>>>>>")
    #     for e in each:
    #         print("ass: ",ast.unparse(e))
    code = '''
a=0
b=0
x = 1
self.c = w
a=0.0
b=0.0
b = a[0]
c= a[1]
b = self.b[0]
c= self.b[1:]
self.num_imgs = 0
self.images = []
a=0.0
b=0.0
  '''
    assign_nodes=[]
    for node in ast.walk(ast.parse(code)):
        if isinstance(node, ast.Assign):
            assign_nodes.append(node)
            if isinstance(node.value,ast.Constant):
                print(node.value.value)
    groups = group_consecutive_assign_nodes(assign_nodes)

    # groups=extract_subscript_assignments(assign_nodes)
    for each in groups:
        print(">>>>>>>")
        for e in each:
            print("ass: ",ast.unparse(e))
#     tree=''''Hello, %s' % name
# print("The quick brown %s jumped over the lazy sleeping %s" % (animal_one, animal_two))
#     '''
#     # for node in ast.walk(ast.parse(tree)):
#     #     print("node: ",node)
#     res_list=extract_formatted_values(ast.parse(tree))
#     res_list=extract_old_formatted_strings_new(ast.parse(tree))
#     print("res_list: ",res_list)
#     for e in res_list:
#         print("format value: ",ast.unparse(e))
    # def extract_assignment_statement(code_str, target_str):
    #     tree = ast.parse(code_str)
    #     for node in ast.walk(tree):
    #         if isinstance(node, ast.Assign):
    #             for target in node.targets:
    #                 print(ast.dump(target))
    #                 if target_str in ast.dump(target):
    #                     return ast.unparse(node).strip()
    #     return None
    # assignment_statement = extract_assignment_statement(code_str, target_str)
    #
    # print(assignment_statement)
