import sys

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

    # Scan for tokens
    for char in file_contents:
        if char == '(':
            print("LEFT_PAREN ( null")
        elif char == ')':
            print("RIGHT_PAREN ) null")

    # End of file
    print("EOF  null")

if __name__ == "__main__":
    main()
