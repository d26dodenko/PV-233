import sys

def main():
    if len(sys.argv) != 4:
        print("Usage: python3 calculator.py <number> <operator> <number>")
        sys.exit(1)

    try:
        a = float(sys.argv[1])
        operator = sys.argv[2]
        b = float(sys.argv[3])
    except ValueError:
        print("Error: Invalid number")
        sys.exit(1)

    if operator == "+":
        result = a + b
    elif operator == "-":
        result = a - b
    elif operator == "*":
        result = a * b
    elif operator == "/":
        if b == 0:
            print("Error: Division by zero")
            sys.exit(1)
        result = a / b
    else:
        print("Error: Unknown operator")
        sys.exit(1)

    # Убираем .0 у целых чисел
    if result.is_integer():
        result = int(result)

    print(result)


if __name__ == "__main__":
    main()