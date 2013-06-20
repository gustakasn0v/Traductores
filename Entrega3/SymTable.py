# -*- coding: utf-8 -*-
# Proyecto Traductores e Interpretadores. Entrega 2
# Realizado por:
# Wilmer Bandres. 1010055
# Gustavo El Khoury. 1010226

class variable():
  def __init__(self,id,type):
    self.id = id
    self.type = type
  
  def __eq__(self,otro):
    return self.id == otro.id
  
  def __str__(self):
    return "variable: " + str(self.id) + " | tipo: " + str(self.type)
  

class SymTable():
  def __init__(self):
    self.lista = []
    
  def insert(self,var):
    self.lista.append(var)
    
  def delete(self,var):
    if self.isMember(var,0):
      self.lista.remove(var)
    
  def update(self,var):
    pass
  
  def isMember(self,var,verbose):
    try:
      self.lista.index(var)
    except ValueError:
      if verbose:
	print "El valor no se encuentra en la tabla de simbolos"
      return 0
    return 1
    
  def find(self,id):
    if self.isMember(variable(id,''),0):
      return self.lista[self.lista.index(variable(id,''))]
    else:
      return None
    
  def merge(self,nuevaTabla):
    for i in nuevaTabla.lista:
      if self.isMember(i,0):
	print 'Variable declarada dos veces'
      else:
	self.insert(i)
	
  def __str__(self):
    retorno = ''
    for i in self.lista:
      retorno += str(i)
      retorno += '\n'
    return retorno

#lista = SymTable()
#lista.insert(variable('xx1','boolean'))
#print lista.isMember(variable('xx1','boolean'),0)
#lista.delete(variable('xx1','boolean'))
#print lista.isMember(variable('xx1','boolean'),0)
#lista.insert(variable('xx1','boolean'))
#print lista.find('xx12')

