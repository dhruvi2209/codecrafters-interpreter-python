from typing import Callable, Dict, List, Optional
import sys

class TokenType:
    LEFT_PAREN = 'LEFT_PAREN'
    RIGHT_PAREN = 'RIGHT_PAREN'
    LEFT_BRACE = 'LEFT_BRACE'
    RIGHT_BRACE = 'RIGHT_BRACE'
    COMMA = 'COMMA'
    DOT = 'DOT'
    MINUS = 'MINUS'
    PLUS = 'PLUS'
    SEMICOLON = 'SEMICOLON'
    STAR = 'STAR'
    BANG = 'BANG'
    BANG_EQUAL = 'BANG_EQUAL'
    EQUAL = 'EQUAL'
    EQUAL_EQUAL = 'EQUAL_EQUAL'
    LESS = 'LESS'
    LESS_EQUAL = 'LESS_EQUAL'
    GREATER = 'GREATER'
    GREATER_EQUAL = 'GREATER_EQUAL'
    SLASH = 'SLASH'
    STRING = 'STRING'
    NUMBER = 'NUMBER'
    EOF = 'EOF'

class Token:
    def __init__(self, type: str, lexeme: str, literal: Optional[object], line: int):
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

class Lox:
    @staticmethod
    def error(line: int, message: str) -> None:
        print(f"[line {line}] Error: {message}", file=sys.stderr)

class Scanner:
    def __init__(self, source: str):
        self.source = source
        self.tokens: List[Token] = []
        self.start = 0
        self.current = 0
        self.line = 1
        self.error_occurred = False
        self.token_actions: Dict[str, Callable[[], None]] = {
            "(": lambda: self.add_token(TokenType.LEFT_PAREN),
            ")": lambda: self.add_token(TokenType.RIGHT_PAREN),
            "{": lambda: self.add_token(TokenType.LEFT_BRACE),
            "}": lambda: self.add_token(TokenType.RIGHT_BRACE),
            ",": lambda: self.add_token(TokenType.COMMA),
            ".": lambda: self.handle_dot(),
            "-": lambda: self.add_token(TokenType.MINUS),
            "+": lambda: self.add_token(TokenType.PLUS),
            ";": lambda: self.add_token(TokenType.SEMICOLON),
            "*": lambda: self.add_token(TokenType.STAR),
            "!": lambda: self.add_token(
                TokenType.BANG_EQUAL if self.match("=") else TokenType.BANG
            ),
            "=": lambda: self.add_token(
                TokenType.EQUAL_EQUAL if self.match("=") else TokenType.EQUAL
            ),
            "<": lambda: self.add_token(
                TokenType.LESS_EQUAL if self.match("=") else TokenType.LESS
            ),
            ">": lambda: self.add_token(
                TokenType.GREATER_EQUAL if self.match("=") else TokenType.GREATER
            ),
            "/": self.handle_slash,
            '"': self.handle_string,
        }

    def scan_tokens(self) -> List[Token]:
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    def scan_token(self) -> None:
        char = self.advance()

        if char in self.token_actions:
            self.token_actions[char]()
        elif char.isalpha():
            self.identifier()
        elif char.isdigit():
            self.number()
        elif char.isspace():
            if char == '\n':
                self.line += 1
        else:
            Lox.error(self.line, f"Unexpected character: {char}")

    def handle_dot(self) -> None:
        if self.peek().isdigit():
            self.number()
        else:
            self.add_token(TokenType.DOT)

    def number(self) -> None:
        while self.peek().isdigit():
            self.advance()

        if self.peek() == '.' and self.is_digit(self.peek_next()):
            self.advance()  # Consume the '.'
            while self.peek().isdigit():
                self.advance()

        value = float(self.source[self.start:self.current])
        self.add_token(TokenType.NUMBER, value)

    def is_digit(self, c: str) -> bool:
        return '0' <= c <= '9'

    def peek_next(self) -> str:
        if self.current + 1 >= len(self.source):
            return '\0'
        return self.source[self.current + 1]

    def handle_slash(self) -> None:
        if self.match("/"):
            while self.peek() != '\n' and not self.is_at_end():
                self.advance()
        else:
            self.add_token(TokenType.SLASH)

    def handle_string(self) -> None:
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == '\n':
                self.line += 1
            self.advance()
        if self.is_at_end():
            Lox.error(self.line, "Unterminated string.")
            self.error_occurred = True
            return
        self.advance()
        value = self.source[self.start + 1:self.current - 1]
        self.add_token(TokenType.STRING, value)

    def identifier(self) -> None:
        while self.peek().isalnum() or self.peek() == "_":
            self.advance()
        text = self.source[self.start:self.current]
        self.add_token(text.upper(), text)

    def advance(self) -> str:
        self.current += 1
        return self.source[self.current - 1]

    def match(self, expected: str) -> bool:
        if self.is_at_end() or self.source[self.current] != expected:
            return False
        self.current += 1
        return True

    def add_token(self, type: str, literal: Optional[object] = None) -> None:
        text = self.source[self.start:self.current]
        self.tokens.append(Token(type, text, literal, self.line))

    def peek(self) -> str:
        return "\0" if self.is_at_end() else self.source[self.current]

    def is_at_end(self) -> bool:
        return self.current >= len(self.source)

    

def main() -> None:
    if len(sys.argv) != 3 or sys.argv[1] != 'tokenize':
        print("Usage: ./your_program.sh tokenize <filename>", file=sys.stderr)
        sys.exit(64)

    filename = sys.argv[2]
    with open(filename, "r") as file:
        source = file.read()

    scanner = Scanner(source)
    tokens = scanner.scan_tokens()

    for token in tokens:
        if token.type == TokenType.EOF:
            print(f"{token.type}  null")
        else:
            literal = 'null' if token.literal is None else token.literal
            print(f"{token.type} {token.lexeme} {literal}")

    if scanner.error_occurred:
        sys.exit(65)

if __name__ == "__main__":
    main()
