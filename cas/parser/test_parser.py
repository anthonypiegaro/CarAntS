import unittest
from .parser import Parser
from tree.tree import Add, Subtract, Multiply, Divide, Constant, Variable

class TestParser(unittest.TestCase):

    def test_parse_expression_addition(self):
        tokens = [("NUMBER", "2"), ("OPERATOR", "+"), ("NUMBER", "3")]
        parser = Parser(tokens)
        result = parser.parse_expression()
        self.assertIsInstance(result, Add)
        self.assertIsInstance(result.left, Constant)
        self.assertIsInstance(result.right, Constant)
        self.assertEqual(result.left.evaluate(), 2)
        self.assertEqual(result.right.evaluate(), 3)

    def test_parse_expression_subtraction(self):
        tokens = [("NUMBER", "5"), ("OPERATOR", "-"), ("NUMBER", "2")]
        parser = Parser(tokens)
        result = parser.parse_expression()
        self.assertIsInstance(result, Subtract)
        self.assertIsInstance(result.left, Constant)
        self.assertIsInstance(result.right, Constant)
        self.assertEqual(result.left.evaluate(), 5)
        self.assertEqual(result.right.evaluate(), 2)

    def test_parse_expression_multiplication(self):
        tokens = [("NUMBER", "3"), ("OPERATOR", "*"), ("NUMBER", "4")]
        parser = Parser(tokens)
        result = parser.parse_expression()
        self.assertIsInstance(result, Multiply)
        self.assertIsInstance(result.left, Constant)
        self.assertIsInstance(result.right, Constant)
        self.assertEqual(result.left.evaluate(), 3)
        self.assertEqual(result.right.evaluate(), 4)

    def test_parse_expression_division(self):
        tokens = [("NUMBER", "10"), ("OPERATOR", "/"), ("NUMBER", "2")]
        parser = Parser(tokens)
        result = parser.parse_expression()
        self.assertIsInstance(result, Divide)
        self.assertIsInstance(result.left, Constant)
        self.assertIsInstance(result.right, Constant)
        self.assertEqual(result.left.evaluate(), 10)
        self.assertEqual(result.right.evaluate(), 2)

    def test_parse_expression_with_parentheses(self):
        tokens = [("LPAREN", "("), ("NUMBER", "3"), ("OPERATOR", "+"), ("NUMBER", "4"), ("RPAREN", ")"), ("OPERATOR", "*"), ("NUMBER", "2")]
        parser = Parser(tokens)
        result = parser.parse_expression()
        self.assertIsInstance(result, Multiply)
        self.assertIsInstance(result.left, Add)
        self.assertIsInstance(result.right, Constant)
        self.assertEqual(result.left.left.evaluate(), 3)
        self.assertEqual(result.left.right.evaluate(), 4)
        self.assertEqual(result.right.evaluate(), 2)

    def test_parse_expression_with_variable(self):
        tokens = [("VARIABLE", "x"), ("OPERATOR", "+"), ("NUMBER", "5")]
        parser = Parser(tokens)
        result = parser.parse_expression()
        self.assertIsInstance(result, Add)
        self.assertIsInstance(result.left, Variable)
        self.assertIsInstance(result.right, Constant)
        self.assertEqual(result.left.evaluate({'x': 2}), 2)
        self.assertEqual(result.right.evaluate(), 5)

    def test_parse_expression_syntax_error(self):
        tokens = [("NUMBER", "2"), ("OPERATOR", "+"), ("OPERATOR", "*")]
        parser = Parser(tokens)
        with self.assertRaises(SyntaxError):
            parser.parse_expression()

if __name__ == '__main__':
    unittest.main()