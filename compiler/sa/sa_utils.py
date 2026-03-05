from compiler.parser.parser_utils import KeyWordParamNode, ParamNode, ArgNode, KeyWordArgNode, FuncDefNode
from enum import Enum, auto

#a semantic analysis state object which persists for the lifetime of semantic analysis
class SA:
    def __init__(self):
        dummy_scope = Scope()
        self.scope_tree = dummy_scope
        self.node_to_scope = {}
        self.scope_stack = [dummy_scope]

#scope class
class Scope():
    def __init__(self):
        self.symbol_table = {}
        self.parent = None
        self.constraints = []
        self.substitution = {}
        self.func_id_symbol = None

#symbol object owned by all ID nodes 
class Symbol():
    def __init__(self, id):
        self.id = id
        self.type = None
        #below attrs only used for function ids
        self.funcdef_node = None
        self.params = None
        self.kwparams = None
        self.param_map = None
        self.analysed = False

#types enum
class Types(Enum):
    number = auto()
    string = auto()
    bool = auto()

#visitor responsible for scoping and declaring variables
class ScopeDeclBaseVisitor():
    def __init__(self, SA):
        self.SA = SA

    def visit(self, node):
        self.SA.node_to_scope[node] = self.SA.scope_stack[-1]
        methodname = "visit_" + node.__class__.__name__
        visit = getattr(self, methodname, None)
        if visit: visit(node)
        else: self.generic_visitor(node)
    
    def generic_visitor(self, node):
        if node:
            for child in node.children_api(): self.visit(child)

class ScopeDeclVisitor(ScopeDeclBaseVisitor):
    def __init__(self, SA):
        super().__init__(SA)

    #visit functions
    def visit_PNode(self, node):
        self.enter_scope(node)
        for child in node.children: self.visit(child)
        self.exit_scope()

    def visit_FuncDefNode(self, node):
        self.visit(node.id)
        for param in node.params.children:
            if isinstance(param, KeyWordParamNode): self.visit(param.expr)

        self.enter_scope(node)
        for param in node.params.children: self.visit(param.id)
        self.visit(node.funcbody)
        self.exit_scope()
    
    def visit_ExprIDNode(self, node): 
        self.resolve_id(node)
    
    def visit_DeclIDNode(self, node): 
        self.check_decl(node)
    
    #semantic functions
    def get_curr_scope(self, node):
        return self.SA.node_to_scope[node]
    
    def enter_scope(self, node):
        scope = Scope()
        scope.parent = self.SA.scope_tree
        self.SA.scope_tree = scope
        self.SA.scope_stack.append(scope)
        if isinstance(node, FuncDefNode): scope.func_id_symbol = node.id.symbol

    def exit_scope(self):
        self.SA.scope_stack.pop()
    
    def check_decl(self, node):
        curr_scope = self.get_curr_scope(node)
        id = node.value
        if id not in curr_scope.symbol_table: 
            new_symbol = Symbol(id)
            curr_scope.symbol_table[id] = new_symbol
            node.symbol = new_symbol
        else: print(f"{id} already defined in scope")
    
    def resolve_id(self, node):
        scope = self.SA.node_to_scope[node]        
        while scope:
            if node.value in scope.symbol_table:
                node.symbol = scope.symbol_table[node.value]
                break
            scope = scope.parent
        else: print(f"{node.value} not defined")

#a visitor responsible for inferring all types
class InferenceBaseVisitor:
    def __init__(self, SA):
        self.SA = SA

    def visit(self, node):
        methodname = "visit_" + node.__class__.__name__
        visit = getattr(self, methodname, self.generic_visit)
        return visit(node)

    def generic_visit(self, node):
        if node: 
            for child in node.children_api(): self.visit(child)

