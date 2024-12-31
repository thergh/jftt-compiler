
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

### VIRTUAL MACHINE COMPILATION

To compile virtual machine, use make command:

```
make virtual-machine/Makefile
```

### USING THE COMPILER

To compile your code, put it's path as an argument to the compilator.

```
python3 src/compiler.py examples/my-gcd.imp output/my-gcd.mr
```

### RUNNING GENERATED CODE

To run generated machine code, use the provided virtual machine. Put path to the code as an argument to the machine.

```
virtual-machine/maszyna-wirtualna output/my-gcd.mr
```


