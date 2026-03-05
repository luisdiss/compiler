from compiler.parser.parse_table import parse_table
from compiler.parser.parser_utils import GrammarProductions, ListInitMarker, TerminalMarkers, NonTerminalMarkers, OpMarkers, BuildMarkers, parser_markers__to_actions

def parser(tokens):
    def get_next_token():
        nonlocal token_index
        token_index += 1
        return tokens[token_index]
    X = GrammarProductions.P
    stack = ["$"]
    semantic_stack = [[]]
    token_index = -1
    token_type, a = get_next_token()
    while X != "$":
        if isinstance(X, GrammarProductions):
            productions = parse_table.get(X).get(token_type)
            if productions is not None:
                stack.extend(productions[::-1])
            else:
                print(f"error no table entry for [{X}, {token_type}]")
                break
        elif isinstance(X, ListInitMarker):
            semantic_stack.append([])
        elif isinstance(X, OpMarkers):
            semantic_stack[-1].append(a)
        elif isinstance(X, TerminalMarkers):
            parser_action = parser_markers__to_actions[X]
            ast_node = parser_action(a)
            semantic_stack[-1].append(ast_node)
        elif isinstance(X, NonTerminalMarkers):
            parser_action = parser_markers__to_actions[X]
            ast_node = parser_action(semantic_stack.pop())
            semantic_stack[-1].append(ast_node)
        elif isinstance(X, BuildMarkers):
            parser_action = parser_markers__to_actions[X]
            ast_node = parser_action(semantic_stack[-1])
            semantic_stack[-1] = []
            semantic_stack[-1].append(ast_node)
        elif X == token_type:
            token_type, a = get_next_token()
        else:
            print(f"current input {X} expected {token_type}")
            break
        X = stack.pop()
    return ast_node