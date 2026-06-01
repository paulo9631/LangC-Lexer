"""
[Questão 3] - Conversão de NFA para DFA usando o algoritmo de subconjuntos.
"""

# Símbolo que representa transição epsilon (vazia)
EPSILON = "$"


def epsilon_closure(nfa, states):
    """Calcula todos os estados alcancaveis via transicoes epsilon."""
    closure_states = set(states)
    stack = list(states)

    while stack:
        current_state = stack.pop()

        # Explorar transicoes epsilon a partir deste estado
        if current_state in nfa["transitions"]:
            for next_state in nfa["transitions"][current_state].get(EPSILON, []):
                if next_state not in closure_states:
                    closure_states.add(next_state)
                    stack.append(next_state)

    return list(closure_states)


def transition_with_symbol(nfa, state, symbol):
    """Encontra estados alcancaveis por uma transicao com o simbolo dado."""
    reachable_states = set()
    stack = [state]

    while stack:
        current_state = stack.pop()

        # Explorar transicoes com o simbolo especificado
        if nfa["transitions"].get(current_state):
            for next_state in nfa["transitions"][current_state].get(symbol, []):
                if next_state not in reachable_states:
                    reachable_states.add(next_state)
                    stack.append(next_state)

    return list(reachable_states)


def dfa_transition(nfa, states, symbol):
    """Calcula para onde vai um conjunto de estados apos o simbolo dado."""
    new_states = set()

    # Para cada estado, encontrar aonde ele vai com este simbolo
    for state in states:
        reachable = transition_with_symbol(nfa, state, symbol)
        
        # Calcular fecho epsilon de cada destino e adicionar
        for next_state in reachable:
            closed = epsilon_closure(nfa, [next_state])
            new_states.update(closed)

    return list(new_states)


def nfa_to_dfa(nfa):
    """Converte NFA em DFA equivalente usando subconjuntos de estados."""
    state_mapping = {}
    state_counter = 0

    def get_state_number(states):
        """Associa um numero unico para cada conjunto de estados NFA."""
        nonlocal state_counter

        # Usar tupla ordenada como chave para ser deterministica
        state_tuple = tuple(sorted(states))

        if state_tuple not in state_mapping:
            state_mapping[state_tuple] = state_counter
            state_counter += 1

        return state_mapping[state_tuple]

    # Estado inicial do DFA é o fecho epsilon do estado inicial do NFA
    initial_closure = epsilon_closure(nfa, [nfa["initial"]])
    initial_state_number = get_state_number(initial_closure)

    # Criar estrutura basica do DFA
    dfa = {
        "states": [initial_state_number],
        "alphabet": nfa["alphabet"],
        "transitions": {},
        "initial": initial_state_number,
        "final": [],
    }

    # Usar busca em profundidade para descobrir todos os estados
    stack = [initial_closure]
    visited_states = set([tuple(sorted(initial_closure))])

    while stack:
        current_states = stack.pop()
        current_state_number = get_state_number(current_states)

        # Calcular transicoes para cada simbolo do alfabeto
        for symbol in dfa["alphabet"]:
            new_states = dfa_transition(nfa, current_states, symbol)
            
            # Pular se nao ha transicao valida
            if not new_states:
                continue

            new_state_number = get_state_number(new_states)

            # Se é um novo estado, adicionar para processar
            if tuple(sorted(new_states)) not in visited_states:
                dfa["states"].append(new_state_number)
                visited_states.add(tuple(sorted(new_states)))
                stack.append(new_states)

            # Marcar como final se contem algum estado final do NFA
            if new_state_number not in dfa["final"] and any(
                state in nfa["final"] for state in new_states
            ):
                dfa["final"].append(new_state_number)

            # Registrar a transicao no DFA
            dfa["transitions"][(current_state_number, symbol)] = new_state_number

    return dfa