from compiler.lexer.token_utils import TokenTypes
from compiler.parser.parser_utils import GrammarProductions, ListInitMarker, NonTerminalMarkers, TerminalMarkers, OpMarkers, BuildMarkers

#tokens that were distinguised in create_token have been entered as raw strings. This is error prone and support to add new tokens to TokenTypes post lexing is needed.
parse_table = {
    GrammarProductions.P: {
        'func': [ListInitMarker.ListInit, GrammarProductions.StmtList, NonTerminalMarkers.P],
        '+': [ListInitMarker.ListInit, GrammarProductions.StmtList, NonTerminalMarkers.P],
        '-': [ListInitMarker.ListInit, GrammarProductions.StmtList, NonTerminalMarkers.P],
        '(': [ListInitMarker.ListInit, GrammarProductions.StmtList, NonTerminalMarkers.P],
        TokenTypes.NUMBER.name: [ListInitMarker.ListInit, GrammarProductions.StmtList, NonTerminalMarkers.P],
        TokenTypes.STRING.name: [ListInitMarker.ListInit, GrammarProductions.StmtList, NonTerminalMarkers.P],
        TokenTypes.ID.name: [ListInitMarker.ListInit, GrammarProductions.StmtList, NonTerminalMarkers.P],
        'call': [ListInitMarker.ListInit, GrammarProductions.StmtList, NonTerminalMarkers.P],
        'assign': [ListInitMarker.ListInit, GrammarProductions.StmtList, NonTerminalMarkers.P],
        'if': [ListInitMarker.ListInit, GrammarProductions.StmtList, NonTerminalMarkers.P],
        '$': [ListInitMarker.ListInit, GrammarProductions.StmtList, NonTerminalMarkers.P]
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
        'func': [GrammarProductions.FuncDef],
        '+': [GrammarProductions.Expr],
        '-': [GrammarProductions.Expr],
        '(': [GrammarProductions.Expr],
        TokenTypes.NUMBER.name: [GrammarProductions.Expr],
        TokenTypes.STRING.name: [GrammarProductions.Expr],
        TokenTypes.ID.name: [GrammarProductions.Expr],
        'call': [GrammarProductions.Expr],
        'assign': [GrammarProductions.Assign],
        'if': [GrammarProductions.Conditional]
    },
    GrammarProductions.FuncDef: {
        'func': [ListInitMarker.ListInit, 'func', TerminalMarkers.DeclID, TokenTypes.ID.name, '(', GrammarProductions.Params, ')', '{', GrammarProductions.FuncBody, '}', NonTerminalMarkers.FuncDef]
    },
    GrammarProductions.FuncBody: {
        '+': [ListInitMarker.ListInit, GrammarProductions.FuncEntry, GrammarProductions.FuncBody, NonTerminalMarkers.FuncBody],
        '-': [ListInitMarker.ListInit, GrammarProductions.FuncEntry, GrammarProductions.FuncBody, NonTerminalMarkers.FuncBody],
        '(': [ListInitMarker.ListInit, GrammarProductions.FuncEntry, GrammarProductions.FuncBody, NonTerminalMarkers.FuncBody],
        TokenTypes.NUMBER.name: [ListInitMarker.ListInit, GrammarProductions.FuncEntry, GrammarProductions.FuncBody, NonTerminalMarkers.FuncBody],
        TokenTypes.STRING.name: [ListInitMarker.ListInit, GrammarProductions.FuncEntry, GrammarProductions.FuncBody, NonTerminalMarkers.FuncBody],
        TokenTypes.ID.name: [ListInitMarker.ListInit, GrammarProductions.FuncEntry, GrammarProductions.FuncBody, NonTerminalMarkers.FuncBody],
        'call': [ListInitMarker.ListInit, GrammarProductions.FuncEntry, GrammarProductions.FuncBody, NonTerminalMarkers.FuncBody],
        'func': [ListInitMarker.ListInit, GrammarProductions.FuncEntry, GrammarProductions.FuncBody, NonTerminalMarkers.FuncBody],
        'return': [ListInitMarker.ListInit, GrammarProductions.FuncEntry, GrammarProductions.FuncBody, NonTerminalMarkers.FuncBody],
        'if': [ListInitMarker.ListInit, GrammarProductions.FuncEntry, GrammarProductions.FuncBody, NonTerminalMarkers.FuncBody],
        'assign': [ListInitMarker.ListInit, GrammarProductions.FuncEntry, GrammarProductions.FuncBody, NonTerminalMarkers.FuncBody],
        '}': []
    },
    GrammarProductions.FuncEntry: {
        '+': [GrammarProductions.Expr],
        '-': [GrammarProductions.Expr],
        '(': [GrammarProductions.Expr],
        TokenTypes.NUMBER.name: [GrammarProductions.Expr],
        TokenTypes.STRING.name: [GrammarProductions.Expr],
        TokenTypes.ID.name: [GrammarProductions.Expr],
        'call': [GrammarProductions.Expr],
        'func': [GrammarProductions.FuncDef],
        'return': [ListInitMarker.ListInit, 'return', GrammarProductions.Expr, NonTerminalMarkers.Return],
        'assign': [GrammarProductions.Assign],
        'if': [GrammarProductions.Conditional]
    },
        GrammarProductions.Params: {
        TokenTypes.ID.name: [ListInitMarker.ListInit, GrammarProductions.ParamList, GrammarProductions.KeyWordParamListTail, NonTerminalMarkers.Params],
        'assign': [ListInitMarker.ListInit, GrammarProductions.KeyWordParamList, NonTerminalMarkers.Params],
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
        '|': [ '|', GrammarProductions.KeyWordParam, GrammarProductions.KeyWordParamListTailRest],
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
        TokenTypes.ID.name: [ListInitMarker.ListInit, TerminalMarkers.DeclID, TokenTypes.ID.name, NonTerminalMarkers.Param]
    },
    GrammarProductions.KeyWordParam: {
        'assign': [ListInitMarker.ListInit, GrammarProductions.Assign, NonTerminalMarkers.KeyWordParam]
    },
    GrammarProductions.Assign: {
        'assign': [ListInitMarker.ListInit, 'assign', TerminalMarkers.DeclID, TokenTypes.ID.name, '=', GrammarProductions.Expr, NonTerminalMarkers.Assign]
    },
    GrammarProductions.Expr: {
        '+': [ListInitMarker.ListInit, GrammarProductions.Term, GrammarProductions.ExprRest, NonTerminalMarkers.Expr],
        '-': [ListInitMarker.ListInit, GrammarProductions.Term, GrammarProductions.ExprRest, NonTerminalMarkers.Expr],
        '(': [ListInitMarker.ListInit, GrammarProductions.Term, GrammarProductions.ExprRest, NonTerminalMarkers.Expr],
        TokenTypes.NUMBER.name: [ListInitMarker.ListInit, GrammarProductions.Term, GrammarProductions.ExprRest, NonTerminalMarkers.Expr],
        TokenTypes.STRING.name: [ListInitMarker.ListInit, GrammarProductions.Term, GrammarProductions.ExprRest, NonTerminalMarkers.Expr],
        TokenTypes.ID.name: [ListInitMarker.ListInit, GrammarProductions.Term, GrammarProductions.ExprRest, NonTerminalMarkers.Expr],
        'call': [ListInitMarker.ListInit, GrammarProductions.Term, GrammarProductions.ExprRest, NonTerminalMarkers.Expr]
    },
    GrammarProductions.ExprRest: {
        '+': [GrammarProductions.AddOp, GrammarProductions.Term, BuildMarkers.BinOp, GrammarProductions.ExprRest],
        '-': [GrammarProductions.AddOp, GrammarProductions.Term, BuildMarkers.BinOp, GrammarProductions.ExprRest],
        #all follow set except '+' and '-' to remove ll(1) conflict
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
        '+': [ListInitMarker.ListInit, GrammarProductions.Factor, GrammarProductions.TermRest, NonTerminalMarkers.Term],
        '-': [ListInitMarker.ListInit, GrammarProductions.Factor, GrammarProductions.TermRest, NonTerminalMarkers.Term],
        '(': [ListInitMarker.ListInit, GrammarProductions.Factor, GrammarProductions.TermRest, NonTerminalMarkers.Term],
        TokenTypes.NUMBER.name: [ListInitMarker.ListInit, GrammarProductions.Factor, GrammarProductions.TermRest, NonTerminalMarkers.Term],
        TokenTypes.STRING.name: [ListInitMarker.ListInit, GrammarProductions.Factor, GrammarProductions.TermRest, NonTerminalMarkers.Term],
        TokenTypes.ID.name: [ListInitMarker.ListInit, GrammarProductions.Factor, GrammarProductions.TermRest, NonTerminalMarkers.Term],
        'call': [ListInitMarker.ListInit, GrammarProductions.Factor, GrammarProductions.TermRest, NonTerminalMarkers.Term]
    },
    GrammarProductions.TermRest: {
        '*': [GrammarProductions.MultOp, GrammarProductions.Factor, BuildMarkers.BinOp, GrammarProductions.TermRest],
        '/': [GrammarProductions.MultOp, GrammarProductions.Factor, BuildMarkers.BinOp, GrammarProductions.TermRest],
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
        '+': [ListInitMarker.ListInit, GrammarProductions.UnaryOp, GrammarProductions.Factor, NonTerminalMarkers.UnaryOp],
        '-': [ListInitMarker.ListInit, GrammarProductions.UnaryOp, GrammarProductions.Factor, NonTerminalMarkers.UnaryOp],
        '(': ['(', GrammarProductions.Expr, ')'],
        TokenTypes.NUMBER.name: [GrammarProductions.Atom],
        TokenTypes.STRING.name: [GrammarProductions.Atom],
        TokenTypes.ID.name: [GrammarProductions.Atom],
        'call': [GrammarProductions.Atom]
    },
    GrammarProductions.UnaryOp: {
        '+': [OpMarkers.Unary, '+'],
        '-': [OpMarkers.Unary, '-']
    },
    GrammarProductions.AddOp: {
        '+': [OpMarkers.AddOp, '+'],
        '-': [OpMarkers.AddOp, '-']
    },
    GrammarProductions.MultOp: {
        '*': [OpMarkers.MultOp, '*'],
        '/': [OpMarkers.AddOp, '/']
    },
    GrammarProductions.Atom: {
        TokenTypes.NUMBER.name: [TerminalMarkers.NUMBER, TokenTypes.NUMBER.name],
        TokenTypes.STRING.name: [TerminalMarkers.STRING, TokenTypes.STRING.name],
        TokenTypes.ID.name: [TerminalMarkers.ExprID, TokenTypes.ID.name],
        'call': [GrammarProductions.Call]
    },
    GrammarProductions.Conditional: {
        'if': [ListInitMarker.ListInit, 'if', GrammarProductions.Comparsion, '{', GrammarProductions.ConditionalBody, '}', GrammarProductions.ConditionalRest, NonTerminalMarkers.Conditional]
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
        '+': [ListInitMarker.ListInit, GrammarProductions.Expr, GrammarProductions.ComparisonTail, NonTerminalMarkers.Comparison],
        '-': [ListInitMarker.ListInit, GrammarProductions.Expr, GrammarProductions.ComparisonTail, NonTerminalMarkers.Comparison],
        '(': [ListInitMarker.ListInit, GrammarProductions.Expr, GrammarProductions.ComparisonTail, NonTerminalMarkers.Comparison],
        TokenTypes.NUMBER.name: [ListInitMarker.ListInit, GrammarProductions.Expr, GrammarProductions.ComparisonTail, NonTerminalMarkers.Comparison],
        TokenTypes.STRING.name: [ListInitMarker.ListInit, GrammarProductions.Expr, GrammarProductions.ComparisonTail, NonTerminalMarkers.Comparison],
        TokenTypes.ID.name: [ListInitMarker.ListInit, GrammarProductions.Expr, GrammarProductions.ComparisonTail, NonTerminalMarkers.Comparison],
        'call': [ListInitMarker.ListInit, GrammarProductions.Expr, GrammarProductions.ComparisonTail, NonTerminalMarkers.Comparison],
        'true': [GrammarProductions.Bool],
        'false': [GrammarProductions.Bool]
    },
    GrammarProductions.ComparisonTail: {
        'gt': [GrammarProductions.CompOp, GrammarProductions.Expr, GrammarProductions.ComparisonTail],
        'lt': [GrammarProductions.CompOp, GrammarProductions.Expr, GrammarProductions.ComparisonTail],
        'ge': [GrammarProductions.CompOp, GrammarProductions.Expr, GrammarProductions.ComparisonTail],
        'le': [GrammarProductions.CompOp, GrammarProductions.Expr, GrammarProductions.ComparisonTail],
        'eq': [GrammarProductions.CompOp, GrammarProductions.Expr, GrammarProductions.ComparisonTail],
        'ne': [GrammarProductions.CompOp, GrammarProductions.Expr, GrammarProductions.ComparisonTail],
        '{': []
    },
    GrammarProductions.CompOp: {
        'gt': [OpMarkers.CompOp, 'gt'],
        'lt': [OpMarkers.CompOp, 'lt'],
        'ge': [OpMarkers.CompOp, 'ge'],
        'le': [OpMarkers.CompOp, 'le'],
        'eq': [OpMarkers.CompOp, 'eq'],
        'ne': [OpMarkers.CompOp, 'ne']
    },
    GrammarProductions.Bool: {
        'true': [TerminalMarkers.Bool, 'true'],
        'false': [TerminalMarkers.Bool, 'false']
    },
    GrammarProductions.ConditionalBody: {
        '+': [ListInitMarker.ListInit, GrammarProductions.Conditionalentry, GrammarProductions.ConditionalBody, NonTerminalMarkers.ConditionalBody],
        '-': [ListInitMarker.ListInit, GrammarProductions.Conditionalentry, GrammarProductions.ConditionalBody, NonTerminalMarkers.ConditionalBody],
        '(': [ListInitMarker.ListInit, GrammarProductions.Conditionalentry, GrammarProductions.ConditionalBody, NonTerminalMarkers.ConditionalBody],
        TokenTypes.NUMBER.name: [ListInitMarker.ListInit, GrammarProductions.Conditionalentry, GrammarProductions.ConditionalBody, NonTerminalMarkers.ConditionalBody],
        TokenTypes.STRING.name: [ListInitMarker.ListInit, GrammarProductions.Conditionalentry, GrammarProductions.ConditionalBody, NonTerminalMarkers.ConditionalBody],
        TokenTypes.ID.name: [ListInitMarker.ListInit, GrammarProductions.Conditionalentry, GrammarProductions.ConditionalBody, NonTerminalMarkers.ConditionalBody],
        'call': [ListInitMarker.ListInit, GrammarProductions.Conditionalentry, GrammarProductions.ConditionalBody, NonTerminalMarkers.ConditionalBody],
        'assign': [ListInitMarker.ListInit, GrammarProductions.Conditionalentry, GrammarProductions.ConditionalBody, NonTerminalMarkers.ConditionalBody],
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
        'assign': [GrammarProductions.Assign]
    },
        GrammarProductions.Call: {
        'call': [ListInitMarker.ListInit, 'call', TerminalMarkers.ExprID, TokenTypes.ID.name, '(', GrammarProductions.Args, ')', NonTerminalMarkers.Call]
    },
    GrammarProductions.Args: {
        '+': [ListInitMarker.ListInit, GrammarProductions.ArgList, GrammarProductions.KeyWordArgListTail, NonTerminalMarkers.Args],
        '-': [ListInitMarker.ListInit, GrammarProductions.ArgList, GrammarProductions.KeyWordArgListTail, NonTerminalMarkers.Args],
        '(': [ListInitMarker.ListInit, GrammarProductions.ArgList, GrammarProductions.KeyWordArgListTail, NonTerminalMarkers.Args],
        TokenTypes.NUMBER.name: [ListInitMarker.ListInit, GrammarProductions.ArgList, GrammarProductions.KeyWordArgListTail, NonTerminalMarkers.Args],
        TokenTypes.STRING.name: [ListInitMarker.ListInit, GrammarProductions.ArgList, GrammarProductions.KeyWordArgListTail, NonTerminalMarkers.Args],
        TokenTypes.ID.name: [ListInitMarker.ListInit, GrammarProductions.ArgList, GrammarProductions.KeyWordArgListTail, NonTerminalMarkers.Args],
        'call': [ListInitMarker.ListInit, GrammarProductions.ArgList, GrammarProductions.KeyWordArgListTail, NonTerminalMarkers.Args],
        'assign': [ListInitMarker.ListInit, GrammarProductions.KeyWordArgList, NonTerminalMarkers.Args],
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
        '+': [ListInitMarker.ListInit, GrammarProductions.Expr, NonTerminalMarkers.Arg],
        '-': [ListInitMarker.ListInit, GrammarProductions.Expr, NonTerminalMarkers.Arg],
        '(': [ListInitMarker.ListInit, GrammarProductions.Expr, NonTerminalMarkers.Arg],
        TokenTypes.NUMBER.name: [ListInitMarker.ListInit, GrammarProductions.Expr, NonTerminalMarkers.Arg],
        TokenTypes.STRING.name: [ListInitMarker.ListInit, GrammarProductions.Expr, NonTerminalMarkers.Arg],
        TokenTypes.ID.name: [ListInitMarker.ListInit, GrammarProductions.Expr, NonTerminalMarkers.Arg],
        'call': [ListInitMarker.ListInit, GrammarProductions.Expr, NonTerminalMarkers.Arg]
    },
    GrammarProductions.KeyWordArg: {
        'assign': [ListInitMarker.ListInit, GrammarProductions.Assign, NonTerminalMarkers.KeyWordArg]
    }
}