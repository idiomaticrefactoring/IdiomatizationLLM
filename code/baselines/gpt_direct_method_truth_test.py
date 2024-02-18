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
Refactor the following Python code with truth value testing. You give all code pairs where each pair consists of non-idiomatic Python code and the corresponding refactored code. You respond according to the response format.

Python code:
{{code}}

response format:
Answer: You respond with Yes or No for whether the code has non-idiomatic Python code that can be refactored with truth value testing.
Information: You respond with all code pairs where each pair consists of non-idiomatic code and the corresponding refactored code. Each pair splits with "******"
Non-Idiomatic Python code: You respond with identified non-idiomatic Python code that can be refactored with truth value testing.
Refactored Python code: You respond with the corresponding idiomatic Python code after refactoring the non-idiomatic code with truth value testing.
******
Non-Idiomatic code:...
Refactored code:...
'''
    examples = [
['''
Refactor the following Python code with truth value testing. You give all code pairs where each pair consists of non-idiomatic Python code and the corresponding refactored code. You respond according to the response format.

Python code:
def patchify2d_cx(cx, w_in, w_out, k, *, bias=True):
    """Accumulates complexity of patchify2d into cx = (h, w, flops, params, acts)."""
    err_str = "Only kernel sizes divisible by the input size are supported."
    assert cx["h"] % k == 0 and cx["w"] % k == 0, err_str
    h, w, flops, params, acts = cx["h"], cx["w"], cx["flops"], cx["params"], cx["acts"]
    h, w = h // k, w // k
    flops += k * k * w_in * w_out * h * w + (w_out * h * w if bias else 0)
    params += k * k * w_in * w_out + (w_out if bias else 0)
    acts += w_out * h * w
    return {"h": h, "w": w, "flops": flops, "params": params, "acts": acts}

response format:
Answer: You respond with Yes or No for whether the code has non-idiomatic Python code that can be refactored with truth value testing.
Information: You respond with all code pairs where each pair consists of non-idiomatic code and the corresponding refactored code. Each pair splits with "******"
Non-Idiomatic Python code: You respond with identified non-idiomatic Python code that can be refactored with truth value testing.
Refactored Python code: You respond with the corresponding idiomatic Python code after refactoring the non-idiomatic code with truth value testing.
******
Non-Idiomatic code:...
Refactored code:...
''',
'''
Answer: Yes
Information:
Non-Idiomatic code:
cx["h"] % k == 0
    
Refactored code:
not cx["h"] % k
******
Non-Idiomatic code:
cx["w"] % k == 0
Refactored code:
not cx["w"] % k''']]
    save_complicated_code_dir_root = util.data_root + "chatgpt/NonIdiomatic/"
    # save_complicated_code_dir_root = util.data_root + "NonIdiomatic/find_code_snippets/"
    save_complicated_code_dir = save_complicated_code_dir_root + "sample_methods/"
    idiom = "truth value testing"
    idiom = "_".join(idiom.split(" "))

    file_name = idiom + "_methods"

    samples = util.load_pkl(save_complicated_code_dir_root, file_name)  # methods_sample

    reponse_list = baseline_util.get_response_directly_refactor(user_instr, examples, samples,
                                                                sys_msg="You are a helpful assistant.")
    
    file_name = "baseline"+idiom
    util.save_pkl(save_complicated_code_dir_root + "baseline/",
                  file_name,
                  reponse_list)
    '''
    file_name = "baseline"+idiom
    reponse_list = util.load_pkl(save_complicated_code_dir_root+ "baseline/", file_name)  # methods_sample
    print("reponse_list: ",len(reponse_list))
    '''
