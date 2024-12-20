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
            self.decs_to_table(declarations)
            
        # Handling initial commands
        main_comms = self.get_main_commands()
        main_comms_list = self.comms_to_list(main_comms)
        
        for x in main_comms_list:
            self.handle_command(x)

        code_string = self.code_list_to_string()
        code_string.append("HALT")
        return code_string
            
        
    
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
    
    
    def decs_to_table(self, decs):
        """ Writes declarations to the sumbl table """
        
        if decs is None:
            print("\nError: declarations type is 'None'")
            return
        
        tag = decs[0]
            
        if tag == 'decs_PID':
            self.table.add_symbol(decs[1])

        elif tag == 'decs_ARRAY':
            self.table.add_array(decs[1], decs[2], decs[3])
        
        elif tag == 'decs_REC_PID':
            self.decs_to_table(decs[1])
            self.table.add_symbol(decs[2])

        elif tag == 'decs_REC_ARRAY':
            self.decs_to_table(decs[1])
            self.table.add_array(decs[2], decs[3], decs[4])
            
        else:
            print("\nError: Wrong tag")
            return
        
    
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
        
        c_list = []
        identifier = command[1]
        tag = identifier[0]
        
        # identifier can be a name TODO: or table name 
        if tag == 'id_PID':
            name = identifier[1]
            mem_idx = self.table.get_symbol(name)['position']
            
            c_list.append(Code('# READ'))
            c_list.append(Code('GET', mem_idx))
            
        elif tag == 'id_ARRAY_NUM':
            arr = identifier[1]
            arr_pos = self.table.get_symbol(arr)['position']
            arr_offset = self.table.get_symbol(name)['start_idx']
            idx_value = identifier[2]
            position = int(arr_pos) + int(idx_value) - int(arr_offset)
            
            c_list.append(Code('# READ'))
            c_list.append(Code('GET', position))
            
        elif tag == 'id_ARRAY_PID': # TODO: not tested!!!
            arr = identifier[1]
            idx = identifier[2]
            arr_pos = self.table.get_symbol(arr)['position']
            idx_pos = self.table.get_symbol(idx)['position']
            arr_offset = self.table.get_symbol(arr)['start_idx']
            
            c_list.append(Code('# READ'))
            c_list.append(Code('SET', arr_offset))
            c_list.append(Code('STORE', 1))
            c_list.append(Code('SET', arr_pos))
            c_list.append(Code('ADD', idx_pos))
            c_list.append(Code('SUB', 1))
            c_list.append(Code('STORE', 1))
            c_list.append(Code('GET', 0))
            c_list.append(Code('STOREI', 1))
        
        if self.debug:
            print(f"gc_comm_READ(): ")
            self.print_code_list(c_list)
        return c_list
        

    def gc_comm_WRITE(self, command):
        """ Generates code for command WRITE """
        c_list = []
        value = command[1]
        val_tag = value[0]
        
        # in this case value is a number
        if val_tag == 'val_NUM':
            # TODO:
            number = value[1]
            
            # 'PUT' prints a value from memory,
            # so I place our value in memory slot '1'
            # and then print it
            # c_list.append(Code('STORE'))
            
        # in this case value is a name of a variable
        elif val_tag == 'val_ID':
            identifier = value[1]
            id_tag = identifier[0]
            
            if id_tag == 'id_PID':
                # TODO: array T case
                name = identifier[1]
                mem_idx = self.table.get_symbol(name)['position']
                
                c_list.append(Code('# WRITE'))
                c_list.append(Code('PUT', mem_idx))
                
            elif id_tag == 'id_ARRAY_NUM':
                arr = identifier[1]
                idx_value = identifier[2]
                arr_pos = self.table.get_symbol(name)['position']
                arr_offset = self.table.get_symbol(name)['start_idx']
                
                position = int(arr_pos) + int(idx_value) - int(arr_offset)
                
                c_list.append(Code('# WRITE'))
                c_list.append(Code('PUT', mem_idx))
                
            elif id_tag == 'id_ARRAY_PID':
                arr = identifier[1]
                idx = identifier[2]
                arr_pos = self.table.get_symbol(arr)['position']
                idx_pos = self.table.get_symbol(idx)['position']
                arr_offset = self.table.get_symbol(arr)['start_idx']
                
                c_list.append(Code('# WRITE'))
                c_list.append(Code('SET', arr_offset))
                c_list.append(Code('STORE', 1))
                c_list.append(Code('SET', arr_pos))
                c_list.append(Code('ADD', idx_pos))
                c_list.append(Code('SUB', 1))
                c_list.append(Code('LOADI', 0))
                c_list.append(Code('PUT', 0))
                
        if self.debug:
            print(f"gc_comm_WRITE(): ")
            self.print_code_list(c_list)
            
        return c_list




if __name__ == '__main__':
    lexer = MyLexer()
    parser = MyParser()
    
    input = 'examples/my0.imp'
    output = 'output/my-out.mr'


    with open(input, 'r') as file:
        data = file.read()
        
    tokens = lexer.tokenize(data)
    
    parsed = parser.parse(tokens)
    
    gen = CodeGenerator(parsed, True)
    
    gen.generate_code()
    
    gen.table.display()
    
        
    # code = gen.generate_code()

    # gen.table.add_array("arr", 0, 10)
    # gen.table.add_symbol("x")
    # gen.table.display()
    
#     # print(gen.code_list_to_string())
#     code = gen.generate_code()

#     with open(output, 'w') as file:
#         for line in code:
#             file.write(line + '\n')