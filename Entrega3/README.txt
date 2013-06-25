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

En cuanto a la verificación estática, se realizó utilizando 4 pilares importantes:

-) Tabla de símbolos: Se implementó una tabla de símbolos que se aplica a cada
bloque, si existe. En caso de que una declaración tenga más de una línea,
cada línea se convierte en una tabla de símbolos, y al final todas se unen
utilizando el método merge de SymTable. Estas tablas se empilan en una lista
global de tablas de símbolo, que se recorren desde el tope de la pila
(declaración más cercana) hasta arriba (declaración más lejana) para respetar
la precedencia de delcaraciones. Cuando se termina de analizar un bloque mediante
el parser, su tabla de símbolos es desempilada y asignada al bloque, pero no
vuelve a ser revisada en las futuras verificaciones. Esta asignación luego de 
desempilar se hace con el propósito de imprimir el AST con tablas de símbolos.
Las tablas son desempiladas pues, al cerrarse un bloque, ninguna instrucción
futura puede usar variables de ese bloque. Cada instrucción revisa si las variables
que usa (si hay) han sido declaradas anteriormente, e imprime mensajes de error
de hacer falta

-) Variable para los errores: Se usa una variable global que indica si ha ocurrido
algún error en la verificación. Si ocurrieron, no e imprime el AST

-) Expresiones auto-verificadas: Las expresiones con reglas distintas según el 
tipo de expresión vistas en la entrega 2 han sido reemplazadas por expresiones 
completamente genéricas, que luego se someten a una verificación recursiva que
determina, respetando las declaraciones de variables, si las expresiones
cumplen con un tipo dado. Esto se hace en dos partes: primero se determina
si una expresión está correctamente formulada, revisando que cada variable haya
sido declarada y que su tipo coincida con la definición de operadores según 
corresponda; y luego verificando que el resultado de las expresiones coincida
con el tipo de la variable a la que se quiere asignar. Para esto, las expresiones
tienen un atributo 'ok' que determina su validez, y un 'tipo' que determina si
son booleanas, aritméticas o rangos.

-Declaraciones de variables con su posición: Cada vez que se declara una variable,
se almacena la posición (fila y columna) de la declaración, accediendo al
atributo público slice de las YaccProduction, que contiene una pila con las instancias
de los tokens que fueron usados al reducir dicha regla. Esto es vital
para imprimir los errores.


En adición a realizar las verificaciones estáticas que se solicitaron, el
programa también valida las expresiones que se encuentran dentro de una
instrucción rtoi, top, bottom y length, validando que resulten en rangos.
Además, verifica que su uso en una expresión permita que la expresión sea
válida
