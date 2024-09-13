import math as _math
import numpy as _np
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Any, Optional
    import numpy.typing as _npt


def isnumber(x: 'Any') -> 'bool':
    """
    Test whether argument is a number

    :param x: input to check
    :type x: Any
    :return: True if can be cast to float, False otherwise
    :rtype: bool
    """    
    try:
        float(x)
        return True
    except:
        return False


def sci_string(
    val: '_np.float64',
    precision: 'Optional[int]' = 1,
    start_sci: 'int' = 1,
    latex: 'bool' = False
) -> 'str':
    """
    Generate a string representation of a float point number in scientific notation a x 10^b.

    :param val: number to represent as string
    :type val: numpy.float64
    :param precision: number of digits of the mantissa a, defaults to 1
    :type precision: Optional[int], optional
    :param start_sci: do not convert to scientific notation if |b|<start_sci, defaults to 1
    :type start_sci: int, optional
    :param latex: use latex strings?, defaults to False
    :type latex: bool, optional
    :return: string representation of float
    :rtype: str
    """    

    if _np.isnan(val):
        return 'NaN'

    f_e = int(_np.floor(_np.log10(val)))
    f_m = val / (10**f_e)

    if precision is not None:
        if _np.abs(f_e) <= start_sci:
            f_str = "{mantissa:.{precision}f}".format(mantissa=val, precision=precision)
        else:
            if latex:
                f_str = r"${mantissa:.{precision}f} \times 10^{{{exponent:d}}}$".format(
                    mantissa=f_m, precision=precision, exponent=f_e)
            else:
                f_str = (
                    "{mantissa:.{precision}f} \u00D7 10<sup>{exponent:d}</sup>".format(
                        mantissa=f_m, exponent=f_e, precision=precision
                    )
                )
    else:
        if _np.abs(f_e) <= start_sci:
            f_str = "{mantissa:f}".format(mantissa=val)
        else:
            if latex:
                f_str = r"${mantissa:f} \times 10^{{{exponent:d}}}$".format(
                    mantissa=f_m, exponent=f_e
                )
            else:
                f_str = "{mantissa:f} \u00D7 10<sup>{exponent:d}</sup>".format(
                    mantissa=f_m, exponent=f_e
                )

    return f_str


def float_string(f: '_np.float64', precision: 'Optional[int]'=1) -> 'str':
    """
    Generate a string representation of a floating point number

    :param f: number to represent as string
    :type f: numpy.float64
    :param precision: number of digits, defaults to 1
    :type precision: Optional[int], optional
    :return: string representation of float
    :rtype: str
    """    
    if _np.isnan(f):
        return "NaN"

    if precision is not None:
        f_str = "{val:.{precision}f}".format(val=f, precision=precision)
    else:
        f_str = "{val:f}".format(val=f)

    return f_str


def nice_round_up(val: '_np.float64', mag: 'Optional[int]' = None) -> '_np.float64':
    """
    Rounds up a number to a nice value of the form a*10^b for integer a and b

    :param val: the number to round
    :type val: numpy.float64
    :param mag: the value of the exponent b, defaults to None
    :type mag: Optional[int], optional
    :return: rounded up number
    :rtype: numpy.float64
    """    
    if mag is None:
        base = 10 ** int(_math.floor(_np.log10(val)))
    else:
        base = 10 ** mag
    return _np.float64(_math.ceil(val / base) * base)


def nice_round_down(val: '_np.float64', mag: 'Optional[int]' = None) -> '_np.float64':
    """
    Rounds down a number to a nice value of the form a*10^b for integer a and b.

    :param val: the number to round
    :type val: numpy.float64
    :param mag: the value of the exponent b, defaults to None
    :type mag: Optional[int], optional
    :return: rounded down number
    :rtype: numpy.float64
    """    
    if _np.isclose(val, 0.0):
        return _np.float64(0.0)
    if mag is None:
        expn = int(_math.floor(_np.log10(_np.abs(val))))
    else:
        expn = mag
    base = 10**expn
    if expn < 0:
        fval = _math.floor(val / base) / (10 ** (-expn))
    else:
        fval = _math.floor(val / base) * (10 ** (expn))

    return fval


def nice_round_nearest(val: '_np.float64', mag: 'Optional[int]' = None) -> '_np.float64':
    """
    Rounds a number to a nearest number of form a*10^b for integer a and b

    :param val: the number to round
    :type val: numpy.float64
    :param mag: the value of the exponent b, defaults to None
    :type mag: Optional[int], optional
    :return: rounded number
    :rtype: numpy.float64
    """
    val_down = nice_round_down(val, mag)
    val_up = nice_round_up(val, mag)

    val_round = _np.array([val_down, val_up])

    i = _np.abs(val_round - val).argmin()

    return val_round[i]


