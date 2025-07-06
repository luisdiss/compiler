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
    keywords = set(["for", "while", "break", "ret", "def", "in", "if", "elif", "else", "int", "flo", "str"])
    if word in keywords:
        return True

def create_token(token_type, token_value, tokens):
    if token_type == TokenTypes.ID.value and is_keyword(token_value):
        tokens.append((TokenTypes.keyword.value, token_value))
    elif token_type == TokenTypes.whitespace.value:
        pass
    else:
        tokens.append((token_type, token_value))