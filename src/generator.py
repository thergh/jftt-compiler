from parser import MyParser
from lexer import MyLexer
from table import SymbolTable
  
  
  
class Code:
    """ Represents vm code """
    
    def __init__(self, name, value=None, comment=None):
        self.name = name
        self.value = value
        self.comment = comment
        
    def to_string(self):
        """ Changes format of a code
        from tuple to string """
        
        if self.value is None:
            return f"{self.name}"
        
        else:
            if self.comment is None:
                return f"{self.name} {self.value}"    
            else:
                return f"{self.name} {self.value} \t# {self.comment}"    
  
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
        self.scope_length = 0
        self.line_number = 0
        
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
        self.line_number += 1 # PROGRAM IS
        
        declarations = self.get_declarations()
        
        if declarations is not None:
            self.decs_to_table(declarations)
            
        self.line_number += 1 # declarations
        self.line_number += 1 # BEGIN
            
        # Handling initial commands
        main_comms = self.get_main_commands()
        main_comms_list = self.comms_to_list(main_comms)
        
        for x in main_comms_list:
            self.code_list.extend(self.gc_command(x))

        code_string = self.code_list_to_string()
        code_string.append("HALT")
        
        self.line_number += 1 # END
        
        
        if self.debug:
            print("SYMBOL TABLE:\n")
            self.table.display()
            print()
            # print("CODE:\n")
            # for c in code_string:
            #     print(c)
            # print(f"line number after generating: {self.line_number}")
            
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
            decs_lineno = decs[2]
            self.table.add_symbol(self.scope + decs[1], decs_lineno)

        elif tag == 'decs_ARRAY':
            decs_lineno = decs[4]
            self.table.add_array(self.scope + decs[1], decs[2], decs[3], decs_lineno)
        
        elif tag == 'decs_REC_PID':
            self.decs_to_table(decs[1])
            decs_lineno = decs[3]
            self.table.add_symbol(self.scope + decs[2], decs_lineno)

        elif tag == 'decs_REC_ARRAY':
            self.decs_to_table(decs[1])
            decs_lineno = decs[5]
            self.table.add_array(self.scope + decs[2], decs[3], decs[4], decs_lineno)
            
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
            
        length = len(c_list)
        self.scope_length += length
            
        return c_list


    def id_pos_to_acc(self, identifier):
        """ returns: Code that puts symbol table position
        of PID into accumulator.
        Uses r60 """
        # TODO: reference arrays
        
        id_tag = identifier[0]
        c_list = []
        
        if id_tag == 'id_PID':
            id = identifier[1]
            id_lineno = identifier[2]
            
            # check if id is a reference
            if(self.table.get_symbol(self.scope + id, id_lineno)['is_reference']):
                ref_pos = self.table.get_symbol(self.scope + id, id_lineno)['position']
                c_list.append(Code('LOAD', ref_pos))
    
            else: # normal case
                id_pos = self.table.get_symbol(self.scope + id)['position']
                c_list.append(Code('SET', id_pos))
            
        elif id_tag == 'id_ARRAY_NUM':
            arr_PID = identifier[1]
            arr_lineno = identifier[3]
            
            if self.table.get_symbol(self.scope + arr_PID, arr_lineno)['is_reference']:
                arr_PID = identifier[1]
                number = identifier[2]
                arr_ref_pos = self.table.get_symbol(self.scope + arr_PID, arr_lineno)['position']

                # TODO: include offset
                c_list.append(Code('LOAD', arr_ref_pos, "DEBUG: ładuję arr_ref_pos")) # load position of array
                c_list.append(Code('STORE ', 60))
                c_list.append(Code('SET ', number))
                c_list.append(Code('ADD ', 60))
            
            else:
                arr_PID = identifier[1]
                number = identifier[2]
                arr_pos = self.table.get_symbol(self.scope + arr_PID, arr_lineno)['position']
                position = int(arr_pos) + int(number)
                c_list.append(Code('SET', position))
                
            
        elif id_tag == 'id_ARRAY_PID':
            arr_PID = identifier[1]
            arr_lineno = identifier[3]
            
            # check if index identifier is assigned
            idx_PID = identifier[2]
            if self.table.get_symbol(self.scope + idx_PID, arr_lineno)["assigned"] != True:
                print(f"\nError in line {arr_lineno}: {idx_PID} not assigned.\n")
                return
            
            if self.table.get_symbol(self.scope + arr_PID, arr_lineno)['is_reference']:
                arr_ref_pos = self.table.get_symbol(self.scope + arr_PID, arr_lineno)['position']
                idx_ref_pos = self.table.get_symbol(self.scope + idx_PID, arr_lineno)['position']

                # load idx to acc
                c_list.append(Code('LOAD', arr_ref_pos, "DEBUG: ładuję arr_ref_pos")) # load position of array
                c_list.append(Code('STORE ', 60))
                c_list.append(Code('LOAD', idx_ref_pos, "DEBUG: ładuję idx_ref_pos")) # load position of array
                c_list.append(Code('ADD ', 60))
                
            else:
                arr_pos = self.table.get_symbol(self.scope + arr_PID, arr_lineno)['position']
                idx_pos = self.table.get_symbol(self.scope + idx_PID, arr_lineno)['position']

                # load idx to acc
                c_list.append(Code('LOAD', idx_pos))
                c_list.append(Code('STORE', 60))
                # add array position and subtract offset
                c_list.append(Code('SET', int(arr_pos)))
                c_list.append(Code('ADD', 60))
            
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
            val_lineno = value[2]
            
            # if identifier is not assigned, return error
            if self.table.get_symbol(self.scope + identifier[1], val_lineno)["assigned"] != True:
                print(f"\nError in line {val_lineno}: {identifier[1]} not assigned.\n")
                return
            
            # if value is an array indexed by an identifier, check if it's assigned
            
            c_list.extend(self.id_pos_to_acc(identifier)) # puts id_pos into acc
            c_list.append(Code('LOADI', 0)) # load value of id to reg0
        
        return c_list
    
    
    def gc_comm_READ(self, command):
        """ returns: Code for command READ """
        
        c_list = []
        identifier = command[1]
        tag = identifier[0]
        
        self.table.mark_assigned(identifier[1])
        
        c_list.extend(self.id_pos_to_acc(identifier))
        c_list.append(Code('STORE', 1))
        c_list.append(Code('GET', 0))
        c_list.append(Code('STOREI', 1))
        
        self.line_number += 1
        return c_list
        

    def gc_comm_WRITE(self, command):
        """ returns: Code for command WRITE """
        c_list = []
        value = command[1]
        
        c_list.extend(self.value_to_acc(value))
        c_list.append(Code('PUT', 0))
        
        self.line_number += 1
        return c_list
    
    
    def gc_comm_ASSIGN(self, command):
        """ returns: Code for command ASSIGN """
 
        c_list = []
        identifier = command[1]
        expression = command[2]
        id_tag = identifier[0]
        
        if id_tag == 'id_PID':
            id_lineno = identifier[2]
        elif id_tag == 'id_ARRAY_PID' or id_tag == 'id_ARRAY_NUM':
            id_lineno = identifier[3]
            
        # check if not normal variable identifier as array
        if id_tag == 'id_ARRAY_PID' or id_tag == 'id_ARRAY_NUM':
            arr_PID = identifier[1]
            id_lineno = identifier[3]
            if self.table.get_symbol(self.scope + arr_PID, id_lineno)["is_array"] != True:
                print(f"\nError in line {id_lineno}: incorrect usage of array {arr_PID}.\n")
                return
            
        # check if trying to change iterator
        id_PID = identifier[1]
        if self.table.get_symbol(self.scope + id_PID, id_lineno)["is_iterator"]:
            print(f"\nError in line {id_lineno}: modifying iterator {id_PID} is not allowed.\n")
            return
        
                
        # mark identifier as assigned
        self.table.mark_assigned(self.scope + identifier[1], id_lineno)
    
        c_list.extend(self.id_pos_to_acc(identifier)) # reg0: id1_pos
        c_list.append(Code('STORE', 1)) # store id1_pos in reg1
        
        c_list.extend(self.calculate_expression(expression)) # calculate value of expression and put into acc
        c_list.append(Code('STOREI', 1)) # set velue on position

        self.line_number += 1
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
            return self.cond_G(condition)
        
        elif cond_tag == "<":
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
        self.line_number += 1 # IF condition
        
        c_list.extend(comms_code)
        
        self.line_number += 1 # IF ENDIF
        return c_list
    
    
    def gc_comm_IF_ELSE(self, command):
        """ returns: Code for command IF """
        
        c_list = []
        condition = command[1]
        commands1 = command[2]
        commands2 = command[3]
        
        self.line_number += 1 # IF condition
        comms1_list: list = self.comms_to_list(commands1)
        comms1_code = self.gc_command_list(comms1_list)
        comms1_code_length = len(comms1_code)
        
        self.line_number += 1 # ELSE
        comms2_list: list = self.comms_to_list(commands2)
        comms2_code = self.gc_command_list(comms2_list)
        comms2_code_length = len(comms2_code)
        
        c_list.extend(self.handle_condition(condition))
        
        # if condition value is 0, we skip the commands and skip 'JUMP'
        c_list.append(Code('JZERO', comms1_code_length + 2))
        c_list.extend(comms1_code)
        c_list.append(Code('JUMP', comms2_code_length + 1)) # skip com2
        c_list.extend(comms2_code)
        
        self.line_number += 1 # ENDIF
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
        self.line_number += 1 # WHILE
        c_list.append(Code('JZERO', comms_code_length + 2))
        c_list.extend(comms_code)
        c_list.append(Code('JUMP', - comms_code_length - 1 - cond_code_length - 1, "WHILE jump back"))
        
        self.line_number += 1 # ENDWHILE
        return c_list
    
    
    def gc_comm_REPEAT(self, command):
        """ returns: Code for command REPEAT """
        
        self.line_number += 1 # REPEAT
        
        c_list = []
        commands = command[1]
        condition = command[2]
        comms_list: list = self.comms_to_list(commands)
        comms_code = self.gc_command_list(comms_list)
        comms_code_length = len(comms_code)
        cond_code = self.handle_condition(condition)
        cond_code_length = len(cond_code)

        c_list.extend(comms_code)
        c_list.extend(self.handle_condition(condition))
        # if condition is false (0), repeat the loop
        c_list.append(Code('JZERO', - comms_code_length - cond_code_length, "REPEAT jump back"))
        
        self.line_number += 1 # UNTIL
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
        for_lineno = command[5]     
        
        # creating a loop iterator and adding it to the symbol table
        for_prefix = '__FOR' + str(self.for_counter) + '_'
        self.for_counter += 1
        # iterator_name = for_prefix + iterator_PID
        iterator_name = iterator_PID # scope error!!! TODO ??? i don't remember anymore XD
        
        self.table.add_iterator(self.scope + iterator_name, for_lineno)    
        
        iterator_pos = self.table.get_symbol(self.scope + iterator_name, for_lineno)["position"]
        
        # adding start and end to symbol table
        start_name = for_prefix + 'start'
        self.table.add_symbol(start_name, for_lineno)
        start_pos = self.table.get_symbol(start_name, for_lineno)["position"]
        end_name = for_prefix + 'end'
        self.table.add_symbol(end_name, for_lineno)
        end_pos = self.table.get_symbol(end_name, for_lineno)["position"]
        
        self.line_number += 1 # FOR
        
        # only now, when vriables are set in table, can we generate the code
        comms_code = self.gc_command_list(comms_list)
        comms_code_length = len(comms_code)   
        
        # load 1 to r50 for incrementation
        c_list.append(Code('SET', 1, "FOR start"))
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
        c_list.append(Code('LOAD', end_pos, "FOR loop condition"))
        c_list.append(Code('SUB', iterator_pos))
        # exit loop when iterator > end
        c_list.append(Code('JNEG', comms_code_length + 5)) 
        c_list.extend(comms_code)
        # increment iterator
        c_list.append(Code('LOAD', iterator_pos))
        c_list.append(Code('ADD', 50))
        c_list.append(Code('STORE', iterator_pos))
        # jump back to start of the loop
        c_list.append(Code('JUMP', - comms_code_length - 6, "FOR jump back"))
        
        self.line_number += 1 # ENDFOR
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
            for_lineno = command[5]
            
            # creating a loop iterator and adding it to the symbol table
            for_prefix = '__FOR' + str(self.for_counter) + '_'
            self.for_counter += 1
            # iterator_name = for_prefix + iterator_PID
            iterator_name = iterator_PID # scope error!!!
            
            self.table.add_iterator(self.scope + iterator_name, for_lineno)    
            
            iterator_pos = self.table.get_symbol(self.scope + iterator_name, for_lineno)["position"]
            
            # adding start and end to symbol table
            start_name = for_prefix + 'start'
            self.table.add_symbol(start_name, for_lineno)
            start_pos = self.table.get_symbol(start_name, for_lineno)["position"]
            end_name = for_prefix + 'end'
            self.table.add_symbol(end_name, for_lineno)
            end_pos = self.table.get_symbol(end_name, for_lineno)["position"]
            
            self.line_number += 1 # FOR
            
            # only now, when vriables are set in table, can we generate the code
            comms_code = self.gc_command_list(comms_list)
            comms_code_length = len(comms_code)   
            
            # load 1 to r50 for incrementation
            c_list.append(Code('SET', 1, "FOR_DOWN start"))
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
            c_list.append(Code('JUMP', - comms_code_length - 6, "FOR_DOWN jump back"))
            
            self.line_number += 1 # ENDFOR
            return c_list


    def calculate_expression(self, expression):
        """ returns: Code that calculates expression
        and puts its value to acc.
        Uses registers 30-36 """
        
        c_list = []
        tag = expression[0]
            
        if tag == 'expr_VAL':
            value = expression[1]
            expr_lineno = value[2]
            
            # check if trying to use array as value
            if value[0] == 'val_ID':
                id = value[1]
                if id[0] == 'id_PID' and self.table.get_symbol(self.scope + id[1], expr_lineno)["is_array"]:
                    print(f"\nError in line {expr_lineno}: incorrect usage of array {id[1]}.\n")
                    return
            
            c_list.extend(self.value_to_acc(value))
        
        elif tag == 'expr_OP':
            
            value1 = expression[1]
            value2 = expression[3]
            operation_tag = expression[2]
            expr_lineno = expression[4]

            # check if values are assigned
            if value1[0] == 'val_ID':
                id = value1[1]
                if self.table.get_symbol(self.scope + id[1], expr_lineno)["assigned"] != True:
                    print(f"\nError in line {expr_lineno}: {id[1]} not assigned.\n")
                    return
            if value2[0] == 'val_ID':
                id = value2[1]
                if self.table.get_symbol(self.scope + id[1], expr_lineno)["assigned"] != True:
                    print(f"\nError in line {expr_lineno}: {id[1]} not assigned.\n")
                    return
            
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
                # r30:  multiplicand
                # r31:  multiplier
                # r32:  result
                # r37:  negative flag
                
                c_list.extend(self.value_to_acc(value1))
                c_list.append(Code('STORE', 30)) # multiplicand to r30
                c_list.extend(self.value_to_acc(value2))
                c_list.append(Code('STORE', 31)) # multiplier to r31
                c_list.append(Code('SET', 0))
                c_list.append(Code('STORE', 32))
                c_list.append(Code('SET', 1)) # negative flag to r37
                c_list.append(Code('STORE', 37))
                
                # # multiplicand flag setup
                c_list.append(Code('LOAD', 30)) 
                c_list.append(Code('JPOS', 10)) 
                c_list.append(Code('JZERO', 9))
                c_list.append(Code('LOAD', 37)) 
                c_list.append(Code('SUB', 37))
                c_list.append(Code('SUB', 37)) 
                c_list.append(Code('STORE', 37))
                # make multiplicand pos
                c_list.append(Code('LOAD', 30))
                c_list.append(Code('SUB', 30)) 
                c_list.append(Code('SUB', 30)) 
                c_list.append(Code('STORE', 30)) 
                
                # # multiplier flag setup
                c_list.append(Code('LOAD', 31)) 
                c_list.append(Code('JPOS', 10)) 
                c_list.append(Code('JZERO', 9))
                c_list.append(Code('LOAD', 37)) 
                c_list.append(Code('SUB', 37))
                c_list.append(Code('SUB', 37)) 
                c_list.append(Code('STORE', 37))
                # make multiplier pos
                c_list.append(Code('LOAD', 31))
                c_list.append(Code('SUB', 31)) 
                c_list.append(Code('SUB', 31)) 
                c_list.append(Code('STORE', 31))
                
                # BEGIN WHILE
                # while multiplier > 0:
                c_list.append(Code('LOAD', 31))
                c_list.append(Code('JZERO', 17))
                c_list.append(Code('JNEG', 16))
                
                # BEGIN IF 
                # if multiplier % 2 == 1:  # check if multiplier is odd
                    # if multiplier / 2 * 2 == multiplier:
                        # multiplier is divisible by 2
                    # else:
                        # multiplier is not divisible by 2
                c_list.append(Code('LOAD', 31))
                c_list.append(Code('HALF'))
                c_list.append(Code('ADD', 0))
                c_list.append(Code('SUB', 31))
                c_list.append(Code('JZERO', 4)) # jump if even
                
                # result = result + multiplicand
                c_list.append(Code('LOAD', 32))
                c_list.append(Code('ADD', 30))
                c_list.append(Code('STORE', 32))
                # END IF 
                
                # multiplicand = multiplicand * 2
                c_list.append(Code('LOAD', 30))
                c_list.append(Code('ADD', 30))
                c_list.append(Code('STORE', 30))
                # multiplier = multiplier / 2      # Halve the multiplier
                c_list.append(Code('LOAD', 31))
                c_list.append(Code('HALF'))
                c_list.append(Code('STORE', 31))
                
                c_list.append(Code('JUMP', -17))
                # END WHILE
                
                # if flag < 0; change result sign
                c_list.append(Code('LOAD', 37))
                c_list.append(Code('JPOS', 5))
                c_list.append(Code('LOAD', 32))
                c_list.append(Code('SUB', 32))
                c_list.append(Code('SUB', 32))
                c_list.append(Code('STORE', 32))
                
                # load result
                c_list.append(Code('LOAD', 32))
                
            elif operation_tag == '/':
                # r30:  dividend
                # r31:  divisor
                # r32:  quotient - Q
                # r33:  remainder - R
                # r34:  temp divisor - D
                # r35:  1
                # r36:  multiple - M
                # r37:  negative flag

                # setup
                c_list.extend(self.value_to_acc(value1)) # dividend to r30
                c_list.append(Code('STORE', 30)) 
                c_list.extend(self.value_to_acc(value2)) # divisor to r31
                c_list.append(Code('STORE', 31))
                c_list.append(Code('SET', 1)) # 1 to r35
                c_list.append(Code('STORE', 35)) 
                c_list.append(Code('SET', 1)) # negative flag to r37
                c_list.append(Code('STORE', 37))
                
                # # dividend flag setup
                c_list.append(Code('LOAD', 30)) 
                c_list.append(Code('JPOS', 10)) 
                c_list.append(Code('JZERO', 9))
                c_list.append(Code('LOAD', 37)) 
                c_list.append(Code('SUB', 37))
                c_list.append(Code('SUB', 37)) 
                c_list.append(Code('STORE', 37))
                # make dividend pos
                c_list.append(Code('LOAD', 30))
                c_list.append(Code('SUB', 30)) 
                c_list.append(Code('SUB', 30)) 
                c_list.append(Code('STORE', 30)) 
                
                # # divisor flag setup
                c_list.append(Code('LOAD', 31)) 
                c_list.append(Code('JPOS', 10)) 
                c_list.append(Code('JZERO', 9))
                c_list.append(Code('LOAD', 37)) 
                c_list.append(Code('SUB', 37))
                c_list.append(Code('SUB', 37)) 
                c_list.append(Code('STORE', 37))
                # make dividend pos
                c_list.append(Code('LOAD', 31))
                c_list.append(Code('SUB', 31)) 
                c_list.append(Code('SUB', 31)) 
                c_list.append(Code('STORE', 31)) 

                # setup Q and R
                c_list.append(Code('SET', 0)) # Q = 0 to r32
                c_list.append(Code('STORE', 32))
                c_list.append(Code('LOAD', 30)) # R = dividend to r33
                c_list.append(Code('STORE', 33))

                # if divisor == 0; return TODO
                c_list.append(Code('LOAD', 31)) 
                c_list.append(Code('JZERO', 32))

                # BEGIN WHILE_2
                # while divisor <= remainder:
                c_list.append(Code('LOAD', 33))
                c_list.append(Code('SUB', 31))
                c_list.append(Code('JNEG', 23))
                
                # before loop1
                # temp_divisor = divisor
                c_list.append(Code('LOAD', 31)) # D = divisor to r34
                c_list.append(Code('STORE', 34))
                # multiple = 1
                c_list.append(Code('LOAD', 35))
                c_list.append(Code('STORE', 36)) # M = 1 to r36
                
                # BEGIN WHILE_1                
                # while temp_divisor * 2 <= remainder:
                c_list.append(Code('LOAD', 33))
                c_list.append(Code('SUB', 34))
                c_list.append(Code('SUB', 34))
                c_list.append(Code('JNEG', 8)) # if D > R, escape loop
                
                # temp_divisor = temp_divisor * 2
                c_list.append(Code('LOAD', 34))
                c_list.append(Code('ADD', 34))
                c_list.append(Code('STORE', 34))
                
                # multiple = multiple * 2
                c_list.append(Code('LOAD', 36))
                c_list.append(Code('ADD', 36))
                c_list.append(Code('STORE', 36))
                
                # jump back to loop1
                c_list.append(Code('JUMP', -10))
                # END WHILE_1
                
                # after loop1
                # remainder = remainder - temp_divisor
                c_list.append(Code('LOAD', 33))
                c_list.append(Code('SUB', 34))
                c_list.append(Code('STORE', 33))
                # quotient = quotient + multiple
                c_list.append(Code('LOAD', 32))
                c_list.append(Code('ADD', 36))
                c_list.append(Code('STORE', 32))
                
                # jump back to loop2
                c_list.append(Code('JUMP', -24))
                # END WHILE_2
                
                # if flag < 0; change result sign
                c_list.append(Code('LOAD', 37))
                c_list.append(Code('JPOS', 5))
                c_list.append(Code('LOAD', 32))
                c_list.append(Code('SUB', 32))
                c_list.append(Code('SUB', 32))
                c_list.append(Code('STORE', 32))
       
                # return quotient
                c_list.append(Code('LOAD', 32))
                
            elif operation_tag == '%':
                # r30:  dividend
                # r31:  divisor
                # r32:  quotient - Q
                # r33:  remainder - R
                # r34:  temp divisor - D
                # r35:  1
                # r36:  multiple - M
                # r37:  negative flag

                # setup
                c_list.extend(self.value_to_acc(value1)) # dividend to r30
                c_list.append(Code('STORE', 30)) 
                c_list.extend(self.value_to_acc(value2)) # divisor to r31
                c_list.append(Code('STORE', 31))
                c_list.append(Code('SET', 1)) # 1 to r35
                c_list.append(Code('STORE', 35)) 
                c_list.append(Code('SET', 1)) # negative flag to r37
                c_list.append(Code('STORE', 37))
                
                # # dividend flag setup
                c_list.append(Code('LOAD', 30)) 
                c_list.append(Code('JPOS', 10)) 
                c_list.append(Code('JZERO', 9))
                c_list.append(Code('LOAD', 37)) 
                c_list.append(Code('SUB', 37))
                c_list.append(Code('SUB', 37)) 
                c_list.append(Code('STORE', 37))
                # make dividend pos
                c_list.append(Code('LOAD', 30))
                c_list.append(Code('SUB', 30)) 
                c_list.append(Code('SUB', 30)) 
                c_list.append(Code('STORE', 30)) 
                
                # # divisor flag setup
                c_list.append(Code('LOAD', 31)) 
                c_list.append(Code('JPOS', 10)) 
                c_list.append(Code('JZERO', 9))
                c_list.append(Code('LOAD', 37)) 
                c_list.append(Code('SUB', 37))
                c_list.append(Code('SUB', 37)) 
                c_list.append(Code('STORE', 37))
                # make dividend pos
                c_list.append(Code('LOAD', 31))
                c_list.append(Code('SUB', 31)) 
                c_list.append(Code('SUB', 31)) 
                c_list.append(Code('STORE', 31)) 

                # setup Q and R
                c_list.append(Code('SET', 0)) # Q = 0 to r32
                c_list.append(Code('STORE', 32))
                c_list.append(Code('LOAD', 30)) # R = dividend to r33
                c_list.append(Code('STORE', 33))

                # if divisor == 0; return TODO
                c_list.append(Code('LOAD', 31)) 
                c_list.append(Code('JZERO', 32))

                # BEGIN WHILE_2
                # while divisor <= remainder:
                c_list.append(Code('LOAD', 33))
                c_list.append(Code('SUB', 31))
                c_list.append(Code('JNEG', 23))
                
                # before loop1
                # temp_divisor = divisor
                c_list.append(Code('LOAD', 31)) # D = divisor to r34
                c_list.append(Code('STORE', 34))
                # multiple = 1
                c_list.append(Code('LOAD', 35))
                c_list.append(Code('STORE', 36)) # M = 1 to r36
                
                # BEGIN WHILE_1                
                # while temp_divisor * 2 <= remainder:
                c_list.append(Code('LOAD', 33))
                c_list.append(Code('SUB', 34))
                c_list.append(Code('SUB', 34))
                c_list.append(Code('JNEG', 8)) # if D > R, escape loop
                
                # temp_divisor = temp_divisor * 2
                c_list.append(Code('LOAD', 34))
                c_list.append(Code('ADD', 34))
                c_list.append(Code('STORE', 34))
                
                # multiple = multiple * 2
                c_list.append(Code('LOAD', 36))
                c_list.append(Code('ADD', 36))
                c_list.append(Code('STORE', 36))
                
                # jump back to loop1
                c_list.append(Code('JUMP', -10))
                # END WHILE_1
                
                # after loop1
                # remainder = remainder - temp_divisor
                c_list.append(Code('LOAD', 33))
                c_list.append(Code('SUB', 34))
                c_list.append(Code('STORE', 33))
                # quotient = quotient + multiple
                c_list.append(Code('LOAD', 32))
                c_list.append(Code('ADD', 36))
                c_list.append(Code('STORE', 32))
                
                # jump back to loop2
                c_list.append(Code('JUMP', -24))
                # END WHILE_2
                
                # if flag < 0; change result sign
                c_list.append(Code('LOAD', 37))
                c_list.append(Code('JPOS', 5))
                c_list.append(Code('LOAD', 33))
                c_list.append(Code('SUB', 33))
                c_list.append(Code('SUB', 33))
                c_list.append(Code('STORE', 33))
       
                # return quotient
                c_list.append(Code('LOAD', 33))
            
            else:
                print(f"Error: wrong operator: {operation_tag}")
                # return
        
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
        call_lineno = proc_call[3]
        
        # check if not recursive call
        if self.scope != '':
            if proc_pid == self.scope[:-2]:
                print(f"\nError in line {call_lineno}: recursive call of {proc_pid} not allowed.\n")
                return
    
        # these are the arguments that were given when calling the procedure
        args_list = self.args_to_list(proc_args)
        args_count = len(args_list)
        
        # mark arguments as assigned
        for a in args_list:
            self.table.mark_assigned(self.scope + a, call_lineno)
        
        # these are argument references of a procedure
        refs_list = self.table.get_symbol(proc_pid, call_lineno)['arguments']
        refs_count = len(refs_list)
        
        # if number of args != number of references, error
        if args_count != refs_count:
            print(f"\nError in line {call_lineno}: number of arguments ({args_count}) does not match number of references ({refs_count}).\n")
            return

        # put argument positions into refs
        refs_assign_code = []
        
        # check if args and refs are matching ("is_array")
        for i in range(refs_count):
            if self.table.get_symbol(self.scope + args_list[i])["is_array"] != self.table.get_symbol(refs_list[i])["is_array"]:
                print(f"Error in line {call_lineno}: procedure parameter {self.scope + args_list[i]} type mismatch.")
                return
        
        if self.scope == '':
            for i in range(refs_count):
                # set acc to position of ref
                refs_assign_code.append(Code('SET', self.table.get_symbol(refs_list[i], call_lineno)["position"]))
                refs_assign_code.append(Code('STORE', 40)) # ref position to r41
                refs_assign_code.append(Code('SET', self.table.get_symbol(self.scope + args_list[i], call_lineno)["position"]))
                refs_assign_code.append(Code('STOREI', 40))
        else:
            for i in range(refs_count):
                # set acc to position of ref
                refs_assign_code.append(Code('SET', self.table.get_symbol(refs_list[i], call_lineno)["position"]))
                refs_assign_code.append(Code('STORE', 40)) # ref position to r41
                refs_assign_code.append(Code('SET', self.table.get_symbol(self.scope + args_list[i], call_lineno)["position"]))
                refs_assign_code.append(Code('LOADI', 0)) # IDK why it must be here ¯\_(ツ)_/¯
                refs_assign_code.append(Code('STOREI', 40))    
        
        refs_assign_code_len = len(refs_assign_code)
        c_list.extend(refs_assign_code)
        
        k = len(self.code_list) # k is a current instruction counter
        
        # adjust for code length of procedure
        # super fucking hacky, I let God take the wheel
        if self.scope != '':
            k += 3 + self.scope_length
            
        c_list.append(Code('SET', k + refs_assign_code_len + 3, "CALL: set return position"))
        # setting return address for procedure
        c_list.append(Code('STORE', self.table.get_symbol(proc_pid, call_lineno)['position'] + 1))
        # RETURN to procedure and perform its code
        c_list.append(Code('RTRN', self.table.get_symbol(proc_pid, call_lineno)['position'],
                           "CALL: go to " + proc_pid + " procedure"))
        
        self.line_number += 1
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
            print("\nError: Argument's type is 'None'")
            return
        
        tag = args_decl[0]
        args_lineno = [3]
            
        if tag == 'ard_PID':
            self.table.add_symbol_ref(self.scope + args_decl[1], args_lineno)

        elif tag == 'ard_ARRAY':
            self.table.add_array_ref(self.scope + args_decl[1], args_lineno)
        
        elif tag == 'ard_REC_PID':
            self.refs_to_table(args_decl[1])
            self.table.add_symbol_ref(self.scope + args_decl[2], args_lineno)

        elif tag == 'ard_REC_ARRAY':
            self.refs_to_table(args_decl[1])
            self.table.add_array_ref(self.scope + args_decl[2], args_lineno)
            
        else:
            print(f"\nError in line {args_lineno}: wrong tag: {tag}")
            return
        

    def gc_proc(self, procedure):
        """ returns: Code for procedure declaration. """
        
        c_list = []
        tag = procedure[0]
        proc_head = self.get_proc_head(procedure)
        proc_PID = self.get_phead_PID(proc_head)
        proc_head_lineno = proc_head[3]
        
        self.scope = proc_PID + '__'
        self.scope_length = 0
        
        # add arguments to table as referances
        args_decl = self.get_phead_args(proc_head)
        self.refs_to_table(args_decl)
        self.line_number += 1 # PROCEDURE
        
        # add declarations to table if there are any
        if tag == 'procs_LONG':
            self.proc_decs_to_table(procedure)
            self.line_number += 1 # proc declarations
            
        self.line_number += 1 # proc BEGIN
        
        # adding procedure to table
        refs_list = self.refs_to_list(args_decl, proc_PID)
        self.table.add_procedure(proc_PID, refs_list)
        
        # setting procedure position in table
        k = len(self.code_list) # current instruction counter
        c_list.append(Code('SET', k + 3, proc_PID + ": set procedure position"))
        c_list.append(Code('STORE', self.table.get_symbol(proc_PID, proc_head_lineno)["position"]))
        
        # generate code for commands
        commands = self.get_proc_commands(procedure)
        comms_list = self.comms_to_list(commands)
        code_list = self.gc_command_list(comms_list)
        code_length = len(code_list)
        
        # jump over the code of procedure
        # +1 for JUMP, +1 for RTRN
        c_list.append(Code('JUMP', code_length + 2, proc_PID + ": jump over procedure code"))
        
        c_list.extend(code_list)
        # adding 1, because RTRN address is 1 after procedure declaration
        c_list.append(Code('RTRN', self.table.get_symbol(proc_PID, proc_head_lineno)["position"] + 1,
                           proc_PID + ": procedure return"))
        
        self.scope = ''
        self.scope_length = 0
        self.line_number += 1 # proc END
        
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