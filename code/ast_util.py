import ast
class Rewrite_call(ast.NodeTransformer):
    def __init__(self,node_list,new_node,call_node):
        self.old_node =node_list
        self.new_node =new_node
        self.call_node=call_node


    def visit_Call(self, node):
        # print("***********come call: ",node.lineno,ast.unparse(node),self.old_node)
        # for e in self.old_node:
        #     print("arg: ",ast.unparse(e),e.lineno)
        new_args = []
        beg = -1
        for ind, arg in enumerate(node.args):

            # print("***********come arg", ast.unparse(arg),arg.lineno)
            for old_arg_node in self.old_node:
                # old_arg_node=old_arg
                if ast.unparse(arg) == ast.unparse(old_arg_node) and arg.lineno == old_arg_node.lineno:
                    # print("***********come here",ast.unparse(arg))
                    if beg == -1:
                        beg = ind
                    break
            else:
                new_args.append(arg)
        if beg==-1:
            for ind, arg in enumerate(node.args):
                node.args[ind] = self.visit(arg)
            return node
        new_args.insert(beg, self.new_node)
        node.args = new_args
        return node


def get_all_var(tars,var_list):

    for e in tars:
        if hasattr(e, "elts"):
            # count += len(e.elts)
            # for cur in e.elts:
            get_all_var(e.elts,var_list)

        else:
            # print(e.__dict__, " are not been parsed")
            var_list.append(e)

def get_basic_count(e):

    count=0
    # print("e dict: ",e.__dict__)
    if isinstance(e, (ast.Tuple,ast.List,ast.Set)):
        # count += len(e.elts)
        for cur in e.elts:
            count +=get_basic_count(cur)

    else:
        # print(e.__dict__, " are not been parsed")
        count +=1


    return count

def get_parent_node(node,find_node):
    from collections import deque
    todo = deque([node])
    while todo:
        node = todo.popleft()
        for child in ast.iter_child_nodes(node):
            if child is find_node:
                return node
            todo.append(child)