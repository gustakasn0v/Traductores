# -*- coding: utf-8 -*-
# Proyecto Traductores e Interpretadores. Entrega 1
# Realizado por:
# Wilmer Bandres. 1010055
# Gustavo El Khoury. 1010226
# -*- coding: utf-8 -*-
import ply.lex as lex
import sys

# Defino un diccionario para las palabras reservadas. Se usa en el metodo de 
# identificacion t_RESERVED

palabrasReservadas = {
  'program' : 'INST_PROGRAM',
  'declare' : 'INST_DECLARE',
  'begin'   : 'INST_BEGIN',
  'end'     : 'INST_END',
  'int'     : 'TYPEDEF_INT',
  'bool'    : 'TYPEDEF_BOOL',
  'range'   : 'TYPEDEF_RANGE',
  'read'    : 'INST_READ',
  'write'   : 'INST_WRITE',
  'writeln' : 'INST_WRITELN',
  'if'      : 'INST_IF',
  'then'    : 'INST_THEN',
  'else'    : 'INST_ELSE',
  'case'    : 'INST_CASE',
  'of'      : 'INST_OF',
  'for'     : 'INST_FOR',
  'in'      : 'INST_IN',
  'do'      : 'INST_DO',
  'while'   : 'INST_WHILE',
  'as'      : 'INST_AS',
  'or'      : 'OR',
  'and'     : 'AND',
  'not'     : 'NOT',
  'rtoi'	: 'RTOI',
  'length'  : 'LENGTH',
  'top'     : 'TOP',
  'bottom'  : 'BOTTOM'
}

# Defino formalmente los tokens como una lista, y le concateno el diccionario
tokens = ['NUMBER','MINUS','EQUAL','TIMES','DIVIDE','MOD','PLUS','GREAT','GREATEQ','LESS','LESSEQ','INTERSECTION',
          'RESERVED','RANGE','VAR_IDENTIFIER','COMMENT','COMMA','SEMICOLON','EQEQ','NEQEQ','IN','STRING','LPAREN','RPAREN','CASE_ASSIGN'] + list(palabrasReservadas.values());
          

# Estas son las formulas reconocedoras de tokens que solo necesiten una regexp
t_MINUS = r'\-'
t_EQUAL = r'='
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MOD = r'\%'
t_PLUS = r'\+'
t_GREAT = r'>'
t_GREATEQ = r'>='
t_LESS = r'<'
t_LESSEQ = r'<='
t_INTERSECTION = r'<>'
t_EQEQ = r'=='
t_NEQEQ = r'/='
t_IN = r'\>\>'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_RANGE = r'\.\.'
t_CASE_ASSIGN = r'\-\>'
t_ignore  = ' \t'


# A continuacion las formulas reconocedoras de tokens que requieran procedimientos

# Especificacion del token para numeros.
def t_NUMBER(t):
  r'\d+'
  t.value = int(t.value,)
  return t

# Especificacion del token que detecta saltos de linea
def t_newline(t):
  r'\n+'
  t.lexer.lineno += len(t.value)

# Especificacion del token que detecta comas
def t_COMMA(t):
  r','
  return t

# Especificacion del token que detecta punto y comas
def t_SEMICOLON(t):
  r';'
  return t

# Definicion del token para comentarios de rangeX
def t_COMMENT(t):
  r'//.*'
  
# Definicion del token que reconoce strings. Acepta comillas escapadas
def t_STRING(t):
  r'\"(\\n|\\\\|\\\"|[^\\\"])*\"'
  return t
  
# Calcula la columna donde esta ubicado un token
def find_column(input,token):
  ultimoSalto = input.rfind('\n',0,token.lexpos)
  if ultimoSalto < 0:
    ultimoSalto = 0
  column = (token.lexpos - ultimoSalto) + 1
  return column

#Especificacion del token para palabras reservadas del lenguaje
def t_RESERVED(t):
  r'[a-zA-Z_][a-zA-Z_0-9]*'
  t.type = palabrasReservadas.get(t.value,'VAR_IDENTIFIER')
  return t

#Definicion de errores para palabras no reconocidas
def t_error(t):
  print("Error: caracter inesperado " + t.value[0] + " en la linea " + str(t.lineno) + ", columna " + str(find_column(t.lexer.lexdata,t)-1)) 
  t.lexer.cl=1
  t.lexer.skip(1)
<<<<<<< HEAD

lexer = lex.lex()
  
#def main():
  #if (len(sys.argv) != 2):
    #print("Usage: python leyer.py nombreArchivo")
    #return -1
  
  ## Se abre el archivo con permisos de lectura
  #string = str(open(str(sys.argv[1]),'r').read())
  
  ## Se crea el lexer
  #lexer = lex.lex()
  
=======
 
lexer = lex.lex()
#def main():
  #if (len(sys.argv) != 2):
    #print("Usage: python leyer.py nombreArchivo")
    #return -1
  
  ## Se abre el archivo con permisos de lectura
  #string = str(open(str(sys.argv[1]),'r').read())
  
  ## Se crea el lexer
  #lexer = lex.lex()
  
>>>>>>> 92998fbc574078492127d8154076d94ff4002106
  ## Variable que determina si hubo un error procesando la entrada
  #lexer.cl = 0
  #lexer.input(string)
  #out=""
  #while 1:
    #mytoken = lexer.token()
    #if not mytoken:
      #break
    #out= out + str(mytoken.type)
    
    ## Se colocan los nombres de variables entre < y >
    #if (str(mytoken.type) == "VAR_IDENTIFIER"):
      #out += " < "+ str(mytoken.value) + " > " 
    #out += " (Linea " + str(mytoken.lineno) + ", Columna " + str(find_column(lexer.lexdata,mytoken)-1) + ')\n'
      
  #if (lexer.cl!=1):
    #lexer.cl=0
    #print(out),

#if __name__ == '__main__':
  #main()