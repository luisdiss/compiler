from enum import Enum, auto
from compiler.lexer.token_utils import TokenTypes

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

transiton_classes = {CharClasses.letters_: "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_",
                      CharClasses.digits: ''.join(str(i) for i in range(10)),
                      CharClasses.ascii: ''.join(chr(i) for i in range(128)),
                      CharClasses.digits_not_0: ''.join(str(i) for i in range(1,10)),
                      CharClasses.op: "+-*/=><|&!%",
                      CharClasses.punctuation: "();:,[]{}",
                      CharClasses.whitespace: " \n\t\r",
                      CharClasses.dot: ".",
                      CharClasses.zero: "0",
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
          "accepting_token_type": TokenTypes.ID.name},
    "S3":{"transitions": {CharClasses.digits: "S11",
                          CharClasses.dot: "S12"},
          "accepting_token_type": TokenTypes.NUMBER.name},
    "S4":{"transitions": {CharClasses.dot: "S12"},
          "accepting_token_type": TokenTypes.NUMBER.name},
    "S5":{"transitions": {CharClasses.ascii: "S13"}},
    "S6":{"transitions": {},
          "accepting_token_type": TokenTypes.OP.name},
    "S7":{"transitions": {},
          "accepting_token_type": TokenTypes.PUNCTUATION.name},
    "S8":{"transitions": {},
          "accepting_token_type": TokenTypes.WHITESPACEE.name},
    "S9":{"transitions": {CharClasses.letters_: "S9",
                          CharClasses.digits: "S10"},
          "accepting_token_type": TokenTypes.ID.name},
    "S10":{"transitions": {CharClasses.letters_: "S9",
                          CharClasses.digits: "S10"},
           "accepting_token_type": TokenTypes.ID.name},
    "S11":{"transitions": {CharClasses.digits: "S11",
                           CharClasses.dot: "S12"},
           "accepting_token_type": TokenTypes.NUMBER.name},
    "S12":{"transitions": {CharClasses.digits: "S15"}},
    "S13":{"transitions": {CharClasses.ascii: "S13",
                           CharClasses.speech_mark: "S14"}},
    "S14":{"transitions": {},
           "accepting_token_type": TokenTypes.STRING.name},
    "S15":{"transitions": {CharClasses.digits: "S15"},
           "accepting_token_type": TokenTypes.STRING.name}}