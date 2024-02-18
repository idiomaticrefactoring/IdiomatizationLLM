import os, sys
import struct
import traceback

import util_rewrite

code_dir = "/".join(os.path.abspath(__file__).split("/")[:-2]) + "/"
print("code path: ", code_dir)
sys.path.append(code_dir)
import chatgpt_util, random,chat_gpt_ast_util
import openai, tiktoken, ast, util,util_rewrite
import ast,ass_same_value_util
find_consecutive_assign_nodes(code_str)