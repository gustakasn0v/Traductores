import ply.lex as lex

tokens = ('NUMBER','MINUS','EQUAL');
def t_NUMBER(t):
	r'\d+'
	t.value = int(t.value)
	return t

t_MINUS = r'\-'
t_EQUAL = r'\='
t_ignore  = ' \t'

def t_error(t):
	print("Illegal expression")
	t.lexer.skip(1)
	
lexer = lex.lex()

def main():
	a = 2
	string = "1-2"
	lexer.input(string)
	while 1:
		mytoken = lexer.token()
		if not mytoken:
			break
		print(mytoken.value)

if __name__ == "__main__":
    main()
    
