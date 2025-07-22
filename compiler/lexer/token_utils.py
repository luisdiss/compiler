from enum import Enum, auto

class TokenTypes(Enum):
    keyword = auto()
    ID = auto()
    number_literal = auto()
    string_literal = auto()
    op = auto()
    punctuation = auto()
    whitespace = auto()

def is_keyword(word):
    keywords = set(["func", "struct", "if", "elif", "else", "self", "gt", "lt", "ge", "le", "eq"])
    if word in keywords:
        return True

def create_token(token_type, token_value, tokens):
    if (token_type == TokenTypes.ID.value and is_keyword(token_value)) or token_type == TokenTypes.op.value or token_type == TokenTypes.punctuation.value:
        tokens.append((token_value, token_value))
    elif token_type == TokenTypes.whitespace.value:
        pass
    else:
        tokens.append((token_type, token_value))