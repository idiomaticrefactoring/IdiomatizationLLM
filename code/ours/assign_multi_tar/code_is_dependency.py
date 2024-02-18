'''
Extract all consecutive assign nodes from a given Python code in Python
'''
import copy
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
    #How to extract blocks consisting of several consecutive assignment statements from the a given Python code. Each block whose statements does not have data dependency.

    real_instruction = '''
How to extract consecutive assignment statements that do not have depdency from the a given Python code. 

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
v1 = np.array([1 + 2j, 3 + 4j, 5 + 6j])
v2 = tensor(v1, chunk_size=2)
v3 = v2.imag.execute().fetch()
v4 = v1.imag

all consecutive assign nodes:
[[event_type = 'ROOT', event_data = 'example data', event_module = '', source_event = ''],
[x = 1, y = 2],
[v3 = v2.imag.execute().fetch(), v4 = v1.imag]
]
    '''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])

def extract_assignment_blocks(code):
    # Parse the code into an AST
    tree = ast.parse(code)

    # Initialize variables
    blocks = []
    current_block = []
    last_assigned_vars = set()

    # Traverse the AST and extract assignment blocks
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            # Get the names of the variables being assigned
            assigned_vars = set()
            for target in node.targets:
                if isinstance(target, ast.Name):
                    assigned_vars.add(target.id)
            print("last_assigned_vars: ",last_assigned_vars)
            # Check if the assigned variables have data dependency
            if assigned_vars.isdisjoint(last_assigned_vars):
                # Add the assignment statement to the current block
                current_block.append(node)

                # Update the set of last assigned variables
                last_assigned_vars.update(assigned_vars)
            else:
                # End the current block and start a new one
                if current_block:
                    blocks.append(current_block)
                current_block = [node]
                last_assigned_vars = set()

    # Add the last block to the list of blocks
    if current_block:
        blocks.append(current_block)

    # Convert the blocks to a list of lists of strings
    result = []
    for block in blocks:
        result.append([ast.unparse(node).strip() for node in block])
    print("len of result: ",len(result))
    return result
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
    '''
    To extract consecutive assignment statements that do not have dependencies, you can use the following steps:

1. Parse the Python code using a parser like `ast.parse()` to get an abstract syntax tree (AST) of the code.
2. Traverse the AST to identify all the assignment statements.
3. Create a dependency graph of the assignment statements, where each node represents an assignment statement and each edge represents a dependency between two statements.
4. Identify the connected components of the dependency graph, which represent groups of assignment statements that do not have dependencies between them.
5. For each connected component, extract the assignment statements and combine them into a single statement.

Here's some sample code that implements these steps:

    '''
    from collections import defaultdict
    tree = ast.parse(code)

    # Step 2: Traverse the AST to identify all the assignment statements
    assignments = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            assignments.append(node)

    # Step 3: Create a dependency graph of the assignment statements
    graph = defaultdict(set)
    for node in assignments:
        for target in node.targets:
            for dep in ast.walk(node.value):
                if isinstance(dep, ast.Name) and dep.id != target.id:
                    graph[target.id].add(dep.id)

    # Step 4: Identify the connected components of the dependency graph
    visited = set()
    components = []
    for node in graph:
        print("1graph: ",graph)
        if node not in visited:
            component = set()
            stack = [node]
            while stack:
                curr = stack.pop()
                if curr not in visited:
                    visited.add(curr)
                    component.add(curr)
                    print("2.2graph: ", graph)
                    print("graph[curr]: ",node,graph[curr])
                    if curr in  graph:
                        stack.extend(graph[curr])
                    print("2.3graph: ", graph)
                    print("stack: ",stack)
            components.append(component)
            print("2graph: ", graph)
        print("3graph: ",graph)

    # Step 5: Extract the assignment statements for each connected component
    consecutive_assignments = []
    for component in components:
        component_assignments = []
        for node in assignments:
            if node.targets[0].id in component:
                component_assignments.append(node)
        consecutive_assignments.append(component_assignments)

    # Print the result
    for component in consecutive_assignments:
        print([ast.unparse(node).strip() for node in component])
