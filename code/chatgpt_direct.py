import ast,chatgpt_util
# For example,
# for the code:
#  sum(a[0],a[1],b),
# the non-idiomatic Python code are a[0],a[1]
def instr_find():

    real_instruction = '''
How to find non-idiomatic Python code that can refactored with chain-comparison'''#star-in-fun-call
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
#self.c.reshape(self.c.shape[0], self.c.shape[1], -1)
#self.c.reshape(feat.shape[0], feat.shape[1], -1)
#self.sigma[:, cc, :].reshape((self.sigma.shape[0], 1, self.sigma.shape[2]))
    real_instruction = '''
Refactor the following Python code with star-in-func-call.
self.sigma[:, cc, :].reshape((self.sigma.shape[0], 1, self.sigma.shape[2]))
'''
    examples=[['''
Refactor the following Python code with star-in-func-call.
func(c[0],c[1])
''','''
func(*c[:2])
''']]
    msg = chatgpt_util.format_message_2(real_instruction, examples=examples, sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)#,model="gpt-3.5-turbo"
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
def instr_unpack():
#self.c.reshape(self.c.shape[0], self.c.shape[1], -1)
#self.c.reshape(feat.shape[0], feat.shape[1], -1)
#self.sigma[:, cc, :].reshape((self.sigma.shape[0], 1, self.sigma.shape[2]))
#self.sigma[:, cc, :].reshape(image_shape[1], image_shape[2])
#reshape(image_shape[1], image_shape[2])
#box_list_ops.to_absolute_coordinates(box_list.BoxList(boxes), image_shape[1], image_shape[2])
#gbot('test', '杩炴帴鎴愬姛', self.load_config()[i], self.load_config()[j], self.config.b)
#
    real_instruction = '''
Use the slice operator [:] to slice "self.data.shape()"  to get the elements "self.data.shape()[-2]", "self.data.shape()[-1]" in Python.
'''
    examples=[['''
Use the slice operator [:] to slice "e"  to get the elements "e[0]", "e[1]" in Python.
''','''
e[:2]
''']]
    msg = chatgpt_util.format_message_2(real_instruction, examples=examples, sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)#,model="gpt-3.5-turbo"
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
def instr_direct_list_comprehension():
    # for i in range(node_count):
    #     self.nodes.append(Node(layer_index, i))
    # for i in range(num_blocks):
    #     self.blocks.append(
    #         block_cls(channels=channels, stride=1 if i else stride, use_projection=i == 0 and use_projection,
    #                   bottleneck=bottleneck, bn_config=bn_config, name='block_%d' % i))
    # for (num, (entry_title, media_kind, download_text)) in enumerate(re.findall(
    #         '(?s)<p[^>]+class="infotext"[^>]*>\\s*(?:<a[^>]+>)?\\s*<strong>(.+?)</strong>.*?</p>.*?%s' % DOWNLOAD_REGEX,
    #         webpage), 1):
    #     entries.append({'id': '%s-%d' % (display_id, num), 'title': '%s' % entry_title,
    #                     'formats': self._extract_formats(download_text, media_kind)})
    #     Answer: No
    # for line in f:
    #     self.nlsyms_list.append(line.strip())
    real_instruction = '''
refactor the following Python code with set comprehension
for line in archive_file:
    self.archive.add(line.strip())
'''
    examples=[['''refactor the following Python code with set comprehension
Python code:
for (num, (entry_title, media_kind, download_text)) in enumerate(re.findall('(?s)<p[^>]+class="infotext"[^>]*>\\s*(?:<a[^>]+>)?\\s*<strong>(.+?)</strong>.*?</p>.*?%s' % DOWNLOAD_REGEX, webpage), 1):
    entries.add({'id': '%s-%d' % (display_id, num), 'title': '%s' % entry_title, 'formats': self._extract_formats(download_text, media_kind)})
''','''
entries = {{'id': '%s-%d' % (display_id, num), 'title': '%s' % entry_title, 'formats': self._extract_formats(download_text, media_kind)} for (num, (entry_title, media_kind, download_text)) in enumerate(re.findall('(?s)<p[^>]+class="infotext"[^>]*>\\s*(?:<a[^>]+>)?\\s*<strong>(.+?)</strong>.*?</p>.*?%s' % DOWNLOAD_REGEX, webpage), 1)}
''']]
    msg = chatgpt_util.format_message_2(real_instruction, examples=examples, sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)#,model="gpt-3.5-turbo"
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
def instr_direct_chain_comparison():
    # for i in range(node_count):
    #     self.nodes.append(Node(layer_index, i))
    # for i in range(num_blocks):
    #     self.blocks.append(
    #         block_cls(channels=channels, stride=1 if i else stride, use_projection=i == 0 and use_projection,
    #                   bottleneck=bottleneck, bn_config=bn_config, name='block_%d' % i))
    # for (num, (entry_title, media_kind, download_text)) in enumerate(re.findall(
    #         '(?s)<p[^>]+class="infotext"[^>]*>\\s*(?:<a[^>]+>)?\\s*<strong>(.+?)</strong>.*?</p>.*?%s' % DOWNLOAD_REGEX,
    #         webpage), 1):
    #     entries.append({'id': '%s-%d' % (display_id, num), 'title': '%s' % entry_title,
    #                     'formats': self._extract_formats(download_text, media_kind)})
    #     Answer: No
    # for line in f:
    #     self.nlsyms_list.append(line.strip())
    #cat not in options and cat != unknown
