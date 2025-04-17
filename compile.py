import sys
import click
from luaparser import ast as lua_ast
import py_converter
import ast as py_ast # dump python AST to check the result

import astunparse

@click.command()
@click.argument('source_file')
def run(source_file):
    file_handler = open(source_file, 'r')
    source = file_handler.read()
    
    lua_ast_tree = lua_ast.parse(source)
    
    # dump Lua AST
    lua_ast.to_pretty_str(lua_ast_tree) 

    # Convert Lua AST to Python AST
    py_ast_tree = py_converter.lua_ast_to_py_ast(lua_ast_tree)

    # dump python AST
    print(py_ast.dump(py_ast_tree))

    # print python source code
    print(astunparse.unparse(py_ast_tree))

    exec(compile(py_ast_tree, filename="<ast>", mode="exec"))


if __name__ == '__main__':
    run()