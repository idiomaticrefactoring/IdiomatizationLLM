import ast,chatgpt_util
# For example,
# for the code:
#  sum(a[0],a[1],b),
# the non-idiomatic Python code are a[0],a[1]
def instr_find():

    real_instruction = '''
How to find non-idiomatic Python code that can refactored with star-in-fun-call'''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg,model="gpt-3.5-turbo")
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
def instr_find_2():

    real_instruction = '''
What is the context (corresponding AST nodes) that non-idiomatic Python code that can refactored with star-in-fun-call?'''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
def instr_find_3():

    real_instruction = '''
What is compositions that non-idiomatic Python code that can refactored with star-in-fun-call that should be in a function calls?'''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
def instr_find_composition():

    real_instruction = '''
In a function call, what does non-idiomatic Python code that can refactored with star-in-fun-call consists of?
For example,
for the given function call sum(a[0],a[1],b),
the non-idiomatic Python code consists of a[0],a[1]'''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
def instr_replace():

    real_instruction = '''
Write Python code to replace a given substring within a given string with a given new substring
    '''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg,model="gpt-3.5-turbo")
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])

if __name__ == '__main__':
    # instr_whether_is_use_var()
    # instr_extract_code_snippets()
    # instr_get_line_number()
    # instr_whether_is_use_var()
    # instr_whether_is_use_var_2()
    # instr_find_assign()
    # instr_is_assign()
    # instr_is_target_subscript_assign()
    # instr_subscript_value_from_subscript()
    # instr_extract_func_specified_name()
    # instr_stmt_fun_call_is_given_string()
    # instr_extract_func_specified_name_from_tree()
    # instr_code_start_line()
    # instr_1()
    # instr_extract_first_line()
    # instr_for_determine_func()
    # instr_all_consec_ass()
    # instr_all_consec_ass_constant()
    # instr_all_consec_ass_constant()
    # instr_all_ass_constant_consecutive()
    # instr_all_ass_constant_consecutive_simply()
    # instr_all_ass_sunscript_simply()
    # instr_find_FormattedValue()
    # instr_replace_iter_for()
    # instr_replace_target_for()
    # instr_find()
    instr_replace()
    # instr_find_3()
    # instr_find_composition()

