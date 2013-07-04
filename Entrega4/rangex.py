# -*- coding: utf-8 -*-
# Proyecto Traductores e Interpretadores. Entrega 2
# Realizado por:
# Wilmer Bandres. 1010055
# Gustavo El Khoury. 1010226
# -*- coding: utf-8 -*-

import ply.yacc as yacc
import ply.lex as lex
import sys
import SymTable
from lexer import tokens, find_column
import inspect

# Variable global que representa una lista de las tablas de símbolos de cada
# bloque. En el código, se recorre de derecha a izquierda para representar la
# precedencia de las declaraciones de variables
listaTablas = []

# Variable que representa si hubo un error en la verificación estática del
# programa. Si ocurrió un error, no se imprime el AST
error = 0

#Esta es una clase que sera utilizada para herencia posteriormente
#Para facilitar la indentacion y asi hacer mas visible la salida
class indentable:
  #este atributo indica cuantos espacios se deben hacer
  level = 0
  def printIndent(self):
    retorno = ''
    for i in range(self.level):
      print(' '),
      retorno = retorno + '  '
    return str(retorno)
  

# Método que determina si una variable fue declarada o no. Si fue declarada,
# retorna la instancia de declaración de dicha variable, respetando la 
# precedencia de las declaraciones

def fueDeclarada(id):
  global listaTablas
  for i in range(1,len(listaTablas)+1):
    if listaTablas[-i].isMember(id,0)==1:
      tmp = listaTablas[-i].find(id)
      return tmp
  return None


#Se define una regla de la gramatica que identifica el inicio de un 
#programa escrito en rangeX y su bloque de instrucciones respectivo
def p_program(p):
    '''program : INST_PROGRAM Bloque_Inst
    | INST_PROGRAM Inst'''
    p[0] = p[2]

 
#Esta clase representa un bloque de instrucciones
#Posee una metodo llamado printArbol que como se dijo en el README
#Es una funcion que se encuentra en todas las clases y se utiliza
#Para imprimir recursivamente el AST
class bloque(indentable):  
  def __init__(self,nombre,contenido):
    self.nombre = nombre
    self.contenido = contenido
    self.level=0
  
  def __iter__(self):
    for i in self.contenido:
      if isinstance(i,listaInstrucciones):
	return iter(i)
    return iter([])
    
    
  def printArbol(self):
    indentacion=self.printIndent()
    print self.nombre
    if self.tabla is not None:
      self.tabla.indent = indentacion
      print str(self.tabla)
    for i in self.contenido:
      i.level = self.level+1
      i.printArbol()
  
  def ejecutar(self):
    global listaTablas
    listaTablas.append(self.tabla)
    for i in self:
      i.ejecutar()
    
    
#Regla del parser que define lo que es un bloque de instrucciones
#Este puede ser varias instrucciones
#O uno o varios declare con un conjunto de instrucciones
#O una bloque con solo declare
#Ademas utiliza la clade bloque para representar la gramatica de 
#atributos
def p_Bloque_Inst(p):
    '''Bloque_Inst : INST_BEGIN Lista_Inst INST_END
    | INST_BEGIN Inst_Declare Lista_Inst INST_END
    | INST_BEGIN Inst_Declare INST_END'''
    if p[1]=='begin':
      if p[3]=='end' and not isinstance(p[2],bloqueDeclaracion):
	p[0] = bloque('BLOQUE',[p[2]])
	p[0].tabla = None
      else:
	p[0] = bloque('BLOQUE',[p[2],p[3]])
	
	try:
	  p[0].tabla = listaTablas.pop()
	except IndexError:
	  pass
	
    elif len(p)==3:
      p[0] = bloque('UNICA INSTRUCCION',[p[1],p[2]])
    else:
      p[0] = bloque('UNICA INSTRUCCION',[p[1]])


#Clase que se utiliza para representar una lista de instrucciones
#igualmente hace uso de la funcion printArbol para imprimir 
#recursivamente el AST
class listaInstrucciones(indentable):
  def __init__(self,listaInst):
    self.listaInst = listaInst
  
  def __iter__(self):
    return iter(self.listaInst)
  
  def printArbol(self):
    for i in self.listaInst:
      i.level = self.level
      i.printArbol()
      self.printIndent()
      if i!= self.listaInst[len(self.listaInst)-1]:
	print "SEPARADOR"
      

#Clase que se utiliza para representar un string pero al ser una clase
#creada por nosotros se le coloca la funcion printArbol para poder 
#imprimir (reiteramos) de manera corecta el AST
class String(indentable):
  def __init__(self,cadena):
    self.cad = cadena
  
  def printArbol(self):
    print self.cad	
      
      
#Rega del parser que define una instruccion o una lista de la misma
#y utiliza la clase listaInstrucciones para poder representar la 
#gramatica de atributos
def p_Lista_Inst(p):
    '''Lista_Inst : Inst 
    | Inst SEMICOLON Lista_Inst'''
    if(len(p)>=3):
      #p[3].listaInst.insert(0,String("\nSEPARADOR\n"))
      p[3].listaInst.insert(0,p[1])
      p[0] = listaInstrucciones( p[3].listaInst )
    else:
      p[0] = listaInstrucciones([p[1]])
      
      
#Regla del parser que define una instruccion, esta puede ser:
#Una instruccion de asignacion
#Una instruccion de lectura o salida
#Una instruccion de iteracion
#Una instruccion que sea una funcion
  