#self.ireference is not None and group_index == self.ireference

    real_instruction = '''
refactor the following Python code with chain comparison
cache is None and cache_func is not None
'''
    examples=[]
    msg = chatgpt_util.format_message_2(real_instruction, examples=examples, sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)#,model="gpt-3.5-turbo"
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
# def instr_direct_chain_comparison():
    # for i in range(node_count):
    #     self.nodes.append(Node(layer_index, i))
    # for i in range(num_blocks):
    #     self.blocks.append(
    #         block_cls(channels=channels, stride=1 if i else stride, use_projection=i == 0 and use_projection,
    #                   bottleneck=bottleneck, bn_config=bn_config, name='block_%d' % i))
    # for (num, (entry_title, media_kind, download_text)) in enumerate(re.findall(
    #         '(?s)<p[^>]+class="infotext"[^>]*>\\s*(?:<a[^>]+>)?\\s*<strong>(.+?)</strong>.*?</p>.*?%s' % DOWNLOAD_REGEX,
    #         webpage), 1):
    #     entries.append({'id': '%s-%d' % (display_id, num), 'title': '%s' % entry_title,
    #                     'formats': self._extract_formats(download_text, media_kind)})
    #     Answer: No
    # for line in f:
    #     self.nlsyms_list.append(line.strip())
    #cat not in options and cat != unknown
#self.ireference is not None and group_index == self.ireference
#refactor the following Python code with list comprehension
def instr_direct_chain_comparison():
        # for i in range(node_count):
        #     self.nodes.append(Node(layer_index, i))
        # for i in range(num_blocks):
        #     self.blocks.append(
        #         block_cls(channels=channels, stride=1 if i else stride, use_projection=i == 0 and use_projection,
        #                   bottleneck=bottleneck, bn_config=bn_config, name='block_%d' % i))
        # for (num, (entry_title, media_kind, download_text)) in enumerate(re.findall(
        #         '(?s)<p[^>]+class="infotext"[^>]*>\\s*(?:<a[^>]+>)?\\s*<strong>(.+?)</strong>.*?</p>.*?%s' % DOWNLOAD_REGEX,
        #         webpage), 1):
        #     entries.append({'id': '%s-%d' % (display_id, num), 'title': '%s' % entry_title,
        #                     'formats': self._extract_formats(download_text, media_kind)})
        #     Answer: No
        # for line in f:
        #     self.nlsyms_list.append(line.strip())
        # cat not in options and cat != unknown
        # self.ireference is not None and group_index == self.ireference

        real_instruction = '''
    refactor the following Python code with chain comparison
    cache is None and cache_func is not None
    '''
        examples = []
        msg = chatgpt_util.format_message_2(real_instruction, examples=examples, sys_msg="You are a helpful assistant.")
        # try:
        print(">>>>>>>>>>instruction:\n", real_instruction)
        response = chatgpt_util.chatGPT_result(msg)  # ,model="gpt-3.5-turbo"
        print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
