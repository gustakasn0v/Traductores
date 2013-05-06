# -*- coding: utf-8 -*-
import ply.lex as lex


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
  'while'   : 'INST_while',
  'or'      : 'OR',
  'and'     : 'AND',
  'not'     : 'NOT'
}

# Defino formalmente los tokens como una lista
tokens = ['NUMBER','MINUS','EQUAL','PLUS','GREAT','GREATEQ','LESS','LESSEQ','INTERSECTION',
          'RESERVED','VAR_IDENTIFIER','COMMENT','COMMA','SEMICOLON','EQEQ','NEQEQ','IN','STRING','LPAREN','RPAREN'] + list(palabrasReservadas.values());
          

# Estas son las formulas reconocedoras de tokens que solo necesiten una regexp
t_MINUS = r'\-'
t_EQUAL = r'='
t_PLUS = r'\+'
t_GREAT = r'>'
t_GREATEQ = r'>='
t_LESS = r'<'
t_LESSEQ = r'<='
t_INTERSECTION = r'<>'
t_EQEQ = r'=='
t_NEQEQ = r'/='
t_IN = r'\>\>'
#t_STRING = r'\"([^\"\\]|(\\\")|((\\)n)|(\\))*\"'
t_STRING = r'\"[^\"]*[^\\]\"'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_ignore  = ' \t \n'


# A continuacion las formulas reconocedoras de tokens que requieran procedimientos

#Especificacion del token para numeros.
def t_NUMBER(t):
  r'\d+'
  t.value = int(t.value,)
  return t

def t_COMMA(t):
  r','
  return t

def t_SEMICOLON(t):
  r';'
  return t

#Definicion de una expresion regular para comentarios de rangeX
def t_COMMENT(t):
  r'//.*'
  return t


#Especificacion del token para palabras reservadas del lenguaje
def t_RESERVED(t):
  r'[a-zA-Z_][a-zA-Z_0-9]*'
  t.type = palabrasReservadas.get(t.value,'VAR_IDENTIFIER')
  return t



#Definicion de errores para palabras no reconocidas
def t_error(t):
  print("Illegal expression")
  t.lexer.skip(1)
	
	
lexer = lex.lex()

def main():
  a = 2
  string = '''program begin declare a,b,c as range \n a = a >> b  \n write("hola")  \n ///esto es , comentario \n a/=b end \n
"hola esto \\" es" \n es"'''
  print string

  lexer.input(string)
  while 1:
    mytoken = lexer.token()
    if not mytoken:
      break
    #print "El nombre es " + mytoken.type + " y el contenido es " + str(mytoken.value)
    print mytoken

if __name__ == "__main__":
  main()
