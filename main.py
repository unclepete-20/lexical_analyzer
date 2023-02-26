from Postfix import Regex
from AFN import AFN

r = 'a(a|b)*ab'
filename = 'automata'

expression = Regex(r).postfixExpression
afn = AFN(expression)


print(expression)
afn.render_afn()




