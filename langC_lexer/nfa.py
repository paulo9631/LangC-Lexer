"""
[Questão 2] - Aqui convertemos expressões regulares em NFAs usando o algoritmo de Thompson.
Contém também funções auxiliares para empilhamento, concatenação, união e fecho de Kleene.
"""

states_counter = 0


def _add_epsilon_edge(transitions, from_state, to_states):
    """Cria transições Epsilon de from_state para cada estado em to_states."""
    # Garantir que to_states é uma lista
    if not isinstance(to_states, list):
        to_states = [to_states]
    
    # Adicionar transição epsilon ao dicionário de transições
    if from_state in transitions:
        if "$" in transitions[from_state]:
            transitions[from_state]["$"].extend(to_states)
        else:
            transitions[from_state]["$"] = to_states
    else:
        transitions[from_state] = {"$": to_states}


def _pop_two_nfas(stack):
    """Desempilha dois NFAs do stack. Retorna erro se houver menos de 2 ou se não forem dicionários."""
    # Verificar se há pelo menos 2 elementos
    if len(stack) < 2:
        return None, None, True

    # Desempilhar e validar tipos
    nfa_2 = stack.pop()
    nfa_1 = stack.pop()

    if not isinstance(nfa_1, dict) or not isinstance(nfa_2, dict):
        # Se não forem NFAs, colocar de volta e retornar erro
        stack.append(nfa_1)
        stack.append(nfa_2)
        return None, None, True

    return nfa_1, nfa_2, False


def merge_nfas(stack, symbol):
    """Combina dois NFAs com concatenacao, uniao ou fecho de Kleene."""
    global states_counter

    if symbol == ".":
        # Concatenacao: estado final do primeiro leva ao inicial do segundo
        nfa_1, nfa_2, err = _pop_two_nfas(stack)
        if err:
            return None, stack

        new_nfa = {
            "states": nfa_1["states"] + nfa_2["states"],
            "alphabet": list(set(nfa_1["alphabet"] + nfa_2["alphabet"])),
            "transitions": {**nfa_1["transitions"], **nfa_2["transitions"]},
            "initial": nfa_1["initial"],
            "final": nfa_2["final"],
        }

        # Conectar estados finais do primeiro aos iniciais do segundo
        for state in nfa_1["final"]:
            _add_epsilon_edge(new_nfa["transitions"], state, nfa_2["initial"])

        stack.append(new_nfa)
        return new_nfa, stack

    if symbol == "|":
        # Uniao: novo inicial conecta aos dois iniciais, dois finais conectam ao novo final
        nfa_1, nfa_2, err = _pop_two_nfas(stack)
        if err:
            return None, stack

        # Criar novo estado inicial e final
        states_counter += 2

        new_nfa = {
            "states": nfa_1["states"] + nfa_2["states"] + [states_counter - 2, states_counter - 1],
            "alphabet": list(set(nfa_1["alphabet"] + nfa_2["alphabet"])),
            "transitions": {**nfa_1["transitions"], **nfa_2["transitions"]},
            "initial": states_counter - 2,
            "final": [states_counter - 1],
        }

        new_initial = new_nfa["initial"]
        new_final = new_nfa["final"][0]

        # Conectar novo inicial aos dois iniciais
        _add_epsilon_edge(new_nfa["transitions"], new_initial, [nfa_1["initial"], nfa_2["initial"]])
        # Conectar todos os finais ao novo final
        for state in nfa_1["final"] + nfa_2["final"]:
            _add_epsilon_edge(new_nfa["transitions"], state, new_final)

        stack.append(new_nfa)
        return new_nfa, stack

    if symbol == "*":
        # Fecho Kleene: novo inicial vai ao novo final ou ao inicial do fragmento
        if not stack:
            return None, stack

        nfa_fragment = stack.pop()

        # Validar que é um NFA
        if not isinstance(nfa_fragment, dict):
            stack.append(nfa_fragment)
            return None, stack

        # Criar novo estado inicial e final
        states_counter += 2

        new_nfa = {
            "states": nfa_fragment["states"] + [states_counter - 2, states_counter - 1],
            "alphabet": nfa_fragment["alphabet"],
            "transitions": {**nfa_fragment["transitions"]},
            "initial": states_counter - 2,
            "final": [states_counter - 1],
        }

        new_initial = new_nfa["initial"]
        new_final = new_nfa["final"][0]

        # Novo inicial pode pular para novo final ou para o fragmento
        _add_epsilon_edge(new_nfa["transitions"], new_initial, [new_final, nfa_fragment["initial"]])
        # Finais do fragmento conectam ao novo final ou reciclam para inicio
        for final_state in nfa_fragment["final"]:
            _add_epsilon_edge(new_nfa["transitions"], final_state, [new_final, nfa_fragment["initial"]])

        stack.append(new_nfa)
        return new_nfa, stack

    return None, stack


def make_stack(expression):
    """Converte expressao em lista alternando NFAs e operadores."""
    RE_list = []
    global states_counter

    for symbol in expression:
        # Se nao é operador, criar um NFA basico com um simbolo
        if symbol not in ["(", ")", "|", "*", "."]:
            states_counter += 2
            new_nfa = {
                "states": [states_counter - 2, states_counter - 1],
                "alphabet": [symbol],
                "transitions": {states_counter - 2: {symbol: [states_counter - 1]}},
                "initial": states_counter - 2,
                "final": [states_counter - 1],
            }

            RE_list.append(new_nfa)
        else:
            # Se é operador, adicionar direto
            RE_list.append(symbol)

    return RE_list


def er_to_nfa(expression):
    """Converte expressao regular em NFA usando algoritmo shunting-yard."""
    output_stack = []
    operator_stack = []

    # Converter expressao em lista de NFAs e operadores
    RE_list = make_stack(expression)

    def apply_operator(operator):
        # Aplicar operador ao topo da pilha de saida
        nonlocal output_stack
        _, output_stack = merge_nfas(output_stack, operator)

    for symbol in RE_list:
        # Se é NFA, adicionar a pilha de saida
        if isinstance(symbol, dict):
            output_stack.append(symbol)
            continue

        # Parenteses aberto vai para pilha de operadores
        if symbol == "(":
            operator_stack.append(symbol)
            continue

        # Parenteses fechado: aplicar operadores ate encontrar abertura
        if symbol == ")":
            while operator_stack and operator_stack[-1] != "(":
                apply_operator(operator_stack.pop())

            if operator_stack and operator_stack[-1] == "(":
                operator_stack.pop()
            continue

        # Operadores: aplicar os de maior precedencia primeiro
        if symbol in [".", "|", "*"]:
            while (
                operator_stack
                and operator_stack[-1] != "("
                and (
                    operator_stack[-1] == "*"
                    or (operator_stack[-1] in [".", "|"] and symbol != "*")
                )
            ):
                apply_operator(operator_stack.pop())

            operator_stack.append(symbol)

    # Aplicar operadores restantes
    while operator_stack:
        op = operator_stack.pop()
        if op == "(":
            continue
        apply_operator(op)

    # Retornar NFA final ou criar NFA vazio
    if output_stack:
        return output_stack[0]

    # Se nenhuma expressao foi processada, retornar NFA vazio
    states_counter += 2
    return {
        "states": [states_counter - 2, states_counter - 1],
        "alphabet": [],
        "transitions": {states_counter - 2: {"$": [states_counter - 1]}},
        "initial": states_counter - 2,
        "final": [states_counter - 1],
    }