from compiler.lexer.token_utils import TokenTypes
from compiler.parser.parser_utils import GrammarProductions

#tokens that were distinguised in create_token have been entered as raw strings. This is error prone and support to add new tokens to TokenTypes post lexing is needed.
parse_table = {
    GrammarProductions.P: {
        'func': [GrammarProductions.StmtList],
        '+': [GrammarProductions.StmtList],
        '-': [GrammarProductions.StmtList],
        '(': [GrammarProductions.StmtList],
        TokenTypes.NUMBER.name: [GrammarProductions.StmtList],
        TokenTypes.STRING.name: [GrammarProductions.StmtList],
        TokenTypes.ID.name: [GrammarProductions.StmtList],
        'call': [GrammarProductions.StmtList],
        'assign': [GrammarProductions.StmtList],
        'if': [GrammarProductions.StmtList],
        '$': [GrammarProductions.StmtList]
    },
    GrammarProductions.StmtList: {
        'func': [GrammarProductions.Stmt, GrammarProductions.StmtList],
        '+': [GrammarProductions.Stmt, GrammarProductions.StmtList],
        '-': [GrammarProductions.Stmt, GrammarProductions.StmtList],
        '(': [GrammarProductions.Stmt, GrammarProductions.StmtList],
        TokenTypes.NUMBER.name: [GrammarProductions.Stmt, GrammarProductions.StmtList],
        TokenTypes.STRING.name: [GrammarProductions.Stmt, GrammarProductions.StmtList],
        TokenTypes.ID.name: [GrammarProductions.Stmt, GrammarProductions.StmtList],
        'call': [GrammarProductions.Stmt, GrammarProductions.StmtList],
        'assign': [GrammarProductions.Stmt, GrammarProductions.StmtList],
        'if': [GrammarProductions.Stmt, GrammarProductions.StmtList],
        '$': []
    },
    GrammarProductions.Stmt: {
        'func': [GrammarProductions.funcDef],
        '+': [GrammarProductions.Expr],
        '-': [GrammarProductions.Expr],
        '(': [GrammarProductions.Expr],
        TokenTypes.NUMBER.name: [GrammarProductions.Expr],
        TokenTypes.STRING.name: [GrammarProductions.Expr],
        TokenTypes.ID.name: [GrammarProductions.Expr],
        'call': [GrammarProductions.Expr],
        'assign': [GrammarProductions.assign],
        'if': [GrammarProductions.Conditional]
    },
    GrammarProductions.funcDef: {
        'func': ['func', TokenTypes.ID.name, '(', GrammarProductions.Params, ')', '{', GrammarProductions.funcBody, '}']
    },
    GrammarProductions.funcBody: {
        '+': [GrammarProductions.funcEntry, GrammarProductions.funcBody],
        '-': [GrammarProductions.funcEntry, GrammarProductions.funcBody],
        '(': [GrammarProductions.funcEntry, GrammarProductions.funcBody],
        TokenTypes.NUMBER.name: [GrammarProductions.funcEntry, GrammarProductions.funcBody],
        TokenTypes.STRING.name: [GrammarProductions.funcEntry, GrammarProductions.funcBody],
        TokenTypes.ID.name: [GrammarProductions.funcEntry, GrammarProductions.funcBody],
        'call': [GrammarProductions.funcEntry, GrammarProductions.funcBody],
        'func': [GrammarProductions.funcEntry, GrammarProductions.funcBody],
        'return': [GrammarProductions.funcEntry, GrammarProductions.funcBody],
        'if': [GrammarProductions.funcEntry, GrammarProductions.funcBody],
        'assign': [GrammarProductions.funcEntry, GrammarProductions.funcBody],
        '}': []
    },
    GrammarProductions.funcEntry: {
        '+': [GrammarProductions.Expr],
        '-': [GrammarProductions.Expr],
        '(': [GrammarProductions.Expr],
        TokenTypes.NUMBER.name: [GrammarProductions.Expr],
        TokenTypes.STRING.name: [GrammarProductions.Expr],
        TokenTypes.ID.name: [GrammarProductions.Expr],
        'call': [GrammarProductions.Expr],
        'func': [GrammarProductions.funcDef],
        'return': ['return', GrammarProductions.Expr],
        'assign': [GrammarProductions.assign],
        'if': [GrammarProductions.Conditional]
    },
        GrammarProductions.Params: {
        TokenTypes.ID.name: [GrammarProductions.ParamList, GrammarProductions.KeyWordParamListTail],
        'assign': [GrammarProductions.KeyWordParamList],
        ')': []
    },
    GrammarProductions.ParamList: {
        TokenTypes.ID.name: [GrammarProductions.Param, GrammarProductions.ParamListRest]
    },
    GrammarProductions.ParamListRest: {
        ',': [',', GrammarProductions.Param, GrammarProductions.ParamListRest],
        '|': [],
        ')': []
    },
    GrammarProductions.KeyWordParamListTail: {
        '|': ['|', GrammarProductions.KeyWordParam, GrammarProductions.KeyWordParamListTailRest],
        ')': []
    },
    GrammarProductions.KeyWordParamListTailRest: {
        ',': [',', GrammarProductions.KeyWordParam, GrammarProductions.KeyWordParamListTailRest],
        ')': []
    },
    GrammarProductions.KeyWordParamList: {
        'assign': [GrammarProductions.KeyWordParam, GrammarProductions.KeyWordParamListRest]
    },
    GrammarProductions.KeyWordParamListRest: {
        ',': [',', GrammarProductions.KeyWordParam, GrammarProductions.KeyWordParamListRest],
        ')': []
    },
    GrammarProductions.Param: {
        TokenTypes.ID.name: [TokenTypes.ID.name]
    },
    GrammarProductions.KeyWordParam: {
        'assign': [GrammarProductions.assign]
    },
    GrammarProductions.assign: {
        'assign': ['assign', TokenTypes.ID.name, '=', GrammarProductions.Expr]
    },
    GrammarProductions.Expr: {
        '+': [GrammarProductions.Term, GrammarProductions.ExprRest],
        '-': [GrammarProductions.Term, GrammarProductions.ExprRest],
        '(': [GrammarProductions.Term, GrammarProductions.ExprRest],
        TokenTypes.NUMBER.name: [GrammarProductions.Term, GrammarProductions.ExprRest],
        TokenTypes.STRING.name: [GrammarProductions.Term, GrammarProductions.ExprRest],
        TokenTypes.ID.name: [GrammarProductions.Term, GrammarProductions.ExprRest],
        'call': [GrammarProductions.Term, GrammarProductions.ExprRest]
    },
    GrammarProductions.ExprRest: {
        '+': ['+', GrammarProductions.Term, GrammarProductions.ExprRest],
        '-': ['-', GrammarProductions.Term, GrammarProductions.ExprRest],
        # ε-production: all follow set except '+' and '-' to remove ll(1) conflict
        '(': [],
        TokenTypes.NUMBER.name: [],
        TokenTypes.STRING.name: [],
        TokenTypes.ID.name: [],
        'call': [],
        'assign': [],
        'if': [],
        '$': [],
        'func': [],
        'return': [],
        '}': [],
        ',': [],
        ')': [],
        'gt': [],
        'lt': [],
        'ge': [],
        'le': [],
        'eq': [],
        'ne': [],
        '{': [],
        '|': []
    },
    GrammarProductions.Term: {
        '+': [GrammarProductions.Factor, GrammarProductions.TermRest],
        '-': [GrammarProductions.Factor, GrammarProductions.TermRest],
        '(': [GrammarProductions.Factor, GrammarProductions.TermRest],
        TokenTypes.NUMBER.name: [GrammarProductions.Factor, GrammarProductions.TermRest],
        TokenTypes.STRING.name: [GrammarProductions.Factor, GrammarProductions.TermRest],
        TokenTypes.ID.name: [GrammarProductions.Factor, GrammarProductions.TermRest],
        'call': [GrammarProductions.Factor, GrammarProductions.TermRest]
    },
    #I think these can be optimised by substituting * and / in directly for GP.MultOp
    GrammarProductions.TermRest: {
        '*': [GrammarProductions.MultOp, GrammarProductions.Factor, GrammarProductions.TermRest],
        '/': [GrammarProductions.MultOp, GrammarProductions.Factor, GrammarProductions.TermRest],
        '+': [],
        '-': [],
        '(': [],
        TokenTypes.NUMBER.name: [],
        TokenTypes.STRING.name: [],
        TokenTypes.ID.name: [],
        'call': [],
        'assign': [],
        'if': [],
        '$': [],
        'func': [],
        'return': [],
        '}': [],
        ',': [],
        ')': [],
        'gt': [],
        'lt': [],
        'ge': [],
        'le': [],
        'eq': [],
        'ne': [],
        '{': [],
        '|': []
    },
    GrammarProductions.Factor: {
        '+': [GrammarProductions.UnaryOp, GrammarProductions.Factor],
        '-': [GrammarProductions.UnaryOp, GrammarProductions.Factor],
        '(': ['(', GrammarProductions.Expr, ')'],
        TokenTypes.NUMBER.name: [GrammarProductions.Atom],
        TokenTypes.STRING.name: [GrammarProductions.Atom],
        TokenTypes.ID.name: [GrammarProductions.Atom],
        'call': [GrammarProductions.Atom]
    },
    GrammarProductions.UnaryOp: {
        '+': ['+'],
        '-': ['-']
    },
    GrammarProductions.AddOp: {
        '+': ['+'],
        '-': ['-']
    },
    GrammarProductions.MultOp: {
        '*': ['*'],
        '/': ['/']
    },
    GrammarProductions.Atom: {
        TokenTypes.NUMBER.name: [TokenTypes.NUMBER.name],
        TokenTypes.STRING.name: [TokenTypes.STRING.name],
        TokenTypes.ID.name: [TokenTypes.ID.name],
        'call': [GrammarProductions.call]
    },
    GrammarProductions.Conditional: {
        'if': ['if', GrammarProductions.Comparsion, '{', GrammarProductions.ConditionalBody, '}', GrammarProductions.ConditionalRest]
    },
    GrammarProductions.ConditionalRest: {
        'else': ['else', '{', GrammarProductions.ConditionalBody, '}'],
        '+': [], 
        '-': [], 
        '(': [], 
        TokenTypes.NUMBER.name: [], 
        TokenTypes.STRING.name: [], 
        TokenTypes.ID.name: [], 
        'call': [],
        'assign': [], 
        'if': [], 
        '$': [], 
        'func': [], 
        'return': [], 
        '}': []
    },
    GrammarProductions.Comparsion: {
        '+': [GrammarProductions.Expr, GrammarProductions.ComparisonTail],
        '-': [GrammarProductions.Expr, GrammarProductions.ComparisonTail],
        '(': [GrammarProductions.Expr, GrammarProductions.ComparisonTail],
        TokenTypes.NUMBER.name: [GrammarProductions.Expr, GrammarProductions.ComparisonTail],
        TokenTypes.STRING.name: [GrammarProductions.Expr, GrammarProductions.ComparisonTail],
        TokenTypes.ID.name: [GrammarProductions.Expr, GrammarProductions.ComparisonTail],
        'call': [GrammarProductions.Expr, GrammarProductions.ComparisonTail],
        'true': [GrammarProductions.Bool],
        'false': [GrammarProductions.Bool]
    },
    #is this opt correct?
    GrammarProductions.ComparisonTail: {
        'gt': ['gt', GrammarProductions.Expr, GrammarProductions.ComparisonTail],
        'lt': ['lt', GrammarProductions.Expr, GrammarProductions.ComparisonTail],
        'ge': ['ge', GrammarProductions.Expr, GrammarProductions.ComparisonTail],
        'le': ['le', GrammarProductions.Expr, GrammarProductions.ComparisonTail],
        'eq': ['eq', GrammarProductions.Expr, GrammarProductions.ComparisonTail],
        'ne': ['ne', GrammarProductions.Expr, GrammarProductions.ComparisonTail],
        '{': []
    },
    GrammarProductions.CompOp: {
        'gt': ['gt'],
        'lt': ['lt'],
        'ge': ['ge'],
        'le': ['le'],
        'eq': ['eq'],
        'ne': ['ne']
    },
    GrammarProductions.Bool: {
        'true': ['true'],
        'false': ['false']
    },
    GrammarProductions.ConditionalBody: {
        '+': [GrammarProductions.Conditionalentry, GrammarProductions.ConditionalBody],
        '-': [GrammarProductions.Conditionalentry, GrammarProductions.ConditionalBody],
        '(': [GrammarProductions.Conditionalentry, GrammarProductions.ConditionalBody],
        TokenTypes.NUMBER.name: [GrammarProductions.Conditionalentry, GrammarProductions.ConditionalBody],
        TokenTypes.STRING.name: [GrammarProductions.Conditionalentry, GrammarProductions.ConditionalBody],
        TokenTypes.ID.name: [GrammarProductions.Conditionalentry, GrammarProductions.ConditionalBody],
        'call': [GrammarProductions.Conditionalentry, GrammarProductions.ConditionalBody],
        'assign': [GrammarProductions.Conditionalentry, GrammarProductions.ConditionalBody],
        '}': []
    },
    GrammarProductions.Conditionalentry: {
        '+': [GrammarProductions.Expr],
        '-': [GrammarProductions.Expr],
        '(': [GrammarProductions.Expr],
        TokenTypes.NUMBER.name: [GrammarProductions.Expr],
        TokenTypes.STRING.name: [GrammarProductions.Expr],
        TokenTypes.ID.name: [GrammarProductions.Expr],
        'call': [GrammarProductions.Expr],
        'assign': [GrammarProductions.assign]
    },
        GrammarProductions.call: {
        'call': ['call', TokenTypes.ID.name, '(', GrammarProductions.Args, ')']
    },
    GrammarProductions.Args: {
        '+': [GrammarProductions.ArgList, GrammarProductions.KeyWordArgListTail],
        '-': [GrammarProductions.ArgList, GrammarProductions.KeyWordArgListTail],
        '(': [GrammarProductions.ArgList, GrammarProductions.KeyWordArgListTail],
        TokenTypes.NUMBER.name: [GrammarProductions.ArgList, GrammarProductions.KeyWordArgListTail],
        TokenTypes.STRING.name: [GrammarProductions.ArgList, GrammarProductions.KeyWordArgListTail],
        TokenTypes.ID.name: [GrammarProductions.ArgList, GrammarProductions.KeyWordArgListTail],
        'call': [GrammarProductions.ArgList, GrammarProductions.KeyWordArgListTail],
        'assign': [GrammarProductions.KeyWordArgList],
        ')': []
    },
    GrammarProductions.ArgList: {
        '+': [GrammarProductions.Arg, GrammarProductions.ArgListRest],
        '-': [GrammarProductions.Arg, GrammarProductions.ArgListRest],
        '(': [GrammarProductions.Arg, GrammarProductions.ArgListRest],
        TokenTypes.NUMBER.name: [GrammarProductions.Arg, GrammarProductions.ArgListRest],
        TokenTypes.STRING.name: [GrammarProductions.Arg, GrammarProductions.ArgListRest],
        TokenTypes.ID.name: [GrammarProductions.Arg, GrammarProductions.ArgListRest],
        'call': [GrammarProductions.Arg, GrammarProductions.ArgListRest]
    },
    GrammarProductions.ArgListRest: {
        ',': [',', GrammarProductions.Arg, GrammarProductions.ArgListRest],
        '|': [],
        ')': []
    },
    GrammarProductions.KeyWordArgListTail: {
        '|': ['|', GrammarProductions.KeyWordArg, GrammarProductions.KeyWordArgListTailRest],
        ')': []
    },
    GrammarProductions.KeyWordArgListTailRest: {
        ',': [',', GrammarProductions.KeyWordArg, GrammarProductions.KeyWordArgListTailRest],
        ')': []
    },
    GrammarProductions.KeyWordArgList: {
        'assign': [GrammarProductions.KeyWordArg, GrammarProductions.KeyWordArgListRest]
    },
    GrammarProductions.KeyWordArgListRest: {
        ',': [',', GrammarProductions.KeyWordArg, GrammarProductions.KeyWordArgListRest],
        ')': []
    },
    GrammarProductions.Arg: {
        '+': [GrammarProductions.Expr],
        '-': [GrammarProductions.Expr],
        '(': [GrammarProductions.Expr],
        TokenTypes.NUMBER.name: [GrammarProductions.Expr],
        TokenTypes.STRING.name: [GrammarProductions.Expr],
        TokenTypes.ID.name: [GrammarProductions.Expr],
        'call': [GrammarProductions.Expr]
    },
    GrammarProductions.KeyWordArg: {
        'assign': [GrammarProductions.assign]
    }
}