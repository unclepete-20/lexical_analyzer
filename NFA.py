# -*-coding:utf-8 -*-
'''
@File    :   NFA.py
@Date    :   2023/02/26
@Author  :   Pedro Arriola (20188)
@Version :   1.0
@Desc    :   Clase que define la estructura de un AFN.
'''

from Subset import SubsetDFA

class NFA(object):

    def __init__(self, states, alphabet, initial_state, acceptance_state, mapping):
        self.states = states
        self.alphabet = alphabet
        self.initial_state = initial_state
        self.acceptance_state = acceptance_state
        self.mapping = mapping
        
    def simulate(self, test_string):

        # Se obtiene el conjunto de estados alcanzables desde el estado inicial.
        current_state = SubsetDFA.ε_closure({ self.initial_state }, self.mapping)

        # Se recorre la cadena de prueba.
        for symbol in test_string:
            
            # Conjunto de estados alcanzables desde el conjunto de estados actual con el símbolo actual.
            current_state = SubsetDFA.ε_closure(SubsetDFA.move(current_state, 
                                                               symbol, 
                                                               self.mapping), 
                                                               self.mapping)

        
        return (current_state in self.acceptance_states)
        
