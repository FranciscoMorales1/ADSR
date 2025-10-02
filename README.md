# Gramáticas y Parsers — Paso a Paso

Este repo resuelve **tres ejercicios** de gramáticas. Para cada uno se muestra:

1) **Gramática original**  
2) **Eliminación de recursividad por la izquierda** (si aplica)  
3) **Procedimientos paso a paso**  
   - 3.1. No terminales anulables (ε)  
   - 3.2. Conjuntos **PRIMEROS (FIRST)**  
   - 3.3. Conjuntos **SIGUIENTES (FOLLOW)**  
   - 3.4. **Predicción** por producción (lookahead)  
   - 3.5. ¿Es **LL(1)**? (detección de colisiones)  
4) **Tipo de parser a usar** (predictivo o con retroceso)  

> Convención: terminales = `uno, dos, tres, cuatro, cinco, seis, siete`.  
> `$` = fin de cadena, `ε` = cadena vacía.

---

## Ejercicio 1

### 0) Gramática **original**
S → A B C
S → D E
A → dos B tres | ε
B → B cuatro C cinco | ε
C → seis A B | ε
D → uno A E | B
E → tres

perl
Copiar código

### 1) Eliminar recursividad por la izquierda
`B` es recursiva inmediata: `B → B α | ε`, con `α = cuatro C cinco`.

Transformación estándar:
B → B'
B' → cuatro C cinco B' | ε

markdown
Copiar código

> El resto de reglas se mantiene igual:
S → A B C | D E
A → dos B tres | ε
C → seis A B | ε
D → uno A E | B
E → tres

markdown
Copiar código

---

### 2) Procedimientos

#### 2.1. **Anulables (ε)**
- `A, B, B', C` pueden ⇒ ε por producción directa.  
- `D` también puede ⇒ ε (porque `D → B` y `B ⇒ ε`).  
- `E` **no** es anulable; `S` sí **puede** ⇒ ε vía `S → A B C` (todas anulables).

#### 2.2. **PRIMEROS (FIRST)**
- `FIRST(A) = { dos, ε }`
- `FIRST(B') = { cuatro, ε }` ⇒ `FIRST(B) = FIRST(B') = { cuatro, ε }`
- `FIRST(C) = { seis, ε }`
- `FIRST(D) = { uno } ∪ FIRST(B) = { uno, cuatro, ε }`
- `FIRST(E) = { tres }`
- `FIRST(S) = FIRST(A B C) ∪ FIRST(D E)`  
  - `FIRST(A B C) = { dos } ∪ { cuatro } ∪ { seis } ∪ {ε}`  
    (A, B, C son anulables)
  - `FIRST(D E) = { uno, cuatro, tres }` (D puede ser ε, entonces entra `tres`)
  - **Resultado:** `FIRST(S) = { dos, cuatro, seis, uno, tres, ε }`

#### 2.3. **SIGUIENTES (FOLLOW)**
Reglas (resumen):  
- `FOLLOW(S) = { $ }`  
- En `S → A B C`:  
  - `FOLLOW(A) ⊇ FIRST(B C)−{ε} = { cuatro, seis }` y, como `B C` ⇒ ε, `FOLLOW(A) ⊇ FOLLOW(S) = { $ }`  
  - `FOLLOW(B) ⊇ FIRST(C)−{ε} = { seis }` y, como `C ⇒ ε`, `FOLLOW(B) ⊇ FOLLOW(S) = { $ }`  
  - `FOLLOW(C) ⊇ FOLLOW(S) = { $ }`  
- `A → dos B tres` ⇒ `FOLLOW(B) ⊇ { tres }`
- `B → B cuatro C cinco` ⇒ `FOLLOW(B) ⊇ { cuatro }` y `FOLLOW(C) ⊇ { cinco }`
- `C → seis A B` ⇒ `FOLLOW(A) ⊇ FIRST(B)−{ε} = { cuatro }` y, como `B ⇒ ε`, `FOLLOW(A) ⊇ FOLLOW(C)`
- `S → D E` ⇒ `FOLLOW(D) ⊇ { tres }` y `FOLLOW(E) ⊇ FOLLOW(S) = { $ }`
- `D → B` ⇒ `FOLLOW(B) ⊇ FOLLOW(D)`

