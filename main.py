from Postfix import Postfix

r = '(a|b)?ab*'

expression = Postfix(r)
postfix = expression.get_postfix_string()

print(postfix)