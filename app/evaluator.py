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
            if right == "true":
                return "false"
            elif right == "false" or right == "nil":
                return "true"
            elif isinstance(right, (float, int)):
                return "false"
            else:
                # Exiting with code 70 without printing an error message
                sys.exit(70)
        elif expr.operator == '-':
            if isinstance(right, (float, int)):
                return -right
            else:
                # Exiting with code 70 without printing an error message
                sys.exit(70)
        else:
            # Exiting with code 70 for unknown operators
            sys.exit(70)

    def evaluate_binary(self, expr: Expr.Binary) -> Union[int, float, str, None]:
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        if expr.operator == '+':
            if isinstance(left, str) and isinstance(right, str):
                return left + right
            elif isinstance(left, (float, int)) and isinstance(right, (float, int)):
                result = left + right
                return int(result) if result.is_integer() else result
            else:
                raise ValueError(f"Unsupported operand types for +: {type(left)}, {type(right)}")
        elif expr.operator == '-':
            if isinstance(left, (float, int)) and isinstance(right, (float, int)):
                result = left - right
                return int(result) if result.is_integer() else result
            else:
                raise ValueError(f"Unsupported operand types for -: {type(left)}, {type(right)}")
        elif expr.operator == '*':
            if isinstance(left, (float, int)) and isinstance(right, (float, int)):
                result = left * right
                return int(result) if result.is_integer() else result
            else:
                # Exiting with code 70 without printing an error message
                sys.exit(70)
        elif expr.operator == '/':
            if isinstance(left, (float, int)) and isinstance(right, (float, int)):
                if right == 0:
                    raise ValueError("Division by zero is not allowed")
                result = left / right
                return int(result) if result.is_integer() else result
            else:
                # Exiting with code 70 without printing an error message
                sys.exit(70)
        elif expr.operator == '>':
            if isinstance(left, (float, int)) and isinstance(right, (float, int)):
                return "true" if left > right else "false"
            else:
                raise ValueError(f"Unsupported operand types for >: {type(left)}, {type(right)}")
        elif expr.operator == '<':
            if isinstance(left, (float, int)) and isinstance(right, (float, int)):
                return "true" if left < right else "false"
            else:
                raise ValueError(f"Unsupported operand types for <: {type(left)}, {type(right)}")
        elif expr.operator == '>=':
            if isinstance(left, (float, int)) and isinstance(right, (float, int)):
                return "true" if left >= right else "false"
            else:
                raise ValueError(f"Unsupported operand types for >=: {type(left)}, {type(right)}")
        elif expr.operator == '<=':
            if isinstance(left, (float, int)) and isinstance(right, (float, int)):
                return "true" if left <= right else "false"
            else:
                raise ValueError(f"Unsupported operand types for <=: {type(left)}, {type(right)}")
        elif expr.operator == '==':
            if isinstance(left, (float, int, str)) and isinstance(right, (float, int, str)):
                return "true" if left == right else "false"
            else:
                raise ValueError(f"Unsupported operand types for ==: {type(left)}, {type(right)}")
        elif expr.operator == '!=':
            if isinstance(left, (float, int, str)) and isinstance(right, (float, int, str)):
                return "true" if left != right else "false"
            else:
                raise ValueError(f"Unsupported operand types for !=: {type(left)}, {type(right)}")
        else:
            raise ValueError(f"Unexpected binary operator: {expr.operator}")
