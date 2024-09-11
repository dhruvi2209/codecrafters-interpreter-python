from typing import List, Union
from token_types import Token, TokenType
import re
from lox import Lox  # Updated import

class Expr:
    pass

class Literal(Expr):
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
        return self.expression()

    def expression(self) -> str:
        return self.equality()  # Start with equality

    def equality(self) -> str:
        expr = self.comparison()  # Parse comparison operators first

        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self.previous().lexeme
            right = self.comparison()  # Parse the right-hand side of the equality
            expr = f"({operator} {expr} {right})"
        
        return expr

    def comparison(self) -> str:
        expr = self.addition()  # Parse addition operators first

        while self.match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
            operator = self.previous().lexeme
            right = self.addition()  # Parse the right-hand side of the comparison
            expr = f"({operator} {expr} {right})"
        
        return expr

    def addition(self) -> str:
        expr = self.multiplication()  # Parse multiplication operators first

        while self.match(TokenType.PLUS, TokenType.MINUS):
            operator = self.previous().lexeme
            right = self.multiplication()  # Parse the right-hand side of the addition
            expr = f"({operator} {expr} {right})"
        
        return expr

    def multiplication(self) -> str:
        expr = self.unary()  # Parse unary operators first

        while self.match(TokenType.STAR, TokenType.SLASH):
            operator = self.previous().lexeme
            right = self.unary()  # Parse the right-hand side of the multiplication
            expr = f"({operator} {expr} {right})"
        
        return expr

    def unary(self) -> str:
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator = self.previous().lexeme
            operand = self.unary()  # Recursively parse the operand
            return f"({operator} {operand})"
        return self.primary()

    def primary(self) -> str:
        if self.match(TokenType.LEFT_PAREN):
            content = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return f"(group {content})"
        elif self.match(TokenType.STRING):
            return self.string()
        elif self.match(TokenType.NUMBER):
            return self.number()
        elif self.match(TokenType.TRUE, TokenType.FALSE):
            return self.boolean()
        elif self.match(TokenType.NIL):
            return "nil"
        else:
            Lox.error(self.peek().line, "Unexpected token")
            return "Unexpected token"

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
            Lox.error(self.peek().line, message)

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


#  def number(self) -> str:
#         token = self.previous()
#         # Check if the number has a decimal point
#         if '.' in token.lexeme:
#             return token.lexeme
#         else:
#             # Convert to float and format to ensure decimal point
#             return f"{float(token.lexeme):.1f}"