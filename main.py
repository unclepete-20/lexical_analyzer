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

r = 'a(a|b)*ab'

expression = Postfix(r).postfixExpression
afn = Thompson(expression)










