import os,sys
import struct
import traceback
code_dir = "/".join(os.path.abspath(__file__).split("/")[:-2]) + "/"
print("code path: ",code_dir)
sys.path.append(code_dir)
import chatgpt_util,random
import openai, tiktoken,ast,util
import ast,code_determine_use_preceding_vars,code_determine_contain
'''
Write Python code to find all Name AST nodes of targets of assignment statements of a given Python code.

for example, for the Python code:
a.imag = 9
res = a.execute().fetch()
c, d[0] = d

targets of assignment statements are: a.imag, res, c, d[0]
so all Name AST nodes of targets of assignment statements are: {a, res, c, d}
'''
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



'''
Write Python code to determine whether a variable set intersects with another variable set
'''
def check_variable_intersection(assignment_set, variable_set):
    if assignment_set.intersection(variable_set):
        return True
    else:
        return False
'''
Write Python code to get all Name AST nodes from a given Python code.
'''
def get_names(code):
    tree = ast.parse(code)

    names = [node.id for node in ast.walk(tree) if isinstance(node, ast.Name)]
    return set(names)
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
def get_blocks_no_depdend(code):
    code_list = code.strip().split("\n")
    all_blocks = []
    for i, ass1 in enumerate(code_list[:-1]):
        pre_blocks = [ass1]
        for j, ass2 in enumerate(code_list[i + 1:]):
            pre_code = "\n".join(pre_blocks)
            assignment_set = get_names(ass2)
            variable_set = get_names_from_targets(pre_code)
            if check_variable_intersection(assignment_set, variable_set):
                if len(pre_blocks)>1:
                    all_blocks.append(pre_code)
                break
            else:
                pre_blocks.append(ass2)
        else:
            pre_code = "\n".join(pre_blocks)
            if len(pre_blocks)>1 and pre_code not in all_blocks:
                all_blocks.append(pre_code)
    # for e in all_blocks:
    #     print("e: ", e)

    new_blocks = remove_substrings(all_blocks)
    # print(new_blocks)
    return new_blocks

def get_blocks_no_depdend_2(code):
    code_list = code.strip().split("\n")
    all_blocks = []
    for i, ass1 in enumerate(code_list[:-1]):
        pre_blocks = [ass1]
        for j, ass2 in enumerate(code_list[i + 1:]):
            pre_code = "\n".join(pre_blocks)
            for node in ast.walk(ast.parse(ass2)):
                if isinstance(node, ast.Assign):
                    value=node.value
                    break
            assignment_set=get_names(ast.unparse(value))
            variable_set = get_names_from_targets(pre_code)
            if check_variable_intersection(assignment_set, variable_set):
                if len(pre_blocks)>1:
                    all_blocks.append(pre_code)
                break
            else:
                pre_blocks.append(ass2)
        else:
            pre_code = "\n".join(pre_blocks)
            if len(pre_blocks)>1 and pre_code not in all_blocks:
                all_blocks.append(pre_code)
    # for e in all_blocks:
    #     print("e: ", e)

    new_blocks = remove_substrings(all_blocks)
    # print(new_blocks)
    return new_blocks
'''
How to know the number of elements and extract elements's nodes of an Tuple AST node in Python

for examples, 
for the tuple x, y, all elements are x, y, so the number is 2
for the tuple  ((a, b[0]), w.c), c, all elements are c, b[0], a, w.c, so the number is 4
'''
def extract_nodes(node):
    nodes = []
    if isinstance(node, tuple):
        for element in node:
            nodes.extend(extract_nodes(element))
    else:
        nodes.append(node)
    return nodes
def extract_ass_targets(pre_code):
    target_list = []
    for node in ast.walk(ast.parse(pre_code)):
        if isinstance(node, ast.Assign):
            target_list.append(node.targets)
            # break
    return target_list
def extract_data_from_ass_targets(pre_code):
    target_list=extract_ass_targets(pre_code)
    data_list=[]
    for tar in target_list:
        data_list.extend(extract_nodes(tar))
    return set([ast.unparse(data) for data in data_list])
def get_blocks_no_depdend_3(code):
    code_list = code.strip().split("\n")
    all_blocks = []
    for i, ass1 in enumerate(code_list[:-1]):
        pre_blocks = [ass1]
        for j, ass2 in enumerate(code_list[i + 1:]):
            pre_code = "\n".join(pre_blocks)
            for node in ast.walk(ast.parse(ass2)):
                if isinstance(node, ast.Assign):
                    value=node.value
                    tar=node.targets
                    break

            assignment_set=get_names(ast.unparse(value))
            tar_set = get_names(ast.unparse(tar))
            tar_pre_set=extract_data_from_ass_targets(pre_code)

            variable_set = get_names_from_targets(pre_code)
            if check_variable_intersection(assignment_set, variable_set) or check_variable_intersection(tar_set, tar_pre_set):
                if len(pre_blocks)>1:
                    all_blocks.append(pre_code)
                break
            else:
                pre_blocks.append(ass2)
        else:
            pre_code = "\n".join(pre_blocks)
            if len(pre_blocks)>1 and pre_code not in all_blocks:
                all_blocks.append(pre_code)
    # for e in all_blocks:
    #     print("e: ", e)

    new_blocks = remove_substrings(all_blocks)
    # print(new_blocks)
    return new_blocks
if __name__ == '__main__':
    code='''
event_type = 'ROOT'
event_data = 'example data'
event_module = ''
source_event = ''
evt = SpiderFootEvent(event_type, event_data, event_module, source_event)
result = module.handleEvent(evt)    
    '''
    code_list=code.strip().split("\n")
    all_blocks=[]
    for i, ass1 in enumerate(code_list[:-1]):
        pre_blocks=[ass1]
        for j, ass2 in enumerate(code_list[i+1:]):
            pre_code="\n".join(pre_blocks)
            for node in ast.walk(ast.parse(ass2)):
                if isinstance(node, ast.Assign):
                    value=node.value
            assignment_set=code_determine_use_preceding_vars.get_names(ast.unparse(value))
            variable_set=code_determine_use_preceding_vars.get_names_from_targets(pre_code)
            if code_determine_use_preceding_vars.check_variable_intersection(assignment_set, variable_set):
                all_blocks.append(pre_code)
                break
            else:
                pre_blocks.append(ass2)
    for e in all_blocks:
        print("e: ",e)

    new_blocks=code_determine_contain.remove_substrings(all_blocks)
    print(new_blocks)

    pass