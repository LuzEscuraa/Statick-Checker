# Static-Checker
Este projeto visa a construção de um static checker como etapa final do Projeto da materia de compiladores, desenvolvida em python a api recebe um arquivo .261 em linguagem PAVA2026-1 executa a análise léxica e parte da análise sintática, conforme definido na especificação do projeto.


O Static Checker recebe como entrada um arquivo com extensão .261 contendo código-fonte em
Pava2026-1 e produz dois arquivos de saída na mesma pasta do fonte:
• Arquivo .LEX – Relatório da análise léxica: todos os átomos encontrados, na ordem de ocorrência.
• Arquivo .TAB – Relatório da tabela de símbolos: todos os identificadores armazenados e seus atributos.
O programa principal (main.py) coordena a leitura do arquivo fonte, realiza chamadas sucessivas ao
analisador léxico até o fim do texto, e ao final invoca a geração dos dois relatórios.

Para utilizar o Statick checker siga os passos a seguir:

Instale o Python
Pré-requisito
O programa só funciona se o Python estiver instalado.
● Abra o terminal e digite python --version
● Precisa ser Python 3.8 ou superior
● Se não tiver, baixe em python.org
● Durante a instalação, marque a opção Add Python to PATH

Baixe os arquivos do projeto
Você precisa ter os arquivos principais na mesma pasta.
● Baixe o pacote do projeto
● Extraia em uma pasta
● Confirme que os arquivos estão lá: main.py, lexico.py, tabsimb.py,
reservadas.py, token.py

Crie um arquivo de teste
Esse arquivo será analisado pelo programa.
● Crie um arquivo de texto com extensão .261
● Exemplo: MeuTeste.261(Ja existente no projeto)
● Escreva algum código na sintaxe da linguagem Pava2026-1


Execute o programa
Agora você vai rodar o analisador léxico.
● Abra o terminal na pasta do projeto ou numa IDE de sua preferência
● Digite: python main.py MeuTeste
● (não coloque .261 no comando)
● O programa vai ler o arquivo e analisar

Confira os resultados
O programa gera relatórios automáticos.
● Na mesma pasta, vão aparecer dois arquivos um .TAB e um .LEX:
○ MeuTeste.LEX: relatório detalhado dos tokens
○ MeuTeste.TAB: tabela de símbolos
● Abra esses arquivos para ver os resultados

