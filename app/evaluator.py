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
        elif isinstance(expr.value, float):
            # Convert float to int if it's a whole number
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
            else:
                raise ValueError(f"Unary '!' is not supported for: {right}")
        elif expr.operator == '-':
            if isinstance(right, (float, int)):
                # Convert result to int if it's a whole number
                result = -right
                if result.is_integer():
                    return int(result)
                return result
            else:
                raise ValueError(f"Unary '-' is not supported for: {right}")
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
            return "true" if left == right else "false"
        elif expr.operator == '!=':
            return "true" if left != right else "false"
        elif expr.operator == '<':
            return "true" if left < right else "false"
        elif expr.operator == '<=':
            return "true" if left <= right else "false"
        elif expr.operator == '>':
            return "true" if left > right else "false"
        elif expr.operator == '>=':
            return "true" if left >= right else "false"
        else:
            raise ValueError(f"Unexpected binary operator: {expr.operator}")
