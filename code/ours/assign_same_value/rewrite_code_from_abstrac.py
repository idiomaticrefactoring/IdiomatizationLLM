import os,sys
import struct
import traceback
code_dir = "/".join(os.path.abspath(__file__).split("/")[:-2]) + "/"
print("code path: ",code_dir)
sys.path.append(code_dir)
import chatgpt_util,random
import openai, tiktoken,ast,util,copy
import ast,ass_same_value_util,util_rewrite
def get_acc(samples,new_python_code_list):
    offset=0#-2
    reponse_list=[]
    ground_truth_list=[]
    for ind_sampl, sample_method in enumerate(samples):
        for code in sample_method:
            repo_name, old_path, file_html, class_name,me_name, old_list, new_tree,\
                old_code,new_code, method_code=code
            # break
            *other, old_list, new_tree, \
            old_code, new_code, method_code = code
            try:
                ele = [repo_name, old_path, file_html, class_name, me_name, method_code,ast.unparse(ast.parse(old_code)), ast.unparse(ast.parse(new_code))]
            except:
                continue
            ground_truth_list.append(ele)
            # print("new_code:\n",ast.unparse(old_list[0][-2]),new_code)
    #         for i,e in enumerate(ele):
    #             print("i,e: ",i,e)
    #         break
    #     # if ind_sampl>2:
    #     break
    print("len of ground_truth_list: ",len(ground_truth_list))
    # return 0

    # ground_copy_truth_list = ground_truth_list
    ground_copy_truth_list=copy.deepcopy(ground_truth_list)
    ground_copy_truth_list=[e[offset:] for e in ground_copy_truth_list]
    predict_res=[]
    acc=0
    pre=0
    now_list=[]
    gpt_all_code_list=[]
    for ind, sample in enumerate(new_python_code_list):
        # print("sample: ",sample)
        # for i,s in enumerate(sample):
        #     print("i,sample: ",i,s)
        # return 0
        flag_can_refactor, refactor_code, abstract_code, symbols_map, me_code, _, repo_name, old_path, file_html, class_name,me_name,_,method_code,*other=sample
        # reponse_list.append([ele_str, abstract_me_code, value, abstract_value, *other])
        # reponse_list.append([0, "Cannot refactor", element_str, slice_str, method_code, me_code, *other])
        # if not flag_can_refactor:
        #     continue
        print("refactor_code: ",refactor_code)
        # flag_can_refactor, refactor_code,element_seq_str, slice_str,method_code,me_code,_,_,repo_name, old_path, file_html, class_name,me_name,*other = sample
        # bool_code, old_code, repo_name, old_path, file_html, class_name,me_name,*other, new_code, method_code, info, response = sample
        old_refactor_code=refactor_code
        # if flag_can_refactor:
        #     try:
        #         refactor_code = ast.unparse(ast.parse(slice_str))
        #         print("me_code,refactor_code:\n",me_code,refactor_code)
        #     except:
        #         refactor_code =traceback.print_exc()
        try:
            e=[repo_name, old_path, file_html, class_name,me_name,method_code,
               ast.unparse(ast.parse(me_code)),
               ast.unparse(ast.parse(refactor_code))]
            if "Cannot refactor" not in refactor_code:
                gpt_all_code_list.append(e)
        except:
            continue
        # print("predict ele: ", e)

        # predict_res.append(e)
        ground_pre_list=[e[offset:-1] for e in ground_copy_truth_list]
        if e in ground_copy_truth_list:
                index = ground_copy_truth_list.index(e)
                now_list.append(index)
                 # e[-1]=old_refactor_code
                e.extend([abstract_code])
                e.append(ground_copy_truth_list[index][-1])
                e.append(1)
                ground_copy_truth_list.pop(index)
                acc+=1
                pre+=1

        elif e[:-1] in ground_pre_list:
            # e[-1] = old_refactor_code
            index=ground_pre_list.index(e[:-1])
            now_list.append(index)
            e.extend([abstract_code])
            e.append(ground_copy_truth_list[index][-1])
            e.append(0)
            ground_copy_truth_list.pop(index)
        else:
            # continue
            e[-1] = old_refactor_code
            e.extend([abstract_code])
            e.append("Cannot refactor")
            e.append(-1)
            # continue
            # acc += 1
        predict_res.append(e + other)

    predict_res.append(["NOFOUND"])

    for ind,e in enumerate(ground_copy_truth_list):
            predict_res.append(e+[0])
    print("acc: ",acc,len(predict_res),len(gpt_all_code_list),len(ground_truth_list))
    print("acc: ",acc,len(predict_res),acc/len(ground_truth_list))
    print("precision: ",pre,len(predict_res),pre/len(ground_truth_list),len(ground_truth_list))

    return predict_res,ground_truth_list,gpt_all_code_list

