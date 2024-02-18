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
Refactor the following Python code with for multiple targets. You give all code pairs where each pair consists of non-idiomatic Python code and the corresponding refactored code. You respond according to the response format.

Python code:
{{code}}

response format:
Answer: You respond with Yes or No for whether the code has non-idiomatic Python code that can be refactored with for multiple targets.
Information: You respond with all code pairs where each pair consists of non-idiomatic code and the corresponding refactored code. Each pair splits with "******"
Non-Idiomatic Python code: You respond with identified non-idiomatic Python code that can be refactored with for multiple targets.
Refactored Python code: You respond with the corresponding idiomatic Python code after refactoring the non-idiomatic code with for multiple targets.
******
Non-Idiomatic code:...
Refactored code:...
'''
    examples = [
['''
Refactor the following Python code with for multiple targets. You give all code pairs where each pair consists of non-idiomatic Python code and the corresponding refactored code. You respond according to the response format.

Python code:
def submit():
    status_code = None
    response_body = None
    data = request.get_json()
    newhost = {}
    newhost = json.loads(data)
    newhost["ctime"] = dt.now(tz.utc)
    if newhost["scan_reason"] == "requested":
        mark_scan_completed(newhost["ip"], newhost["scan_id"])

    try:
        nmap = NmapParser.parse(newhost.get("xml_data", None))
        # If there's more or less than 1 host in the xml data, reject it (for now)
        if nmap.hosts_total != 1:
            status_code = 400
            response_body = json.dumps(
                {
                    "status": status_code,
                    "message": "XML had too many hosts in it",
                    "retry": False,
                }
            )

        # If it's not an acceptable target, tell the agent it's out of scope
        elif len(nmap.hosts) == 1 and not current_app.ScopeManager.is_acceptable_target(
            nmap.hosts[0].address
        ):
            status_code = 400
            response_body = json.dumps(
                {
                    "status": status_code,
                    "message": "Out of scope: " + nmap.hosts[0].address,
                    "retry": False,
                }
            )

        # If there's no further processing to do, store the host and prepare the response
        elif not newhost["is_up"] or (newhost["is_up"] and newhost["port_count"] == 0):
            current_app.elastic.new_result(newhost)
            status_code = 200
            response_body = json.dumps(
                {"status": status_code, "message": "Received: " + newhost["ip"]}
            )
    except NmapParserException:
        status_code = 400
        response_body = json.dumps(
            {
                "status": status_code,
                "message": "Invalid nmap xml data provided",
                "retry": False,
            }
        )

    # If status_code and response_body have been set by this point, return a response.
    if status_code and response_body:
        response = Response(
            response=response_body, status=status_code, content_type=json_content
        )
        return response

    if newhost["scan_start"] and newhost["scan_stop"]:
        elapsed = dateutil.parser.parse(newhost["scan_stop"]) - dateutil.parser.parse(
            newhost["scan_start"]
        )
        newhost["elapsed"] = elapsed.seconds

    newhost["ip"] = nmap.hosts[0].address
    if len(nmap.hosts[0].hostnames) > 0:
        newhost["hostname"] = nmap.hosts[0].hostnames[0]

    tmpports = []
    newhost["ports"] = []

    for port in nmap.hosts[0].get_open_ports():
        tmpports.append(str(port[0]))
        srv = nmap.hosts[0].get_service(port[0], port[1])
        portinfo = srv.get_dict()
        portinfo["service"] = srv.service_dict
        portinfo["scripts"] = []
        for script in srv.scripts_results:
            scriptsave = {"id": script["id"], "output": script["output"]}
            portinfo["scripts"].append(scriptsave)
            if script["id"] == "ssl-cert":
                portinfo["ssl"] = parse_ssl_data(script)

        newhost["ports"].append(portinfo)

    newhost["port_str"] = ", ".join(tmpports)

    if "screenshots" in newhost and newhost["screenshots"]:
        newhost["screenshots"], newhost["num_screenshots"] = process_screenshots(
            newhost["screenshots"]
        )

    if len(newhost["ports"]) == 0:
        status_code = 200
        response_body = json.dumps(
            {
                "status": status_code,
                "message": f"Expected open ports but didn't find any for {newhost['ip']}",
            }
        )
    elif len(newhost["ports"]) > 500:
        status_code = 200
        response_body = json.dumps(
            {
                "status": status_code,
                "message": "More than 500 ports found, throwing data out",
            }
        )
    else:
        status_code = 200
        current_app.elastic.new_result(newhost)
        response_body = json.dumps(
            {
                "status": status_code,
                "message": f"Received {len(newhost['ports'])} ports for {newhost['ip']}",
            }
        )

    response = Response(
        response=response_body, status=status_code, content_type=json_content
    )
    return response

response format:
Answer: You respond with Yes or No for whether the code has non-idiomatic Python code that can be refactored with for multiple targets.
Information: You respond with all code pairs where each pair consists of non-idiomatic code and the corresponding refactored code. Each pair splits with "******"
Non-Idiomatic Python code: You respond with identified non-idiomatic Python code that can be refactored with for multiple targets.
Refactored Python code: You respond with the corresponding idiomatic Python code after refactoring the non-idiomatic code with for multiple targets.
******
Non-Idiomatic code:...
Refactored code:...
''',
'''
Answer: Yes
Information:
Non-Idiomatic code:
for port in nmap.hosts[0].get_open_ports():
    tmpports.append(str(port[0]))
    srv = nmap.hosts[0].get_service(port[0], port[1])
    portinfo = srv.get_dict()
    portinfo["service"] = srv.service_dict
    portinfo["scripts"] = []
    for script in srv.scripts_results:
        scriptsave = {"id": script["id"], "output": script["output"]}
        portinfo["scripts"].append(scriptsave)
        if script["id"] == "ssl-cert":
            portinfo["ssl"] = parse_ssl_data(script)

    newhost["ports"].append(portinfo)
    
Refactored code:
for port_0, port_1, *_ in nmap.hosts[0].get_open_ports():
    tmpports.append(str(port_0))
    srv = nmap.hosts[0].get_service(port_0, port_1)
    portinfo = srv.get_dict()
    portinfo["service"] = srv.service_dict
    portinfo["scripts"] = []
    for script in srv.scripts_results:
        scriptsave = {"id": script["id"], "output": script["output"]}
        portinfo["scripts"].append(scriptsave)
        if script["id"] == "ssl-cert":
            portinfo["ssl"] = parse_ssl_data(script)

    newhost["ports"].append(portinfo)
''']]
    save_complicated_code_dir_root = util.data_root + "chatgpt/NonIdiomatic/"
    # save_complicated_code_dir_root = util.data_root + "NonIdiomatic/find_code_snippets/"
    save_complicated_code_dir = save_complicated_code_dir_root + "sample_methods/"
    idiom = "for multi targets"
    idiom = "_".join(idiom.split(" "))
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
