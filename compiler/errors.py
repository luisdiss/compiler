from typing import NamedTuple, Optional, List


class SourcePos(NamedTuple):
    line: int
    col: int

    def __str__(self) -> str:
        return f"line {self.line}, col {self.col}"


class CompilerError(Exception):
    def __init__(self, message: str, pos: Optional[SourcePos] = None) -> None:
        self.pos = pos
        loc = f" ({pos})" if pos else ""
        super().__init__(f"{message}{loc}")


class LexError(CompilerError):
    pass


class ParseError(CompilerError):
    pass


class SemanticError(CompilerError):
    pass


class CompilationFailed(Exception):
    def __init__(self, errors: List[CompilerError]) -> None:
        self.errors = errors
        msgs = "\n".join(str(e) for e in errors)
        super().__init__(f"Compilation failed with {len(errors)} error(s):\n{msgs}")
