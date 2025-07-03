from enum import Enum, auto
from token_utils import TokenTypes

class CharClasses(Enum):
    letters_ = auto()
    digits = auto()
    ascii = auto()
    digits_not_0 = auto()
    op = auto()
    punctuation = auto()
    whitespace = auto()
    dot = auto()
    zero = auto()
    speech_mark = auto()

transiton_classes = {CharClasses.letters_: set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_"),
                      CharClasses.digits: set(str(i) for i in range(0,10)),
                      CharClasses.ascii: set(chr(i) for i in range(128)),
                      CharClasses.digits_not_0: set(str(i) for i in range(1,10)),
                      CharClasses.op: set("+-*/=><|&!%"),
                      CharClasses.punctuation: set("();:,[]{}"),
                      CharClasses.whitespace: set(" \n\t\r"),
                      CharClasses.dot: ".",
                      CharClasses.zero: str(""),
                      CharClasses.speech_mark: "\""
}

raw_state_table = {
    "S1":{"transitions": {CharClasses.letters_: "S2",
                           CharClasses.digits_not_0: "S3",
                           CharClasses.zero: "S4",
                           CharClasses.speech_mark: "S5",
                           CharClasses.op: "S6",
                           CharClasses.punctuation: "S7",
                           CharClasses.whitespace: "S8"}},
    "S2":{"transitions": {CharClasses.letters_: "S9",
                          CharClasses.digits: "S10"},
          "accepting_token_type": TokenTypes.ID.value},
    "S3":{"transitions": {CharClasses.digits: "S11",
                          CharClasses.dot: "S12"},
          "accepting_token_type": TokenTypes.number_literal.value},
    "S4":{"transitions": {CharClasses.dot: "S12"},
          "accepting_token_type": TokenTypes.number_literal.value},
    "S5":{"transitions": {CharClasses.ascii: "S13"}},
    "S6":{"transitions": {},
          "accepting_token_type": TokenTypes.op.value},
    "S7":{"transitions": {},
          "accepting_token_type": TokenTypes.punctuation.value},
    "S8":{"transitions": {},
          "accepting_token_type": TokenTypes.whitespace.value},
    "S9":{"transitions": {CharClasses.letters_: "S9",
                          CharClasses.digits: "S10"},
          "accepting_token_type": TokenTypes.ID.value},
    "S10":{"transitions": {CharClasses.letters_: "S9",
                          CharClasses.digits: "S10"},
           "accepting_token_type": TokenTypes.ID.value},
    "S11":{"transitions": {CharClasses.digits: "S11",
                           CharClasses.dot: "S12"},
           "accepting_token_type": TokenTypes.number_literal.value},
    "S12":{"transitions": {CharClasses.digits: "S15"}},
    "S13":{"transitions": {CharClasses.ascii: "S13",
                           CharClasses.speech_mark: "S14"}},
    "S14":{"transitions": {},
           "accepting_token_type": TokenTypes.string_literal.value},
    "S15":{"transitions": {CharClasses.digits: "S15"},
           "accepting_token_type": TokenTypes.string_literal.value}}