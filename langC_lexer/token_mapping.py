"""

[Questão 1] - Aqui definimos nosso mapeamento de tokens.
"""

token_map = {
    "SHOW": "show",
    "NUM_TYPE": "num",
    "TEXT_TYPE": "text",
    "TRUE": "true",
    "FALSE": "false",
    "VAR": "nome_variável",
    "NUM": "número",
    "CONST": "cadeia de caracteres",
    "ADD": "+",
    "MINUS": "-",
    "MULTIPLY": "#",
    "DIVIDE": "/",
    "EQUAL": "=",
    "BIGGER": ">",
    "SMALLER": "<",
    "SEMI": ";",
}

single_mapping = {
    "+": "ADD",
    "-": "MINUS",
    "#": "MULTIPLY",
    "/": "DIVIDE",
    "=": "EQUAL",
    ">": "BIGGER",
    "<": "SMALLER",
    ";": "SEMI",
}
