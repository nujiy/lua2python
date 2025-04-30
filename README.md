# lua2python
A "Lua to Python" transpiler via AST manipulation: Parses Lua code, transforms its AST to Python AST, and generates Python source. Built with luaparser and astunparse.



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
- [ ] Multiplication
- [ ] 引き算（Subtraction）
- [ ] Boolean types
- [ ] If statements
- [ ] Nested if statements
- [ ] `function` declarations
- [ ] `return`
- [ ] Assign function return to variable
- [ ] `or` logical operator
- [ ] `and` logical operator
- [ ] `local` variables

## Referrence

- [lua parser](https://github.com/boolangery/py-lua-parser)