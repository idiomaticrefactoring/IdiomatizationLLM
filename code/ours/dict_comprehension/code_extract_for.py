
import os,sys
import struct
import traceback
code_dir = "/".join(os.path.abspath(__file__).split("/")[:-2]) + "/"
print("code path: ",code_dir)
sys.path.append(code_dir)
import chatgpt_util,random
import openai, tiktoken,ast,util
import ast


def instr6_cfg():
    real_instruction = '''How to determine statements that reach a node of a given Python code in Python.

    for example, for the following Python code:
    graph = {}
    for u in self.complete:
        graph[u] = set()
        for v in self.complete[u]:
            if u != v:  # ignore self-loop
                graph[u].add(v)
            else:
                graph[u] = c

    for the node: graph[u].add(v)

    its statements are: graph = {} -> for -> graph[u] = set() -> graph[u].add(v)
    '''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])


#determine defs that reach a node
def instr6_defs():
    real_instruction = '''How to determine the def that reach a node of a given Python code in Python.
    
    for example, for the following Python code:
    graph = {}
    for u in self.complete:
        graph[u] = set()
        for v in self.complete[u]:
            if u != v:  # ignore self-loop
                graph[u].add(v)
            else:
                graph[u] = c
                
    for the node: graph[u].add(v)
    
    its defs are: graph[u] = set()
    '''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])


def instr_5_whether_write_a_variable():
    #Compute use-def chains of a given Python code.
    real_instruction = '''Does the following Python code has tool to compute the use-def chains of a python program in Python.
'''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])

def instr_4():
    #Compute use-def chains of a given Python code.
    real_instruction = '''Does it has tool to compute the use-def chains of a python program in Python.
'''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])

def instr_3():
    real_instruction = '''
Does it have python packages to directly get use-def chains for a variable of Python code?
'''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])


def instr_2():
    real_instruction = '''
How to extract the definition of a variable of statement in a given Python code in Python

for example, for a Python code:
simple_includes = set()
try:
    with open(manifest_in, "r") as f:
        for line in f:
            if line.startswith("include "):
                for include in line.split()[1:]:
                    simple_includes.add(include)
except EnvironmentError:
    pass
    
I want find the definition of a variable, simple_includes, of statement simple_includes.add(include) in the Python code, the definition statement is simple_includes = set().

    '''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])

def instr_1():
    real_instruction = '''
We give you a code template, you write Python code to extract all For AST nodes from a given Python code.
def get_for(code):
    """
    extract all For AST nodes

    Parameters
    ----------
    code : string
        a Python code
    Returns
    -------
    result : set
          all For AST nodes
    """

    '''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
def get_for(code):
    """
    extract all For AST nodes

    Parameters
    ----------
    code : string
        a Python code
    Returns
    -------
    result : set
          all For AST nodes
    """
    result = set()
    tree = ast.parse(code)
    for node in ast.walk(tree):
        if isinstance(node, ast.For):
            result.add(node)
    return result

def get_for_2(code):
    """
    extract all For AST nodes

    Parameters
    ----------
    code : string
        a Python code
    Returns
    -------
    result : set
          all For AST nodes
    """
    result = []
    tree = ast.parse(code)
    for node in ast.walk(tree):
        if isinstance(node, ast.For):
            if node not in result:
                result.append(node)
    return result
if __name__ == '__main__':
    # instr_1()
    # instr_2()
    # instr_3()
    # instr_4()
    instr6_defs()
    # instr6_cfg()
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
    code='''def do_setup():
    """Main VCS-independent setup function for installing Versioneer."""
    root = get_root()
    try:
        cfg = get_config_from_root(root)
    except (EnvironmentError, configparser.NoSectionError,
            configparser.NoOptionError) as e:
        if isinstance(e, (EnvironmentError, configparser.NoSectionError)):
            print("Adding sample versioneer config to setup.cfg",
                  file=sys.stderr)
            with open(os.path.join(root, "setup.cfg"), "a") as f:
                f.write(SAMPLE_CONFIG)
        print(CONFIG_ERROR, file=sys.stderr)
        return 1

    print(" creating %s" % cfg.versionfile_source)
    with open(cfg.versionfile_source, "w") as f:
        LONG = LONG_VERSION_PY[cfg.VCS]
        f.write(LONG % {"DOLLAR": "$",
                        "STYLE": cfg.style,
                        "TAG_PREFIX": cfg.tag_prefix,
                        "PARENTDIR_PREFIX": cfg.parentdir_prefix,
                        "VERSIONFILE_SOURCE": cfg.versionfile_source,
                        })

    ipy = os.path.join(os.path.dirname(cfg.versionfile_source),
                       "__init__.py")
    if os.path.exists(ipy):
        try:
            with open(ipy, "r") as f:
                old = f.read()
        except EnvironmentError:
            old = ""
        if INIT_PY_SNIPPET not in old:
            print(" appending to %s" % ipy)
            with open(ipy, "a") as f:
                f.write(INIT_PY_SNIPPET)
        else:
            print(" %s unmodified" % ipy)
    else:
        print(" %s doesn't exist, ok" % ipy)
        ipy = None

    # Make sure both the top-level "versioneer.py" and versionfile_source
    # (PKG/_version.py, used by runtime code) are in MANIFEST.in, so
    # they'll be copied into source distributions. Pip won't be able to
    # install the package without this.
    manifest_in = os.path.join(root, "MANIFEST.in")
    simple_includes = set()
    try:
        with open(manifest_in, "r") as f:
            for line in f:
                if line.startswith("include "):
                    for include in line.split()[1:]:
                        simple_includes.add(include)
    except EnvironmentError:
        pass
    # That doesn't cover everything MANIFEST.in can do
    # (http://docs.python.org/2/distutils/sourcedist.html#commands), so
    # it might give some false negatives. Appending redundant 'include'
    # lines is safe, though.
    if "versioneer.py" not in simple_includes:
        print(" appending 'versioneer.py' to MANIFEST.in")
        with open(manifest_in, "a") as f:
            f.write("include versioneer.py\\n")
    else:
        print(" 'versioneer.py' already in MANIFEST.in")
    if cfg.versionfile_source not in simple_includes:
        print(" appending versionfile_source ('%s') to MANIFEST.in" %
              cfg.versionfile_source)
        with open(manifest_in, "a") as f:
            f.write("include %s\\n" % cfg.versionfile_source)
    else:
        print(" versionfile_source already in MANIFEST.in")

    # Make VCS-specific changes. For git, this means creating/changing
    # .gitattributes to mark _version.py for export-subst keyword
    # substitution.
    do_vcs_install(manifest_in, cfg.versionfile_source, ipy)
    return 0    
    '''
    # import pyan as pyan

    # Define the Python code to analyze
    code = """
    x = 1
    y = x + 2
    z = y * 3
    """
    '''
    # Create a Pyan object and analyze the code
    graph = pyan.create_callgraph(code)

    # Get the use-def chains for the variable 'x'
    chains = graph.get_use_def_chains('x')

    # Print the use-def chains
    for chain in chains:
        print(chain)
    nodes=get_for_2(code)
    print("nodes: ",nodes)
    for e in nodes:
        print("e: ",ast.unparse(e))
    '''
