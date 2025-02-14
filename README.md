# CarAntS
A lightweight Computer Algebra System (CAS) designed for symbolic mathematics. This project provides foundational components for parsing and manipulating mathematical expressions symbolically.

## Usage
You can use the CAS by initializing the class with an expression. You can then call the `differentiate` method to get the derivative of the expression with respect to the passed variable.
```{python}
from cas import CAS

def main():
    expression = "(2 * x) + 5"

    cas = CAS(expression)

    print("Expression:", expression)
    print("Derivative:", cas.differentiate("x"))

if __name__ == '__main__':
    main()
```
## Data Flow

The CAS system processes expressions through the following data flow:

1. **Expression**
   - The starting point is a mathematical expression written in ([infix notation](https://en.wikipedia.org/wiki/Infix_notation)). This is the standard notation for mathematical expressions where operators are placed between operands, such as `(2 * x) + 5`.

2. **Tokenize**
   - The expression is passed to the tokenizer, which converts the mathematical expression into a series of tokens. Tokens are the basic building blocks of the expression, such as numbers, operators, and variables.

3. **Parse**
   - The parser takes the list of tokens generated by the tokenizer and constructs an algebraic expression tree. This tree structure represents the hierarchical nature of the expression, capturing the precedence and associativity of the operators.

4. **Algebraic Expression Tree**
   - The algebraic expression tree is then used for various computations. It allows for the evaluation of the expression with given variable values, the simplification of the expression, and the differentiation of the expression with respect to a given variable. The tree structure enables efficient and accurate manipulation of the mathematical expression.