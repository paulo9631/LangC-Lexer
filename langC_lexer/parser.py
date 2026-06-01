"""
[Questão 4] - Aqui é onde a mágica acontece, convertemos os regex_patterns em NFAs
Depois transformamos os NFAs em DFAs, e finalmente usamos os DFAs para validar os tokens
"""

from . import regex_patterns, nfa, dfa, token_mapping

# Mapeamento de tipos especiais que precisam transformação de nome
type_name_mapping = {
    "NUM_TYPE": "NUM",
    "TEXT_TYPE": "TEXT",
}

# Mapeamento de símbolos especiais para nomes de tokens
single_mapping = token_mapping.single_mapping


def _build_token_dfas():
    """Constrói todos os DFAs a partir dos padrões usando Thompson NFA."""
    # Lista de padrões disponíveis em regex_patterns
    token_patterns = [
        "SHOW", "NUM_TYPE", "TEXT_TYPE", "TRUE", "FALSE",
        "VAR", "NUM", "CONST", "SINGLE"
    ]
    
    # Construir DFA para cada padrão: Thompson NFA -> Conversão de subconjuntos
    dfas_dict = {}
    for pattern_name in token_patterns:
        pattern = getattr(regex_patterns, pattern_name)
        dfas_dict[pattern_name] = dfa.nfa_to_dfa(nfa.er_to_nfa(pattern))
    
    return dfas_dict


# Dicionário com todos os DFAs para fácil acesso
dfas = _build_token_dfas()


def process_string_dfa(dfa_, string):
    """Simula DFA sobre uma string, retornando estado final e palavra processada."""
    # Começar no estado inicial do DFA
    current_state = dfa_["initial"]
    word = ""

    # Processar cada caractere da string
    for char in string:
        # Se há transição válida, prosseguir
        if (current_state, char) in dfa_["transitions"]:
            word += char
            current_state = dfa_["transitions"][(current_state, char)]
        else:
            # Se não há transição, rejeitar
            return "ERRO"

    # Retornar estado final e palavra processada
    return current_state, word


def check_word(word):
    """Identifica qual token a string pertence testando contra todos os DFAs."""
    # Tentar cada padrão de token em ordem
    for token_name, dfa_pattern in dfas.items():
        result = process_string_dfa(dfa_pattern, word)
        
        # Se DFA aceitou a string
        if result != "ERRO":
            final_state, processed_word = result
            
            # Verificar se terminou em estado final
            if final_state in dfa_pattern["final"]:
                # Lidar com token especial SINGLE (símbolos)
                if token_name == "SINGLE":
                    return single_mapping.get(processed_word, "ERRO")
                
                # Aplicar transformação de tipo se existir
                if token_name in type_name_mapping:
                    return type_name_mapping[token_name]
                
                # Retornar nome do token
                return token_name
    
    # Se nenhum padrão coincidiu, rejeitar
    return "ERRO"
