import re

def tokenize(expression: str) -> list[tuple[str, str]]:
    token_specification = [
        ("NUMBER", r"\d+(\.\d*)?"),
        ("VARIABLE", r"[A-Za-z]+"),
        ("OPERATOR", r"[+\-*/]"),
        ("LPAREN", r"\("),
        ("RPAREN", r"\)"),
        ("SKIP", r"[ \t]"),
        ("MISMATCH", r".")
    ]

    token_regex = '|'.join(f"(?P<{pair[0]}>{pair[1]})" for pair in token_specification)

    tokens = []

    for mo in re.finditer(token_regex, expression):
        kind = mo.lastgroup
        value = mo.group()
        if kind == 'NUMBER':
            tokens.append(('NUMBER', value))
        elif kind == 'VARIABLE':
            tokens.append(('VARIABLE', value))
        elif kind == 'OPERATOR':
            tokens.append(('OPERATOR', value))
        elif kind == 'LPAREN':
            tokens.append(('LPAREN', value))
        elif kind == 'RPAREN':
            tokens.append(('RPAREN', value))
        elif kind == 'SKIP':
            continue
        elif kind == 'MISMATCH':
            raise SyntaxError(f'Unexpected character: {value}')

    return tokens