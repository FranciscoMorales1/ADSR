# Gramáticas y Parsers — Resolución paso a paso

Terminales: `uno, dos, tres, cuatro, cinco, seis, siete`  
No terminal inicial: se indica en cada ejercicio.  
Símbolos: `ε` = cadena vacía, `$` = fin de entrada.

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

markdown
Copiar código

### 1) Eliminación de recursividad por la izquierda (solo si existe)
Hay **recursividad inmediata** en `B`:
B → B (cuatro C cinco) | ε

less
Copiar código
Transformación estándar `B → Bα | ε`:
B → B' (equivalente a B → ε B')
B' → cuatro C cinco B' | ε

markdown
Copiar código
> El resto de reglas **no cambia**.

Gramática a analizar (post-transformación solo para `B`):
S → A B C | D E
A → dos B tres | ε
B → B'
B'→ cuatro C cinco B' | ε
C → seis A B | ε
D → uno A E | B
E → tres

markdown
Copiar código

### 2) No terminales **anulables** (derivan ε)
- `A` (tiene `ε`)
- `B'` (tiene `ε`) ⇒ `B` también es anulable
- `C` (tiene `ε`)
- `D` es anulable porque `D → B` y `B ⇒ ε`
- `S` puede anularse por `S → A B C` (todos anulables)
- `E` **no** es anulable

### 3) Conjuntos **PRIMEROS**
- `FIRST(E) = { tres }`
- `FIRST(A) = { dos, ε }`
- `FIRST(B') = { cuatro, ε }` ⇒ `FIRST(B) = { cuatro, ε }`
- `FIRST(C) = { seis, ε }`
- `FIRST(D) = { uno } ∪ FIRST(B) = { uno, cuatro, ε }`
- `FIRST(S) = FIRST(A B C) ∪ FIRST(D E)`  
  - `FIRST(A B C) = { dos, cuatro, seis, ε }` (A,B,C anulables)  
  - `FIRST(D E)   = { uno, cuatro, tres }` (si `D ⇒ ε`, entra `tres` por `E`)  
  - **Resultado:** `FIRST(S) = { dos, cuatro, seis, uno, tres, ε }`

### 4) Conjuntos **SIGUIENTES**
Reglas usadas:  
- Si `A → α B β`, entonces `FOLLOW(B) ⊇ FIRST(β) − {ε}` y si `β ⇒* ε` entonces `FOLLOW(B) ⊇ FOLLOW(A)`.  
- `FOLLOW(S) = { $ }` (símbolo inicial).

Cálculo (acumulado hasta cierre):
- `FOLLOW(S) = { $ }`
- De `S → A B C`:
  - `FOLLOW(A) ⊇ FIRST(B C)−{ε} = { cuatro, seis }` y como `B C ⇒ ε`, `FOLLOW(A) ⊇ FOLLOW(S) = { $ }`
  - `FOLLOW(B) ⊇ FIRST(C)−{ε} = { seis }`; como `C ⇒ ε`, `FOLLOW(B) ⊇ { $ }`
  - `FOLLOW(C) ⊇ FOLLOW(S) = { $ }`
- De `A → dos B tres`: `FOLLOW(B) ⊇ { tres }`
- De `B → B'` y `B' → cuatro C cinco B'`:
  - el `B` dentro de `B → B cuatro…` aporta `FOLLOW(B) ⊇ { cuatro }`
  - `FOLLOW(C) ⊇ { cinco }`
- De `C → seis A B`:
  - `FOLLOW(A) ⊇ FIRST(B)−{ε} = { cuatro }`
  - como `B ⇒ ε`, `FOLLOW(A) ⊇ FOLLOW(C)`
  - `FOLLOW(B) ⊇ FOLLOW(C)`
- De `S → D E`:
  - `FOLLOW(D) ⊇ FIRST(E) = { tres }`
  - `FOLLOW(E) ⊇ FOLLOW(S) = { $ }`
- De `D → uno A E`: `FOLLOW(A) ⊇ FIRST(E) = { tres }`; `FOLLOW(E) ⊇ FOLLOW(D)`
- De `D → B`: `FOLLOW(B) ⊇ FOLLOW(D)`

**Cierre final:**
FOLLOW(S) = { $ }
FOLLOW(A) = { cuatro, seis, tres, cinco, $ }
FOLLOW(B) = { seis, tres, cuatro, cinco, $ }
FOLLOW(C) = { cinco, $ }
FOLLOW(D) = { tres }
FOLLOW(E) = { tres, $ }

