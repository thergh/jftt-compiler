

class SymbolTable:
    def __init__(self):
        self.table = {}
        self.mem_pos = 100
        # mem slot 0: accumulator
        # 1-9 slots for code generation
        # 10-19 slots for utility functions
        # 100+ memory
    
    
    def add_symbol(self, name, lineno=-1):
        if name in self.table:
            print(f"\nError in line {lineno}: {name} redeclaration.\n")
            return
        
        self.table[name] = {
            'position': self.mem_pos,
            'is_array': False,
            'start_idx': 0,
            'end_idx': 0,
            'assigned': False,
            'is_reference': False,
            'is_iterator': False
        }
        
        self.mem_pos += 1
        
        
    def add_array(self, name, start_idx, end_idx, lineno=-1):
        if name in self.table:
            print(f"\nError in line {lineno}: {name} redeclaration.\n")
            return
        
        start_idx = int(start_idx)
        end_idx = int(end_idx)
        
        
        if end_idx < start_idx:
            print(f"\nError in line {lineno}: start_idx ({start_idx}) bigger than end_idx ({end_idx})\n")
            return
        
        # length = int(end_idx) - int(start_idx)
        
        if int(start_idx) < 0 or int(end_idx) < 0:
            length = abs(int(start_idx)) + abs(int(end_idx)) + 1
        else:
            length = end_idx + 1
        
        
        if start_idx < 0:
            self.table[name] = {
                'position': self.mem_pos + abs(start_idx),
                'is_array': True,
                'start_idx': start_idx,
                'end_idx': end_idx,
                'assigned': False,
                'is_reference': False,
                'is_iterator': False
            }
            
        else:
            self.table[name] = {
                'position': self.mem_pos,
                'is_array': True,
                'start_idx': start_idx,
                'end_idx': end_idx,
                'assigned': False,
                'is_reference': False,
                'is_iterator': False
            }
        
        self.mem_pos += length + 1
        
        
    def add_symbol_ref(self, name, line_number=-1):
        if name in self.table:
            print(f"\nError in line {line_number}: {name} redeclaration.\n")
            return
        
        self.table[name] = {
            'position': self.mem_pos,
            'is_array': False,
            'start_idx': 0,
            'end_idx': 0,
            'assigned': True, # i treat references as assigned
            'is_reference': True,
            'is_iterator': False
        }
        
        self.mem_pos += 1
        
        
    def add_array_ref(self, name, line_number=-1):
        if name in self.table:
            print(f"\nError in line {line_number}: {name} redeclaration.\n")
            return

        self.table[name] = {
            'position': self.mem_pos,
            'is_array': True,
            'start_idx': 0,
            'end_idx': 0,
            'assigned': True, # i treat references as assigned
            'is_reference': True,
            'is_iterator': False
        }
        
        self.mem_pos += 1
        
    
    def add_procedure(self, name, arguments, line_number=-1):
        if name in self.table:
            print(f"\nError in line {line_number}: {name} redeclaration.\n")
            return
        
        self.table[name] = {
            'position': self.mem_pos,
            'is_array': False,
            'start_idx': 0,
            'end_idx': 0,
            'assigned': True,
            'is_reference': False,
            'arguments': arguments,
            'is_iterator': False
        }
        
        self.mem_pos += 1

        self.add_symbol(name + "_rtrn")
        
        
    def add_iterator(self, name, lineno=-1):
        if name in self.table:
            # I allow iterator redeclaration,
            # it will jsut overwrite the previous one
            self.table[name]["assigned"] = True
            return
        
        self.table[name] = {
            'position': self.mem_pos,
            'is_array': False,
            'start_idx': 0,
            'end_idx': 0,
            'assigned': True,
            'is_reference': False,
            'is_iterator': True
        }
        
        self.mem_pos += 1
        
    
    def get_symbol(self, name, line_number=-1):
        if name not in self.table:
            print(f"\nError in line {line_number}: {name} not declared.\n")
            return      
        return self.table[name]  
        
        
    def display(self):
        for x in self.table:
            print(f"{x}: {self.table[x]}")
        
        
    def find_name(self, position):
        for x in self.table:
            if self.table[x]['position'] == position:
                return x
 
        
    def mark_assigned(self, name, line_number=-1):
        self.table[name]["assigned"] = True