
### Author: Łukasz Ciświcki

Program compiles a procedural language to machine code that can be run using a virtual machine.

### FILES

- **src/kompilator.py**: Compiler main file
- **src/generator.py**: Machine code generator for the compiler
- **src/table.py**: Symbol table for the compiler
- **src/lexer.py**: Lexer
- **src/table.py**: Parser

### REQUIREMENTS

To run the compiler, **python 3.6** and **sly** library are required.

```
apt install python3
```

```
pip3 install sly
```

### USING THE COMPILER

To compile your code, put its path as an argument to the compiler.

```
python3 src/kompilator.py examples/my-gcd.imp output/my-gcd.mr
```


