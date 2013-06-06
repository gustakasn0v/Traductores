# -*- coding: utf-8 -*-
# Proyecto Traductores e Interpretadores. Entrega 2
# Realizado por:
# Wilmer Bandres. 1010055
# Gustavo El Khoury. 1010226
# -*- coding: utf-8 -*-

import ply.yacc as yacc
import ply.lex as lex
from lexer import tokens

class bloque:
  def __init__(self,nombre,contenido):
    self.nombre = nombre
    self.contenido = contenido
    
  def printArbol(self,indent):
    print self.nombre
    self.contenido.printArbol()
    
class bloqueDeclaracion:
  def __init__(self,listaDeclaraciones):
    # Esta es una lista de cada linea del declare
    self.listaDeclaraciones = listaDeclaraciones
    
  def printArbol(indent):
    print('DECLARACION:')
    
class unaDeclaracion:
  def __init__(self,listaVariables,tipo):
    self.listaVariables = listaVariables
    self.tipo = tipo
    
  def printArbol(self,indent):
    None

class listaVariables:
  def __init__(self,lista):
    self.lista = lista
    
  def printArbol(self):
    None
    
class listaInstrucciones:
  def __init__(self,listaInst):
    self.listaInst = listaInst
    
  def printArbol(self):
    None
   
def p_program(p):
    'program : INST_PROGRAM Bloque_Inst'
    p[0] = p[2]
    #print p
    
def p_Bloque_Inst(p):
    '''Bloque_Inst : INST_BEGIN Lista_Inst INST_END
    | Inst'''
    if p[1]=='begin':
      p[0] = bloque('BLOQUE',p[2])
    else:
      p[0] = bloque('UNICA INSTRUCCION',p[1])

def p_Lista_Inst(p):
    '''Lista_Inst : Inst 
    | Inst SEMICOLON Lista_Inst'''
    if(len(p)>=3):
      p[0] = listaInstrucciones( [ p[3] ].insert(0,p[1]) )
    else:
      p[0] = listaInstrucciones([p[1]])

def p_Inst(p):
  '''Inst : Inst_Declare 
  | Inst_Asignacion
  | Inst_Lectura 
  | Inst_For 
  | Inst_While
  | Inst_If 
  | Inst_Case '''
  #| Inst_Salida
  p[0] = p[1]


def p_Inst_Declare(p):
  '''Inst_Declare : INST_DECLARE Lista_Declare'''
  p[0] = bloqueDeclaracion(p[2])
  
def p_Lista_Declare(p):
  '''Lista_Declare : Lista_Variables INST_AS Tipo'''
  p[0] = unaDeclaracion(p[1],p[3])
  
def p_Lista_Variables(p):
  '''Lista_Variables : VAR_IDENTIFIER
  | VAR_IDENTIFIER COMMA Lista_Variables '''
  
  if(len(p)>=3):
    p[0] = [ p[3] ].insert(0,p[1])
  else:
    p[0] = listaVariables([p[1]])
  
def p_Tipo(p):
  ''' Tipo : TYPEDEF_INT 
  | TYPEDEF_BOOL 
  | TYPEDEF_RANGE '''
  p[0] = 'de tipo ' + p[1]
  
def p_Inst_Asignacion(p):
  '''Inst_Asignacion : VAR_IDENTIFIER EQUAL Expresion'''
  p[0] = p[1] + ' ' + p[2] + ' ' + p[3]


