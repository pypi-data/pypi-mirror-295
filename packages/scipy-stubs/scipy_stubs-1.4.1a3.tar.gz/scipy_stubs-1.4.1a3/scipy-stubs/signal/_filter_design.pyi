import numpy as np
from scipy._lib._util import float_factorial as float_factorial
from scipy._typing import Untyped
from scipy.special import comb as comb

class BadCoefficients(UserWarning): ...

abs = np.absolute

def findfreqs(num, den, N, kind: str = "ba") -> Untyped: ...
def freqs(b, a, worN: int = 200, plot: Untyped | None = None) -> Untyped: ...
def freqs_zpk(z, p, k, worN: int = 200) -> Untyped: ...
def freqz(
    b, a: int = 1, worN: int = 512, whole: bool = False, plot: Untyped | None = None, fs=..., include_nyquist: bool = False
) -> Untyped: ...
def freqz_zpk(z, p, k, worN: int = 512, whole: bool = False, fs=...) -> Untyped: ...
def group_delay(system, w: int = 512, whole: bool = False, fs=...) -> Untyped: ...
def sosfreqz(sos, worN: int = 512, whole: bool = False, fs=...) -> Untyped: ...
def tf2zpk(b, a) -> Untyped: ...
def zpk2tf(z, p, k) -> Untyped: ...
def tf2sos(b, a, pairing: Untyped | None = None, *, analog: bool = False) -> Untyped: ...
def sos2tf(sos) -> Untyped: ...
def sos2zpk(sos) -> Untyped: ...
def zpk2sos(z, p, k, pairing: Untyped | None = None, *, analog: bool = False) -> Untyped: ...
def normalize(b, a) -> Untyped: ...
def lp2lp(b, a, wo: float = 1.0) -> Untyped: ...
def lp2hp(b, a, wo: float = 1.0) -> Untyped: ...
def lp2bp(b, a, wo: float = 1.0, bw: float = 1.0) -> Untyped: ...
def lp2bs(b, a, wo: float = 1.0, bw: float = 1.0) -> Untyped: ...
def bilinear(b, a, fs: float = 1.0) -> Untyped: ...
def iirdesign(
    wp, ws, gpass, gstop, analog: bool = False, ftype: str = "ellip", output: str = "ba", fs: Untyped | None = None
) -> Untyped: ...
def iirfilter(
    N,
    Wn,
    rp: Untyped | None = None,
    rs: Untyped | None = None,
    btype: str = "band",
    analog: bool = False,
    ftype: str = "butter",
    output: str = "ba",
    fs: Untyped | None = None,
) -> Untyped: ...
def bilinear_zpk(z, p, k, fs) -> Untyped: ...
def lp2lp_zpk(z, p, k, wo: float = 1.0) -> Untyped: ...
def lp2hp_zpk(z, p, k, wo: float = 1.0) -> Untyped: ...
def lp2bp_zpk(z, p, k, wo: float = 1.0, bw: float = 1.0) -> Untyped: ...
def lp2bs_zpk(z, p, k, wo: float = 1.0, bw: float = 1.0) -> Untyped: ...
def butter(N, Wn, btype: str = "low", analog: bool = False, output: str = "ba", fs: Untyped | None = None) -> Untyped: ...
def cheby1(N, rp, Wn, btype: str = "low", analog: bool = False, output: str = "ba", fs: Untyped | None = None) -> Untyped: ...
def cheby2(N, rs, Wn, btype: str = "low", analog: bool = False, output: str = "ba", fs: Untyped | None = None) -> Untyped: ...
def ellip(N, rp, rs, Wn, btype: str = "low", analog: bool = False, output: str = "ba", fs: Untyped | None = None) -> Untyped: ...
def bessel(
    N, Wn, btype: str = "low", analog: bool = False, output: str = "ba", norm: str = "phase", fs: Untyped | None = None
) -> Untyped: ...
def maxflat(): ...
def yulewalk(): ...
def band_stop_obj(wp, ind, passb, stopb, gpass, gstop, type) -> Untyped: ...
def buttord(wp, ws, gpass, gstop, analog: bool = False, fs: Untyped | None = None) -> Untyped: ...
def cheb1ord(wp, ws, gpass, gstop, analog: bool = False, fs: Untyped | None = None) -> Untyped: ...
def cheb2ord(wp, ws, gpass, gstop, analog: bool = False, fs: Untyped | None = None) -> Untyped: ...
def ellipord(wp, ws, gpass, gstop, analog: bool = False, fs: Untyped | None = None) -> Untyped: ...
def buttap(N) -> Untyped: ...
def cheb1ap(N, rp) -> Untyped: ...
def cheb2ap(N, rs) -> Untyped: ...

EPSILON: float

def ellipap(N, rp, rs) -> Untyped: ...
def besselap(N, norm: str = "phase") -> Untyped: ...
def iirnotch(w0, Q, fs: float = 2.0) -> Untyped: ...
def iirpeak(w0, Q, fs: float = 2.0) -> Untyped: ...
def iircomb(w0, Q, ftype: str = "notch", fs: float = 2.0, *, pass_zero: bool = False) -> Untyped: ...
def gammatone(
    freq, ftype, order: Untyped | None = None, numtaps: Untyped | None = None, fs: Untyped | None = None
) -> Untyped: ...

filter_dict: Untyped
band_dict: Untyped
bessel_norms: Untyped
