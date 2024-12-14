from sly import Parser
from lexer import MyLexer


class ASTNode:
    pass

class ProgramAll(ASTNode):
    def __init__(self, procedures, main):
        super().__init__()
        self.procedures = procedures
        self.main = main
    

class ProceduresDecl(ASTNode):
    def __init__(self, procedures, proc_head, declarations, commands):
        super().__init__()
        self.procedures = procedures
        self.proc_head = proc_head
        self.declarations = declarations
        self.commands = commands
    
class MyParser(Parser):
    
    tokens = MyLexer.tokens
    
    # @_('procedures main')
    # def program_all(self, p):
    #     return ('prall=procs_mn', p[0], p[1])
    
    @_('procedures main')
    def program_all(self, p):
        return ProgramAll(p[0], p[1])
    
    
    # @_('procedures PROCEDURE proc_head IS declarations BEGIN commands END')
    # def procedures(self, p):
    #     return ('procs=procs_PROCEDURE_phead_IS_decs_BEGIN_comms_END',
    #             p[0], p[2], p[4], p[6])
    
    @_('procedures PROCEDURE proc_head IS declarations BEGIN commands END')
    def procedures(self, p):
        return (ProceduresDecl(p[0], p[2], p[4], p[6]))
    
    @_('procedures PROCEDURE proc_head IS BEGIN commands END')
    def procedures(self, p):
        return ('procs=procs_PROCEDURE_phead_IS_BEGIN_comm_END',
                p[0], p[2], p[5])
    
    @_('')
    def procedures(self, p):
        return [('procs=empty')]
    
    
    @_('PROGRAM IS declarations BEGIN commands END')
    def main(self, p):
        return ('mn=PROGRAM_IS_decs_BEGIN_comms_END', p[2], p[4])
    
    @_('PROGRAM IS BEGIN commands END')
    def main(self, p):
        return ('mn=PROGRAM_IS_BEGIN_comms_END', p[3])
    
    
    @_('commands command')
    def commands(self, p):
        return ('comms=comms_comm', p[0], p[1])
    
    @_('command')
    def commands(self, p):
        return ('comms=comm', p[0])
    
    
    @_('identifier ASSIGN expression ";"')
    def command(self, p):
        return ('comm_id=ASSIGN_expr_;', p[0], p[2])
    
    @_('IF condition THEN commands ELSE commands ENDIF')
    def command(self, p):
        return ('comm=IF_cond_THEN_comm_ELSE_comm_ENDIF', p[1], p[3], p[5])
    
    @_('IF condition THEN commands ENDIF')
    def command(self, p):
        return ('comm=IF_cond_THEN_cond_ENDIF', p[1], p[3])
    
    @_('WHILE condition DO commands ENDWHILE')
    def command(self, p):
        return ('comm=WHILE_cond_DO_comm_ENDWHILE', p[1], p[3])
    
    @_('REPEAT commands UNTIL condition ";"')
    def command(self, p):
        return ('comm=REPEAT_comm_UNTIL_cond_;', p[1], p[3])
    
    @_('FOR PID FROM value TO value DO commands ENDFOR')
    def command(self, p):
        return ('comm=FROM_PID_FROM_val_TO_val_DO_comm_ENDFOR',
                p.PID, p[3], p[5], p[7])
    
    @_('FOR PID FROM value DOWNTO value DO commands ENDFOR')
    def command(self, p):
        return ('comm=FOR_PID_FROM_val_DOWNTO_val_DO_comm_ENDFOR',
                p.PID, p[3], p[5], p[7])
    
    @_('proc_call ";"')
    def command(self, p):
        return ('comm=pcall_;', p[0])
    
    @_('READ identifier ";"')
    def command(self, p):
        return ('comm=READ_id_;', p[1])
    
    @_('WRITE value ";"')
    def command(self, p):
        return ('comm=WRITE_val_;', p[1])
    
    
    @_('PID "(" args_decl ")"')
    def proc_head(self, p):
        return ('phead=PID_(_ard_)', p.PID, p[2])
    
    
    @_('PID "(" args ")"')
    def proc_call(self, p):
        return ('pcall=PID_(_ar_)', p.PID, p[2])
    
    
    @_('declarations "," PID')
    def declarations(self, p):
        return ('decs=decs_,_PID', p[0], p[2])
    
    @_('declarations "," PID "[" NUM ":" NUM "]"')
    def declarations(self, p):
        return ('decs=decs_,_PID_[_NUM_:_NUM_]', p[0], p.PID, p[4], p[6])
    
    @_('PID')
    def declarations(self, p):
        return ('decs=PID', p.PID)
    
    @_('"T" PID')
    def declarations(self, p):
        return ('decs=T_PID', p.PID)    
        
    
    @_('args_decl "," PID')
    def args_decl(self, p):
        return ('ard=ard_,_PID', p[0], p[2])
    
    @_('args_decl "," "T" PID')
    def args_decl(self, p):
        return ('ard=ard_T_PID', p[0], p[3])    
            
    @_('PID')
    def args_decl(self, p):
        return ('ard=PID', p.PID)   
    
    @_('"T" PID')
    def args_decl(self, p):
        return ('ard=T_PID', p[0], p.PID)
    
    
    @_('args "," PID')
    def args(self, p):
        return ('ar=ar_,_PID', p[0], p[2])
    
    @_('PID')
    def args(self, p):
        return ('ar=PID', p[0])
    
    
    @_('value')
    def expression(self, p):
        return ('expr=val', p[0])

    @_('value "+" value',
       'value "-" value',
       'value "*" value',
       'value "/" value',
       'value "%" value',)
    def expression(self, p):
        return ('expr=val_*_val')
    
    
    @_('value "=" value',
       'value NE value',
       'value ">" value',
       'value "<" value',
       'value GE value',
       'value LE value',
       )
    def condition(self, p):
        return ('cond=val_?_val', p[1], p[0], p[2])
    
    
    @_('NUM')
    def value(self, p):
        return ('val=NUM', p.NUM)
        
    @_('identifier')
    def value(self, p):
        return('val=id', p[0])
    
    
    @_('PID "[" PID "]"')
    def identifier(self, p):
        return ('id=PID_[_PID_]', p[0], p[2])
        
    @_('PID "[" NUM "]"')  
    def identifier(self, p):
        return ('id=[_num_]', p.PID, p.NUM)
        
    @_('PID')  
    def identifier(self, p):
        return ('id=PID', p.PID)
    
    
if __name__ == '__main__':
    lexer = MyLexer()
    parser = MyParser()

    with open('examples/program3.imp', 'r') as file:
        data = file.read()
        
    tokens = lexer.tokenize(data)
    
    result: ProgramAll = parser.parse(tokens)
    
    print(result)
    print(result)

    
    
