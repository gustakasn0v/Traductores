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

    Copyright (C) 2014  Gustavo El Khoury <gustavoelkhoury@gmail.com>

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

    The full GPLv2 License can be fount at the root of the repo, in the 
    LICENSE file.
