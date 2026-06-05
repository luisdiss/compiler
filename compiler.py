from compiler.lexer.lexer import lexer
from compiler.parser.parser import parser
from compiler.parser.parser_utils import ASTPrinter
from compiler.sa.semantic_analyser import semantic_analyser
import sys

filename = sys.argv[1]

with open(filename, 'r') as file:
    content = file.read()

#lexing
tokens = lexer(content)
print(f'Tokens:\n\n{tokens}\n')

#parsing
tokens.append(("$", "$"))
root = parser(tokens)

#semantic analysis + code gen
semantic_analyser(root)

print('Syntax tree:\n')
printer = ASTPrinter()
printer.visit(root)