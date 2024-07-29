from cas import CAS

def main():
    expression = "(2 * x) + 5"

    cas = CAS(expression)

    print("Expression:", expression)
    print("Derivative:", cas.differentiate("x"))

if __name__ == '__main__':
    main()