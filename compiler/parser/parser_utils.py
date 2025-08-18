from enum import Enum, auto

#an enum for the nonterminals of the grammar
class GrammarProductions(Enum):
    #spacing matches the grammar defined in compiler/parser/grammar.txt
    P = auto()
    StmtList = auto()
    Stmt = auto()

    FuncDef = auto()
    FuncBody = auto()
    FuncEntry = auto()

    Params = auto()
    ParamList = auto()
    ParamListRest = auto()
    KeyWordParamListTail = auto()
    KeyWordParamListTailRest = auto()
    KeyWordParamList = auto()
    KeyWordParamListRest = auto()
    Param = auto()
    KeyWordParam = auto()

    Assign = auto()

    Expr = auto()
    ExprRest = auto()
    Term = auto()
    TermRest = auto()
    Factor = auto()
    UnaryOp = auto()
    AddOp = auto()
    MultOp = auto()
    Atom = auto()

    Conditional = auto()
    ConditionalRest = auto()
    Comparsion = auto()
    ComparisonTail = auto()
    CompOp = auto()
    Bool = auto()
    ConditionalBody = auto()
    Conditionalentry = auto()

    Call = auto()

    Args = auto()
    ArgList = auto()
    ArgListRest = auto()
    KeyWordArgListTail = auto()
    KeyWordArgListTailRest = auto()
    KeyWordArgList = auto()
    KeyWordArgListRest = auto()
    Arg = auto()
    KeyWordArg = auto()

class Node:
    def __init__(self, symbol):
        self.symbol = symbol
        self.value = None
        self.children = []
    
def print_children(node, space=' '):
    if node.children:
        for i in node.children:
            print(f"{space}({i.symbol}: {i.value})")
            print_children(i, space=space+' ')