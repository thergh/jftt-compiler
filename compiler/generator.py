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
            print("CodeGenerator.procedures: ", self.procedures)
            print("CodeGenerator.main: ", self.main)
        
    
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
        
        # if self.debug:
        #     print("main comms: ", main_comms_list)
            
        for x in main_comms_list:
            self.handle_command(x)

        
            
        
    
    def get_declarations(self):
        """ Gets declarations from program
        and returns them in a recursive form """
            
        if self.main[0] != 'mn_LONG': # program has no declarations
            print("Program has no declarations")
            return None
        
        declarations = self.main[1]   
         
        if self.debug:
            print("get_declarations(): ", declarations)
            
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
        decs_list: list = []
            
        if tag == 'decs_PID':
            decs_list.append(decs[1])
        
        elif tag == 'decs_REC_PID':
            decs_list = self.decs_to_list(decs[1])
            decs_list.append(decs[2])
            
        
        else:
            print("\nError: Wrong tag")
            return
        
        return decs_list
            
        
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
            print("get_main_commands(): ", commands)
        
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
            
            
    def handle_command(self, command):
        tag = command[0]
        
        # TODO: add other commands
        if tag == 'comm_WRITE':
            self.code_list.extend(self.gc_comm_WRITE(command))
            
        elif tag == 'comm_READ':
            self.code_list.extend(self.gc_comm_READ(command))
            
        else:
            print(f"Error: wrong command tag: {tag}")
            return
            
            
    def print_code_list(self, code_list):
        for x in code_list:
            print(f"{x.name, x.value}")
            
            
    def code_list_to_string(self):
        string_list = []
        for x in self.code_list:
            string_list.append(x.to_string())
            
        return string_list
            
    ################ VM code generation ################
    
    def gc_comm_READ(self, command):
        """ Generates code for command READ """
        
        identifier = command[1]
        
        # identifier can be a name TODO: or table name 
        if identifier[0] == 'id_PID':
            name = identifier[1]
            
        mem_idx = self.table.get_symbol(name)['idx']
        
        c: Code = Code('GET', mem_idx)
        
        if self.debug:
            print(f"gc_comm_READ(): ", end='')
            self.print_code_list([c])
                        
        return [c]
        

    def gc_comm_WRITE(self, command):
        """ Generates code for command WRITE """
        c_list = []
        
        value = command[1]
        
        # in this case value is a number
        if value[0] == 'val_NUM':
            # TODO:
            number = value[1]
            
            # 'PUT' prints a value from memory,
            # so I place our value in memory slot '1'
            # and then pint it
            # c_list.append(Code('STORE'))
            
        # in this case value is a name of a variable
        elif value[0] == 'val_ID':
            identifier = value[1]
            
            if identifier[0] == 'id_PID':
                # TODO: array T case
                name = identifier[1]
                mem_idx = self.table.get_symbol(name)['idx']
                # mem_idx = self.table[name]['idx']
                
                c_list.append(Code('PUT', mem_idx))
                
        if self.debug:
            print(f"gc_comm_WRITE(): ", end='')
            self.print_code_list(c_list)
            
        return c_list




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
    # print(gen.code_list_to_string())
    code_string = gen.code_list_to_string()
    print(code_string)