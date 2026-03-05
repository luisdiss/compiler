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

#an enum for parser action markers
class NonTerminalMarkers(Enum):
    P = auto()
    FuncDef = auto()
    FuncBody = auto()
    Return = auto()
    Params = auto()
    Param = auto()
    KeyWordParam = auto()
    Assign = auto()
    Expr = auto()
    Term = auto()
    BinOp = auto()
    UnaryOp = auto()
    Conditional = auto()
    ConditionalBody = auto()
    Comparison = auto()
    Call = auto()
    Args = auto()
    Arg = auto()
    KeyWordArg = auto()

class BuildMarkers(Enum):
    BinOp = auto()

class OpMarkers(Enum):
    AddOp = auto()
    MultOp = auto()
    Unary = auto()
    CompOp = auto()

class TerminalMarkers(Enum):
    Bool = auto()
    NUMBER = auto()
    ExprID = auto()
    DeclID = auto()
    STRING = auto()

class ListInitMarker(Enum):
    ListInit = auto()

#this class is used as a namespace to collect all parser actions
class ParserActions:
    #the below parser actions must accept a list of semantic values and return an astnode
    def P(sem_values):
        return PNode(children=sem_values)
    def FuncDef(sem_values):
        if len(sem_values) == 3: 
            params, funcbody = sem_values[1], sem_values[2]
        elif len(sem_values) == 2 :
            params, funcbody = ParamsNode(children=[]), sem_values[1]
        else:
            params, funcbody = sem_values[1], sem_values[2]
        return FuncDefNode(id=sem_values[0], params=params, funcbody=funcbody)
    def FuncBody(sem_values):
        return FuncBodyNode(children=sem_values)
    def Return(sem_values):
        return ReturnNode(expr=sem_values[0])
    def Params(sem_values):
        return ParamsNode(children=sem_values)
    def Param(sem_values):
        return ParamNode(id=sem_values[0])
    def KeyWordParam(sem_values):
        assign_node=sem_values[0]
        return KeyWordParamNode(id=assign_node.id, expr=assign_node.expr)
    def Assign(sem_values):
        return AssignNode(id=sem_values[0], expr=sem_values[1])
    def Expr(sem_values):
        return ExprNode(entry=sem_values[0])
    def Term(sem_values):
        return sem_values[0]
    def UnaryOp(sem_values):
        return UnaryOpNode(op=sem_values[0], value=sem_values[1])
    def Conditional(sem_values):
        if len(sem_values) == 1: 
            _if, _else = None, None
        elif len(sem_values) == 2:
            _if, _else = sem_values[1], None
        else:
            _if, _else = sem_values[1], sem_values[2]
        return ConditionalNode(comparison=sem_values[0], _if=_if, _else=_else)
    def ConditionalBody(sem_values):
        return ConditionalBodyNode(children=sem_values)
    def Comparsion(sem_values):
        i, n = 0, len(sem_values)
        if n == 1: return ExprNode(sem_values[0])
        comparisons = []
        while i+2 < n:
            comparisons.append(ComparisonOpNode(left=sem_values[i], op=sem_values[i+1], right=sem_values[i+2]))
            i+=2
        return ComparisonsNode(children=comparisons)
    def Call(sem_values):
        if len(sem_values) == 1: args = ArgsNode(children=[])
        else: args = sem_values[1]
        return CallNode(id=sem_values[0], args=args)
    def Args(sem_values):
        return ArgsNode(children=sem_values)
    def Arg(sem_values):
        return ArgNode(expr=sem_values[0])
    def KeyWordArg(sem_values):
        assign_node=sem_values[0]
        return KeyWordArgNode(id=assign_node.id, expr=assign_node.expr)
    
    #the below parser action must clear the current accumulator list, accept a list of semantic values and return an astnode
    def BinOp(sem_values):
        return BinaryOpNode(left=sem_values[0], op=sem_values[1], right=sem_values[2])
    
    #the below parser actions push the current token to the stack
    def AddOp():
        pass
    def MultOp():
        pass
    def Unary():
        pass
    def CompOp():
        pass

    #the below parser actions construct terminal ast nodes by receiving the current token and pushing it onto the stack
    def Bool(token):
        return BoolNode(value=token)
    def Number(token):
        return NumberNode(value=token)
    def ExprID(token):
        return ExprIDNode(value=token) 
    def DeclID(token):
        return DeclIDNode(value=token)
    def String(token):
        return StringNode(value=token)

    #the below parser action pushes an empty accumulator list onto the stack
    def ListInit():
        pass

