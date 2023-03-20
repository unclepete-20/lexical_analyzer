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
    
    # Método para simular un NFA.
    def simulate(self, input_string):
        
        mapping = self.mapping
        
        # Se obtiene el conjunto de estados alcanzables desde el estado inicial.
        current_state = SubsetDFA.ε_closure({ self.initial_state }, mapping)

        # Se recorre la cadena de entrada.
        for symbol in input_string:

            # Se obtiene el conjunto de estados alcanzables desde el conjunto de estados actual con el símbolo actual.
            current_state = SubsetDFA.ε_closure(SubsetDFA.move(current_state, symbol, self.mapping), self.mapping)

        # Se retorna si el estado de aceptación está en el conjunto de estados actual.
        return (self.acceptance_state in current_state)
        
