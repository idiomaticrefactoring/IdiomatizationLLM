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
Refactor the following Python code containing open() function call with With statement. You give all code pairs where each pair consists of non-idiomatic code and the corresponding refactored code. You respond according to the response format.

Python code:
{{code}}

response format:
Answer: You respond with Yes or No for whether the code has non-idiomatic code that can be refactored with With statement.
Information: You respond with all code pairs where each pair consists of non-idiomatic code and the corresponding refactored code. Each pair splits with "******"
Non-Idiomatic code: You respond with identified non-idiomatic code that can be refactored with  With statement.
Refactored code: You respond with the corresponding idiomatic code after refactoring the non-idiomatic code with  With statement.
******
Non-Idiomatic code:...
Refactored code:...
'''
    examples = [
['''
Refactor the following Python code containing open() function call with With statement. You give all code pairs where each pair consists of non-idiomatic code and the corresponding refactored code. You respond according to the response format.

Python code:
def main(source_files, outpath, keywords=None):
    if options.excludefilename:
        try:
            fp = open(options.excludefilename, encoding='utf-8')
            options.toexclude = fp.readlines()
            fp.close()
        except IOError:
            print("Can't read --exclude-file: %s" % options.excludefilename, file=sys.stderr)
            sys.exit(1)
    else:
        options.toexclude = []
    fp = open(options.outfile, 'w', encoding='utf-8')
    closep = 1
    try:
        eater.write(fp)
    finally:
        if closep:
            fp.close()

response format:
Answer: You respond with Yes or No for whether the code has non-idiomatic code that can be refactored with With statement.
Information: You respond with all code pairs where each pair consists of non-idiomatic code and the corresponding refactored code. Each pair splits with "******"
Non-Idiomatic code: You respond with identified non-idiomatic code that can be refactored with  With statement.
Refactored code: You respond with the corresponding idiomatic code after refactoring the non-idiomatic code with  With statement.
******
Non-Idiomatic code:...
Refactored code:...
''',
'''
Answer: Yes
Information:
Non-Idiomatic code:
try:
    fp = open(options.excludefilename, encoding='utf-8')
    options.toexclude = fp.readlines()
    fp.close()
except IOError:
    print("Can't read --exclude-file: %s" % options.excludefilename, file=sys.stderr)
    sys.exit(1)

Refactored code:
try:
    with open(options.excludefilename, encoding='utf-8') as fp:
        options.toexclude = fp.readlines()
except IOError:
    print("Can't read --exclude-file: %s" % options.excludefilename, file=sys.stderr)
    sys.exit(1) 
******
Non-Idiomatic code:    
fp = open(options.outfile, 'w', encoding='utf-8')
closep = 1
try:
    eater.write(fp)
finally:
    if closep:
        fp.close()

Refactored code:
with open(options.outfile, 'w', encoding='utf-8') as fp:
    closep = 1
    try:
        eater.write(fp)
    finally:
        if closep:
            fp.close()
''']

    ]
    save_complicated_code_dir_root = util.data_root + "chatgpt/NonIdiomatic/"
    # save_complicated_code_dir_root = util.data_root + "NonIdiomatic/find_code_snippets/"
    save_complicated_code_dir = save_complicated_code_dir_root + "sample_methods/"
    file_name="new_idiom_methods_600"
    samples = util.load_pkl(save_complicated_code_dir_root, file_name)  # methods_sample
    reponse_list = baseline_util.get_response_directly_refactor(user_instr, examples, samples,
                                                                sys_msg="You are a helpful assistant.")
    file_name = "baseline_with_stmt_with_open"
    util.save_pkl(save_complicated_code_dir_root+ "baseline/",
                      file_name,
                      reponse_list)

