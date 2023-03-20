# -*-coding:utf-8 -*-
'''
@File    :   Thompson.py
@Date    :   2023/02/26
@Author  :   Pedro Arriola (20188)
@Version :   1.0
@Desc    :   Clase que implementa el algoritmo de Thompson para la construccion de un AFN.
'''

from NFA import NFA
from graphviz import Digraph

class Thompson(object):
    
    def __init__(self, regex_postfix):
        self.postfix = regex_postfix
        self.nfa = self.thompson_algorithm()
        self.visualize_nfa()

    
    def thompson_algorithm(self):
        
        current_state = 0
        stack = []
        
        for token in self.postfix:

            if (token == "*"):

                nfa_to_kleene = stack.pop()

                kleene_closure = NFA(states=nfa_to_kleene.states | { current_state, current_state + 1 },alphabet=nfa_to_kleene.alphabet,initial_state=current_state,acceptance_state=current_state + 1,
                    mapping={
                        **nfa_to_kleene.mapping,
                        nfa_to_kleene.acceptance_state: {
                            "ε": set([nfa_to_kleene.initial_state, current_state + 1])
                        },
                        current_state: {
                            "ε": set([nfa_to_kleene.initial_state, current_state + 1])
                        },
                        current_state + 1: {}
                    }
                )
                
                current_state += 2
                stack.append(kleene_closure)
            
            elif (token == "?"):

                nfa_to_null = stack.pop()

                nullable = NFA(states=nfa_to_null.states | { current_state, current_state + 1 },alphabet=nfa_to_null.alphabet,initial_state=current_state,acceptance_state=current_state + 1,
                    mapping={
                        **nfa_to_null.mapping,
                        nfa_to_null.acceptance_state: {
                            "ε": set([current_state + 1])
                        },
                        current_state: {
                            "ε": set([nfa_to_null.initial_state, current_state + 1])
                        },
                        current_state + 1: {}
                    }
                )

                current_state += 2
                stack.append(nullable)

            elif (token == "+"):

                nfa_to_positive = stack.pop()

                
                positive_closure = NFA(states=nfa_to_positive.states | { current_state, current_state + 1 },alphabet=nfa_to_positive.alphabet,initial_state=current_state,acceptance_state=current_state + 1,
                    mapping={
                        **nfa_to_positive.mapping,
                        nfa_to_positive.acceptance_state: {
                            "ε": set([nfa_to_positive.initial_state, current_state + 1])
                        },
                        current_state: {
                            "ε": set([nfa_to_positive.initial_state])
                        },
                        current_state + 1: {}
                    }
                )

                
                current_state += 2
                stack.append(positive_closure)

            elif (token == "."):

                second_nfa = stack.pop()
                first_nfa = stack.pop()

                
                concatenation = NFA(states=first_nfa.states | second_nfa.states - { second_nfa.initial_state },alphabet=first_nfa.alphabet | second_nfa.alphabet,initial_state=first_nfa.initial_state,acceptance_state=second_nfa.acceptance_state,
                    mapping={
                        **first_nfa.mapping,
                        **second_nfa.mapping,
                        first_nfa.acceptance_state: {
                            **second_nfa.mapping[second_nfa.initial_state]
                        }
                    }
                )

                stack.append(concatenation)

            elif (token == "|"):
                
                second_nfa = stack.pop()
                first_nfa = stack.pop()

                union_state = NFA(states=set([*first_nfa.states, *second_nfa.states, current_state, current_state + 1]),alphabet=set([*first_nfa.alphabet, *second_nfa.alphabet]),initial_state=current_state,acceptance_state=current_state + 1,
                    mapping={
                        **first_nfa.mapping,
                        **second_nfa.mapping,
                        first_nfa.acceptance_state: {
                            "ε": set([current_state + 1])
                        },
                        second_nfa.acceptance_state: {
                            "ε": set([current_state + 1])
                        },
                        current_state: {
                            "ε": set([first_nfa.initial_state, second_nfa.initial_state])
                        },
                        current_state + 1: {}
                    }
                )

                
                current_state += 2
                stack.append(union_state)

            else:

                char = NFA(states=set([current_state, current_state + 1]),alphabet=set([token]),initial_state=current_state,acceptance_state=current_state + 1,
                    mapping={
                        current_state: {
                            token: set([current_state + 1])
                        },
                        current_state + 1: {}
                    }
                )

                current_state += 2
                stack.append(char)

        final_nfa = stack[-1]
        
        return final_nfa
    
    def visualize_nfa(self):
        
        description = ("NFA of " + self.postfix)
        dot_graph = Digraph(comment=description)
        dot_graph.attr(
            rankdir="LR",
            labelloc="t",
            label=description
        )

        for state in self.nfa.states:
            
            if (state == self.nfa.initial_state):
                dot_graph.node(str(state), str(state), shape="circle", style="filled")
            elif (state == self.nfa.acceptance_state):
                dot_graph.node(str(state), str(state), shape="doublecircle", style="filled")
            else:
                dot_graph.node(str(state), str(state), shape="circle")

            
            for transition in self.nfa.mapping[state]:
                for next_state in self.nfa.mapping[state][transition]:
                    dot_graph.edge(str(state), str(next_state), label=transition)

        
        dot_graph.render("NFA", format="png", view=True)
        
