from parser import MyParser
from lexer import MyLexer
from generator import CodeGenerator
from table import SymbolTable



# if __name__ == '__main__':
#     lexer = MyLexer()
#     parser = MyParser()

#     input = 'examples/my-print.imp'
#     output = 'output/my-out.mr'

#     with open(input, 'r') as file:
#         data = file.read()
        
#     tokens = lexer.tokenize(data)
#     parsed = parser.parse(tokens)
    
#     gen = CodeGenerator(parsed, True)
#     code = gen.generate_code()
    
# with open(output, 'w') as file:
#     for line in code:
#         file.write(line + '\n')