import os,sys
import struct
import traceback
code_dir = "/".join(os.path.abspath(__file__).split("/")[:-2]) + "/"
print("code path: ",code_dir)
sys.path.append(code_dir)
import chatgpt_util,random,chat_gpt_ast_util
import openai, tiktoken,ast,util
import ast
def instr_for_no_enumerate():
    real_instruction = '''
Write Python code to determine whether a given for node whose iterated object is an enumerate function or not in Python
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
    instr_for_no_enumerate()
    # tree=ast.parse(code)
    # all_nodes=chat_gpt_ast_util.extract_function_calls_from_tree(tree,"open")
    # for node in all_nodes:
    #     stmt=chat_gpt_ast_util.extract_function_call_stmt_from_tree(tree,node)
    #     # if isinstance(stmt,ast.With):
    #     #     continue
    #     body=chat_gpt_ast_util.find_parent_node(stmt,tree)
    #
    #     print("node: ",ast.unparse(node))
    #     print("stmt: ",ast.unparse(stmt))
    #     print("body: ",ast.unparse(body))
