import unittest
from tokenizer.tokenizer import tokenize

class TestTokenizer(unittest.TestCase):

    def test_simple_expression(self):
        expression = "3 + 5"
        expected_output = [('NUMBER', '3'), ('OPERATOR', '+'), ('NUMBER', '5')]
        self.assertEqual(tokenize(expression), expected_output)

    def test_expression_with_variables(self):
        expression = "x * y + 42"
        expected_output = [('VARIABLE', 'x'), ('OPERATOR', '*'), ('VARIABLE', 'y'), ('OPERATOR', '+'), ('NUMBER', '42')]
        self.assertEqual(tokenize(expression), expected_output)

    def test_expression_with_parentheses(self):
        expression = "(3 + x) * 7"
        expected_output = [('LPAREN', '('), ('NUMBER', '3'), ('OPERATOR', '+'), ('VARIABLE', 'x'), ('RPAREN', ')'), ('OPERATOR', '*'), ('NUMBER', '7')]
        self.assertEqual(tokenize(expression), expected_output)

    def test_expression_with_whitespace(self):
        expression = " 3 +  4 * x "
        expected_output = [('NUMBER', '3'), ('OPERATOR', '+'), ('NUMBER', '4'), ('OPERATOR', '*'), ('VARIABLE', 'x')]
        self.assertEqual(tokenize(expression), expected_output)

    def test_expression_with_invalid_character(self):
        expression = "3 + @"
        with self.assertRaises(SyntaxError):
            tokenize(expression)

if __name__ == '__main__':
    unittest.main()
