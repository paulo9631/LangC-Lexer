"""
Este script executa o analisador léxico para a linguagem LangC.
O arquivo contendo o código-fonte a ser analisado deve ser passado como argumento via linha de comando.

Uso:
    python main.py input.txt
"""

import sys
from langC_lexer.lexer import Lexer


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("falta o arquivo!")
        sys.exit(1)
    
    arquivo = sys.argv[1]
    lex = Lexer()
    
    try:
        with open(arquivo) as f:
            for linha in f:
                linha = linha.strip()
                if linha:
                    print(lex.analyze(linha))
    except FileNotFoundError:
        print(f"arquivo '{arquivo}' não existe")

