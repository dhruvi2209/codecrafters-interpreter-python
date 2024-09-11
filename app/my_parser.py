import sys
from typing import List, Union
from token_types import Token, TokenType
import re
from lox import Lox  # Updated import

class Expr:
    class Literal:
        def __init__(self, value: Union[bool, None]):
            self.value = value

        def __repr__(self):
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
        try:
            return self.expression()
        except SystemExit as e:
            if e.code == 65:
                # Exit with code 65 for syntax errors
                sys.exit(65)
            else:
                raise

    def expression(self) -> str:
        try:
            return self.assignment()
        except SystemExit as e:
            if e.code == 65:
                sys.exit(65)
            else:
                raise

    def assignment(self) -> str:
        expr = self.equality()
        if self.match(TokenType.EQUAL):
            value = self.assignment()
            return f"(= {expr} {value})"
        return expr

    def equality(self) -> str:
        expr = self.comparison()
        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self.previous().lexeme
            right = self.comparison()
            expr = f"({operator} {expr} {right})"
        return expr

    def comparison(self) -> str:
        expr = self.addition()
        while self.match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
            operator = self.previous().lexeme
            right = self.addition()
            expr = f"({operator} {expr} {right})"
        return expr

    def addition(self) -> str:
        expr = self.multiplication()
        while self.match(TokenType.PLUS, TokenType.MINUS):
            operator = self.previous().lexeme
            right = self.multiplication()
            expr = f"({operator} {expr} {right})"
        return expr

    def multiplication(self) -> str:
        expr = self.unary()
        while self.match(TokenType.STAR, TokenType.SLASH):
            operator = self.previous().lexeme
            right = self.unary()
            expr = f"({operator} {expr} {right})"
        return expr

    def unary(self) -> str:
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator = self.previous().lexeme
            operand = self.unary()
            return f"({operator} {operand})"
        return self.primary()

    def primary(self) -> str:
        if self.match(TokenType.NUMBER):
            return self.number()
        elif self.match(TokenType.STRING):
            return self.string()
        elif self.match(TokenType.TRUE, TokenType.FALSE):
            return self.boolean()
        elif self.match(TokenType.NIL):
            return "nil"
        elif self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return f"(group {expr})"
        else:
            self.error(self.peek(), "Expect expression.")
            raise SystemExit(65)  # Exit with code 65 for syntax errors

    def number(self) -> str:
        token = self.previous()
        if '.' in token.lexeme:
            return token.lexeme
        else:
            return f"{float(token.lexeme):.1f}"

    def string(self) -> str:
        token = self.previous()
        return token.literal

    def boolean(self) -> str:
        token = self.previous()
        return token.lexeme

    def match(self, *types: str) -> bool:
        for token_type in types:
            if self.check(token_type):
                self.advance()
                return True
        return False

    def consume(self, token_type: str, message: str) -> None:
        if self.check(token_type):
            self.advance()
        else:
            self.error(self.peek(), message)
            raise SystemExit(65)  # Exit with code 65 for syntax errors

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

    def error(self, token: Token, message: str) -> None:
        Lox.error(token.line, message)


#  def number(self) -> str:
#         token = self.previous()
#         # Check if the number has a decimal point
#         if '.' in token.lexeme:
#             return token.lexeme
#         else:
#             # Convert to float and format to ensure decimal point
#             return f"{float(token.lexeme):.1f}"