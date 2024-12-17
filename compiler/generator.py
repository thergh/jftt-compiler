from parser import MyParser
from lexer import MyLexer
from table import SymbolTable
  
  
  
class CodeGenerator:
    def __init__(self, program, debug=False):
        self.program = program
        self.debug = debug
        self.procedures = program[1]
        self.main = program[2]
        self.table: SymbolTable = SymbolTable()
        
        if self.debug:
            print("\nprocedures: ", self.procedures)
            print("\nmain: ", self.main)
        
    
    def generate_code(self):

        declarations = self.get_declarations()
        
        if declarations is not None:
            decs_list = self.decs_to_list(declarations)
        else:
            decs_list = None
        
    
    def get_declarations(self):
        """ Gets declarations from program
        and returns them in a recursive form """
        
        # if self.debug:
        #     print("\nmain[0]: ", self.main[0])
            
        if self.main[0] != 'mn=LONG': # program has no declarations
            print("Program has no declarations")
            return None
        
        declarations = self.main[1]   
         
        if self.debug:
            print("\ndeclarations: ", declarations)
            
        return declarations
    
    
    def decs_to_list(self, decs):
        """ Changes declarations from
        recursive form to a list 
        # TODO: implement arrays: 'T_PID', 'REC_T'
        """
        
        if decs is None:
            print("\nError: declarations type is 'None'")
            return
        
        tag = decs[0]
        # if self.debug:
        #     print("\ndecs tag: ", tag)
            
        if tag == 'decs=PID':
            decs_list = []
            decs_list.append(decs[1])
            return decs_list
        
        elif tag == 'decs=REC_PID':
            decs_list: list = self.decs_to_list(decs[1])
            decs_list.append(decs[2])
            return decs_list
        
        else:
            print("\nError: Wrong tag")
            return
            
        
    # def group_commands(self, commands):
    #     comm_list = []
    #     comm_list.append(commands[1]) 
    #     if commands[0] == 'comms=SINGLE':        
    #         return comm_list
        
    #     else:
    #         comm_list.append(self.group_commands(commands[1]))
    #         return comm_list
    
    
    def get_main_commands(self):
        """ Gets main commands from the program
        and returns them in a recursive form """
        
        main_tag = self.main[0]
        
        if main_tag == 'mn=SHORT': # program has no declarations
            commands = self.main[1]
        elif main_tag == 'mn=LONG':
            commands = self.main[2]
        else:
            print("\nError: Wrong tag: ", main_tag)
            return
        
        if self.debug:
            print("\nmain commands: ", commands)
        
        return commands


    def comms_to_list(self, comms):
        """ Changes commands from
        recursive form to a list """
        
        if decs is None:
            print("\nError: comms' type is 'None'")
            return
        
        tag = comms[0]
        
        if tag == 'comms=SINGLE':
            comms_list = []
            comms_list.append(comms[1])
            return comms_list
        
        elif tag == 'comms=REC':
            comms_list: list = self.comms_to_list(comms[1])
            comms_list.append(comms[2])
            return comms_list
            
        else: 
            print("\nError: Wrong tag: ", tag)
            return
        
        
    def insert_decs_list(self, decs_list):
        """ 
        # TODO: HANDLE ARRAYS T
        """
        for x in decs_list:
            self.table.add_symbol(x)


if __name__ == '__main__':
    lexer = MyLexer()
    parser = MyParser()

    # with open('examples/program0.imp', 'r') as file:
    #     data = file.read()
        
    with open('examples/my0.imp', 'r') as file:
        data = file.read()
        
    tokens = lexer.tokenize(data)
    
    parsed = parser.parse(tokens)
    
    gen = CodeGenerator(parsed, True)
    decs = gen.get_declarations()
    decs_list = gen.decs_to_list(decs)


    gen.insert_decs_list(decs_list)
    gen.table.display()