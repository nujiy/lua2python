import ast as py_ast
from luaparser import ast as lua_ast
from luaparser import astnodes

def lua_ast_to_py_ast(lua_tree):
    py_ast_tree = parse_tree(lua_tree)

    py_final_tree = py_ast.Module(py_ast_tree)
    py_final_tree = py_ast.fix_missing_locations(py_final_tree)

    return py_final_tree

def parse_tree(lua_tree):
    # remove the leaf node
    filtered_nodes = []
    for node in lua_ast.walk(lua_tree):
        if isinstance(node, (astnodes.Name, astnodes.Number, 
                            astnodes.TrueExpr, astnodes.FalseExpr,
                            astnodes.Comment, astnodes.String,
                            astnodes.Nil, astnodes.AriOp)):
            continue
        filtered_nodes.append(node)
    return parse_nodes(filtered_nodes)

def parse_nodes(lua_nodes, ctx_klass = py_ast.Load):
    out = []
    while len(lua_nodes) > 0:
        node = lua_nodes.pop(0)

        if isinstance(node, astnodes.Chunk):
            continue

        if isinstance(node, astnodes.Comment):
            continue

        if isinstance(node, astnodes.Assign):
            target_expr = parse_nodes(node.targets, ctx_klass=py_ast.Store)
            value_expr = parse_nodes(node.values)

            out.append(
                py_ast.Assign(
                    targets=target_expr,
                    value=value_expr
                )
            )
            continue

        if isinstance(node, astnodes.Number):
            # ast.Num will be removed in future Python releases
            # out.append(py_ast.Num(n=node.n))
            out.append(py_ast.Constant(value=node.n))
            continue
        
        if isinstance(node, astnodes.TrueExpr):
            out.append(py_ast.Constant(True))
            continue
        
        if isinstance(node, astnodes.FalseExpr):
            out.append(py_ast.Constant(True))
            continue
        
        if isinstance(node, astnodes.String):
            out.append(py_ast.Constant(node.s))
            continue

        if isinstance(node, astnodes.Nil):
            out.append(py_ast.Constant(value=None))
            continue
        
        if isinstance(node, astnodes.Call):
            out.append(
                py_ast.Expr(
                    value = py_ast.Call(
                            func=py_ast.Name(id=node.func.id, ctx=py_ast.Load()),
                            args=parse_nodes(node.args, ctx_klass=py_ast.Load),
                            keywords=[]
                    )
                )
            )
            continue
        
        if isinstance(node, astnodes.AriOp):
            arg_left = parse_nodes([node.left])
            arg_right = parse_nodes([node.right])
            op_type = node.__class__.__name__
            ops_ref = ARITHMETIC_OPERATORS[op_type]()
            # other Arithmetic Operators
            out.append(
                py_ast.BinOp(
                    left=arg_left,
                    op=ops_ref,
                    right=arg_right,
                )
            )
            continue
        
        if isinstance(node, astnodes.Name):
            out.append(
                py_ast.Name(id=node.id, ctx=ctx_klass())
            )
            continue
    return out

ARITHMETIC_OPERATORS = {
    'AddOp': py_ast.Add,
    'SubOp': py_ast.Sub,
    'MultOp': py_ast.Mult,
    'FloatDivOp': py_ast.Div,
    'FloorDivOp': py_ast.FloorDiv,
    'ModOp': py_ast.Mod,
    'ExpoOp': py_ast.Pow,
}