def p_Inst(p):
  '''Inst : Inst_Asignacion
  | Inst_Lectura 
  | Inst_For 
  | Inst_While
  | Inst_If 
  | Inst_Case 
  | Inst_Salida
  | Bloque_Inst
  '''
  p[0] = p[1]
  p[0].level = p[1].level
  

#Clase utilizada para representar una instruccion que hace llamada
#a una funcion
class InstFuncion(indentable):
  def __init__(self,func,var):
    global error
    self.funcion = func
    self.var = var
    self.ok = self.var.ok and self.var.tipo =="range"
    self.tipo = "None"
    if self.ok:
      self.tipo = "int"
    elif self.var.tipo != 'None':
      pos = self.getPosition()
      print "Error: Linea %d, Columna %d: La funcion \"%s\" recibe una expresion de tipo \"range\" y se le esta pasando una expresion de tipo \"%s\"" % (pos[0],pos[1],self.funcion,self.var.tipo)
      error = 1
  def printArbol(self):
    print
    self.printIndent(),
    print "Funcion: " + self.funcion  #", Expresion:" + str(self.ok) + self.tipo
    self.printIndent(),
    print "Expresion: " ,
    self.var.level=self.level+1
    self.var.printArbol()
  
  def getValor(self):
    pass
    #return self.var.valor hay que retornar el valor
  def getPosition(self):
    return self.var.getPosition()
    
    
#Regla del parser que se utiliza para la representacion de una funcion
#La cual actua sobre un rango o tambien puede actuar sobre
#una variable si esta es de tipo rango (aunque por ahora no nos
#interesa el tipo del mismo ya que estamos construyendo un AST)
def p_Inst_Funcion(p):
  ''' Inst_Funcion : RTOI LPAREN Expresion RPAREN 
  | LENGTH LPAREN Expresion RPAREN
  | TOP LPAREN Expresion RPAREN
  | BOTTOM LPAREN Expresion RPAREN 
  | RTOI LPAREN VAR_IDENTIFIER RPAREN 
  | LENGTH LPAREN VAR_IDENTIFIER RPAREN
  | TOP LPAREN VAR_IDENTIFIER RPAREN
  | BOTTOM LPAREN VAR_IDENTIFIER RPAREN'''
  if type(p[3])==str:
    p[0]= InstFuncion(p[1],Operacion(p[3]))
  else:
    p[0] = InstFuncion(p[1],p[3])
 
 
 
#Clase utilizada para representar una declaracion de variables en 
#rangeX
class bloqueDeclaracion(indentable):
  def __init__(self,listaDeclaraciones):
    # Esta es una lista de lineas del declare
    self.listaDeclaraciones = listaDeclaraciones
    self.tablaSimbolos = SymTable.SymTable()
    for i in self.listaDeclaraciones.listaPorTipos:
      retorno = self.tablaSimbolos.merge(i.tablaSimbolos)
      global error
      if retorno is not None:
	print 'Error: Linea '+str(retorno[0])+', columna '+str(retorno[1])+': Variable "'+retorno[2]+'" declarada dos veces'
	error = 1
	
	
    
  def printArbol(self):
    #self.printIndent(),
    #print('DECLARACION:')
    #self.listaDeclaraciones.level = self.level+1
    #self.listaDeclaraciones.printArbol()
    pass

class declareTipos(indentable):
  def __init__(self,listaPorTipos):
    self.listaPorTipos = listaPorTipos
    
    
  def printArbol(self):
    for i in self.listaPorTipos:
      i.level = self.level
      i.printArbol()

      
#Clase que representara una declaracion de variables
#donde contendra en listaVariables todas las variables
#declaradas y en otro atributo tendra el tipo de esas variables
#declaradas
class unaDeclaracion(indentable):
  def __init__(self,listaVariables,tipo):
    global error
    self.listaVariables = listaVariables
    self.tipo = tipo
    self.tablaSimbolos = SymTable.SymTable()
    for i in self.listaVariables.lista: 
      retorno = self.tablaSimbolos.insert(i)
      if retorno == 1:
	error = retorno
	print 'Error: Linea '+str(i.lineno)+', columna '+str(i.colno)+': Variable "'+i.id+'" declarada dos veces'

    
  def printArbol(self):
   self.printIndent()
   print "Variables: ",
   self.listaVariables.printArbol()
   print "declaradas como " + self.tipo

#Clase que representa una lista de variables que se dan en una misma
#linea de un declare
class listaVariables(indentable):
  def __init__(self,lista):
    self.lista = lista
    
  def printArbol(self):
    for i in self.lista:
      print i.id +",",

#Regla de la gramatica utilizada para reconocer una declaracion de
#variables asi como sus tipos
def p_Inst_Declare(p):
  '''Inst_Declare : INST_DECLARE Lista_DeclareTipos'''
  p[0] = bloqueDeclaracion(p[2])
  global listaTablas
  listaTablas.append(p[0].tablaSimbolos)

  
#Regla de la gramatica utilizada para reconocer varias lineas
#de un declare de un bloque
def p_Lista_DeclareTipos(p):   
  '''Lista_DeclareTipos : Lista_Declare
     | Lista_Declare SEMICOLON Lista_DeclareTipos'''
  if len(p)>=4:
    p[0] = declareTipos(p[3].listaPorTipos)
    p[0].listaPorTipos.insert(0,p[1])
  else:
    p[0]=declareTipos([p[1]])

  
#Regla de la gramatica utilizada para representar una lista 
#de variables seguida por su tipo
def p_Lista_Declare(p):
  '''Lista_Declare : Lista_Variables INST_AS Tipo'''
  p[0] = unaDeclaracion(p[1],p[3])
  for i in p[1].lista:
    i.setType(p[3])
  
