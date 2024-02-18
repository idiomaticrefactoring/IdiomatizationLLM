import ast,os,sys
import copy
import traceback

import util_rewrite

code_dir = "/".join(os.path.abspath(__file__).split("/")[:-2]) + "/"
print("code path: ",code_dir)
sys.path.append(code_dir)
import chatgpt_util,random
import openai, tiktoken,ast,util,chat_gpt_ast_util
def parse_refactor_code(content):
    code_pairs=[]
    try:
        answer_list = content.split("Information:")
        code_pair_info="Information:".join(answer_list[1:])
        content_list = content.split("\n")

        for content in content_list:
            if "Answer: No" in content:
                return 0, code_pairs
            else:
                code_pair_list=code_pair_info.split("******\n")
                for code_pair in code_pair_list:
                    old_code,new_code=code_pair.split("Refactored code:\n")
                    old_code=old_code.split("Non-Idiomatic code:\n")[-1].strip()
                    new_code=new_code.strip()
                    code_pairs.append([old_code,new_code])
                return 1,  code_pairs
    except:
        print("content: ",content)
        traceback.print_exc()
        pass
    return 0, None

def get_response_directly_refactor(user_instr, examples, samples,
                                                     sys_msg="You are a helpful assistant."):
    count=0
    reponse_list = []
    # method_code_list = []
    # one_other = []
    # for ind_sampl, sample_method in enumerate(samples):
    #     method_code_list.append(sample_method)

    for *other, node in samples:

        if 1:
            # code=ast.unparse(node)

            real_instruction = user_instr.replace("{{code}}",node)

            count+=1
            # '''
            print(">>>>>>>>>>real_instruction: ", real_instruction)

            msg = chatgpt_util.format_message_2(real_instruction, examples=examples, sys_msg=sys_msg)

            try:
                response = chatgpt_util.chatGPT_result(msg)
                print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
                reponse_list.append(
                    [*other,node])
                reponse_list[-1].extend([[msg], response])
            except:
                traceback.print_exc()
                reponse_list.append([*other,node])
                reponse_list[-1].extend([[msg], traceback.format_exc()])

    print("count: ",count)
    return reponse_list