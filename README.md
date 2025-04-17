# lua2python
Lua-to-Python transpiler via AST manipulation: Parses Lua code, transforms its AST to Python AST, and generates Python source. Built with luaparser and astunparse.



## How to Run

```shell
pip install -r requirements.txt
python3 compile.py <source_file>
```
the output file will write to lua2python/output path

Example `python3 compile.py ./example/basic_test.lua` will output to example/basic_test.lua

## Architecture

![image](./Image/image.png)

## Roadmap

- [x] Single line comments
- [x] Multiline comments
- [x] Numbers
- [x] Strings
- [x] Nil types
- [x] Variable assignments
- [x] Addition

## Referrence

- [lua parser](https://github.com/boolangery/py-lua-parser)