#map of markers nand tokens to actions
parser_markers__to_actions = {
                    NonTerminalMarkers.P: ParserActions.P,
                    NonTerminalMarkers.FuncDef:ParserActions.FuncDef,
                    NonTerminalMarkers.FuncBody:ParserActions.FuncBody,
                    NonTerminalMarkers.Return:ParserActions.Return,
                    NonTerminalMarkers.Params:ParserActions.Params,
                    NonTerminalMarkers.Param:ParserActions.Param,
                    NonTerminalMarkers.KeyWordParam:ParserActions.KeyWordParam,
                    NonTerminalMarkers.Assign:ParserActions.Assign,
                    NonTerminalMarkers.Expr:ParserActions.Expr,
                    NonTerminalMarkers.Term:ParserActions.Term,
                    NonTerminalMarkers.UnaryOp:ParserActions.UnaryOp,
                    NonTerminalMarkers.Conditional:ParserActions.Conditional,
                    NonTerminalMarkers.ConditionalBody:ParserActions.ConditionalBody,
                    NonTerminalMarkers.Comparison:ParserActions.Comparsion,
                    NonTerminalMarkers.Call: ParserActions.Call,
                    NonTerminalMarkers.Args:ParserActions.Args,
                    NonTerminalMarkers.Arg:ParserActions.Arg,
                    NonTerminalMarkers.KeyWordArg:ParserActions.KeyWordArg,
                    BuildMarkers.BinOp:ParserActions.BinOp,
                    OpMarkers.AddOp:ParserActions.AddOp,
                    OpMarkers.MultOp:ParserActions.MultOp,
                    OpMarkers.Unary:ParserActions.Unary,
                    OpMarkers.CompOp:ParserActions.CompOp,
                    TerminalMarkers.Bool:ParserActions.Bool,
                    TerminalMarkers.NUMBER:ParserActions.Number,
                    TerminalMarkers.ExprID:ParserActions.ExprID,
                    TerminalMarkers.DeclID:ParserActions.DeclID,
                    TerminalMarkers.STRING:ParserActions.String,
                    ListInitMarker.ListInit:ParserActions.ListInit
                }

#AST nodes
class PNode:
    def __init__(self, children):
        self.children = children
    def accept(self, visitor):
        return visitor.visit(self)
    def children_api(self):
        yield from self.children
class FuncDefNode:
    def __init__(self, id, params, funcbody):
        self.id = id
        self.params = params
        self.funcbody = funcbody
    def accept(self, visitor):
        return visitor.visit(self)
    def children_api(self):
        yield self.params
        yield self.funcbody
class FuncBodyNode:
    def __init__(self, children):
        self.children = children
    def accept(self, visitor):
        return visitor.visit(self)
    def children_api(self):
        yield from self.children
class ReturnNode:
    def __init__(self, expr):
        self.expr = expr
    def accept(self, visitor):
        return visitor.visit(self)
    def children_api(self):
        yield self.expr
class ParamsNode:
    def __init__(self, children):
        self.children = children
    def accept(self, visitor):
        return visitor.visit(self)
    def children_api(self):
        yield from self.children
class ParamNode:
    def __init__(self, id):
        self.id = id
        self.has_default = False
    def accept(self, visitor):
        return visitor.visit(self)
    def children_api(self):
        yield self.id
class KeyWordParamNode:
    def __init__(self, id, expr):
        self.id = id
        self.expr = expr
        self.has_default = True
    def accept(self, visitor):
        return visitor.visit(self)
    def children_api(self):
        yield self.id
        yield self.expr
