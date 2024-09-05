import sys

def report_error(line, message):
    print(f"[line {line}] Error: {message}", file=sys.stderr)

def main():
    print("Logs from your program will appear here!", file=sys.stderr)

    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh tokenize <filename>", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    if command != "tokenize":
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)

    with open(filename) as file:
        file_contents = file.read()

    line = 1
    has_error = False
    i = 0

    # Scan for tokens
    while i < len(file_contents):
        char = file_contents[i]
        
        if char == '(':
            print("LEFT_PAREN ( null")
        elif char == ')':
            print("RIGHT_PAREN ) null")
        elif char == '{':
            print("LEFT_BRACE { null")
        elif char == '}':
            print("RIGHT_BRACE } null")
        elif char == ',':
            print("COMMA , null")
        elif char == '.':
            print("DOT . null")
        elif char == '-':
            print("MINUS - null")
        elif char == '+':
            print("PLUS + null")
        elif char == ';':
            print("SEMICOLON ; null")
        elif char == '*':
            print("STAR * null")
        elif char == '=':
            if i + 1 < len(file_contents) and file_contents[i + 1] == '=':
                print("EQUAL_EQUAL == null")
                i += 1  # Skip the next character as it's part of "=="
            else:
                print("EQUAL = null")
        elif char == '!':
            if i + 1 < len(file_contents) and file_contents[i + 1] == '=':
                print("BANG_EQUAL != null")
                i += 1  # Skip the next character as it's part of "!="
            else:
                print("BANG ! null")
        elif char == '<':
            if i + 1 < len(file_contents) and file_contents[i + 1] == '=':
                print("LESS_EQUAL <= null")
                i += 1  # Skip the next character as it's part of "<="
            else:
                print("LESS < null")
        elif char == '>':
            if i + 1 < len(file_contents) and file_contents[i + 1] == '=':
                print("GREATER_EQUAL >= null")
                i += 1  # Skip the next character as it's part of ">="
            else:
                print("GREATER > null")
        else:
            report_error(line, f"Unexpected character: {char}")
            has_error = True

        i += 1

    # End of file
    print("EOF  null")

    # Exit with code 65 if there were errors
    if has_error:
        exit(65)

if __name__ == "__main__":
    main()
