# -*- coding: utf-8 -*-
# Proyecto Traductores e Interpretadores. Entrega 2
# Realizado por:
# Wilmer Bandres. 1010055
# Gustavo El Khoury. 1010226
# -*- coding: utf-8 -*-

import ply.yacc as yacc
import ply.lex as lex
import sys
from lexer import tokens, find_column


#Esta es una clase que sera utilizada para herencia posteriormente
#Para facilitar la indentacion y asi hacer mas visible la salida
class indentable:
  #este atributo indica cuantos espacios se deben hacer
  level = 0
  def printIndent(self):
    for i in range(self.level):
      print('  '),
    return ''

    
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
    
  def printArbol(self):
    self.printIndent(),
    print self.nombre
    for i in self.contenido:
      i.level = self.level+1
      i.printArbol()
    
    
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
      if p[3]=='end':
	p[0] = bloque('BLOQUE',[p[2]])
      else:
	p[0] = bloque('BLOQUE',[p[2],p[3]])
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
  | Inst_Funcion 
  | Bloque_Inst
  '''
  p[0] = p[1]
  p[0].level = p[1].level
  

#Clase utilizada para representar una instruccion que hace llamada
#a una funcion
class InstFuncion(indentable):
  def __init__(self,func,var):
    self.funcion = func
    self.var = var
  def printArbol(self):
    #print "mi nivel es " + str(self.level)
    self.printIndent(),
    print "Funcion: " + self.funcion
    self.printIndent(),
    print "Expresion: ",
    self.var.printArbol()
    
    
#Regla del parser que se utiliza para la representacion de una funcion
#La cual actua sobre un rango o tambien puede actuar sobre
#una variable si esta es de tipo rango (aunque por ahora no nos
#interesa el tipo del mismo ya que estamos construyendo un AST)
def p_Inst_Funcion(p):
  ''' Inst_Funcion : RTOI LPAREN Rango RPAREN 
  | LENGTH LPAREN Rango RPAREN
  | TOP LPAREN Rango RPAREN
  | BOTTOM LPAREN Rango RPAREN 
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
    # Esta es una lista de cada linea del declare
    self.listaDeclaraciones = listaDeclaraciones
    
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
    self.listaVariables = listaVariables
    self.tipo = tipo
    
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
      print i +",",

#Regla de la gramatica utilizada para reconocer una declaracion de
#variables asi como sus tipos
def p_Inst_Declare(p):
  '''Inst_Declare : INST_DECLARE Lista_DeclareTipos'''
  p[0] = bloqueDeclaracion(p[2])

  
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
    

#Regla de la gramatica que representa una lista de variables
def p_Lista_Variables(p):
  '''Lista_Variables : VAR_IDENTIFIER
  | VAR_IDENTIFIER COMMA Lista_Variables '''
  
  if(len(p)>=3):
    p[3].lista.insert(0,p[1])
    p[0] = listaVariables( p[3].lista)
  else:
    p[0] = listaVariables([p[1]])
  
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
    self.printIndent()
    print "A la variable: " + str(self.variable) + " se le asigna ",
    self.expresion.level = self.level
    self.expresion.printArbol()
    
#Regla de la gramatica utilizada para reconocer una asignacion
def p_Inst_Asignacion(p):
  '''Inst_Asignacion : VAR_IDENTIFIER EQUAL Expresion'''
  p[0] = Asignacion(p[1],p[3])

  
