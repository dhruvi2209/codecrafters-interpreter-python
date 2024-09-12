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
            sys.exit(70)  # Ensure we exit with code 70 for runtime errors

    def evaluate_literal(self, expr: Expr.Literal) -> Union[Decimal, str, None]:
        if expr.value is True:
            return "true"
        elif expr.value is False:
            return "false"
        elif expr.value is None:
            return "nil"
        elif isinstance(expr.value, (int, float)):
            return Decimal(expr.value)
        elif isinstance(expr.value, str):
            return expr.value
        else:
            raise ValueError(f"Unexpected literal value: {expr.value}")

    def evaluate_unary(self, expr: Expr.Unary) -> Union[Decimal, str, None]:
        right = self.evaluate(expr.right)
        if expr.operator.type == TokenType.BANG:
            return "false" if right in ["true", "nil"] else "true"
        elif expr.operator.type == TokenType.MINUS:
            if not isinstance(right, (Decimal, int)):
                raise RuntimeError(expr.operator, "Operand must be a number.")
            return -Decimal(right)
        else:
            raise RuntimeError(expr.operator, f"Unknown unary operator: {expr.operator}")

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

    def evaluate_comparison(self, operator: Token, left: Union[Decimal, str], right: Union[Decimal, str]) -> str:
        if isinstance(left, (Decimal, int)) and isinstance(right, (Decimal, int)):
            if operator.type == TokenType.GREATER:
                return "true" if left > right else "false"
            elif operator.type == TokenType.GREATER_EQUAL:
                return "true" if left >= right else "false"
            elif operator.type == TokenType.LESS:
                return "true" if left < right else "false"
            elif operator.type == TokenType.LESS_EQUAL:
                return "true" if left <= right else "false"
            elif operator.type == TokenType.EQUAL_EQUAL:
                return "true" if left == right else "false"
            elif operator.type == TokenType.BANG_EQUAL:
                return "true" if left != right else "false"
        else:
            raise RuntimeError(operator, "Operands must be numbers.")

    def runtime_error(self, error: RuntimeError) -> None:
        print(f"{error.args[1]}\n[line {error.operator.line}]", file=sys.stderr)
