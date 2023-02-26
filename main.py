from Postfix import Postfix

r = 'a(a|b)*ab(a|b)'

expression = Postfix(r)
postfix = expression.get_postfix_string()

print(postfix)