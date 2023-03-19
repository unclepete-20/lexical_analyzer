# -*-coding:utf-8 -*-
'''
@File    :   main.py
@Date    :   2023/02/26
@Author  :   Pedro Arriola (20188)
@Version :   1.0
@Desc    :   Main donde se ejecuta toda la logica implementada.
'''

import time
from Postfix import Postfix
from Thompson import Thompson
from Errors import Errors
from Subset import SubsetDFA

# Regex de prueba

# r = 'a(b*|c+)b|baa'
# r = 'ab*a(b+)'
r = 'b*ab?'

test = 'bbbbab'

# Se verifican errores, si los hay
Errors(r)

# Se convierte la expresion regular a formato postfix
expression = Postfix(r).postfixExpression

# Se realiza la construccion de un AFN
afn = Thompson(expression).nfa


# Se realiza la construccion de un AFD por medio de subconjuntos
subset_dfa = SubsetDFA(expression, afn).subset_dfa
simulate_subset = subset_dfa.simulate(test)

if (simulate_subset == True):
    print(f"\nLa cadena {test} SI pertence a L(r) de la expresion regular {r}\n")
else:
    print(f"\nLa cadena {test} NO pertence a L(r  de la expresion regular {r})\n")










