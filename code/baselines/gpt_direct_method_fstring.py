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
Refactor the following Python code containing old "C-style" method of formatting strings with fstring. You give all code pairs where each pair consists of non-idiomatic code and the corresponding refactored code. You respond according to the response format.

Python code:
{{code}}

response format:
Answer: You respond with Yes or No for whether the code has non-idiomatic code that can be refactored with fstring.
Information: You respond with all code pairs where each pair consists of non-idiomatic code and the corresponding refactored code. Each pair splits with "******"
Non-Idiomatic code: You respond with identified non-idiomatic code that can be refactored with fstring.
Refactored code: You respond with the corresponding idiomatic code after refactoring the non-idiomatic code with fstring.
******
Non-Idiomatic code:...
Refactored code:...
'''
    examples = [
['''
Refactor the following Python code containing old "C-style" method of formatting strings with fstring. You give all code pairs where each pair consists of non-idiomatic code and the corresponding refactored code. You respond according to the response format.

Python code:
def assign_variable_names(self, labels=None, types=None):
    """
        Assign default names to all SSA variables.

        :param labels:  Known labels in the binary.
        :return:        None
        """
    for var in self._variables:
        if (types is None or SimStackVariable in types) and isinstance(var, SimStackVariable):
            if var.name is not None:
                continue
            if var.ident.startswith('iarg'):
                var.name = 'arg_%x' % var.offset
            else:
                var.name = 's_%x' % -var.offset
        elif (types is None or SimRegisterVariable in types) and isinstance(var, SimRegisterVariable):
            if var.name is not None:
                continue
            var.name = var.ident
        elif (types is None or SimMemoryVariable in types) and isinstance(var, SimMemoryVariable):
            if var.name is not None:
                continue
            if labels is not None and var.addr in labels:
                var.name = labels[var.addr]
                if '@@' in var.name:
                    var.name = var.name[:var.name.index('@@')]
            elif var.ident is not None:
                var.name = var.ident
response format:
Answer: You respond with Yes or No for whether the code has non-idiomatic code that can be refactored with fstring.
Information: You respond with all code pairs where each pair consists of non-idiomatic code and the corresponding refactored code. Each pair splits with "******"
Non-Idiomatic code: You respond with identified non-idiomatic code that can be refactored with fstring.
Refactored code: You respond with the corresponding idiomatic code after refactoring the non-idiomatic code with fstring.
******
Non-Idiomatic code:...
Refactored code:...
''',
'''
Answer: Yes
Information:
Non-Idiomatic code:
'arg_%x' % var.offset

Refactored code:
f'arg_{var.offset:x}'
******
Non-Idiomatic code:    
var.name = 's_%x' % -var.offset

Refactored code:
f's_{-var.offset:x}'
''']

    ]
    save_complicated_code_dir_root = util.data_root + "chatgpt/NonIdiomatic/"
    # save_complicated_code_dir_root = util.data_root + "NonIdiomatic/find_code_snippets/"
    save_complicated_code_dir = save_complicated_code_dir_root + "sample_methods/"
    file_name="new_idiom_methods_600"
    samples = util.load_pkl(save_complicated_code_dir_root, file_name)  # methods_sample
    reponse_list = baseline_util.get_response_directly_refactor(user_instr, examples, samples,
                                                                sys_msg="You are a helpful assistant.")
    file_name = "baseline_fstring_stmt"
    util.save_pkl(save_complicated_code_dir_root+ "baseline/",
                      file_name,
                      reponse_list)

