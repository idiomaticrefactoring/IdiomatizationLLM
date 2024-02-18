import os, sys
import struct
import traceback

code_dir = "/".join(os.path.abspath(__file__).split("/")[:-2]) + "/"
print("code path: ", code_dir)
sys.path.append(code_dir)
import chatgpt_util, random
import openai, tiktoken, ast, util
import ast
import dict_util,util_rewrite
#direct_refactor_dict_comprehension_instr_add_one_example_instr3_2_real_examp_all_improve.py
if __name__ == '__main__':
    '''
    Variable unpacking in for statements in Python is a way to assign values to multiple variables at once from an iterable object such as a list, tuple, or dictionary. It allows you to iterate over the iterable and assign each value to a separate variable in a single line of code. 
    '''
    user_instr = '''
Refactor the following Python code with dict comprehension in Python as much as possible. Do not refactor other part of code.

Python code:
{{code}}

response format:
Answer: You respond with Yes or No for whether the code can be refactored with dict comprehension.
Information: If your answer is Yes, you give the refactored code. Otherwise, you respond with None. Please explain it.
'''
    examples = [
['''
Refactor the following Python code with dict comprehension in Python as much as possible. Do not refactor other part of code.

Python code:
for param in DockerAPIInterface._kwopt_to_param_names(map_spec, key):
    zj[param] = value
        
response format:
Answer: You respond with Yes or No for whether the code can be refactored with dict comprehension.
Information: If your answer is Yes, you give the refactored code. Otherwise, you respond with None. Please explain it.
''',
'''
Answer: Yes
Information:
zj = {param:value for param in DockerAPIInterface._kwopt_to_param_names(map_spec, key)}
'''],
['''
Refactor the following Python code with dict comprehension in Python as much as possible. Do not refactor other part of code.

Python code:
for (num, (entry_title, media_kind, download_text)) in enumerate(re.findall('(?s)<p[^>]+class="infotext"[^>]*>\\s*(?:<a[^>]+>)?\\s*<strong>(.+?)</strong>.*?</p>.*?%s' % DOWNLOAD_REGEX, webpage), 1):
    zj[num]={'id': '%s-%d' % (display_id, num), 'title': '%s' % entry_title, 'formats': self._extract_formats(download_text, media_kind)}

response format:
Answer: You respond with Yes or No for whether the code can be refactored with dict comprehension.
Information: If your answer is Yes, you give the refactored code. Otherwise, you respond with None. Please explain it.
''',
'''
Answer: Yes
Information:
zj = {num:{'id': '%s-%d' % (display_id, num), 'title': '%s' % entry_title, 'formats': self._extract_formats(download_text, media_kind)} for (num, (entry_title, media_kind, download_text)) in enumerate(re.findall('(?s)<p[^>]+class="infotext"[^>]*>\\s*(?:<a[^>]+>)?\\s*<strong>(.+?)</strong>.*?</p>.*?%s' % DOWNLOAD_REGEX, webpage), 1)}}
'''],
['''
Refactor the following Python code with dict comprehension in Python as much as possible. Do not refactor other part of code.

Python code:
for (index, (first, second)) in enumerate(zip(x_shape[0:-2], self.dx.shape[0:-2])):
    if first != second:
        zj[r['id'], entity_type, r['domain_id']]=index
        
response format:
Answer: You respond with Yes or No for whether the code can be refactored with dict comprehension.
Information: If your answer is Yes, you give the refactored code. Otherwise, you respond with None. Please explain it.
''',
'''
Answer: Yes
Information:
zj = {r['id'], entity_type, r['domain_id']:index for (index, (first, second)) in enumerate(zip(x_shape[0:-2], self.dx.shape[0:-2])) if first != second}
'''],
['''
Refactor the following Python code with dict comprehension in Python as much as possible. Do not refactor other part of code.

Python code:
for k in keys:
    zj[k] = concatenate(list((a[k] for a in arrays)), axis=axes[0])
        
response format:
Answer: You respond with Yes or No for whether the code can be refactored with dict comprehension.
Information: If your answer is Yes, you give the refactored code. Otherwise, you respond with None. Please explain it.
''',
'''
Answer: Yes
Information:
zj = {k:concatenate(list((a[k] for a in arrays)), axis=axes[0]) for k in keys}
''']

]
    #for param in DockerAPIInterface._kwopt_to_param_names(map_spec, key):

    idiom = "dict_comprehension"
    save_complicated_code_dir_root = util.data_root + "chatgpt/NonIdiomatic/"
    # save_complicated_code_dir_root = util.data_root + "NonIdiomatic/find_code_snippets/"
    save_complicated_code_dir = save_complicated_code_dir_root + "sample_methods/"

    samples = util.load_pkl(save_complicated_code_dir, "sample_methods_" + idiom)

    # random.seed(2023)
    #
    # samples = random.sample(samples, 70)
    file_name = "direct_refactor_set_comprehension_instr_add_one_example_instr3_2_real_examp_all"  # "extract_arithmetic_seq_from_arguments_instr3_all"  # "whether_can_var_unpack_for_subscript_stmt_instr_explain_4_new"
    file_name = "direct_refactor_set_comprehension_instr_add_one_example_instr3_2_real_examp_all_new"  # "extract_arithmetic_seq_from_arguments_instr3_all"  # "whether_can_var_unpack_for_subscript_stmt_instr_explain_4_new"
    file_name = "find_def_stmt_for_a_node_all_filter_for_improve_all"
    file_name = "find_def_stmt_improve_all_3"
    # file_name = "extract_arithmetic_seq_from_abstract_same_subscript_value_arguments_instr7_all_2_sample"  # "extract_arithmetic_seq_from_arguments_instr3_all"  # "whether_can_var_unpack_for_subscript_stmt_instr_explain_4_new"
    samples = util.load_pkl(save_complicated_code_dir_root + idiom + "/",file_name)
    samples_def = util.load_pkl(save_complicated_code_dir_root + idiom + "/",file_name)

    '''
    reponse_list = dict_util.get_response_directly_refactor_from_def_stmt_abstract_obj_filter_for(user_instr, examples, samples[:],
                                                        sys_msg="You are a helpful assistant.")
    # util.save_pkl(save_complicated_code_dir_root + "chain_comparison_bool_compare/",
    #               "abstract_one_compare_instr",
    #               reponse_list)
    # util.save_pkl(save_complicated_code_dir_root+ idiom + "/",
    #               "extract_comparators_one_compare_instr",
    #               reponse_list)
    # file_name="direct_refactor_dict_comprehension_instr_from_def_stmt_from_abstract_var_add_examp_new_filter_for_improve_all_2"
    file_name = "direct_refactor_dict_comprehension_improve_new"
    util.save_pkl(save_complicated_code_dir_root + idiom + "/",
                  file_name,
                  reponse_list)
    '''
    file_name="direct_refactor_dict_comprehension_instr_from_def_stmt_from_abstract_var_add_examp_new_filter_for_improve_all_2"
    file_name="direct_refactor_dict_comprehension_improve_new"

    reponse_list=[]

    samples = util.load_pkl(save_complicated_code_dir_root + idiom + "/",file_name)
    print("len of samples: ",len(samples))
    w=0
    except_error = 0

    for ind,sample in enumerate(samples):
        if ind==0:
            for ind_e,e in enumerate(sample):
                print("ind_e,e: ",ind_e,e)
       # abstract_me_code,me_code, old_code, ass_flag, ass_stmt,flag_use, object_var, *other])

        abstract_me_code,me_code,old_code,ass_flag, ass_stmt,flag_use, object_var, repo_name,old_path, file_html, class_name,me_name,new_code,method_code,_,response=sample
        if "for head in self.heads:" not in old_code:#for key in alternatives: for (i, arg) in enumerate(gate.gate_args):for (i, arg) in enumerate(gate.gate_args):
            continue
        flag_use=samples_def[ind][4]
        if not object_var:
            w+=1
            continue

        # print("old_path: ",old_path)
        # repo_name=old_path.split("/")[8].strip()
        # print("repo_name: ",repo_name)
        #
        # break
        content = response["choices"][0]["message"]["content"]
        print("Content: ", content, abstract_me_code)

        flag_can_refactor, refactor_code=dict_util.parse_refactor_code(content)
        try:
            if flag_can_refactor:
                refactor_code = util_rewrite.replace("zj", object_var, refactor_code)
                if flag_use:
                    refactor_code=util_rewrite.replace_first_occur(object_var+" =",object_var+".update(",refactor_code)+")"
                # print("refactor_code: ", refactor_code, me_code)
                e = [repo_name, old_path, file_html, class_name, me_name, method_code, me_code, ast.unparse(ast.parse(refactor_code)),ass_flag, ass_stmt,content]

                reponse_list.append(e)
            else:
                print("Content: ",content,abstract_me_code)
        except:
            except_error+=1
    '''
    util.save_pkl(save_complicated_code_dir_root + idiom + "/",
                  "gpt_result_refactor_new" + idiom,
                  reponse_list)
    # util.save_pkl(save_complicated_code_dir_root + idiom + "/",
    #               "gpt_result_from_def_stmt_from_abstract_var_all_add_examp_new_filter_for_improve_all_"+idiom,
    #               reponse_list)
    print("no obj var: ",w,except_error)
    print("len of reponse_list: ",len(reponse_list))
   '''