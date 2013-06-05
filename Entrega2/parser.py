# -*- coding: utf-8 -*-
# Proyecto Traductores e Interpretadores. Entrega 2
# Realizado por:
# Wilmer Bandres. 1010055
# Gustavo El Khoury. 1010226
# -*- coding: utf-8 -*-

import ply.yacc as yacc
import ply.lex as lex
from lexer import tokens

indentation = '\t'

def p_program(p):
    'program : INST_PROGRAM Bloque_Inst'
    p[0] = p[2]
    #print p
    
def p_Bloque_Inst(p):
    '''Bloque_Inst : INST_BEGIN Lista_Inst INST_END
    | Inst'''
    if p[1]=='begin':
      global indentation
      indentation = indentation + "\t"
      p[0] = 'BLOQUE' + '\n' + p[2]
    else:
      p[0] = p[1]

def p_Lista_Inst(p):
    '''Lista_Inst : Inst 
    | Inst SEMICOLON Lista_Inst'''
    if(len(p)>=3):
      p[0] = indentation + p[1]  + p[3]
    else:
      p[0] = indentation + p[1]

def p_Inst(p):
  '''Inst : Inst_Declare 
  | Inst_Asignacion'''
  #| Inst_Lectura
  #| Inst_Salida
  #| Inst_If 
  #| Inst_Case 
  #| Inst_For 
  #| Inst_While'''
  p[0] = indentation + p[1]


def p_Inst_Declare(p):
  '''Inst_Declare : INST_DECLARE Lista_Declare'''
  p[0] = p[1] + ' ' + p[2] + '\n'
  
def p_Lista_Declare(p):
  '''Lista_Declare : Lista_Variables INST_AS Tipo'''
  p[0] = p[1] + ' ' + p[3]
  
def p_Lista_Variables(p):
  '''Lista_Variables : VAR_IDENTIFIER
  | VAR_IDENTIFIER COMMA Lista_Variables '''
  
  if(len(p)>=3):
    p[0] = p[1] + ' ' + p[2] + ' ' + p[3]
  else:
    p[0] = p[1]
  
def p_Tipo(p):
  ''' Tipo : TYPEDEF_INT 
  | TYPEDEF_BOOL 
  | TYPEDEF_RANGE '''
  p[0] = 'de tipo ' + p[1]
  
def p_Inst_Asignacion(p):
  '''Inst_Asignacion : VAR_IDENTIFIER EQUAL Expresion'''
  p[0] = p[1] + ' ' + p[2] + ' ' + p[3]
  
def p_Expresion(p):
  '''Expresion : Expresion_Bool
  | Expresion_Aritm
  | Rango'''
  p[0] = p[1]
  
def p_Expresion_Bool(p):
  '''Expresion_Bool : SEMICOLON '''
  
def p_Expresion_Aritm(p):
  '''Expresion_Aritm : SEMICOLON '''

def p_Rango(p):
  '''Rango : SEMICOLON '''
  
#def p_Inst_Lectura(p):
 # '''Inst_Lectura : INST_READ VAR_IDENTIFIER'''
  
#def p_Inst_Salida(p):
  #'''Inst_Salida : '''

#def p_Inst_If(p):
  #'''Inst_If : '''

#def p_Inst_Case(p):
  #'''Inst_Case : '''

#def p_Inst_For(p):
  #'''Inst_For : '''

#def p_Inst_While(p):
  #'''Inst_While : '''

def p_error(p):
    print "Syntax error in input!"

# Build the parser
parser = yacc.yacc()

s = str(open(str('entrada.txt'),'r').read())
#while True:
    
   #try:
      #s = raw_input('calc > ')
   #except EOFError:
      #break
   #if not s: continue
result = parser.parse(s)
print result


    