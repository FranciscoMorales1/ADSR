class ParserEJ1:
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
        # Intentar S → A B C
        try:
            start = self.pos
            self.A(); self.B(); self.C()
            if self.pos == start:  # no se consumió nada → no vale
                raise Exception("ε total, probar otra rama")
            return
        except Exception:
            self.pos = save
            self.D(); self.E()

    def A(self):
        if self.la() == "dos":
            self.match("dos"); self.B(); self.match("tres")
        else:
            return  # ε

    def B(self):
        if self.la() == "cuatro":
            self.match("cuatro"); self.C(); self.match("cinco"); self.B()
        else:
            return  # ε

    def C(self):
        if self.la() == "seis":
            self.match("seis"); self.A(); self.B()
        else:
            return  # ε

    def D(self):
        save = self.pos
        try:
            self.match("uno"); self.A(); self.E()
            return
        except Exception:
            self.pos = save
            self.B()   # puede ser ε

    def E(self):
        self.match("tres")

def parse(tokens):
    p = ParserEJ1(tokens)
    p.S()
    if p.la() == "$":
        print(f"Ej1 {tokens} → ACEPTADA ✓")
    else:
        raise Exception(f"Tokens sobrantes: {p.la()}")

if __name__ == "__main__":
    print("\n=== PRUEBAS EJ1 ===\n")
    parse(["dos", "tres"])              # válido
    parse(["tres"])                     # válido ahora
    parse(["uno", "tres", "tres"])      # válido
    try:
        parse(["uno", "tres"])          # inválido
    except Exception as e:
        print("Cadena ['uno','tres'] → RECHAZADA ✗", e)