#Regla de la gramatica que representa una lista de variables
def p_Lista_Variables(p):
  '''Lista_Variables : VAR_IDENTIFIER
  | VAR_IDENTIFIER COMMA Lista_Variables '''
  insercion = SymTable.variable(p[1],'')
  insercion.setLine(p.lineno(1))
  insercion.setColumn(find_column(p.slice[1].lexer.lexdata,p.slice[1]))
  if(len(p)>=3):  
    p[3].lista.insert(0,insercion)
    p[0] = listaVariables( p[3].lista)
  else:
    p[0] = listaVariables([insercion])
  
#Regla de la grmaatica utilizada que reconoce cualquiera de los 
#3 tipos de variables disponibles en rangeX
def p_Tipo(p):
  ''' Tipo : TYPEDEF_INT 
  | TYPEDEF_BOOL 
  | TYPEDEF_RANGE '''
  p[0] =  p[1]

#Clase utilizada para representar una instruccion de asignacion de
#varaible
class Asignacion(indentable):
  def __init__(self,variable,expresion):
    self.variable = variable
    self.expresion = expresion
  
  def printArbol(self):
    self.printIndent(),
    print "A la variable: " + str(self.variable) + " se le asigna ",
    self.expresion.level = self.level
    self.expresion.printArbol()
    
  def ejecutar(self):
    instancia = fueDeclarada(self.variable)
    try:
      self.expresion.calculaValor()
      instancia.valor = self.expresion.valor
    except AttributeError:
      print 'Valor de la expresion no seteado'
      
    
#Regla de la gramatica utilizada para reconocer una asignacion
def p_Inst_Asignacion(p):
  '''Inst_Asignacion : VAR_IDENTIFIER EQUAL Expresion'''
  p[0] = Asignacion(p[1],p[3])
  global error
  # Verifico que la variable a asignar haya sido declarada,
  # y si su tipo coincide con el tipo de la expresion
  existente = fueDeclarada(p[1])
  col = find_column(p.slice[1].lexer.lexdata,p.slice[1])
  if existente is None:
    print '''Error: Linea %d, columna %d: Variable "%s" no declarada'''  % (p.lineno(1),col,p[1])
    error = 1
  else:
    if existente.blocked == 1:
      print '''Error: Linea %d, columna %d: Variable "%s" es el indice de un bloque FOR, y no puede modificarse'''% (p.lineno(1),col,p[1])
      error = 1
    elif existente.type != p[3].tipo and p[3].tipo != 'None':
      error = 1
      print 'Error: Linea '+str(p.lineno(1))+', columna ' + str(col) + ':',
      print 'A la variable "'+p[1]+'"',
      print 'de tipo "' + existente.type  + '" no se le puede asignar',
      print 'una expresion de tipo "' + p[3].tipo + '"'
    elif p[3].tipo == 'None':
      error = 1
      
  

  
