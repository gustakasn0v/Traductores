# -*- coding: utf-8 -*-
# Proyecto Traductores e Interpretadores. Entrega 2
# Realizado por:
# Wilmer Bandres. 1010055
# Gustavo El Khoury. 1010226
# -*- coding: utf-8 -*-

import ply.yacc as yacc
import ply.lex as lex
import sys
from lexer import tokens

class indentable:
  level = 0
  def printIndent(self):
    for i in range(self.level):
      print('  '),
    return ''

def p_program(p):
    '''program : INST_PROGRAM Bloque_Inst
    | INST_PROGRAM Inst'''
    p[0] = p[2]

class bloque(indentable):
  def __init__(self,nombre,contenido):
    self.nombre = nombre
    self.contenido = contenido
    self.level=0
    
  def printArbol(self):
    self.printIndent(),
    print self.nombre
    for i in self.contenido:
      i.level = self.level+1
      i.printArbol()
    
    
def p_Bloque_Inst(p):
    '''Bloque_Inst : INST_BEGIN Lista_Inst INST_END
    | INST_BEGIN Inst_Declare Lista_Inst INST_END
    | INST_BEGIN Inst_Declare INST_END'''
    if p[1]=='begin':
      if p[3]=='end':
	p[0] = bloque('BLOQUE',[p[2]])
      else:
	p[0] = bloque('BLOQUE',[p[2],p[3]])
    elif len(p)==3:
      p[0] = bloque('UNICA INSTRUCCION',[p[1],p[2]])
    else:
      p[0] = bloque('UNICA INSTRUCCION',[p[1]])



class listaInstrucciones(indentable):
  def __init__(self,listaInst):
    self.listaInst = listaInst
    
  def printArbol(self):
    for i in self.listaInst:
      i.level = self.level
      i.printArbol()
      

class String(indentable):
  def __init__(self,cadena):
    self.cad = cadena
  
  def printArbol(self):
    print self.cad	
      
def p_Lista_Inst(p):
    '''Lista_Inst : Inst 
    | Inst SEMICOLON Lista_Inst'''
    if(len(p)>=3):
      #p[3].listaInst.insert(0,String("\nSEPARADOR\n"))
      p[3].listaInst.insert(0,p[1])
      p[0] = listaInstrucciones( p[3].listaInst )
      
    else:
      p[0] = listaInstrucciones([p[1]])
      
def p_Inst(p):
  '''Inst : Inst_Asignacion
  | Inst_Lectura 
  | Inst_For 
  | Inst_While
  | Inst_If 
  | Inst_Case 
  | Inst_Salida
  | Inst_Funcion 
  | Bloque_Inst
  '''
  p[0] = p[1]
  p[0].level = p[1].level
  

class InstFuncion(indentable):
  def __init__(self,func,var):
    self.funcion = func
    self.var = var
  def printArbol(self):
    #print "mi nivel es " + str(self.level)
    self.printIndent(),
    print "Funcion: " + self.funcion
    self.printIndent(),
    print "Variable: " + self.var
    
def p_Inst_Funcion(p):
  ''' Inst_Funcion : RTOI LPAREN VAR_IDENTIFIER RPAREN 
  | LENGTH LPAREN VAR_IDENTIFIER RPAREN
  | TOP LPAREN VAR_IDENTIFIER RPAREN
  | BOTTOM LPAREN VAR_IDENTIFIER RPAREN '''
  
  p[0] = InstFuncion(p[1],p[3])
  
class bloqueDeclaracion(indentable):
  def __init__(self,listaDeclaraciones):
    # Esta es una lista de cada linea del declare
    self.listaDeclaraciones = listaDeclaraciones
    
  def printArbol(self):
    self.printIndent(),
    print('DECLARACION:')
    self.listaDeclaraciones.level = self.level+1
    self.listaDeclaraciones.printArbol()
      
class declareTipos(indentable):
  def __init__(self,listaPorTipos):
    self.listaPorTipos = listaPorTipos
    
  def printArbol(self):
    for i in self.listaPorTipos:
      i.level = self.level
      i.printArbol()
	       
