from Postfix import Postfix

r = 'a(a|b)*ab(a|b)'

expression = Postfix(r)
alphabet = expression.get_alphabet()

print(alphabet)
print(expression.postfix_final)