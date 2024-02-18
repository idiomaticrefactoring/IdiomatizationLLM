'''
We give you a code template, you write Python code to extract all Call AST nodes from a given Python code.
def get_for(code):
    """
    extract all For AST nodes

    Parameters
    ----------
    code : string
        a Python code
    Returns
    -------
    result : list
          all For AST nodes, please do not have the same element more than once
    """
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

def get_for_2(code):
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
    result = []
    tree = ast.parse(code)
    for node in ast.walk(tree):
        if isinstance(node, ast.For):
            if node not in result:
                result.append(node)
    return result
'''
Python code:
def __init__(self, ref, snapshot, ignore_device=False):
        created = snapshot.paths - ref.paths
        deleted = ref.paths - snapshot.paths

        if ignore_device:
            def get_inode(directory, full_path):
                return directory.inode(full_path)[0]
        else:
            def get_inode(directory, full_path):
                return directory.inode(full_path)

        # check that all unchanged paths have the same inode
        for path in ref.paths & snapshot.paths:
            if get_inode(ref, path) != get_inode(snapshot, path):
                created.add(path)
                deleted.add(path)
                
a given node:
deleted.add(path)
def __init__(self, command_loader=None, help_file_entries=None, loaded_help=None):
        self._all_yaml_help = help_file_entries
        self._loaded_help = loaded_help
        self._command_loader = command_loader
        self._parameters = {}
        self._help_file_entries = set(help_file_entries.keys())
        self._command_parser = command_loader.cli_ctx.invocation.parser
        for command_name, command in self._command_loader.command_table.items():
            self._parameters[command_name] = set()
            for name, param in command.arguments.items():
                self._parameters[command_name].add(name)
                            
a given node:
self._parameters[command_name].add(name)             
'''
def instr_cfg():
    real_instruction = '''Determine the assignment statement of self._parameters[command_name] that reach a given node of the following Python code in Python.

Python code:
def __init__(self, command_loader=None, help_file_entries=None, loaded_help=None):
        self._all_yaml_help = help_file_entries
        self._loaded_help = loaded_help
        self._command_loader = command_loader
        self._parameters = {}
        self._help_file_entries = set(help_file_entries.keys())
        self._command_parser = command_loader.cli_ctx.invocation.parser
        for command_name, command in self._command_loader.command_table.items():
            self._parameters[command_name] = set()
            for name, param in command.arguments.items():
                self._parameters[command_name].add(name)
                            
a given node:
self._parameters[command_name].add(name) 

response format:
Answer: You respond with Yes or No for whether there is a statement statement that reach a statement of a given Python code.
Information: If your answer is Yes, you give the assignment statement. Otherwise, you respond with None. Please explain it.
   
for example, for the following Python code:
graph = {}
for u in self.complete:
    graph[u] = set()
    for v in self.complete[u]:
        if u != v:  # ignore self-loop
            graph[u].add(v)
        else:
            graph[u] = c
            
for the node: graph[u].add(v)

the response is as follows:
Answer: Yes
Information: graph[u] = set()
    '''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])

if __name__ == '__main__':
    # instr_1()
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
    instr_cfg()
    # tree = ast.parse(code)
    # target_node = ...  # the AST node you want to find the control flow for
    # visitor = ControlFlowVisitor(target_node)
    # visitor.visit(tree)
    # print(visitor.control_flow)
    code='''   
    '''
    nodes=get_for_2(code)
    print("nodes: ",nodes)
    for e in nodes:
        print("e: ",ast.unparse(e))
