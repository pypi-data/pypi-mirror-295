from scipy._typing import Untyped
from scipy.fft import fft as fft, ifft as ifft, next_fast_len as next_fast_len

def czt_points(m, w: Untyped | None = None, a: complex = ...) -> Untyped: ...

class CZT:
    def __init__(self, n, m: Untyped | None = None, w: Untyped | None = None, a: complex = ...): ...
    def __call__(self, x, *, axis: int = -1) -> Untyped: ...
    def points(self) -> Untyped: ...

class ZoomFFT(CZT):
    w: Untyped
    a: Untyped
    def __init__(self, n, fn, m: Untyped | None = None, *, fs: int = 2, endpoint: bool = False): ...

def czt(x, m: Untyped | None = None, w: Untyped | None = None, a: complex = ..., *, axis: int = -1) -> Untyped: ...
def zoom_fft(x, fn, m: Untyped | None = None, *, fs: int = 2, endpoint: bool = False, axis: int = -1) -> Untyped: ...
