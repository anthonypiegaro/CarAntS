from cas.tree.tree import Node, Constant, Variable, Add, Multiply, Subtract, Divide

class Parser:
    def __init__(self, tokens: list[tuple[str, str]]) -> None:
        self.tokens = tokens
        self.pos = -1
        self.current_token = None
        self.next_token()
    
    def next_token(self) -> None:
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = None
    
    def parse_expression(self):
        node = self.parse_term()
        while self.current_token is not None and self.current_token[0] == "OPERATOR" and self.current_token[1] in ("+", "-"):
            operator = self.current_token
            self.next_token()
            if operator[1] == "+":
                node = Add(left=node, right=self.parse_term())
            elif operator[1] == "-":
                node = Subtract(left=node, right=self.parse_term())
        return node

    def parse_term(self) -> Node:
        node = self.parse_factor()
        while self.current_token is not None and self.current_token[0] == "OPERATOR" and self.current_token[1] in ("*", "/"):
            operation = self.current_token[1]
            self.next_token()
            if operation == "*":
                node = Multiply(left=node, right=self.parse_factor())
            elif operation == "/":
                node = Divide(left=node, right=self.parse_factor())
        return node

    def parse_factor(self) -> Node:
        token = self.current_token
        if token[0] == "NUMBER":
            self.next_token()
            return Constant(float(token[1]))
        elif token[0] == "VARIABLE":
            self.next_token()
            return Variable(token[1])
        elif token[0] == "LPAREN":
            self.next_token()
            node = self.parse_expression()
            if self.current_token is None or self.current_token[0] != "RPAREN":
                raise SyntaxError("Expected )")
            self.next_token()
            return node
        else:
            raise SyntaxError(f"Unexpected token: {token}")