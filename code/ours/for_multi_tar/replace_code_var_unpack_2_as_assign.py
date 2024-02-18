
import copy

'''
Python how to insert a string at the first occurrence of a substring of a string
'''
'''
You can use the `index()` method to find the index of the first occurrence of a substring in a string, and then use string concatenation to insert the new string at that index. Here's an example:

```
original_string = "hello world"
substring = "world"
new_string = "beautiful "

index = original_string.index(substring)
new_string_at_index = original_string[:index] + new_string + original_string[index:]

print(new_string_at_index)  # output: "hello beautiful world"
```

In this example, we first define the original string and the substring we want to find. We then use the `index()` method to find the index of the first occurrence of the substring in the original string. We then use string concatenation to insert the new string at that index, by slicing the original string into two parts (before and after the index) and concatenating the new string in between. Finally, we print the resulting string.
'''
def insert_first_occur(substring,new_string,original_string):

    index = original_string.index(substring)
    new_string_at_index = original_string[:index] + new_string + original_string[index:]
    return new_string_at_index
'''
Python how to insert a string after the first occurrence of a substring of a string
'''

'''
You can use the `replace()` method to replace the first occurrence of a substring with a new string. Here's an example:

```
string = "hello world"
substring = "l"
new_string = "123"

index = string.find(substring) + len(substring)
result = string[:index] + new_string + string[index:]

print(result)
```

Output:
```
hel123lo world
```

Explanation:
- `string.find(substring)` returns the index of the first occurrence of the substring in the string.
- `index = string.find(substring) + len(substring)` calculates the index of the character after the first occurrence of the substring.
- `string[:index]` returns the substring before the first occurrence of the substring.
- `string[index:]` returns the substring after the first occurrence of the substring.
- `result = string[:index] + new_string + string[index:]` concatenates the three substrings with the new string in the middle.
'''
def insert_after_first_occur(substring,new_string,string):

    index = string.find(substring) + len(substring)
    result = string[:index] + new_string + string[index:]
    return result

'''
Python how to replace the first occurrence of a substring within a string with a new substring.  
'''

'''
You can use the `replace()` method with a `count` parameter of 1 to replace only the first occurrence of a substring within a string. Here's an example:

```
string = "hello world"
substring = "l"
new_substring = "z"

new_string = string.replace(substring, new_substring, 1)

print(new_string)  # "hezlo world"
```

In this example, we replace the first occurrence of the substring "l" with the new substring "z" in the string "hello world". The resulting string is "hezlo world".
'''
def replace_first_occur(substring,replace_string,string):
    new_string = string.replace(substring,replace_string,1 )
    return new_string

'''
Python how to replace all occurrences of a substring within a string with a new substring.
'''
'''
You can use the `replace()` method to replace all occurrences of a substring within a string with a new substring. Here's an example:

```
string = "Hello, world! Hello, Python!"
new_string = string.replace("Hello", "Hi")
print(new_string)
```

Output:
```
Hi, world! Hi, Python!
```

In this example, we replaced all occurrences of the substring "Hello" with the new substring "Hi". The `replace()` method returns a new string with the replacements made. Note that the original string is not modified.
'''

def replace(substring,replace_string,string):
    new_string = string.replace(substring,replace_string )
    return new_string
'''
Python how to remove all occurrences of a substring within a string
'''

'''
There are several ways to remove all occurrences of a substring within a string in Python. Here are a few examples:

1. Using the replace() method:

```python
string = "Hello World"
substring = "l"
new_string = string.replace(substring, "")
print(new_string) # Output: Heo Word
```

2. Using the re.sub() method from the re module:

```python
import re

string = "Hello World"
substring = "l"
new_string = re.sub(substring, "", string)
print(new_string) # Output: Heo Word
```

3. Using a loop and string slicing:

```python
string = "Hello World"
substring = "l"
new_string = ""

for i in range(len(string)):
    if string[i:i+len(substring)] != substring:
        new_string += string[i]

print(new_string) # Output: Heo Word
```

All of these methods will remove all occurrences of the specified substring within the original string.
'''
def remove(substring,string):
    new_string = string.replace(substring,'')
    return new_string

