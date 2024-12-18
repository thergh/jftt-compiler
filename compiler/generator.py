from parser import MyParser
from lexer import MyLexer
from table import SymbolTable
  
  
  
class Code:
    """ Represents vm code """
    
    def __init__(self, name, value=None):
        self.name = name
        self.value = value
        
    def to_string(self):
        """ Changes format of a code
        from tuple to string """
        
        if self.value is None:
            return f"{self.name}"
        
        else:
            return f"{self.name} {self.value}"    

  
class CodeGenerator:
    def __init__(self, program, debug=False):
        self.program = program
        self.debug = debug
        self.procedures = program[1]
        self.main = program[2]
        self.table: SymbolTable = SymbolTable()
        self.code_list = []
        
        if self.debug:
            print("\nprocedures: ", self.procedures)
            print("\nmain: ", self.main)
        
    
    def generate_code(self):

        # Handling initial declarations
        declarations = self.get_declarations()
        
        if declarations is not None:
            decs_list = self.decs_to_list(declarations)
        else:
            decs_list = None
            
        for x in decs_list:
            self.table.add_symbol(x)
            
        # Handling initial commands
        main_comms = self.get_main_commands()
        main_comms_list = self.comms_to_list(main_comms)
        
        if self.debug:
            print("main comms: ", main_comms_list)

            
        
    
    def get_declarations(self):
        """ Gets declarations from program
        and returns them in a recursive form """
        
        # if self.debug:
        #     print("\nmain[0]: ", self.main[0])
            
        if self.main[0] != 'mn_LONG': # program has no declarations
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
            
        if tag == 'decs_PID':
            decs_list = []
            decs_list.append(decs[1])
            return decs_list
        
        elif tag == 'decs_REC_PID':
            decs_list: list = self.decs_to_list(decs[1])
            decs_list.append(decs[2])
            return decs_list
        
        else:
            print("\nError: Wrong tag")
            return
            
        
    # def group_commands(self, commands):
    #     comm_list = []
    #     comm_list.append(commands[1]) 
    #     if commands[0] == 'comms_SINGLE':        
    #         return comm_list
        
    #     else:
    #         comm_list.append(self.group_commands(commands[1]))
    #         return comm_list
    
    
    def get_main_commands(self):
        """ Gets main commands from the program
        and returns them in a recursive form """
        
        main_tag = self.main[0]
        
        if main_tag == 'mn_SHORT': # program has no declarations
            commands = self.main[1]
        elif main_tag == 'mn_LONG':
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
        
        if comms is None:
            print("\nError: comms' type is 'None'")
            return
        
        tag = comms[0]
        
        if tag == 'comms_SINGLE':
            comms_list = []
            comms_list.append(comms[1])
            return comms_list
        
        elif tag == 'comms_REC':
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
            
            
            
            
    ################ VM code generation ################
    
    def gc_comm_READ(self, identifier):
        """ Generates code for command READ """
        
        # identifier can be a name TODO: or table name 
        if identifier[0] == 'id_PID':
            name = identifier[1]
            
        mem_idx = self.table[name]['idx']
        c: Code = Code('GET', mem_idx)
        return [c]
        

    def gc_comm_WRITE(self, value):
        """ Generates code for command WRITE """
        
        # # value can be a number or an identifier
        # if value[0] == 'val_NUM':
        #     return
        
        # mem_idx = self.table[val]['idx']
        # c: Code = Code('PUT', mem_idx)
        # return [c]
        return



if __name__ == '__main__':
    lexer = MyLexer()
    parser = MyParser()

    # with open('examples/program0.imp', 'r') as file:
    #     data = file.read()
        
    with open('examples/my-print.imp', 'r') as file:
        data = file.read()
        
    tokens = lexer.tokenize(data)
    
    parsed = parser.parse(tokens)
    
    gen = CodeGenerator(parsed, True)
    gen.generate_code()
    print(gen.code_list)