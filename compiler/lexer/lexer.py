from compiler.lexer.token_utils import create_token
from compiler.lexer.flattened_state_table import flattened_state_table as state_table

class LexerError(Exception):
    def __init__(self, message: str, position: int, char: str):
        super().__init__(message)
        self.position = position
        self.char = char

def lexer(s):
    state, i, tokens, accepted_token_type, buffer = "S1", 0, [], "", ""
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
                raise LexerError(f"Unexpected character '{char}' at position {i}", i, char)
    else:
        if accepted_token_type:
            create_token(accepted_token_type, buffer, tokens)
    return tokens

