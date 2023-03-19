# -*-coding:utf-8 -*-
'''
@File    :   Subset.py
@Date    :   2023/02/26
@Author  :   Pedro Arriola (20188)
@Version :   1.0
@Desc    :   Clase Subset que implementa la construccion de AFN a un AFD por medio de subconjuntos
'''

from DFA import DFA
from graphviz import Digraph

class SubsetDFA(object):
    
    def __init__(self, postfix, nfa_to_subset):
        
        self.postfix = postfix
        self.nfa = nfa_to_subset 
        self.subset_dfa = self.subset_construction(self.nfa)
        self.visualize_subset_dfa("Subset DFA", self.subset_dfa)
        
        # DFA minimizado
        self.minimized_dfa = self.subset_dfa.minimization()
        self.visualize_subset_dfa("Minimized Subset DFA", self.minimized_dfa)
        
    # Definición de la función ε-closure.
    def ε_closure(self, states, mapping):

        # Instancia inicial del resultado.
        result = set()

        # En primer lugar, todos los estados del conjunto se agregan al resultado.
        result = result | states
        
        last_result = set()

        # Mientras el resultado no sea igual al último resultado, se itera sobre el último resultado.
        while (result != last_result):

            # Se actualiza el último resultado.
            last_result = result.copy()

            # Para cada estado del último resultado, se unen los estados a los que se llega con el símbolo ε.
            for state in last_result:
                if ("ε" in mapping[state]):
                    result = result | mapping[state]["ε"]
                    
                    

        # Retorno del resultado.
        return result

    # Definición de movimiento de estados con un símbolo.
    def move(self, states, symbol, mapping):

        # Instancia inicial del resultado.
        result = set()

        # Para cada estado del conjunto, se unen los estados a los que se llega con el símbolo.
        for state in states:
            if (symbol in mapping[state]):
                result = result | mapping[state][symbol]

        # Retorno del resultado obtenido.
        return result

    # Definición de la función de construcción de subconjuntos.
    def subset_construction(self, nfa):

        # El alfabeto del DFA es el mismo que el del NFA.
        # Se instancia un mapping para las transiciones del DFA.
        alphabet = nfa.alphabet
        mapping = {}

        # Se crea un diccionario para almacenar los estados del DFA y su respectivo conjunto de estados del NFA.
        states = {}

        # El estado actual es 0. Se guarda en la lista de estados a procesar.
        current_state = 0
        queue = []
        
        initial_state = self.ε_closure({ nfa.initial_state }, 
                                nfa.mapping)
        
        states[current_state] = initial_state
        queue.append(current_state)
        current_state += 1

        # Se itera el algoritmo de construcción de subconjuntos mientras haya estados qué analizar en el stack.
        while (len(queue) > 0):

            # Se toma el primer estado de la lista de estados a procesar.
            state = queue.pop(0)

            # Para cada símbolo del alfabeto:
            for symbol in alphabet:

                # Se crea un nuevo estado a partir de la función move del estado actual con el símbolo iterado.
                new_state = self.ε_closure(self.move(states[state], 
                                        symbol, 
                                        nfa.mapping), 
                                        nfa.mapping)

                # Si el nuevo estado no es vacío y no está en los estados ya creados, se crea un nuevo estado.
                if ((new_state != set()) 
                    and (new_state not in states.values())):
                    
                    states[current_state] = new_state
                    queue.append(current_state)
                    current_state += 1

                # Se guarda el índice del nuevo estado creado.
                for key in states:
                    if (states[key] == new_state):
                        new_state = key

                # Se crea la transición del estado actual con el símbolo iterado hacia el nuevo estado.
                if (state not in mapping):
                    mapping[state] = {}
                
                mapping[state][symbol] = new_state

        # Se crea el conjunto de estados de aceptación del DFA.
        acceptance_states = set()

        # Se itera sobre los estados creados para agregar los estados de aceptación del NFA al conjunto de estados de aceptación del DFA.
        for state in states:
            if (nfa.acceptance_state in states[state]):
                acceptance_states.add(state)

        # Se crea un mapping temporal del DFA.
        t_mapping = {}

        # Se itera sobre las transiciones del mapping original para agregar las transiciones que no van a estados de atrapamiento al mapping temporal.
        for transition in mapping:
            t_mapping[transition] = {}
            
            for entry in mapping[transition]:
                if (mapping[transition][entry] != set()):
                    t_mapping[transition][entry] = mapping[transition][entry]

        # Se actualiza el mapping del DFA.
        mapping = t_mapping

        # Se retorna el DFA.
        return DFA(
            states=set(states.keys()),
            alphabet=alphabet,
            initial_state=0,
            acceptance_states=acceptance_states,
            mapping=mapping
        )
    def visualize_subset_dfa(self, name, dfa):

        description = ("Subset DFA of " + self.postfix)
        dot_graph = Digraph(comment=description)
        dot_graph.attr(
            rankdir="LR",
            labelloc="t",
            label=description
        )

        # Iteración para dibujar los estados.
        for state in dfa.states:

            # Dibujo de los estados del autómata.
            if (state == dfa.initial_state):
                dot_graph.node(str(state), str(state), shape="circle", style="filled")
            elif (state in dfa.acceptance_states):
                dot_graph.node(str(state), str(state), shape="doublecircle", style="filled")
            else:
                dot_graph.node(str(state), str(state), shape="circle")

            # Dibujo de las transiciones del autómata.
            for transition in dfa.mapping[state]:
                next_state = dfa.mapping[state][transition]
                dot_graph.edge(str(state), str(next_state), label=transition)

        # Visualización del DFA.
        dot_graph.render(name, format="png", view=True)