# Trabalho 01 Compiladores - Analisador Léxico - LangC

Autores:

- Os amigos que fizemos no caminho (Esquecemos de caçar um terceiro membro)
- Paulo Vitor Pinheiro da Silva - 542156
- Cauã Victor Pinheiro da Silva - 563868

---

## Componentes do Projeto

**Questão 1 - Tokens e Expressões Regulares**
- `regex_patterns.py` - Padrões de regex para reconhecimento
- `token_mapping.py` - Mapeamento e classificação de tokens

**Questão 2 - Autômato Finito Não-Determinístico**
- `nfa.py` - Converte expressões regulares em NFA

**Questão 3 - Autômato Finito Determinístico**
- `dfa.py` - Converte NFA para DFA

**Questão 4 - Análise Léxica**
- `parser.py` - Reconhecimento de tokens usando o DFA
- `lexer.py` - Analisador léxico da LangC
- `main.py` - Programa principal
- `tokens_list.txt` - Caso de teste

---

## Pré-Requisitos

- Python 3.x instalado

---

## Como rodar o programa

1. Crie um arquivo com código da linguagem LangC. Exemplo: `input.txt`

2. No terminal, execute o analisador com:

```bash
python main.py input.txt
```