markdown
Copiar código

### 5) Conjuntos de **PREDICCIÓN**  (por producción `A → α`)
`PRED(A→α) = FIRST(α)−{ε} ∪ (FOLLOW(A) si α ⇒* ε)`

- `S → A B C` : `{ dos, cuatro, seis } ∪ { $ }` (porque `A B C ⇒ ε`)
- `S → D E`   : `{ uno, cuatro, tres }`
- `A → dos B tres` : `{ dos }`
- `A → ε`          : `FOLLOW(A) = { cuatro, seis, tres, cinco, $ }`
- `B → B'`         : `FIRST(B')−{ε} ∪ FOLLOW(B) = { cuatro } ∪ { seis, tres, cuatro, cinco, $ }`
- `B'→ cuatro C cinco B'` : `{ cuatro }`
- `B'→ ε`                 : `FOLLOW(B') = FOLLOW(B) = { seis, tres, cuatro, cinco, $ }`
- `C → seis A B` : `{ seis }`
- `C → ε`        : `FOLLOW(C) = { cinco, $ }`
- `D → uno A E` : `{ uno }`
- `D → B`       : `FIRST(B)−{ε} ∪ FOLLOW(D) = { cuatro } ∪ { tres } = { cuatro, tres }`
- `E → tres` : `{ tres }`

### 6) ¿La gramática es **LL(1)**?
**No.** Hay colisiones, p. ej. en `B`/`B'` (el terminal `cuatro` aparece tanto en una producción no-ε como en la producción ε vía FOLLOW), y en `S` (`cuatro` se repite en ambas alternativas).

### 7) **Parser recomendado**
ASDR **con retroceso** (no predictivo).

---

## Ejercicio 2

### 0) Gramática **original**
S → B uno | dos C | ε
A → S tres B C | cuatro | ε
B → A cinco C seis | ε
C → siete B | ε

markdown
Copiar código

### 1) Anulables
Los cuatro no terminales (`S, A, B, C`) son anulables (cada uno tiene regla `ε` directa o indirecta).

### 2) Conjuntos **PRIMEROS**
- `FIRST(C) = { siete, ε }`
- `FIRST(A) = { cuatro } ∪ FIRST(S)−{ε} ∪ { tres si S⇒ε } ∪ { ε }`
- `FIRST(B) = FIRST(A)−{ε} ∪ { cinco si A⇒ε } ∪ { ε }`
- `FIRST(S) = FIRST(B)−{ε} ∪ { uno si B⇒ε } ∪ { dos } ∪ { ε }`

Resolviendo iterativamente (hasta cierre):
FIRST(S) = { dos, uno, tres, cuatro, cinco, ε }
FIRST(A) = { cuatro, dos, uno, tres, cinco, ε }
FIRST(B) = { cuatro, dos, uno, tres, cinco, ε }
FIRST(C) = { siete, ε }

markdown
Copiar código

### 3) Conjuntos **SIGUIENTES**
- `FOLLOW(S) = { $, tres }`  (inicial y por `A → S tres …`)
- `FOLLOW(A) = { cinco }`    (por `B → A cinco …`)
- `FOLLOW(C) = { $, cinco, seis, tres }`  (`S→dos C`, `A→… B C`, `B→… C seis`)
- `FOLLOW(B) = { uno, siete, seis, tres, cinco, $ }`  
  (`S→B uno`, `A→… B C`, `C→siete B`, más `FOLLOW(C)` cuando `C ⇒ ε`)

### 4) Conjuntos de **PREDICCIÓN**
S → B uno : { cuatro, dos, uno, tres, cinco }
S → dos C : { dos }
S → ε : { $, tres }

A → S tres B C : { cuatro, dos, uno, tres, cinco }
A → cuatro : { cuatro }
A → ε : { cinco }

B → A cinco C seis : { cuatro, dos, uno, tres, cinco }
B → ε : { uno, siete, seis, tres, cinco, $ }

C → siete B : { siete }
C → ε : { $, cinco, seis, tres }

markdown
Copiar código

### 5) ¿La gramática es **LL(1)**?
**No.** Hay intersecciones: por ejemplo en `S`, el terminal `dos` aparece en `S→B uno` y `S→dos C`; en `A`, el `cuatro` colisiona entre dos producciones.

### 6) **Parser recomendado**
ASDR **con retroceso**.

---

## Ejercicio 3

### 0) Gramática **original**
S → A B C
S → S uno
A → dos B C | ε
B → C tres | ε
C → cuatro B | ε

