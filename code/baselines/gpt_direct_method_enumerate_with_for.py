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
Refactor the for statement contained in the following Python code with enumerate. You give all code pairs where each pair consists of non-idiomatic code and the corresponding refactored code. You respond according to the response format.

Python code:
{{code}}

response format:
Answer: You respond with Yes or No for whether the code has non-idiomatic code (for statement) that can be refactored with enumerate.
Information: You respond with all code pairs where each pair consists of non-idiomatic code and the corresponding refactored code. Each pair splits with "******"
Non-Idiomatic code: You respond with identified non-idiomatic code that can be refactored with enumerate.
Refactored code: You respond with the corresponding idiomatic code after refactoring the non-idiomatic code with enumerate.
******
Non-Idiomatic code:...
Refactored code:...
'''
    examples = [
['''
Refactor the for statement contained in the following Python code with enumerate. You give all code pairs where each pair consists of non-idiomatic code and the corresponding refactored code. You respond according to the response format.

Python code:
def real_sph_harm(k, zero_m_only=True, spherical_coordinates=True):
    P_l_m = associated_legendre_polynomials(k, zero_m_only)
    if spherical_coordinates:
        theta = sym.symbols('theta')
        z = sym.symbols('z')
        for i in range(len(P_l_m)):
            for j in range(len(P_l_m[i])):
                if type(P_l_m[i][j]) != int:
                    P_l_m[i][j] = P_l_m[i][j].subs(z, sym.cos(theta))
        if not zero_m_only:
            phi = sym.symbols('phi')
            for i in range(len(S_m)):
                S_m[i] = S_m[i].subs(x, sym.sin(theta) * sym.cos(phi)).subs(y, sym.sin(theta) * sym.sin(phi))
response format:
Answer: You respond with Yes or No for whether the code has non-idiomatic code (for statement) that can be refactored with enumerate.
Information: You respond with all code pairs where each pair consists of non-idiomatic code and the corresponding refactored code. Each pair splits with "******"
Non-Idiomatic code: You respond with identified non-idiomatic code that can be refactored with enumerate.
Refactored code: You respond with the corresponding idiomatic code after refactoring the non-idiomatic code with enumerate.
******
Non-Idiomatic code:...
Refactored code:...
''',
'''
Answer: Yes
Information:
Non-Idiomatic code:
for i in range(len(P_l_m)):
    for j in range(len(P_l_m[i])):
        if type(P_l_m[i][j]) != int:
            P_l_m[i][j] = P_l_m[i][j].subs(z, sym.cos(theta))

Refactored code:
for i, row in enumerate(P_l_m):
    for j, val in enumerate(row):
        if type(val) != int:
            P_l_m[i][j] = val.subs(z, sym.cos(theta))
******
Non-Idiomatic code:    
for i in range(len(S_m)):
    S_m[i] = S_m[i].subs(x, sym.sin(theta) * sym.cos(phi)).subs(y, sym.sin(theta) * sym.sin(phi))

Refactored code:
for i,val in enumerate(S_m):
    S_m[i] = val.subs(x, sym.sin(theta) * sym.cos(phi)).subs(y, sym.sin(theta) * sym.sin(phi))
''']

    ]
    save_complicated_code_dir_root = util.data_root + "chatgpt/NonIdiomatic/"
    # save_complicated_code_dir_root = util.data_root + "NonIdiomatic/find_code_snippets/"
    save_complicated_code_dir = save_complicated_code_dir_root + "sample_methods/"
    file_name="new_idiom_methods_600"
    samples = util.load_pkl(save_complicated_code_dir_root, file_name)  # methods_sample
    reponse_list = baseline_util.get_response_directly_refactor(user_instr, examples, samples,
                                                                sys_msg="You are a helpful assistant.")
    file_name = "baseline_enumerate_stmt_with_for_stmt"
    util.save_pkl(save_complicated_code_dir_root+ "baseline/",
                      file_name,
                      reponse_list)

