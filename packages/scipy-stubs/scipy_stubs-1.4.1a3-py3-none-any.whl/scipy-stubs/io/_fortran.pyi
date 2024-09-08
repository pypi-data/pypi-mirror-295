from types import TracebackType

from scipy._typing import Untyped

class FortranEOFError(TypeError, OSError): ...
class FortranFormattingError(TypeError, OSError): ...

class FortranFile:
    def __init__(self, filename, mode: str = "r", header_dtype=...): ...
    def write_record(self, *items): ...
    def read_record(self, *dtypes, **kwargs) -> Untyped: ...
    def read_ints(self, dtype: str = "i4") -> Untyped: ...
    def read_reals(self, dtype: str = "f8") -> Untyped: ...
    def close(self): ...
    def __enter__(self) -> Untyped: ...
    def __exit__(self, type: type[BaseException] | None, value: BaseException | None, tb: TracebackType | None): ...
