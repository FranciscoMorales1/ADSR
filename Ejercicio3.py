# Ejercicio 3 - ASDR con retroceso

class ParserEJ3:
    def __init__(self, tokens):
        self.tokens = tokens + ["$"]
        self.pos = 0

    def la(self):
        return self.tokens[self.pos]

    def match(self, t):
        if self.la() == t:
            self.pos += 1
        else:
            raise Exception(f"Error: esperaba {t}, se encontró {self.la()}")

    def S(self):
        self.A(); self.B(); self.C(); self.Sprima()

    def Sprima(self):
        if self.la() == "uno":
            self.match("uno"); self.Sprima()
        else:
            return  # ε

    def A(self):
        save = self.pos
        try:  # A → dos B C
            self.match("dos"); self.B(); self.C()
            return
        except Exception:
            self.pos = save
            return  # ε

    def B(self):
        save = self.pos
        try:  # B → C tres
            self.C(); self.match("tres")
            return
        except Exception:
            self.pos = save
            return  # ε

    def C(self):
        if self.la() == "cuatro":
            self.match("cuatro"); self.B()
        else:
            return  # ε

def parse(tokens):
    p = ParserEJ3(tokens)
    p.S()
    if p.la() == "$":
        print(f"Ej3 {tokens} → ACEPTADA ✓")
    else:
        raise Exception(f"Tokens sobrantes: {p.la()}")

if __name__ == "__main__":
    print("\n=== PRUEBAS EJ3 ===\n")
    parse([])                          # válido (ε)
    parse(["dos", "cuatro", "tres"])   # válido (A→dos B C con B→C tres)
    parse(["uno", "uno"])              # válido por S'
    try:
        parse(["cuatro", "tres", "dos"])   # inválido
    except Exception as e:
        print("Cadena ['cuatro','tres','dos'] → RECHAZADA ✗", e)
