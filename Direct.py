# -*-coding:utf-8 -*-
'''
@File    :   Direct.py
@Date    :   2023/03/18
@Author  :   Pedro Arriola (20188)
@Version :   1.0
@Desc    :   Clase que permite realizar la construccion directa de un AFD.
'''

from DFA import DFA
from Node import Node
from graphviz import Digraph

class DirectDFA(object):
    
    def __init__(self, postfix):
        self.postfix = postfix
        self.direct_dfa = self.direct_construction()
        self.visualize_direct_dfa("Direct DFA", self.direct_dfa)
    
    def syntactic_tree(self):

        # Variables necesarias para la construcción del árbol.
        stack = []
        node_array = []
        position = 1

        # Iteración en la expresión postfix aumentada.
        for char in self.postfix:

            # Construcción de un nodo con operador kleene.
            if (char == "*"):

                # Obtención del nodo hijo del operador kleene.
                operand = stack.pop()
                node = Node(char)
                node.left = operand
                stack.append(node)
                node_array.append(node)

            # Construcción de un nodo con operador positivo.
            elif (char == "+"):

                # Obtención del nodo hijo del operador positivo.
                operand = stack.pop()
                node = Node(char)
                node.left = operand
                stack.append(node)
                node_array.append(node)

            # Construcción de un nodo con operador nullable.
            elif (char == "?"):

                # Obtención del nodo hijo del operador nullable.
                operand = stack.pop()
                node = Node(char)
                node.left = operand
                stack.append(node)
                node_array.append(node)

            # Construcción de un nodo con operador concatenación.
            elif (char == "."):

                # Obtención de los nodos hijos del operador concatenación.
                right_operand = stack.pop()
                left_operand = stack.pop()
                node = Node(char)
                node.left = left_operand
                node.right = right_operand
                stack.append(node)
                node_array.append(node)

            # Construcción de un nodo con operador or.
            elif (char == "|"):

                # Obtención de los nodos hijos del operador or.
                right_operand = stack.pop()
                left_operand = stack.pop()
                node = Node(char)
                node.left = left_operand
                node.right = right_operand
                stack.append(node)
                node_array.append(node)

            # Construcción de una hoja del árbol (símbolo del alfabeto, epsilon o #).
            else:

                # Creación de la hoja.
                node = Node(char, position)
                stack.append(node)
                node_array.append(node)
                position += 1

        # Retorno del nodo raíz del árbol y del arreglo de nodos.
        return stack.pop(), node_array

    # Método para calcular si un nodo es nullable o no.
    def nullable(self, node):
        
        # Cálculo del caso base de nullable, es decir, una hoja.
        if ((node.left == None) and (node.right == None)):

            # Retorno del valor de nullable según la hoja es epsilon o no.
            return (node.value == "ε")

        # Cálculo del caso inductivo del nullable, es decir, un operador.
        else:

            # Retorno del valor de nullable.
            if (node.value == "*"):
                return True
            elif (node.value == "+"):
                return self.nullable(node.left)
            elif (node.value == "?"):
                return True
            elif (node.value == "."):
                return (self.nullable(node.left) and self.nullable(node.right))
            elif (node.value == "|"):
                return (self.nullable(node.left) or self.nullable(node.right))

    # Método para calcular el conjunto de firstpos de un nodo.
    def firstpos(self, node):

        # Cálculo del caso base de firstpos, es decir, una hoja.
        if ((node.left == None) and (node.right == None)):

            # Retorno del valor de firstpos según la hoja es epsilon o no.
            if (node.value == "ε"):
                return set()
            else:
                return { node }

        # Cálculo del caso inductivo de firstpos, es decir, un operador.
        else:

            # Retorno del valor de firstpos.
            if (node.value == "*"):
                return self.firstpos(node.left)
            elif (node.value == "+"):
                return self.firstpos(node.left)
            elif (node.value == "?"):
                return self.firstpos(node.left)
            elif (node.value == "."):
                if (self.nullable(node.left)):
                    return self.firstpos(node.left) | self.firstpos(node.right)
                else:
                    return self.firstpos(node.left)
            elif (node.value == "|"):
                return self.firstpos(node.left) | self.firstpos(node.right)

    # Método para calcular el conjunto de lastpos de un nodo.
    def lastpos(self, node):

        # Cálculo del caso base de lastpos, es decir, una hoja.
        if ((node.left == None) and (node.right == None)):

            # Retorno del valor de lastpos según la hoja es epsilon o no.
            if (node.value == "ε"):
                return set()
            else:
                return { node }

        # Cálculo del caso inductivo de lastpos, es decir, un operador.
        else:

            # Retorno del valor de lastpos.
            if (node.value == "*"):
                return self.lastpos(node.left)
            elif (node.value == "+"):
                return self.lastpos(node.left)
            elif (node.value == "?"):
                return self.lastpos(node.left)
            elif (node.value == "."):
                if (self.nullable(node.right)):
                    return self.lastpos(node.left) | self.lastpos(node.right)
                else:
                    return self.lastpos(node.right)
            elif (node.value == "|"):
                return self.lastpos(node.left) | self.lastpos(node.right)

    # Método para calcular el conjunto de followpos de un nodo.
    def followpos(self, node):

        # Cálculo del caso base de followpos, es decir, una hoja.
        if ((node.left == None) and (node.right == None)):

            # Retorno del valor de followpos según la hoja es epsilon o no.
            return set()

        # Cálculo del caso inductivo de followpos, es decir, un operador.
        else:

            # Retorno del valor de followpos.
            if ((node.value == "*") or (node.value == "+")):
                first_step = self.lastpos(node)
                for state in first_step:
                    state.properties["followpos"] |= self.firstpos(node)
            elif (node.value == "."):
                first_step = self.lastpos(node.left)
                for state in first_step:
                    state.properties["followpos"] |= self.firstpos(node.right)
            else:
                return set()

    # Método para la construcción directa de expresión postfix a DFA.
    def direct_construction(self):
        
        OPERATORS = ("+", "?", "*", ".", "|")

        # Extensión de la expresión regular con el símbolo #.
        self.postfix += "#."
        
        # Obtención del árbol de expresión y del arreglo de nodos.
        expression_tree_root, node_array = self.syntactic_tree()

        # Cálculo de los conjuntos nullable, firstpos, lastpos y followpos para cada nodo.
        for node in node_array:
            node.properties["nullable"] = self.nullable(node)
            node.properties["firstpos"] = self.firstpos(node)
            node.properties["lastpos"] = self.lastpos(node)
            node.properties["followpos"] = self.followpos(node)

        # Variables importantes para el DFA.
        states = set()
        alphabet = set([char for char in self.postfix if char not in set(OPERATORS) | {"ε", "#"}])
        indexed_states = []
        mapping = {}
        state_stack = []

        # Obtención del estado inicial (firspos de la raíz) y agregación del mismo al stack.
        initial_state = self.firstpos(expression_tree_root)
        state_stack.append(initial_state)
        indexed_states.append(initial_state)

        # Iteración en el stack de estados a meter al mapping.
        while (not len(state_stack) == 0):

            # Obtención del estado actual, su índice y creación en el mapping.
            current_state = state_stack.pop()
            current_state_index = indexed_states.index(current_state)
            mapping[current_state_index] = {}

            # Iteración en el alfabeto para obtener los estados siguientes.
            for char in alphabet:

                # Instancia inicial del próximo estado alcanzado con el caracter actual.
                next_state = set()

                # Iteración en el estado actual para obtener los estados siguientes.
                for node in current_state:

                    # Si el valor del nodo es el caracter, debemos agregar los followpos del nodo al conjunto de estados siguientes.
                    if (node.value == char):

                        # Unión del followpos del nodo al estado siguiente.
                        next_state |= node.properties["followpos"]

                # Si el estado siguiente no está indexado o registrado, se agrega al stack y al arreglo de estados indexados.
                if (next_state not in indexed_states):
                    indexed_states.append(next_state)
                    state_stack.append(next_state)

                # Se agrega el estado siguiente al mapping.
                mapping[current_state_index][char] = indexed_states.index(next_state)

        # Obtención del conjunto de estados del DFA.
        for index in range(len(indexed_states)):
            states.add(index)

       # Obtención del estado inicial del DFA.
        initial_state = indexed_states.index(initial_state)

        # Obtención del conjunto de estados de aceptación del DFA.
        acceptance_states = set(indexed_states.index(state) for state in indexed_states if (state & self.lastpos(expression_tree_root)))

        # Si no hay estados de aceptación, se establece como tal el estado inicial.
        if not acceptance_states:
            acceptance_states = {initial_state}

        # Obtención de estados muertos del DFA.
        deleted_states = set()
        for deleted_state in states.copy():
            if all(mapping[deleted_state][char] == deleted_state for char in alphabet) and deleted_state not in acceptance_states:
                deleted_states.add(deleted_state)
                states.remove(deleted_state)

        # Eliminación de estados muertos del mapping.
        for deleted_state in deleted_states:
            for state in states:
                entry_mapping = mapping.get(state, {})
                for char in alphabet:
                    if entry_mapping.get(char, None) == deleted_state:
                        del mapping[state][char]
            del mapping[deleted_state]

        # Arreglo de DFAs con un estado sin transiciones.
        if len(mapping) < 2:
            states = {0}
            mapping = {0: {char: 0 for char in alphabet}}


        # Retorno del DFA.
        return DFA(
            states=states,
            alphabet=alphabet,
            initial_state=initial_state,
            acceptance_states=acceptance_states,
            mapping=mapping
        )
    
    def visualize_direct_dfa(self, name, dfa):

        description = (name + " of " + self.postfix)
        dot_graph = Digraph(comment=description)
        dot_graph.attr(
            rankdir="LR",
            labelloc="t",
            label=description
        )

        # Iteración para dibujar los estados.
        for state in dfa.states:

            # Dibujo de los estados del autómata.
            if (state in dfa.acceptance_states):
                dot_graph.node(str(state), str(state), shape="doublecircle", style="filled")
            elif (state == dfa.initial_state):
                dot_graph.node(str(state), str(state), shape="circle", style="filled")
            else:
                dot_graph.node(str(state), str(state), shape="circle")

            # Dibujo de las transiciones del autómata.
            for transition in dfa.mapping[state]:
                next_state = dfa.mapping[state][transition]
                dot_graph.edge(str(state), str(next_state), label=transition)

        # Visualización del DFA.
        dot_graph.render(name, format="png", view=True)