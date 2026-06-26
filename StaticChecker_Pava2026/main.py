

import sys
import os
from tabsimb import TabSimb
from lexico import Lexico


DADOS_EQUIPE = {
    "codigo": "[Eq05]",
    "componentes": [
        {"nome": "[João Antonio Luz dos Santos]", "email": "[joaoantionio.santos@ucsal.edu.br]", "telefone": "[(71)99721-1113]"},
        {"nome": "[Guilherme Andrade Silva De Lacerda]", "email": "[guilhermeandrade.lacerda@ucsal.edu.br", "telefone": "[(71)98860-2565]"},
        {"nome": "[Pedro Lucas Azevedo Marinho]", "email": "pedro.marinho@ucsal.edu.br", "telefone": "[(71)98399-9777]"},
        {"nome": "[Diego Gabriel Pinheiro Damasceno]", "email": "[diego.damasceno@ucsal.edu.br]", "telefone": "[(71)98426-6975]"},
    ]
}

def cabecalho(nome_arquivo: str, tipo_relatorio: str) -> str:
    linhas = []
    linhas.append(f"Código da Equipe: {DADOS_EQUIPE['codigo']}")
    linhas.append("Componentes:")
    for comp in DADOS_EQUIPE["componentes"]:
        linhas.append(f"{comp['nome']}; {comp['email']}; {comp['telefone']}")
    linhas.append("")
    linhas.append(f"{tipo_relatorio}")
    linhas.append(f"Texto fonte analisado: {nome_arquivo}")
    linhas.append("")
    return "\n".join(linhas)


def abrir_arquivo(caminho: str) -> str:
    if not os.path.exists(caminho):
        print(f"Erro: arquivo '{caminho}' não encontrado.")
        sys.exit(1)
    with open(caminho, "r", encoding="utf-8") as f:
        return f.read()


def gerar_lex(tokens, nome_arquivo: str) -> str:
    linhas = [cabecalho(nome_arquivo, "RELATÓRIO DA ANÁLISE LÉXICA.")]
    for tok in tokens:
        idx = tok.indice if tok.indice is not None else "-"
        linhas.append(
            f"Lexeme: {tok.lexeme}, Código: {tok.codigo}, "
            f"indiceTabSimb: {idx}, Linha: {tok.linha}."
        )
    return "\n".join(linhas)


def main():
    if len(sys.argv) < 2:
        print("Uso: python main.py <nome_do_arquivo_sem_extensao>")
        sys.exit(1)

    arg = sys.argv[1]
    if arg.endswith(".261"):
        caminho_fonte = arg
    else:
        caminho_fonte = arg + ".261"

    pasta_saida   = os.path.dirname(os.path.abspath(caminho_fonte))
    nome_base     = os.path.splitext(os.path.basename(caminho_fonte))[0]
    nome_arquivo  = os.path.basename(caminho_fonte)

    texto_fonte = abrir_arquivo(caminho_fonte)

    tabsimb = TabSimb()

    lexico = Lexico(texto_fonte, tabsimb)

    tokens = []
    while True:
        tok = lexico.proximo_atomo()
        if tok.codigo == "EOF":
            break
        tokens.append(tok)

    caminho_lex = os.path.join(pasta_saida, nome_base + ".LEX")
    with open(caminho_lex, "w", encoding="utf-8") as f:
        f.write(gerar_lex(tokens, nome_arquivo))
    print(f"Relatório léxico gerado: {caminho_lex}")

    caminho_tab = os.path.join(pasta_saida, nome_base + ".TAB")
    with open(caminho_tab, "w", encoding="utf-8") as f:
        f.write(tabsimb.gerar_relatorio(nome_arquivo, DADOS_EQUIPE))
    print(f"Tabela de símbolos gerada: {caminho_tab}")


if __name__ == "__main__":
    main()
