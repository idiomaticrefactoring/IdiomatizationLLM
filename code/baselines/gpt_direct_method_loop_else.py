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
Refactor the following Python code with loop else. You give all code pairs where each pair consists of non-idiomatic Python code and the corresponding refactored code. You respond according to the response format.

Python code:
{{code}}

response format:
Answer: You respond with Yes or No for whether the code has non-idiomatic Python code that can be refactored with loop else.
Information: You respond with all code pairs where each pair consists of non-idiomatic code and the corresponding refactored code. Each pair splits with "******"
Non-Idiomatic Python code: You respond with identified non-idiomatic Python code that can be refactored with loop else.
Refactored Python code: You respond with the corresponding idiomatic Python code after refactoring the non-idiomatic code with loop else.
******
Non-Idiomatic code:...
Refactored code:...
'''
    examples = [
['''
Refactor the following Python code with loop else. You give all code pairs where each pair consists of non-idiomatic Python code and the corresponding refactored code. You respond according to the response format.

Python code:
def _get_rule_changes(rules, _rules):
    """
    given a list of desired rules (rules) and existing rules (_rules) return
    a list of rules to delete (to_delete) and to create (to_create)
    """
    to_delete = []
    to_create = []
    # for each rule in state file
    # 1. validate rule
    # 2. determine if rule exists in existing security group rules
    for rule in rules:
        try:
            ip_protocol = str(rule.get("ip_protocol"))
        except KeyError:
            raise SaltInvocationError(
                "ip_protocol, to_port, and from_port are"
                " required arguments for security group"
                " rules."
            )
        supported_protocols = [
            "tcp",
            "6",
            6,
            "udp",
            "17",
            17,
            "icmp",
            "1",
            1,
            "all",
            "-1",
            -1,
        ]
        if ip_protocol not in supported_protocols and (
            not "{}".format(ip_protocol).isdigit() or int(ip_protocol) > 255
        ):
            raise SaltInvocationError(
                "Invalid ip_protocol {} specified in security group rule.".format(
                    ip_protocol
                )
            )
        # For the 'all' case, we need to change the protocol name to '-1'.
        if ip_protocol == "all":
            rule["ip_protocol"] = "-1"
        cidr_ip = rule.get("cidr_ip", None)
        group_name = rule.get("source_group_name", None)
        group_id = rule.get("source_group_group_id", None)
        if cidr_ip and (group_id or group_name):
            raise SaltInvocationError(
                "cidr_ip and source groups can not both"
                " be specified in security group rules."
            )
        if group_id and group_name:
            raise SaltInvocationError(
                "Either source_group_group_id or"
                " source_group_name can be specified in"
                " security group rules, but not both."
            )
        if not (cidr_ip or group_id or group_name):
            raise SaltInvocationError(
                "cidr_ip, source_group_group_id, or"
                " source_group_name must be provided for"
                " security group rules."
            )
        rule_found = False
        # for each rule in existing security group ruleset determine if
        # new rule exists
        for _rule in _rules:
            if _check_rule(rule, _rule):
                rule_found = True
                break
        if not rule_found:
            to_create.append(rule)
    # for each rule in existing security group configuration
    # 1. determine if rules needed to be deleted
    for _rule in _rules:
        rule_found = False
        for rule in rules:
            if _check_rule(rule, _rule):
                rule_found = True
                break
        if not rule_found:
            # Can only supply name or id, not both. Since we're deleting
            # entries, it doesn't matter which we pick.
            _rule.pop("source_group_name", None)
            to_delete.append(_rule)
    log.debug("Rules to be deleted: %s", to_delete)
    log.debug("Rules to be created: %s", to_create)
    return (to_delete, to_create)

response format:
Answer: You respond with Yes or No for whether the code has non-idiomatic Python code that can be refactored with loop else.
Information: You respond with all code pairs where each pair consists of non-idiomatic code and the corresponding refactored code. Each pair splits with "******"
Non-Idiomatic Python code: You respond with identified non-idiomatic Python code that can be refactored with loop else.
Refactored Python code: You respond with the corresponding idiomatic Python code after refactoring the non-idiomatic code with loop else.
******
Non-Idiomatic code:...
Refactored code:...
''',
'''
Answer: Yes
Information:
Non-Idiomatic code:
rule_found = False
for _rule in _rules:
    if _check_rule(rule, _rule):
        rule_found = True
        break
if not rule_found:
    to_create.append(rule)
    
Refactored code:
for _rule in _rules:
    if _check_rule(rule, _rule):
        break
else:
    to_create.append(rule)''']]
    save_complicated_code_dir_root = util.data_root + "chatgpt/NonIdiomatic/"
    # save_complicated_code_dir_root = util.data_root + "NonIdiomatic/find_code_snippets/"
    save_complicated_code_dir = save_complicated_code_dir_root + "sample_methods/"
    idiom = "loop_else"
    file_name = idiom + "_methods"

    samples = util.load_pkl(save_complicated_code_dir_root, file_name)  # methods_sample

    reponse_list = baseline_util.get_response_directly_refactor(user_instr, examples, samples,
                                                                sys_msg="You are a helpful assistant.")
    
    file_name = "baseline"+idiom
    util.save_pkl(save_complicated_code_dir_root + "baseline/",
                  file_name,
                  reponse_list)
    '''
    file_name = "baseline"+idiom
    reponse_list = util.load_pkl(save_complicated_code_dir_root+ "baseline/", file_name)  # methods_sample
    print("reponse_list: ",len(reponse_list))
    '''
