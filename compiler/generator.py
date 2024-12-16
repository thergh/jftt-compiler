from parser import MyParser
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
        
        
        
class CodeGenerator:
    def __init__(self, program, debug=False):
        self.program = program
        self.debug = debug
        self.procedures = program[1]
        self.main = program[2]
        
        if self.debug:
            print("\nprocedures: ", self.procedures)
            print("\nmain: ", self.main)
        
        
    
    def generate_code(self):
        # declarations will be 
        declarations = self.get_declarations()
    
    
    
    def get_declarations(self):
        """ Gets declarations from program
        and returns them in the recursive form """
        
        if self.debug:
            print("\nmain[0]: ", self.main[0])
            
        if self.main[0] != 'mn=LONG': # program has no declarations
            if self.debug:
                    print("Program has no declarations")
            return None
        
        declarations = self.main[1]    
        if self.debug:
            print("\ndeclarations: ", declarations)
            
        return declarations
    
    
    # def extract_decs(self, decs):
    #     """ Changes declarations from
    #     recursive form to a list """
        
        
        

    
    
    def group_commands(self, commands):
        comm_list = []
        comm_list.append(commands[1]) 
        if commands[0] == 'comms=SINGLE':        
            return comm_list
        
        else:
            comm_list.append(self.group_commands(commands[1]))
            return comm_list




if __name__ == '__main__':
    lexer = MyLexer()
    parser = MyParser()

    with open('examples/program0.imp', 'r') as file:
        data = file.read()
        
    tokens = lexer.tokenize(data)
    
    parsed = parser.parse(tokens)
    
    
    gen = CodeGenerator(parsed, True)
    gen.get_declarations()
    
    # print(result)