def get_acc_2(samples,new_python_code_list):
    offset=0#-2
    reponse_list=[]
    ground_truth_list=[]
    for ind_sampl, sample_method in enumerate(samples):
        for code in sample_method:
            repo_name, old_path, file_html, class_name,me_name, old_list, new_tree,\
                old_code,new_code, method_code=code
            # break
            *other, old_list, new_tree, \
            old_code, new_code, method_code = code
            try:
                ele = [repo_name, old_path, file_html, class_name, me_name, method_code,ast.unparse(ast.parse(old_code)), ast.unparse(ast.parse(new_code))]
            except:
                continue
            ground_truth_list.append(ele)
            # print("new_code:\n",ast.unparse(old_list[0][-2]),new_code)
    #         for i,e in enumerate(ele):
    #             print("i,e: ",i,e)
    #         break
    #     # if ind_sampl>2:
    #     break
    print("len of ground_truth_list: ",len(ground_truth_list))
    # return 0

    # ground_copy_truth_list = ground_truth_list
    ground_copy_truth_list=copy.deepcopy(ground_truth_list)
    ground_copy_truth_list=[e[offset:] for e in ground_copy_truth_list]
    predict_res=[]
    acc=0
    pre=0
    now_list=[]
    for ind, sample in enumerate(new_python_code_list):
        # print("sample: ",sample)
        # for i,s in enumerate(sample):
        #     print("i,sample: ",i,s)
        # return 0
        flag_can_refactor, refactor_code, abstract_code, symbols_map, me_code, _, repo_name, old_path, file_html, class_name,me_name,_,method_code,*other=sample
        # reponse_list.append([ele_str, abstract_me_code, value, abstract_value, *other])
        # reponse_list.append([0, "Cannot refactor", element_str, slice_str, method_code, me_code, *other])
        if not flag_can_refactor:
            continue
        print("refactor_code: ",refactor_code)
        # flag_can_refactor, refactor_code,element_seq_str, slice_str,method_code,me_code,_,_,repo_name, old_path, file_html, class_name,me_name,*other = sample
        # bool_code, old_code, repo_name, old_path, file_html, class_name,me_name,*other, new_code, method_code, info, response = sample
        old_refactor_code=refactor_code
        # if flag_can_refactor:
        #     try:
        #         refactor_code = ast.unparse(ast.parse(slice_str))
        #         print("me_code,refactor_code:\n",me_code,refactor_code)
        #     except:
        #         refactor_code =traceback.print_exc()
        try:
            e=[repo_name, old_path, file_html, class_name,me_name,method_code,
               ast.unparse(ast.parse(me_code)),
               ast.unparse(ast.parse(refactor_code))]
        except:
            continue
        # print("predict ele: ", e)

        # predict_res.append(e)
        ground_pre_list=[e[offset:-1] for e in ground_copy_truth_list]
        if e in ground_copy_truth_list:
                index = ground_copy_truth_list.index(e)
                now_list.append(index)
                 # e[-1]=old_refactor_code
                e.extend([abstract_code])
                e.append(ast.unparse(ast.parse(ground_copy_truth_list[index][-1])))
                e.append(1)
                ground_copy_truth_list.pop(index)
                acc+=1
                pre+=1

        elif e[:-1] in ground_pre_list:
            # e[-1] = old_refactor_code
            index=ground_pre_list.index(e[:-1])
            now_list.append(index)
            e.extend([abstract_code])
            e.append(ast.unparse(ast.parse(ground_copy_truth_list[index][-1])))
            e.append(0)
            ground_copy_truth_list.pop(index)
        else:
            # continue
            e[-1] = old_refactor_code
            e.extend([abstract_code])
            e.append("Cannot refactor")
            e.append(-1)
            # continue
            acc += 1
        predict_res.append(e + other)

    predict_res.append(["NOFOUND"])

    for ind,e in enumerate(ground_copy_truth_list):
            predict_res.append(e+[0])
    print("acc: ",acc,len(predict_res),acc/len(ground_truth_list))
    print("precision: ",pre,len(predict_res),pre/len(ground_truth_list))

    return predict_res
