from collections.abc import Sequence
from typing import Any, TypeAlias

import numpy as np
import numpy.typing as npt

__all__ = ["Rotation", "Slerp"]

_IntegerType: TypeAlias = int | np.integer[Any]

class Rotation:
    def __init__(self, quat: npt.ArrayLike, normalize: bool = ..., copy: bool = ...) -> None: ...
    @property
    def single(self) -> bool: ...
    def __len__(self) -> int: ...
    @classmethod
    def from_quat(cls, quat: npt.ArrayLike, *, scalar_first: bool = ...) -> Rotation: ...
    @classmethod
    def from_matrix(cls, matrix: npt.ArrayLike) -> Rotation: ...
    @classmethod
    def from_rotvec(cls, rotvec: npt.ArrayLike, degrees: bool = ...) -> Rotation: ...
    @classmethod
    def from_euler(cls, seq: str, angles: float | npt.ArrayLike, degrees: bool = ...) -> Rotation: ...
    @classmethod
    def from_davenport(cls, axes: npt.ArrayLike, order: str, angles: float | npt.ArrayLike, degrees: bool = ...) -> Rotation: ...
    @classmethod
    def from_mrp(cls, mrp: npt.ArrayLike) -> Rotation: ...
    def as_quat(self, canonical: bool = ..., *, scalar_first: bool = ...) -> npt.NDArray[np.float64]: ...
    def as_matrix(self) -> npt.NDArray[np.float64]: ...
    def as_rotvec(self, degrees: bool = ...) -> npt.NDArray[np.float64]: ...
    def as_euler(self, seq: str, degrees: bool = ...) -> npt.NDArray[np.float64]: ...
    def as_davenport(self, axes: npt.ArrayLike, order: str, degrees: bool = ...) -> npt.NDArray[np.float64]: ...
    def as_mrp(self) -> npt.NDArray[np.float64]: ...
    @classmethod
    def concatenate(cls, rotations: Sequence[Rotation]) -> Rotation: ...
    def apply(self, vectors: npt.ArrayLike, inverse: bool = ...) -> npt.NDArray[np.float64]: ...
    def __mul__(self, other: Rotation) -> Rotation: ...
    def __pow__(self, n: float, modulus: int | None) -> Rotation: ...
    def inv(self) -> Rotation: ...
    def magnitude(self) -> npt.NDArray[np.float64] | float: ...
    def approx_equal(self, other: Rotation, atol: float | None, degrees: bool = ...) -> npt.NDArray[np.bool_] | bool: ...
    def mean(self, weights: npt.ArrayLike | None = ...) -> Rotation: ...
    def reduce(
        self,
        left: Rotation | None = ...,
        right: Rotation | None = ...,
        return_indices: bool = ...,
    ) -> Rotation | tuple[Rotation, npt.NDArray[np.float64], npt.NDArray[np.float64]]: ...
    @classmethod
    def create_group(cls, group: str, axis: str = ...) -> Rotation: ...
    def __getitem__(self, indexer: int | slice | npt.ArrayLike) -> Rotation: ...
    @classmethod
    def identity(cls, num: int | None = ...) -> Rotation: ...
    @classmethod
    def random(
        cls,
        num: int | None = ...,
        random_state: _IntegerType | np.random.Generator | np.random.RandomState | None = ...,
    ) -> Rotation: ...
    @classmethod
    def align_vectors(
        cls,
        a: npt.ArrayLike,
        b: npt.ArrayLike,
        weights: npt.ArrayLike | None = ...,
        return_sensitivity: bool = ...,
    ) -> tuple[Rotation, float] | tuple[Rotation, float, npt.NDArray[np.float64]]: ...

class Slerp:
    times: npt.NDArray[Any]
    timedelta: npt.NDArray[Any]
    rotations: Rotation
    rotvecs: npt.NDArray[np.float64]
    def __init__(self, times: npt.ArrayLike, rotations: Rotation) -> None: ...
    def __call__(self, times: npt.ArrayLike) -> Rotation: ...
