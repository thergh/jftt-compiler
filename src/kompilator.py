from parser import MyParser
from lexer import MyLexer
from generator import CodeGenerator
import sys


if __name__ == '__main__':
    lexer = MyLexer()
    parser = MyParser()

    input = sys.argv[1]
    output = sys.argv[2]

    with open(input, 'r') as file:
        data = file.read()
        
    tokens = lexer.tokenize(data)
    
    parsed = parser.parse(tokens)
    
    gen = CodeGenerator(parsed, False)
    
    code = gen.generate_code()

    with open(output, 'w') as file:
        for line in code:
            file.write(line + '\n')