def instr_direct_list_comprehension():
    real_instruction = '''
Refactor the following Python code with set comprehension. You give all code pairs where each pair consists of non-idiomatic Python code and the corresponding refactored code. 
def permissions(self, trans, payload=None, **kwd):
    """
        Sets the permissions on a history.
        """
    history_id = kwd.get('id')
    if not history_id:
        return self.message_exception(trans, f'Invalid history id ({str(history_id)}) received')
    history = self.history_manager.get_owned(self.decode_id(history_id), trans.user, current_history=trans.history)
    if trans.request.method == 'GET':
        inputs = []
        all_roles = trans.user.all_roles()
        current_actions = history.default_permissions
        for (action_key, action) in trans.app.model.Dataset.permitted_actions.items():
            in_roles = set()
            for a in current_actions:
                if a.action == action.action:
                    in_roles.add(a.role)
            inputs.append({'type': 'select', 'multiple': True, 'optional': True, 'individual': True, 'name': action_key, 'label': action.action, 'help': action.description, 'options': [(role.name, trans.security.encode_id(role.id)) for role in set(all_roles)], 'value': [trans.security.encode_id(role.id) for role in in_roles]})
        return {'title': "Change default dataset permissions for history '%s'" % history.name, 'inputs': inputs}
    else:
        permissions = {}
        for (action_key, action) in trans.app.model.Dataset.permitted_actions.items():
            in_roles = payload.get(action_key) or []
            in_roles = [trans.sa_session.query(trans.app.model.Role).get(trans.security.decode_id(x)) for x in in_roles]
            permissions[trans.app.security_agent.get_action(action.action)] = in_roles
        trans.app.security_agent.history_set_default_permissions(history, permissions)
        return {'message': "Default history '%s' dataset permissions have been changed." % history.name}
'''
    # examples = []
    examples=[['''Refactor the following Python code with set comprehension. You give all code pairs where each pair consists of non-idiomatic Python code and the corresponding refactored code.
def read_set_from_file(filename):
    """
    Extract a de-duped collection (set) of text from a file.
    Expected file format is one item per line.
    """
    collection = set()
    with open(filename, 'r', encoding='utf-8') as file_:
        for line in file_:
            collection.add(line.rstrip())
    return collection
    ''','''
Non-idiomatic code:
collection = set()
with open(filename, 'r', encoding='utf-8') as file_:
    for line in file_:
        collection.add(line.rstrip())
Refactored code:
with open(filename, 'r', encoding='utf-8') as file_:
    collection = {line.rstrip() for line in open(filename, 'r', encoding='utf-8')}
    ''']]
    msg = chatgpt_util.format_message_2(real_instruction, examples=examples, sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)#,model="gpt-3.5-turbo"
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
def instr_direct_star_func():

    real_instruction = '''
refactor the following Python code with chain comparison. You give all code pairs where each pair consists of non-idiomatic Python code and the corresponding refactored code. 
def permissions(self, trans, payload=None, **kwd):
    """
        Sets the permissions on a history.
        """
    history_id = kwd.get('id')
    if not history_id:
        return self.message_exception(trans, f'Invalid history id ({str(history_id)}) received')
    history = self.history_manager.get_owned(self.decode_id(history_id), trans.user, current_history=trans.history)
    if trans.request.method == 'GET':
        inputs = []
        all_roles = trans.user.all_roles()
        current_actions = history.default_permissions
        for (action_key, action) in trans.app.model.Dataset.permitted_actions.items():
            in_roles = set()
            for a in current_actions:
                if a.action == action.action:
                    in_roles.add(a.role)
            inputs.append({'type': 'select', 'multiple': True, 'optional': True, 'individual': True, 'name': action_key, 'label': action.action, 'help': action.description, 'options': [(role.name, trans.security.encode_id(role.id)) for role in set(all_roles)], 'value': [trans.security.encode_id(role.id) for role in in_roles]})
        return {'title': "Change default dataset permissions for history '%s'" % history.name, 'inputs': inputs}
    else:
        permissions = {}
        for (action_key, action) in trans.app.model.Dataset.permitted_actions.items():
            in_roles = payload.get(action_key) or []
            in_roles = [trans.sa_session.query(trans.app.model.Role).get(trans.security.decode_id(x)) for x in in_roles]
            permissions[trans.app.security_agent.get_action(action.action)] = in_roles
        trans.app.security_agent.history_set_default_permissions(history, permissions)
        return {'message': "Default history '%s' dataset permissions have been changed." % history.name}'''
    examples=[]
    msg = chatgpt_util.format_message_2(real_instruction, examples=examples, sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)#,model="gpt-3.5-turbo"
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
def instr_direct_chain_comapre():
#self.c.reshape(self.c.shape[0], self.c.shape[1], -1)
#self.c.reshape(feat.shape[0], feat.shape[1], -1)
#self.sigma[:, cc, :].reshape((self.sigma.shape[0], 1, self.sigma.shape[2]))
#self.sigma[:, cc, :].reshape(image_shape[1], image_shape[2])
#reshape(image_shape[1], image_shape[2])
#box_list_ops.to_absolute_coordinates(box_list.BoxList(boxes), image_shape[1], image_shape[2])
#gbot('test', '杩炴帴鎴愬姛', self.load_config()[i], self.load_config()[j], self.config.b)
#j + k > last_seen[1] and j + k >= 0 and j + k < len(split_docs[i])
#start is not None and end is not None
# refactor the following Python code with chain comparison. You give all code pairs where each pair consists of non-idiomatic Python code and the corresponding refactored code.
#y_int < h_img and x_int < w_img
#v1 < v2 and v3 < v2
#y_int < h_img and y_int < w_img
# refactor the following Python code with chain comparison.
# Python code:
# v1 < v2 and v1 < v3
#reverse compare operands of the first compare, second compare or first compare and second compare of the following Python code so that "v1 and v1" is in the New Python code
#v1 < v2 and v1 < v3
#reverse compare operands of the first compare, second compare or first compare and second compare of the following Python code so that "y_int and y_int" is in the New Python code
#y_int < h_img and y_int < w_img
# x_int < h_img and x_int < w_img
#v1 < v2 and v1 > v3
#x_int > h_img and x_int > w_img
#0 > h_img and 0 < w_img
#0 <= y_int < h_img and w_img > 0
#v1 <= v2 < v3 and v4 < v1
#"0 != y_int < h_img and 0>a"
#0 != y_int < h_img and w_img < 0
#v1 != v2 < v3 and v4 < v1
#a != y_int < h_img and w_img < a
#0 <= y_int < h and w < 0
#0 <= y_int < h_i and w_i < 0
#0 <= y_int > h_i and w_i < 0
#v4 <= v1 and v1 <= v2 < v3
#v4 > v1 and v1 <= v2 < v3
#h_i <= 0 and 0 <= y_int <= w_i
#h_i <= 0 and 0 <= y_int <= w_i
#v1 <= v2 and v2 <= v3 <=v4
#0 <= y_int < h_i and w_i < 0
#v1 < v2 < v3 and v4 < v1
#v1 < v2 < v3 and v4 < v1
#0 < y_int < h_i and w_i <= 0: 0 < y_int < h_i <= 0
    real_instruction = '''
refactor the following Python code with chain comparison. You give all code pairs where each pair consists of non-idiomatic Python code and the corresponding refactored code.  
Python code: 
if 0 < y_int < h_i and w_i < 0:
    a=1
'''
# ['''refactor the following Python code with chain comparison.
# Python code:
# c < b and a <c
#     ''','''a < c < b
#     ''']
    examples=[]#
    msg = chatgpt_util.format_message_2(real_instruction, examples=examples, sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg,model="gpt-3.5-turbo")#,model="gpt-3.5-turbo" , ,model="gpt-3.5-turbo"model="gpt-4" ,model="gpt-4" ,model="gpt-3.5-turbo"
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])