**Resultado final:**
- `FOLLOW(S) = { $ }`
- `FOLLOW(A) = { cuatro, seis, tres, cinco, $ }`
- `FOLLOW(B) = { seis, tres, cuatro, cinco, $ }`
- `FOLLOW(C) = { cinco, $ }`
- `FOLLOW(D) = { tres }`
- `FOLLOW(E) = { tres, $ }`

#### 2.4. **Predicción** `P(A→α) = FIRST(α)−{ε} ∪ (FOLLOW(A) si α⇒ε)`
- `S → A B C` : `{ dos, cuatro, seis } ∪ { $ }` (porque `A B C ⇒ ε`)
- `S → D E`   : `{ uno, cuatro, tres }`

- `A → dos B tres` : `{ dos }`
- `A → ε`          : `FOLLOW(A) = { cuatro, seis, tres, cinco, $ }`

- `B → B'`         : `FIRST(B')−{ε} ∪ FOLLOW(B) = { cuatro } ∪ { seis, tres, cuatro, cinco, $ }`
- `B' → cuatro C cinco B'` : `{ cuatro }`
- `B' → ε`         : `FOLLOW(B') = FOLLOW(B) = { seis, tres, cuatro, cinco, $ }`

- `C → seis A B` : `{ seis }`
- `C → ε`        : `FOLLOW(C) = { cinco, $ }`

- `D → uno A E` : `{ uno }`
- `D → B`       : `FIRST(B)−{ε} ∪ FOLLOW(D) = { cuatro } ∪ { tres } = { cuatro, tres }`

- `E → tres` : `{ tres }`

#### 2.5. ¿**LL(1)**?
No. Hay **colisiones** claras, p. ej. en `S` (símbolo `cuatro` aparece en ambas alternativas), y en `B'` (`cuatro` también está en `FOLLOW(B')`).  

### 3) **Tipo de parser**  
➡️ **ASDR con retroceso** (no predictivo).

---

## Ejercicio 2

### 0) Gramática **original**
S → B uno | dos C | ε
A → S tres B C | cuatro | ε
B → A cinco C seis | ε
C → siete B | ε

markdown
Copiar código

(No requiere eliminación de recursividad.)

### 1) Procedimientos

#### 1.1. **Anulables**
`S, A, B, C` son anulables (todas tienen `ε`).

#### 1.2. **PRIMEROS**
- `FIRST(C) = { siete, ε }`
- `FIRST(A) = { cuatro } ∪ FIRST(S)−{ε} ∪ { tres si S⇒ε } ∪ { ε }`
- `FIRST(B) = FIRST(A)−{ε} ∪ { cinco si A⇒ε } ∪ { ε }`
- `FIRST(S) = FIRST(B)−{ε} ∪ { uno si B⇒ε } ∪ { dos } ∪ { ε }`

Resolviendo iterativamente, se obtiene:
- `FIRST(S) = { dos, uno, tres, cuatro, cinco, ε }`
- `FIRST(A) = { cuatro, dos, uno, tres, cinco, ε }`
- `FIRST(B) = { cuatro, dos, uno, tres, cinco, ε }`
- `FIRST(C) = { siete, ε }`

#### 1.3. **SIGUIENTES**
- `FOLLOW(S) = { $, tres }` (inicial y por `A → S tres …`)
- `FOLLOW(A) = { cinco }` (por `B → A cinco …`)
- `FOLLOW(C) = { $, cinco, seis, tres }`  
  (`S → dos C`, `A → … B C`, `B → … C seis`)
- `FOLLOW(B) = { uno, siete, seis, tres, cinco, $ }`  
  (`S → B uno`, `A → … B C`, `C → siete B`, más `FOLLOW(C)`)

#### 1.4. **Predicción**
- `S → B uno` : `{ cuatro, dos, uno, tres, cinco }`
- `S → dos C` : `{ dos }`
- `S → ε`     : `{ $, tres }`

- `A → S tres B C` : `{ cuatro, dos, uno, tres, cinco }`
- `A → cuatro`     : `{ cuatro }`
- `A → ε`          : `{ cinco }`

