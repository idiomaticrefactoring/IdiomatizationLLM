import os,sys
import struct
import traceback
code_dir = "/".join(os.path.abspath(__file__).split("/")[:-2]) + "/"
print("code path: ",code_dir)
sys.path.append(code_dir)
import chatgpt_util,random,chat_gpt_ast_util
import openai, tiktoken,ast,util
import ast
def instr_cfg():
    real_instruction = '''
    '''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])


if __name__ == '__main__':
    code='''def gener():
    f = open('output.log', 'a', encoding='utf-8')
    webinfo = Sqldb(dbname).query('select domain,ipaddr,title,server,apps,waf,os from webinfo')
    for i in webinfo:
        domain, ipaddr, title, server, apps, waf, os = i
    with open(filename, 'w') as f:
        for e in edges:
            f.write('%i;%i' % (e[0], e[1]))       
'''
    tree=ast.parse(code)
    all_nodes=chat_gpt_ast_util.extract_function_calls_from_tree(tree,"open")
    for node in all_nodes:
        stmt=chat_gpt_ast_util.extract_function_call_stmt_from_tree(tree,node)
        # if isinstance(stmt,ast.With):
        #     continue
        body=chat_gpt_ast_util.find_parent_node(stmt,tree)

        print("node: ",ast.unparse(node))
        print("stmt: ",ast.unparse(stmt))
        print("body: ",ast.unparse(body))


        # break
    # instr_1()
    # idiom = "call_star"
    # save_complicated_code_dir_root = util.data_root + "chatgpt/NonIdiomatic/"
    # # save_complicated_code_dir_root = util.data_root + "NonIdiomatic/find_code_snippets/"
    # save_complicated_code_dir = save_complicated_code_dir_root + "sample_methods/"
    #
    # samples = util.load_pkl(save_complicated_code_dir, "sample_methods_" + idiom)
    #
    # # extract_consecutive_subscripts(node)
    # # random.seed(2023)
    # # samples = random.sample(samples, 30)
    # file_name="abstract_same_value_all"#"whether_can_var_unpack_for_subscript_stmt_instr_explain_4_new"
    # reponse_list = call_star_util.abstract_consecutive(samples)
    # util.save_pkl(save_complicated_code_dir_root + idiom + "/",
    #               file_name,
    #               reponse_list)
    # instr_cfg()
    # # tree = ast.parse(code)
    # # target_node = ...  # the AST node you want to find the control flow for
    # # visitor = ControlFlowVisitor(target_node)
    # # visitor.visit(tree)
    # # print(visitor.control_flow)
    # code = '''
    # '''
    # nodes = get_for_2(code)
    # print("nodes: ", nodes)
    # for e in nodes:
    #     print("e: ", ast.unparse(e))
    '''
    fin_anno = open(os.path.join(parent, filename), 'r')
    bbox_list = []
    for (i, anno) in enumerate(fin_anno):
        if i == 0:
            continue
        anno = anno.strip('\n').split(' ')
        if anno[0] != 'person':
            continue
        x = math.floor(float(anno[1]))
        y = math.floor(float(anno[2]))
        width = math.ceil(float(anno[3]))
        height = math.ceil(float(anno[4]))
        width_vis = math.ceil(float(anno[8]))
        height_vis = math.ceil(float(anno[9]))
        if width_vis * height_vis / (width * height) < 0.2:
            continue
        bbox_list.append((x, y, width, height))
    if len(bbox_list) == 0:
        line += ',0,0'
        fout.write(line + '\n')
    else:
        bbox_line = ''
        for bbox in bbox_list:
            bbox_line += ',' + str(bbox[0]) + ',' + str(bbox[1]) + ',' + str(bbox[2]) + ',' + str(bbox[3])
        line += ',1,' + str(len(bbox_list)) + bbox_line
        fout.write(line + '\n')
    counter += 1
    print(counter)
    '''