def add(substring,string):
    new_string = string.replace(substring,'')
    return new_string
import os,sys
import struct
import traceback
code_dir = "/".join(os.path.abspath(__file__).split("/")[:-2]) + "/"
print("code path: ",code_dir)
sys.path.append(code_dir)
import chatgpt_util,random
import openai, tiktoken,ast,util
import ast,for_multi_tar_util
import extract_for,extract_loop_var_name,extract_subscript,determine_subscript_name
def parse_mapping(response,var):
    new_target = ""
    new_mapping = dict()
    print(">>>>>>>>>>>response, var: ",response, "\n",var)
    target_str=response.split("Iterable Unpacking:")[1]
    mapping_str=""
    if "Variable Mapping:" in response:
        target_str,mapping_str=target_str.split("Variable Mapping:")
    elif "variable mapping:" in response:
        target_str,mapping_str=target_str.split("variable mapping:")
    if "Explanation:" in response:
        mapping_str=mapping_str.split("Explanation:")[0]
    for e in target_str.split("\n"):
        if "=" in e:
            left, right = e.split("=")
            left, right = left.strip(), right.strip()
            print("right: ", right)
            last_ele = left.split(",")[-1].strip()
            if last_ele=='_':
                left = left[:-1]+"_"+last_ele
            elif not last_ele.startswith("*") and "*" not in left:
                left += ", *_"
            if right == var.strip():
                new_target = "    "+left + " = " +right+"\n"
    for e in mapping_str.strip().split("\n"):
        map_list = e.split(":")
        key, value = map_list[0].strip(), "".join(map_list[1:]).strip()
        if "-" in key:
            key=key.split("-")[-1].strip()
        new_mapping[key] = value


    flag= bool(new_target and new_mapping)
    print("flag,new_target,new_mapping: ",flag,new_target)
    return flag,new_target,new_mapping

def parse(samples,var_unpack_response):
    reponse_list = []
    method_code_list = []
    for ind_sampl, sample_method in enumerate(samples):
        for code in sample_method:
            # repo_name, old_path, file_html, class_name,me_name, old_list, new_tree,\
            #     old_code,new_code, method_code=code
            # break
            *other, old_list, new_tree, \
            old_code, new_code, method_code = code
            # print("method_code: ", method_code)
            method_code_list.append([*other, old_list, new_tree, old_code, new_code, method_code])
            break
    start = 0
    for *other, old_list, new_tree, old_code, new_code, method_code in method_code_list:
        tmp_list = extract_for.get_for(method_code)

        for bool_node in tmp_list:
            extract_subscript.subscripts = []
            extract_subscript.find_subscripts(bool_node)
            print(">>>>>>>>>>loop: ",ast.unparse(bool_node))
            vars = extract_loop_var_name.extract_iterated_variables(bool_node)
            bool_node_string=ast.unparse(bool_node)
            old_code_string=ast.unparse(bool_node)
            target_string=ast.unparse(bool_node.target)
            new_target_string=copy.deepcopy(target_string)
            flag_can_refactor=0
            count=0
            response_str_list=[]
            print(">>>>>vars: ", vars)

            for var in vars:
                # print(">>>>>var: ", var,vars,extract_subscript.subscripts)
                elements_list = set([])
                for sub in extract_subscript.subscripts:
                    if determine_subscript_name.is_subscript_var_name(sub, var):
                        elements_list.add(ast.unparse(sub))
                elements_list = sorted(elements_list)
                if elements_list:
                    response=var_unpack_response[start+count][-1]["choices"][0]["message"]["content"]
                    response_str_list.append(response)
                    flag,new_target,new_mapping=parse_mapping(response, var)
                    print(">>>>>>>>>>flag,new_target,new_mapping: ",flag,new_target,new_mapping)
                    if flag:
                        flag_can_refactor=1
                        for key,value in new_mapping.items():
                            old_code_string=replace(value,key ,old_code_string)
                        # new_target_string=replace(var, new_target, new_target_string)
                        old_code_string = insert_after_first_occur("\n", new_target, old_code_string)
                    count+=1

            if count!=0:

                if flag_can_refactor:
                    try:
                        print(">>>>>>>>>>new_code_string: \n",old_code_string)

                        # new_code_string=replace_first_occur(" "+target_string, " "+new_target_string, old_code_string)
                        new_code_string=ast.unparse(ast.parse(old_code_string))
                        reponse_list.append([True,new_code_string,new_code,bool_node_string,method_code,*other,"***************\n".join(response_str_list)])
                    except:
                        reponse_list.append([False,traceback.print_exc(),new_code,bool_node_string,method_code,*other,"***************\n".join(response_str_list)])

                else:
                    print(">>>>>>>>>>new_code_string: \n","It cannot be refactored by var unpacking")
                    reponse_list.append([False,"It cannot be refactored by var unpacking",new_code,bool_node_string,method_code,*other,"***************\n".join(response_str_list)])

            start += count
    return reponse_list
