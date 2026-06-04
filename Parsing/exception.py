class ParsingError(Exception):
    def __init__(self, line: int | None, error: str):
        self.line = line
        self.error = error
        msg = error if line is None else f"Line {line}: {error}"
        super().__init__(msg)
