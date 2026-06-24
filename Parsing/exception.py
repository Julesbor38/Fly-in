class ParsingError(Exception):
    """If we find an Error in the map . txxt raise a
    specific error no know which line failed"""
    def __init__(self,  line: int | None, error: str) -> None:
        self.line = line
        self.error = error
        msg = error if line is None else f"Line {line}: {error}"
        super().__init__(msg)


class MapError(Exception):
    def __init__(self, error: str) -> None:
        """with a valid Parsing, raise Error if we don't
        find any connextion between start and goal"""
        self.error = error
        super().__init__(error)