def instr_direct_chain_comapre_reverse():
#self.c.reshape(self.c.shape[0], self.c.shape[1], -1)
#self.c.reshape(feat.shape[0], feat.shape[1], -1)
#self.sigma[:, cc, :].reshape((self.sigma.shape[0], 1, self.sigma.shape[2]))
#self.sigma[:, cc, :].reshape(image_shape[1], image_shape[2])
#reshape(image_shape[1], image_shape[2])
#box_list_ops.to_absolute_coordinates(box_list.BoxList(boxes), image_shape[1], image_shape[2])
#gbot('test', '杩炴帴鎴愬姛', self.load_config()[i], self.load_config()[j], self.config.b)
#j + k > last_seen[1] and j + k >= 0 and j + k < len(split_docs[i])
#start is not None and end is not None
    real_instruction = '''
reverse the comparison operand
v1 is not v2
'''
    examples=[]
    msg = chatgpt_util.format_message_2(real_instruction, examples=examples, sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)#,model="gpt-3.5-turbo"
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])
# refactor the following Python code with star-in-func-call. You give all code pairs where each pair consists of non-idiomatic Python code and the corresponding refactored code.
# def attack_single_run(self, x, y=None, use_rand_start=False):
#     """
#         :param x:    clean images
#         :param y:    clean labels, if None we use the predicted labels
#         """
#     self.orig_dim = list(x.shape[1:])
#     self.ndims = len(self.orig_dim)
#     x = x.detach().clone().float().to(self.device)
#     y_pred = self._get_predicted_label(x)
#     if y is None:
#         y = y_pred.detach().clone().long().to(self.device)
#     else:
#         y = y.detach().clone().long().to(self.device)
#     pred = y_pred == y
#     corr_classified = pred.float().sum()
#     if self.verbose:
#         print('Clean accuracy: {:.2%}'.format(pred.float().mean()))
#     if pred.sum() == 0:
#         return x
#     pred = self.check_shape(pred.nonzero().squeeze())
#     startt = time.time()
#     im2 = x[pred].detach().clone()
#     la2 = y[pred].detach().clone()
#     if len(im2.shape) == self.ndims:
#         im2 = im2.unsqueeze(0)
#     bs = im2.shape[0]
#     u1 = torch.arange(bs)
#     adv = im2.clone()
#     adv_c = x.clone()
#     res2 = 10000000000.0 * torch.ones([bs]).to(self.device)
#     res_c = torch.zeros([x.shape[0]]).to(self.device)
#     x1 = im2.clone()
#     x0 = im2.clone().reshape([bs, -1])
#     counter_restarts = 0
#     while counter_restarts < 1:
#         if use_rand_start:
#             if self.norm == 'Linf':
#                 t = 2 * torch.rand(x1.shape).to(self.device) - 1
#                 x1 = im2 + torch.min(res2, self.eps * torch.ones(res2.shape).to(self.device)).reshape([-1, *[1] * self.ndims]) * t / t.reshape([t.shape[0], -1]).abs().max(dim=1, keepdim=True)[0].reshape([-1, *[1] * self.ndims]) * 0.5
#             elif self.norm == 'L2':
#                 t = torch.randn(x1.shape).to(self.device)
#                 x1 = im2 + torch.min(res2, self.eps * torch.ones(res2.shape).to(self.device)).reshape([-1, *[1] * self.ndims]) * t / (t ** 2).view(t.shape[0], -1).sum(dim=-1).sqrt().view(t.shape[0], *[1] * self.ndims) * 0.5
#             elif self.norm == 'L1':
#                 t = torch.randn(x1.shape).to(self.device)
#                 x1 = im2 + torch.min(res2, self.eps * torch.ones(res2.shape).to(self.device)).reshape([-1, *[1] * self.ndims]) * t / t.abs().view(t.shape[0], -1).sum(dim=-1).view(t.shape[0], *[1] * self.ndims) / 2
#             x1 = x1.clamp(0.0, 1.0)
#         counter_iter = 0
#         while counter_iter < self.steps:
#             with torch.no_grad():
#                 (df, dg) = self.get_diff_logits_grads_batch(x1, la2)
#                 if self.norm == 'Linf':
#                     dist1 = df.abs() / (1e-12 + dg.abs().view(dg.shape[0], dg.shape[1], -1).sum(dim=-1))
#                 elif self.norm == 'L2':
#                     dist1 = df.abs() / (1e-12 + (dg ** 2).view(dg.shape[0], dg.shape[1], -1).sum(dim=-1).sqrt())
#                 elif self.norm == 'L1':
#                     dist1 = df.abs() / (1e-12 + dg.abs().reshape([df.shape[0], df.shape[1], -1]).max(dim=2)[0])
#                 else:
#                     raise ValueError('norm not supported')
#                 ind = dist1.min(dim=1)[1]
#                 dg2 = dg[u1, ind]
#                 b = -df[u1, ind] + (dg2 * x1).view(x1.shape[0], -1).sum(dim=-1)
#                 w = dg2.reshape([bs, -1])
#                 if self.norm == 'Linf':
#                     d3 = projection_linf(torch.cat((x1.reshape([bs, -1]), x0), 0), torch.cat((w, w), 0), torch.cat((b, b), 0))
#                 elif self.norm == 'L2':
#                     d3 = projection_l2(torch.cat((x1.reshape([bs, -1]), x0), 0), torch.cat((w, w), 0), torch.cat((b, b), 0))
#                 elif self.norm == 'L1':
#                     d3 = projection_l1(torch.cat((x1.reshape([bs, -1]), x0), 0), torch.cat((w, w), 0), torch.cat((b, b), 0))
#                 d1 = torch.reshape(d3[:bs], x1.shape)
#                 d2 = torch.reshape(d3[-bs:], x1.shape)
#                 if self.norm == 'Linf':
#                     a0 = d3.abs().max(dim=1, keepdim=True)[0].view(-1, *[1] * self.ndims)
#                 elif self.norm == 'L2':
#                     a0 = (d3 ** 2).sum(dim=1, keepdim=True).sqrt().view(-1, *[1] * self.ndims)
#                 elif self.norm == 'L1':
#                     a0 = d3.abs().sum(dim=1, keepdim=True).view(-1, *[1] * self.ndims)
#                 a0 = torch.max(a0, 1e-08 * torch.ones(a0.shape).to(self.device))
#                 a1 = a0[:bs]
#                 a2 = a0[-bs:]
#                 alpha = torch.min(torch.max(a1 / (a1 + a2), torch.zeros(a1.shape).to(self.device)), self.alpha_max * torch.ones(a1.shape).to(self.device))
#                 x1 = ((x1 + self.eta * d1) * (1 - alpha) + (im2 + d2 * self.eta) * alpha).clamp(0.0, 1.0)
#                 is_adv = self._get_predicted_label(x1) != la2
#                 if is_adv.sum() > 0:
#                     ind_adv = is_adv.nonzero().squeeze()
#                     ind_adv = self.check_shape(ind_adv)
#                     if self.norm == 'Linf':
#                         t = (x1[ind_adv] - im2[ind_adv]).reshape([ind_adv.shape[0], -1]).abs().max(dim=1)[0]
#                     elif self.norm == 'L2':
#                         t = ((x1[ind_adv] - im2[ind_adv]) ** 2).view(ind_adv.shape[0], -1).sum(dim=-1).sqrt()
#                     elif self.norm == 'L1':
#                         t = (x1[ind_adv] - im2[ind_adv]).abs().view(ind_adv.shape[0], -1).sum(dim=-1)
#                     adv[ind_adv] = x1[ind_adv] * (t < res2[ind_adv]).float().reshape([-1, *[1] * self.ndims]) + adv[ind_adv] * (t >= res2[ind_adv]).float().reshape([-1, *[1] * self.ndims])
#                     res2[ind_adv] = t * (t < res2[ind_adv]).float() + res2[ind_adv] * (t >= res2[ind_adv]).float()
#                     x1[ind_adv] = im2[ind_adv] + (x1[ind_adv] - im2[ind_adv]) * self.beta
#                 counter_iter += 1
#         counter_restarts += 1
#     ind_succ = res2 < 10000000000.0
#     if self.verbose:
#         print('success rate: {:.0f}/{:.0f}'.format(ind_succ.float().sum(), corr_classified) + ' (on correctly classified points) in {:.1f} s'.format(time.time() - startt))
#     res_c[pred] = res2 * ind_succ.float() + 10000000000.0 * (1 - ind_succ.float())
#     ind_succ = self.check_shape(ind_succ.nonzero().squeeze())
#     adv_c[pred[ind_succ]] = adv[ind_succ].clone()
#     return adv_c
def instr_direct_star_func():
# def __init__(self, in_channels: int, out_channels: int, filter_counts: tuple, batch_norm=True):
#     super(UNet, self).__init__()
#     assert batch_norm, 'Not yet implemented'
#     self._levels = len(filter_counts)
#     self.inc = DoubleConv(in_channels, filter_counts[0])
#     for i in range(1, self._levels):
#         self.add_module(f'down{i}', Down(filter_counts[i - 1], filter_counts[i]))
#         self.add_module(f'up{i}', Up(filter_counts[i] + filter_counts[i - 1], filter_counts[i - 1]))
#     self.outc = OutConv(filter_counts[0], out_channels)
    real_instruction = '''refactor the following Python code with star-in-func-call. You give all code pairs where each pair consists of non-idiomatic Python code and the corresponding refactored code. 
def forward(self, teacher_model, student_model):
        teacher_distill_pairs = teacher_model.yolo_head.loss.distill_pairs
        student_distill_pairs = student_model.yolo_head.loss.distill_pairs
        distill_reg_loss, distill_cls_loss, distill_obj_loss = [], [], []
        for s_pair, t_pair in zip(student_distill_pairs, teacher_distill_pairs):
            distill_reg_loss.append(
                self.obj_weighted_reg(s_pair[0], s_pair[1], s_pair[2], s_pair[
                    3], t_pair[0], t_pair[1], t_pair[2], t_pair[3], t_pair[4]))
            distill_cls_loss.append(
                self.obj_weighted_cls(s_pair[5], t_pair[5], t_pair[4]))
            distill_obj_loss.append(self.obj_loss(s_pair[4], t_pair[4]))
        distill_reg_loss = paddle.add_n(distill_reg_loss)
        distill_cls_loss = paddle.add_n(distill_cls_loss)
        distill_obj_loss = paddle.add_n(distill_obj_loss)
        loss = (distill_reg_loss + distill_cls_loss + distill_obj_loss
                ) * self.weight
        return loss
'''
    examples=[]
    msg = chatgpt_util.format_message_2(real_instruction, examples=examples, sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)#,model="gpt-3.5-turbo"
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])