def log_levels(vmin: '_np.float64', vmax: '_np.float64') -> '_npt.NDArray[_np.float64]':
    """
    Generate sequence of nice logarithmically spaced values between vmin and vmax

    :param vmin: lower bound
    :type vmin: numpy.float64
    :param vmax: upper bound
    :type vmax: numpy.float64
    :raises ValueError: if vmin >= vmax
    :return: array of logarithmically spaced values
    :rtype: _npt.NDArray[.float64]
    """    

    if (vmin >= vmax):
        raise ValueError(f"must have vmin < vmax, received vmin = {vmin} and vmax={vmax}")
    
    mag_low = _math.floor(_np.log10(_np.abs(vmin)))
    mag_high = _math.floor(_np.log10(_np.abs(vmax)))

    if vmin<0:
        vals = _np.arange(-9,10)
    else:
        vals = _np.arange(1, 10)
    levels = []
    for mag in range(mag_low, mag_high + 1):
        levels.append(vals * 10**mag)

    levels = _np.asarray(levels).flatten()

    levels = _np.unique(levels)

    return levels[(levels >= vmin) & (levels <= vmax)]


def log_steps(vmin: '_np.float64',
              vmax: '_np.float64',
              step: '_np.float64'=_np.float64(10.0),
              include_max: 'bool'=True
              ) -> '_npt.NDArray[_np.float64]':
    """
    Generate a sequence of values between vmin and vmax, incremented by the multiplicative factor step

    :param vmin: lower bound
    :type vmin: numpy.float64
    :param vmax: upper bound
    :type vmax: numpy.float64
    :param step: multiplicative factor, defaults to numpy.float64(10.0)
    :type step: numpy.float64, optional
    :param include_max: should output included vmax, even if it does not fit the pattern?, defaults to True
    :type include_max: bool, optional
    :raises ValueError: if vmin < 0
    :raises ValueError: if vmin >= vmax
    :raises ValueError: if step < 1
    :return: array of values
    :rtype: NDArray[numpy.float64]
    """    
    if vmin <= 0:
        raise ValueError(f"vmin must be positive, received {vmin}")
    
    if (vmin >= vmax):
        raise ValueError(f"must have vmin < vmax, received vmin = {vmin} and vmax={vmax}")
    
    if (step<1):
        raise ValueError(f"must have step>=1, received {step}")
    
    levels = []
    this_level = vmin
    while this_level < vmax:
        levels.append(this_level)
        this_level *= step

    if include_max:
        if vmax not in levels:
            levels.append(vmax)

    levels = _np.asarray(levels).flatten()

    return levels


def lin_steps(
    vmin: '_np.float64',
    vmax: '_np.float64',
    step: '_np.float64' = _np.float64(1.0),
    include_endpoints: 'bool' = True,
) -> '_npt.NDArray[_np.float64]':
    """
    Generate a sequence of nice linearly separated values vmin and vmax, with increment step , optionally including end-point.
    Example: if step = 10 vmin=15 and vmax=50, rather than having numpy.arange(15,50,10) = [15, 25, 35, 45], we have
    lin_steps(15,50,step=10) = [15., 20., 30., 40., 50.]

    :param vmin: lower bound
    :type vmin: numpy.float64
    :param vmax: upper bound
    :type vmax: numpy.float64
    :param step: increment, defaults to numpy.float64(1.0)
    :type step: numpy.float64, optional
    :param include_endpoints: should lower and upper bounds be part of the set?, defaults to True
    :type include_endpoints: bool, optional
    :return: array of separated values
    :rtype: NDArray[numpy.float64]
    """
    
    direction = int(_np.sign((vmax-vmin)/step))

    step_mag = _np.log10(_np.abs(step))

    if direction == -1:
        start = vmax
        stop = vmin
    else:
        start = vmin
        stop = vmax

    levels = [_np.float64(start)]
    this_level = start
    while this_level < stop:
        this_level += step
        if this_level < stop:
            levels.append(nice_round_nearest(this_level, mag=step_mag))

    if include_endpoints:
        if start not in levels:
            levels.append(start)
        if stop not in levels:
            levels.append(stop)

    levels = _np.atleast_1d(levels)
    levels = _np.unique(levels)
    levels = _np.sort(levels)

    return levels