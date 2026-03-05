from compiler.lexer.lexer import lexer
from compiler.parser.parser import parser
from compiler.parser.parser_utils import ASTPrinter
from compiler.sa.semantic_analyser import semantic_analyser

input = """
func fol(a){
    return a+2*3
}
call fol(1)

if 1 lt 2 gt 3{
    assign b = "hello world!"
}
"""
    
#lexing
tokens = lexer(input)
print(f'Tokens:\n\n{tokens}\n')

#parsing
tokens.append(("$", "$"))
root = parser(tokens)

#semantic analysis + code gen
semantic_analyser(root)

print('Syntax tree:\n')
printer = ASTPrinter()
printer.visit(root)