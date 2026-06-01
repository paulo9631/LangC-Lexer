"""
[Questão 4] - Analisador léxico para a LangC.
Recebe código como entrada, identifica tokens e valida usando autômatos em parser.py
"""

import re
from .parser import check_word

# Placeholder para proteger strings literais durante tokenização
STRING_PLACEHOLDER = "__STRING__{index}__"
STRING_PATTERN = r'"[^"]*"'
STRING_MARKER_PATTERN = r"__STRING__(\d+)__"


class Lexer:
    def __init__(self):
        pass

    def analyze(self, code_line):
        """Analisa uma linha de código e retorna tokens separados por espaço."""
        # Guardar strings e substituir por marcadores temporários
        strings = []
        line_with_markers = self._extract_strings(code_line, strings)

        # Tokenizar a linha sem as strings
        tokens_with_markers = self._tokenize_line(line_with_markers)

        # Processar tokens e recuperar strings originais
        tokens = self._validate_tokens(tokens_with_markers, strings)

        # Retornar resultado final
        if tokens is None:
            return "ERRO"
        return " ".join(tokens)

    def _extract_strings(self, code_line, strings):
        """Remove strings literais e substitui por marcadores temporários."""
        def replace_string(match):
            # Armazenar string original e criar marcador
            string_value = match.group(0)
            strings.append(string_value)
            return STRING_PLACEHOLDER.format(index=len(strings) - 1)

        # Substituir todas as strings pelo padrão
        return re.sub(STRING_PATTERN, replace_string, code_line)

    def _tokenize_line(self, line):
        """Separa linha em tokens usando espaço e ponto-e-vírgula como delimitadores."""
        tokens = []
        current_token = ""

        # Processar cada caractere da linha
        for char in line:
            if char == " ":
                # Espaço: terminar token atual
                if current_token:
                    tokens.append(current_token)
                    current_token = ""
            elif char == ";":
                # Ponto-e-vírgula: terminar token e adicionar como separado
                if current_token:
                    tokens.append(current_token)
                    current_token = ""
                tokens.append(";")
            else:
                # Caractere normal: adicionar ao token atual
                current_token += char

        # Adicionar último token se houver
        if current_token:
            tokens.append(current_token)

        return tokens

    def _validate_tokens(self, tokens_with_markers, strings):
        """Valida cada token usando autômatos do parser."""
        tokens = []

        for token in tokens_with_markers:
            # Verificar se token é um marcador de string
            string_match = re.match(STRING_MARKER_PATTERN, token)

            if string_match:
                # Recuperar string original e validar
                index = int(string_match.group(1))
                original_string = strings[index]
                token_type = check_word(original_string)
            else:
                # Validar token normalmente
                token_type = check_word(token)

            # Se validação falhar, retornar erro
            if token_type == "ERRO":
                return None

            # Adicionar token válido
            tokens.append(token_type)

        return tokens