def instr_direct_star_func_code_pair():
    # def attack_single_run(self, x, y=None, use_rand_start=False):
    #     """
    #         :param x:    clean images
    #         :param y:    clean labels, if None we use the predicted labels
    #         """
    #     self.orig_dim = list(x.shape[1:])
    #     self.ndims = len(self.orig_dim)
    #     x = x.detach().clone().float().to(self.device)
    #     y_pred = self._get_predicted_label(x)
    #     if y is None:
    #         y = y_pred.detach().clone().long().to(self.device)
    #     else:
    #         y = y.detach().clone().long().to(self.device)
    #     pred = y_pred == y
    #     corr_classified = pred.float().sum()
    #     if self.verbose:
    #         print('Clean accuracy: {:.2%}'.format(pred.float().mean()))
    #     if pred.sum() == 0:
    #         return x
    #     pred = self.check_shape(pred.nonzero().squeeze())
    #     startt = time.time()
    #     im2 = x[pred].detach().clone()
    #     la2 = y[pred].detach().clone()
    #     if len(im2.shape) == self.ndims:
    #         im2 = im2.unsqueeze(0)
    #     bs = im2.shape[0]
    #     u1 = torch.arange(bs)
    #     adv = im2.clone()
    #     adv_c = x.clone()
    #     res2 = 10000000000.0 * torch.ones([bs]).to(self.device)
    #     res_c = torch.zeros([x.shape[0]]).to(self.device)
    #     x1 = im2.clone()
    #     x0 = im2.clone().reshape([bs, -1])
    #     counter_restarts = 0
    #     while counter_restarts < 1:
    #         if use_rand_start:
    #             if self.norm == 'Linf':
    #                 t = 2 * torch.rand(x1.shape).to(self.device) - 1
    #                 x1 = im2 + torch.min(res2, self.eps * torch.ones(res2.shape).to(self.device)).reshape(
    #                     [-1, *[1] * self.ndims]) * t / t.reshape([t.shape[0], -1]).abs().max(dim=1, keepdim=True)[
    #                          0].reshape([-1, *[1] * self.ndims]) * 0.5
    #             elif self.norm == 'L2':
    #                 t = torch.randn(x1.shape).to(self.device)
    #                 x1 = im2 + torch.min(res2, self.eps * torch.ones(res2.shape).to(self.device)).reshape(
    #                     [-1, *[1] * self.ndims]) * t / (t ** 2).view(t.shape[0], -1).sum(dim=-1).sqrt().view(t.shape[0],
    #                                                                                                          *[
    #                                                                                                               1] * self.ndims) * 0.5
    #             elif self.norm == 'L1':
    #                 t = torch.randn(x1.shape).to(self.device)
    #                 x1 = im2 + torch.min(res2, self.eps * torch.ones(res2.shape).to(self.device)).reshape(
    #                     [-1, *[1] * self.ndims]) * t / t.abs().view(t.shape[0], -1).sum(dim=-1).view(t.shape[0], *[
    #                                                                                                                   1] * self.ndims) / 2
    #             x1 = x1.clamp(0.0, 1.0)
    #         counter_iter = 0
    #         while counter_iter < self.steps:
    #             with torch.no_grad():
    #                 (df, dg) = self.get_diff_logits_grads_batch(x1, la2)
    #                 if self.norm == 'Linf':
    #                     dist1 = df.abs() / (1e-12 + dg.abs().view(dg.shape[0], dg.shape[1], -1).sum(dim=-1))
    #                 elif self.norm == 'L2':
    #                     dist1 = df.abs() / (1e-12 + (dg ** 2).view(dg.shape[0], dg.shape[1], -1).sum(dim=-1).sqrt())
    #                 elif self.norm == 'L1':
    #                     dist1 = df.abs() / (1e-12 + dg.abs().reshape([df.shape[0], df.shape[1], -1]).max(dim=2)[0])
    #                 else:
    #                     raise ValueError('norm not supported')
    #                 ind = dist1.min(dim=1)[1]
    #                 dg2 = dg[u1, ind]
    #                 b = -df[u1, ind] + (dg2 * x1).view(x1.shape[0], -1).sum(dim=-1)
    #                 w = dg2.reshape([bs, -1])
    #                 if self.norm == 'Linf':
    #                     d3 = projection_linf(torch.cat((x1.reshape([bs, -1]), x0), 0), torch.cat((w, w), 0),
    #                                          torch.cat((b, b), 0))
    #                 elif self.norm == 'L2':
    #                     d3 = projection_l2(torch.cat((x1.reshape([bs, -1]), x0), 0), torch.cat((w, w), 0),
    #                                        torch.cat((b, b), 0))
    #                 elif self.norm == 'L1':
    #                     d3 = projection_l1(torch.cat((x1.reshape([bs, -1]), x0), 0), torch.cat((w, w), 0),
    #                                        torch.cat((b, b), 0))
    #                 d1 = torch.reshape(d3[:bs], x1.shape)
    #                 d2 = torch.reshape(d3[-bs:], x1.shape)
    #                 if self.norm == 'Linf':
    #                     a0 = d3.abs().max(dim=1, keepdim=True)[0].view(-1, *[1] * self.ndims)
    #                 elif self.norm == 'L2':
    #                     a0 = (d3 ** 2).sum(dim=1, keepdim=True).sqrt().view(-1, *[1] * self.ndims)
    #                 elif self.norm == 'L1':
    #                     a0 = d3.abs().sum(dim=1, keepdim=True).view(-1, *[1] * self.ndims)
    #                 a0 = torch.max(a0, 1e-08 * torch.ones(a0.shape).to(self.device))
    #                 a1 = a0[:bs]
    #                 a2 = a0[-bs:]
    #                 alpha = torch.min(torch.max(a1 / (a1 + a2), torch.zeros(a1.shape).to(self.device)),
    #                                   self.alpha_max * torch.ones(a1.shape).to(self.device))
    #                 x1 = ((x1 + self.eta * d1) * (1 - alpha) + (im2 + d2 * self.eta) * alpha).clamp(0.0, 1.0)
    #                 is_adv = self._get_predicted_label(x1) != la2
    #                 if is_adv.sum() > 0:
    #                     ind_adv = is_adv.nonzero().squeeze()
    #                     ind_adv = self.check_shape(ind_adv)
    #                     if self.norm == 'Linf':
    #                         t = (x1[ind_adv] - im2[ind_adv]).reshape([ind_adv.shape[0], -1]).abs().max(dim=1)[0]
    #                     elif self.norm == 'L2':
    #                         t = ((x1[ind_adv] - im2[ind_adv]) ** 2).view(ind_adv.shape[0], -1).sum(dim=-1).sqrt()
    #                     elif self.norm == 'L1':
    #                         t = (x1[ind_adv] - im2[ind_adv]).abs().view(ind_adv.shape[0], -1).sum(dim=-1)
    #                     adv[ind_adv] = x1[ind_adv] * (t < res2[ind_adv]).float().reshape([-1, *[1] * self.ndims]) + adv[
    #                         ind_adv] * (t >= res2[ind_adv]).float().reshape([-1, *[1] * self.ndims])
    #                     res2[ind_adv] = t * (t < res2[ind_adv]).float() + res2[ind_adv] * (t >= res2[ind_adv]).float()
    #                     x1[ind_adv] = im2[ind_adv] + (x1[ind_adv] - im2[ind_adv]) * self.beta
    #                 counter_iter += 1
    #         counter_restarts += 1
    #     ind_succ = res2 < 10000000000.0
    #     if self.verbose:
    #         print('success rate: {:.0f}/{:.0f}'.format(ind_succ.float().sum(),
    #                                                    corr_classified) + ' (on correctly classified points) in {:.1f} s'.format(
    #             time.time() - startt))
    #     res_c[pred] = res2 * ind_succ.float() + 10000000000.0 * (1 - ind_succ.float())
    #     ind_succ = self.check_shape(ind_succ.nonzero().squeeze())
    #     adv_c[pred[ind_succ]] = adv[ind_succ].clone()
    #     return adv_c
    real_instruction = '''
refactor the following Python code with star-in-func-call. You give all code pairs where each pair consists of non-idiomatic Python code and the corresponding refactored code. 
def forward(self, teacher_model, student_model):
        teacher_distill_pairs = teacher_model.yolo_head.loss.distill_pairs
        student_distill_pairs = student_model.yolo_head.loss.distill_pairs
        distill_reg_loss, distill_cls_loss, distill_obj_loss = [], [], []
        for s_pair, t_pair in zip(student_distill_pairs, teacher_distill_pairs):
            distill_reg_loss.append(
                self.obj_weighted_reg(s_pair[0], s_pair[1], s_pair[2], s_pair[
                    3], t_pair[0], t_pair[1], t_pair[2], t_pair[3], t_pair[4]))
            distill_cls_loss.append(
                self.obj_weighted_cls(s_pair[5], t_pair[5], t_pair[4]))
            distill_obj_loss.append(self.obj_loss(s_pair[4], t_pair[4]))
        distill_reg_loss = paddle.add_n(distill_reg_loss)
        distill_cls_loss = paddle.add_n(distill_cls_loss)
        distill_obj_loss = paddle.add_n(distill_obj_loss)
        loss = (distill_reg_loss + distill_cls_loss + distill_obj_loss
                ) * self.weight
        return loss'''
    examples=[['''refactor the following Python code with star-in-func-call. You give all code pairs where each pair consists of non-idiomatic Python code and the corresponding refactored code. 
def get_plan(self, xyt_position):
    """
        Generates a plan that can take take the robot to given goal state.

        :param xyt_position: The goal state of the form (x,y,t)

        :type xyt_position: list
        """
    collector.add_change(region[0], region[1], mapping[name])
    (plan, status) = self.planner.get_plan_absolute(xyt_position[0], xyt_position[1], xyt_position[2])
    if not status:
        raise ValueError('Failed to find a valid plan!')
    return self.planner.parse_plan(plan)
    ''','''Non-idiomatic code:xyt_position[0], xyt_position[1], xyt_position[2]
refactored code: *xyt_position[:3]
********
Non-idiomatic code: region[0], region[1]
refactored code: *region[:2]
    ''']]
    msg = chatgpt_util.format_message_2(real_instruction, examples=examples, sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)#,model="gpt-3.5-turbo"
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])

