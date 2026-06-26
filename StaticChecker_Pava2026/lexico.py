from token import Token
from reservadas import get_codigo_palavra, get_codigo_simbolo
from tabsimb import TabSimb

LIMITE_ATOMO = 30

LETRAS     = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
DIGITOS    = set("0123456789")
SIMBOLOS_V = set(";,:=?()[]{}+-*/%#<>!\"'._")

def _eh_valido(c: str) -> bool:
    return (c in LETRAS or c in DIGITOS or c in SIMBOLOS_V or c == '_' or c in ' \t\n\r')

class Lexico:
    def __init__(self, texto: str, tabsimb: TabSimb):
        self._texto  = texto + '\0'
        self._pos    = 0
        self._linha  = 1
        self._tabsimb = tabsimb

    def proximo_atomo(self):
        self._pular_espacos_e_comentarios()
        c = self._atual()
        if c == '\0':
            return Token("EOF", "", self._linha)

        if c in LETRAS:
            return self._formar_identificador_ou_reservada()
        elif c in DIGITOS:
            return self._formar_numero()
        elif c == '"':
            return self._formar_string_const()
        elif c == "'":
            return self._formar_char_const()
        else:
            return self._formar_simbolo()

    def _atual(self) -> str:
        return self._texto[self._pos]

    def _peek(self) -> str:
        p = self._pos + 1
        return self._texto[p] if p < len(self._texto) else '\0'

    def _avancar(self):
        if self._texto[self._pos] == '\n':
            self._linha += 1
        self._pos += 1

    def _pular_espacos_e_comentarios(self):
        while True:
            c = self._atual()
            if c == '\0':
                break
            if c in ' \t\n\r':
                self._avancar()
                continue
            if c == '/' and self._peek() == '/':
                while self._atual() not in ('\n', '\0'):
                    self._avancar()
                continue
            if c == '/' and self._peek() == '*':
                self._avancar()
                self._avancar()
                while self._atual() != '\0':
                    if self._atual() == '*' and self._peek() == '/':
                        self._avancar()
                        self._avancar()
                        break
                    self._avancar()
                continue
            if not _eh_valido(c):
                self._avancar()
                continue
            break

    def _formar_identificador_ou_reservada(self):
        linha_inicio = self._linha
        lexeme_completo = []
        lexeme_truncado = []
        count = 0

        while True:
            c = self._atual()
            if c in LETRAS or c in DIGITOS or c == '_':
                lexeme_completo.append(c)
                if count < LIMITE_ATOMO:
                    lexeme_truncado.append(c)
                count += 1
                self._avancar()
            elif not _eh_valido(c) and c != '\0':
                lexeme_completo.append(c)
                self._avancar()
            else:
                break

        qtd_antes  = len(lexeme_completo)
        qtd_depois = len(lexeme_truncado)
        lexeme = "".join(lexeme_truncado).upper()

        codigo_res = get_codigo_palavra(lexeme)
        if codigo_res:
            return Token(codigo_res, lexeme, linha_inicio, None)

        codigo = "C01"
        indice = self._tabsimb.inserir(codigo, lexeme, qtd_antes, qtd_depois, linha_inicio)
        return Token(codigo, lexeme, linha_inicio, indice)

    def _formar_numero(self):
        linha_inicio = self._linha
        lexeme = []
        count = 0
        qtd_antes_chars = []

        while self._atual() in DIGITOS:
            qtd_antes_chars.append(self._atual())
            if count < LIMITE_ATOMO:
                lexeme.append(self._atual())
            count += 1
            self._avancar()

        if self._atual() == '.' and self._peek() in DIGITOS:
            qtd_antes_chars.append('.')
            if count < LIMITE_ATOMO:
                lexeme.append('.')
            count += 1
            self._avancar()

            while self._atual() in DIGITOS:
                qtd_antes_chars.append(self._atual())
                if count < LIMITE_ATOMO:
                    lexeme.append(self._atual())
                count += 1
                self._avancar()

            if self._atual().lower() == 'e':
                qtd_antes_chars.append(self._atual())
                if count < LIMITE_ATOMO:
                    lexeme.append('E')
                count += 1
                self._avancar()

                if self._atual() in ('+', '-'):
                    qtd_antes_chars.append(self._atual())
                    if count < LIMITE_ATOMO:
                        lexeme.append(self._atual())
                    count += 1
                    self._avancar()

                while self._atual() in DIGITOS:
                    qtd_antes_chars.append(self._atual())
                    if count < LIMITE_ATOMO:
                        lexeme.append(self._atual())
                    count += 1
                    self._avancar()

            codigo  = "C07"
        else:
            codigo = "C06"

        qtd_antes  = len(qtd_antes_chars)
        qtd_depois = len(lexeme)
        lex_str    = "".join(lexeme)

        indice = self._tabsimb.inserir(codigo, lex_str, qtd_antes, qtd_depois, linha_inicio)
        return Token(codigo, lex_str, linha_inicio, indice)

    def _formar_string_const(self):
        linha_inicio = self._linha
        lexeme = []
        count  = 0
        qtd_antes = 0

        lexeme.append('"')
        count += 1
        qtd_antes += 1
        self._avancar()

        chars_validos_miolo = LETRAS | DIGITOS | {' ', '$', '_', '.'}

        while self._atual() != '\0':
            c = self._atual()
            if c == '"':
                qtd_antes += 1
                if count < LIMITE_ATOMO:
                    lexeme.append('"')
                count += 1
                self._avancar()
                break
            elif c in chars_validos_miolo:
                qtd_antes += 1
                if count < LIMITE_ATOMO:
                    lexeme.append(c)
                count += 1
                self._avancar()
            elif c == '\n':
                break
            else:
                self._avancar()

        qtd_depois = len(lexeme)
        lex_str    = "".join(lexeme)
        indice = self._tabsimb.inserir("C04", lex_str, qtd_antes, qtd_depois, self._linha) # CORRIGIDO: self minúsculo
        return Token("C04", lex_str, linha_inicio, indice)

    def _formar_char_const(self):
        linha_inicio = self._linha
        lexeme = ["'"]
        qtd_antes = 1
        self._avancar()

        if self._atual() in LETRAS:
            lexeme.append(self._atual())
            qtd_antes += 1
            self._avancar()

        if self._atual() == "'":
            lexeme.append("'")
            qtd_antes += 1
            self._avancar()

        lex_str    = "".join(lexeme).upper()
        qtd_depois = len(lex_str)
        indice = self._tabsimb.inserir("C05", lex_str, qtd_antes, qtd_depois, linha_inicio)
        return Token("C05", lex_str, linha_inicio, indice)

    def _formar_simbolo(self):
        linha_inicio = self._linha
        simbolo, codigo = get_codigo_simbolo(self._texto, self._pos)
        if simbolo:
            for _ in simbolo:
                self._avancar()
            return Token(codigo, simbolo, linha_inicio, None)

        self._avancar()
        return self.proximo_atomo()