import os, sys
import struct
import traceback

import util_rewrite

code_dir = "/".join(os.path.abspath(__file__).split("/")[:-2]) + "/"
print("code path: ", code_dir)
sys.path.append(code_dir)
import chatgpt_util, random, chat_gpt_ast_util
import openai, tiktoken, ast, util, util_rewrite,baseline_util
import ast
if __name__ == '__main__':
    user_instr = '''
Refactor the following Python code with set comprehension. You give all code pairs where each pair consists of non-idiomatic Python code and the corresponding refactored code. You respond according to the response format.

Python code:
{{code}}

response format:
Answer: You respond with Yes or No for whether the code has non-idiomatic Python code that can be refactored with set comprehension.
Information: You respond with all code pairs where each pair consists of non-idiomatic code and the corresponding refactored code. Each pair splits with "******"
Non-Idiomatic Python code: You respond with identified non-idiomatic Python code that can be refactored with set comprehension.
Refactored Python code: You respond with the corresponding idiomatic Python code after refactoring the non-idiomatic code with set comprehension.
******
Non-Idiomatic code:...
Refactored code:...
'''
    examples = [
['''
Refactor the following Python code with set comprehension. You give all code pairs where each pair consists of non-idiomatic Python code and the corresponding refactored code. You respond according to the response format.

Python code:
def build_wire_filter(wire_filter):
    wires_to_include = set()
    with OpenSafeFile(wire_filter) as f:
        for l in f:
            wire = l.strip()
            if not wire:
                continue
            wires_to_include.add(wire)

    def filter_net(net):
        wires_in_net = set()
        for node in net['nodes']:
            for wire in node['wires']:
                wires_in_net.add(wire['name'])
        return len(wires_in_net & wires_to_include) > 0
    return filter_net

response format:
Answer: You respond with Yes or No for whether the code has non-idiomatic Python code that can be refactored with set comprehension.
Information: You respond with all code pairs where each pair consists of non-idiomatic code and the corresponding refactored code. Each pair splits with "******"
Non-Idiomatic Python code: You respond with identified non-idiomatic Python code that can be refactored with set comprehension.
Refactored Python code: You respond with the corresponding idiomatic Python code after refactoring the non-idiomatic code with set comprehension.
******
Non-Idiomatic code:...
Refactored code:...
''',
'''
Answer: Yes
Information:
Non-Idiomatic code:
wires_in_net = set()
for node in net['nodes']:
    for wire in node['wires']:
        wires_in_net.add(wire['name'])
    
Refactored code:
wires_in_net = {wire['name'] for node in net['nodes'] for wire in node['wires']}''']]
    save_complicated_code_dir_root = util.data_root + "chatgpt/NonIdiomatic/"
    # save_complicated_code_dir_root = util.data_root + "NonIdiomatic/find_code_snippets/"
    save_complicated_code_dir = save_complicated_code_dir_root + "sample_methods/"
    idiom = "set_comprehension"
    file_name = idiom + "_methods"

    samples = util.load_pkl(save_complicated_code_dir_root, file_name)  # methods_sample
    reponse_list = baseline_util.get_response_directly_refactor(user_instr, examples, samples,
                                                                sys_msg="You are a helpful assistant.")
    file_name = "baseline_set_comprehension"
    util.save_pkl(save_complicated_code_dir_root + "baseline/",
                  file_name,
                  reponse_list)
