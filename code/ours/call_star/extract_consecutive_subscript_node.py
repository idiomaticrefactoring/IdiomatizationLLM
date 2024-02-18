'''
Extract consecutive subscript elements whose value is same from a given element sequence
'''

'''
As an AI language model, I do not have the capability to write code. However, I can explain the logic behind the solution to the problem.

To extract consecutive subscript elements whose value is the same from a given element sequence, we can use a loop to iterate through the sequence and compare each element with the previous one. If the current element is the same as the previous one, we add it to a temporary list. If it is different, we check the length of the temporary list. If it is greater than 1, we add it to the final list of consecutive elements. We then clear the temporary list and continue iterating through the sequence.

Here is an example implementation in Python:

```
def extract_consecutive_elements(sequence):
    consecutive_elements = []
    temp = [sequence[0]]
    for i in range(1, len(sequence)):
        if sequence[i] == sequence[i-1]:
            temp.append(sequence[i])
        else:
            if len(temp) > 1:
                consecutive_elements.append(temp)
            temp = [sequence[i]]
    if len(temp) > 1:
        consecutive_elements.append(temp)
    return consecutive_elements
```

This function takes a sequence as input and returns a list of lists, where each inner list contains the consecutive elements with the same value. For example, if the input sequence is [1, 2, 2, 3, 3, 3, 4, 4], the output would be [[2, 2], [3, 3, 3], [4, 4]].
'''
def extract_consecutive_elements(sequence):
    consecutive_elements = []
    temp = [sequence[0]]
    for i in range(1, len(sequence)):
        if sequence[i] == sequence[i-1]:
            temp.append(sequence[i])
        else:
            if len(temp) > 1:
                consecutive_elements.append(temp)
            temp = [sequence[i]]
    if len(temp) > 1:
        consecutive_elements.append(temp)
    return consecutive_elements

'''
Extract consecutive subscript node whose value is same from the arguments of Call AST node in Python
'''

'''
As an AI language model, I do not have access to the specific code you are working with. However, I can provide a general approach to extract consecutive subscript nodes whose value is the same from the arguments of a Call AST node in Python.

1. Traverse the AST tree to find the Call node.
2. Get the arguments of the Call node.
3. Traverse the arguments to find the subscript nodes.
4. Check if the value of the subscript node is the same as the previous one.
5. If it is the same, add it to a list of consecutive subscript nodes.
6. If it is not the same, check if the list of consecutive subscript nodes has more than one element.
7. If it does, extract the list of consecutive subscript nodes and add it to a list of extracted subscript nodes.
8. Repeat steps 4-7 until all arguments have been traversed.
9. Return the list of extracted subscript nodes.

Here is some sample code that demonstrates this approach:

```
import ast

def extract_consecutive_subscripts(node):
    if isinstance(node, ast.Call):
        args = node.args
        extracted_subscripts = []
        consecutive_subscripts = []
        prev_value = None
        for arg in args:
            if isinstance(arg, ast.Subscript):
                value = ast.dump(arg.value)
                if value == prev_value:
                    consecutive_subscripts.append(arg)
                else:
                    if len(consecutive_subscripts) > 1:
                        extracted_subscripts.append(consecutive_subscripts)
                    consecutive_subscripts = [arg]
                    prev_value = value
            else:
                if len(consecutive_subscripts) > 1:
                    extracted_subscripts.append(consecutive_subscripts)
                consecutive_subscripts = []
                prev_value = None
        if len(consecutive_subscripts) > 1:
            extracted_subscripts.append(consecutive_subscripts)
        return extracted_subscripts
    else:
        return []
```

This function takes an AST node as input and returns a list of lists of consecutive subscript nodes whose value is the same in the arguments of a Call node.
'''
import ast
def extract_consecutive_subscripts(node):
    if isinstance(node, ast.Call):
        args = node.args
        extracted_subscripts = []
        consecutive_subscripts = []
        prev_value = None
        for arg in args:
            if isinstance(arg, ast.Subscript):
                value = ast.dump(arg.value)
                if value == prev_value:
                    consecutive_subscripts.append(arg)
                else:
                    if len(consecutive_subscripts) > 1:
                        extracted_subscripts.append(consecutive_subscripts)
                    consecutive_subscripts = [arg]
                    prev_value = value
            else:
                if len(consecutive_subscripts) > 1:
                    extracted_subscripts.append(consecutive_subscripts)
                consecutive_subscripts = []
                prev_value = None
        if len(consecutive_subscripts) > 1:
            extracted_subscripts.append(consecutive_subscripts)
        return extracted_subscripts
    else:
        return []

import os,sys
import struct
import traceback
code_dir = "/".join(os.path.abspath(__file__).split("/")[:-2]) + "/"
print("code path: ",code_dir)
sys.path.append(code_dir)
import chatgpt_util,random
import openai, tiktoken,ast,util
import ast
import call_star_util
if __name__ == '__main__':
    idiom = "call_star"
    save_complicated_code_dir_root = util.data_root + "chatgpt/NonIdiomatic/"
    # save_complicated_code_dir_root = util.data_root + "NonIdiomatic/find_code_snippets/"
    save_complicated_code_dir = save_complicated_code_dir_root + "sample_methods/"

    samples = util.load_pkl(save_complicated_code_dir, "sample_methods_" + idiom)

    # extract_consecutive_subscripts(node)
    # random.seed(2023)
    # samples = random.sample(samples, 30)
    file_name="abstract_same_value_all"#"whether_can_var_unpack_for_subscript_stmt_instr_explain_4_new"
    reponse_list = call_star_util.abstract_consecutive(samples)
    util.save_pkl(save_complicated_code_dir_root + idiom + "/",
                  file_name,
                  reponse_list)
