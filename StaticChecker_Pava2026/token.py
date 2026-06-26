class Token:
    def __init__(self, codigo: str, lexeme: str, linha: int, indice=None):
        self.codigo = codigo
        self.lexeme = lexeme
        self.linha  = linha
        self.indice = indice

    def __repr__(self):
        idx = self.indice if self.indice is not None else "-"
        return (f"Lexeme: {self.lexeme}, Código: {self.codigo}, "
                f"indiceTabSimb: {idx}, Linha: {self.linha}")
