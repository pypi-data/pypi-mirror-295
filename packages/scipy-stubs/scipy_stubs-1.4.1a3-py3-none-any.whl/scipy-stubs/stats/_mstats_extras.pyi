from scipy._typing import Untyped
from scipy.stats.distributions import beta as beta, binom as binom, norm as norm, t as t

def hdquantiles(data, prob=(0.25, 0.5, 0.75), axis: Untyped | None = None, var: bool = False) -> Untyped: ...
def hdmedian(data, axis: int = -1, var: bool = False) -> Untyped: ...
def hdquantiles_sd(data, prob=(0.25, 0.5, 0.75), axis: Untyped | None = None) -> Untyped: ...
def trimmed_mean_ci(
    data, limits=(0.2, 0.2), inclusive=(True, True), alpha: float = 0.05, axis: Untyped | None = None
) -> Untyped: ...
def mjci(data, prob=(0.25, 0.5, 0.75), axis: Untyped | None = None) -> Untyped: ...
def mquantiles_cimj(data, prob=(0.25, 0.5, 0.75), alpha: float = 0.05, axis: Untyped | None = None) -> Untyped: ...
def median_cihs(data, alpha: float = 0.05, axis: Untyped | None = None) -> Untyped: ...
def compare_medians_ms(group_1, group_2, axis: Untyped | None = None) -> Untyped: ...
def idealfourths(data, axis: Untyped | None = None) -> Untyped: ...
def rsh(data, points: Untyped | None = None) -> Untyped: ...
