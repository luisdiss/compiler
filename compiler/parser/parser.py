from compiler.parser.parse_table import parse_table
from compiler.parser.parser_utils import (
    GrammarProductions, ListInitMarker, TerminalMarkers, NonTerminalMarkers,
    OpMarkers, BuildMarkers, parser_markers__to_actions,
)
from compiler.errors import ParseError, SourcePos
from compiler.lexer.token_utils import Token
from typing import Any


def parser(tokens: list) -> Any:
    """
    Parse a token stream using the configured LL parsing table and
    construct an Abstract Syntax Tree (AST).

    Args:
        tokens: Token stream produced by the lexer.

    Returns:
        The root AST node produced by the parse.

    Raises:
        ParseError: If the token stream does not conform to the grammar.
    """

    def get_next_token() -> Any:
        nonlocal token_index
        token_index += 1
        return tokens[token_index]

    def current_pos() -> SourcePos | None:
        if isinstance(current_token, Token) and current_token.line > 0:
            return SourcePos(current_token.line, current_token.col)
        return None

    X: Any = GrammarProductions.P
    stack: list[Any] = ["$"]
    semantic_stack: list[list[Any]] = [[]]
    token_index: int = -1
    ast_node: Any = None

    current_token = get_next_token()
    token_type, a = current_token

    while X != "$":
        if isinstance(X, GrammarProductions):
            productions = parse_table.get(X).get(token_type)
            if productions is not None:
                stack.extend(productions[::-1])
            else:
                desc = "unexpected end of input" if a == "$" else f"unexpected token '{a}'"
                raise ParseError(f"{desc} (in state {X.name})", current_pos())

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
            current_token = get_next_token()
            token_type, a = current_token

        else:
            raise ParseError(
                f"Expected '{X}' but got '{a}'",
                current_pos(),
            )

        X = stack.pop()

    return ast_node