precedence = (
	('left', 'OR'),
	('left', 'AND'),
	('nonassoc', 'EQEQ' ,'NEQEQ','LESS','LESSEQ' ,'GREAT','GREATEQ'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
) 


class Operacion:
	def __init__(self,left,opr,right):
		this.left = left
		this.opr = opr
		this.right = right
	def printOperacion(self):
		print "Operacion binaria:\n" + "Operador: " + this.opr + "\n" + "Operando izquierdo: " + this.left + "\nOperador Derecho: " + this.right + "\n"
	
  
def p_Expresion(p):
  '''Expresion : Operacion_binaria
  | Operacion_booleana 
  | Rango'''
  p[0] = p[1]

def p_Operacion_booleana(p):
  ''' Operacion_booleana : Operacion_binaria Opr_bool Operacion_binaria
  | Operacion_binaria Opr_bool Operacion_booleana
  | Operacion_booleana Opr_bool Operacion_binaria
  | Operacion_booleana Opr_bool Operacion_booleana 
  | 't'
  | 'f' '''

  if len(p)>=3:
	  p[0] = Operacion(p[1],p[2],p[3])
  else: 
	  p[0] = p[1]

def p_Opr_bool(p):
  ''' Opr_bool : OR
  | AND
  | EQEQ
  | NEQEQ
  | GREAT
  | LESS
  | GREATEQ
  | LESSEQ '''
  p[0] = p[1]

def p_Operacion_binaria(p):
  ''' Operacion_binaria : Operacion_binaria PLUS Term
  | Operacion_binaria MINUS Term
  | Term'''	
  if len(p) >= 3:
	  p[0] = Operacion(p[1],p[2],p[3])
  else:
	  p[0] = p[1]

def p_Term(p):
  '''Term : Term TIMES Factor
  | Term DIVIDE Factor
  | Factor'''
  if len(p) >=3:
	  p[0] = Operacion(p[1],p[2],p[3])
  else:
	  p[0] = p[1]

def p_Factor(p):
  ''' Factor : NUMBER
  | VAR_IDENTIFIER
  | LPAREN Operacion_binaria RPAREN '''
  if len(p)>=3:
	  p[0] = p[2]
  else:
	  p[0] = p[1]

def p_Rango(p):
  ''' Rango : Operacion_binaria RANGE Operacion_binaria
  | Rango PLUS Rango
  | Rango TIMES Operacion_binaria
  | Rango INTERSECTION Rango 
  | RangoF'''
  if len(p)>=3:
	  p[0] = Operacion(p[1],p[2],p[3])
  else:
	  p[0] = p[1]

def p_RangoF(p):
  ''' RangoF : LPAREN Rango RPAREN'''
  p[0] = p[2]

  
def p_Inst_Lectura(p):
  '''Inst_Lectura : INST_READ VAR_IDENTIFIER'''
  p[0] = 'READ:' + '\n' + '\t\t' + p[2]
 
  
#def p_Inst_Salida(p):
  #'''Inst_Salida : '''

class ifc:
	def __init__(self,cond,bloque,bloque2=""):
		this.cond = cond
		this.bloque = bloque
		this.bloque2 = bloque2

def p_Inst_If(p):
  '''Inst_If : INST_IF Operacion_booleana INST_THEN Bloque_Inst 
  | INST_IF Operacion_booleana INST_THEN Bloque_Inst INST_ELSE Bloque_Inst'''
  if len(p)>=6:
	  p[0] = ifc(p[2],p[4],p[6])
  else:
	  p[0] = ifc(p[2], p[4])
  


def p_Inst_Case(p):
  '''Inst_Case : INST_CASE Operacion_binaria INST_OF Casos '''

def p_Casos(p):
  ''' Casos : VAR_IDENTIFIER '-' '>' Bloque_Inst 
  | Rango '-' '>' Bloque_Inst 
  | Casos Casos'''

class forc:
	def __init__(self,var,rango,inst):
		this.var = var
		this.rango = rango
		this.inst = inst

def p_Inst_For(p):
  '''Inst_For : INST_FOR VAR_IDENTIFIER INST_IN Rango INST_DO Bloque_Inst '''
  p[0] = forc(p[2],p[4],p[6])

class whilec:
	def __init__(self,cond,inst):
		this.cond = cond
		this.inst = inst

def p_Inst_While(p):
  '''Inst_While : INST_WHILE Operacion_booleana INST_DO Bloque_Inst '''
  p[0] = whilec(p[2],p[4])

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


    
