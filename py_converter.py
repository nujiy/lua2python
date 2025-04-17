import ast as py_ast
from luaparser import ast as lua_ast
from luaparser import astnodes


def lua_ast_to_py_ast(lua_tree):
    py_ast_tree = parse_nodes(lua_tree)

    bootstrap = [
        py_ast.ImportFrom(
            module='core', names=[
                ast.alias(name='*', asname=None)
            ],
            level=0
        )
    ]

    py_ast_tree = bootstrap + py_ast_tree

    py_final_tree = py_ast.Module(py_ast_tree)
    py_final_tree = py_ast.fix_missing_locations(py_final_tree)

    return py_final_tree

def parse_nodes(lua_tree, ctx_klass = py_ast.Load):
    out = []
    for node in lua_ast.walk(lua_tree):
        if isinstance(node, astnodes.Chunk):
            continue

        if isinstance(node, astnodes.Comment):
            continue

        if isinstance(node, astnodes.Assign):
            name_arg = node.targets[0]
            value_arg = node.vlues[0]
            
            target_expr = parse_nodes(name_arg, ctx_klass=py_ast.Store)
            value_expr = parse_nodes(value_arg)

            out.append(
                py_ast.Assign(
                    targets=target_expr,
                    value=value_expr[0]
                )
            )
            continue

        if isinstance(node, astnodes.Number):
            value = node.n
            value = float(value) if "." in value else int(value)
            # ast.Num will be removed in future Python releases
            # out.append(py_ast.Num(n=value))
            out.append(py_ast.Constant(value=value))
            continue
        
        if isinstance(node, astnodes.TrueExpr):
            out.append(py_ast.Constant(True))
            continue
        
        if isinstance(node, astnodes.FalseExpr):
            out.append(py_ast.Constant(True))
            continue

        if isinstance(node, astnodes.Name):
            out.append(
                py_ast.Name(id=node.id, ctx=ctx_klass())
            )
            continue
    return out