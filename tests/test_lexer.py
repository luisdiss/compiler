import unittest
from compiler.lexer.lexer  import lexer, LexerError
from compiler.lexer.token_utils import TokenTypes, keywords
from compiler.lexer.raw_state_table import transiton_classes, CharClasses

#tests
class TestLexer(unittest.TestCase):

    def test_empty_input(self):
        tokens = lexer("")
        self.assertEqual(tokens, [])
    
    def test_whitespace_only(self):
        tokens = lexer("   \t\n\r  ")
        self.assertEqual(tokens, [])
    
    def test_single_identifier(self):
        tokens = lexer("variable")
        expected = [(TokenTypes.ID.name, "variable")]
        self.assertEqual(tokens, expected)
    
    def test_identifier_with_underscore(self):
        tokens = lexer("_private_var")
        expected = [(TokenTypes.ID.name, "_private_var")]
        self.assertEqual(tokens, expected)
    
    def test_identifier_with_numbers(self):
        tokens = lexer("var123")
        expected = [(TokenTypes.ID.name, "var123")]
        self.assertEqual(tokens, expected)
    
    def test_all_keywords(self):
        for keyword in keywords:
            with self.subTest(keyword=keyword):
                tokens = lexer(keyword)
                expected = [(keyword, keyword)]
                self.assertEqual(tokens, expected)
    
    def test_integer_literals(self):
        test_cases = ["0", "1", "123", "999"]
        for num in test_cases:
            with self.subTest(number=num):
                tokens = lexer(num)
                expected = [(TokenTypes.NUMBER.name, num)]
                self.assertEqual(tokens, expected)
    
    def test_float_literals(self):
        test_cases = ["0.0", "1.5", "123.456", "0.999"]
        for num in test_cases:
            with self.subTest(number=num):
                tokens = lexer(num)
                expected = [(TokenTypes.NUMBER.name, num)]
                self.assertEqual(tokens, expected)
    
    def test_string_literals(self):
        test_cases = [
            ('""', '""'),
            ('"hello"', '"hello"'),
            ('"hello world"', '"hello world"'),
            ('"123"', '"123"'),
            ('"!@#$%"', '"!@#$%"')
        ]
        for input_str, expected_content in test_cases:
            with self.subTest(string=input_str):
                tokens = lexer(input_str)
                expected = [(TokenTypes.STRING.name, expected_content)]
                self.assertEqual(tokens, expected)
    
    def test_operators(self):
        operators = transiton_classes.get(CharClasses.op)
        for op in operators:
            with self.subTest(operator=op):
                tokens = lexer(op)
                expected = [(op, op)]
                self.assertEqual(tokens, expected)
    
    def test_punctuation(self):
        punctuation = transiton_classes.get(CharClasses.punctuation)
        for punc in punctuation:
            with self.subTest(punctuation=punc):
                tokens = lexer(punc)
                expected = [(punc, punc)]
                self.assertEqual(tokens, expected)
    
    def test_complex_expression(self):
        source = "if x gt 0 { assign result = x * 2 }"
        tokens = lexer(source)
        expected = [
            ("if", "if"),
            (TokenTypes.ID.name, "x"),
            ("gt", "gt"),
            (TokenTypes.NUMBER.name, "0"),
            ("{", "{"),
            ("assign", "assign"),
            (TokenTypes.ID.name, "result"),
            ("=", "="),
            (TokenTypes.ID.name, "x"),
            ("*", "*"),
            (TokenTypes.NUMBER.name, "2"),
            ("}", "}")
        ]
        self.assertEqual(tokens, expected)
    
    def test_function_definition(self):
        source = 'func calculate(x, y) {return x + y}'
        tokens = lexer(source)
        expected = [
            ("func", "func"),
            (TokenTypes.ID.name, "calculate"),
            ("(", "("),
            (TokenTypes.ID.name, "x"),
            (",", ","),
            (TokenTypes.ID.name, "y"),
            (")", ")"),
            ("{", "{"),
            ("return", "return"),
            (TokenTypes.ID.name, "x"),
            ("+", "+"),
            (TokenTypes.ID.name, "y"),
            ("}", "}")
        ]
        self.assertEqual(tokens, expected)
    
    def test_maximal_munch_identifiers(self):
        tokens = lexer("iffffffff")
        expected = [(TokenTypes.ID.name, "iffffffff")]
        self.assertEqual(tokens, expected)
    
    def test_maximal_munch_numbers(self):
        tokens = lexer("123.456")
        expected = [(TokenTypes.NUMBER.name, "123.456")]
        self.assertEqual(tokens, expected)
    
    def test_adjacent_tokens(self):
        tokens = lexer("x+y")
        expected = [
            (TokenTypes.ID.name, "x"),
            ("+", "+"),
            (TokenTypes.ID.name, "y")
        ]
        self.assertEqual(tokens, expected)
    
    def test_invalid_character_error(self):
        with self.assertRaises(LexerError) as context:
            lexer("invalid@character")
        error = context.exception
        self.assertEqual(error.position, 7)
        self.assertEqual(error.char, "@")
        self.assertIn("Unexpected character", str(error))
    
    def test_mixed_tokens_with_whitespace(self):
        source = "  if   x  ge  42.0  \n\t  { \r\n   assign u = call a()  \n  }"
        tokens = lexer(source)
        expected = [
            ("if", "if"),
            (TokenTypes.ID.name, "x"),
            ("ge", "ge"),
            (TokenTypes.NUMBER.name, "42.0"),
            ("{", "{"),
            ("assign", "assign"),
            (TokenTypes.ID.name, "u"),
            ("=", "="),
            ("call", "call"),
            (TokenTypes.ID.name, "a"),
            ("(", "("),
            (")", ")"),
            ("}", "}")
        ]
        self.assertEqual(tokens, expected)
    
    def test_zero_handling(self):
        test_cases = ["0", "0.0", "0.123"]
        for num in test_cases:
            with self.subTest(number=num):
                tokens = lexer(num)
                expected = [(TokenTypes.NUMBER.name, num)]
                self.assertEqual(tokens, expected)

if __name__ == "__main__": 
    unittest.main()