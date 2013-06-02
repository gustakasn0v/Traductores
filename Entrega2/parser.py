# Proyecto Traductores e Interpretadores. Entrega 2
# Realizado por:
# Wilmer Bandres. 1010055
# Gustavo El Khoury. 1010226
# -*- coding: utf-8 -*-

import ply.yacc as yacc
from lexer import tokens

def p_program_structure(p):
    'programa : INST_PROGRAM2 VAR_IDENTIFIER; '
    
    yacc.yacc()
    