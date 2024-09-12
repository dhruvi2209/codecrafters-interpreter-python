class RuntimeError(Exception):
    def __init__(self, token, message):
        super().__init__(message)
        self.token = token  # Token provides the line number and other details

    def __str__(self):
        return f"[line {self.token.line}] Error: {self.message}"
