from compiler.parser.parse_table import parse_table, GrammarProductions
from compiler.parser.parser_utils import Node

def parser(tokens):
    def get_next_token():
        nonlocal token_index
        token_index += 1
        return tokens[token_index]

    node = root = Node(GrammarProductions.P)
    X = GrammarProductions.P
    stack = [("$", "$"), (X, root)]
    token_index = 0
    token_type, a = tokens[token_index]
    while X != "$":
        if isinstance(X, GrammarProductions):
            productions = parse_table.get(X).get(token_type)
            if productions is not None:
                stack.pop()
                children = [] 
                for Y in productions[::-1]:
                    child = Node(Y)
                    children.append(child)
                    stack.append((Y, child))
                node.children = children[::-1]
            else:
                print(f"error no table entry for [{X}, {token_type}]")
                break
        elif X == token_type:
            stack.pop()
            node.value = a
            token_type, a = get_next_token()
        else:
            print(f"current input {X} expected {token_type}")
            break
        X, node = stack[-1]
    return root