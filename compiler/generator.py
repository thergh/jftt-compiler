from sly import Parser
from lexer import MyLexer




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
            print(f"Error: {name} not in table.")
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
        
        
        
        
if __name__ == '__main__':
    st = SymbolTable()
    st.add_symbol('n1')
    st.add_symbol('n2')
    
    n = st.get_symbol('n1')

    st.display()
    st.find_name(1)
    
    
    # item = table['nazwa']