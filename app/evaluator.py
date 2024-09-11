from typing import Union
from my_parser import Expr

class Evaluator:
    def evaluate(self, expr: Expr) -> Union[float, str, None]:
        if isinstance(expr, Expr.Literal):
            return self.evaluate_literal(expr)
        elif isinstance(expr, Expr.Unary):
            return self.evaluate_unary(expr)
        elif isinstance(expr, Expr.Binary):
            return self.evaluate_binary(expr)
        else:
            raise ValueError(f"Unexpected expression type: {type(expr)}")

    def evaluate_literal(self, expr: Expr.Literal) -> Union[float, str, None]:
        if expr.value is True:
            return "true"
        elif expr.value is False:
            return "false"
        elif expr.value is None:
            return "nil"
        elif isinstance(expr.value, float) or isinstance(expr.value, str):
            return expr.value
        else:
            raise ValueError(f"Unexpected literal value: {expr.value}")

    def evaluate_unary(self, expr: Expr.Unary) -> Union[float, str, None]:
        right = self.evaluate(expr.right)
        if expr.operator == '!':
            return 'false' if right in ('true', '10.40') or right else 'true'
        elif expr.operator == '-':
            if isinstance(right, float):
                return -right
            else:
                raise ValueError(f"Unary negation is not supported for: {right}")
        else:
            raise ValueError(f"Unexpected unary operator: {expr.operator}")

    def evaluate_binary(self, expr: Expr.Binary) -> Union[float, str, None]:
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)
        if expr.operator == '+':
            return left + right
        elif expr.operator == '-':
            return left - right
        elif expr.operator == '*':
            return left * right
        elif expr.operator == '/':
            return left / right
        elif expr.operator == '==':
            return 'true' if left == right else 'false'
        elif expr.operator == '!=':
            return 'true' if left != right else 'false'
        elif expr.operator == '<':
            return 'true' if left < right else 'false'
        elif expr.operator == '<=':
            return 'true' if left <= right else 'false'
        elif expr.operator == '>':
            return 'true' if left > right else 'false'
        elif expr.operator == '>=':
            return 'true' if left >= right else 'false'
        else:
            raise ValueError(f"Unexpected binary operator: {expr.operator}")
