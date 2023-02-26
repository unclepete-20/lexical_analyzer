# -*-coding:utf-8 -*-
'''
@File    :   regex.py
@Date    :   2023/02/26
@Author  :   Pedro Arriola (20188) y Oscar Lopez (20679)
@Version :   1.0
@Desc    :   Implementacion de caracteristicas de un Regex y funcionalidad Postfix
'''

class Regex(object):

    def __init__(self, regex):
        self.expression = regex
        self.operatorStack = []
        self.postfixExpression = self.shunting_yard()

    def precedence(self, token):
        if (token == '('):
            return 1
        elif (token == '|'):
            return 2
        elif (token == '.'):
            return 3
        elif (token == '?'):
            return 4
        elif (token == '*'):
            return 4
        elif (token == '+'):
            return 4
        else:
            return 5

    def shunting_yard(self):

        operators = ['|', '?', '+', '*']
        bin = ['|']

        queue = ""

        for l in range(len(self.expression)):

            s = self.expression[l]

            if ((l + 1) < len(self.expression)):
                r = self.expression[l + 1]

                if ((s != '(') and (r != ')') and (r not in operators) and (s not in bin)):
                    queue += s + '.'

                else:
                    queue += s

            elif (s not in operators):
                queue += s

        postfix = ''
        for exp in queue:

            if (exp == '('):
                self.operatorStack.append(exp)

            elif (exp == ')'):
                while (self.operatorStack[-1] != '('):
                    postfix += self.operatorStack.pop()

                self.operatorStack.pop()

            else:
                while (len(self.operatorStack) > 0):
                    ultimoChar = self.operatorStack[-1]
                    observado = self.precedence(ultimoChar)
                    actual = self.precedence(exp)

                    if (observado >= actual):
                        postfix += self.operatorStack.pop()

                    else:
                        break

                self.operatorStack.append(exp)

        while (len(self.operatorStack) > 0):
            postfix += self.operatorStack.pop()

        return postfix