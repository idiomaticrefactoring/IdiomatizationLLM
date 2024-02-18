a=[range(10)]
code='''
for _,e0,*_ in a:
    print(e0)
'''

import ast
class Rewrite(ast.NodeTransformer):
    def visit_Name(self, node):
        return ast.Name(id='data', ctx=ast.Load())

for e in ast.walk(ast.parse(code)):
    if isinstance(e,ast.For):
        e.target = Rewrite().visit(e.target)
        print("for: ",ast.unparse(e))

a=["10,20,30"]
print(a)
for e in a:
    e_0,e_1,*e_remain=e
    e=e.split(",")
    print(e_0)
a=["10,20,30"]
for e in a:
    e_0,e_1,*e_remain=e
    e=e.split(",")
    print(e[0])
a=[list(range(10))]
for val in a:
    val[0] = 'user'
    print(val[0])

a=[range(10)]
for val in a:
    a_0,*_=val
    a_0 = 'user'
    print(val[0])