class InferenceVisitor(InferenceBaseVisitor):
    def __init__(self, SA):
        super().__init__(SA)

    #visit functions
    def visit_FuncDefNode(self, node):
        node.id.symbol.param_map = {param.id.value:param for param in node.params.children}
        node.id.symbol.params = [paramnode for paramnode in node.params.children]
        node.id.symbol.funcdef_node = node
    
    def visit_CallNode(self, node):
        symbol = node.id.symbol
        param_arg_map = self.bind_call_arguments(node, symbol)

        if not symbol.analysed:
            self.infer_parameter_types(symbol, param_arg_map)
            self.visit(symbol.funcdef_node.funcbody)
            symbol.analysed = True
        else: self.check_argument_types(symbol, param_arg_map)
        return symbol.type
    
    def visit_ReturnNode(self, node):
        scope = self.SA.node_to_scope[node]
        func_scope = scope
        while func_scope and not hasattr(func_scope, "func_id_symbol"): func_scope = func_scope.parent
        func_id_symbol = func_scope.func_id_symbol
        func_id_symbol.type = self.visit(node.expr)

    def visit_ArgNode(self, node):
        node.id.symbol.type = self.visit(node.expr)

    def visit_AssignNode(self, node):
        node.id.symbol.type = self.visit(node.expr)
    
    def visit_ExprNode(self, node):
        return self.visit(node.entry)
    
    def visit_BinaryOpNode(self, node):
        left_t = self.visit(node.left)
        right_t = self.visit(node.right)
        if left_t == right_t and left_t == Types.number: return Types.number
        else: print(f"error: both left and right operands of {node.op.value} must be of type number")
    
    def visit_CompOpNode(self, node):
        left_t = self.visit(node.left)
        right_t = self.visit(node.right)
        if left_t == right_t and left_t == Types.number: return Types.number
        else: print(f"error: both left and right operands of {node.op.value} must be of type number")
    
    def visit_UnaryOpNode(self, node):
        return self.visit(node.value)

    def visit_ExprIDNode(self, node):
        return node.symbol.type

    def visit_NumberNode(self, node):
        return Types.number
    
    def visit_StringNode(self, node):
        return Types.string

    def visit_BoolNode(self, node):
        return Types.bool

    #semantic functions
    def infer_parameter_types(self, symbol, param_arg_map):
        for param in symbol.params:
            #compute default type if needed
            default_type = None
            if param.has_default: default_type = self.visit(param.expr)
            arg_node = param_arg_map[param]

            #check if this binding came from default
            using_default = param.has_default and arg_node is param.expr

            if using_default: param.id.symbol.type = default_type
            else: 
                arg_type = self.visit(arg_node.expr)
                if param.has_default:
                    if arg_type != default_type:
                            print(f"type mismatch for parameter '{param.id.value}': ")
                            print(f"default type {default_type}, ")
                            print(f"argument type {arg_type}")
                            return
                
                param.id.symbol.type = arg_type

    def check_argument_types(self, symbol, param_arg_map):
        for param in symbol.params:
            param_id = param.id
            arg_node = param_arg_map[param]
            arg_type = self.visit(arg_node.expr)

            if arg_type != param_id.symbol.type:
                    print(f"type mismatch for parameter '{param_id.value}': ")
                    print(f"expected {param_id.symbol.type}, got {arg_type}")

    def bind_call_arguments(self, call_node, symbol):
        #change parser to separate args and kwargs
        args = [arg for arg in call_node.args.children if isinstance(arg, ArgNode)]
        kwargs = [arg for arg in call_node.args.children if isinstance(arg, KeyWordArgNode)]
        params = symbol.params
        param_map = symbol.param_map
        param_arg_map = {}
        total_params = len(params)

        if len(args) + len(kwargs) > total_params:
            print(f"error: too many arguments in call to {call_node.id.value}")

        #bind positional args
        for i, arg in enumerate(args):
            param = params[i]
            param_arg_map[param] = arg

        #bind keyword args
        for kwarg in kwargs:
            name = kwarg.id.value
            if name not in param_map:
                print(f"error: unknown parameter '{name}' in call to {call_node.id.value}")
            param = param_map[name]
            if param in param_arg_map:
                print(f"error: parameter '{name}' already bound")
            param_arg_map[param] = kwarg

        #check for missing positonal args
        for param in params:
            if param not in param_arg_map:
                if param.has_default: param_arg_map[param] = param.expr
                else: print(f"error: missing required parameter '{param.id.value}'")

        return param_arg_map