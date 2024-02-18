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
Refactor the following Python code with assign multiple values to multiple targets simultaneously. You give all code pairs where each pair consists of non-idiomatic Python code and the corresponding refactored code. You respond according to the response format.

Python code:
{{code}}

response format:
Answer: You respond with Yes or No for whether the code has non-idiomatic Python code that can be refactored with assign multiple values to multiple targets simultaneously.
Information: You respond with all code pairs where each pair consists of non-idiomatic code and the corresponding refactored code. Each pair splits with "******"
Non-Idiomatic Python code: You respond with identified non-idiomatic Python code that can be refactored with assign multiple values to multiple targets simultaneously.
Refactored Python code: You respond with the corresponding idiomatic Python code after refactoring the non-idiomatic code with assign multiple values to multiple targets simultaneously.
******
Non-Idiomatic code:...
Refactored code:...
'''
    examples = [
['''
Refactor the following Python code with assign multiple values to multiple targets simultaneously. You give all code pairs where each pair consists of non-idiomatic Python code and the corresponding refactored code. You respond according to the response format.

Python code:
def f(a):
    nd = a.shape.rank
    if (axis + nd if axis < 0 else axis) >= nd:
      raise ValueError("axis %s is out of bounds for array of dimension %s" %
                       (axis, nd))
    if n < 0:
      raise ValueError("order must be non-negative but got %s" % n)
    slice1 = [slice(None)] * nd
    slice2 = [slice(None)] * nd
    slice1[axis] = slice(1, None)
    slice2[axis] = slice(None, -1)
    slice1 = tuple(slice1)
    slice2 = tuple(slice2)
    op = tf.not_equal if a.dtype == tf.bool else tf.subtract
    for _ in range(n):
      a = op(a[slice1], a[slice2])
    return a

response format:
Answer: You respond with Yes or No for whether the code has non-idiomatic Python code that can be refactored with assign multiple values to multiple targets simultaneously.
Information: You respond with all code pairs where each pair consists of non-idiomatic code and the corresponding refactored code. Each pair splits with "******"
Non-Idiomatic Python code: You respond with identified non-idiomatic Python code that can be refactored with assign multiple values to multiple targets simultaneously.
Refactored Python code: You respond with the corresponding idiomatic Python code after refactoring the non-idiomatic code with assign multiple values to multiple targets simultaneously.
******
Non-Idiomatic code:...
Refactored code:...
''',
'''
Answer: Yes
Information:
Non-Idiomatic code:
slice1 = [slice(None)] * nd
slice2 = [slice(None)] * nd
    
Refactored code:
slice1, slice2 = [slice(None)] * nd, [slice(None)] * nd
******
Non-Idiomatic code:
slice1[axis] = slice(1, None)
slice2[axis] = slice(None, -1)
Refactored code:
slice1[axis], slice2[axis] = slice(1, None), slice(None, -1)
******
Non-Idiomatic code:
slice1 = tuple(slice1)
slice2 = tuple(slice2)
op = tf.not_equal if a.dtype == tf.bool else tf.subtract
Refactored code:
slice1, slice2, op = tuple(slice1), tuple(slice2), tf.not_equal if a.dtype == tf.bool else tf.subtract
''']]
    save_complicated_code_dir_root = util.data_root + "chatgpt/NonIdiomatic/"
    # save_complicated_code_dir_root = util.data_root + "NonIdiomatic/find_code_snippets/"
    save_complicated_code_dir = save_complicated_code_dir_root + "sample_methods/"
    idiom = "assign_multiple_targets"
    idiom = "_".join(idiom.split(" "))

    file_name = idiom + "_methods"

    samples = util.load_pkl(save_complicated_code_dir_root, file_name)  # methods_sample

    reponse_list = baseline_util.get_response_directly_refactor(user_instr, examples, samples,
                                                                sys_msg="You are a helpful assistant.")
    '''
    file_name = "baseline"+idiom
    util.save_pkl(save_complicated_code_dir_root + "baseline/",
                  file_name,
                  reponse_list)
    
    file_name = "baseline"+idiom
    reponse_list = util.load_pkl(save_complicated_code_dir_root+ "baseline/", file_name)  # methods_sample
    print("reponse_list: ",len(reponse_list))
    '''
