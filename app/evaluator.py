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
                self.runtime_error("Invalid operand type for unary '!'")
        elif expr.operator == '-':
            if isinstance(right, (float, int)):
                return -right
            else:
                self.runtime_error("Invalid operand type for unary '-'")
        else:
            self.runtime_error(f"Unknown unary operator: {expr.operator}")

    def evaluate_binary(self, expr: Expr.Binary) -> Union[float, str, None]:
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        if expr.operator == '+':
            # Check if both are strings
            if isinstance(left, str) and isinstance(right, str):
                return left + right
            # Check if both are numbers
            elif isinstance(left, (float, int)) and isinstance(right, (float, int)):
                result = left + right
                return int(result) if isinstance(result, float) and result.is_integer() else result
            else:
                # Raise error if incompatible types (like string + boolean)
                self.runtime_error(f"Invalid types for '+': {type(left).__name__} and {type(right).__name__}")
        
        elif expr.operator == '-':
            if isinstance(left, (float, int)) and isinstance(right, (float, int)):
                result = left - right
                return int(result) if isinstance(result, float) and result.is_integer() else result
            else:
                self.runtime_error("Operands must be numbers.")
        
        elif expr.operator == '*':
            if isinstance(left, (float, int)) and isinstance(right, (float, int)):
                result = left * right
                return int(result) if result.is_integer() else result
            else:
                self.runtime_error("Operands must be numbers.")
        
        elif expr.operator == '/':
            if isinstance(left, (float, int)) and isinstance(right, (float, int)):
                if right == 0:
                    self.runtime_error("Division by zero is not allowed.")
                result = left / right
                return int(result) if result.is_integer() else result
            else:
                self.runtime_error("Operands must be numbers.")
        
        elif expr.operator == '>':
            if isinstance(left, (float, int)) and isinstance(right, (float, int)):
                return "true" if left > right else "false"
            else:
                self.runtime_error("Operands must be numbers.")
        
        elif expr.operator == '<':
            if isinstance(left, (float, int)) and isinstance(right, (float, int)):
                return "true" if left < right else "false"
            else:
                self.runtime_error("Operands must be numbers.")
        
        elif expr.operator == '>=':
            if isinstance(left, (float, int)) and isinstance(right, (float, int)):
                return "true" if left >= right else "false"
            else:
                self.runtime_error("Operands must be numbers.")
        
        elif expr.operator == '<=':
            if isinstance(left, (float, int)) and isinstance(right, (float, int)):
                return "true" if left <= right else "false"
            else:
                self.runtime_error("Operands must be numbers.")
        
        elif expr.operator == '==':
            return "true" if left == right else "false"
        
        elif expr.operator == '!=':
            return "true" if left != right else "false"
        
        else:
            self.runtime_error(f"Unexpected binary operator: {expr.operator}")



    def runtime_error(self, message: str) -> None:
        print(message, file=sys.stderr)
        sys.exit(70)
