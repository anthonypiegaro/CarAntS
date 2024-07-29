from __future__ import annotations
from abc import ABC, abstractmethod

class Node(ABC):
    def __init__(self):
        pass
    
    @abstractmethod
    def evaluate(self, values: dict[str, float]) -> float:
        pass
    
    @abstractmethod
    def differentiate(self, var: str) -> Node:
        pass
    
    @abstractmethod
    def simplify(self) -> Node:
        pass
    
    @abstractmethod
    def __str__(self) -> str:
        pass


class Constant(Node):
    def __init__(self, value: float) -> None:
        self.value = value
    
    def evaluate(self) -> float:
        return self.value
    
    def differentiate(self, var: str) -> Constant:
        return Constant(0)
    
    def simplify(self) -> Constant:
        return self
    
    def __str__(self) -> str:
        return str(self.value)


class Variable(Node):
    def __init__(self, name: str) -> None:
        self.name = name
    
    def evaluate(self, values: dict[str, float]) -> float:
        if self.name in values:
            return values[self.name]
        else:
            raise ValueError(f"Value for variable '{self.name}' not provided")

    def differentiate(self, var: str) -> Constant:
        if var == self.name:
            return Constant(1)
        return Constant(0)
    
    def simplify(self) -> Variable:
        return self
    
    def __str__(self) -> str:
        return self.name


class Add(Node):
    def __init__(self, left: Node, right: Node) -> None:
        self.left = left
        self.right = right
    
    def evaluate(self, values: dict[str, float]) -> float:
        left_value = self.left.evaluate(values)
        right_value = self.right.evaluate(values)
        return left_value + right_value

    def differentiate(self, var: str) -> Add:
        left_derivative = self.left.differentiate(var)
        right_derivative = self.right.differentiate(var)
        return Add(left=left_derivative, right=right_derivative)

    def simplify(self) -> Add | Constant:
        left_simplified = self.left.simplify()
        right_simplified = self.right.simplify()

        if isinstance(left_simplified, Constant) and isinstance(right_simplified, Constant):
            return Constant(left_simplified.evaluate() + right_simplified.evaluate())
        
        if isinstance(left_simplified, Constant) and left_simplified.value == 0:
            return right_simplified
        elif isinstance(right_simplified, Constant) and right_simplified.value == 0:
            return left_simplified

        return Add(left=left_simplified, right=right_simplified)
    
    def __str__(self) -> str:
        return f"({str(self.left)} + {str(self.right)})"


class Multiply(Node):
    def __init__(self, left: Node, right: Node) -> None:
        self.left = left
        self.right = right
    
    def evaluate(self, values: dict[str, float]) -> float:
        left_value = self.left.evaluate(values)
        right_value = self.right.evaluate(values)
        return left_value * right_value
    
    def differentiate(self, var: str) -> Add:
        left_derivative = self.left.differentiate(var)
        right_derivative = self.right.differentiate(var)
        
        left_side = Multiply(left=self.left, right=right_derivative)
        right_side = Multiply(left=left_derivative, right=self.right)
        return Add(left=left_side, right=right_side)
    
    def simplify(self) -> Multiply | Constant:
        left_simplified = self.left.simplify()
        right_simplified = self.right.simplify()

        if isinstance(left_simplified, Constant) and isinstance(right_simplified, Constant):
            return Constant(left_simplified.evaluate() * right_simplified.evaluate())
        
        if isinstance(left_simplified, Constant) and left_simplified.value == 0:
            return Constant(0)
        elif isinstance(right_simplified, Constant) and right_simplified.value == 0:
            return Constant(0)
        elif isinstance(left_simplified, Constant) and left_simplified.value == 1:
            return right_simplified
        elif isinstance(right_simplified, Constant) and right_simplified.value == 1:
            return left_simplified
        
        return Multiply(left=left_simplified, right=right_simplified)

    def __str__(self):
        return f"({str(self.left)} * {str(self.right)})"


class Subtract(Node):
    def __init__(self, left: Node, right: Node) -> None:
        self.left = left
        self.right = right

    def evaluate(self, values: dict[str, float]) -> float:
        left_value = self.left.evaluate(values)
        right_value = self.right.evaluate(values)

        return left_value - right_value
    
    def differentiate(self, var: str) -> Subtract:
        left_derivative = self.left.differentiate(var)
        right_derivative = self.right.differentiate(var)
        return Subtract(left=left_derivative, right=right_derivative)

    def simplify(self) -> Subtract | Constant:
        left_simplified = self.left.simplify()
        right_simplified = self.right.simplify()

        if isinstance(left_simplified, Constant) and isinstance(right_simplified, Constant):
            return Constant(left_simplified.evaluate() - right_simplified.evaluate())
    
        if isinstance(right_simplified, Constant) and right_simplified.value == 0:
            return left_simplified

        return Subtract(left=left_simplified, right=right_simplified)

    def __str__(self) -> str:
        return f"({str(self.left)} - {str(self.right)})"


class Divide(Node):
    def __init__(self, left: Node, right: Node) -> None:
        self.left = left
        self.right = right
    
    def evaluate(self, values: dict[str, float]) -> float:
        left_value = self.left.evaluate(values)
        right_value = self.right.evaluate(values)
        return left_value / right_value

    def differentiate(self, var: str) -> Divide:
        u = self.left
        v = self.right
        u_prime = self.left.differentiate(var)
        v_prime = self.right.differentiate(var)

        numerator = Subtract(left=Multiply(left=u_prime, right=v), right=Multiply(left=u, right=v_prime))
        denominator = Multiply(left=v, right=v)

        return Divide(left=numerator, right=denominator)

    def simplify(self) -> Divide | Constant:
        left_simplified = self.left.simplify()
        right_simplified = self.right.simplify()

        if isinstance(left_simplified, Constant) and isinstance(right_simplified, Constant):
            return Constant(left_simplified / right_simplified)
    
        if isinstance(right_simplified, Constant) and right_simplified.value == 1:
            return left_simplified
    
        return Divide(left=left_simplified, right=right_simplified)

    def __str__(self):
        return f"({str(self.left)} / {str(self.right)})"