import sys
from luaparser import ast as lua_ast
import py_converter
import ast as py_ast # dump python AST to check the result

import astunparse

def run(source_file):
    file_handler = open(source_file, 'r')
    source = file_handler.read()
    
    ast_ = lua_ast.parse(source)
    print(lua_ast.to_pretty_str(ast_))



if __name__ == '__main__':
    run('test.lua')