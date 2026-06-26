class TabSimb:
    MAX_LINHAS = 5

    def __init__(self):
        self._entradas = []
        self._indice = {}

    def buscar(self, lexeme: str):
        return self._indice.get(lexeme)

    def inserir(self, codigo: str, lexeme: str, qtd_antes: int, qtd_depois: int, linha: int):
        existente = self.buscar(lexeme)
        if existente is not None:
            self.atualizar_linha(existente, linha)
            return existente

        entrada = {
            "entrada":            len(self._entradas) + 1,
            "codigo":             codigo,
            "lexeme":             lexeme,
            "qtdCharsAntesTrunc": qtd_antes,
            "qtdCharsDepoisTrunc":qtd_depois,
            "tipoSimb":           "-",
            "linhas":             [linha],
        }
        self._entradas.append(entrada)
        idx = len(self._entradas)
        self._indice[lexeme] = idx
        return idx

    def atualizar_linha(self, indice: int, linha: int):
        entrada = self._entradas[indice - 1]
        if len(entrada["linhas"]) < self.MAX_LINHAS:
            if linha not in entrada["linhas"]:
                entrada["linhas"].append(linha)

    def atualizar_tipo(self, indice: int, tipo: str):
        self._entradas[indice - 1]["tipoSimb"] = tipo

    def gerar_relatorio(self, nome_arquivo: str, dados_equipe: dict):
        linhas = []
        linhas.append(f"Código da Equipe: {dados_equipe['codigo']}")
        linhas.append("Componentes:")
        for comp in dados_equipe["componentes"]:
            linhas.append(f"{comp['nome']}; {comp['email']}; {comp['telefone']}")
        linhas.append("")
        linhas.append("RELATÓRIO DA TABELA DE SÍMBOLOS.")
        linhas.append(f"Texto fonte analisado: {nome_arquivo}")
        linhas.append("")

        for e in self._entradas:
            linhas_str = "(" + ", ".join(str(l) for l in e["linhas"]) + ")"
            linhas.append(f"Entrada: {e['entrada']}, Código: {e['codigo']}, Lexeme: {e['lexeme']},")
            # CORRIGIDO: Adicionado o "s" em QtdCharsDepoisTrunc para parear perfeitamente com a especificação
            linhas.append(f"QtdCharsAntesTrunc: {e['qtdCharsAntesTrunc']}, QtdCharsDepoisTrunc: {e['qtdCharsDepoisTrunc']},")
            linhas.append(f"TipoSimb: {e['tipoSimb']}, Linhas: {linhas_str}.")
            linhas.append("-" * 64)

        return "\n".join(linhas)