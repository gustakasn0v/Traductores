Traductores e Interpretadores
=====================
Proyecto 1 : Interpretador del Lenguaje RangeX
Wilmer Bandres - carnet 1010055
Gustavo El Khoury - carnet 1010226

-)Descripción: Este proyecto consiste en implementar, utilizando el lenguaje
  imperativo Python, una versión simplificada de un interpretador para el 
  lenguaje RangeX, utilizando la herramienta Ply. Esto contempla los pasos de 
  Lexer, Parser, generador de AST, y generador de AST mejorado, 
  además de la interpretación en sí.
  
-)Entregas: Para este proyecto se contemplan 4 entregas. A continuación se listan
  los detalles más importantes sobre la implementación de cada una de estas entregas:
  
  -)Lexer: Utilizando ply, se definió un diccionario para las palabras reservadas,
    donde la clave es el propio string, y el valor es el nombre del token. Además
    se definieron tokens para los símbolos de comparación, asignación y demás. 
    Estos últimos elementos tienen sus especificación mediante expresiones regulares
    sencillas, mientras que las palabras reservadas y números se revisan con métodos.
    Luego se tiene un Main que analiza un texto secuencialmente e imprime
    información relevante de los tokens por pantalla
  
  -)Parser
  
  -)AST
 
  -)AST mejorado e interprete:
