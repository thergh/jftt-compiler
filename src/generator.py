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
        self.scope = ''
        self.for_counter = 0
        self.proc_offset = 0
        
        # if self.debug:
        #     print("CodeGenerator.procedures: ", self.procedures)
        #     print("CodeGenerator.main: ", self.main)
        
    
    def generate_code(self):
        """ returns: String of machine code instructions
        compiled from the input langage. """
        
        # handle procedures     
        procs_list = self.procs_to_list(self.procedures)
        # self.code_list.extend(procs_list)
        
        for p in procs_list:
            self.code_list.extend(self.gc_proc(p))
        
        # Handling initial declarations
        declarations = self.get_declarations()
        
        if declarations is not None:
            self.decs_to_table(declarations)
            
        # Handling initial commands
        main_comms = self.get_main_commands()
        main_comms_list = self.comms_to_list(main_comms)
        
        for x in main_comms_list:
            self.code_list.extend(self.gc_command(x))

        code_string = self.code_list_to_string()
        code_string.append("HALT")
        
        
        if self.debug:
            print("SYMBOL TABLE:\n")
            self.table.display()
            print()
            print("CODE:\n")
            for c in code_string:
                print(c)
            
        return code_string
            
        
    
    def get_declarations(self):
        """ returns: Variable declarations from main program
        in a recursive form. """
            
        if self.main[0] != 'mn_LONG': # program has no declarations
            print("Program has no declarations")
            return None
        
        declarations = self.main[1]   
         
        # if self.debug:
        #     print("get_declarations(): ", declarations)
            
        return declarations
    
    
    def decs_to_table(self, decs):
        """ Writes declarations to the symbol table """
        
        if decs is None:
            print("\nError: declarations type is 'None'")
            return
        
        tag = decs[0]
            
        if tag == 'decs_PID':
            self.table.add_symbol(self.scope + decs[1])

        elif tag == 'decs_ARRAY':
            self.table.add_array(self.scope + decs[1], decs[2], decs[3])
        
        elif tag == 'decs_REC_PID':
            self.decs_to_table(decs[1])
            self.table.add_symbol(self.scope + decs[2])

        elif tag == 'decs_REC_ARRAY':
            self.decs_to_table(decs[1])
            self.table.add_array(self.scope + decs[2], decs[3], decs[4])
            
        else:
            print("\nError: Wrong tag")
            return
        
    
    def get_main_commands(self):
        """ returns: Commands from main program
        in a recursive form. """
        
        main_tag = self.main[0]
        
        if main_tag == 'mn_SHORT': # program has no declarations
            commands = self.main[1]
        elif main_tag == 'mn_LONG':
            commands = self.main[2]
        else:
            print("\nError: Wrong tag: ", main_tag)
            return
        
        # if self.debug:
        #     print("get_main_commands(): ", commands)
        
        return commands


    def comms_to_list(self, comms):
        """ Changes main commands from
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
        """ Prints machine code from object form. """
        for x in code_list:
            print(f"{x.name, x.value}")
            
            
    def code_list_to_string(self):
        """ returns: Machine codes in string form. """
        string_list = []
        for x in self.code_list:
            string_list.append(x.to_string())
            
        return string_list
    

    ###################### code generation ######################
    
    
    def gc_command_list(self, comm_list: list):
        """ returns: Code for a command list """
        
        c_list = []
        
        for x in comm_list:
            c_list.extend(self.gc_command(x))
            
        return c_list
    
            
    def gc_command(self, command):
        """ returns: Code for a command. """
        
        tag = command[0]
        c_list = []
        
        # TODO: add other commands
        if tag == 'comm_WRITE':
            c_list.extend(self.gc_comm_WRITE(command))
            
        elif tag == 'comm_READ':
            c_list.extend(self.gc_comm_READ(command))
            
        elif tag == 'comm_ASSIGN':
            c_list.extend(self.gc_comm_ASSIGN(command))
            
        elif tag == 'comm_IF':
            c_list.extend(self.gc_comm_IF(command))
            
        elif tag == 'comm_IF_ELSE':
            c_list.extend(self.gc_comm_IF_ELSE(command))
            
        elif tag == 'comm_WHILE':
            c_list.extend(self.gc_comm_WHILE(command))
            
        elif tag == 'comm_REPEAT':
            c_list.extend(self.gc_comm_REPEAT(command))
            
        elif tag == 'comm_CALL':
            c_list.extend(self.gc_comm_CALL(command))
            
        elif tag == 'comm_FOR':
            c_list.extend(self.gc_comm_FOR(command))
            
        elif tag == 'comm_FOR_DOWN':
            c_list.extend(self.gc_comm_FOR_DOWN(command))

        else:
            print(f"Error: wrong command tag: {tag}")
            return
            
        return c_list
    
    
    def gc_comm_READ(self, command):
        """ returns: Code for command READ """
        
        c_list = []
        identifier = command[1]
        tag = identifier[0]
        
        c_list.extend(self.id_pos_to_acc(identifier))
        c_list.append(Code('STORE', 1))
        c_list.append(Code('GET', 0))
        c_list.append(Code('STOREI', 1))
        
        # if self.debug:
        #     print(f"gc_comm_READ(): ")
        #     self.print_code_list(c_list)
        return c_list
        

    def gc_comm_WRITE(self, command):
        """ returns: Code for command WRITE """
        c_list = []
        value = command[1]
        
        c_list.extend(self.value_to_acc(value))
        c_list.append(Code('PUT', 0))
                
        # if self.debug:
        #     print(f"gc_comm_WRITE(): ")
        #     self.print_code_list(c_list)
            
        return c_list
    
    
    def gc_comm_ASSIGN(self, command):
        """ returns: Code for command ASSIGN """
 
        c_list = []
        identifier = command[1]
        expression = command[2]
    
        c_list.extend(self.id_pos_to_acc(identifier)) # reg0: id1_pos
        c_list.append(Code('STORE', 1)) # store id1_pos in reg1
        
        c_list.extend(self.calculate_expression(expression)) # calculate value of expression and put into acc
        c_list.append(Code('STOREI', 1)) # set velue on position

        return c_list    
    
    
    def id_pos_to_acc(self, identifier):
        """ returns: Code that puts symbol table position
        of PID into accumulator. """
        # TODO: reference arrays
        
        id_tag = identifier[0]
        c_list = []
        
        if id_tag == 'id_PID':
            id = identifier[1]
            # check if id is a reference
            if(self.table.get_symbol(self.scope + id)['is_reference']):
                ref_pos = self.table.get_symbol(self.scope + id)['position']
                
                # czyli mam teraz pozycję referencji. chcę dostać pozycję wartości
                # pozycja wartości jest wartością referencji
                # czyli chcę dostać wartość tego, co jest na pozycji referencji
                
                c_list.append(Code('LOAD', ref_pos))
    
            else: # normal case
                id_pos = self.table.get_symbol(self.scope + id)['position']
                c_list.append(Code('SET', id_pos))
            
        elif id_tag == 'id_ARRAY_NUM':
            arr = identifier[1]
            number = identifier[2]
            arr_pos = self.table.get_symbol(self.scope + arr)['position']
            arr_offset = self.table.get_symbol(self.scope + arr)['start_idx']
            position = int(arr_pos) + int(number) - int(arr_offset)
            c_list.append(Code('SET', position))
            
        elif id_tag == 'id_ARRAY_PID':
            arr = identifier[1]
            idx = identifier[2]
            arr_pos = self.table.get_symbol(self.scope + arr)['position']
            arr_offset = self.table.get_symbol(self.scope + arr)['start_idx']
            idx_pos = self.table.get_symbol(self.scope + idx)['position']
            c_list.append(Code('LOADI', idx_pos)) # loads idx value to acc
            c_list.append(Code('ADD', arr_pos))
            c_list.append(Code('SUB', arr_offset)) # now id position is in acc
            
        else:
            print(f"Error: wrong tag: {id_tag}")
            return
            
        return c_list
    
    
    def value_to_acc(self, value):
        """ returns: Code that puts the number held
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

    
    def cond_EQ(self, condition):
        # OK
        """ returns: Code that puts evaluation
        of condition '=' in the accumulator.
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
        # OK
        """ returns: Code that puts evaluation
        of condition '!=' in the accumulator.
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
        """ returns: Code that puts evaluation
        of condition '>' in the accumulator.
        True:   1
        False:  0
        Side effects in registers: 10 """
            
        c_list = []
        value1 = condition[1]
        value2 = condition[3]
        
        c_list.extend(self.value_to_acc(value2))
        c_list.append(Code('STORE', 10))
        c_list.extend(self.value_to_acc(value1))
        c_list.append(Code('SUB', 10))
        c_list.append(Code('JPOS', 3))
        c_list.append(Code('SET', 0))
        c_list.append(Code('JUMP', 2))  
        c_list.append(Code('SET', 1))
        
        return c_list
    
    
    def cond_L(self, condition):
        """ returns: Code that puts evaluation
        of condition '<' in the accumulator.
        True:   1
        False:  0
        Side effects in registers: 10 """
            
        c_list = []
        value1 = condition[1]
        value2 = condition[3]
        
        c_list.extend(self.value_to_acc(value2))
        c_list.append(Code('STORE', 10))
        c_list.extend(self.value_to_acc(value1))
        c_list.append(Code('SUB', 10))
        c_list.append(Code('JNEG', 3))
        c_list.append(Code('SET', 0))
        c_list.append(Code('JUMP', 2))  
        c_list.append(Code('SET', 1))
        
        return c_list
    
    
    def cond_GE(self, condition):
        """ returns: Code that puts evaluation
        of condition '>=' in the accumulator.
        True:   1
        False:  0
        Side effects in registers: 10 """
            
        c_list = []
        value1 = condition[1]
        value2 = condition[3]
        
        c_list.extend(self.value_to_acc(value2))
        c_list.append(Code('STORE', 10))
        c_list.extend(self.value_to_acc(value1))
        c_list.append(Code('SUB', 10))
        c_list.append(Code('JNEG', 3))
        c_list.append(Code('SET', 1))
        c_list.append(Code('JUMP', 2))  
        c_list.append(Code('SET', 0))
        
        return c_list
    
    
    def cond_LE(self, condition):
        """ returns: Code that puts evaluation
        of condition '<=' in the accumulator.
        True:   1
        False:  0
        Side effects in registers: 10 """
            
        c_list = []
        value1 = condition[1]
        value2 = condition[3]
        
        c_list.extend(self.value_to_acc(value2))
        c_list.append(Code('STORE', 10))
        c_list.extend(self.value_to_acc(value1))
        c_list.append(Code('SUB', 10))
        c_list.append(Code('JPOS', 3))
        c_list.append(Code('SET', 1))
        c_list.append(Code('JUMP', 2))  
        c_list.append(Code('SET', 0))
        
        return c_list
    
    
    def handle_condition(self, condition):
        """ returns: Code that puts evaluation
        of condition in the accumulator. """
        
        cond_tag = condition[2]
        
        if cond_tag == "=":
            return self.cond_EQ(condition)
        
        elif cond_tag == "!=":
            return self.cond_NE(condition)
        
        elif cond_tag == ">":
            print("\ncond_G\n")
            return self.cond_G(condition)
        
        elif cond_tag == "<":
            print("\ncond_L\n")
            return self.cond_L(condition)
        
        elif cond_tag == ">=":
            return self.cond_GE(condition)
        
        elif cond_tag == "<=":
            return self.cond_LE(condition)

        else:
            print(f"Error: Wrong tag: {cond_tag}")
            return
        
        
    def gc_comm_IF(self, command):
        """ returns: Code for command IF """
        
        c_list = []
        condition = command[1]
        commands = command[2]
        comms_list: list = self.comms_to_list(commands)
        comms_code = self.gc_command_list(comms_list)
        comms_code_length = len(comms_code)
        
        c_list.extend(self.handle_condition(condition))
        # if condition value is 0, we skip the commands
        c_list.append(Code('JZERO', comms_code_length + 1))
        c_list.extend(comms_code)
        
        return c_list
    
    
    def gc_comm_IF_ELSE(self, command):
        """ returns: Code for command IF """
        
        c_list = []
        condition = command[1]
        commands1 = command[2]
        commands2 = command[3]
        
        comms1_list: list = self.comms_to_list(commands1)
        comms1_code = self.gc_command_list(comms1_list)
        comms1_code_length = len(comms1_code)
        
        comms2_list: list = self.comms_to_list(commands2)
        comms2_code = self.gc_command_list(comms2_list)
        comms2_code_length = len(comms2_code)
        
        c_list.extend(self.handle_condition(condition))
        # if condition value is 0, we skip the commands and skip 'JUMP'
        c_list.append(Code('JZERO', comms1_code_length + 2))
        c_list.extend(comms1_code)
        c_list.append(Code('JUMP', comms2_code_length + 1)) # skip com2
        c_list.extend(comms2_code)
        
        return c_list

    
    def gc_comm_WHILE(self, command):
        """ returns: Code for command WHILE """
    
        c_list = []
        condition = command[1]
        commands = command[2]
        comms_list: list = self.comms_to_list(commands)
        comms_code = self.gc_command_list(comms_list)
        comms_code_length = len(comms_code)
        cond_code = self.handle_condition(condition)
        cond_code_length = len(cond_code)
        
        c_list.extend(self.handle_condition(condition))
        c_list.append(Code('JZERO', comms_code_length + 2))
        c_list.extend(comms_code)
        c_list.append(Code('JUMP', - comms_code_length - 1 - cond_code_length - 1))
        
        return c_list
    
    
    def gc_comm_REPEAT(self, command):
        """ returns: Code for command REPEAT """

        c_list = []
        commands = command[1]
        condition = command[2]
        comms_list: list = self.comms_to_list(commands)
        comms_code = self.gc_command_list(comms_list)
        comms_code_length = len(comms_code)
        cond_code = self.handle_condition(condition)
        cond_code_length = len(cond_code)
        
        # c_list.extend(self.handle_condition(condition))
        # c_list.append(Code('JZERO', comms_code_length + 2))
        # c_list.extend(comms_code)
        # c_list.append(Code('JUMP', - comms_code_length - 1 - cond_code_length - 1))
        
        c_list.extend(comms_code)
        c_list.extend(self.handle_condition(condition))
        # if condition is false (0), repeat the loop
        c_list.append(Code('JZERO', - comms_code_length - cond_code_length))
        
        return c_list
    
    
    def gc_comm_FOR(self, command):
        """ returns: Code for command FOR
        Uses registers: 50 """
        
        c_list = []
        iterator_PID = command[1]
        start_value = command[2]
        end_value = command[3]
        commands = command[4]
        comms_list: list = self.comms_to_list(commands)
        
        
        # creating a loop iterator and adding it to the symbol table
        for_prefix = '__FOR' + str(self.for_counter) + '_'
        self.for_counter += 1
        # iterator_name = for_prefix + iterator_PID
        iterator_name = iterator_PID # scope error!!!
        
        self.table.add_symbol(self.scope + iterator_name)    
        
        iterator_pos = self.table.get_symbol(self.scope + iterator_name)["position"]
        
        # adding start and end to symbol table
        start_name = for_prefix + 'start'
        self.table.add_symbol(start_name)
        start_pos = self.table.get_symbol(start_name)["position"]
        end_name = for_prefix + 'end'
        self.table.add_symbol(end_name)
        end_pos = self.table.get_symbol(end_name)["position"]
        
        # only now, when vriables are set in table, can we generate the code
        comms_code = self.gc_command_list(comms_list)
        comms_code_length = len(comms_code)   
        
        # load 1 to r50 for incrementation
        c_list.append(Code('SET', 1))
        c_list.append(Code('STORE', 50))
        
        # initial loop setup
        # load start and end loop values to start_pos and end_pos
        c_list.extend(self.value_to_acc(start_value))
        c_list.append(Code('STORE', start_pos))
        c_list.extend(self.value_to_acc(end_value))
        c_list.append(Code('STORE', end_pos))
        # set value of iterator to start
        c_list.append(Code('LOAD', start_pos))
        c_list.append(Code('STORE', iterator_pos))
        
        # start loop
        # check condition
        c_list.append(Code('LOAD', end_pos))
        c_list.append(Code('SUB', iterator_pos))
        # exit loop when iterator > end
        c_list.append(Code('JNEG', comms_code_length + 5)) 
        c_list.extend(comms_code)
        # increment iterator
        c_list.append(Code('LOAD', iterator_pos))
        c_list.append(Code('ADD', 50))
        c_list.append(Code('STORE', iterator_pos))
        # jump back to start of the loop
        c_list.append(Code('JUMP', - comms_code_length - 6))
        
        return c_list
    
    
    def gc_comm_FOR_DOWN(self, command):
            """ returns: Code for command FOR
            Uses registers: 50 """
            
            c_list = []
            iterator_PID = command[1]
            start_value = command[2]
            end_value = command[3]
            commands = command[4]
            comms_list: list = self.comms_to_list(commands)
            
            
            # creating a loop iterator and adding it to the symbol table
            for_prefix = '__FOR' + str(self.for_counter) + '_'
            self.for_counter += 1
            # iterator_name = for_prefix + iterator_PID
            iterator_name = iterator_PID # scope error!!!
            
            self.table.add_symbol(self.scope + iterator_name)    
            
            iterator_pos = self.table.get_symbol(self.scope + iterator_name)["position"]
            
            # adding start and end to symbol table
            start_name = for_prefix + 'start'
            self.table.add_symbol(start_name)
            start_pos = self.table.get_symbol(start_name)["position"]
            end_name = for_prefix + 'end'
            self.table.add_symbol(end_name)
            end_pos = self.table.get_symbol(end_name)["position"]
            
            # only now, when vriables are set in table, can we generate the code
            comms_code = self.gc_command_list(comms_list)
            comms_code_length = len(comms_code)   
            
            # load 1 to r50 for incrementation
            c_list.append(Code('SET', 1))
            c_list.append(Code('STORE', 50))
            
            # initial loop setup
            # load start and end loop values to start_pos and end_pos
            c_list.extend(self.value_to_acc(start_value))
            c_list.append(Code('STORE', start_pos))
            c_list.extend(self.value_to_acc(end_value))
            c_list.append(Code('STORE', end_pos))
            # set value of iterator to start
            c_list.append(Code('LOAD', start_pos))
            c_list.append(Code('STORE', iterator_pos))
            
            # start loop
            # check condition
            c_list.append(Code('LOAD', end_pos))
            c_list.append(Code('SUB', iterator_pos))
            # exit loop when iterator > end
            c_list.append(Code('JPOS', comms_code_length + 5)) 
            c_list.extend(comms_code)
            # increment iterator
            c_list.append(Code('LOAD', iterator_pos))
            c_list.append(Code('SUB', 50))
            c_list.append(Code('STORE', iterator_pos))
            # jump back to start of the loop
            c_list.append(Code('JUMP', - comms_code_length - 6))
            
            return c_list


    def calculate_expression(self, expression):
        """ returns: Code that calculates expression
        and puts its value to acc.
        Uses registers 30, 31 """
        
        c_list = []
        tag = expression[0]
        
        if tag == 'expr_VAL':
            value = expression[1]
            c_list.extend(self.value_to_acc(value))
        
        elif tag == 'expr_OP':
            value1 = expression[1]
            value2 = expression[3]
            operation_tag = expression[2]
            
            if operation_tag == "+":
                c_list.extend(self.value_to_acc(value2))
                c_list.append(Code('STORE', 30))
                c_list.extend(self.value_to_acc(value1))
                c_list.append(Code('ADD', 30))
            
            if operation_tag == "-":
                c_list.extend(self.value_to_acc(value2))
                c_list.append(Code('STORE', 30))
                c_list.extend(self.value_to_acc(value1))
                c_list.append(Code('SUB', 30))
            
            if operation_tag == '*':
                # naive O(n); TODO: improve

                # initiate values to registers
                c_list.extend(self.value_to_acc(value1))
                c_list.append(Code('STORE', 30)) # multiplicand to r30
                c_list.extend(self.value_to_acc(value2))
                c_list.append(Code('STORE', 31)) # multiplier to r31
                c_list.append(Code('STORE', 32)) # counter to r32, we will count downward
                c_list.append(Code('SET', 0))
                c_list.append(Code('STORE', 33)) # current value to r33
                c_list.append(Code('SET', 1))
                c_list.append(Code('STORE', 34)) # put "1" in r34 to use it to decrement counter
                
                # if multiplier is negative, perform special actions
                c_list.append(Code('LOAD', 31))
                c_list.append(Code('JPOS', 9)) # if positive, skip TODO: calc length
                c_list.append(Code('JZERO', 8)) # if zero, also skip TODO: calc length
                # subtract multiplier twice to make it positive
                c_list.append(Code('SUB', 31))
                c_list.append(Code('SUB', 31))
                c_list.append(Code('STORE', 32)) # put the value to r32 as a counter
                # subtract multiplicand twice to change its sign xdd, so hacky i'm embarrassed XD
                c_list.append(Code('LOAD', 30))
                c_list.append(Code('SUB', 30))
                c_list.append(Code('SUB', 30))
                c_list.append(Code('STORE', 30))
                
                # get out of loop when counter reaches 0
                c_list.append(Code('LOAD', 32))
                c_list.append(Code('JZERO', 8)) # 8 is hardcoded length of loop
                
                # loop:
                # add multiplicand to curr
                c_list.append(Code('LOAD', 33))
                c_list.append(Code('ADD', 30))
                c_list.append(Code('STORE', 33))
                # decrement counter
                c_list.append(Code('LOAD', 32))
                c_list.append(Code('SUB', 34))
                c_list.append(Code('STORE', 32))
                
                # go back to the start of loop
                c_list.append(Code('JUMP', -8)) # loop starts at -8, hardcoded
                
                # put result in acc
                c_list.append(Code('LOAD', 33))
                
            elif operation_tag == '/':
                # naive O(n); TODO: improve, implement negatives
                
                c_list.extend(self.value_to_acc(value1))
                c_list.append(Code('STORE', 30)) # dividend to r30
                c_list.append(Code('STORE', 33)) # current value to r33
                c_list.extend(self.value_to_acc(value2))
                c_list.append(Code('JZERO', 15)) # if divisor = 0 return 0
                c_list.append(Code('STORE', 31)) # divisor to r31
                c_list.append(Code('SET', 0))
                c_list.append(Code('STORE', 32)) # counter to r32
                c_list.append(Code('SET', 1))
                c_list.append(Code('STORE', 34)) # positive constant to r34
                c_list.append(Code('SET', -1))
                c_list.append(Code('STORE', 35)) # negative constant to r35
                c_list.append(Code('SET', 1))
                c_list.append(Code('STORE', 36)) # sign flag to r36
                
                # handle negative dividend
                c_list.append(Code('LOAD', 30))
                c_list.append(Code('JPOS', 9))
                c_list.append(Code('JZERO', 8))
                c_list.append(Code('SET', -1))
                c_list.append(Code('STORE', 36)) # change flag to negative
                # subtract dividend twice to make it positive
                c_list.append(Code('LOAD', 30))
                c_list.append(Code('SUB', 30))
                c_list.append(Code('SUB', 30))
                c_list.append(Code('STORE', 30)) # positive dividend to r30
                c_list.append(Code('STORE', 33))# positive current to 33
                
                # handle negative divisor
                c_list.append(Code('LOAD', 31))
                c_list.append(Code('JPOS', 10))
                c_list.append(Code('JZERO', 9))
                # swap sign of flag
                c_list.append(Code('LOAD', 36))
                c_list.append(Code('SUB', 36))
                c_list.append(Code('SUB', 36))
                c_list.append(Code('STORE', 36))
                # subtract divisor twice to make it positive
                c_list.append(Code('LOAD', 31))
                c_list.append(Code('SUB', 31))
                c_list.append(Code('SUB', 31))
                c_list.append(Code('STORE', 31))

                # loop:
                c_list.append(Code('LOAD', 33))
                c_list.append(Code('SUB', 31))
                c_list.append(Code('JNEG', 6)) # if negative, end loop
                
                # increment and go back    
                c_list.append(Code('STORE', 33))
                c_list.append(Code('LOAD', 32))
                c_list.append(Code('ADD', 34))
                c_list.append(Code('STORE', 32))
                c_list.append(Code('JUMP', -7))
                # endloop

                # if flag is negative, negate the result
                c_list.append(Code('LOAD', 36))
                c_list.append(Code('JPOS', 5))
                c_list.append(Code('LOAD', 32))
                c_list.append(Code('SUB', 32))
                c_list.append(Code('SUB', 32))
                c_list.append(Code('STORE', 32))
                
                c_list.append(Code('LOAD', 32)) # load result to acc
                
            elif operation_tag == '%':
                c_list.extend(self.value_to_acc(value1))
                c_list.append(Code('STORE', 30)) # dividend to r30
                c_list.append(Code('STORE', 33)) # current value to r33
                c_list.extend(self.value_to_acc(value2))
                c_list.append(Code('JZERO', 15)) # if divisor = 0 return 0
                c_list.append(Code('STORE', 31)) # divisor to r31
                c_list.append(Code('SET', 0))
                c_list.append(Code('STORE', 32)) # counter to r32
                c_list.append(Code('SET', 1))
                c_list.append(Code('STORE', 34)) # positive constant to r34
                c_list.append(Code('SET', -1))
                c_list.append(Code('STORE', 35)) # negative constant to r35
                c_list.append(Code('SET', 1))
                c_list.append(Code('STORE', 36)) # sign flag to r36
                
                # handle negative dividend
                c_list.append(Code('LOAD', 30))
                c_list.append(Code('JPOS', 9))
                c_list.append(Code('JZERO', 8))
                c_list.append(Code('SET', -1))
                c_list.append(Code('STORE', 36)) # change flag to negative
                # subtract dividend twice to make it positive
                c_list.append(Code('LOAD', 30))
                c_list.append(Code('SUB', 30))
                c_list.append(Code('SUB', 30))
                c_list.append(Code('STORE', 30)) # positive dividend to r30
                c_list.append(Code('STORE', 33))# positive current to 33
                
                # handle negative divisor
                c_list.append(Code('LOAD', 31))
                c_list.append(Code('JPOS', 10))
                c_list.append(Code('JZERO', 9))
                # swap sign of flag
                c_list.append(Code('LOAD', 36))
                c_list.append(Code('SUB', 36))
                c_list.append(Code('SUB', 36))
                c_list.append(Code('STORE', 36))
                # subtract divisor twice to make it positive
                c_list.append(Code('LOAD', 31))
                c_list.append(Code('SUB', 31))
                c_list.append(Code('SUB', 31))
                c_list.append(Code('STORE', 31))

                # loop:
                c_list.append(Code('LOAD', 33))
                c_list.append(Code('SUB', 31))
                c_list.append(Code('JNEG', 6)) # if negative, end loop
                
                # increment and go back    
                c_list.append(Code('STORE', 33))
                c_list.append(Code('LOAD', 32))
                c_list.append(Code('ADD', 34))
                c_list.append(Code('STORE', 32))
                c_list.append(Code('JUMP', -7))
                # endloop

                c_list.append(Code('LOAD', 32))
                c_list.append(Code('SUB', 32))

                # if flag is negative, negate the result
                c_list.append(Code('LOAD', 36))
                c_list.append(Code('JPOS', 5))
                c_list.append(Code('LOAD', 33))
                c_list.append(Code('SUB', 33))
                c_list.append(Code('SUB', 33))
                c_list.append(Code('STORE', 33))
                
                c_list.append(Code('LOAD', 33)) # load result to acc
            
            else:
                print(f"Error: wrong operator: {operation_tag}")
        
        return c_list
    
    
    ################## PROCEDURES ##################
    
    def procs_to_list(self, procs):
        """ returns: Procedures in form of a list """

        if procs == 'procs_EMPTY': 
            return []
        
        else:
            procs_list: list = self.procs_to_list(procs[1])
            procs_list.append(procs)
            return procs_list
    
    
    def get_proc_declarations(self, proc):
        """ returns: Procedure's declarations"""
        tag = proc[0]
        
        if tag == 'procs_LONG':
            return proc[3]
        
        else:
            print(f"Error: No procedure declarations. Tag: {tag}")
            return
        
    
    def get_proc_head(self, proc):
        """ returns: Procedure's proc_head """
        tag = proc[0]
        
        if tag == 'procs_LONG' or tag == 'procs_SHORT':
            return proc[2]
        else:
            print(f"Error: No proc_head. Tag: {tag}")
            return
    
    
    def get_phead_PID(self, proc_head):
        """ returns: Procedure's PID """
        return proc_head[1]
    
    
    def get_phead_args(self, proc_head):
        """ returns: Procedure's arguments """
        return proc_head[2]
    
    
    def get_proc_commands(self, procedures):
        tag = procedures[0]
        
        if tag == 'procs_SHORT':
            commands = procedures[3]
            
        elif tag == 'procs_LONG':  
            commands = procedures[4]
        
        return commands
        
           
    def proc_decs_to_table(self, proc):
        """ Puts procedure's declarations in the symbol table. """
        tag = proc[0]
        phead = self.get_proc_head(proc)
        proc_PID = self.get_phead_PID(phead)
        
        if tag == 'procs_LONG':
            decs = self.get_proc_declarations(proc)
        else:
            print(f"Error: no declarations. Tag: {tag}")
        
        self.decs_to_table(decs)
 

    def args_to_list(self, args):
        """ returns: Arguments in the list form. """
        tag = args[0]
        
        if tag == 'ar_PID':
            return [args[1]]
        
        elif tag == 'ar_REC':
            args_list: list = self.args_to_list(args[1])
            args_list.append(args[2])
            return args_list         


    def gc_comm_CALL(self, command):
        """ returns: Code for CALL command
        Uses registers 40 """

        c_list = []
        
        proc_call = command[1]
        proc_pid = proc_call[1]
        proc_args = proc_call[2] 
        
        # these are the arguments that were given when calling the procedure
        args_list = self.args_to_list(proc_args)
        print("args list: ", args_list)
        args_count = len(args_list)
        
        # these are argument references of a procedure
        refs_list = self.table.get_symbol(proc_pid)['arguments']
        refs_count = len(refs_list)
        print(f"refs_list: {refs_list}")
        # print(f"refs_list[0]: {refs_list[0]}")
        
        # if number of args != number of references, error
        if args_count != refs_count:
            print(f"Error: Number of arguments ({args_count}) does not match number of references ({refs_count}).")
            return
        

        # put argument positions into refs
        refs_assign_code = []
        for i in range(refs_count):
            # set acc to position of ref
            refs_assign_code.append(Code('SET', self.table.get_symbol(refs_list[i])["position"]))
            refs_assign_code.append(Code('STORE', 40)) # ref position to r41
            print("111")
            refs_assign_code.append(Code('SET', self.table.get_symbol(self.scope + args_list[i])["position"]))
            print("222")
            refs_assign_code.append(Code('STOREI', 40))
        refs_assign_code_len = len(refs_assign_code)
        c_list.extend(refs_assign_code)
        
        
        k = len(self.code_list) # k is a current instruction counter
        
        # adjust for code length of procedure
        # super fucking hacky idc anymore
        if self.scope != '':
            k += 10
            
            
        # Error: błędny adres powrotu, za mały
        c_list.append(Code('SET', k + refs_assign_code_len + 3))
        # setting return address for procedure
        c_list.append(Code('STORE', self.table.get_symbol(proc_pid)['position'] + 1))
        # RETURN to procedure and perform its code
        c_list.append(Code('RTRN', self.table.get_symbol(proc_pid)['position']))
        
        # XD
        if self.scope != '':
            c_list.append(Code('JUMP', 1))
            c_list.append(Code('JUMP', 1))
            c_list.append(Code('JUMP', 1))
            c_list.append(Code('JUMP', 1))
            c_list.append(Code('JUMP', 1))
            c_list.append(Code('JUMP', 1))
            c_list.append(Code('JUMP', 1))
            c_list.append(Code('JUMP', 1))
            c_list.append(Code('JUMP', 1))
            c_list.append(Code('JUMP', 1))
            c_list.append(Code('JUMP', 1))
            c_list.append(Code('JUMP', 1))
            c_list.append(Code('JUMP', 1))
            c_list.append(Code('JUMP', 1))
            c_list.append(Code('JUMP', 1))
        
        return c_list
         
        
    def refs_to_list(self, args_decl, proc_PID):
        """ returns: A list of argument declarations (references / refs)
        of a precodure.
        Doesn't differentiate between arrays and normal variables.
        Adds procedure scope prefix to names of variables. """

        tag = args_decl[0]
        
        # non recursive case
        if tag == 'ard_ARRAY' or tag == 'ard_PID':
            return [proc_PID + '__' + args_decl[1]]
        elif tag == 'ard_REC_PID' or tag == 'ard_REC_ARRAY':
            ard_list: list = self.refs_to_list(args_decl[1], proc_PID)
            ard_list.append(proc_PID + '__' + args_decl[2])
            return ard_list
        else:
            print(f"Error: Wrong tag: {tag}")
        
        
    def refs_to_table(self, args_decl):
        """ Writes argument declarations (references / refs) to the symbol table. """
        
        if args_decl is None:
            print("\nError: Arguments type is 'None'")
            return
        
        tag = args_decl[0]
            
        if tag == 'ard_PID':
            self.table.add_symbol_ref(self.scope + args_decl[1])

        elif tag == 'ard_ARRAY':
            self.table.add_array(self.scope + args_decl[1], 0, 0)
        
        elif tag == 'ard_REC_PID':
            self.refs_to_table(args_decl[1])
            self.table.add_symbol_ref(self.scope + args_decl[2])

        elif tag == 'ard_REC_ARRAY':
            self.refs_to_table(args_decl[1])
            self.table.add_array(self.scope + args_decl[2], 0, 0)
            
        else:
            print(f"\nError: Wrong tag: {tag}")
            return
        

    def gc_proc(self, procedure):
        """ returns: Code for procedure declaration. """
        
        c_list = []
        tag = procedure[0]
        proc_head = self.get_proc_head(procedure)
        proc_PID = self.get_phead_PID(proc_head)
        
        self.scope = proc_PID + '__'
        
        # add declarations to table if there are any
        if tag == 'procs_LONG':
            self.proc_decs_to_table(procedure)
        
        # add arguments to table as referances
        args_decl = self.get_phead_args(proc_head)
        self.refs_to_table(args_decl)
        
        # adding procedure to table
        
        refs_list = self.refs_to_list(args_decl, proc_PID)
        self.table.add_procedure(proc_PID, refs_list)
        
        # setting procedure position in table
        k = len(self.code_list) # current instruction counter
        c_list.append(Code('SET', k + 3))
        c_list.append(Code('STORE', self.table.get_symbol(proc_PID)["position"]))
        
        # generate code for commands
        commands = self.get_proc_commands(procedure)
        comms_list = self.comms_to_list(commands)
        code_list = self.gc_command_list(comms_list)
        code_length = len(code_list)
        
        # jump over the code of procedure
        # +1 for JUMP, +1 for RTRN
        c_list.append(Code('JUMP', code_length + 2))
        
        c_list.extend(code_list)
        # adding 1, because RTRN address is 1 after procedure declaration
        c_list.append(Code('RTRN', self.table.get_symbol(proc_PID)["position"] + 1))
        
        self.scope = ''
        
        return c_list
    
    

        
        
    




if __name__ == '__main__':
    lexer = MyLexer()
    parser = MyParser()
    
    input = 'examples/my-proc.imp'
    # input = 'examples/program1.imp'
    output = 'output/my-out.mr'


    with open(input, 'r') as file:
        data = file.read()
        
    tokens = lexer.tokenize(data)
    
    parsed = parser.parse(tokens)
    
    gen = CodeGenerator(parsed, False)

    code = gen.generate_code()
    
    
    # with open(output, 'w') as file:
    #     for line in code:
    #         file.write(line + '\n')