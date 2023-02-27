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

r = '(a|b)*a(a|b)(a|b)'

expression = Postfix(r).postfixExpression
print(expression)
afn = Thompson(expression)










