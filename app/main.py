from typing import Callable, Dict, List, Optional
import sys

class TokenType:
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
    STRING = "STRING"
    EOF = "EOF"

class Token:
    def __init__(self, type: str, lexeme: str, literal: Optional[object], line: int):
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __repr__(self):
        return f"{self.type} {self.lexeme} {self.literal}"

class Lox:
    @staticmethod
    def error(line: int, message: str):
        print(f"[line {line}] Error: {message}", file=sys.stderr)

class Scanner:
    def __init__(self, source: str):
        self.source = source
        self.tokens: List[Token] = []
        self.start = 0
        self.current = 0
        self.line = 1
        self.token_actions: Dict[str, Callable[[], None]] = {
            "(": lambda: self.add_token(TokenType.LEFT_PAREN),
            ")": lambda: self.add_token(TokenType.RIGHT_PAREN),
            "{": lambda: self.add_token(TokenType.LEFT_BRACE),
            "}": lambda: self.add_token(TokenType.RIGHT_BRACE),
            ",": lambda: self.add_token(TokenType.COMMA),
            ".": lambda: self.add_token(TokenType.DOT),
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
            char = self.advance()
            if char in ' \t':
                continue
            elif char == '\n':
                self.line += 1
            elif char in self.token_actions:
                self.token_actions[char]()
            else:
                Lox.error(self.line, f"Unexpected character: {char}")
        self.add_token(TokenType.EOF)
        self.print_tokens()
        return self.tokens

    def handle_string(self) -> None:
        self.start += 1  # Skip the initial quote
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == "\n":
                self.line += 1
            self.advance()
        if self.is_at_end():
            Lox.error(self.line, "Unterminated string.")
            return
        self.advance()  # Consume the closing quote
        value = self.source[self.start : self.current - 1]
        lexeme = self.source[self.start - 1 : self.current]
        self.add_token(TokenType.STRING, value)

    def handle_slash(self) -> None:
        if self.match('/'):
            while self.peek() != '\n' and not self.is_at_end():
                self.advance()
        else:
            self.add_token(TokenType.SLASH)

    def advance(self) -> str:
        self.current += 1
        return self.source[self.current - 1]

    def match(self, expected: str) -> bool:
        if self.is_at_end() or self.source[self.current] != expected:
            return False
        self.current += 1
        return True

    def add_token(self, type: str, literal: Optional[object] = None) -> None:
        text = self.source[self.start : self.current]
        token = Token(type, text, literal, self.line)
        self.tokens.append(token)

    def print_tokens(self) -> None:
        for token in self.tokens:
            print(token)

    def peek(self) -> str:
        return "\0" if self.is_at_end() else self.source[self.current]

    def is_at_end(self) -> bool:
        return self.current >= len(self.source)