class unaDeclaracion(indentable):
  def __init__(self,listaVariables,tipo):
    self.listaVariables = listaVariables
    self.tipo = tipo
    
  def printArbol(self):
   self.printIndent()
   print "Variables: ",
   self.listaVariables.printArbol()
   print "declaradas como " + self.tipo

class listaVariables(indentable):
  def __init__(self,lista):
    self.lista = lista
    
  def printArbol(self):
    for i in self.lista:
      print i +",",

def p_Inst_Declare(p):
  '''Inst_Declare : INST_DECLARE Lista_DeclareTipos'''
  p[0] = bloqueDeclaracion(p[2])

def p_Lista_DeclareTipos(p):   
  '''Lista_DeclareTipos : Lista_Declare
     | Lista_Declare SEMICOLON Lista_DeclareTipos'''
  if len(p)>=4:
    p[0] = declareTipos(p[3].listaPorTipos)
    p[0].listaPorTipos.insert(0,p[1])
  else:
    p[0]=declareTipos([p[1]])
  
def p_Lista_Declare(p):
  '''Lista_Declare : Lista_Variables INST_AS Tipo'''
  p[0] = unaDeclaracion(p[1],p[3])
    

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

class Asignacion(indentable):
  def __init__(self,variable,expresion):
    self.variable = variable
    self.expresion = expresion
  
  def printArbol(self):
    self.printIndent()
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
    ('nonassoc','UMINUS'),
    ('nonassoc', 'RANGE'),
) 

  

