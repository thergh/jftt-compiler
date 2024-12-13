from sly import Lexer


class MyLexer(Lexer):
    
    tokens = {PROCEDURE, IS, BEGIN, END, PROGRAM, IF, THEN, ELSE, ENDIF,
              WHILE, DO, ENDWHILE, REPEAT, UNTIL, FOR, FROM, TO, ENDFOR,
              READ, WRITE, PID, NUM, T, NE, GE, LE, ASSIGN}
    
    literals = {'+', '-', '*', '/', '%', '=', '>', '<', '(', ')',
                '[', ']', ',', ';', ':'}
    
    PROCEDURE = r'PROCEDURE'
    IS = r'IS'
    BEGIN = r'BEGIN'
    END = r'END'
    PROGRAM = r'PROGRAM'
    IF = r'IF'
    THEN = r'THEN'
    ELSE = r'ELSE'
    ENDIF = r'ENDIF'
    WHILE = r'WHILE'
    DO = r'DO'
    ENDWHILE = r'ENDWHILE'
    REPEAT = r'REPEAT'
    UNTIL = r'UNTIL'
    FOR = r'FOR'
    FROM = r'FROM'
    TO = r'TO'
    ENDFOR = r'ENDFOR'
    READ = r'READ'
    WRITE = r'WRITE'
    T = r'T'    
    PID = r'[_a-z]+'
    NUM = r'0|[1-9]+[0-9]*'
    NE = r'!='
    GE = r'>='
    LE = r'<='
    ASSIGN = r':='
    
    
    
    
    ignore = ' \t'
    
    ignore_comment = r'\#.*' 
    
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += len(t.value)
        
    def error(self, t):
        print("Line %d: Wrong character %r '%s'" % (self.lineno, t.value[0]))
        self.index += 1
        
        
        
if __name__ == '__main__':
    
    lexer = MyLexer()
    
    with open('../examples/program0.imp', 'r') as file:
        data = file.read()
        
    for token in lexer.tokenize(data):
        print('type=%r, value=%r' % (token.type, token.value))