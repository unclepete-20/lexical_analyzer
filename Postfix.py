# -*-coding:utf-8 -*-
'''
@File    :   Postfix.py
@Date    :   2023/02/24
@Author  :   Pedro Arriola (20188)
@Version :   1.0
@Desc    :   Clase para convertir un regex de formato infix a postfix.
'''

class Postfix(object):
    
    def __init__(self, regex):
        self.regex = self.concatenation(regex)
        self.postfix = self.infix_to_postfix()
        self.stack = []
        self.operators = ["*", "+", "|", "?", "."]
        self.precedence = {
            "|": 1,
            "*": 2,
            "+": 2,
            "?": 2,
            ".": 3
        }
    
    
    
    # Convierte regex de infix a postfix utilizando Shunting Yard Algorithm
    def infix_to_postfix(self):
        pass
    
    
    # Permite agregar el operador de concatenacion antes de convertir el regex a postfix
    def concatenation(self, infix_regex):
        pass