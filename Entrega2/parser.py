# -*- coding: utf-8 -*-
# Proyecto Traductores e Interpretadores. Entrega 2
# Realizado por:
# Wilmer Bandres. 1010055
# Gustavo El Khoury. 1010226
# -*- coding: utf-8 -*-

import ply.yacc as yacc
import ply.lex as lex
from lexer import tokens

   
def p_program(p):
    'program : INST_PROGRAM Bloque_Inst'
    p[0] = p[2]
    

class bloque:
  def __init__(self,nombre,contenido):
    self.nombre = nombre
    self.contenido = contenido
    
  def printArbol(self):
    print self.nombre
    self.contenido.printArbol()
    
    
def p_Bloque_Inst(p):
    '''Bloque_Inst : INST_BEGIN Lista_Inst INST_END
    | Inst'''
    if p[1]=='begin':
      p[0] = bloque('BLOQUE',p[2])
    else:
      p[0] = bloque('UNICA INSTRUCCION',p[1])
    


class listaInstrucciones:
  def __init__(self,listaInst):
    self.listaInst = listaInst
    
  def printArbol(self):
    for i in self.listaInst:
      i.printArbol()

class String:
  def __init__(self,cadena):
    self.cad = cadena
  
  def printArbol(self):
    print self.cad	
      
def p_Lista_Inst(p):
    '''Lista_Inst : Inst 
    | Inst SEMICOLON Lista_Inst'''
    if(len(p)>=3):
      p[3].listaInst.insert(0,String("\nSERPARADOR\n"))
      p[3].listaInst.insert(0,p[1])
      p[0] = listaInstrucciones( p[3].listaInst )
      
    else:
      p[0] = listaInstrucciones([p[1]])
      
def p_Inst(p):
  '''Inst : Inst_Declare 
  | Inst_Asignacion
  | Inst_Lectura 
  | Inst_For 
  | Inst_While
  | Inst_If 
  | Inst_Case 
  | Inst_Salida
  | Inst_Funcion '''
  p[0] = p[1]
  

class InstFuncion:
  def __init__(self,func,var):
    self.funcion = func
    self.var = var
  def printArbol(self):
    print "Funcion: " + self.funcion + "\n\tVariable: " + self.var
    
def p_Inst_Funcion(p):
  ''' Inst_Funcion : RTOI LPAREN VAR_IDENTIFIER RPAREN 
  | LENGTH LPAREN VAR_IDENTIFIER RPAREN
  | TOP LPAREN VAR_IDENTIFIER RPAREN
  | BOTTOM LPAREN VAR_IDENTIFIER RPAREN '''
  
  p[0] = InstFuncion(p[1],p[3])
  
class bloqueDeclaracion:
  def __init__(self,listaDeclaraciones):
    # Esta es una lista de cada linea del declare
    self.listaDeclaraciones = listaDeclaraciones
    
  def printArbol(self):
    print('DECLARACION:')
    for i in self.listaDeclaraciones:
      i.printArbol()

def p_Inst_Declare(p):
  '''Inst_Declare : Inst_Declareau
  | Inst_Declareau SEMICOLON Inst_Declare'''
  if len(p)>=3:
    p[3].listaDeclaraciones.insert(0,p[1])
    p[0] = bloqueDeclaracion(p[3].listaDeclaraciones)
  else:
    p[0]=bloqueDeclaracion([p[1]])
    
    
def p_Inst_Declareau(p):
  '''Inst_Declareau : INST_DECLARE Lista_Declare'''
  p[0] = p[2]
  

class unaDeclaracion:
  def __init__(self,listaVariables,tipo):
    self.listaVariables = listaVariables
    self.tipo = tipo
    
  def printArbol(self):
   print "\tVariables: ",
   self.listaVariables.printArbol()
   print "declaradas como " + self.tipo

  
def p_Lista_Declare(p):
  '''Lista_Declare : Lista_Variables INST_AS Tipo'''
  p[0] = unaDeclaracion(p[1],p[3])
  

class listaVariables:
  def __init__(self,lista):
    self.lista = lista
    
  def printArbol(self):
    for i in self.lista:
      print i +",",
    

def p_Lista_Variables(p):
  '''Lista_Variables : VAR_IDENTIFIER
  | VAR_IDENTIFIER COMMA Lista_Variables '''
  
  if(len(p)>=3):
    p[3].lista.insert(0,p[1])
    p[0] = listaVariables( p[3].lista)
  else:
    p[0] = listaVariables([p[1]])
  
def p_Tipo(p):
  ''' Tipo : TYPEDEF_INT 
  | TYPEDEF_BOOL 
  | TYPEDEF_RANGE '''
  p[0] =  p[1]

class Asignacion:
  def __init__(self,variable,expresion):
    self.variable = variable
    self.expresion = expresion
  
  def printArbol(self):
    print "A la variable: " + str(self.variable) + " se le asigna ",
    self.expresion.printArbol()
    