if __name__ == '__main__':
    idiom = "for multi targets"
    idiom = "_".join(idiom.split(" "))
    save_complicated_code_dir_root = util.data_root + "chatgpt/NonIdiomatic/"
    # save_complicated_code_dir_root = util.data_root + "NonIdiomatic/find_code_snippets/"
    save_complicated_code_dir = save_complicated_code_dir_root + "sample_methods/"

    samples = util.load_pkl(save_complicated_code_dir, "sample_methods_" + idiom)
    file_name="whether_can_var_unpack_for_subscript_stmt_instr_explain_4_new_all_2"#"whether_can_var_unpack_for_subscript_stmt_instr_explain_4_new_all"#"whether_can_var_unpack_for_subscript_stmt_instr_explain_4_new"
    mapping = util.load_pkl(save_complicated_code_dir_root + idiom + "/", file_name)
    response_list=parse(samples, mapping)
    file_name="replace_code_var_unpack"
    # util.save_pkl(save_complicated_code_dir_root + idiom + "/",
    #               file_name,
    #               response_list)
    # util.save_csv(
    #     save_complicated_code_dir_root + idiom + "/" + file_name+".csv",
    #     response_list,
    #     ["repo_name", "file_path", "file_html", "class_name", "me_name", "me_code", "old_code", "new_code", "bool_code",
    #      "chatGPT_code", "if_correct", "reversed_code", "non_replace_var_refactored_code", "refactored_code", "acc",
    #      "instruction", "sys_msg", "exam_msg", "user_msg"])
    refactor_code_list = util.load_pkl(save_complicated_code_dir_root + idiom + "/",
                                       file_name)
    # print("final refactor_code: ", refactor_code_list[124])
    # # '''
    new_refactor_code_list = [e[1] for e in refactor_code_list]
    #
    # csv_res_list = for_multi_tar_util.get_acc_2(samples, refactor_code_list, new_refactor_code_list)
    csv_res_list = for_multi_tar_util.get_acc_3(samples, refactor_code_list, new_refactor_code_list)

    acc_file_name = file_name + "_get_acc_new_as_assign.csv"  # "rewrite_instr_replace_with_real_var_all.csv"#"rewrite_instr_replace_with_real_var.csv"
    acc_file_name = file_name + "_get_acc_new_as_assign_acc_3.csv"  # "rewrite_instr_replace_with_real_var_all.csv"#"rewrite_instr_replace_with_real_var.csv"

    print("len: ", len(samples))
    # util.save_csv(
    #     save_complicated_code_dir_root + idiom + "/" + acc_file_name ,
    #     csv_res_list,
    #     ["repo_name", "file_path", "file_html", "class_name", "me_name", "me_code", "old_code", "new_code", "bool_code",
    #      "chatGPT_code", "if_correct", "reversed_code", "non_replace_var_refactored_code", "refactored_code", "acc",
    #      "instruction", "sys_msg", "exam_msg", "user_msg"])
    #





