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
        if self.match(TokenType.LEFT_PAREN):
            content = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return f"(group {content})"  # Ensure proper formatting here
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
        try:
            # Convert the token lexeme to a float
            number = float(token.lexeme)
            # Return the number formatted with the same precision as the original input
            # Remove trailing zeros in the decimal part
            formatted_number = f"{number:.{len(token.lexeme.split('.')[1])}f}" if '.' in token.lexeme else f"{number:.0f}"
            return formatted_number
        except ValueError:
            # Handle the case where the token is not a valid number
            raise ValueError(f"Invalid number literal: {token.lexeme}")


    
    def string(self) -> str:
        token = self.previous()
        return token.literal 


    def boolean(self) -> str:
        token = self.previous()
        return token.lexeme

    def nil(self) -> str:
        return "nil"

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
