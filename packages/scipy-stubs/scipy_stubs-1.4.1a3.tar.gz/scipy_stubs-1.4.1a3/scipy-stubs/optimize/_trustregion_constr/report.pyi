class ReportBase:
    COLUMN_NAMES: list[str]
    COLUMN_WIDTHS: list[int]
    ITERATION_FORMATS: list[str]
    @classmethod
    def print_header(cls) -> None: ...
    @classmethod
    def print_iteration(cls, *args) -> None: ...
    @classmethod
    def print_footer(cls) -> None: ...

class BasicReport(ReportBase): ...
class SQPReport(ReportBase): ...
class IPReport(ReportBase): ...
