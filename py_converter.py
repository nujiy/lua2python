import ast as py_ast
from luaparser import ast as lua_ast
from luaparser import astnodes

processed_nodes = set()

def lua_ast_to_py_ast(lua_tree):
    lua_truthy_func = py_ast.FunctionDef(
        name='lua_truthy',
        args=py_ast.arguments(
            posonlyargs=[],
            args=[py_ast.arg(arg='value', annotation=None)],
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[],
        ),
        body=[
            py_ast.Return(
                value=py_ast.BoolOp(
                    op=py_ast.And(),
                    values=[
                        py_ast.Compare(
                            left=py_ast.Name(id='value', ctx=py_ast.Load()),
                            ops=[py_ast.IsNot()],
                            comparators=[py_ast.Constant(value=None)]
                        ),
                        py_ast.Compare(
                            left=py_ast.Name(id='value', ctx=py_ast.Load()),
                            ops=[py_ast.IsNot()],
                            comparators=[py_ast.Constant(value=False)]
                        )
                    ]
                )
            )
        ],
        decorator_list=[],
    )
    global processed_nodes
    processed_nodes.clear()
    lua_nodes = parse_tree(lua_tree)
    need_lua_truthy_= need_lua_truthy(lua_nodes)
    py_ast_tree = parse_nodes(lua_nodes)

    if need_lua_truthy_:
        if isinstance(py_ast_tree, list):
            py_final_tree = py_ast.Module(body=[lua_truthy_func] + py_ast_tree)
        else:
            py_final_tree = py_ast.Module(body=[lua_truthy_func, py_ast_tree])
    else:
        py_final_tree = py_ast.Module(py_ast_tree)

    py_final_tree = py_ast.fix_missing_locations(py_final_tree)

    return py_final_tree


def need_lua_truthy(lua_nodes):
    for node in lua_nodes:
        if isinstance(node, (astnodes.If)):
            return True
    return False
        

def parse_tree(lua_tree):
    lua_nodes = []
    for node in lua_ast.walk(lua_tree):
        lua_nodes.append(node)
    return lua_nodes

