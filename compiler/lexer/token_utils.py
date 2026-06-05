from enum import Enum, auto

from enum import Enum, auto


class TokenTypes(Enum):
    """
    Token types recognized by the lexer.
    """

    ID = auto()
    NUMBER = auto()
    STRING = auto()
    OP = auto()
    PUNCTUATION = auto()
    WHITESPACEE = auto()


# Used to determine whether an identifier should be treated as a keyword.
keywords = {
    "func",
    "assign",
    "if",
    "else",
    "return",
    "call",
    "gt",
    "lt",
    "ge",
    "le",
    "eq",
    "ne",
    "true",
    "false",
}


def is_keyword(word: str, keywords: set[str]) -> bool | None:
    """
    Check whether a parsed identifier is a reserved keyword.

    Args:
        word: Identifier text to check.
        keywords: Collection of reserved keywords.

    Returns:
        True if the identifier is a keyword.

    Notes:
        This function intentionally preserves the existing behavior of
        returning ``None`` when the word is not a keyword.
    """
    if word in keywords:
        return True


def create_token(
    token_type: str,
    token_value: str,
    tokens: list,
) -> None:
    """
    Append a token to the token stream.

    Keywords, operators, and punctuation are emitted using their
    literal value as both token type and token value. Whitespace
    tokens are ignored. All other tokens are emitted using their
    lexer token type.

    Args:
        token_type: Name of the token type.
        token_value: Raw token text.
        tokens: Mutable token list to append to.
    """
    if (
        (
            token_type == TokenTypes.ID.name
            and is_keyword(token_value, keywords)
        )
        or token_type == TokenTypes.OP.name
        or token_type == TokenTypes.PUNCTUATION.name
    ):
        tokens.append((token_value, token_value))
    elif token_type == TokenTypes.WHITESPACEE.name:
        pass
    else:
        tokens.append((token_type, token_value))