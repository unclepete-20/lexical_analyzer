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

        
        print(f"\nSimulacion de la cadena de prueba {test_string} por medio de NFA\n")
        
        # Se devuelve la respuesta final
        if (self.acceptance_state in current_state):
            print(f"\nLa cadena de prueba {test_string} SI pertenece a L(r)\n")
        else:
            print(f"\nLa cadena de prueba {test_string} NO pertenece a L(r)\n")
        