#Reglas de precedencia de los operadores permitidos por rangeX
precedence = (
    ('right','INST_ELSE'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('nonassoc', 'NOT'),
    ('nonassoc','LESS','LESSEQ' ,'GREAT','GREATEQ'),
    ('left','EQEQ' ,'NEQEQ'),
    ('left','IN'),
    ('left','INTERSECTION'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE','MOD'),
    ('left', 'RANGE'),
    ('right','UMINUS'),
) 

class Rango:
  def __init__(self,iz,der):
    self.iz = iz
    self.der = der
  
  def __eq__(self,otr):
    return self.iz == otr.iz and self.der == otr.der
    
  def __ne__(self,otr):
    return self.iz != otr.iz or self.der != otr.der
    
  def __add__(self,otr):
    return Rango(self.iz,otr.der)
  
  def __lt__ (self,otr):
    return self.der<otr.der
    
  def __le__ (self,otr):
    return self.der<=otr.der
    
  def __gt__(self,otr):
    return self.iz>otr.iz
    
  def __ge__(self,otr):
    return self.iz>=otr.iz
    
  def __str__(self):
    return str(self.iz)+'..'+str(self.der)
    
    
  
#Clase utilizada para representar una operacion realizable 
#en rangeX, esta misma clase representa operaciones binarias,
#unarias y variables o numeros
class Operacion(indentable):
  # Metodo que calcula el valor de una expresion
  def calculaValor(self):
    self.valor = self.getValor()
  
  def __init__(self,left,opr="",right=""):
    self.left = left
    self.opr = opr
    self.right = right
    global listaTablas

    if right != "":
      if self.opr=="+" or self.opr == "*" or self.opr==">" or self.opr==">=" or self.opr=="<" or self.opr=="<=":
	self.ok = self.left.ok and self.right.ok and ((self.left.tipo==self.right.tipo and (self.left.tipo=="int" or self.left.tipo=="range")) or (self.opr == '*' and self.left.tipo == "range" and self.right.tipo == "int" ))
	self.tipo = "None"
	if self.ok:
	  if self.opr==">" or self.opr==">=" or self.opr=="<" or self.opr=="<=":
	    self.tipo = "bool"
	  else:
	    self.tipo = self.left.tipo
	elif self.left.tipo != 'None' and self.right.tipo != 'None':
	  if self.opr==">" or self.opr==">=" or self.opr=="<" or self.opr=="<=":
	    pos = self.right.getPosition()
	    print "Error: Linea %d, Columna %d: El operador %s compara dos expresiones de tipo \"int\" o de tipo rango y se le estan pasando las expresiones de tipo \"%s\" y tipo \"%s\" respectivamente." % (pos[0],pos[1],self.opr,self.left.tipo,self.right.tipo)
	  else:
	    pos = self.right.getPosition()
	    if self.opr=="*":
	      print "Error: Linea %d, Columna %d: El operador * opera sobre dos expresiones de tipo \"int\" o una de tipo \"range\" y la otrade tipo \"int\" y se le estan pasando las expresiones de tipo \"%s\" y tipo \"%s\" respectivamente." % (pos[0],pos[1],self.left.tipo,self.right.tipo)
	    else:
	      print "Error: Linea %d, Columna %d: El operador + opera sobre dos expresiones de tipo \"int\" o dos de tipo \"range\" y se le estan pasando las expresiones de tipo \"%s\" y tipo \"%s\" respectivamente." % (pos[0],pos[1],self.left.tipo,self.right.tipo)
      elif self.opr=="-" or self.opr=="/" or self.opr=="%":
	self.ok = self.left.ok and self.right.ok and self.left.tipo==self.right.tipo and (self.left.tipo=="int")
	self.tipo = "None"
	if self.ok:
	  self.tipo = self.left.tipo
	elif self.left.tipo != 'None' and self.right.tipo != 'None':
	  pos = self.right.getPosition()
	  print "Error: Linea %d, Columna %d: El operador %s opera sobre dos expresiones de tipo \"int\" y se le estan pasando las expresiones de tipo \"%s\" y tipo \"%s\" respectivamente." % (pos[0],pos[1],self.opr,self.left.tipo,self.right.tipo)
      elif self.opr=="and" or self.opr=="or":
	self.ok = self.left.ok and self.right.ok and self.left.tipo==self.right.tipo and (self.left.tipo=="bool")
	self.tipo = "None"
	if self.ok:
	  self.tipo = self.left.tipo
	elif self.left.tipo != 'None' and self.right.tipo != 'None':
	  pos = self.right.getPosition()
	  print "Error: Linea %d, Columna %d: El operador %s opera sobre dos expresiones de tipo \"bool\" y se le estan pasando las expresiones de tipo \"%s\" y tipo \"%s\" respectivamente." % (pos[0],pos[1],self.opr,self.left.tipo,self.right.tipo)
	  
      elif self.opr=="==" or self.opr=="/=": 
	self.ok = self.left.ok and self.right.ok and self.left.tipo==self.right.tipo
	self.tipo = "None"
	if self.ok:
	  self.tipo = "bool"
	elif self.left.tipo != 'None' and self.right.tipo != 'None':
	  pos = self.right.getPosition()
	  print "Error: Linea %d, Columna %d: El operador %s opera sobre dos expresiones de tipo \"bool\" y se le estan pasando las expresiones de tipo \"%s\" y tipo \"%s\" respectivamente." % (pos[0],pos[1],self.opr,self.left.tipo,self.right.tipo)
      
      elif self.opr==">>":
	self.ok = self.left.ok and self.right.ok and self.left.tipo=="int" and self.right.tipo=="range"
	self.tipo = "None"
	if self.ok:
	  self.tipo = "bool"
	elif self.left.tipo != 'None' and self.right.tipo != 'None':
	   pos = self.right.getPosition()
	   print "Error: Linea %d, Columna %d: El operador >> opera sobre una expresion de tipo \"int\" y una de tipo \"range\" y se le estan pasando las expresiones de tipo \"%s\" y tipo \"%s\" respectivamente." % (pos[0],pos[1],self.left.tipo,self.right.tipo)
	
      elif self.opr=="..":
	self.ok = self.left.ok and self.right.ok and self.left.tipo==self.right.tipo and (self.left.tipo=="int")
	self.tipo = "None"
	if self.ok:
	  self.tipo = "range"
	elif self.left.tipo != 'None' and self.right.tipo != 'None':
	  pos = self.right.getPosition()
	  print "Error: Linea %d, Columna %d: El operador .. opera sobre dos expresiones de tipo \"int\" y se le estan pasando las expresiones de tipo \"%s\" y tipo \"%s\" respectivamente." % (pos[0],pos[1],self.left.tipo,self.right.tipo)
	
      elif self.opr=="<>":
	self.ok = self.left.ok and self.right.ok and self.left.tipo==self.right.tipo and (self.left.tipo=="range")
	self.tipo = "None"
	if self.ok:
	  self.tipo = "range"
	elif self.left.tipo != 'None' and self.right.tipo != 'None':
	  pos = self.right.getPosition()
	  print "Error: Linea %d, Columna %d: El operador <> opera sobre dos expresiones de tipo \"range\" y se le estan pasando las expresiones de tipo \"%s\" y tipo \"%s\" respectivamente." % (pos[0],pos[1],self.left.tipo,self.right.tipo)
	
    elif self.opr != "":
      if self.opr=="-":
	self.ok = self.left.ok and self.left.tipo == "int"
	self.tipo = "int"
	if not self.ok:
	  pos = self.left.getPosition()
	  print "Error: Linea %d, Columna %d: El operador \"-\" unario debe estar seguido de una expresion de tipo \"int\"" % (pos[0],pos[1])
	  self.tipo = "None"
      else:
	self.ok = self.left.ok and self.left.tipo == "bool"
	self.tipo = "bool"
	if not self.ok:
	  pos = self.left.getPosition()
	  print "Error: Linea %d, Columna %d: El operador \"not\" debe estar seguido de una expresion de tipo \"bool\"" % (pos[0],pos[1])
	  self.tipo="None"
    else:
      if type(self.left)==str and self.left!="true" and self.left!="false":
	no = False
	#var = SymTable.variable(self.left,'bool')
	for i in range(1,len(listaTablas)+1):
	  if listaTablas[-i].isMember(self.left,0)==1:
	    tmp = listaTablas[-i].find(self.left)
	    self.tipo = tmp.type
	    no = True
	    break
	    
	if not no:
	  self.ok = False
	  self.tipo = "None"
	  #print "Variable " + self.left + " no declarada"
	  #global error
	  #error = 1
	else:
	  self.ok = True
      elif type(self.left)==int:
	self.ok = True
	self.tipo = "int"
      elif self.left == "true" or self.left == "false":
	self.ok = True
	self.tipo = "bool"
      else:
	self.ok = self.left.var.ok and (self.left.var.tipo == "range")
	if self.ok:
	  self.tipo = "int"
	else:
	  self.tipo = "None" 
	
  def setPosition(self,fila,columna):
    self.lineno = fila
    self.colno = columna
    
  def getPosition(self):
    if self.opr == '' and self.right == '' and not isinstance(self.left,Operacion) and not isinstance(self.left,InstFuncion):
      return (self.lineno,self.colno+1)
    else:
      return self.left.getPosition()
  
  #
  
  
  def getValor(self):
    global listaTablas

    if self.right != "":
      if self.opr == "+" :
	return self.left.getValor() + self.right.getValor()
	  
      elif self.opr == "*" :
	if self.left.tipo == "int":
	  return self.left.getValor() * self.right.getValor()
	else:
	  tmp = self.right.getValor()
	  if tmp >= 0:
	    return Rango(tmp*self.left.getValor().iz,tmp*self.left.getValor().der)
	  else:
	    return Rango(tmp*self.left.getValor().der,tmp*self.left.getValor().iz)
	  
      elif self.opr == "-":
	return self.left.getValor() - self.right.getValor()
	
      elif self.opr == "/":
	tmp = self.right.getValor()
	if tmp == 0:
	  print "Error: Intento de division por cero."
	  sys.exit()
	else:
	  return self.left.getValor() / tmp
	  
      elif self.opr == "%":
	tmp = self.right.getValor()
	if tmp == 0:
	  print "Error: Intento de buscar el resto al dividir por cero."
	  sys.exit()
	else:
	  return self.left.getValor() % tmp
	  
      elif self.opr == ">":
	return self.left.getValor() > self.right.getValor()
	
      elif self.opr == ">=":
	return self.left.getValor() >= self.right.getValor()
	
      elif self.opr == "<":
	return self.left.getValor() < self.right.getValor()
	
      elif self.opr == "<=":
	return self.left.getValor() <= self.right.getValor()
	
      elif self.opr == "and":
	return self.left.getValor() and self.right.getValor()
	
      elif self.opr == "or":
	return self.left.getValor() or self.right.getValor()
	
	
      elif self.opr == "==":
	return self.left.getValor() == self.right.getValor()
	
	
      elif self.opr == "/=":
	return self.left.getValor() != self.right.getValor()
	
      elif self.opr==">>":
	tmp = self.right.getValor()
	return self.left.getValor() >= tmp.iz and self.left.getValor()<= tmp.der
	
      elif self.opr=="..":
	if self.left.getValor() > self.right.getValor():
	  print "Error: Intento de crear Rango, expresion izquierda mayor que la expresion entera de la derecha"
	  sys.exit()
	else:
	  return Rango(self.left.getValor(),self.right.getValor())
	
      elif self.opr=="<>":
	tmp = self.left.getValor()
	tmp2 = self.right.getValor()
	
	if (tmp.iz <= tmp2.der and tmp.iz>=tmp2.iz) or (tmp2.iz <= tmp.der and tmp2.iz>=tmp.iz):
	  if (tmp.iz <= tmp2.der and tmp.iz>=tmp2.iz):
	    return Rango(tmp.iz,min(tmp.der,tmp2.der))
	  else:
	    return Rango(tmp2.iz,min(tmp.der,tmp2.der))
	else:
	  print "Error: Intento de interceptar rangos, subrango vacio."
	  sys.exit()
	
    elif self.opr != "":
      if self.opr=="-":
	return -self.left.getValor()
      else:
	return not self.left.getValor()
    else:
      if type(self.left)==str and self.left!="true" and self.left!="false":
	no = False
	#var = SymTable.variable(self.left,'bool')
	tmp = fueDeclarada(self.left)
	return tmp.valor
	#for i in range(1,len(listaTablas)+1):
	  #if listaTablas[-i].isMember(self.left,0)==1:
	    #tmp = listaTablas[-i].find(self.left)
	    #self.tipo = tmp.type
	    #no = True
	    #break
	    
	#Retorno valor de la variable 
	
      elif type(self.left)==int:
	return self.left
	
      elif self.left == "true" or self.left == "false":
	if self.left == "true":
	  return True
	else:
	  return False
	  
      else:
	tmp = self.left.var.getValor()
	if self.left.funcion == "rtoi":
	  if tmp.iz == tmp.der:
	    return tmp.iz
	  else:
	    print "Error: El \"range\" no se puede convertir a \"int\" cotas distintas. "
	    sys.exit()
	elif self.left.funcion == "length":
	  return tmp.der-tmp.iz+1
	elif self.left.funcion == "top":
	  return tmp.der
	else:
	  return tmp.iz
	   
	  
	  ##
    
  def printArbol(self):
    #Este if revisa si la operacion es binaria
    if self.right!="":
      print ""
      self.level = self.level+ 1
      self.printIndent(),
      print "Operacion binaria:" 
      self.level = self.level + 1
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
    #Este if revisa si la operacion es unaria
    elif self.opr!="":
      self.level+=1
      print ""
      self.printIndent(),
      print "Operacion unaria:"+ "\n" 
      self.printIndent(),
      print "Operador: " +  "\n" 
      self.printIndent(),
      print "Operando: ",
      self.left.level = self.level+1
      self.left.printArbol()
    #Revisa si la instacia no es una operacion sino una variable o 
    #numero
    else:
      if type(self.left)==str and self.left!="true" and self.left!="false":
	print "Variable: " ,
	print self.left
      elif type(self.left)==int or self.left == "true" or self.left == "false":
	print "Constante: " ,
	print self.left
      else:
	self.left.level = self.level+1
	self.left.printArbol()
	
  
#Esta es la regla de la gramatica que reconoce las expresiones 
#permitidas en rangeX, estas pueden ser binarias (que para nuestros
#efectos representa en realidad una operacion arimetica), 
#operacion booleana o un rango


def p_Expresion(p):
  '''Expresion : Operacion_binaria'''
  #| Operacion_booleana 
  p[0] = p[1]


def p_Operacion_binaria(p):
  ''' Operacion_binaria : Operacion_binaria PLUS Operacion_binaria
  | Operacion_binaria MINUS Operacion_binaria
  | Operacion_binaria TIMES Operacion_binaria
  | Operacion_binaria DIVIDE Operacion_binaria
  | Operacion_binaria MOD Operacion_binaria
  | Operacion_binaria AND Operacion_binaria
  | Operacion_binaria OR Operacion_binaria
  | Operacion_binaria EQEQ Operacion_binaria
  | Operacion_binaria NEQEQ Operacion_binaria
  | Operacion_binaria GREAT Operacion_binaria
  | Operacion_binaria GREATEQ Operacion_binaria
  | Operacion_binaria LESS Operacion_binaria
  | Operacion_binaria LESSEQ Operacion_binaria
  | Operacion_binaria IN Operacion_binaria
  | Operacion_binaria RANGE Operacion_binaria
  | Operacion_binaria INTERSECTION Operacion_binaria
  | NOT Operacion_binaria
  | NUMBER
  | VAR_IDENTIFIER
  | LPAREN Operacion_binaria RPAREN
  | RTOI LPAREN Operacion_binaria RPAREN 
  | LENGTH LPAREN Operacion_binaria RPAREN
  | TOP LPAREN Operacion_binaria RPAREN
  | BOTTOM LPAREN Operacion_binaria RPAREN 
  | MINUS Operacion_binaria %prec UMINUS 
  | TRUE
  | FALSE
  '''
  global error
  if len(p)>=5:
    p[0] = Operacion(InstFuncion(p[1],p[3]))
  elif len(p)>=4:
    if p[1]=='(':
      p[0]=p[2]
    else:
      p[0] = Operacion(p[1],p[2],p[3])
  elif len(p)>=3:
    p[0] = Operacion(p[2],p[1])
  else:
    p[0] = Operacion(p[1])
    col = find_column(p.slice[1].lexer.lexdata,p.slice[1])+1
    #print 'machete ' + str(p.slice[1])
    p[0].setPosition(p.lineno(1),col)
    # Verificacion de si la variable fue declarada o no
    if p[1] != 'true' and p[1] != 'false' and type(p[1]) != int:
      retorno = fueDeclarada(p[1])
      if retorno is None:
	col = find_column(p.slice[1].lexer.lexdata,p.slice[1])
	print 'Error: Linea '+str(p.lineno(1))+', columna '+str(col)+': Variable "'+p[1]+'" no declarada'
	error = 1

    
    
#Clase utilizada para representar una instruccion de salida
#aceptada por rangeX
class Lectura(indentable):
  def __init__(self,var):
    self.variable = var
  
  def printArbol(self):
    self.printIndent(),
    print "Read de la variable: " + self.variable
  
  def ejecutar(self):
    valor = raw_input()
    instanciaVariable = fueDeclarada(self.variable)
    if instanciaVariable.type == 'int':
      try:
	# Almaceno el valor en la variable
	instanciaVariable.valor = int(valor)
      except ValueError:
	print 'El valor introducido no es un entero'
	raise
      
    elif instanciaVariable.type == 'bool':
      if valor != 'true' and valor != 'true':
	print 'Valor de la lectura no coincide con el tipo de la variable'
	sys.exit(1)
      else:
	# Almaceno el valor en la variable
	instanciaVariable.valor = valor
	
    elif instanciaVariable.type == 'range':
      
      dosPuntos = 1
      pos = valor.rfind('..')
      if pos == -1:
	pos = valor.rfind(',')
	if pos == -1:
	  print 'Valor de la lectura no coincide con el tipo de la variable'
	  sys.exit(1)
	else:
	  dosPuntos = 0
      try:
	inicio = int(valor[:pos])
	fin = int(valor[pos+1+dosPuntos:])
	if inicio > fin:
	  raise ValueError
	# Almaceno el valor en la variable
	instanciaVariable.valor = Rango(inicio,fin)
      except ValueError:
	print 'Rango mal definido'
    
#Regla de la gramatica utilizada para reconocer una instruccion
#de lectura
def p_Inst_Lectura(p):
  '''Inst_Lectura : INST_READ VAR_IDENTIFIER '''
  p[0] = Lectura(p[2])
  global listaTablas
  global error
  check = 0
  retorno = fueDeclarada(p[2])
  if retorno is None:
    col = find_column(p.slice[2].lexer.lexdata,p.slice[2])
    print 'Error: Linea '+str(p.lineno(2))+', columna '+ str(col)+': Variable "'+p[2]+'" no declarada'
    error = 1
  elif retorno.blocked:
    col = find_column(p.slice[1].lexer.lexdata,p.slice[1])
    print 'Error: Linea '+str(p.lineno(2))+', columna '+ str(col)+': Variable "'+p[2]+'"',
    print 'es el indice de un bloque FOR, y no puede modificarse'
    error = 1
  
  
#Clase utilizada para representar una instruccion de lectura
#aceptada por rangeX, la cual puede escribir una o mas expresiones
class Salida(indentable):
  def __init__(self,tipow,lista):
    self.tipo = tipow
    self.lista = lista
  
  def printArbol(self):
    self.printIndent()
    print self.tipo
    j = int(1)
    self.level = self.level + 1
    self.printIndent()
    print "Las Expresiones de la operacion de escritura son:"
    #Para cada elemento en la lista de expresiones, se imprime
    #que tipo es y como se llama o su valor
    for i in self.lista:
      i.level = self.level + 1
      self.printIndent(),
      print "Expresion " + str(j) + ": ",
      j+=1
      if i.tipo=="Cadena":
	print "Cadena",
      print ""
      if i.tipo=="Variable":
	pass
      else:
	self.printIndent(),
	print "Valor: "
      self.printIndent()
      i.printArbol()
      
  def ejecutar(self):
    for i in self.lista:
      if isinstance(i.val,Operacion):	
	i.val.calculaValor()
	print str(i.val.valor) + ' ',
      else:
	print i.val.cad[1:-1] + ' ',
    if self.tipo == 'WRITELN':
      print
	
    
      

      
#Esta clase se usa para facilitar la implementacion de las clases
#y reglas de la instruccion write de rangeX
class Aux(indentable):
  def __init__(self,tipo,valor):
    self.val = valor
    self.tipo = tipo
    
  def printArbol(self):
    self.val.level = self.level+1
    self.val.printArbol()


#Definicion de la regla de la gramatica que reconoce la instruccion 
#write o writeln
def p_Inst_Salida(p):
  '''Inst_Salida : INST_WRITE Lista_Aux
  | INST_WRITELN  Lista_Aux '''
  if p[1]=="write":
    p[1]="WRITE"
  else:
    p[1]="WRITELN"
  p[0] = Salida(p[1],p[2])

#Regla de la gramatica utilizada para reconocer las expresiones
#de una instruccion writeo writeln aceptadas por rangeX
def p_Lista_Aux(p):
  '''Lista_Aux : Expresion
  | STRING 
  | Expresion COMMA Lista_Aux
  | STRING COMMA Lista_Aux '''
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

#Clase utilizada para representar la instruccion if - then - else
#en rangeX
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
    self.cond.level = self.level+1
    self.cond.printArbol()
    
    self.bloque.level = self.level+1
    self.printIndent(),
    print "Instrucciones del if:"
    self.bloque.printArbol()
    #Si la instruccion posee else
    if self.bloque2!=None:
      self.printIndent(),
      print "Bloque del else"
      self.bloque2.level = self.level + 1
      self.bloque2.printArbol()
      
  def ejecutar(self):
    self.cond.calculaValor()
    if self.cond.valor:
      self.bloque.ejecutar()
    elif self.bloque2 != None:
      self.bloque2.ejecutar()

#Clase utilizada para representar un bloque de control de la
#instruccion case
class bloqueControl(indentable):
  def __init__(self,content):
    self.contenido = content
    
  def printArbol(self):
    self.contenido.printArbol()
    
#Regla del la gramatica utilizada para reconocer un bloque de control
def p_Bloque_Control(p):
  '''Bloque_Control : Inst
  | Bloque_Inst'''
  p[0] = p[1]
  
#Regla de la gramatica utilizada para reconocer un if
def p_Inst_If(p):
  '''Inst_If : INST_IF Expresion INST_THEN Bloque_Control 
  | INST_IF Expresion INST_THEN Bloque_Control INST_ELSE Bloque_Control'''
  
  if len(p)>=6:
	  p[0] = ifc(p[2],p[4],p[6])
  else:
	  p[0] = ifc(p[2], p[4])
  
#Clase utilizada pra representar un caso de un case, incluyendo su 
#condicional
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

#Clase utilizada para representar una lista de casos dentro de una 
#instruccion case
class listaCasos(indentable):
  def __init__(self,listCase):
    self.lista = listCase
    
  def printArbol(self):
    for elemento in self.lista:
      elemento.level = self.level
      elemento.printArbol()

#Clase utilizada para representar una instruccion case de rangeX
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

#Regla del parser utilizada para reconocer una instruccion case
#de rangeX
def p_Inst_Case(p):
  '''Inst_Case : INST_CASE Operacion_binaria INST_OF Casos INST_END'''
  p[0] = case(p[2],p[4])
    
#Regla del parser utilizada para reconocer los casos de una instruccion
#case de rangeX
def p_Casos(p):
  ''' Casos : VAR_IDENTIFIER CASE_ASSIGN Bloque_Control SEMICOLON
  | Expresion CASE_ASSIGN Bloque_Control SEMICOLON
  | VAR_IDENTIFIER CASE_ASSIGN Bloque_Control SEMICOLON Casos 
  | Expresion CASE_ASSIGN Bloque_Control SEMICOLON Casos'''

  if len(p)==6:
    p[5].lista.insert(0,casos(p[1],p[3]))
    p[0] = listaCasos(p[5].lista)
  else:
    p[0]=listaCasos([casos(p[1],p[3])])
    
#Clase utilizada para representar una instruccion de for aceptada
#por rangeX
class forc(indentable):
    def __init__(self,var,rango,inst):
      self.var = var
      self.rango = rango
      self.inst = inst
      
    def printArbol(self):
      self.printIndent()
      print "Bloque FOR"
      self.printIndent()
      print "\tidentificador: ",
      print self.var
      self.printIndent()
      print "\tRango:",
      
      self.rango.level = self.level+2
      self.rango.printArbol()
      self.printIndent()
      print "\tBloque de instrucciones:" 
      self.inst.level = self.level + 3
      self.inst.printArbol()
    
    def ejecutar(self):
      self.rango.inferior = self.rango.getValor().iz
      self.rango.superior = self.rango.getValor().der
      
      global listaTablas
      listaTablas.append(self.tabla)
      self.rango.calculaValor()
      # Inicializo el valor de la variable del for
      self.tabla.lista[0].valor = self.rango.inferior 
      
      for i in range(self.rango.inferior,self.rango.superior):
	self.inst.ejecutar()
	self.rango.calculaValor()
	# Incremento el valor de la variable del for
	self.tabla.lista[0].valor += 1
      
#Regla del a gramatica utilizada para reconocer una instruccion for
#en rangeX  
def p_Inst_For(p):
  '''Inst_For : INST_FOR Variable_For INST_IN Expresion INST_DO Bloque_Control '''
  p[0] = forc(p[2],p[4],p[6])
  
  # Elimino la tabla de simbolos que contiene la variable del for 
  try:
    p[0].tabla = listaTablas.pop()
  except IndexError:
    pass
  
def p_Variable_For(p):
  '''Variable_For : VAR_IDENTIFIER'''
  p[0] = p[1]
  
  # Se crea una tabla de simbolos con una entrada para la variable del for
  # Se bloquea la modificacion de dicha variable
  global error
  anterior = fueDeclarada(p[1])
  #if anterior is not None:
    #col = find_column(p.slice[1].lexer.lexdata,p.slice[1])
    #print '''Error: Linea %d, columna %d: Variable del FOR "%s" ya fue declarada'''  % (p.lineno(1),col,p[1])
    #error = 1
  tabla = SymTable.SymTable()
  tabla.insert(SymTable.variable(p[1],'int',1))
  listaTablas.append(tabla)
  
  

  
#Clase utilizada para representar una instruccion while en rangeX
class whilec(indentable):
    def __init__(self,cond,inst):
      self.cond = cond
      self.inst = inst
      
    def printArbol(self):
      self.printIndent()
      print "Ciclo while con condicion:"
      self.cond.level = self.level+1
      self.cond.printArbol()
      self.printIndent(),
      print "instrucciones del while: "
      #self.printIndent(),
      self.inst.level = self.level+1
      self.inst.printArbol()

#Regla de la gramatica que reconoce una instruccion while en rangeX
def p_Inst_While(p):
  '''Inst_While : INST_WHILE Expresion INST_DO Bloque_Inst 
  | INST_WHILE Expresion INST_DO Inst '''
  p[0] = whilec(p[2],p[4])

#Regla del parser que especifica que debe hacerse en caso de un 
#error en la entrada de un string o archivo al parser
def p_error(p):
    print "Error de sintaxis en la linea",
    print p.lineno -1 ,
    print ", columna: " + str(find_column(p.lexer.lexdata,p)),
    print ": token inesperado:",
    print p.value
    yacc.restart()

#
## Seccion para la ejecucion del codigo de RangeX a traves de Python
#

# Procedimiento que se encarga de ejecutar bloques de instrucciones
#def executeBlock(root):
  #print 'Nuevo bloque'
  #global listaTablas
  #listaTablas.append(root.tabla)
  #for i in root:
    #executeInstruction(i,root.tabla)
  #listaTablas.pop()
    
#def executeInstruction(i,tabla):
  #nombre = i.__class__.__name__
  #function = methodDict[str(nombre)]
  #if len(inspect.getargspec(function).args) == 1:
    #function(i)
  #else:
    #function(i,tabla)
    

#def executeAsignacion(i,tabla):
  #print 'Esta es una asignacion a ' + i.variable 
  #instanciaVariable = fueDeclarada(i.variable)
  #try:
    #print str(instanciaVariable.valor)
  #except AttributeError:
    #pass
  ##variable.valor = i.expresion.valor
  #instanciaVariable.valor = 42

#def executeIf(i):
  #print 'Este es un if'
  
#def executeSalida(i):
  #print 'Esta es una Salida'


## Variable global con un diccionario de los metodos que se ejecutan
## para cada instruccion de RangeX  
#methodDict = {
  #'bloque':executeBlock,  
  #'Asignacion':executeAsignacion,
  #'Salida':executeSalida,
  #'ifc':executeIf
  #}

def main():
  parser = yacc.yacc()

  if (len(sys.argv) != 2):
      print("Usage: python rangex.py nombreArchivo")
      return -1
    
  # Se abre el archivo con permisos de lectura
  string = str(open(str(sys.argv[1]),'r').read())
  result = parser.parse(string)
  try:
    global error
    if not error:
      #result.printArbol()
      result.ejecutar()
  except AttributeError:
    return
if __name__ == '__main__':
  main()
