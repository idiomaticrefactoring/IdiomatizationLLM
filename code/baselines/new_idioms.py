import os, sys
import struct
import traceback

import util_rewrite

code_dir = "/".join(os.path.abspath(__file__).split("/")[:-2]) + "/"
print("code path: ", code_dir)
sys.path.append(code_dir)
import chatgpt_util, random, chat_gpt_ast_util
import openai, tiktoken, ast, util, util_rewrite
import ast


def extract_module(samples):
    all_codes = []
    count = 0
    reponse_list = []
    method_code_list = []
    one_other = []
    for ind_sampl, sample_method in enumerate(samples):
        method_code_list.append(sample_method)
        # if ind_sampl>=9000:
        #     break

    for *other, method_code in method_code_list:
        # if "do_setup$1697" not in other:
        #     continue
        # print(other[2:])

        method_code = ast.unparse(ast.parse(method_code))
        # tree=ast.parse(method_code)
        # if "data_shifted.append(data[(column - row & 3) * 4 + row])" not in method_code:#"y.append(_triangular_inv(x[i]))" _all_input_text.append(i_text) addresses.append({'doctype':a.append(getattr(self, i)) area.append(m_id.eq(i).sum().item()) addresses.append({'doctype':psutil.process_iter(attrs=['name'])#"for item in account_dumps:" "wires_in_net.add(wire['name'])" "for interaction in interactions:" "for (_name, email) in settings.ADMINS" "for syn in synsets:"
        #     continue
        all_nodes = chat_gpt_ast_util.find_consecutive_assign_nodes(method_code)
        for nodes in all_nodes:
            ass_same_value_nodes = chat_gpt_ast_util.group_assign_nodes(nodes)
            for ass_list in ass_same_value_nodes:
                if len(ass_list) <= 1:
                    continue
                count += 1
                all_codes.append([*other, method_code, [ast.unparse(e) for e in ass_list]])
                # print("code:\n", "\n".join([ast.unparse(e) for e in ass_list]))
                # break
    print("count: ", count)
    return all_codes


if __name__ == '__main__':

    user_instr = '''
Refactor the following Python code consisting of multiple assignment statements with chained assignment to assign the same value to multiple variables in a single line.

Python code:
{{code}}

response format:
Answer: You respond with Yes or No for whether the code can be refactored with chained assignment.
Information: If your answer is Yes, you give the refactored code. Otherwise, you respond with None. 
'''
    examples = [
        ['''
Refactor the following Python code consisting of multiple assignment statements with chained assignment to assign the same value to multiple variables in a single line.

Python code:
a=1
b=1

response format:
Answer: You respond with Yes or No for whether the code can be refactored with chained assignment.
Information: If your answer is Yes, you give the refactored code. Otherwise, you respond with None. 
''',
         '''
         Answer: Yes
         Information:
         a=b=1
         ''']

    ]
    save_complicated_code_dir_root = util.data_root + "chatgpt/NonIdiomatic/"
    # save_complicated_code_dir_root = util.data_root + "NonIdiomatic/find_code_snippets/"
    save_complicated_code_dir = save_complicated_code_dir_root + "sample_methods/"
    file_name = "abstract_ass_tar_consecutive"
    samples = util.load_pkl(save_complicated_code_dir_root, "methods_sample_10000")  # methods_sample
    # samples_methods=[tuple(e) for e in samples[:]]
    # print(samples_methods[0])
    samples_methods=[tuple(other+[ast.unparse(ast.parse(e))]) for *other,e in samples[:]]

    # for i, s in enumerate(samples_methods[0]):
    #     print("i,sample: ", i, s)
    idiom = "fstring"
    file_name = "gpt_fstring_res"  # "direct_refactor_with_stmt_instr_sample_methods"
    fstring_res=util.load_pkl(save_complicated_code_dir_root + idiom + "/",
                  file_name)

    idiom = "chained_assignment"
    file_name = "gpt_chain_assign_res"
    ass_same_value_res=util.load_pkl(save_complicated_code_dir_root + idiom + "/",
                  file_name)

    idiom = "with_stmt"
    file_name = "gpt_with_res_sample_methods"
    with_res=util.load_pkl(save_complicated_code_dir_root + idiom + "/",
                  file_name)

    idiom = "enumerate"
    file_name = "gpt_enumerate_res_sample_methods"
    enumerate_res=util.load_pkl(save_complicated_code_dir_root + idiom + "/",
                  file_name)

    csv_res=[]
    for ind, sample in enumerate(enumerate_res):
        repo_name, file_html, old_path, class_name, method_code, old_code, refactor_code, flag_can_refac = sample
        method_code = ast.unparse(ast.parse(method_code))
        if flag_can_refac:
            print("refactor_code: ", refactor_code)
            tuple_e = [repo_name, file_html, old_path, class_name, method_code,old_code,refactor_code]
            csv_res.append(tuple_e)
            # if tuple_e in samples_methods:
            #     samples_methods.remove(tuple_e)
    util.save_csv(
        save_complicated_code_dir_root + idiom+"/" + file_name + "_gd.csv",
        csv_res,
        ["repo_name", "file_path", "file_html", "class_name", "me_code", "old_code", "new_code"
         "acc"])
    file_name="our_method_res_"+idiom
    util.save_pkl(save_complicated_code_dir_root+idiom+"/",
                  file_name,
                  csv_res)
    '''
    all_res=fstring_res+ass_same_value_res+with_res+enumerate_res
    refact_res=[]
    methods_set=[]
    for ind, sample in enumerate(all_res):
        repo_name, file_html, old_path, class_name, method_code, old_code,refactor_code,flag_can_refac = sample
        method_code= ast.unparse(ast.parse(method_code))
        if flag_can_refac:
            print("refactor_code: ",refactor_code)
            refact_res.append(sample)
            tuple_e=(repo_name, file_html, old_path, class_name, method_code)
            methods_set.append(tuple_e)
            if tuple_e in samples_methods:
                samples_methods.remove(tuple_e)

    print("len of refact_res: ",len(refact_res))
    print("len of methods_set: ",len(set(methods_set)))
    expr_methods=samples_methods[:65]+list(set(methods_set))
    print("total methods: ",len(set(samples_methods)))
    file_name="new_idiom_methods_600"
    util.save_pkl(save_complicated_code_dir_root,
                      file_name,
                      expr_methods)
    print("len of methods: ",len(expr_methods))

    file_name="new_idiom_methods_600"
    util.save_csv(
        save_complicated_code_dir_root +file_name + ".csv",
        expr_methods,
        ["repo_name", "file_path", "file_html", "class_name", "me_code", "old_code", "new_code", "bool_code",
         "chatGPT_code", "if_correct", "reversed_code", "non_replace_var_refactored_code", "refactored_code", "acc",
         "instruction", "sys_msg", "exam_msg", "user_msg"])
    '''