def rewrite_code(samples):
    reponse_list = []
    count=0
    for abstract_code, symbols_map, me_code, old_code, *other, new_code, method_code, _, response in samples:
        if "labels = utils.get_batch_label(dataset, idx)" not in me_code:#self.tokenizer = tokenizer self._fn = None slice2[axis] = slice(None, -1) doc = self._download_xml(self.fc0 = layers.fc(
            continue
        content = response["choices"][0]["message"]["content"]
        print("content: ",content)
        flag,new_code=ass_same_value_util.parse_code(content)
        print("flag,new_code: ",flag,new_code)

        if flag:
            print("new_code:",new_code)
            print("symbols_map: ",symbols_map)
            for key,value in symbols_map.items():
                new_code=util_rewrite.replace(key,value,new_code)
                print(">>>new_code: ",new_code)

            print("new_code: ",abstract_code,"******\n",new_code)
            count+=1
            reponse_list.append([flag,new_code,abstract_code, symbols_map, me_code, old_code, *other, new_code, method_code])
        else:
            print("come here: ",abstract_code,"******\n",new_code)

            reponse_list.append([flag,"'Cannot refactor'",abstract_code, symbols_map, me_code, old_code, *other, new_code, method_code])

        # break
    print("len of rewrite code: ",count,len(reponse_list))
    return reponse_list
def rewrite_code_2_no_abstract(samples):
    reponse_list = []
    count=0
    for me_code, old_code,bool_node, *other, new_code, method_code, _, response in samples:
        content = response["choices"][0]["message"]["content"]
        flag,new_code=ass_util.parse_code(content)
        if flag:

            print("new_code: ",new_code)
            count+=1
            reponse_list.append([flag,new_code, me_code, old_code, *other, new_code, method_code])
        else:
            reponse_list.append([flag,"Cannot refactor", me_code, old_code, *other, new_code, method_code])

        # break
    print("len of rewrite code: ",count,len(reponse_list))
    return reponse_list
if __name__ == '__main__':
    idiom = "assign_multiple_targets"
    save_complicated_code_dir_root = util.data_root + "chatgpt/NonIdiomatic/"
    # save_complicated_code_dir_root = util.data_root + "NonIdiomatic/find_code_snippets/"
    save_complicated_code_dir = save_complicated_code_dir_root + "sample_methods/"



    samples = util.load_pkl(save_complicated_code_dir_root + idiom + "/", "abstract_ass_instr")
    # extract_stmt_depend_ass_from_abstract_instr_7
    file_name = "direct_refactor_from_blocks_no_dependinstr_improve_depdend_4_4_examp_all"
    # file_name = "direct_refactor_from_blocks_no_dependinstr_improve_depdend_4_4_examp"
    # file_name = "direct_refactor_from_blocks_no_dependinstr_improve_depdend_2_4_examp_all"
    # file_name = "direct_refactor_from_blocks_no_dependinstr_improve_depdend_2_4_examp"#"direct_refactor_from_blocks_no_dependinstr_improve_depdend_2"#"direct_refactor_from_blocks_no_dependinstr_improve_depdend_no_abstract"#"direct_refactor_from_blocks_no_dependinst_improve_depend_all"#"direct_refactor_from_blocks_no_dependinst"  # "extract_arithmetic_seq_from_arguments_instr3_all"  # "whether_can_var_unpack_for_subscript_stmt_instr_explain_4_new"
    # file_name = "extract_arithmetic_seq_from_abstract_same_subscript_value_arguments_instr7_all_2_sample"  # "extract_arithmetic_seq_from_arguments_instr3_all"  # "whether_can_var_unpack_for_subscript_stmt_instr_explain_4_new"
    samples = util.load_pkl(save_complicated_code_dir_root + idiom + "/", file_name)
    print("len of samples: ",len(samples))

    # new_python_code_list=rewrite_code(samples)
    new_python_code_list=rewrite_code(samples)
    '''
    print("len of new_python_code_list: ",len(new_python_code_list))

    samples = util.load_pkl(save_complicated_code_dir, "sample_methods_" + idiom)

    # random.seed(2023)
    #
    # samples = random.sample(samples, 30)
    csv_res_list,ridiom_code_list,new_all_code_list=get_acc(samples, new_python_code_list)

    acc_file_name=file_name+"_get_acc.csv"#"direct_refactor_from_blocks_no_dependinstr_get_acc.csv"
    util.save_pkl(save_complicated_code_dir_root + idiom + "/",
                  file_name+"_get_acc",
                  csv_res_list)
    util.save_pkl(save_complicated_code_dir_root + idiom + "/",
                  "gpt_res_" + idiom,
                  new_all_code_list)
    util.save_pkl(save_complicated_code_dir_root + idiom + "/",
                  "ridiom_res_" + idiom,
                  ridiom_code_list)
    '''
    # ridiom_code_list = util.load_pkl(save_complicated_code_dir_root + idiom + "/", "ridiom_res_" + idiom)
    # new_all_code_list = util.load_pkl(save_complicated_code_dir_root + idiom + "/", "gpt_res_" + idiom)

    # util.save_csv(
    #     save_complicated_code_dir_root + idiom + "/" + acc_file_name,
    #     csv_res_list,
    #     ["repo_name", "file_path", "file_html", "class_name", "me_name", "me_code", "old_code", "chatGPT_code", "element_str",
    #      "slice_str", "truth_code"])
