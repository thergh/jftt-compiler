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
    REC = 'REC'
    SINGLE = 'SINGLE'    
        
        
class Commands(ASTNode):
    def __init__(self, commands_type,  **kwargs):
        super().__init__()
        
        if not isinstance(commands_type, CommandsType):
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
    REC_PID = 'REC_PID'
    REC_TABLE = 'REC_TABLE'
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
    REC_PID = 'PLURATL_PID'
    REC_T = 'REC_T'
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
    REC = 'REC'
    SINGLE = 'SINGLE'        
        
        
class Args(ASTNode):
    def __init__(self, args_type, **kwargs):
        super().__init__()
        
        if not isinstance(args_type, ArgsType):
            raise ValueError("Invalid type")
        
        self.args_type = args_type
        self.attributes = kwargs
        
    
class ExpressionType(Enum):
    VALUE = 'VALUE'    
    OPER = 'OPER'

class Expression(ASTNode):
    def __init__(self, expression_type, **kwargs):
        super().__init__()

        if not isinstance(expression_type, ExpressionType):
            raise ValueError("Invalid type")

        self.expression_type = expression_type
        self.attributes = kwargs
        
        
class Condition(ASTNode):
    def __init__(self, value1=None, value2=None, condition=None):
        super().__init__()
        self.value1 = value1
        self.value2 = value2
        self.condition = condition
        
        
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
        return Commands(CommandsType.REC, commands=p[0], command=p[1])
    
    @_('command')
    def commands(self, p):
        return Commands(CommandsType.SINGLE, command=p[0])
    
    
    @_('identifier ASSIGN expression ";"')
    def command(self, p):
        return Command(CommandType.ASSIGN, identifier=p[0], expression=p[2])
    
    @_('IF condition THEN commands ELSE commands ENDIF')
    def command(self, p):
        return Command(CommandType.IF_ELSE, condition=p[1], commands1=p[3], commands2=p[5])
    
    @_('IF condition THEN commands ENDIF')
    def command(self, p):
        return Command(CommandType.IF, condition=p[1], commands=p[3])
    
    @_('WHILE condition DO commands ENDWHILE')
    def command(self, p):
        return Command(CommandType.WHILE, condition=p[1], commands=p[3])
    
    @_('REPEAT commands UNTIL condition ";"')
    def command(self, p):
        return Command(CommandType.REPEAT, commands=p[1], condition=p[3])
    
    @_('FOR PID FROM value TO value DO commands ENDFOR')
    def command(self, p):
        return Command(CommandType.FOR, PID=p.PID, value1=p[3], value2=p[5], commands=p[7])
    
    @_('FOR PID FROM value DOWNTO value DO commands ENDFOR')
    def command(self, p):
        return Command(CommandType.FOR_DOWN, PID=p.PID, value1=p[3], value2=p[5], commands=p[7])
    
    @_('proc_call ";"')
    def command(self, p):
        return Command(CommandType.PROC_CALL, proc_call=p[0])
    
    @_('READ identifier ";"')
    def command(self, p):
        return Command(CommandType.READ, idenditief=p[1])
    
    @_('WRITE value ";"')
    def command(self, p):
        return Command(CommandType.WRITE, value=p[1])
    
    
    @_('PID "(" args_decl ")"')
    def proc_head(self, p):
        return ProcHead(p.PID, p[2])
    
    
    @_('PID "(" args ")"')
    def proc_call(self, p):
        return ProcCall(p.PID, p[2])
    
    
    @_('declarations "," PID')
    def declarations(self, p):
        return Declarations(DeclarationsType.REC_PID, declarations=p[0], PID=p.PID)
    
    @_('declarations "," PID "[" NUM ":" NUM "]"')
    def declarations(self, p):
        return Declarations(DeclarationsType.REC_TABLE, declarations=p[0], PID=p.PID, num1=p[4], num2=p[6])
    
    @_('PID')
    def declarations(self, p):
        return Declarations(DeclarationsType.SINGLE_PID, PID=p.PID)
    
    @_('"T" PID')
    def declarations(self, p):
        return Declarations(DeclarationsType.SINGLE_TABLE, PID=p.PID)
        
    
    @_('args_decl "," PID')
    def args_decl(self, p):
        return ArgsDecl(ArgsDeclType.REC_PID, args_decl=p[0], PID=p.PID)
    
    @_('args_decl "," "T" PID')
    def args_decl(self, p):
        return ArgsDecl(ArgsDeclType.REC_T, args_decl=p[0], PID=p.PID)
            
    @_('PID')
    def args_decl(self, p):
        return ArgsDecl(ArgsDeclType.SINGLE_PID, PID=p.PID)
    
    @_('"T" PID')
    def args_decl(self, p):
        return ArgsDecl(ArgsDeclType.SINGLE_T, PID=p.PID)
    
    
    @_('args "," PID')
    def args(self, p):
        return Args(ArgsType.REC, args=p[0], PID=p.PID)
    
    @_('PID')
    def args(self, p):
        return Args(ArgsType.SINGLE, PID=p.PID)
    
    
    @_('value')
    def expression(self, p):
        return Expression(ExpressionType.VALUE, value=p[0])

    @_('value "+" value',
       'value "-" value',
       'value "*" value',
       'value "/" value',
       'value "%" value',)
    def expression(self, p):
        return Expression(ExpressionType.OPER, value1=p[0], value2=p[2], operator=p[1])
    
    
    @_('value "=" value',
       'value NE value',
       'value ">" value',
       'value "<" value',
       'value GE value',
       'value LE value',
       )
    def condition(self, p):
        return Condition(p[0], p[2], p[1])
    
    
    @_('NUM')
    def value(self, p):
        return Value(ValueType.NUM, value=p[0])
        
    @_('identifier')
    def value(self, p):
        return Value(ValueType.ID, identifier=p[0])
    
    
    @_('PID "[" PID "]"')
    def identifier(self, p):
        return Identifier(IdentifierType.PID_TABLE, PID1=p[0], PID2=p[2])
        
    @_('PID "[" NUM "]"')  
    def identifier(self, p):
        return Identifier(IdentifierType.NUM_TABLE, PID=p.PID, NUM=p.NUM)
        
    @_('PID')  
    def identifier(self, p):
        return Identifier(IdentifierType.PID, PID=p.PID)
    
    
if __name__ == '__main__':
    lexer = MyLexer()
    parser = MyParser()

    with open('examples/program3.imp', 'r') as file:
        data = file.read()
        
    tokens = lexer.tokenize(data)
    
    result: ProgramAll = parser.parse(tokens)
    
    print(result)
    print(result)

    
    
