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
}

# Defino formalmente los tokens como una lista
tokens = ['NUMBER','MINUS','EQUAL','PLUS','GREAT','GREATEQ','LESS','LESSEQ',
          'RESERVED','VAR_IDENTIFIER'] + list(palabrasReservadas.values());
          

# Estas son las formulas reconocedoras de tokens que solo necesiten una regexp
t_MINUS = r'\-'
t_EQUAL = r'\='
t_PLUS = r'\+'
t_GREAT = r'\>'
t_GREATEQ = r'\>='
t_LESS = r'\<'
t_LESSEQ = r'\<='
t_ignore  = ' \t \n'


# A continuacion las formulas reconocedoras de tokens que requieran procedimientos

#Especificacion del token para numeros.
def t_NUMBER(t):
  r'\d+'
  t.value = int(t.value,)
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
  string = "program pedro begin declare hola end"
  lexer.input(string)
  while 1:
    mytoken = lexer.token()
    if not mytoken:
      break
    print "El nombre es " + mytoken.type + " y el contenido es " + str(mytoken.value)
    

if __name__ == "__main__":
  main()