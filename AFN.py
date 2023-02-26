# -*-coding:utf-8 -*-
'''
@File    :   NFA.py
@Date    :   2023/02/25
@Author  :   Pedro Arriola (20188)
@Version :   1.0
@Desc    :   Clase que permite construir un AFN a partir de una expresion regular.
'''

from graphviz import Digraph

class State:
    id_counter = 0

    def __init__(self, is_accepting=False):
        self.id = State.id_counter
        State.id_counter += 1
        self.transitions = {}
        self.is_accepting = is_accepting

    def add_transition(self, symbol, next_state):
        if symbol in self.transitions:
            self.transitions[symbol].append(next_state)
        else:
            self.transitions[symbol] = [next_state]


class AFN:
    def __init__(self, postfix_regex):
        self.start_state = None
        self.end_state = None

        state_stack = []

        for token in postfix_regex:
            if token == '|':
                s1 = state_stack.pop()
                s2 = state_stack.pop()

                start = State()
                start.add_transition('ε', s1)
                start.add_transition('ε', s2)

                end = State()
                s1.is_accepting = False
                s2.is_accepting = False
                s1.add_transition('ε', end)
                s2.add_transition('ε', end)

                state_stack.append(start)
                self.start_state = start
                self.end_state = end

            elif token == '.':
                s1 = state_stack.pop()
                s2 = state_stack.pop()

                s2.is_accepting = False
                s1.add_transition('ε', s2)

                state_stack.append(s1)
                self.start_state = s1
                self.end_state = s2

            elif token == '?':
                s = state_stack.pop()

                start = State()
                end = State()

                start.add_transition('ε', s)
                start.add_transition('ε', end)
                s.is_accepting = False
                s.add_transition('ε', end)

                state_stack.append(start)
                self.start_state = start
                self.end_state = end

            elif token == '*':
                s = state_stack.pop()

                start = State()
                end = State()

                start.add_transition('ε', s)
                start.add_transition('ε', end)
                s.is_accepting = False
                s.add_transition('ε', start)
                s.add_transition('ε', end)

                state_stack.append(start)
                self.start_state = start
                self.end_state = end

            elif token == '+':
                s = state_stack.pop()

                start = State()
                end = State()

                start.add_transition('ε', s)
                s.is_accepting = False
                s.add_transition('ε', end)
                s.add_transition('ε', start)

                state_stack.append(start)
                self.start_state = start
                self.end_state = end

            else:
                s = State()
                e = State(True)

                s.add_transition(token, e)

                state_stack.append(s)
                self.start_state = s
                self.end_state = e

        if len(state_stack) != 1:
            raise Exception("Invalid postfix regex")

    def render_afn(self):
        dot = Digraph(comment='AFN')

        dot.attr(rankdir='LR')

        states = set()
        stack = [self.start_state]

        while stack:
            current_state = stack.pop()

            # Add current state to set of visited states
            states.add(current_state)

            # Add accepting state marker
            if current_state.is_accepting:
                dot.node(str(current_state.id), shape='doublecircle')
            else:
                dot.node(str(current_state.id))

            # Add transition edges
            for symbol, next_states in current_state.transitions.items():
                for next_state in next_states:
                    if next_state not in states:
                        stack.append(next_state)
                    if symbol == None:
                        dot.edge(str(current_state.id), str(next_state.id), label='ε')
                    else:
                        dot.edge(str(current_state.id), str(next_state.id), label=symbol)

        dot.attr('node', shape='circle')
        dot.attr('edge', arrowhead='none')

        # Get a sorted list of states by their IDs
        sorted_states = sorted(states, key=lambda s: s.id)

        # Add the states to the graph in the sorted order
        for state in sorted_states:
            if state.is_accepting:
                dot.node(str(state.id), shape='doublecircle')
            else:
                dot.node(str(state.id))

        dot.format = 'pdf'
        dot.render(view=True)


