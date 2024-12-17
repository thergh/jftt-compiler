

class SymbolTable:
    def __init__(self):
        self.table = {}
        self.memory_offset = 0
    
    
    def add_symbol(self, name, is_array=False, is_assigned=False):
        if name in self.table:
            print(f"Error: {name} already exists.")
            return
        self.table[name] = {
            'offset': self.memory_offset,
            'is_array': is_array,
            'is_assigned' : is_assigned
        }
        self.memory_offset += 1
        
    
    def get_symbol(self, name):
        if name not in self.table:
            print(f"\nError: {name} not in table.")
            return      
        return self.table[name]  
        
        
    def display(self):
        for x in self.table:
            print(self.table[x])
        # for name, attributes in name_table.table.items():
        
        
    def find_name(self, offset):
        for x in self.table:
            if self.table[x]['offset'] == offset:
                return x