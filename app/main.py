import sys
import os
from typing import Callable, Dict, List, Optional

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from token_types import Token, TokenType
from evaluator import Evaluator
from lox import Lox
from my_parser import Parser
from my_parser import Expr
from runtime_error import RuntimeError

class Scanner:
    def __init__(self, source: str):
        self.source = source
        self.tokens: List[Token] = []
        self.start = 0
        self.current = 0
        self.line = 1
        self.error_occurred = False
        
        self.reserved_words = {
            "and": TokenType.AND,
            "class": TokenType.CLASS,
            "else": TokenType.ELSE,
            "false": TokenType.FALSE,
            "for": TokenType.FOR,
            "fun": TokenType.FUN,
            "if": TokenType.IF,
            "nil": TokenType.NIL,
            "or": TokenType.OR,
            "print": TokenType.PRINT,
            "return": TokenType.RETURN,
            "super": TokenType.SUPER,
            "this": TokenType.THIS,
            "true": TokenType.TRUE,
            "var": TokenType.VAR,
            "while": TokenType.WHILE,
        }

        self.token_actions: Dict[str, Callable[[], None]] = {
            "(": lambda: self.add_token(TokenType.LEFT_PAREN),
            ")": lambda: self.add_token(TokenType.RIGHT_PAREN),
            "{": lambda: self.add_token(TokenType.LEFT_BRACE),
            "}": lambda: self.add_token(TokenType.RIGHT_BRACE),
            ",": lambda: self.add_token(TokenType.COMMA),
            ".": self.handle_dot,
            "-": lambda: self.add_token(TokenType.MINUS),
            "+": lambda: self.add_token(TokenType.PLUS),
            ";": lambda: self.add_token(TokenType.SEMICOLON),
            "*": lambda: self.add_token(TokenType.STAR),
            "!": lambda: self.add_token(TokenType.BANG_EQUAL if self.match("=") else TokenType.BANG),
            "=": lambda: self.add_token(TokenType.EQUAL_EQUAL if self.match("=") else TokenType.EQUAL),
            "<": lambda: self.add_token(TokenType.LESS_EQUAL if self.match("=") else TokenType.LESS),
            ">": lambda: self.add_token(TokenType.GREATER_EQUAL if self.match("=") else TokenType.GREATER),
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
        elif char.isalpha() or char == "_":
            self.identifier()
        elif char.isdigit():
            self.number()
        elif char.isspace():
            if char == '\n':
                self.line += 1
        else:
            Lox.error(self.line, f"Unexpected character: {char}")
            self.error_occurred = True

    def identifier(self) -> None:
        while self.peek().isalnum() or self.peek() == "_":
            self.advance()
        text = self.source[self.start:self.current]
        token_type = self.reserved_words.get(text, TokenType.IDENTIFIER)
        self.add_token(token_type)

    def handle_dot(self) -> None:
        if self.peek().isdigit():
            self.number()
        else:
            self.add_token(TokenType.DOT)

    def number(self) -> None:
        while self.peek().isdigit():
            self.advance()
        if self.peek() == '.' and self.is_digit(self.peek_next()):
            self.advance()
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
            return

        self.advance()
        lexeme = self.source[self.start:self.current]
        value = self.source[self.start + 1:self.current - 1]
        self.add_token(TokenType.STRING, value)

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
    if len(sys.argv) != 3 or sys.argv[1] not in ['tokenize', 'parse', 'evaluate']:
        print("Usage: python main.py <tokenize|parse|evaluate> <filename>", file=sys.stderr)
        sys.exit(64)

    filename = sys.argv[2]
    if not os.path.isfile(filename):
        print(f"Error: {filename} does not exist.", file=sys.stderr)
        sys.exit(66)

    with open(filename, 'r') as f:
        source_code = f.read()

    scanner = Scanner(source_code)
    tokens = scanner.scan_tokens()

    if sys.argv[1] == 'tokenize':
        for token in tokens:
            literal = 'null' if token.literal is None else token.literal
            print(f'{token.type} {token.lexeme} {literal}')

    elif sys.argv[1] == 'parse':
        parser = Parser(tokens)
        expression = parser.parse()
        print(expression)

    elif sys.argv[1] == 'evaluate':
        parser = Parser(tokens)
        expr = parser.parse()
        evaluator = Evaluator()
        try:
            result = evaluator.evaluate(expr)
            if result is not None:
                print(result)
        except RuntimeError as e:
            print(f"Runtime Error: {e.args[1]}\n[line {e.operator.line}]", file=sys.stderr)
            sys.exit(70)

    if Lox.had_error:
        sys.exit(65)
    if Lox.had_runtime_error:
        sys.exit(70)

if __name__ == "__main__":
    main()