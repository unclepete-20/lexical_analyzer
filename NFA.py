# -*-coding:utf-8 -*-
'''
@File    :   NFA.py
@Date    :   2023/02/26
@Author  :   Pedro Arriola (20188)
@Version :   1.0
@Desc    :   Clase que define la estructura de un AFN.
'''

class NFA(object):

    def __init__(self, states, alphabet, initial_state, acceptance_state, mapping):
        self.states = states
        self.alphabet = alphabet
        self.initial_state = initial_state
        self.acceptance_state = acceptance_state
        self.mapping = mapping