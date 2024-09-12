from typing import Union
from token_types import Token, TokenType
from runtime_error import RuntimeError
from decimal import Decimal
from my_parser import Expr
import sys

class Evaluator:
    def evaluate(self, expr: Expr) -> Union[Decimal, str, None]:
        try:
            if isinstance(expr, Expr.Literal):
                return self.evaluate_literal(expr)
            elif isinstance(expr, Expr.Unary):
                return self.evaluate_unary(expr)
            elif isinstance(expr, Expr.Binary):
                return self.evaluate_binary(expr)
            elif isinstance(expr, Expr.Grouping):
                return self.evaluate(expr.expression)
            else:
                raise ValueError(f"Unexpected expression type: {type(expr)}")
        except RuntimeError as e:
            self.runtime_error(e)
            sys.exit(70)  # Exit with code 70 for runtime errors


    def evaluate_binary(self, expr: Expr.Binary) -> Union[Decimal, str, None]:
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        if expr.operator.type == TokenType.PLUS:
            if isinstance(left, str) and isinstance(right, str):
                return left + right
            elif isinstance(left, (Decimal, int)) and isinstance(right, (Decimal, int)):
                return Decimal(left) + Decimal(right)
            else:
                raise RuntimeError(expr.operator, "Operands must be two numbers or two strings.")
        
        elif expr.operator.type == TokenType.MINUS:
            if isinstance(left, (Decimal, int)) and isinstance(right, (Decimal, int)):
                return Decimal(left) - Decimal(right)
            else:
                raise RuntimeError(expr.operator, "Operands must be numbers.")
        
        elif expr.operator.type == TokenType.STAR:
            if isinstance(left, (Decimal, int)) and isinstance(right, (Decimal, int)):
                return Decimal(left) * Decimal(right)
            else:
                raise RuntimeError(expr.operator, "Operands must be numbers.")
        
        elif expr.operator.type == TokenType.SLASH:
            if isinstance(left, (Decimal, int)) and isinstance(right, (Decimal, int)):
                if right == 0:
                    raise RuntimeError(expr.operator, "Division by zero is not allowed.")
                return Decimal(left) / Decimal(right)
            else:
                raise RuntimeError(expr.operator, "Operands must be numbers.")
        
        elif expr.operator.type in {
            TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, 
            TokenType.LESS_EQUAL, TokenType.EQUAL_EQUAL, TokenType.BANG_EQUAL
        }:
            return self.evaluate_comparison(expr.operator, left, right)
        
        else:
            raise RuntimeError(expr.operator, f"Unexpected binary operator: {expr.operator}")

    def runtime_error(self, error: RuntimeError) -> None:
        print(f"{error}\n[line {error.token.line}]", file=sys.stderr)