markdown
Copiar código

### 1) Eliminación de recursividad por la izquierda
`S` es recursiva inmediata (`S → S uno`). Transformación:
S → A B C S'
S' → uno S' | ε

markdown
Copiar código
Las reglas de `A, B, C` **no cambian**.

### 2) No terminales **anulables**
`A, B, C` son anulables (tienen `ε`).  
`S'` también es anulable (`ε`).  
Por tanto, `S` puede anularse a través de `A B C S'` (todas anulables).

### 3) Conjuntos **PRIMEROS**
- `FIRST(C) = { cuatro, ε }`
- `FIRST(B) = FIRST(C tres) ∪ { ε } = { cuatro, tres, ε }`
- `FIRST(A) = { dos, ε }`
- `FIRST(S')= { uno, ε }`
- `FIRST(S) = FIRST(A B C S') = { dos, cuatro, tres, uno, ε }`
  (si A=ε mira B; si A=ε y B=ε mira C; si A=B=C=ε mira S', etc.)

### 4) Conjuntos **SIGUIENTES**
De `S → A B C S'` y reglas de `A, B, C`:

- `FOLLOW(S)  = { $ }`
- `FOLLOW(A)  ⊇ FIRST(B C S')−{ε} = { cuatro, tres, uno }` y como `B C S' ⇒ ε`, también `{ $ }`
- `FOLLOW(B)  ⊇ FIRST(C S')−{ε} = { cuatro, uno }` y por anulabilidad de `C S'`, también `{ $ }`
- `FOLLOW(C)  ⊇ FIRST(S')−{ε} = { uno }` y como `S' ⇒ ε`, también `{ $ }`
- De `A → dos B C`:  
  `FOLLOW(B) ⊇ FIRST(C)−{ε} = { cuatro }` y como `C ⇒ ε`, `FOLLOW(B) ⊇ FOLLOW(A)`
- De `B → C tres`: `FOLLOW(C) ⊇ { tres }`
- De `C → cuatro B`: `FOLLOW(B) ⊇ FOLLOW(C)`

**Cierre final:**
FOLLOW(S) = { $ }
FOLLOW(A) = { cuatro, tres, uno, $ }
FOLLOW(B) = { cuatro, uno, tres, $ }
FOLLOW(C) = { uno, tres, $ }
FOLLOW(S') = { $ }

markdown
Copiar código

### 5) Conjuntos de **PREDICCIÓN**
- `S  → A B C S'` : `FIRST(A B C S')−{ε} ∪ FOLLOW(S) = { dos, cuatro, tres, uno } ∪ { $ }`
- `S' → uno S'`   : `{ uno }`
- `S' → ε`        : `FOLLOW(S') = { $ }`

- `A → dos B C`   : `{ dos }`
- `A → ε`         : `FOLLOW(A) = { cuatro, tres, uno, $ }`

- `B → C tres`    : `FIRST(C tres) = { cuatro, tres }`
- `B → ε`         : `FOLLOW(B) = { cuatro, uno, tres, $ }`

- `C → cuatro B`  : `{ cuatro }`
- `C → ε`         : `FOLLOW(C) = { uno, tres, $ }`

### 6) ¿La gramática es **LL(1)**?
**No.** Hay **colisiones** en `B`:
- `PRED(B→C tres) = { cuatro, tres }`
- `PRED(B→ε)      = { cuatro, uno, tres, $ }`
Intersección: `{ cuatro, tres }` → conflicto.  
> *(Aclaración: si solo se mirara la eliminación de recursividad en `S`, podría parecer LL(1); el conflicto aparece al cerrar `FIRST/FOLLOW` en `B`.)*

### 7) **Parser recomendado**
ASDR **con retroceso**.

---

## Resumen final (tipo de parser)
| Ejercicio | ¿LL(1)? | Parser recomendado |
|-----------|---------|--------------------|
| 1         | No      | ASDR con **retroceso** |
| 2         | No      | ASDR con **retroceso** |
| 3         | No      | ASDR con **retroceso** |

---

## Nota sobre implementación
- **Entrada** de un ASDR: lista de tokens del alfabeto `{uno, dos, tres, cuatro, cinco, seis, siete}`.  
- **Salida**: aceptación/rechazo (y opcionalmente el árbol de derivación si se implementa).  
- Para estas tres gramáticas, un **ASDR predictivo puro (LL(1))** no es suficiente; se requiere **retroceso** o re-factorización adicional de las gramáticas para hacerlas LL(1).
