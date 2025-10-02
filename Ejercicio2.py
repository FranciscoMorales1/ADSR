# Ejercicio 2 - ASDR con retroceso

class ParserEJ2:
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
        save = self.pos
        try:  # S → B uno
            start = self.pos
            self.B(); self.match("uno")
            if self.pos == start: 
                raise Exception("ε total en rama")
            return
        except Exception:
            self.pos = save
            try:  # S → dos C
                self.match("dos"); self.C()
                return
            except Exception:
                self.pos = save
                return  # ε

    def A(self):
        save = self.pos
        try:  # A → S tres B C
            self.S(); self.match("tres"); self.B(); self.C()
            return
        except Exception:
            self.pos = save
            if self.la() == "cuatro":
                self.match("cuatro")
                return
            return  # ε

    def B(self):
        save = self.pos
        try:  # B → A cinco C seis
            self.A(); self.match("cinco"); self.C(); self.match("seis")
            return
        except Exception:
            self.pos = save
            return  # ε

    def C(self):
        if self.la() == "siete":
            self.match("siete"); self.B()
        else:
            return  # ε

def parse(tokens):
    p = ParserEJ2(tokens)
    p.S()
    if p.la() == "$":
        print(f"Ej2 {tokens} → ACEPTADA ✓")
    else:
        raise Exception(f"Tokens sobrantes: {p.la()}")

if __name__ == "__main__":
    print("\n=== PRUEBAS EJ2 ===\n")
    parse([])                                # válido (ε)
    parse(["dos", "siete", "cuatro", "cinco", "seis"])  # válido
    parse(["cuatro", "cinco", "seis", "uno"])           # válido (por A, luego S)
    try:
        parse(["dos", "cinco"])              # inválido
    except Exception as e:
        print("Cadena ['dos','cinco'] → RECHAZADA ✗", e)
