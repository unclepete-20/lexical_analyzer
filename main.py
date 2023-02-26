from Postfix import Postfix
from AFN import AFN

r = 'a(a|b)*ab'
filename = 'automata'

expression = Postfix(r).postfixExpression
afn = AFN(expression)


print(expression)
afn.render_afn()




