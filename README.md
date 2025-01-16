
### Author: Łukasz Ciświcki

Program compiles a procedural language to machine code that can by run using the provided virtual machine.

### FILES

- **src/kompilator.py**: Compiler main file
- **src/generator.py**: Machine code generator for the compiler
- **src/table.py**: Symbol table for the compiler
- **src/lexer.py**: Lexer
- **src/table.py**: Parser

### REQUIREMENTS

To run the compiler, **python 3.6** and **sly** library are required.

```
apt install python3.6
```

```
pip3 install sly
```

For instructions about the virtual machine,
go to /virtual-machine/ReadMe.txt 

### USING THE COMPILER

To compile your code, put its path as an argument to the compiler.

```
python3 src/compiler.py examples/my-gcd.imp output/my-gcd.mr
```


