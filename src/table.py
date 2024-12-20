

class SymbolTable:
    def __init__(self):
        self.table = {}
        self.mem_pos = 100
        # mem slot 0: accumulator
        # mem slot 1: printing values
    
    
    def add_symbol(self, name):
        if name in self.table:
            print(f"Error: {name} already exists.")
            return
        
        self.table[name] = {
            'position': self.mem_pos,
            'is_array': False,
            'start_idx': 0,
            'end_idx': 0
        }
        
        self.mem_pos += 1
        
        
    def add_array(self, name, start_idx, end_idx):
        if name in self.table:
            print(f"Error: {name} already exists.")
            return
        
        if end_idx < start_idx:
            print(f"Error: start_idx bigger than end_idx: {start_idx} > {end_idx}")
            return
        
        length = int(end_idx) - int(start_idx)
        
        self.table[name] = {
            'position': self.mem_pos,
            'is_array': True,
            'start_idx': start_idx,
            'end_idx': end_idx
        }
        
        self.mem_pos += length + 1
        
    
    def get_symbol(self, name):
        if name not in self.table:
            print(f"\nError: {name} not in table.")
            return      
        return self.table[name]  
        
        
    def display(self):
        for x in self.table:
            print(f"{x}: {self.table[x]}")
        
        
    def find_name(self, position):
        for x in self.table:
            if self.table[x]['position'] == position:
                return x