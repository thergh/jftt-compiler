from sly import Parser
from lexer import MyLexer


class MyParser(Parser):
    
    tokens = MyLexer.tokens
    
    
    
    @_('NUM')
    def value(self, p):
        return ('val_num', p.NUM)
        
    @_('identifier')
    def value(self, p):
        return('val_id', p[0])
    
    
    @_('PID "[" PID "]"')
    def identifier(self, p):
        return ('id_PID', p[0], p[2])
        
    @_('PID "[" NUM "]"')  
    def identifier(self, p):
        return ('id_num', p.PID, p.NUM)
        
    @_('PID')  
    def identifier(self, p):
        return ('id', p.PID)
    
    
# if __name__ == '__main__':
#     lexer = MyLexer()
#     parser = MyParser()

#     with open('../examples/program0.imp', 'r') as file:
#         data = file.read()
        
#     tokens = lexer.tokenize(data)
    
#     result = parser.parse(tokens)
    
#     print(result)


if __name__ == '__main__':
    lexer = MyLexer()
    parser = MyParser()

    while True:
        try:
            text = input('calc > ')
            result = parser.parse(lexer.tokenize(text))
            print(result)
        except EOFError:
            break
        
        
    