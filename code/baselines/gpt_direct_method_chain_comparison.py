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
Refactor the following Python code with chain comparison. You give all code pairs where each pair consists of non-idiomatic Python code and the corresponding refactored code. You respond according to the response format.

Python code:
{{code}}

response format:
Answer: You respond with Yes or No for whether the code has non-idiomatic Python code that can be refactored with chain comparison.
Information: You respond with all code pairs where each pair consists of non-idiomatic code and the corresponding refactored code. Each pair splits with "******"
Non-Idiomatic Python code: You respond with identified non-idiomatic Python code that can be refactored with chain comparison.
Refactored Python code: You respond with the corresponding idiomatic Python code after refactoring the non-idiomatic code with chain comparison.
******
Non-Idiomatic code:...
Refactored code:...
'''
    examples = [
['''
Refactor the following Python code with chain comparison. You give all code pairs where each pair consists of non-idiomatic Python code and the corresponding refactored code. You respond according to the response format.

Python code:
def get_jieba_dict(min_freq=0, max_freq=float('inf'), with_pos=False, use_proxy=False, proxies=None):
    """
    获得jieba自带的中文词语词频词典
    
    :params min_freq: 选取词语需要的最小词频
    :params max_freq: 选取词语允许的最大词频
    :params with_pos: 返回结果是否包括词性信息
    :return if not with_pos, dict of {wd: freq}, else, dict of {(wd, pos): freq} 
    """
    from .download_utils import RemoteFileMetadata, check_download_resource
    remote = RemoteFileMetadata(
        filename='jieba_dict.txt',
        url='https://github.com/blmoistawinde/HarvestText/releases/download/V0.8/jieba_dict.txt',
        checksum='7197c3211ddd98962b036cdf40324d1ea2bfaa12bd028e68faa70111a88e12a8')
    file_path = check_download_resource(remote, use_proxy, proxies)
    ret = defaultdict(int)
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            if len(line.strip().split()) == 3:
                wd, freq, pos = line.strip().split()
                freq = int(freq)
            if freq > min_freq and freq < max_freq:
                if not with_pos:
                    ret[wd] = freq
                else:
                    ret[(wd, pos)] = freq
    return ret

response format:
Answer: You respond with Yes or No for whether the code has non-idiomatic Python code that can be refactored with chain comparison.
Information: You respond with all code pairs where each pair consists of non-idiomatic code and the corresponding refactored code. Each pair splits with "******"
Non-Idiomatic Python code: You respond with identified non-idiomatic Python code that can be refactored with chain comparison.
Refactored Python code: You respond with the corresponding idiomatic Python code after refactoring the non-idiomatic code with chain comparison.
******
Non-Idiomatic code:...
Refactored code:...
''',
'''
Answer: Yes
Information:
Non-Idiomatic code:
freq > min_freq and freq < max_freq
    
Refactored code:
min_freq < freq < max_freq
''']]
    save_complicated_code_dir_root = util.data_root + "chatgpt/NonIdiomatic/"
    # save_complicated_code_dir_root = util.data_root + "NonIdiomatic/find_code_snippets/"
    save_complicated_code_dir = save_complicated_code_dir_root + "sample_methods/"
    idiom = "chain_comparison"

    file_name = idiom + "_methods"

    samples = util.load_pkl(save_complicated_code_dir_root, file_name)  # methods_sample

    reponse_list = baseline_util.get_response_directly_refactor(user_instr, examples, samples,
                                                                sys_msg="You are a helpful assistant.")
    
    file_name = "baseline_"+idiom
    util.save_pkl(save_complicated_code_dir_root + "baseline/",
                  file_name,
                  reponse_list)
    '''
    file_name = "baseline_"+idiom
    reponse_list = util.load_pkl(save_complicated_code_dir_root+ "baseline/", file_name)  # methods_sample
    print("reponse_list: ",len(reponse_list))
    '''