class AssignNode:
    def __init__(self, id, expr):
        self.id = id
        self.expr = expr
    def accept(self, visitor):
        return visitor.visit(self)
    def children_api(self):
        yield self.id
        yield self.expr
class ExprNode:
    def __init__(self, entry):
        self.entry = entry
    def accept(self, visitor):
        return visitor.visit(self)
    def children_api(self):
        yield self.entry
class BinaryOpNode:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right
    def accept(self, visitor):
        return visitor.visit(self)
    def children_api(self):
        yield self.left
        yield self.right
class UnaryOpNode:
    def __init__(self, op, value):
        self.op = op
        self.value = value
    def accept(self, visitor):
        return visitor.visit(self)
    def children_api(self):
        yield self.value
class ConditionalNode:
    def __init__(self, comparison, _if, _else):
        self.comparison = comparison
        self._if = _if
        self._else = _else
    def accept(self, visitor):
        return visitor.visit(self)
    def children_api(self):
        yield self.comparison
        yield self._if
        if self._else:
            yield self._else
class ConditionalBodyNode:
    def __init__(self, children):
        self.children = children
    def accept(self, visitor):
        return visitor.visit(self)
    def children_api(self):
        yield from self.children
class ComparisonOpNode:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right
    def accept(self, visitor):
        return visitor.visit(self)
    def children_api(self):
        yield self.left
        yield self.right
class ComparisonsNode:
    def __init__(self, children):
        self.children = children
    def accept(self, visitor):
        return visitor.visit(self)
    def children_api(self):
        yield from self.children
class BoolNode:
    def __init__(self, value):
        self.value = value
    def accept(self, visitor):
        return visitor.visit(self)
    def children_api(self):
        return []
class CallNode:
    def __init__(self, id, args):
        self.id = id
        self.args = args
        self.param_arg_map = {}
    def accept(self, visitor):
        return visitor.visit(self)
    def children_api(self):
        yield self.id
        yield self.args
class ArgsNode:
    def __init__(self, children):
        self.children = children
    def accept(self, visitor):
        return visitor.visit(self)
    def children_api(self):
        yield from self.children
class ArgNode:
    def __init__(self, expr):
        self.expr = expr
    def accept(self, visitor):
        return visitor.visit(self)
    def children_api(self):
        yield self.expr
class KeyWordArgNode:
    def __init__(self, id, expr):
        self.id = id
        self.expr = expr
    def accept(self, visitor):
        return visitor.visit(self)
    def children_api(self):
        yield self.id
        yield self.expr
class NumberNode:
    def __init__(self, value):
        self.value = value
    def accept(self, visitor):
        return visitor.visit(self)
    def children_api(self):
        return []
class ExprIDNode:
    def __init__(self, value):
        self.value = value
        self.symbol = None
    def accept(self, visitor):
        return visitor.visit(self)
    def children_api(self):
        return []
class DeclIDNode:
    def __init__(self, value):
        self.value = value
        self.symbol = None
    def accept(self, visitor):
        return visitor.visit(self)
    def children_api(self):
        return []
class StringNode:
    def __init__(self, value):
        self.value = value
    def accept(self, visitor):
        return visitor.visit(self)
    def children_api(self):
        return []
    
class ASTPrinter:
    def __init__(self):
        self.indent = 0

    def _pad(self):
        return "  " * self.indent
    
    def _print(self, text):
        print(self._pad() + text)

    def visit(self, node):
        if node is None:
            self._print("None")
            return
        method = "visit_" + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        visitor(node)

    def generic_visit(self, node):
        self._print(node.__class__.__name__)
        self.indent += 1
        for attr, value in vars(node).items():
            self._print(f"{attr}:")
            self.indent += 1
            self._visit_value(value)
            self.indent -= 1
        self.indent -= 1

    def _visit_value(self, value):
        if isinstance(value, list):
            for v in value:
                self.visit(v)
        elif hasattr(value, "__dict__"):
            self.visit(value)
        else:
            self._print(repr(value))