def call_star_one():
    real_instruction = '''refactor the following Python code with star-in-func-call. 
self.obj_weighted_cls(s_pair[5], t_pair[5], t_pair[4]))
                '''
    examples = []
    msg = chatgpt_util.format_message_2(real_instruction, examples=examples, sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)  # ,model="gpt-3.5-turbo"
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])

def call_star_one():
    real_instruction = '''Use the slice operator [:] to slice "a.t_pair()" to get the elements "a.t_pair()[5]", "a.t_pair()[4]" in Python.
                '''
    examples = []
    msg = chatgpt_util.format_message_2(real_instruction, examples=examples, sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)  # ,model="gpt-3.5-turbo"
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])

def instr_extract_call_node():
    #Write Python code to extract Call nodes for a given Python code.
    #Write Python code to extract all BoolOp nodes whose op is and for a given Python code.
#Write Python code to extract combinations consisting of two different Compare AST nodes from a given BoolOP AST node.
#Write Python code to determine if compare operands of a given compare AST node and another given compare AST node intersect.
#Write Python code to determine if compare operands of a given compare AST node and another given compare AST node intersect.
#Write Python method code to join a given list of strings.

    real_instruction = '''
Write Python code to extract combinations consisting of two different Compare AST nodes from a given BoolOP AST node.
    '''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])