def parse_nodes(lua_nodes, ctx_klass = py_ast.Load):
    global processed_nodes
    out = []
    while len(lua_nodes) > 0:
        node = lua_nodes.pop(0)

        if id(node) in processed_nodes:
            continue

        if isinstance(node, astnodes.Chunk):
            continue

        if isinstance(node, astnodes.Comment):
            continue

        if isinstance(node, astnodes.Block):
            processed_nodes.add(id(node))
            block = parse_nodes(node.body)
            wrap_expr = lambda x: py_ast.Expr(value=x) if isinstance(x, py_ast.Call) else x
            out.append(
                [wrap_expr(elem) for elem in block]
            )
            # TODO handle `local` keyword
            continue

        if isinstance(node, astnodes.Assign):
            processed_nodes.add(id(node))
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
            processed_nodes.add(id(node))
            # ast.Num will be removed in future Python releases
            # out.append(py_ast.Num(n=node.n))
            out.append(py_ast.Constant(value=node.n))
            continue
        
        if isinstance(node, astnodes.TrueExpr):
            processed_nodes.add(id(node))
            out.append(py_ast.Constant(True))
            continue
        
        if isinstance(node, astnodes.FalseExpr):
            processed_nodes.add(id(node))
            out.append(py_ast.Constant(True))
            continue
        
        if isinstance(node, astnodes.String):
            processed_nodes.add(id(node))
            out.append(py_ast.Constant(node.s))
            continue

        if isinstance(node, astnodes.Nil):
            processed_nodes.add(id(node))
            out.append(py_ast.Constant(value=None))
            continue
        
        if isinstance(node, astnodes.Call):
            processed_nodes.add(id(node))
            processed_nodes.add(id(node.func))
            out.append(
                py_ast.Call(
                    func=py_ast.Name(id=node.func.id, ctx=py_ast.Load()),
                    args=parse_nodes(node.args, ctx_klass=py_ast.Load),
                    keywords=[]
                )
            )
            continue
        
        if isinstance(node, astnodes.AriOp):
            processed_nodes.add(id(node))
            arg_left = parse_nodes([node.left])
            arg_right = parse_nodes([node.right])
            ops_type = node.__class__.__name__
            ops_ref = ARITHMETIC_OPERATORS[ops_type]()
            # other Arithmetic Operators
            out.append(
                py_ast.BinOp(
                    left=arg_left,
                    op=ops_ref,
                    right=arg_right,
                )
            )
            continue

        if isinstance(node, astnodes.If):
            processed_nodes.add(id(node))
            test_nodes = parse_nodes([node.test])
            body_nodes = parse_nodes([node.body])
            else_nodes = parse_nodes([node.orelse])
            wrapped_test = py_ast.Call(
                func=py_ast.Name(id='lua_truthy', ctx=py_ast.Load()),
                args=[test_nodes],  # test_nodes
                keywords=[]
            )

            out.append(
                py_ast.If(
                    test=wrapped_test,
                    body=body_nodes,
                    orelse=else_nodes,
                )
            )
            continue
        
        # ">", ">=", "<", "<=", "==", "~="
        if isinstance(node, astnodes.RelOp):
            processed_nodes.add(id(node))
            arg_left = parse_nodes([node.left])
            arg_right = parse_nodes([node.right])
            ops_type = node.__class__.__name__
            ops_ref = RELATIONAL_OPERATORS[ops_type]()
            out.append(
                py_ast.Compare(
                    left=arg_left,
                    ops=[ops_ref],
                    comparators=arg_right,
                )
            )
            continue

        if isinstance(node, astnodes.LoOp):
            processed_nodes.add(id(node))
            arg_left = parse_nodes([node.left])
            arg_right = parse_nodes([node.right])
            ops_type = node.__class__.__name__
            ops_ref = LOGICAL_OPERATORS[ops_type]()
            out.append(
                py_ast.BoolOp(
                    op=ops_ref,
                    values=[
                        arg_left,
                        arg_right
                    ]
                )
            )
            continue

        if isinstance(node, astnodes.ULNotOp):
            processed_nodes.add(id(node))
            operand = parse_nodes([node.operand])
            out.append(
                py_ast.UnaryOp(
                    op=py_ast.Not(),
                    operand=operand
                )
            )
            continue

        if isinstance(node, astnodes.Function):
            processed_nodes.add(id(node))
            processed_nodes.add(id(node.name))
            body_nodes = parse_nodes([node.body])
            out.append(
                py_ast.FunctionDef(
                    name=node.name.id,
                    args=py_ast.arguments(
                        args=[
                            py_ast.arg(
                                arg = x.id,
                                annotation = None,
                            ) for x in node.args if not processed_nodes.add(id(x)) or True
                        ],
                        vararg=None,
                        kwonlyargs=[],
                        kw_defaults=[],
                        kwarg=None,
                        defaults=[]
                    ),
                    body=body_nodes,
                    decorator_list=[],
                )
            )
            continue

        if isinstance(node, astnodes.Return):
            processed_nodes.add(id(node))
            out.append(
                py_ast.Return(
                    value=parse_nodes(node.values)
                )
            )
            continue 

        if isinstance(node, astnodes.Name):
            processed_nodes.add(id(node))
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

RELATIONAL_OPERATORS = {
    'GreaterThanOp': py_ast.Gt,
    'GreaterOrEqThanOp': py_ast.GtE,
    'LessThanOp': py_ast.Lt,
    'LessOrEqThanOp': py_ast.LtE,
    'EqToOp': py_ast.Eq,
    'NotEqToOp': py_ast.NotEq
}

LOGICAL_OPERATORS = {
    'AndLoOp': py_ast.And,
    'OrLoOp': py_ast.Or,
}

def lua_truthy(value):
    return value is not None and value is not False