class ASTPrinter(ASTPrinter):

    def visit_PNode(self, node):
        self._print("Program")
        self.indent += 1
        for child in node.children:
            self.visit(child)
        self.indent -= 1

    def visit_FuncDefNode(self, node):
        self._print(f"FuncDef {node.id.value} type {node.id.symbol.type}")
        self.indent += 1
        self._print("Params:")
        self.indent += 1
        self.visit(node.params)
        self.indent -= 1
        self._print("Body:")
        self.indent += 1
        self.visit(node.funcbody)
        self.indent -= 2

    def visit_FuncBodyNode(self, node):
        self.indent += 1
        for stmt in node.children:
            self.visit(stmt)
        self.indent -= 1

    def visit_ReturnNode(self, node):
        self._print("Return")
        self.indent += 1
        self.visit(node.expr)
        self.indent -= 1

    def visit_ParamsNode(self, node):
        self._print("Params")
        self.indent += 1
        for p in node.children:
            self.visit(p)
        self.indent -= 1

    def visit_ParamNode(self, node):
        self._print(f"Param {node.id.value} type: {node.id.symbol.type}")

    def visit_KeyWordParamNode(self, node):
        self._print(f"KeyWordParam {node.id.value} type: {node.id.symbol.type}")
        self.indent += 1
        self.visit(node.expr)
        self.indent -= 1

    def visit_AssignNode(self, node):
        self._print(f"Assign {node.id.value} type: {node.id.symbol.type}")
        self.indent += 1
        self.visit(node.expr)
        self.indent -= 1

    def visit_ExprNode(self, node):
        self._print("Expr")
        self.indent += 1
        self.visit(node.entry)
        self.indent -= 1

    def visit_BinaryOpNode(self, node):
        self._print(f"BinaryOp {node.op}")
        self.indent += 1
        self.visit(node.left)
        self.visit(node.right)
        self.indent -= 1

    def visit_UnaryOpNode(self, node):
        self._print(f"UnaryOp {node.op}")
        self.indent += 1
        self.visit(node.value)
        self.indent -= 1

    def visit_ConditionalNode(self, node):
        self._print("Conditional")
        self.indent += 1
        self._print("Condition:")
        self.indent += 1
        self.visit(node.comparison)
        self.indent -= 1
        self._print("If:")
        self.indent += 1
        self.visit(node._if)
        self.indent -= 1
        self._print("Else:")
        self.indent += 1
        self.visit(node._else)
        self.indent -= 2

    def visit_ConditionalBodyNode(self, node):
        self._print("ConditionalBody")
        self.indent += 1
        for stmt in node.children:
            self.visit(stmt)
        self.indent -= 1
    
    def visit_ComparisonsNode(self, node):
        self._print("Comparisons")
        self.indent += 1
        for stmt in node.children:
            self.visit(stmt)
        self.indent -= 1

    def visit_ComparisonOpNode(self, node):
        self._print(f"Compare {node.op}")
        self.indent += 1
        self.visit(node.left)
        self.visit(node.right)
        self.indent -= 1

    def visit_BoolNode(self, node):
        self._print(f"Bool {node.value}")

    def visit_CallNode(self, node):
        self._print(f"Call {node.id.value} type: {node.id.symbol.type}")
        self.indent += 1
        self.visit(node.args)
        self.indent -= 1

    def visit_ArgsNode(self, node):
        self._print("Args")
        self.indent += 1
        for arg in node.children:
            self.visit(arg)
        self.indent -= 1

    #we cant get the type of the arg because it is on the parameter.
    def visit_ArgNode(self, node):
        self._print(f"Arg")
        self.indent += 1
        self.visit(node.expr)
        self.indent -= 1

    def visit_KeyWordArgNode(self, node):
        self._print(f"KeyWordArg {node.id.value}")
        self.indent += 1
        self.visit(node.expr)
        self.indent -= 1

    def visit_NumberNode(self, node):
        self._print(f"Number {node.value}")

    def visit_ExprIDNode(self, node):
        self._print(f"ID {node.value} type: {node.symbol.type}")
    
    def visit_DeclIDNode(self, node):
        self._print(f"ID {node.value} type: {node.symbol.type}")

    def visit_StringNode(self, node):
        self._print(f"String {node.value}")