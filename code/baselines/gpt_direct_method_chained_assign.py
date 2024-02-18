import os, sys
import struct
import traceback

import util_rewrite

code_dir = "/".join(os.path.abspath(__file__).split("/")[:-2]) + "/"
print("code path: ", code_dir)
sys.path.append(code_dir)
import chatgpt_util, random, chat_gpt_ast_util
import openai, tiktoken, ast, util, util_rewrite
import ast,baseline_util
if __name__ == '__main__':
    user_instr = '''
Refactor the following Python code with chained assignment to assign same constant values to multiple variables in a single line. You give all code pairs where each pair consists of non-idiomatic code and the corresponding refactored code. You respond according to the response format.

Python code:
{{code}}

response format:
Answer: You respond with Yes or No for whether the code has non-idiomatic code that can be refactored with chained assignment to assign same constant values to multiple variables in a single line.
Information: You respond with all code pairs where each pair consists of non-idiomatic code and the corresponding refactored code. Each pair splits with "******"
Non-Idiomatic code: You respond with identified non-idiomatic code that can be refactored with chained assignment to assign same constant values to multiple variables in a single line.
Refactored code: You respond with the corresponding idiomatic code after refactoring the non-idiomatic code with chained assignment to assign same constant values to multiple variables in a single line.
******
Non-Idiomatic code:...
Refactored code:...
'''
    examples = [
['''
Refactor the following Python code with chained assignment to assign same constant values to multiple variables in a single line. You give all code pairs where each pair consists of non-idiomatic code and the corresponding refactored code. You respond according to the response format.

Python code:
def parse_lamda_lines(data):
    meta_rad = {}
    meta_mol = {}
    meta_coll = {}
    levels = []
    radtrans = []
    collider = None
    ncolltrans = None
    for (ii, line) in enumerate(data):
        if line[0] == '!':
            continue
        if len(collrates[collider]) == meta_coll[collname]['ntrans']:
            log.debug('{ii} Finished loading collider {0:d}: {1}'.format(collider, collider_ids[collider], ii=ii))
            collider = None
            ncolltrans = None
            if len(collrates) == meta_coll['ncoll']:
                break
response format:
Answer: You respond with Yes or No for whether the code has non-idiomatic code that can be refactored with chained assignment to assign same constant values to multiple variables in a single line.
Information: You respond with all code pairs where each pair consists of non-idiomatic code and the corresponding refactored code. Each pair splits with "******"
Non-Idiomatic code: You respond with identified non-idiomatic code that can be refactored with chained assignment to assign same constant values to multiple variables in a single line.
Refactored code: You respond with the corresponding idiomatic code after refactoring the non-idiomatic code with chained assignment to assign same constant values to multiple variables in a single line.
******
Non-Idiomatic code:...
Refactored code:...
''',
'''
Answer: Yes
Information:
Non-Idiomatic code:
collider = None
ncolltrans = None

Refactored code:
ncolltrans = collider = None
******
Non-Idiomatic code:    
collider = None
ncolltrans = None

Refactored code:
ncolltrans = collider = None
''']

    ]
    save_complicated_code_dir_root = util.data_root + "chatgpt/NonIdiomatic/"
    # save_complicated_code_dir_root = util.data_root + "NonIdiomatic/find_code_snippets/"
    save_complicated_code_dir = save_complicated_code_dir_root + "sample_methods/"
    file_name="new_idiom_methods_600"
    samples = util.load_pkl(save_complicated_code_dir_root, file_name)  # methods_sample
    reponse_list = baseline_util.get_response_directly_refactor(user_instr, examples, samples,
                                                                sys_msg="You are a helpful assistant.")
    file_name = "baseline_chain_ass_stmt"
    util.save_pkl(save_complicated_code_dir_root+ "baseline/",
                      file_name,
                      reponse_list)

