import abc
from typing_extensions import override

from scipy._lib._util import MapWrapper as MapWrapper
from scipy._typing import Untyped

class VertexBase(abc.ABC):
    x: Untyped
    hash: Untyped
    nn: Untyped
    index: Untyped
    def __init__(self, x, nn: Untyped | None = None, index: Untyped | None = None): ...
    x_a: Untyped
    def __getattr__(self, item) -> Untyped: ...
    @abc.abstractmethod
    def connect(self, v) -> Untyped: ...
    @abc.abstractmethod
    def disconnect(self, v) -> Untyped: ...
    st: Untyped
    def star(self) -> Untyped: ...

class VertexScalarField(VertexBase):
    check_min: bool
    check_max: bool
    def __init__(
        self,
        x,
        field: Untyped | None = None,
        nn: Untyped | None = None,
        index: Untyped | None = None,
        field_args=(),
        g_cons: Untyped | None = None,
        g_cons_args=(),
    ): ...
    @override
    def connect(self, v) -> Untyped: ...
    @override
    def disconnect(self, v) -> Untyped: ...
    def minimiser(self) -> Untyped: ...
    def maximiser(self) -> Untyped: ...

class VertexVectorField(VertexBase, metaclass=abc.ABCMeta):
    def __init__(
        self,
        x,
        sfield: Untyped | None = None,
        vfield: Untyped | None = None,
        field_args=(),
        vfield_args=(),
        g_cons: Untyped | None = None,
        g_cons_args=(),
        nn: Untyped | None = None,
        index: Untyped | None = None,
    ): ...

class VertexCacheBase:
    cache: Untyped
    nfev: int
    index: int
    def __init__(self) -> None: ...
    def __iter__(self) -> Untyped: ...
    def size(self) -> Untyped: ...
    def print_out(self): ...

class VertexCube(VertexBase):
    def __init__(self, x, nn: Untyped | None = None, index: Untyped | None = None): ...
    @override
    def connect(self, v) -> Untyped: ...
    @override
    def disconnect(self, v) -> Untyped: ...

class VertexCacheIndex(VertexCacheBase):
    Vertex: Untyped
    def __init__(self) -> None: ...
    def __getitem__(self, x, nn: Untyped | None = None) -> Untyped: ...

class VertexCacheField(VertexCacheBase):
    index: int
    Vertex: Untyped
    field: Untyped
    field_args: Untyped
    wfield: Untyped
    g_cons: Untyped
    g_cons_args: Untyped
    wgcons: Untyped
    gpool: Untyped
    fpool: Untyped
    sfc_lock: bool
    workers: Untyped
    process_gpool: Untyped
    process_fpool: Untyped
    def __init__(
        self, field: Untyped | None = None, field_args=(), g_cons: Untyped | None = None, g_cons_args=(), workers: int = 1
    ): ...
    def __getitem__(self, x, nn: Untyped | None = None) -> Untyped: ...
    def process_pools(self): ...
    def feasibility_check(self, v): ...
    def compute_sfield(self, v): ...
    def proc_gpool(self): ...
    def pproc_gpool(self): ...
    def proc_fpool_g(self): ...
    def proc_fpool_nog(self): ...
    def pproc_fpool_g(self): ...
    def pproc_fpool_nog(self): ...
    def proc_minimisers(self): ...

class ConstraintWrapper:
    g_cons: Untyped
    g_cons_args: Untyped
    def __init__(self, g_cons, g_cons_args) -> None: ...
    def gcons(self, v_x_a) -> Untyped: ...

class FieldWrapper:
    field: Untyped
    field_args: Untyped
    def __init__(self, field, field_args) -> None: ...
    def func(self, v_x_a) -> Untyped: ...
