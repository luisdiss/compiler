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
