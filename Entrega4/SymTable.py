# -*- coding: utf-8 -*-
# Proyecto Traductores e Interpretadores. Entrega 2
# Clase para la tabla de símbolos
# Realizado por:
# Wilmer Bandres. 1010055
# Gustavo El Khoury. 1010226

# Clase para la delcaración de una variable
# Almacena el tipo de la variable, su iddentificador,
# su nivel de indentacion al imprimirse y su posición en el archivo

class variable():
  def __init__(self,id,type,block = None):
    self.id = id
    self.type = type
    self.indent = ''
    self.lineno = -1
    self.colno = -1
    if block is None:
      self.blocked = 0
    else:
      self.blocked = block    
      
  def setLine(self,line):
    self.lineno = line
  
  def setColumn(self,col):
    self.colno = col
    
  def setType(self,type):
    self.type = type

  def __eq__(self,otro):
    return self.id == otro.id
  
  def __str__(self):
    retorno = self.indent + "variable: " + str(self.id) + " | tipo: " + str(self.type)
    try:
      retorno = retorno + " | valor: " + str(self.valor)
    except ValueError:
      pass
    return retorno
  
# Clase para la tabla de símbolos. Almacena una lista de variables, y una indentación
# que se usa al imprimirse
class SymTable():
  def __init__(self):
    self.lista = []
    self.indent=''
    
  def insert(self,var):
    error = 0
    if self.isMember(var.id,0):
      error = 1
    else:
      self.lista.append(var)
    return error
    
  def delete(self,var):
    if self.isMember(var.id,0):
      self.lista.remove(var)
    
  def update(self,var):
    pass
  
  # El parametro verbose indica si debe imprimirse errores en pantalla
  def isMember(self,var,verbose):
    try:
      self.lista.index(variable(var,''))
    except ValueError:
      if verbose:
	print "El valor no se encuentra en la tabla de simbolos"
      return 0
    return 1
    
  def find(self,id):
    if self.isMember(id,0):
      return self.lista[self.lista.index(variable(id,''))]
    else:
      return None
    
  # Este procedimiento hacer merge dos tablas de símblos. Si hay símbolos
  # repetidos, retorna una tupla con la posición de la variable repetida. De
  # lo contrario retorna None
  
  def merge(self,nuevaTabla):
    error = None
    for i in nuevaTabla.lista:
      if self.isMember(i.id,0):
	error = (i.lineno,i.colno,i.id)
      else:
	self.insert(i)
    return error
	
  def __str__(self):
    self.indent = self.indent + '  '
    retorno = self.indent + 'Tabla de simbolos:\n'
    
    for i in self.lista:
      i.indent = self.indent
      retorno += str(i)
      retorno += '\n'
    retorno = retorno + self.indent +'---\n'
    return retorno

