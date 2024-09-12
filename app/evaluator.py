from typing import Union
from my_parser import Expr
import sys

class Evaluator:
    def evaluate(self, expr: Expr) -> Union[float, str, None]:
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

    def evaluate_literal(self, expr: Expr.Literal) -> Union[float, str, None]:
        if expr.value is True:
            return "true"
        elif expr.value is False:
            return "false"
        elif expr.value is None:
            return "nil"
        elif isinstance(expr.value, float):
            if expr.value.is_integer():
                return int(expr.value)
            return expr.value
        elif isinstance(expr.value, str):
            return expr.value
        else:
            raise ValueError(f"Unexpected literal value: {expr.value}")

    def evaluate_unary(self, expr: Expr.Unary) -> Union[float, str, None]:
        right = self.evaluate(expr.right)
        if expr.operator == '!':
            return "false" if right in ["true", None] else "true"
        elif expr.operator == '-':
            self.check_number_operand(expr.right)
            return -right
        else:
            self.runtime_error(f"Unknown unary operator: {expr.operator}")

    def evaluate_binary(self, expr: Expr.Binary) -> Union[float, str, None]:
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        if expr.operator == '+':
            return self.evaluate_addition(left, right)
        elif expr.operator == '-':
            self.check_number_operands(left, right)
            return left - right
        elif expr.operator == '*':
            self.check_number_operands(left, right)
            return left * right
        elif expr.operator == '/':
            self.check_number_operands(left, right)
            if right == 0:
                self.runtime_error("Division by zero is not allowed.")
            return left / right
        elif expr.operator == '>':
            self.check_number_operands(left, right)
            return "true" if left > right else "false"
        elif expr.operator == '<':
            self.check_number_operands(left, right)
            return "true" if left < right else "false"
        elif expr.operator == '>=':
            self.check_number_operands(left, right)
            return "true" if left >= right else "false"
        elif expr.operator == '<=':
            self.check_number_operands(left, right)
            return "true" if left <= right else "false"
        elif expr.operator == '==':
            return "true" if left == right else "false"
        elif expr.operator == '!=':
            return "true" if left != right else "false"
        else:
            self.runtime_error(f"Unexpected binary operator: {expr.operator}")

    def evaluate_addition(self, left, right) -> Union[float, str, None]:
        if isinstance(left, str) and isinstance(right, str):
            return left + right
        elif isinstance(left, (float, int)) and isinstance(right, (float, int)):
            return left + right
        else:
            self.runtime_error(f"Invalid types for '+': {type(left).__name__} and {type(right).__name__}")

    def check_number_operands(self, left, right) -> None:
        if not isinstance(left, (float, int)) or not isinstance(right, (float, int)):
            self.runtime_error("Operands must be numbers.")

    def check_number_operand(self, operand) -> None:
        if not isinstance(operand, (float, int)):
            self.runtime_error("Operand must be a number.")

    def runtime_error(self, message: str) -> None:
        print(message, file=sys.stderr)
        sys.exit(70)
