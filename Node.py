# -*-coding:utf-8 -*-
'''
@File    :   Node.py
@Date    :   2023/03/10
@Author  :   Pedro Arriola (20188)
@Version :   1.0
@Desc    :   Clase que define la estructura de un nodo para construir el arbol sintactico.
'''

class Node(object):
    def __init__(self, value, position=None):
        self.value = value
        self.position = position
        self.left = None
        self.right = None
        self.properties = { "firstpos": set(), 
                           "lastpos": set(), 
                           "followpos": set() }

    def print_tree_by_inorder(self):
        if (self.left != None):
            self.left.print_tree_by_inorder()
        print(self.value)
        if (self.right != None):
            self.right.print_tree_by_inorder()