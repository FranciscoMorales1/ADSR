Introducción

Este documento resuelve los tres ejercicios de gramáticas propuestos.
Cada ejercicio incluye:

Eliminación de recursividad por la izquierda (si aplica).

Cálculo de los conjuntos de PRIMEROS y SIGUIENTES.

Cálculo de los conjuntos de PREDICCIÓN.

Determinación de si la gramática es LL(1).

Definición del tipo de parser a usar (predictivo o con retroceso).

Ejercicio 1
Gramática
S → A B C | D E
A → dos B tres | ε
B → B cuatro C cinco | ε
C → seis A B | ε
D → uno A E | B
E → tres

a) Eliminación de recursividad por la izquierda

B → B cuatro C cinco | ε tiene recursividad por la izquierda.
Se reescribe como:

B → ε B'
B' → cuatro C cinco B' | ε

b) Conjuntos PRIMEROS
FIRST(S) = { dos, seis, uno, tres, cuatro, ε }
FIRST(A) = { dos, ε }
FIRST(B) = { cuatro, ε }
FIRST(C) = { seis, ε }
FIRST(D) = { uno, dos, tres, seis, cuatro, ε }
FIRST(E) = { tres }

c) Conjuntos SIGUIENTES
FOLLOW(S) = { $ }
FOLLOW(A) = { dos, seis, tres, cuatro, ε }
FOLLOW(B) = { cuatro, seis, tres, $ }
FOLLOW(C) = { cinco, $ }
FOLLOW(D) = { tres }
FOLLOW(E) = { $ }

d) Conjuntos de predicción

Cada producción genera PRED según FIRST y FOLLOW.
(Ejemplo: S → A B C → { dos, seis, cuatro, tres, ε }).

e) ¿Es LL(1)?

No es LL(1), porque hay conflictos entre las producciones de S y D.

f) Tipo de parser

👉 Se debe usar ASDR con retroceso.

Ejercicio 2
Gramática
S → B uno | dos C | ε
A → S tres B C | cuatro | ε
B → A cinco C seis | ε
C → siete B | ε

a) Conjuntos PRIMEROS
FIRST(S) = { dos, uno, tres, cuatro, cinco, ε }
FIRST(A) = { cuatro, dos, uno, tres, cinco, ε }
FIRST(B) = { cuatro, dos, uno, tres, cinco, ε }
FIRST(C) = { siete, ε }

b) Conjuntos SIGUIENTES
FOLLOW(S) = { $, tres }
FOLLOW(A) = { cinco }
FOLLOW(B) = { uno, siete, seis, tres, cinco, $ }
FOLLOW(C) = { $, cinco, seis, tres }

c) Conjuntos de predicción
S → B uno      : { cuatro, dos, uno, tres, cinco }
S → dos C      : { dos }
S → ε          : { $, tres }

A → S tres B C : { cuatro, dos, uno, tres, cinco }
A → cuatro     : { cuatro }
A → ε          : { cinco }

B → A cinco C seis : { cuatro, dos, uno, tres, cinco }
B → ε               : { uno, siete, seis, tres, cinco, $ }

C → siete B : { siete }
C → ε       : { $, cinco, seis, tres }

d) ¿Es LL(1)?

No es LL(1). Hay colisiones (dos, tres, cuatro aparecen en varias predicciones).

e) Tipo de parser

👉 Se debe usar ASDR con retroceso.

Ejercicio 3
Gramática
S → A B C | S uno
A → dos B C | ε
B → C tres | ε
C → cuatro B | ε

a) Eliminación de recursividad por la izquierda

S → S uno es recursiva por la izquierda.
Reescribimos:

S → A B C S'
S' → uno S' | ε

b) Conjuntos PRIMEROS
FIRST(S) = { dos, cuatro, ε }
FIRST(A) = { dos, ε }
FIRST(B) = { cuatro, ε }
FIRST(C) = { cuatro, ε }

c) Conjuntos SIGUIENTES
FOLLOW(S) = { $ }
FOLLOW(A) = { cuatro, $ }
FOLLOW(B) = { tres, $ }
FOLLOW(C) = { cuatro, tres, $ }

d) Conjuntos de predicción

Con la gramática transformada no hay colisiones.

e) ¿Es LL(1)?

✅ Sí es LL(1) después de eliminar recursividad.

f) Tipo de parser

👉 Se puede usar ASDR predictivo (sin retroceso).

📌 Resumen de tipos de parser

Ejercicio 1 → ASDR con retroceso.

Ejercicio 2 → ASDR con retroceso.

Ejercicio 3 → ASDR predictivo (LL(1) válido).
