# -*-coding:utf-8 -*-
'''
@File    :   main.py
@Date    :   2023/02/26
@Author  :   Pedro Arriola (20188)
@Version :   1.0
@Desc    :   Main donde se ejecuta toda la logica implementada.
'''

from Postfix import Postfix
from Thompson import Thompson
from Errors import Errors

r = 'a(a|b)*ab'

# Se verifican errores, si los hay
check_regex = Errors(r).valid
print(check_regex)


expression = Postfix(r).postfixExpression
afn = Thompson(expression)










