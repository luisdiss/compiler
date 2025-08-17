from enum import Enum, auto

#tokens that lexer.py can recognise
class TokenTypes(Enum):
    ID = auto()
    NUMBER = auto()
    STRING = auto()
    OP = auto()
    PUNCTUATION  = auto()
    WHITESPACEE = auto()

keywords = set([    
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
    "false"
    ])

#used to see which parsed IDs are actually keywords
def is_keyword(word, keywords):
    if word in keywords:
        return True

def create_token(token_type, token_value, tokens):
    if (token_type == TokenTypes.ID.name and is_keyword(token_value, keywords)) or token_type == TokenTypes.OP.name or token_type == TokenTypes.PUNCTUATION.name:
        tokens.append((token_value, token_value))
    elif token_type == TokenTypes.WHITESPACEE.name:
        pass
    else:
        tokens.append((token_type, token_value))