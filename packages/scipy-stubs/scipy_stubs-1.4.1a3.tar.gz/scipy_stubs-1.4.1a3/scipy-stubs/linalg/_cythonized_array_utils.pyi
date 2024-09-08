from typing import TypeAlias

import numpy as np
import numpy.typing as npt

__all__ = ["bandwidth", "ishermitian", "issymmetric"]

# see `scipy/linalg/_cythonized_array_utils.pxd`
_Numeric: TypeAlias = (
    np.int8
    | np.int16
    | np.int32
    | np.int64
    | np.uint8
    | np.uint16
    | np.uint32
    | np.uint64
    | np.float32
    | np.float64
    | np.longdouble
    | np.complex64
    | np.complex128
)

def bandwidth(a: npt.NDArray[_Numeric]) -> tuple[int, int]: ...
def issymmetric(a: npt.NDArray[_Numeric], atol: float | None = None, rtol: float | None = None) -> bool: ...
def ishermitian(a: npt.NDArray[_Numeric], atol: float | None = None, rtol: float | None = None) -> bool: ...
