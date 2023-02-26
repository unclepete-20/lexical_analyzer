# -*-coding:utf-8 -*-
'''
@File    :   Postfix.py
@Date    :   2023/02/24
@Author  :   Pedro Arriola (20188)
@Version :   1.0
@Desc    :   Clase para convertir un regex de formato infix a postfix.
'''

import re


class Postfix(object):
    def __init__(self, regex):
        self.regex = regex
        self.operators = {'|': 1, '.': 2, '*': 3, '?': 3, '+': 3}
        self.tokens = self.tokenize()
        self.postfix = self.shunting_yard()
        self.add_concatenation()
        self.postfix_final = self.get_postfix_string()
    
    def add_concatenation(self):
        i = 0
        while i < len(self.postfix) - 1:
            curr_token = self.postfix[i]
            next_token = self.postfix[i+1]
            if self.is_operand(curr_token) and self.is_operand(next_token):
                # Add the concatenation operator
                self.postfix.insert(i+1, '.')
                i += 1
            elif curr_token == ')' and next_token == '(':
                # Add the concatenation operator
                self.postfix.insert(i+1, '.')
                i += 1
            i += 1
        # Add concatenation operator at end of expression
        if len(self.postfix) > 1 and self.postfix[-1] not in '|.)':
            self.postfix.append('.')
    
    def is_operand(self, token):
        return token.isalpha() or token == 'ε'
    
    def shunting_yard(self):
        output = []
        operator_stack = []
        for token in self.tokens:
            if self.is_operand(token):
                output.append(token)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                while operator_stack[-1] != '(':
                    output.append(operator_stack.pop())
                operator_stack.pop()
            else:
                while operator_stack and operator_stack[-1] != '(' and self.operators.get(token, 0) <= self.operators.get(operator_stack[-1], 0):
                    output.append(operator_stack.pop())
                operator_stack.append(token)
        while operator_stack:
            output.append(operator_stack.pop())
        return output
    
    def tokenize(self):
        tokens = []
        i = 0
        while i < len(self.regex):
            if self.regex[i] == '\\':
                # Escaped character
                tokens.append(self.regex[i:i+2])
                i += 2
            elif self.regex[i] in self.operators.keys() or self.regex[i] in "()":
                # Operator or Parenthesis
                tokens.append(self.regex[i])
                i += 1
            else:
                # Operand
                j = i + 1
                while j < len(self.regex) and self.regex[j] not in self.operators.keys() and self.regex[j] not in "()":
                    j += 1
                tokens.append(self.regex[i:j])
                i = j
        # Replace ? with |ε
        for i in range(len(tokens)):
            if tokens[i] == '?':
                tokens[i] = '|'
                tokens.insert(i+1, 'ε')
        return tokens
    
    def get_postfix_string(self):
        postfix_final = ''.join(self.postfix)
        return postfix_final
    
    def get_alphabet(self):
        
        substrings = re.findall(r'\b\w+\b', self.postfix_final)
        full_string = "".join(substrings)
        
        alphabet = set()
        
        for token in full_string:
            if token.isalpha() and token not in alphabet:
                alphabet.add(token)
        
        return sorted(list(alphabet))
            
        