def instr_refact_set_comprehension_for_code():
    #Write Python code to extract Call nodes for a given Python code.
    #Write Python code to extract all BoolOp nodes whose op is and for a given Python code.
#Write Python code to extract combinations consisting of two different Compare AST nodes from a given BoolOP AST node.
#Write Python code to determine if compare operands of a given compare AST node and another given compare AST node intersect.
#Write Python code to determine if compare operands of a given compare AST node and another given compare AST node intersect.
#Write Python method code to join a given list of strings.

    real_instruction = '''Refactor the following Python code with set comprehension. You give all code pairs where each pair consists of non-idiomatic Python code and the corresponding refactored code. 
Python code:
for subdomain in subdomains:
    a.add(subdomain)
subdomains = a.union(bruteforce_list)
                    '''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
    print(">>>>>>>>>>each response:\n", response["choices"][0]["message"]["content"])

def instr_get_For_node():
    #Write Python code to extract Call nodes for a given Python code.
    #Write Python code to extract all BoolOp nodes whose op is and for a given Python code.
#Write Python code to extract combinations consisting of two different Compare AST nodes from a given BoolOP AST node.
#Write Python code to determine if compare operands of a given compare AST node and another given compare AST node intersect.
#Write Python code to determine if compare operands of a given compare AST node and another given compare AST node intersect.
#Write Python method code to join a given list of strings.
# Write Python method code to extract For nodes from a Python code.Write Python method code to extract BoolOP nodes whose op is "and" from a Python code.
    #Write Python method code to replace substring1 with substring2 in a string

    real_instruction = '''Write Python method code to check whether a For node has a "append" function call
'''
    msg = chatgpt_util.format_message_2(real_instruction, examples=[], sys_msg="You are a helpful assistant.")
    # try:
    print(">>>>>>>>>>instruction:\n", real_instruction)
    response = chatgpt_util.chatGPT_result(msg)
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
    # instr_unpack()
    # instr_direct_list_comprehension()


      # instr_direct_chain_comparison()
    # instr_direct_star_func()
    # instr_direct_chain_comapre()
    # instr_direct_chain_comapre_reverse()
    # instr_direct_list_comprehension()
    # instr_direct_star_func()
    # instr_direct_star_func_code_pair()
    # call_star_one()
    # instr_extract_call_node()
    # instr_direct_chain_comapre()
    # instr_refact_set_comprehension_for_code()
    # instr_find()
    # instr_direct_chain_comapre()
    instr_get_For_node()
    # instr_direct_star_func_code_pair()
# instr_find_3()
    # instr_find_composition()

