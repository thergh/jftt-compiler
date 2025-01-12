from sly import Parser
from lexer import MyLexer


class MyParser(Parser):
    
    tokens = MyLexer.tokens
    
    precedence = (
    ('right', 'UMINUS'),
    ('left', '+', '-'),
    ('left', '*', '/', '%'),
    )
    
    
    
    @_('procedures main')
    def program_all(self, p):
        return ('prall', p[0], p[1], p.lineno)
    
    
    @_('procedures PROCEDURE proc_head IS declarations BEGIN commands END')
    def procedures(self, p):
        return ('procs_LONG',
                p[0], p[2], p[4], p[6], p.lineno)
    
    @_('procedures PROCEDURE proc_head IS BEGIN commands END')
    def procedures(self, p):
        return ('procs_SHORT',
                p[0], p[2], p[5], p.lineno)
    
    @_('')
    def procedures(self, p):
        return ('procs_EMPTY')
    
    
    @_('PROGRAM IS declarations BEGIN commands END')
    def main(self, p):
        return ('mn_LONG', p[2], p[4], p.lineno)
    
    @_('PROGRAM IS BEGIN commands END')
    def main(self, p):
        return ('mn_SHORT', p[3], p.lineno)
    
    
    @_('commands command')
    def commands(self, p):
        return ('comms_REC', p[0], p[1], p.lineno)
    
    @_('command')
    def commands(self, p):
        return ('comms_SINGLE', p[0], p.lineno)
    
    
    @_('identifier ASSIGN expression ";"')
    def command(self, p):
        return ('comm_ASSIGN', p[0], p[2], p.lineno)
    
    @_('IF condition THEN commands ELSE commands ENDIF')
    def command(self, p):
        return ('comm_IF_ELSE', p[1], p[3], p[5], p.lineno)
    
    @_('IF condition THEN commands ENDIF')
    def command(self, p):
        return ('comm_IF', p[1], p[3], p.lineno)
    
    @_('WHILE condition DO commands ENDWHILE')
    def command(self, p):
        return ('comm_WHILE', p[1], p[3], p.lineno)
    
    @_('REPEAT commands UNTIL condition ";"')
    def command(self, p):
        return ('comm_REPEAT', p[1], p[3], p.lineno)
    
    @_('FOR PID FROM value TO value DO commands ENDFOR')
    def command(self, p):
        return ('comm_FOR',
                p.PID, p[3], p[5], p[7], p.lineno)
    
    @_('FOR PID FROM value DOWNTO value DO commands ENDFOR')
    def command(self, p):
        return ('comm_FOR_DOWN',
                p.PID, p[3], p[5], p[7], p.lineno)
    
    @_('proc_call ";"')
    def command(self, p):
        return ('comm_CALL', p[0], p.lineno)
    
    @_('READ identifier ";"')
    def command(self, p):
        return ('comm_READ', p[1], p.lineno)
    
    @_('WRITE value ";"')
    def command(self, p):
        return ('comm_WRITE', p[1], p.lineno)
    
    
    @_('PID "(" args_decl ")"')
    def proc_head(self, p):
        return ('phead', p.PID, p[2], p.lineno)
    
    
    @_('PID "(" args ")"')
    def proc_call(self, p):
        return ('pcall', p.PID, p[2], p.lineno)
    
    
    @_('declarations "," PID')
    def declarations(self, p):
        return ('decs_REC_PID', p[0], p[2], p.lineno)
    
    @_('declarations "," PID "[" NUM ":" NUM "]"')
    def declarations(self, p):
        return ('decs_REC_ARRAY', p[0], p.PID, p[4], p[6], p.lineno)
    
    @_('PID')
    def declarations(self, p):
        return ('decs_PID', p.PID, p.lineno)
    
    @_('PID "[" NUM ":" NUM "]"')
    def declarations(self, p):
        return ('decs_ARRAY', p.PID, p[2], p[4], p.lineno)    
        
    
    @_('args_decl "," PID')
    def args_decl(self, p):
        return ('ard_REC_PID', p[0], p[2], p.lineno)
    
    @_('args_decl "," "T" PID')
    def args_decl(self, p):
        return ('ard_REC_ARRAY', p[0], p[3], p.lineno)    
            
    @_('PID')
    def args_decl(self, p):
        return ('ard_PID', p.PID, p.lineno)   
    
    @_('"T" PID')
    def args_decl(self, p):
        return ('ard_ARRAY', p.PID, p.lineno)
    
    
    @_('args "," PID')
    def args(self, p):
        return ('ar_REC', p[0], p[2], p.lineno)
    
    @_('PID')
    def args(self, p):
        return ('ar_PID', p[0], p.lineno)
    
    
    @_('"-" value %prec UMINUS')
    def expression(self, p):
        return ('expr_UMINUS', p[1], p.lineno)

    @_('value')
    def expression(self, p):
        return ('expr_VAL', p[0])

    @_('value "+" value',
       'value "-" value',
       'value "*" value',
       'value "/" value',
       'value "%" value',)
    def expression(self, p):
        return ('expr_OP', p[0], p[1], p[2], p.lineno)
    
    
    @_('value "=" value',
       'value NE value',
       'value ">" value',
       'value "<" value',
       'value GE value',
       'value LE value',
       )
    def condition(self, p):
        return ('cond', p[0], p[1], p[2], p.lineno)
    
    
    @_('NUM')
    def value(self, p):
        return ('val_NUM', p.NUM, p.lineno)
        
    @_('identifier')
    def value(self, p):
        return('val_ID', p[0], p.lineno)
    
    
    @_('PID "[" PID "]"')
    def identifier(self, p):
        return ('id_ARRAY_PID', p[0], p[2], p.lineno)
        
    @_('PID "[" NUM "]"')  
    def identifier(self, p):
        return ('id_ARRAY_NUM', p.PID, p.NUM, p.lineno)
        
    @_('PID')  
    def identifier(self, p):
        return ('id_PID', p.PID, p.lineno)
    
    
if __name__ == '__main__':
    lexer = MyLexer()
    parser = MyParser()

    with open('examples/program3.imp', 'r') as file:
        data = file.read()
        
    tokens = lexer.tokenize(data)
    
    result = parser.parse(tokens)
    
    print(result)

    