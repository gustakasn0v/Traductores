A la hora de la realizacion del parser, lo primero que 
se hizo fue un analisis de toda la definicion del lenguaje 
para luego proceder con la realizacion de la gramatica.

A la hora de crear la gramatica se hizo de una forma descendente 
como esta presente en el mismo codigo, esto es, primero se dan las 
reglas mas generales (como por ejemplo los bloques de instrucciones) 
y luego se dan las reglas mas especificas (como por ejemplo los casos 
bases como VAR_IDENTIFIER en las expresiones binarias en el codigo).

Con respecto a la implementacion, se procedio a realizar una clase
(en algunos casos se realizaron dos clases) por cada regla del 
parser para poder facilitar la implementacion de la gramatica 
de atributos. Ademas, en cada clase se creo una funcion recursiva 
llamada printArbol que es utilizada para que la impresion de la 
de lo que se ha leido y que pasa por la gramatica se haga de 
forma correcta.

Por ultimo, con respecto a los problemas que posiblemente tenga
el parser, se cree que solo existe uno y es a la hora de la 
instruccion write o writeln ya que en la definicion del lenguaje
existe un ejemplo que dice ser valido donde esta la siguiente
linea:


	write x=10;


que se encuentra en la pagina 6 del documento de definicion del 
lenguaje. Sin embargo, el write implementado aca se hizo pensando
en que los argumentos del write deberian ser expresiones y no 
instrucciones como es el caso mostrado arriba. Esto fue pensado asi
debido a que si la sentencia dada arriba es valida entonces tambien
es valido colocar un write con un bloque completo de instrucciones 
con begin y end como argumento del write, y esto es justamente lo 
que no ha quedado claro.