class Operacion(indentable):
  def __init__(self,left,opr="",right=""):
    self.left = left
    self.opr = opr
    self.right = right
  def printArbol(self):
    if self.right!="":
      self.printIndent(),
      print "Operacion binaria:" 
      self.level +=1
      self.printIndent(),
      print "Operador: " + self.opr
      self.printIndent()
      print "Operando izquierdo: ",
      
      self.left.level = self.level+1
      self.left.printArbol()
      self.printIndent()
      print "Operando Derecho: ",
      self.right.level = self.level+1
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
  if len(p)>=4:
    p[0] = Operacion(p[1],p[2],p[3])
  elif len(p)==3:
    p[0] = Operacion(p[2],p[1])
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
  | LPAREN Operacion_binaria RPAREN 
  | MINUS Operacion_binaria %prec UMINUS'''
  if len(p)>=3:
	  p[0] = p[2]
  else:
	  p[0] = Operacion(p[1])

def p_Rango(p):
  ''' Rango : Operacion_binaria RANGE Operacion_binaria
  | Rango PLUS Rango
  | Rango TIMES Operacion_binaria
  | Rango INTERSECTION Rango 
  | LPAREN Rango RPAREN
  | VAR_IDENTIFIER '''
  if len(p)>=3:
   if p[1]!='(':
      p[0] = Operacion(p[1],p[2],p[3])
   else:
     p[0] = p[2]
  else:
    p[0] = Operacion(p[1])


class Lectura(indentable):
  def __init__(self,var):
    self.variable = var
  
  def printArbol(self):
    self.printIndent(),
    print "Read de la variable: " + self.variable
    
  
def p_Inst_Lectura(p):
  '''Inst_Lectura : INST_READ VAR_IDENTIFIER '''
  p[0] = Lectura(p[2])
  
  
class Salida(indentable):
  def __init__(self,tipow,lista):
    self.tipo = tipow
    self.lista = lista
  
  def printArbol(self):
    self.printIndent()
    print self.tipo
    for i in self.lista:
      self.printIndent()
      print "Expresion: ",
      print i.tipo
      
      if i.tipo=="Variable":
	self.printIndent()
	print "Nombre: ",
      else:
	self.printIndent()
	print "Valor: "
      self.printIndent()
      i.printArbol()
      print ""

      
#Esta clase se usa para facilitar el write
class Aux(indentable):
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

class ifc(indentable):
  def __init__(self,cond,bloque,bloque2=None):
    self.cond = cond
    self.bloque = bloque
    self.bloque2 = bloque2
    
  def printArbol(self):
    self.printIndent()
    print "Condicional if"
    self.printIndent(),
    print "Condicion: ",
    self.cond.printArbol()
    
    self.bloque.level = self.level
    self.bloque.printArbol()
    if self.bloque2!=None:
      print "Bloque del else"
      self.bloque2.printArbol()

class bloqueControl(indentable):
  def __init__(self,content):
    self.contenido = content
    
  def printArbol(self):
    self.contenido.printArbol()
    
def p_Bloque_Control(p):
  '''Bloque_Control : Inst
  | Bloque_Inst'''
  p[0] = p[1]
  
def p_Inst_If(p):
  '''Inst_If : INST_IF Operacion_booleana INST_THEN Bloque_Control 
  | INST_IF Operacion_booleana INST_THEN Bloque_Control INST_ELSE Bloque_Control'''
  
  if len(p)>=6:
	  p[0] = ifc(p[2],p[4],p[6])
  else:
	  p[0] = ifc(p[2], p[4])
  

class case(indentable):
  def __init__(self,var,lista):
    self.lista = lista
    self.var = var
  
  def printArbol(self):
    self.printIndent()
    print "Condicional case, con expresion: ",
    self.var.level = self.level
    self.var.printArbol()
    
    self.lista.level = self.level +1
    self.lista.printArbol()

class listaCasos(indentable):
  def __init__(self,listCase):
    self.lista = listCase
    
  def printArbol(self):
    for elemento in self.lista:
      elemento.level = self.level
      elemento.printArbol()

class casos(indentable):
  def __init__(self,rango,bloque):
    self.rango = rango
    self.bloque = bloque
    self.bloque.level = self.level
    
  def printArbol(self):
    self.printIndent(),
    print "Caso "
    self.printIndent(),
    print "Ran: "
    if ( isinstance(self.rango,str) ):
      self.printIndent(),
      print('  Variable: ' + self.rango)
    else:
      self.rango.level = self.level+1
      self.rango.printArbol()    
      
    self.bloque.level = self.level
    self.bloque.printArbol()

def p_Inst_Case(p):
  '''Inst_Case : INST_CASE Operacion_booleana INST_OF Casos INST_END'''
  p[0] = case(p[2],p[4])
    
def p_Casos(p):
  ''' Casos : VAR_IDENTIFIER CASE_ASSIGN Bloque_Control
  | Rango CASE_ASSIGN Bloque_Control
  | VAR_IDENTIFIER CASE_ASSIGN Bloque_Control Casos 
  | Rango CASE_ASSIGN Bloque_Control Casos'''

  if len(p)==5:
    p[4].lista.insert(0,casos(p[1],p[3]))
    p[0] = listaCasos(p[4].lista)
  else:
    p[0]=listaCasos([casos(p[1],p[3])])
    
class forc(indentable):
    def __init__(self,var,rango,inst):
      self.var = var
      self.rango = rango
      self.inst = inst
      
    def printArbol(self):
      self.printIndent()
      print "Bloque FOR"
      self.printIndent()
      print "CONDICION:"
      
      self.rango.level = self.level+1
      self.rango.printArbol()
      self.printIndent()
      print "Bloque de instrucciones:" 
      self.inst.level = self.level + 1
      self.inst.printArbol()
      
      

def p_Inst_For(p):
  '''Inst_For : INST_FOR VAR_IDENTIFIER INST_IN Rango INST_DO Bloque_Control '''
  p[0] = forc(p[2],p[4],p[6])

  
class whilec(indentable):
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
    print "Error de sintaxis en la linea",
    print p.lineno -1 ,
    print ": token inesperado:",
    print p.value
    yacc.restart()


# Build the parser
def main():
  parser = yacc.yacc()

  if (len(sys.argv) != 2):
      print("Usage: python parser.py nombreArchivo")
      return -1
    
  # Se abre el archivo con permisos de lectura
  string = str(open(str(sys.argv[1]),'r').read())
  result = parser.parse(string)
  try:
    result.printArbol()
  except AttributeError:
    return
if __name__ == '__main__':
  main()
