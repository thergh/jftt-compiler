

class SymbolTable:
    def __init__(self):
        self.table = {}
        self.memory_idx = 100
        # mem slot 0: accumulator
        # mem slot 1: printing values
    
    
    def add_symbol(self, name, is_array=False, is_assigned=False):
        if name in self.table:
            print(f"Error: {name} already exists.")
            return
        self.table[name] = {
            'idx': self.memory_idx,
            'is_array': is_array,
            'is_assigned' : is_assigned
        }
        self.memory_idx += 1
        
    
    def get_symbol(self, name):
        if name not in self.table:
            print(f"\nError: {name} not in table.")
            return      
        return self.table[name]  
        
        
    def display(self):
        for x in self.table:
            print(f"{x}: {self.table[x]}")
        
        
    def find_name(self, idx):
        for x in self.table:
            if self.table[x]['idx'] == idx:
                return x