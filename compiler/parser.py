from sly import Parser
from lexer import MyLexer
from enum import Enum


class ASTNode:
    pass


class ProgramAll(ASTNode):
    def __init__(self, procedures, main):
        super().__init__()
        self.procedures = procedures
        self.main = main
    
    
class ProceduresType(Enum):
    LONG = 'LONG'
    SHORT = 'SHORT'
    EMPTY = 'EMPTY'
    
class Procedures(ASTNode):
    def __init__(self, procedures_type, **kwargs):
        super().__init__()
        
        if not isinstance(procedures_type, ProceduresType):
            raise ValueError("Invalid type")
        
        self.procedures_type = procedures_type
        self.attributes = kwargs
    
    
class MainType(Enum):
    LONG = 'LONG'    
    SHORT = 'SHORT'

class Main(ASTNode):
    def __init__(self, main_type, **kwargs):
        super().__init__()
        
        if not isinstance(main_type, MainType):
            raise ValueError("Invalid type")
        
        self.main_type = main_type
        self.attributes = kwargs
        
        
class CommandsType(Enum):
    PLURAL = 'PLURAL'
    SINGLE = 'SINGLE'    
        
class Commands(ASTNode):
    def __init__(self, commands_type,  **kwargs):
        super().__init__()
        
        if not isinstance(commands_type, MainType):
            raise ValueError("Invalid type")
        
        self.commands_type = commands_type
        self.attributes = kwargs
        
        
class CommandType(Enum):
    ASSIGN = 'ASSIGN'
    IF_ELSE = 'IF_ELSE'
    IF = 'IF'
    WHILE = 'WHILE'
    REPEAT = 'REPEAT'
    FOR = 'FOR'
    FOR_DOWN = 'FOR_DOWN'
    PROC_CALL = 'PROC_CALL'
    READ = 'READ'
    WRITE = 'WRITE'    
    
class Command(ASTNode):
    def __init__(self, command_type, **kwargs):
        super().__init__()
        
        if not isinstance(command_type, CommandType):
            raise ValueError("Invalid type")
        
        self.command_type = command_type
        self.attributes = kwargs
        

class ProcHead(ASTNode):
    def __init__(self, PID=None, args_decl=None):
        super().__init__()
        self.PID = PID
        self.args_decl =args_decl
        
        
class ProcCall(ASTNode):
    def __init__(self, PID=None, args=None):
        super().__init__()
        self.PID = PID
        self.args = args
        

class DeclarationsType(Enum):
    PLURAL_PID = 'PLURAL_PID'
    PLURAL_TABLE = 'PLURAL_TABLE'
    SINGLE_PID = 'SINGLE_PID'
    SINGLE_TABLE = 'SINGLE_TABLE'
    
        
class Declarations(ASTNode):
    def __init__(self, declarations_type, **kwargs):
        super().__init__()
        
        if not isinstance(declarations_type, DeclarationsType):
            raise ValueError("Invalid type")
          
        self.declarations_type = declarations_type
        self.attributes = kwargs
        

class ArgsDeclType(Enum):
    PLURAL_PID = 'PLURATL_PID'
    PLURAL_T = 'PLURAL_T'
    SINGLE_PID = 'SINGLE_PID'
    SINGLE_T = 'SINGLE_T'    
          
class ArgsDecl(ASTNode):
    def __init__(self, args_decl_type, **kwargs):
        super().__init__()
        
        if not isinstance(args_decl_type, ArgsDeclType):
            raise ValueError("Invalid type")
        
        self.args_decl_type = args_decl_type
        self.attributes = kwargs
        
        
class ArgsType(Enum):
    PLURAL = 'PLURAL'
    SINGLE = 'SINGLE'        
        
class Args(ASTNode):
    def __init__(self, args_type, **kwargs):
        super().__init__()
        
        if not isinstance(args_type, ArgsType):
            raise ValueError("Invalid type")
        
        self.args_type = args_type
        self.attributes = kwargs
        
    
class ExpressionType(Enum):
    ADD = 'ADD'
    SUB = 'SUB'
    MUL = 'MUL'
    DIV ='DIV'
    MOD = 'MOD'
    SINGLE = 'SINGLE'    
    
class Expression(ASTNode):
    def __init__(self, expression_type, **kwargs):
        super().__init__()
        
        if not isinstance(expression_type, ExpressionType):
            raise ValueError("Invalid type")
        
        self.expression_type = expression_type
        self.attributes = kwargs
        
        
class ConditionType(Enum):
    EQ = 'EQ'
    NE = 'NE'
    G = 'G'
    L = 'L'
    GE = 'GE'
    LE = 'LE'

class Condition(ASTNode):
    def __init__(self, condition_type, **kwargs):
        super().__init__()
        
        if not isinstance(condition_type, ConditionType):
            raise ValueError("Invalid type")
        
        self.condition_type = condition_type
        self.attributes = kwargs
        
        
class ValueType(Enum):
    NUM = 'NUM'
    ID = 'ID'
        
class Value(ASTNode):
    def __init__(self, value_type, **kwargs):
        super().__init__()
        
        if not isinstance(value_type, ValueType):
            raise ValueError("Invalid type")
        
        self.value_type = value_type
        self.attributes = kwargs
        
        
class IdentifierType(Enum):
    PID_TABLE = 'PID_TABLE'
    NUM_TABLE = 'NUM_TABLE'
    PID = 'PID'
        
class Identifier(ASTNode):
    def __init__(self, identifier_type, **kwargs):
        super().__init__()
        
        if not isinstance(identifier_type, IdentifierType):
            raise ValueError("Invalid type")
        
        self.identifier_type = identifier_type
        self.attributes = kwargs
            
    
    
class MyParser(Parser):
    
    tokens = MyLexer.tokens


    @_('procedures main')
    def program_all(self, p):
        return ProgramAll(p[0], p[1])
    
    
    @_('procedures PROCEDURE proc_head IS declarations BEGIN commands END')
    def procedures(self, p):
        return Procedures(ProceduresType.LONG, procedures=p[0], proc_head=p[2], declarations=p[4], commands=p[6])
    
    @_('procedures PROCEDURE proc_head IS BEGIN commands END')
    def procedures(self, p):
        return Procedures(ProceduresType.SHORT, procedures=p[0], proc_head=p[2], commands=p[5])
    
    @_('')
    def procedures(self, p):
        return Procedures(ProceduresType.EMPTY)
    
    
    @_('PROGRAM IS declarations BEGIN commands END')
    def main(self, p):
        return Main(MainType.LONG, declarations=p[2], commands=p[4])
    
    @_('PROGRAM IS BEGIN commands END')
    def main(self, p):
        return Main(MainType.SHORT, commands=p[3])
    
    
    @_('commands command')
    def commands(self, p):
        return ('comms=comms_comm', p[0], p[1])
    
    @_('command')
    def commands(self, p):
        return ('comms=comm', p[0])
    
    
    @_('identifier ASSIGN expression ";"')
    def command(self, p):
        return Command(CommandType.ASSIGN, identifier=p[0], expression=p[2])
    
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

    
    
