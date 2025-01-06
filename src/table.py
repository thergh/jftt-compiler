

class SymbolTable:
    def __init__(self):
        self.table = {}
        self.mem_pos = 100
        # mem slot 0: accumulator
        # 1-9 slots for code generation
        # 10-19 slots for utility functions
        # 100+ memory
    
    
    def add_symbol(self, name):
        if name in self.table:
            print(f"Error: {name} already exists.")
            return
        
        self.table[name] = {
            'position': self.mem_pos,
            'is_array': False,
            'start_idx': 0,
            'end_idx': 0,
            'assigned': False,
            'is_reference': False
        }
        
        self.mem_pos += 1
        
        
    def add_array(self, name, start_idx, end_idx):
        if name in self.table:
            print(f"Error: {name} already exists.")
            return
        
        if end_idx < start_idx:
            print(f"Error: start_idx: {start_idx} bigger than end_idx: {end_idx}")
            return
        
        length = int(end_idx) - int(start_idx)
        
        self.table[name] = {
            'position': self.mem_pos,
            'is_array': True,
            'start_idx': start_idx,
            'end_idx': end_idx,
            'assigned': False,
            'is_reference': False
        }
        
        self.mem_pos += length + 1
        
    
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
            'is_reference': True
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
            'is_reference': True
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
            'assigned': False,
            'is_reference': False,
            'arguments': arguments
        }
        
        self.mem_pos += 1

        self.add_symbol(name + "_rtrn")
        
        
    def mark_assigned(self, name, line_number=-1):
        self.table[name]["assigned"] = True