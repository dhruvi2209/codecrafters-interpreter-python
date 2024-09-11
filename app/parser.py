from typing import List, Union
from main import Token, TokenType

# Base class for all expressions
class Expr:
    pass

# Class for handling literal expressions
class Literal(Expr):
    def __init__(self, value: Union[bool, None]):
        self.value = value

    def __repr__(self):
        return str(self.value)

# Parser class for converting tokens into an AST
class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current = 0

    def parse(self) -> Expr:
        return self.expression()

    def expression(self) -> Expr:
        return self.literal()

    def literal(self) -> Expr:
        if self.match(TokenType.TRUE):
            return Literal(True)
        elif self.match(TokenType.FALSE):
            return Literal(False)
        elif self.match(TokenType.NIL):
            return Literal(None)

        raise Exception("Expected a literal.")

    def match(self, type: str) -> bool:
        if self.check(type):
            self.advance()
            return True
        return False

    def check(self, type: str) -> bool:
        if self.is_at_end():
            return False
        return self.peek().type == type

    def advance(self) -> Token:
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def is_at_end(self) -> bool:
        return self.peek().type == TokenType.EOF

    def peek(self) -> Token:
        return self.tokens[self.current]

    def previous(self) -> Token:
        return self.tokens[self.current - 1]
