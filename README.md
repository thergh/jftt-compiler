# JFTT Compiler

**A compiler for a custom procedural language, generating machine code for a dedicated virtual machine.**

[![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![SLY](https://img.shields.io/badge/SLY-Lex--Yacc-blue)](https://github.com/dabeaz/sly)


## Features
*   **Lexical Analysis:** Tokenization of source code using Sly Lex-Yacc.
*   **Syntax Parsing:** Grammar validation and AST construction.
*   **Symbol Management:** Symbol table for tracking variables and scope.
*   **Machine Code Generation:** Translation of high-level constructs into low-level instructions.

| Component | Technology |
| :--- | :--- |
| **Language** | Python 3.6+ |
| **Parser Generator** | SLY (Sly Lex-Yacc) |
| **Architecture** | Modular Compiler Design |
| **Target** | Virtual Machine Assembly |


## Local Installation and Execution

1.  **Environment Setup:**
    Ensure you have Python 3 installed.
    ```bash
    apt install python3
    ```

2.  **Dependencies:**
    Install the required `sly` library:
    ```bash
    pip3 install sly
    ```

3.  **Compilation:**
    To compile a source file, provide the input and output paths:
    ```bash
    python3 src/kompilator.py tests/exampleA.imp output.mr
    ```

4.  **Testing:**
    Run the provided test scripts to verify the compiler:
    ```bash
    ./run-tests.sh
    ```
