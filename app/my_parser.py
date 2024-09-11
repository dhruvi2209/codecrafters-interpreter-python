from typing import List, Union, Optional
from token_types import Token, TokenType
import re

class Expr:
    pass

class Literal(Expr):
    def __init__(self, value: Union[bool, None, str]):
        self.value = value

    def __repr__(self):
        if isinstance(self.value, str):
            return f'"{self.value}"'
        if self.value is True:
            return 'true'
        elif self.value is False:
            return 'false'
        elif self.value is None:
            return 'nil'
        return str(self.value)

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current = 0

    def parse(self) -> str:
        # Start parsing from the top-level expression
        return self.expression()

    def expression(self) -> str:
        # Try parsing different types of literals
        if self.match(TokenType.NUMBER):
            return self.number()
        elif self.match(TokenType.TRUE, TokenType.FALSE):
            return self.boolean()
        elif self.match(TokenType.NIL):
            return self.nil()
        elif self.match(TokenType.STRING):
            return self.string()
        # Handle other expressions as needed
        else:
            return "Unexpected token"

    def number(self) -> str:
        token = self.previous()
        value = token.lexeme
        
        # Use regex to preserve decimal precision
        if re.match(r'^\d+$', value):
            return f"{float(value):.1f}"
        else:
            return value

    def boolean(self) -> str:
        token = self.previous()
        return token.lexeme

    def nil(self) -> str:
        return "nil"

    def string(self) -> str:
        token = self.previous()
        return token.literal

    def match(self, *types: str) -> bool:
        for token_type in types:
            if self.check(token_type):
                self.advance()
                return True
        return False

    def check(self, token_type: str) -> bool:
        if self.is_at_end():
            return False
        return self.peek().type == token_type

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
