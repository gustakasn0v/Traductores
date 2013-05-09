# -*- coding: utf-8 -*-
import ply.lex as lex
#import re

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
tokens = ['NUMBER','MINUS','EQUAL','TIMES','DIVIDE','MOD','PLUS','GREAT','GREATEQ','LESS','LESSEQ','INTERSECTION',
          'RESERVED','RANGE','VAR_IDENTIFIER','COMMENT','COMMA','SEMICOLON','EQEQ','NEQEQ','IN','STRING','LPAREN','RPAREN'] + list(palabrasReservadas.values());
          

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
t_ignore  = ' \t'


# A continuacion las formulas reconocedoras de tokens que requieran procedimientos

#Especificacion del token para numeros.
def t_NUMBER(t):
  r'\d+'
  t.value = int(t.value,)
  return t

# Define a rule so we can track line numbers
def t_newline(t):
  r'\n+'
  t.lexer.lineno = len(t.value)

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



def t_STRING(t):
  r'\"(\\n|\\\\|\\\"|[^\\\"])*\"'

  
  return t
  
# Calcula la columna donde esta ubicado un token
def find_column(input,token):
  last_cr = input.rfind('\n',0,token.lexpos)
  if last_cr < 0:
    last_cr = 0
  column = (token.lexpos - last_cr) + 1
  return column

# Define a rule so we can track line numbers
#def t_newline(t):
#  r'\n+'
#  t.lexer.lineno = len(t.value)

#Especificacion del token para palabras reservadas del lenguaje
def t_RESERVED(t):
  r'[a-zA-Z_][a-zA-Z_0-9]*'
  t.type = palabrasReservadas.get(t.value,'VAR_IDENTIFIER')
  return t



#Definicion de errores para palabras no reconocidas
def t_error(t):
  print("Error: caracter inesperado " + t.value[0] + " en tus nalgas"),
  t.lexer.skip(1)

string = str(open('c2.rgx','r').read())
print(string)
lexer = lex.lex()
lexer.input(string)
while 1:
  mytoken = lexer.token()
  if not mytoken:
    break

