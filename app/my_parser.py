import sys
from typing import List, Union
from token_types import Token, TokenType
from lox import Lox

class Expr:
    class Literal:
        def __init__(self, value: Union[bool, None, float, str]):
            self.value = value

        def __repr__(self):
            if self.value is True:
                return 'true'
            elif self.value is False:
                return 'false'
            elif self.value is None:
                return 'nil'
            return str(self.value)

        def __str__(self):
            return self.__repr__()

    class Binary:
        def __init__(self, left, operator: str, right):
            self.left = left
            self.operator = operator
            self.right = right

        def __str__(self):
            # Format strings to include parentheses for negative numbers
            def format_operand(operand):
                if isinstance(operand, Expr.Unary):
                    return f"({operand})"  # Enclose the unary expression in parentheses
                return str(operand)

            left_str = format_operand(self.left)
            right_str = format_operand(self.right)
            return f"({self.operator} {left_str} {right_str})"


    class Unary:
        def __init__(self, operator: str, right):
            self.operator = operator
            self.right = right

        def __str__(self):
            # Add parentheses around unary expressions to match expected output
            return f"({self.operator} {self.right})"


    class Grouping:
        def __init__(self, expression):
            self.expression = expression

        def __str__(self):
            return f"(group {self.expression})"


# Now define the Parser class
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def parse(self) -> Expr:
        try:
            return self.expression()
        except SystemExit as e:
            if e.code == 65:
                sys.exit(65)
            else:
                raise

    def expression(self) -> Expr:
        return self.assignment()

    def assignment(self) -> Expr:
        expr = self.equality()
        if self.match(TokenType.EQUAL):
            value = self.assignment()
            return Expr.Binary(expr, '=', value)
        return expr

    def equality(self) -> Expr:
        expr = self.comparison()
        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self.previous().lexeme
            right = self.comparison()
            expr = Expr.Binary(expr, operator, right)
        return expr

    def comparison(self) -> Expr:
        expr = self.addition()
        while self.match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
            operator = self.previous().lexeme
            right = self.addition()
            expr = Expr.Binary(expr, operator, right)
        return expr

    def addition(self) -> Expr:
        expr = self.multiplication()
        while self.match(TokenType.PLUS, TokenType.MINUS):
            operator = self.previous().lexeme
            right = self.multiplication()
            expr = Expr.Binary(expr, operator, right)
        return expr

    def multiplication(self) -> Expr:
        expr = self.unary()
        while self.match(TokenType.STAR, TokenType.SLASH):
            operator = self.previous().lexeme
            right = self.unary()
            expr = Expr.Binary(expr, operator, right)
        return expr

    def unary(self) -> Expr:
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator = self.previous().lexeme
            operand = self.unary()
            return Expr.Unary(operator, operand)
        return self.primary()

    def primary(self) -> Expr:
        if self.match(TokenType.NUMBER):
            return Expr.Literal(float(self.previous().lexeme))
        elif self.match(TokenType.STRING):
            return Expr.Literal(self.previous().literal)
        elif self.match(TokenType.TRUE):
            return Expr.Literal(True)
        elif self.match(TokenType.FALSE):
            return Expr.Literal(False)
        elif self.match(TokenType.NIL):
            return Expr.Literal(None)
        elif self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Expr.Grouping(expr)
        else:
            self.error(self.peek(), "Expect expression.")
            raise SystemExit(65)

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
