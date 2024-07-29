from .tokenizer.tokenizer import tokenize
from .parser.parser import Parser

class CAS:
    def __init__(self, expression):
        self.expression = expression
        self.tokens = tokenize(expression)
        self.tree = Parser(self.tokens).parse_expression()
    
    def evaluate(self, values: dict[str, int]) -> str:
        return str(self.tree.evaluate(values))

    def differentiate(self, var: str) -> str:
        return str(self.tree.differentiate(var).simplify())

    def simplify(self) -> str:
        return str(self.tree.simplify())