- `B → A cinco C seis` : `{ cuatro, dos, uno, tres, cinco }`
- `B → ε`               : `{ uno, siete, seis, tres, cinco, $ }`

- `C → siete B` : `{ siete }`
- `C → ε`       : `{ $, cinco, seis, tres }`

#### 1.5. ¿**LL(1)**?
No. Hay intersecciones (p. ej., en `S`: `dos` aparece en dos alternativas).

### 2) **Tipo de parser**  
➡️ **ASDR con retroceso** (no predictivo).

---

## Ejercicio 3

### 0) Gramática **original**
S → A B C
S → S uno
A → dos B C | ε
B → C tres | ε
C → cuatro B | ε

perl
Copiar código

### 1) Eliminar recursividad por la izquierda
En `S`:
S → A B C S'
S' → uno S' | ε

markdown
Copiar código
Las demás reglas quedan iguales.

### 2) Procedimientos

#### 2.1. **Anulables**
`A, B, C, S'` son anulables; consecuentemente `S` también puede anularse.

#### 2.2. **PRIMEROS**
- `FIRST(A) = { dos, ε }`
- `FIRST(C) = { cuatro, ε }`
- `FIRST(B) = FIRST(C tres) ∪ {ε} = ({ cuatro } ∪ { tres }) ∪ { ε } = { cuatro, tres, ε }`
- `FIRST(S') = { uno, ε }`
- `FIRST(S) = FIRST(A B C S') = { dos, cuatro, tres, uno, ε }`

#### 2.3. **SIGUIENTES**
De `S → A B C S'`:
- `FOLLOW(A) ⊇ { cuatro, tres, uno } ∪ { $ }`
- `FOLLOW(B) ⊇ { cuatro, uno } ∪ { $ }`
- `FOLLOW(C) ⊇ { uno } ∪ { $ }`
- `FOLLOW(S') ⊇ { $ }`

De `A → dos B C`:
- `FOLLOW(B) ⊇ { cuatro } ∪ FOLLOW(A)`
- `FOLLOW(C) ⊇ FOLLOW(A)`

De `B → C tres`:
- `FOLLOW(C) ⊇ { tres }`

De `C → cuatro B`:
- `FOLLOW(B) ⊇ FOLLOW(C)`

**Resultado final (cerrado):**
- `FOLLOW(S)  = { $ }`
- `FOLLOW(A)  = { cuatro, tres, uno, $ }`
- `FOLLOW(B)  = { cuatro, uno, tres, $ }`
- `FOLLOW(C)  = { cuatro, tres, uno, $ }`
- `FOLLOW(S') = { $ }`

#### 2.4. **Predicción**
- `S → A B C S'` : `{ dos, cuatro, tres, uno } ∪ { $ }`
- `S' → uno S'`  : `{ uno }`
- `S' → ε`       : `{ $ }`

- `A → dos B C` : `{ dos }`
- `A → ε`       : `FOLLOW(A) = { cuatro, tres, uno, $ }`

- `B → C tres` : `{ cuatro, tres }`
- `B → ε`      : `FOLLOW(B) = { cuatro, uno, tres, $ }`

- `C → cuatro B` : `{ cuatro }`
- `C → ε`        : `FOLLOW(C) = { cuatro, tres, uno, $ }`

#### 2.5. ¿**LL(1)**?
No. Por ejemplo, en `B` hay intersección entre `{ cuatro, tres }` y `FOLLOW(B)` (contiene `cuatro` y `tres`).  

### 3) **Tipo de parser**  
➡️ **ASDR con retroceso** (aun sin recursividad por la izquierda, no queda LL(1)).

---

## Resumen de tipo de parser

| Ejercicio | ¿LL(1)? | Parser recomendado |
|-----------|---------|--------------------|
| 1         | No      | ASDR con **retroceso** |
| 2         | No      | ASDR con **retroceso** |
| 3         | No (tras eliminar rec. izq.) | ASDR con **retroceso** |

---

## Cómo correr

Cada parser está en un archivo Python independiente.  
Ejecuta, por ejemplo:

```bash
python parser_ej1.py
python parser_ej2.py
python parser_ej3.py
