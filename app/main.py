import sys

def report_error(line, message):
    print(f"[line {line}] Error: {message}", file=sys.stderr)

def main():
    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh tokenize <filename>", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    if command != "tokenize":
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)

    try:
        with open(filename) as file:
            file_contents = file.read()
    except IOError as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        exit(1)

    line = 1
    has_error = False
    i = 0
    length = len(file_contents)

    while i < length:
        char = file_contents[i]

        if char in ' \t':  # Skip whitespace (space and tab)
            i += 1
            continue

        if char == '\n':  # Handle newlines
            line += 1
        elif char == '/':
            if i + 1 < length and file_contents[i + 1] == '/':
                # Skip to the end of the line for comments
                i += 2
                while i < length and file_contents[i] != '\n':
                    i += 1
                continue
            else:
                print("SLASH / null")
        elif char == '(':
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
            if i + 1 < length and file_contents[i + 1] == '=':
                print("EQUAL_EQUAL == null")
                i += 1
            else:
                print("EQUAL = null")
        elif char == '!':
            if i + 1 < length and file_contents[i + 1] == '=':
                print("BANG_EQUAL != null")
                i += 1
            else:
                print("BANG ! null")
        elif char == '<':
            if i + 1 < length and file_contents[i + 1] == '=':
                print("LESS_EQUAL <= null")
                i += 1
            else:
                print("LESS < null")
        elif char == '>':
            if i + 1 < length and file_contents[i + 1] == '=':
                print("GREATER_EQUAL >= null")
                i += 1
            else:
                print("GREATER > null")
        elif char == '"':
            start = i
            i += 1
            while i < length and file_contents[i] != '"':
                if file_contents[i] == '\n':
                    line += 1
                i += 1
            if i < length and file_contents[i] == '"':
                lexeme = file_contents[start:i+1]
                literal = file_contents[start+1:i]
                print(f"STRING {lexeme} {literal}")
                i += 1
            else:
                report_error(line, "Unterminated string.")
                has_error = True
        else:
            report_error(line, f"Unexpected character: {char}")
            has_error = True

        i += 1

    # End of file
    print("EOF  null")

    if has_error:
        exit(65)

if __name__ == "__main__":
    main()

