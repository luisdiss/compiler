from compiler.parser.parse_table import parse_table
from compiler.parser.parser_utils import GrammarProductions, ListInitMarker, TerminalMarkers, NonTerminalMarkers, OpMarkers, BuildMarkers, parser_markers__to_actions
from typing import Any


def parser(tokens: list[tuple[str, str]]) -> Any:
    """
    Parse a token stream using the configured LL parsing table and
    construct an Abstract Syntax Tree (AST).

    The parser maintains:

    - A parsing stack containing grammar symbols.
    - A semantic stack used to build AST nodes.
    - A token cursor into the input stream.

    Grammar reductions trigger parser actions defined in
    ``parser_markers__to_actions`` which construct AST nodes and
    accumulate semantic values.

    Args:
        tokens: Token stream produced by the lexer.

    Returns:
        The root AST node produced by the parse.
    """

    def get_next_token() -> tuple[str, str]:
        """
        Advance to the next token in the input stream.

        Returns:
            The next ``(token_type, token_value)`` tuple.
        """
        nonlocal token_index

        token_index += 1
        return tokens[token_index]

    X: Any = GrammarProductions.P
    stack: list[Any] = ["$"]
    semantic_stack: list[list[Any]] = [[]]
    token_index: int = -1

    token_type, a = get_next_token()

    while X != "$":
        # Expand a non-terminal using the parse table.
        if isinstance(X, GrammarProductions):
            productions = parse_table.get(X).get(token_type)

            if productions is not None:
                stack.extend(productions[::-1])
            else:
                print(f"error no table entry for [{X}, {token_type}]")
                break

        # Initialize a new semantic value accumulator.
        elif isinstance(X, ListInitMarker):
            semantic_stack.append([])

        # Push operator tokens onto the current semantic stack.
        elif isinstance(X, OpMarkers):
            semantic_stack[-1].append(a)

        # Build a terminal AST node.
        elif isinstance(X, TerminalMarkers):
            parser_action = parser_markers__to_actions[X]
            ast_node = parser_action(a)
            semantic_stack[-1].append(ast_node)

        # Reduce a completed non-terminal.
        elif isinstance(X, NonTerminalMarkers):
            parser_action = parser_markers__to_actions[X]
            ast_node = parser_action(semantic_stack.pop())
            semantic_stack[-1].append(ast_node)

        # Build an intermediate AST node from accumulated values.
        elif isinstance(X, BuildMarkers):
            parser_action = parser_markers__to_actions[X]
            ast_node = parser_action(semantic_stack[-1])

            semantic_stack[-1] = []
            semantic_stack[-1].append(ast_node)

        # Match a terminal symbol in the input stream.
        elif X == token_type:
            token_type, a = get_next_token()

        else:
            print(f"current input {X} expected {token_type}")
            break

        X = stack.pop()

    return ast_node