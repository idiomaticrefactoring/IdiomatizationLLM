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
Refactor the following Python code with dictionary comprehension. You give all code pairs where each pair consists of non-idiomatic Python code and the corresponding refactored code. You respond according to the response format.

Python code:
{{code}}

response format:
Answer: You respond with Yes or No for whether the code has non-idiomatic Python code that can be refactored with dictionary comprehension.
Information: You respond with all code pairs where each pair consists of non-idiomatic code and the corresponding refactored code. Each pair splits with "******"
Non-Idiomatic Python code: You respond with identified non-idiomatic Python code that can be refactored with dictionary comprehension.
Refactored Python code: You respond with the corresponding idiomatic Python code after refactoring the non-idiomatic code with dictionary comprehension.
******
Non-Idiomatic code:...
Refactored code:...
'''
    examples = [
['''
Refactor the following Python code with dictionary comprehension. You give all code pairs where each pair consists of non-idiomatic Python code and the corresponding refactored code. You respond according to the response format.

Python code:
def dataset_update_method(dataset: 'Dataset', other: 'CoercibleMapping') -> _MergeResult:
    """Guts of the Dataset.update method.

    This drops a duplicated coordinates from `other` if `other` is not an
    `xarray.Dataset`, e.g., if it's a dict with DataArray values (GH2068,
    GH2180).
    """
    from .dataarray import DataArray
    from .dataset import Dataset
    if not isinstance(other, Dataset):
        other = dict(other)
        for (key, value) in other.items():
            if isinstance(value, DataArray):
                coord_names = [c for c in value.coords if c not in value.dims and c in dataset.coords]
                if coord_names:
                    other[key] = value.drop_vars(coord_names)
    indexes = {}
    for (key, index) in dataset.xindexes.items():
        if isinstance(index, PandasIndex):
            indexes[key] = dataset.coords[key]
        else:
            indexes[key] = index
    return merge_core([dataset, other], priority_arg=1, indexes=indexes, combine_attrs='override')

response format:
Answer: You respond with Yes or No for whether the code has non-idiomatic Python code that can be refactored with dictionary comprehension.
Information: You respond with all code pairs where each pair consists of non-idiomatic code and the corresponding refactored code. Each pair splits with "******"
Non-Idiomatic Python code: You respond with identified non-idiomatic Python code that can be refactored with dictionary comprehension.
Refactored Python code: You respond with the corresponding idiomatic Python code after refactoring the non-idiomatic code with dictionary comprehension.
******
Non-Idiomatic code:...
Refactored code:...
''',
'''
Answer: Yes
Information:
Non-Idiomatic code:
indexes = {}
for (key, index) in dataset.xindexes.items():
    if isinstance(index, PandasIndex):
        indexes[key] = dataset.coords[key]
    else:
        indexes[key] = index
    
Refactored code:
indexes = {key: dataset.coords[key] if isinstance(index, PandasIndex) else index for (key, index) in dataset.xindexes.items()}
''']]
    save_complicated_code_dir_root = util.data_root + "chatgpt/NonIdiomatic/"
    # save_complicated_code_dir_root = util.data_root + "NonIdiomatic/find_code_snippets/"
    save_complicated_code_dir = save_complicated_code_dir_root + "sample_methods/"
    idiom = "dict_comprehension"
    file_name = idiom + "_methods"

    samples = util.load_pkl(save_complicated_code_dir_root, file_name)  # methods_sample
    reponse_list = baseline_util.get_response_directly_refactor(user_instr, examples, samples,
                                                                sys_msg="You are a helpful assistant.")
    file_name = "baseline_dict_comprehension"
    util.save_pkl(save_complicated_code_dir_root + "baseline/",
                  file_name,
                  reponse_list)
