from compiler.lexer.token_utils import create_token
from compiler.lexer.flattened_state_table import flattened_state_table as state_table

class LexerError(Exception):
    """
    Raised when the lexer encounters a character that cannot be
    consumed by the current state machine.
    """

    def __init__(self, message: str, position: int, char: str) -> None:
        super().__init__(message)
        self.position: int = position
        self.char: str = char


def lexer(s: str) -> list:
    """
    Tokenize the input string using the configured DFA state table.

    The lexer walks the input character by character, following
    transitions defined in ``state_table``. Whenever an accepting
    state is reached, the corresponding token type is remembered.
    If no further transition is possible, the most recently accepted
    token is emitted and lexing resumes from the start state.

    Args:
        s: Input source text to tokenize.

    Returns:
        A list of generated tokens.

    Raises:
        LexerError: If an unexpected character is encountered and no
            valid token has been accepted.
    """
    state: str = "S1"
    i: int = 0
    tokens: list = []
    accepted_token_type: str = ""
    buffer: str = ""

    while i < len(s):
        char = s[i]

        transitions = state_table[state]["transitions"]
        next_state = transitions.get(char)

        if next_state:
            buffer += char
            i += 1
            state = next_state

            if (a := state_table[state].get("accepting_token_type")) is not None:
                accepted_token_type = a
        else:
            if accepted_token_type:
                create_token(accepted_token_type, buffer, tokens)
                state, accepted_token_type, buffer = "S1", "", ""
            else:
                raise LexerError(
                    f"Unexpected character '{char}' at position {i}",
                    i,
                    char,
                )
    else:
        if accepted_token_type:
            create_token(accepted_token_type, buffer, tokens)

    return tokens