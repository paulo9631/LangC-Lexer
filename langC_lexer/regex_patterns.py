"""
[Questão 1] - Aqui definimos nossas expressões regulares para os tokens da linguagem LangC. 
"""

# Convenções utilizadas para facilitar a construção das expressões regulares:
a_to_z = "a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z"
A_to_Z = "A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z"
zero_to_nine = "0|1|2|3|4|5|6|7|8|9"
letter = "(" + a_to_z + "|" + A_to_Z + ")"
digit = "(" + zero_to_nine + ")"
all_chars = letter + "|" + digit + "|_|!|@|#|$|%|&|?| "

# Palavras reservadas e tipos de dados (Todos literais)
SHOW = "(s.h.o.w)"
NUM_TYPE = "(n.u.m)"
TEXT_TYPE = "(t.e.x.t)"
TRUE = "(t.r.u.e)"
FALSE = "(f.a.l.s.e)"

# Estrutura dos tipos
VAR = "(" + letter +  "|_" +  ".(" + letter + "|" + digit + "|_)*)"
NUM = "(" + digit + ".(" + digit + ")*)"
CONST = '(".((' + all_chars + ')*.)".)'


# Operadores e símbolos (Todos literais)
ADD = "+"
MINUS = "-"
MULTIPLY = "#" # Trocar esse simbolo 
DIVIDE = "/"
EQUAL = "="
BIGGER = ">"
SMALLER = "<"
SEMI = ";"

SINGLE = (
    "("
    + ADD
    + "|"
    + MINUS
    + "|"
    + MULTIPLY
    + "|"
    + DIVIDE
    + "|"
    + EQUAL
    + "|"
    + BIGGER
    + "|"
    + SMALLER
    + "|"
    + SEMI
    + ")"
)