def p_Inst_Asignacion(p):
  '''Inst_Asignacion : VAR_IDENTIFIER EQUAL Expresion'''
  p[0] = Asignacion(p[1],p[3])


precedence = (
    ('right','INST_ELSE'),
    ('left','INTERSECTION'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('nonassoc', 'NOT'),
    ('nonassoc', 'EQEQ' ,'NEQEQ','LESS','LESSEQ' ,'GREAT','GREATEQ'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('nonassoc', 'RANGE'),
) 


class Operacion:
  def __init__(self,left,opr="",right=""):
    self.left = left
    self.opr = opr
    self.right = right
  def printArbol(self):
    if self.right!="":
      print "Operacion binaria:\n" + "Operador: " + self.opr + "\n" + "Operando izquierdo: "
      self.left.printArbol()
      print "\nOperando Derecho: ",
      self.right.printArbol()
    elif self.opr!="":
      print "Operacion unaria:\n" + "Operador: " + self.opr + "\n" + "Operando: "
      self.left.printArbol()
    else:
      print self.left
  
  
def p_Expresion(p):
  '''Expresion : Operacion_binaria
  | Operacion_booleana 
  | Rango'''
  p[0] = p[1]

  
def p_Operacion_booleana(p):
  ''' Operacion_booleana : Operacion_binaria Opr_bool Operacion_binaria
  | Operacion_booleana AND Operacion_booleana 
  | Operacion_booleana OR Operacion_booleana 
  | LPAREN Operacion_booleana RPAREN
  | TRUE
  | FALSE
  | VAR_IDENTIFIER
  | NOT Operacion_booleana '''

  if len(p)>=3:
    if p[1]!='(' and p[1]!="not":
      p[0] = Operacion(p[1],p[2],p[3])
    elif p[1]=="not":
      p[0] = Operacion(p[2],p[1])
    else:
      p[0]=p[2]
  else: 
    p[0] = Operacion(p[1])

	  
def p_Opr_bool(p):
  ''' Opr_bool : EQEQ
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
	  p[0] = Operacion(p[1])

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


class Lectura:
  def __init__(self,var):
    self.variable = var
  
  def printArbol(self):
    print "Read de la variable: " + self.variable
    
  
def p_Inst_Lectura(p):
  '''Inst_Lectura : INST_READ VAR_IDENTIFIER '''
  p[0] = Lectura(p[2])
  
  
class Salida:
  def __init__(self,tipow,lista):
    self.tipo = tipow
    self.lista = lista
  
  def printArbol(self):
    print self.tipo + "\n"
    for i in self.lista:
      print "Expresion: ",
      print i.tipo
      
      if i.tipo=="Variable":
	print "Nombre: ",
      else:
	print "Valor: "
      i.printArbol()
      print ""

      
#Esta clase se usa para facilitar el write
class Aux:
  def __init__(self,tipo,valor):
    self.val = valor
    self.tipo = tipo
    
  def printArbol(self):
    self.val.printArbol()


    
def p_Inst_Salida(p):
  '''Inst_Salida : INST_WRITE Lista_Aux
  | INST_WRITELN  Lista_Aux '''
  if p[1]=="write":
    p[1]="WRITE"
  else:
    p[1]="WRITELN"
  p[0] = Salida(p[1],p[2])

  
def p_Lista_Aux(p):
  '''Lista_Aux : Expresion
  | STRING 
  | Expresion COMMA Lista_Aux
  | STRING COMMA Lista_Aux '''
  print p[1]
  if(len(p)>=3):
    if isinstance(p[1],Operacion):
      p[3].insert(0,Aux("Variable",p[1]))
    else:
      p[3].insert(0,Aux("Cadena",String(p[1])))
    p[0] = p[3]
  else:
    if isinstance(p[1],Operacion):
      p[0] = [Aux("Variable",p[1])]
    else:
      p[0] = [Aux("Cadena",String(p[1]))]

class ifc:
  def __init__(self,cond,bloque,bloque2=""):
    self.cond = cond
    self.bloque = bloque
    self.bloque2 = bloque2
    
  def printArbol(self):
    print "Condicional if \n Condicion: ",
    self.cond.printArbol()
    
    self.bloque.printArbol()
    if self.bloque2!="":
      print "Bloque del else"
      self.bloque2.printArbol()
    
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
  | Casos Casos '''


class forc:
    def __init__(self,var,rango,inst):
      self.var = var
      self.rango = rango
      self.inst = inst
      
    def printArbol(self):
      self.rango.printArbol()
      print "Bloque de instrucciones: \n" 
      self.inst.printArbol()
      
      

def p_Inst_For(p):
  '''Inst_For : INST_FOR VAR_IDENTIFIER INST_IN Rango INST_DO Bloque_Inst '''
  p[0] = forc(p[2],p[4],p[6])

  
class whilec:
    def __init__(self,cond,inst):
      self.cond = cond
      self.inst = inst
      
    def printArbol(self):
      print "Ciclo while con condicion ",
      self.cond.printArbol()
      print " e instrucciones "
      self.inst.printArbol()

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
print result.printArbol()