#Reglas de precedencia de los operadores permitidos por rangeX
precedence = (
    ('right','INST_ELSE'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('nonassoc', 'NOT'),
    ('nonassoc','LESS','LESSEQ' ,'GREAT','GREATEQ'),
    ('left','EQEQ' ,'NEQEQ'),
    ('nonassoc','IN'),
    ('left','INTERSECTION'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE','MOD'),
    ('nonassoc', 'RANGE'),
    ('right','UMINUS'),
) 

  
#Clase utilizada para representar una operacion realizable 
#en rangeX, esta misma clase representa operaciones binarias,
#unarias y variables o numeros
class Operacion(indentable):
  def __init__(self,left,opr="",right=""):
    self.left = left
    self.opr = opr
    self.right = right
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
      print "Operacion unaria:\n" 
      self.printIndent(),
      print "Operador: " + self.opr + "\n" 
      self.printIndent(),
      print "Operando: ",
      self.left.level = self.level+1
      self.left.printArbol()
    #Revisa si la instacia no es una operacion sino una variable o 
    #numero
    else:
      if type(self.left)==str and self.left!="true" and self.left!="false":
	print "Variable: ",
      else:
	print "Constante: ",
      print self.left
  
#Esta es la regla de la gramatica que reconoce las expresiones 
#permitidas en rangeX, estas pueden ser binarias (que para nuestros
#efectos representa en realidad una operacion arimetica), 
#operacion booleana o un rango
def p_Expresion(p):
  '''Expresion : Operacion_binaria
  | Rango'''
  #| Operacion_booleana 
  p[0] = p[1]

##Regla que permite reconocer una operacion booleana en 
##rangeX
#def p_Operacion_booleana(p):
  #''' Operacion_booleana : Operacion_binaria Opr_bool Operacion_binaria
  #| Operacion_booleana AND Operacion_booleana 
  #| Operacion_booleana OR Operacion_booleana 
  #| Operacion_binaria IN Rango
  #| LPAREN Operacion_booleana RPAREN
  #| Operacion_booleana EQEQ Operacion_booleana
  #| Operacion_booleana NEQEQ Operacion_booleana
  #| Operacion_binaria EQEQ Operacion_binaria
  #| Operacion_binaria NEQEQ Operacion_binaria
  #| TRUE
  #| FALSE
  #| VAR_IDENTIFIER
  #| NOT Operacion_booleana '''

  #if len(p)>=3:
    ##Revisa si la operacion no esta entre parentesis y no es un not
    #if p[1]!='(' and p[1]!="not":
      #p[0] = Operacion(p[1],p[2],p[3])
    ##Si la operacion es un not se hace una operacion unaria con la 
    ##expresion reconocida de segunda
    #elif p[1]=="not":
      #p[0] = Operacion(p[2],p[1])
    ##La expresion reconocida esta entre parentesis y por lo tanto
    ##Le asigno a p el valor del valor que esta en medio de los parentesis
    #else:
      #p[0]=p[2]
  #else: 
    #p[0] = Operacion(p[1])

##Regla de la gramatica utilizada para reconocer los operadores no 
##asociativos de rangeX
#def p_Opr_bool(p):
  #''' Opr_bool : GREAT
  #| LESS
  #| GREATEQ
  #| LESSEQ '''
  #p[0] = p[1]

#Regla de la gramatica utilizada para reconocer una operacion
#aritmetica
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
  | Operacion_binaria IN Rango
  | NOT Operacion_binaria
  | NUMBER
  | VAR_IDENTIFIER
  | LPAREN Operacion_binaria RPAREN
  | Inst_Funcion
  | MINUS Operacion_binaria %prec UMINUS 
  | TRUE
  | FALSE'''
  if len(p)>=4:
    if p[1]=='(':
      p[0]=p[2]
    else:
      p[0] = Operacion(p[1],p[2],p[3])
  elif len(p)>=3:
    p[0] = Operacion(p[2],p[1])
  else:
    p[0] = Operacion(p[1])

##Regla del parser utilizada para reconocer una multiplicacion,
##una division o una operacion de modulo
#def p_Term(p):
  #'''Term : Term TIMES Factor
  #| Term DIVIDE Factor
  #| Term MOD Factor
  #| Factor'''
  #if len(p) ==4:
    #p[0] = Operacion(p[1],p[2],p[3])
  #elif len(p)==5:
    #p[0] = Operacion(Operacion(p[2],p[1]),p[3],p[4])
  #else:
	  #p[0] = p[1]

##Regla de la gramatica utilizada para reconocer un numero, una variable,
##algun menos unario con una expresion o una expresion entre parentesis
#def p_Factor(p):
  #''' Factor : NUMBER
  #| VAR_IDENTIFIER
  #| LPAREN Operacion_binaria RPAREN
  #| Inst_Funcion
  #| MINUS Factor %prec UMINUS 
  #| TRUE
  #| FALSE '''
  
  #if len(p)==4:
    #p[0] = p[2]
  #elif len(p)==3:
    #p[0] = Operacion(p[2],p[1])
  #elif type(p[1]) != str and type(p[1])!= int:  
    #p[0]= p[1]
  #else:
    #p[0] = Operacion(p[1])

    
#Regla de la gramatica utilizada para reoconocer un rango
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

#Clase utilizada para representar una instruccion de salida
#aceptada por rangeX
class Lectura(indentable):
  def __init__(self,var):
    self.variable = var
  
  def printArbol(self):
    self.printIndent(),
    print "Read de la variable: " + self.variable
    
#Regla de la gramatica utilizada para reconocer una instruccion
#de lectura
def p_Inst_Lectura(p):
  '''Inst_Lectura : INST_READ VAR_IDENTIFIER '''
  p[0] = Lectura(p[2])
  
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

      
#Esta clase se usa para facilitar la implementacion de las clases
#y reglas de la instruccion write de rangeX
class Aux(indentable):
  def __init__(self,tipo,valor):
    self.val = valor
    self.tipo = tipo
    
  def printArbol(self):
    self.val.level = self.level+1
    self.val.printArbol()


#Definicion de la regla de la grmaatica que reconoce la instruccion 
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
      self.printIndent(),
      self.bloque2.level+=1
      self.bloque2.printArbol()

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
  | Rango CASE_ASSIGN Bloque_Control SEMICOLON
  | VAR_IDENTIFIER CASE_ASSIGN Bloque_Control SEMICOLON Casos 
  | Rango CASE_ASSIGN Bloque_Control SEMICOLON Casos'''

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
      print "\tRango:"
      
      self.rango.level = self.level+2
      self.rango.printArbol()
      self.printIndent()
      print "\tBloque de instrucciones:" 
      self.inst.level = self.level + 3
      self.inst.printArbol()
      
      
#Regla del a gramatica utilizada para reconocer una instruccion for
#en rangeX
def p_Inst_For(p):
  '''Inst_For : INST_FOR VAR_IDENTIFIER INST_IN Rango INST_DO Bloque_Control '''
  p[0] = forc(p[2],p[4],p[6])

  
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
