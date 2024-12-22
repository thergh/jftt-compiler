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
        
        # for x in main_comms_list:
        #     self.gc_command(x)
        self.code_list.extend(self.gc_command_list(main_comms_list))

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
    
            
    def print_code_list(self, code_list):
        for x in code_list:
            print(f"{x.name, x.value}")
            
            
    def code_list_to_string(self):
        string_list = []
        for x in self.code_list:
            string_list.append(x.to_string())
            
        return string_list
    

    ###################### code generation ######################
    
    
    def gc_command_list(self, comm_list: list):
        """ Generates code for a command list """
        
        c_list = []
        
        for x in comm_list:
            c_list.extend(self.gc_command(x))
            
        return c_list
    
            
    def gc_command(self, command):
        """ Generates code for a command """
        
        tag = command[0]
        c_list = []
        
        # TODO: add other commands
        if tag == 'comm_WRITE':
            c_list.extend(self.gc_comm_WRITE(command))
            
        elif tag == 'comm_READ':
            c_list.extend(self.gc_comm_READ(command))
            
        elif tag == 'comm_ASSIGN':
            c_list.extend(self.gc_comm_ASSIGN(command))

        else:
            print(f"Error: wrong command tag: {tag}")
            return
            
        return c_list
    
    
    def handle_condition(self, condition):
        cond_tag = condition[2]
        
        if cond_tag == "=":
            return self.cond_EQ(condition)
        
        elif cond_tag == "NE":
            return self.cond_NE(condition)
        
        elif cond_tag == ">":
            return self.cond_G(condition)
        
        elif cond_tag == "<":
            return self.cond_L(condition)
        
        elif cond_tag == "GE":
            return self.cond_GE(condition)
        
        elif cond_tag == "LE":
            return self.cond_LE(condition)

        else:
            print(f"Error: Wrong tag: {cond_tag}")
            return
    
    
    def cond_EQ(self, condition):
        """ Puts evaluation of condition '=' in accumulator. 
        True:   1
        False:  0
        Side effects in registers: 10 """
            
        c_list = []
        value1 = condition[1]
        value2 = condition[3]
        
        c_list.extend(self.value_to_acc(value1))
        c_list.append(Code('STORE', 10))
        c_list.extend(self.value_to_acc(value2))
        c_list.append(Code('SUB', 10))
        c_list.append(Code('JZERO', 3)) # if True, acc := 1
        c_list.append(Code('SET', 0))   # if False, acc := 0
        c_list.append(Code('JUMP', 2))  
        c_list.append(Code('SET', 1))
        
        return c_list
    
    
    def cond_NE(self, condition):
        """ Puts evaluation of condition '!=' in accumulator. 
        True:   1
        False:  0
        Side effects in registers: 10 """
            
        c_list = []
        value1 = condition[1]
        value2 = condition[3]
        
        c_list.extend(self.value_to_acc(value1))
        c_list.append(Code('STORE', 10))
        c_list.extend(self.value_to_acc(value2))
        c_list.append(Code('SUB', 10))
        c_list.append(Code('JZERO', 3))
        c_list.append(Code('SET', 1))
        c_list.append(Code('JUMP', 2))  
        c_list.append(Code('SET', 0))
        
        return c_list
    
    
    def cond_G(self, condition):
        """ Puts evaluation of condition '>' in accumulator. 
        True:   1
        False:  0
        Side effects in registers: 10 """
            
        c_list = []
        value1 = condition[1]
        value2 = condition[3]
        
        c_list.extend(self.value_to_acc(value1))
        c_list.append(Code('STORE', 10))
        c_list.extend(self.value_to_acc(value2))
        c_list.append(Code('SUB', 10))
        c_list.append(Code('JPOS', 3))
        c_list.append(Code('SET', 0))
        c_list.append(Code('JUMP', 2))  
        c_list.append(Code('SET', 1))
        
        return c_list
    
    
    def cond_L(self, condition):
        """ Puts evaluation of condition '<' in accumulator. 
        True:   1
        False:  0
        Side effects in registers: 10 """
            
        c_list = []
        value1 = condition[1]
        value2 = condition[3]
        
        c_list.extend(self.value_to_acc(value1))
        c_list.append(Code('STORE', 10))
        c_list.extend(self.value_to_acc(value2))
        c_list.append(Code('SUB', 10))
        c_list.append(Code('JNEG', 3))
        c_list.append(Code('SET', 0))
        c_list.append(Code('JUMP', 2))  
        c_list.append(Code('SET', 1))
        
        return c_list
    
    
    def cond_GE(self, condition):
        """ Puts evaluation of condition '>=' in accumulator. 
        True:   1
        False:  0
        Side effects in registers: 10 """
            
        c_list = []
        value1 = condition[1]
        value2 = condition[3]
        
        c_list.extend(self.value_to_acc(value1))
        c_list.append(Code('STORE', 10))
        c_list.extend(self.value_to_acc(value2))
        c_list.append(Code('SUB', 10))
        c_list.append(Code('JNEG', 3))
        c_list.append(Code('SET', 1))
        c_list.append(Code('JUMP', 2))  
        c_list.append(Code('SET', 0))
        
        return c_list
    
    
    def cond_LE(self, condition):
        """ Puts evaluation of condition '<=' in accumulator. 
        True:   1
        False:  0
        Side effects in registers: 10 """
            
        c_list = []
        value1 = condition[1]
        value2 = condition[3]
        
        c_list.extend(self.value_to_acc(value1))
        c_list.append(Code('STORE', 10))
        c_list.extend(self.value_to_acc(value2))
        c_list.append(Code('SUB', 10))
        c_list.append(Code('JPOS', 3))
        c_list.append(Code('SET', 1))
        c_list.append(Code('JUMP', 2))  
        c_list.append(Code('SET', 0))
        
        return c_list
    
    
    def value_to_acc(self, value):
        """ Generates code that puts the number held
        by 'value' into the accumulator """
    
        c_list = []
        
        value_tag = value[0]
        
        if value_tag == 'val_NUM':
            number = value[1]
            c_list.append(Code('SET', number))
        
        elif value_tag == 'val_ID':
            identifier = value[1]
            c_list.extend(self.id_pos_to_acc(identifier)) # puts id_pos into acc
            c_list.append(Code('LOADI', 0)) # load value of id to reg0
        
        return c_list
    
    
    def id_pos_to_acc(self, identifier):
        """ Generates code that puts position
        of id into accumulator. """

        id_tag = identifier[0]
        c_list = []
        
        if id_tag == 'id_PID':
            id = identifier[1]
            id_pos = self.table.get_symbol(id)['position']
            c_list.append(Code('SET', id_pos))
            
        elif id_tag == 'id_ARRAY_NUM':
            arr = identifier[1]
            number = identifier[2]
            arr_pos = self.table.get_symbol(arr)['position']
            arr_offset = self.table.get_symbol(arr)['start_idx']
            position = int(arr_pos) + int(number) - int(arr_offset)
            c_list.append(Code('SET', position))
            
        elif id_tag == 'id_ARRAY_PID':
            arr = identifier[1]
            idx = identifier[2]
            arr_pos = self.table.get_symbol(arr)['position']
            arr_offset = self.table.get_symbol(arr)['start_idx']
            idx_pos = self.table.get_symbol(idx)['position']
            c_list.append(Code('LOADI', idx_pos)) # loads idx value to acc
            c_list.append(Code('ADD', arr_pos))
            c_list.append(Code('SUB', arr_offset)) # now id position is in acc
            
        return c_list
    
    
    def gc_comm_IF(self, command):
        """ Generates code for command IF """
        # TODO
        condition = command[1]
        commands = command[2]
        comm_list = self.comms_to_list()
        
    
    def gc_comm_ASSIGN(self, command):
        """ Generates code for command ASSIGN """
        # TODO:
        # for now only for single numbers,
        # not complicated expressions
        
        c_list = []
        identifier = command[1]
        expression = command[2]
        
        if expression[0] == 'expr_VAL':
            value = expression[1]
            
        else:
            print("Error: Complicated expressions not yet implemented :(")
            return

        
        c_list.extend(self.id_pos_to_acc(identifier)) # reg0: id1_pos
        c_list.append(Code('STORE', 1)) # store id1_pos in reg1
        
        value_tag = value[0]
        
        if value_tag == 'val_NUM':
            num_val = value[1]
            c_list.append(Code('SET', num_val)) # put num_val in reg0
            c_list.append(Code('STOREI', 1)) # set velue on position
            
        elif value_tag == 'val_ID':
            identifier2 = value[1]
            c_list.extend(self.id_pos_to_acc(identifier2)) # reg0: id2_pos
            c_list.append(Code('LOADI', 0)) # load value of id2_pos to reg0
            c_list.append(Code('STOREI', 1)) # set velue on position
            
        return c_list    
    
    
    def gc_comm_READ(self, command):
        """ Generates code for command READ """
        
        c_list = []
        identifier = command[1]
        tag = identifier[0]
        
        c_list.extend(self.id_pos_to_acc(identifier))
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
        
        c_list.extend(self.value_to_acc(value))
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
    
    
    
    # gen.table.display()

    val1 = ('val_NUM', 10)
    val2 = ('val_NUM', -10)
    cond = ('cond', val1, "=", val2)
    gen.code_list.extend(gen.cond_eq(cond))
    
    
    code = gen.generate_code()
    for c in code:
        print(c)
    
    
    # code = gen.generate_code()

    # gen.table.add_array("arr", 0, 10)
    # gen.table.add_symbol("x")
    # gen.table.display()
    
#     # print(gen.code_list_to_string())
#     code = gen.generate_code()

#     with open(output, 'w') as file:
#         for line in code:
#             file.write(line + '\n')