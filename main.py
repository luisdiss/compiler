from compiler.lexer.lexer import lexer
from compiler.parser.parser import parser
from compiler.parser.parser_utils import print_children

input = "assign a = 2 + 2 3 + 4 call hello(5+5) func fol(a, b | assign r=5, assign e=2+2){2+2}"

#lexing
tokens = lexer(input)
print(f'Tokens:\n\n{tokens}\n')

#parsing
tokens.append(("$", "$"))
root = parser(tokens)
print('Syntax tree:\n')
print_children(root)