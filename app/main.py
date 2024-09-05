import sys
from typing import Optional, List

class TokenType:
    STRING = "STRING"
    LEFT_PAREN = "LEFT_PAREN"
    RIGHT_PAREN = "RIGHT_PAREN"
    LEFT_BRACE = "LEFT_BRACE"
    RIGHT_BRACE = "RIGHT_BRACE"
    COMMA = "COMMA"
    DOT = "DOT"
    MINUS = "MINUS"
    PLUS = "PLUS"
    SEMICOLON = "SEMICOLON"
    STAR = "STAR"
    BANG = "BANG"
    BANG_EQUAL = "BANG_EQUAL"
    EQUAL = "EQUAL"
    EQUAL_EQUAL = "EQUAL_EQUAL"
    LESS = "LESS"
    LESS_EQUAL = "LESS_EQUAL"
    GREATER = "GREATER"
    GREATER_EQUAL = "GREATER_EQUAL"
    SLASH = "SLASH"
    EOF = "EOF"
    ERROR = "ERROR"

class Token:
    def __init__(self, type: TokenType, lexeme: str, literal: Optional[str], line: int):
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __repr__(self):
        return f"{self.type} {self.lexeme} {self.literal}"

class Scanner:
    def __init__(self, source: str):
        self.source = source
        self.tokens: List[Token] = []
        self.start = 0
        self.current = 0
        self.line = 1

    def scan_tokens(self) -> List[Token]:
        while not self.is_at_end():
            self.start = self.current
            char = self.advance()
            if char == '"':
                self.handle_string()
            elif char in "()+-*/;,.{}":
                self.add_token(self.map_single_char_token(char))
            elif char in "!=<>":
                self.add_token(self.map_two_char_token(char))
            elif char in " \t":
                pass  # Ignore whitespace
            elif char.isalpha() or char == '_':
                self.handle_identifier()  # Example for identifiers
            elif char.isdigit():
                self.handle_number()  # Example for numbers
            else:
                self.add_token(TokenType.ERROR, f"[line {self.line}] Error: Unexpected character.", None, self.line)

        self.add_token(TokenType.EOF, "", None, self.line)
        return self.tokens

    def handle_string(self):
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == '\n':
                self.line += 1
            self.advance()

        if self.is_at_end():
            self.add_token(TokenType.ERROR, f"[line {self.line}] Error: Unterminated string.", None, self.line)
            return

        self.advance()  # Skip the closing "
        value = self.source[self.start + 1:self.current - 1]
        self.add_token(TokenType.STRING, f'"{value}"', value, self.line)

    def handle_identifier(self):
        # Example handling of identifiers (e.g., keywords, variables)
        pass

    def handle_number(self):
        # Example handling of numbers
        pass

    def map_single_char_token(self, char: str) -> TokenType:
        mapping = {
            '(': TokenType.LEFT_PAREN,
            ')': TokenType.RIGHT_PAREN,
            '{': TokenType.LEFT_BRACE,
            '}': TokenType.RIGHT_BRACE,
            ',': TokenType.COMMA,
            '.': TokenType.DOT,
            '-': TokenType.MINUS,
            '+': TokenType.PLUS,
            ';': TokenType.SEMICOLON,
            '*': TokenType.STAR
        }
        return mapping.get(char, TokenType.ERROR)

    def map_two_char_token(self, char: str) -> TokenType:
        if char == '!':
            return TokenType.BANG_EQUAL if self.match('=') else TokenType.BANG
        elif char == '=':
            return TokenType.EQUAL_EQUAL if self.match('=') else TokenType.EQUAL
        elif char == '<':
            return TokenType.LESS_EQUAL if self.match('=') else TokenType.LESS
        elif char == '>':
            return TokenType.GREATER_EQUAL if self.match('=') else TokenType.GREATER
        return TokenType.ERROR

    def advance(self) -> str:
        self.current += 1
        return self.source[self.current - 1]

    def match(self, expected: str) -> bool:
        if self.is_at_end() or self.source[self.current] != expected:
            return False
        self.current += 1
        return True

    def add_token(self, type: TokenType, lexeme: Optional[str] = None, literal: Optional[str] = None, line: Optional[int] = None):
        if lexeme is None:
            lexeme = self.source[self.start:self.current]
        if line is None:
            line = self.line
        self.tokens.append(Token(type, lexeme, literal, line))

    def peek(self) -> str:
        if self.is_at_end():
            return '\0'
        return self.source[self.current]

    def is_at_end(self) -> bool:
        return self.current >= len(self.source)

def main():
    if len(sys.argv) != 2:
        print("Usage: python scanner.py <source file>")
        return

    source_file = sys.argv[1]
    try:
        with open(source_file, 'r') as file:
            source = file.read()
    except IOError as e:
        print(f"Error reading file {source_file}: {e}")
        return

    scanner = Scanner(source)
    tokens = scanner.scan_tokens()

    for token in tokens:
        print(token)

if __name__ == "__main__":
    main()
