class ParsingError(Exception):
    def __init__(self, line: int | None, error: str) -> None:
        self.line = line
        self.error = error
        msg = error if line is None else f"Line {line}: {error}"
        super().__init__(msg)


class MapError(Exception):
    def __init__(self, error: str) -> None:
        self.error = error
        super().__init__(error)
