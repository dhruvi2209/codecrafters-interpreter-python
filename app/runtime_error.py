class RuntimeError(Exception):
    def __init__(self, operator, message):
        super().__init__(message)
        self.operator = operator
