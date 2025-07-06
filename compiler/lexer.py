from token_utils import create_token
from flattened_state_table import flattened_state_table as state_table

s = "shshshs if * *& {} % lalalals"
    
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
                raise ValueError("")
    else:
        if accepted_token_type:
            create_token(accepted_token_type, buffer, tokens)
    return tokens

print(lexer(s))

