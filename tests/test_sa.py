import unittest
from compiler.parser.parser_utils import PNode, ExprNode, NumberNode, StringNode, ExprIDNode, AssignNode, DeclIDNode, ParamNode, ParamsNode, ArgNode, CallNode, ReturnNode, ArgsNode, FuncDefNode, FuncBodyNode, KeyWordParamNode
from compiler.sa.sa_utils import SA, ScopeDeclVisitor, InferenceVisitor, Types

#run sa
def run_complete_sa(ast):
    sa = SA()
    ScopeDeclVisitor(sa).visit(ast)
    InferenceVisitor(sa).visit(ast)
    return sa

def run_scoping_sa(ast):
    sa = SA()
    ScopeDeclVisitor(sa).visit(ast)
    return sa

#tests
class TestSemanticAnalysis(unittest.TestCase):
    
    #redefinition tests
    def test_variable_redefinition_illegal(self):
        ast = PNode([
            AssignNode(DeclIDNode("x"), NumberNode("1")),
            AssignNode(DeclIDNode("x"), NumberNode("2")),
        ])

        sa = run_scoping_sa(ast)
        scope = sa.node_to_scope[ast.children[0]]

        self.assertEqual(len(scope.symbol_table), 1)

    def test_function_redefinition_illegal(self):
        ast = PNode([
            FuncDefNode(
                id=DeclIDNode("f"),
                params=ParamsNode([]),
                funcbody=FuncBodyNode([])
            ),
            FuncDefNode(
                id=DeclIDNode("f"),
                params=ParamsNode([]),
                funcbody=FuncBodyNode([])
            ),
        ])

        sa = run_scoping_sa(ast)
        scope = sa.node_to_scope[ast.children[0]]

        self.assertEqual(len(scope.symbol_table), 1)

    #lexical scoping
    def test_outer_variable_access(self):
        ast = PNode([
            AssignNode(DeclIDNode("x"), NumberNode("1")),
            FuncDefNode(
                id=DeclIDNode("f"),
                params=ParamsNode([]),
                funcbody=FuncBodyNode([
                    ReturnNode(ExprNode(ExprIDNode("x")))
                ])
            ),
            CallNode(
                id=ExprIDNode("f"),
                args=ArgsNode([])
            )
        ])

        sa = run_complete_sa(ast)
        f_symbol = sa.node_to_scope[ast.children[1]].symbol_table["f"]

        self.assertEqual(f_symbol.type, Types.number)

    def test_shadowing(self):
        ast = PNode([
            AssignNode(DeclIDNode("x"), NumberNode("1")),
            FuncDefNode(
                id=DeclIDNode("f"),
                params=ParamsNode([]),
                funcbody=FuncBodyNode([
                    AssignNode(DeclIDNode("x"), ExprNode(StringNode("a"))),
                    ReturnNode(ExprNode(ExprIDNode("x")))
                ])
            ),
            CallNode(
                id=ExprIDNode("f"),
                args=ArgsNode([])
            )
        ])

        sa = run_complete_sa(ast)
        f_symbol = sa.node_to_scope[ast.children[1]].symbol_table["f"]

        self.assertEqual(f_symbol.type, Types.string)

    def test_undefined_variable(self):
        ast = PNode([
            ExprIDNode("x")
        ])

        sa = run_scoping_sa(ast)

        self.assertNotIn("x", sa.node_to_scope[ast.children[0]].symbol_table)

    #function inference
    def test_uncalled_function_type_none(self):
        ast = PNode([
            FuncDefNode(
                id=DeclIDNode("f"),
                params=ParamsNode([ParamNode(DeclIDNode("x"))]),
                funcbody=FuncBodyNode([
                    ReturnNode(ExprNode(ExprIDNode("x")))
                ])
            )
        ])

        sa = run_complete_sa(ast)
        f_symbol = sa.node_to_scope[ast.children[0]].symbol_table["f"]

        self.assertIsNone(f_symbol.type)

    def test_first_call_infers_param_type(self):
        ast = PNode([
            FuncDefNode(
                id=DeclIDNode("f"),
                params=ParamsNode([ParamNode(DeclIDNode("x"))]),
                funcbody=FuncBodyNode([
                    ReturnNode(ExprNode(ExprIDNode("x")))
                ])
            ),
            CallNode(
                id=ExprIDNode("f"),
                args=ArgsNode([
                    ArgNode(NumberNode("1"))
                ])
            )
        ])

        sa = run_complete_sa(ast)
        f_symbol = sa.node_to_scope[ast.children[0]].symbol_table["f"]
        param = f_symbol.params[0]

        self.assertEqual(param.id.symbol.type, Types.number)

    def test_second_call_type_mismatch(self):
        ast = PNode([
            FuncDefNode(
                id=DeclIDNode("f"),
                params=ParamsNode([ParamNode(DeclIDNode("x"))]),
                funcbody=FuncBodyNode([
                    ReturnNode(ExprNode(ExprIDNode("x")))
                ])
            ),
            CallNode(
                id=ExprIDNode("f"),
                args=ArgsNode([ArgNode(ExprNode(NumberNode("1")))])
            ),
            CallNode(
                id=ExprIDNode("f"),
                args=ArgsNode([ArgNode(ExprNode(StringNode("a")))])
            )
        ])

        sa = run_complete_sa(ast)
        f_symbol = sa.node_to_scope[ast.children[0]].symbol_table["f"]

        self.assertEqual(
            f_symbol.params[0].id.symbol.type,
            Types.number
        )

    #default parameters
    def test_default_parameter_type(self):
        ast = PNode([
            FuncDefNode(
                id=DeclIDNode("f"),
                params=ParamsNode([
                    KeyWordParamNode(
                        DeclIDNode("x"),
                        expr=NumberNode("1"),
                    )
                ]),
                funcbody=FuncBodyNode([
                    ReturnNode(ExprIDNode("x"))
                ])
            ),
            CallNode(
                id=ExprIDNode("f"),
                args=ArgsNode([])
            )
        ])

        sa = run_complete_sa(ast)
        f_symbol = sa.node_to_scope[ast.children[0]].symbol_table["f"]

        self.assertEqual(
            f_symbol.params[0].id.symbol.type,
            Types.number
        )

    # test for raises error when proper error system in place
    # def test_default_mismatch_error(self):
    #     ast = PNode([
    #         FuncDefNode(
    #             id=DeclIDNode("f"),
    #             params=ParamsNode([
    #                 KeyWordParamNode(
    #                     DeclIDNode("x"),
    #                     expr=NumberNode("1"),
    #                 )
    #             ]),
    #             funcbody=FuncBodyNode([
    #                 ReturnNode(ExprNode(ExprIDNode("x")))
    #             ])
    #         ),
    #         CallNode(
    #             id=ExprIDNode("f"),
    #             args=ArgsNode([
    #                 ArgNode(StringNode("a"))
    #             ])
    #         )
    #     ])

    #     sa = run_complete_sa(ast)
    #     f_symbol = sa.node_to_scope[ast.children[0]].symbol_table["f"]

if __name__ == "__main__":
    unittest.main()