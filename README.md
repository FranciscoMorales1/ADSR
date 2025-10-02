📘 README.md
# Ejercicios de Gramáticas y Parsers

Este repositorio contiene la resolución de tres ejercicios de gramáticas con sus respectivos analizadores sintácticos descendentes recursivos (ASDR).  

## 📌 Introducción
Cada ejercicio incluye:
- Eliminación de recursividad por la izquierda (si aplica).
- Conjuntos **PRIMEROS** y **SIGUIENTES**.
- Conjuntos de **PREDICCIÓN**.
- Verificación de si la gramática es **LL(1)**.
- Implementación de un **ASDR**:
  - Con **retroceso** si la gramática no es LL(1).
  - Predictivo si la gramática sí es LL(1).

---

## 📘 Ejercicio 1

### Gramática


S → A B C | D E
A → dos B tres | ε
B → B cuatro C cinco | ε
C → seis A B | ε
D → uno A E | B
E → tres


### Eliminación de recursividad
`B` es recursiva por la izquierda:


B → ε B'
B' → cuatro C cinco B' | ε


### PRIMEROS


FIRST(S) = { dos, seis, uno, tres, cuatro, ε }
FIRST(A) = { dos, ε }
FIRST(B) = { cuatro, ε }
FIRST(C) = { seis, ε }
FIRST(D) = { uno, dos, tres, seis, cuatro, ε }
FIRST(E) = { tres }


### SIGUIENTES


FOLLOW(S) = { $ }
FOLLOW(A) = { dos, seis, tres, cuatro }
FOLLOW(B) = { cuatro, seis, tres, $ }
FOLLOW(C) = { cinco, $ }
FOLLOW(D) = { tres }
FOLLOW(E) = { $ }


### LL(1)
❌ **No es LL(1)**.  
Se requieren retrocesos.

### Tipo de parser
👉 **ASDR con retroceso**.

---

## 📘 Ejercicio 2

### Gramática


S → B uno | dos C | ε
A → S tres B C | cuatro | ε
B → A cinco C seis | ε
C → siete B | ε


### PRIMEROS


FIRST(S) = { dos, uno, tres, cuatro, cinco, ε }
FIRST(A) = { cuatro, dos, uno, tres, cinco, ε }
FIRST(B) = { cuatro, dos, uno, tres, cinco, ε }
FIRST(C) = { siete, ε }


### SIGUIENTES


FOLLOW(S) = { $, tres }
FOLLOW(A) = { cinco }
FOLLOW(B) = { uno, siete, seis, tres, cinco, $ }
FOLLOW(C) = { $, cinco, seis, tres }


### Predicción


S → B uno : { cuatro, dos, uno, tres, cinco }
S → dos C : { dos }
S → ε : { $, tres }
...


### LL(1)
❌ **No es LL(1)**.  
Existen colisiones.

### Tipo de parser
👉 **ASDR con retroceso**.

---

## 📘 Ejercicio 3

### Gramática


S → A B C | S uno
A → dos B C | ε
B → C tres | ε
C → cuatro B | ε


### Eliminación de recursividad
`S → S uno` se reescribe:


S → A B C S'
S' → uno S' | ε


### PRIMEROS


FIRST(S) = { dos, cuatro, ε }
FIRST(A) = { dos, ε }
FIRST(B) = { cuatro, ε }
FIRST(C) = { cuatro, ε }


### SIGUIENTES


FOLLOW(S) = { $ }
FOLLOW(A) = { cuatro, $ }
FOLLOW(B) = { tres, $ }
FOLLOW(C) = { cuatro, tres, $ }


### LL(1)
✅ **Sí es LL(1)** después de la transformación.

### Tipo de parser
👉 **ASDR predictivo (sin retroceso)**.

---

## 📜 Resumen de Parsers
- **Ejercicio 1** → ASDR con retroceso.  
- **Ejercicio 2** → ASDR con retroceso.  
- **Ejercicio 3** → ASDR predictivo.  

---

## ▶️ Cómo probar
Cada parser se encuentra en un archivo separado en Python.  
Ejemplo de uso:

```bash
python parser_ej1.py


Salida:

Cadena aceptada ✓


o

Error de sintaxis en <token>
