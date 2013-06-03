# Proyecto Traductores e Interpretadores. Entrega 2
# Realizado por:
# Wilmer Bandres. 1010055
# Gustavo El Khoury. 1010226
# -*- coding: utf-8 -*-

import ply.yacc as yacc
from lexer import tokens


def p_program(p):
    'program : INST_PROGRAM VAR_IDENTIFIER SEMICOLON'
    p[0] = p[1] + p[2] + p[3]
    #print p
    

def p_error(p):
    print "Syntax error in input!"

# Build the parser
parser = yacc.yacc()

while True:
    
   #try:
   #    s = raw_input('calc > ')
   #except EOFError:
   #    break
   #if not s: continue
   string = str(open('prueba1.txt','r').read())
   print string
   
   result = parser.parse(string)
   print result


    