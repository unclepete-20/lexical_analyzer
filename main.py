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

r = 'a(a|b)*ab'
test = 'abbbbbab'

# Se verifican errores, si los hay
check_regex = Errors(r).valid
print(check_regex)

# Se convierte la expresion regular a formato postfix
expression = Postfix(r).postfixExpression

# Se realiza la construccion de un AFN
afn = Thompson(expression).nfa

subset_dfa = SubsetDFA(expression, afn)










