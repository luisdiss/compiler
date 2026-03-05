"""
Unit tests for the parserr
"""

import unittest
from compiler.parser.parser_utils import NumberNode, StringNode, ExprIDNode, BinaryOpNode, UnaryOpNode, AssignNode, DeclIDNode, ExprNode, ParamNode, KeyWordParamNode, ArgNode, KeyWordArgNode, BoolNode, CallNode, ReturnNode, ArgsNode, ConditionalNode, ComparisonsNode, ComparisonOpNode, FuncDefNode
from compiler.parser.parser import parser

#helpers to create terminal tokens
def NUM(v): return ('NUMBER', v)
def STR(v): return ('STRING', v)
def ID(v): return ('ID', v)
def T(v): return (v, v)

#ast shape assertion
def assert_shape(tc, node, shape):
    cls, attrs, children = shape
    tc.assertIsInstance(node, cls)

    for attr, expected in attrs.items(): 
        tc.assertEqual(getattr(node, attr), expected)

    actual_children = list(node.children_api())
    tc.assertEqual(len(actual_children), len(children))

    for actual, expected_shape in zip(actual_children, children):
        assert_shape(tc, actual, expected_shape)

#tests
class TestParser(unittest.TestCase):

    #atomic programming constructs
    def test_number(self):
        ast = parser([NUM('5'), ('$', '$')])
        assert_shape(self, ast.children[0].entry,
            (NumberNode, {'value':'5'}, []))

    def test_string(self):
        ast = parser([STR('"hi"'), ('$', '$')])
        assert_shape(self, ast.children[0].entry,
            (StringNode, {'value':'"hi"'}, []))

    def test_identifier(self):
        ast = parser([ID('x'), ('$', '$')])
        assert_shape(self, ast.children[0].entry,
            (ExprIDNode, {'value':'x'}, []))

    def test_unary_minus(self):
        ast = parser([T('-'), NUM('1'), ('$', '$')])
        assert_shape(self, ast.children[0].entry,
            (UnaryOpNode, {'op':'-'}, [
                (NumberNode, {'value':'1'}, [])
            ]))

    def test_binary_add(self):
        ast = parser([NUM('1'), T('+'), NUM('2'), ('$', '$')])
        assert_shape(self, ast.children[0].entry,
            (BinaryOpNode, {'op':'+'}, [
                (NumberNode, {'value':'1'}, []),
                (NumberNode, {'value':'2'}, [])
            ]))

    def test_assignment(self):
        ast = parser([T('assign'), ID('x'), T('='), NUM('1'), ('$', '$')])
        assert_shape(self, ast.children[0],
            (AssignNode, {}, [
                (DeclIDNode, {'value':'x'}, []),
                (ExprNode, {}, [
                    (NumberNode, {'value':'1'}, [])
                ])
            ]))

    def test_call_empty(self):
        ast = parser([T('call'), ID('f'), T('('), T(')'), ('$', '$')])
        assert_shape(self, ast.children[0].entry,
            (CallNode, {}, [
                (ExprIDNode, {'value':'f'}, []),
                (ArgsNode, {}, [])
            ]))

    def test_bool_true(self):
        ast = parser([T('if'), T('true'), T('{'), NUM('1'), T('}'), ('$', '$')])
        assert_shape(self, ast.children[0].comparison,
            (BoolNode, {'value':'true'}, []))

    def test_param(self):
        ast = parser([
            T('func'), ID('f'), T('('), 
            ID('a'), 
            T(')'), 
            T('{'), NUM('1'), T('}'), 
            ('$', '$')
        ])
        assert_shape(self, ast.children[0].params.children[0],
            (ParamNode, {'id':ast.children[0].params.children[0].id}, [
                (DeclIDNode, {'value': 'a'}, [])
            ]))

    def test_keyword_param(self):
        ast = parser([
            T('func'), ID('f'), T('('),
            T('assign'), ID('x'), T('='), NUM('1'),
            T(')'), T('{'), NUM('2'), T('}'),
            ('$', '$')
        ])
        assert_shape(self, ast.children[0].params.children[0],
            (KeyWordParamNode, {}, [
                (DeclIDNode, {'value':'x'}, []),
                (ExprNode, {}, [
                    (NumberNode, {'value':'1'}, [])
                ])
            ]))

    def test_arg(self):
        ast = parser([T('call'), ID('f'), T('('), NUM('1'), T(')'), ("$", "$")])
        assert_shape(self, ast.children[0].entry.args.children[0],
            (ArgNode, {}, [
                (ExprNode, {}, [
                    (NumberNode, {'value':'1'}, [])
                ])
            ]))

    def test_keyword_arg(self):
        ast = parser([
            T('call'), ID('f'), T('('),
            T('assign'), ID('x'), T('='), NUM('1'),
            T(')'), 
            ("$", "$")
        ])
        assert_shape(self, ast.children[0].entry.args.children[0],
            (KeyWordArgNode, {}, [
                (DeclIDNode, {'value':'x'}, []),
                (ExprNode, {}, [
                    (NumberNode, {'value':'1'}, [])
                ])
            ]))

    def test_return(self):
        ast = parser([
            T('func'), ID('f'), T('('), T(')'), T('{'),
            T('return'), NUM('1'),
            T('}'),
            ('$', '$')
        ])
        assert_shape(self, ast.children[0].funcbody.children[0],
            (ReturnNode, {}, [
                (ExprNode, {}, [
                    (NumberNode, {'value':'1'}, [])
                ])
            ]))

    def test_conditional(self):
        ast = parser([T('if'), T('true'), T('{'), NUM('1'), T('}'), ('$', '$')])
        self.assertIsInstance(ast.children[0], ConditionalNode)

    def test_comparison(self):
        ast = parser([
            T('if'), NUM('1'), T('gt'), NUM('2'), T('lt'), NUM('3'),
            T('{'), NUM('3'), T('}'),
            ('$', '$')
        ])
        assert_shape(self, ast.children[0].comparison,
            (ComparisonsNode, {}, [
                (ComparisonOpNode, {'op':'gt'}, [
                    (ExprNode, {}, [
                        (NumberNode, {'value':'1'}, []),
                    ]),
                    (ExprNode, {}, [
                        (NumberNode, {'value':'2'}, [])
                    ])
                ]),
                (ComparisonOpNode, {'op':'lt'}, [
                    (ExprNode, {}, [
                        (NumberNode, {'value':'2'}, []),
                    ]),
                    (ExprNode, {}, [
                        (NumberNode, {'value':'3'}, [])
                    ])
                ])
            ]))

    #precedence
    def test_mul_precedence(self):
        ast = parser([NUM('1'), T('+'), NUM('2'), T('*'), NUM('3'), ('$', '$')])
        root = ast.children[0].entry
        self.assertEqual(root.op, '+')
        self.assertEqual(root.right.op, '*')

    def test_parentheses_override(self):
        ast = parser([
            T('('), NUM('1'), T('+'), NUM('2'), T(')'),
            T('*'), NUM('3'),
            ('$', '$')
        ])
        self.assertEqual(ast.children[0].entry.op, '*')

    def test_left_assoc(self):
        ast = parser([NUM('5'), T('-'), NUM('2'), T('-'), NUM('1'), ('$', '$')])
        self.assertEqual(ast.children[0].entry.op, '-')

    def test_unary_precedence(self):
        ast = parser([T('-'), NUM('1'), T('*'), NUM('2'), ('$', '$')])
        self.assertEqual(ast.children[0].entry.op, '*')

    def test_div_precedence(self):
        ast = parser([NUM('8'), T('/'), NUM('2'), T('+'), NUM('1'), ('$', '$')])
        self.assertEqual(ast.children[0].entry.op, '+')

    def test_nested_expr(self):
        ast = parser([
            T('('), NUM('1'), T('+'), NUM('2'), T(')'),
            T('*'),
            T('('), NUM('3'), T('-'), NUM('4'), T(')'),
            ('$', '$')
        ])
        self.assertIsInstance(ast.children[0].entry, BinaryOpNode)

    #empty
    def test_empty_program(self):
        ast = parser([('$', '$')])
        self.assertEqual(len(ast.children), 0)

    def test_empty_params(self):
        ast = parser([T('func'), ID('f'), T('('), T(')'), T('{'), NUM('1'), T('}'), ('$', '$')])
        self.assertEqual(len(ast.children[0].params.children), 0)

    def test_no_else(self):
        ast = parser([T('if'), T('true'), T('{'), NUM('1'), T('}'), ('$', '$')])
        self.assertIsNone(ast.children[0]._else)

    def test_empty_args(self):
        ast = parser([T('call'), ID('f'), T('('), T(')'), ('$', '$')])
        self.assertEqual(len(ast.children[0].entry.args.children), 0)

    def test_empty_conditional_body(self):
        ast = parser([T('if'), T('true'), T('{'), T('}'), ('$', '$')])
        self.assertEqual(ast.children[0]._if, None)

    def test_single_expr(self):
        ast = parser([NUM('1'), ('$', '$')])
        self.assertIsInstance(ast.children[0].entry, NumberNode)

    def test_single_term(self):
        ast = parser([NUM('1'), T('+'), NUM('2'), ('$', '$')])
        self.assertIsInstance(ast.children[0].entry, BinaryOpNode)

    def test_single_comparison_expr(self):
        ast = parser([T('if'), NUM('1'), T('{'), NUM('2'), T('}'), ('$', '$')])
        self.assertIsNotNone(ast.children[0].comparison)

    def test_keyword_param_only(self):
        ast = parser([
            T('func'), ID('f'), T('('),
            T('assign'), ID('x'), T('='), NUM('1'), 
            T(')'), 
            T('{'), NUM('1'), T('}'),
            ('$', '$')
        ])
        self.assertEqual(len(ast.children[0].params.children), 1)

    #composite programming constructs
    def test_call_inside_assign(self):
        ast = parser([
            T('assign'), ID('x'), T('='),
            T('call'), ID('f'), T('('), NUM('1'), T(')'),
            ('$', '$')
        ])
        self.assertIsInstance(ast.children[0].expr.entry, CallNode)

    def test_assign_inside_if(self):
        ast = parser([
            T('if'), T('true'), T('{'),
            T('assign'), ID('x'), T('='), NUM('1'),
            T('}'),
            ('$', '$')
        ])
        self.assertIsInstance(ast.children[0]._if.children[0], AssignNode)

    def test_nested_function(self):
        ast = parser([
            T('func'), ID('outer'), T('('), T(')'), T('{'),
            T('func'), ID('inner'), T('('), T(')'), T('{'), NUM('1'), T('}'),
            T('}'),
            ('$', '$')
        ])
        self.assertIsInstance(ast.children[0].funcbody.children[0], FuncDefNode)

    def test_if_else(self):
        ast = parser([
            T('if'), T('true'), T('{'), NUM('1'), T('}'),
            T('else'), T('{'), NUM('2'), T('}'),
            ('$', '$')
        ])
        self.assertIsNotNone(ast.children[0]._else)

    def test_return_binary(self):
        ast = parser([
            T('func'), ID('f'), T('('), T(')'), T('{'),
            T('return'), NUM('1'), T('+'), NUM('2'),
            T('}'),
            ('$', '$')
        ])
        self.assertIsInstance(
            ast.children[0].funcbody.children[0].expr.entry,
            BinaryOpNode
        )

    def test_complex_program(self):
        ast = parser([
            T('func'), ID('f'), T('('), T(')'), T('{'),
            T('return'), NUM('1'),
            T('}'),
            T('assign'), ID('x'), T('='), NUM('5'),
            ('$', '$')
        ])
        self.assertEqual(len(ast.children), 2)

if __name__ == "__main__":
    unittest.main()