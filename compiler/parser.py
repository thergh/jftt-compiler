from sly import Parser
from lexer import MyLexer


class MyParser(Parser):
    
    tokens = MyLexer.tokens
    
    
    @_('procedures main')
    def program_all(self, p):
        return ('prall_procs_mn', p[0], p[1])
    
    
    @_('procedures PROCEDURE proc_head IS declarations BEGIN commands END')
    def procedures(self, p):
        return ('procs_procs_PROCEDURE_phead_IS_decs_BEGIN_comms_END',
                p[0], p[2], p[4], p[6])
    
    @_('procedures PROCEDURE proc_head IS BEGIN commands END')
    def procedures(self, p):
        return ('procs_procs_PROCEDURE_phead_IS_BEGIN_comm_END',
                p[0], p[2], p[5])
    
    @_('')
    def procedures(self, p):
        return [('procs_empty')]
    
    
    @_('PROGRAM IS declarations BEGIN commands END')
    def main(self, p):
        return ('mn_PROGRAM_IS_decs_BEGIN_comms_END', p[2], p[4])
    
    @_('PROGRAM IS BEGIN commands END')
    def main(self, p):
        return ('mn_PROGRAM_IS_BEGIN_comms_END', p[3])
    
    
    @_('commands command')
    def commands(self, p):
        return ('comms_comms_comm', p[0], p[1])
    
    @_('command')
    def commands(self, p):
        return ('comms_comm', p[0])
    
    
    @_('identifier ASSIGN expression ";"')
    def command(self, p):
        return ('comm_id_ASSIGN_expr', p[0], p[2])
    
    @_('IF condition THEN commands ELSE commands ENDIF')
    def command(self, p):
        return ('comm_IF_cond_THEN_comm_ELSE_comm_ENDIF', p[1], p[3], p[5])
    
    @_('IF condition THEN commands ENDIF')
    def command(self, p):
        return ('comm_IF_cond_THEN_cond_ENDIF', p[1], p[3])
    
    @_('WHILE condition DO commands ENDWHILE')
    def command(self, p):
        return ('comm_WHILE_cond_DO_comm_ENDWHILE', p[1], p[3])
    
    @_('REPEAT commands UNTIL condition ";"')
    def command(self, p):
        return ('comm_REPEAT_comm_UNTIL_cond', p[1], p[3])
    
    @_('FOR PID FROM value TO value DO commands ENDFOR')
    def command(self, p):
        return ('comm_FROM_PID_FROM_val_TO_val_DO_comm_ENDFOR',
                p.PID, p[3], p[5], p[7])
    
    @_('FOR PID FROM value DOWNTO value DO commands ENDFOR')
    def command(self, p):
        return ('comm_FOR_PID_FROM_val_DOWNTO_val_DO_comm_ENDFOR',
                p.PID, p[3], p[5], p[7])
    
    @_('proc_call ";"')
    def command(self, p):
        return ('comm_pcall', p[0])
    
    @_('READ identifier ";"')
    def command(self, p):
        return ('comm_READ_id', p[1])
    
    @_('WRITE value ";"')
    def command(self, p):
        return ('comm_WRITE_val', p[1])
    
    
    @_('PID "(" args_decl ")"')
    def proc_head(self, p):
        return ('phead_PID_ard', p.PID, p[2])
    
    
    @_('PID "(" args ")"')
    def proc_call(self, p):
        return ('pcall_PID_ar', p.PID, p[2])
    
    
    @_('declarations "," PID')
    def declarations(self, p):
        return ('decs_decs_PID', p[0], p[2])
    
    @_('declarations "," PID "[" NUM ":" NUM "]"')
    def declarations(self, p):
        return ('decs_decs_PID_NUM_NUM', p[0], p.PID, p[4], p[6])
    
    @_('PID')
    def declarations(self, p):
        return ('decs_PID', p.PID)
    
    @_('"T" PID')
    def declarations(self, p):
        return ('decs_T_PID', p.PID)    
        
    
    @_('args_decl "," PID')
    def args_decl(self, p):
        return ('ard_ard_PID', p[0], p[2])
    
    @_('args_decl "," "T" PID')
    def args_decl(self, p):
        return ('ard_ard_T_PID', p[0], p[1])    
            
    @_('PID')
    def args_decl(self, p):
        return ('ard_PID', p.PID)   
    
    @_('"T" PID')
    def args_decl(self, p):
        return ('ard_T_PID', p[0], p.PID)
    
    
    @_('args "," PID')
    def args(self, p):
        return ('ar_ar_PID', p[0], p[1])
    
    @_('PID')
    def args(self, p):
        return ('ar_PID', p[0])
    
    
    @_('value')
    def expression(self, p):
        return ('expr_val', p[0])

    @_('value "+" value',
       'value "-" value',
       'value "*" value',
       'value "/" value',
       'value "%" value',)
    def expression(self, p):
        return ('expr')
    
    
    @_('value "=" value',
       'value NE value',
       'value ">" value',
       'value "<" value',
       'value GE value',
       'value LE value',
       )
    def condition(self, p):
        return ('cond', p[1], p[0], p[2])
    
    
    @_('NUM')
    def value(self, p):
        return ('val_NUM', p.NUM)
        
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
    
    
if __name__ == '__main__':
    lexer = MyLexer()
    parser = MyParser()

    with open('examples/program0.imp', 'r') as file:
        data = file.read()
        
    tokens = lexer.tokenize(data)
    
    result = parser.parse(tokens)
    
    print(result)


# if __name__ == '__main__':
#     lexer = MyLexer()
#     parser = MyParser()

#     while True:
#         try:
#             text = input('calc > ')
#             result = parser.parse(lexer.tokenize(text))
#             print(result)
#         except EOFError:
#             break
        
        
    