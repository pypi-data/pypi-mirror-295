# import numbers
from __future__ import annotations

import warnings as _warnings
from typing import TYPE_CHECKING as _TYPE_CHECKING

if _TYPE_CHECKING:
    from typing import IO, Optional

import matplotlib as mpl
import matplotlib.figure
import matplotlib.pyplot
import matplotlib.pyplot as plt
import numpy as _np
import numpy.typing as npt
import pandas as pd
from matplotlib import is_interactive
from matplotlib.colors import LogNorm
from mpl_toolkits.axes_grid1.axes_divider import make_axes_locatable
from pkg_resources import resource_stream
from scipy.stats import invgamma, multivariate_normal, t
from scipy.stats._distn_infrastructure import rv_continuous_frozen

from merph.utilities.number_tools import (nice_round_down, nice_round_up,
                                          sci_string)
from merph.utilities.plot_tools import plotTitle


class PosteriorPredictivePlot:
    """
    Class to create plots of the posterior predictive distributions
    """

    _pred: PosteriorPredictive
    _logscale: bool

    _xvar: str
    _yvar: str
    _xvar_unit: str
    _yvar_unit: str

    def __init__(self, pred: PosteriorPredictive):
        """
        Constructor

        :param pred: Instance of a PosteriorPredictive class, containing data and parameters
        :type pred: PosteriorPredictive
        """
        self._pred = pred
        self._logscale = pred._logscale

        self._xvar = pred._xvar
        self._yvar = pred._yvar
        self._xvar_unit = pred._xvar_unit
        self._yvar_unit = pred._yvar_unit


    def pdf(self) -> tuple[matplotlib.figure.Figure, plt.Axes]:
        """
        Plot posterior predictive probability density functions

        :return: (fig, ax)
        :rtype: tuple[matplotlib.figure.Figure, plt.Axes]
        """        
        logscale = self._logscale
        ylow = nice_round_down(self._pred.ppf(1e-4).min())
        yhigh = nice_round_up(self._pred.ppf(1-1e-4).max())
        if logscale:
            y = _np.linspace(ylow, yhigh, 1000)
        else:
            y = _np.logspace(_np.log10(ylow), _np.log10(yhigh), 1000)
        
        obs_label = f'$\\log {self._xvar}$' if logscale else f'${self._xvar}$'
        xlabel = f'$\\log {self._yvar}$' if logscale else f'${self._yvar}$ ({self._yvar_unit})'
        ylabel = f'posterior predictive density '
        ylabel += f'p(log {self._yvar} | log {self._xvar})' if logscale else f'p({self._yvar} | {self._xvar})'

        fig, ax = plt.subplots()
        pdf = self._pred.pdf(y)
        for j, obs in enumerate(self._pred.obs):
            this_label = f'{obs_label} = {obs}'
            if not logscale:
                this_label += f' {self._pred._xvar_unit}'
            ax.plot(y,pdf[j,:], label=this_label)
        ax.legend()
        if not logscale:
            ax.set_xscale('log')
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        if not is_interactive():
            fig.show()

        return fig, ax
    
    def cdf(self) -> tuple[matplotlib.figure.Figure, plt.Axes]:
        """
        Plot posterior predictive cumulative density functions

        :return: (fig, ax)
        :rtype: tuple[matplotlib.figure.Figure, plt.Axes]
        """    
        logscale = self._logscale
        ylow = nice_round_down(self._pred.ppf(1e-4).min())
        yhigh = nice_round_up(self._pred.ppf(1-1e-4).max())
        if logscale:
            y = _np.linspace(ylow, yhigh, 1000, dtype=_np.float64)
        else:
            y = _np.logspace(_np.log10(ylow), _np.log10(yhigh), 1000, dtype=_np.float64)

        obs_label = f'$\\log {self._xvar}$' if logscale else f'{self._xvar}'
        xlabel = f'$\\log {self._yvar}$' if logscale else f'{self._yvar} ({self._yvar_unit})'
        ylabel = f'posterior predictive cumulative distribution '
        ylabel += f'P(log {self._yvar} | log {self._xvar})' if logscale else f'P({self._yvar} | {self._xvar})'

        fig, ax = plt.subplots()
        cdf = self._pred.cdf(y)
        for j, obs in enumerate(self._pred.obs):
            this_label = f'{obs_label} = {obs}'
            if not logscale:
                this_label += f' {self._xvar_unit}'
            ax.plot(y,cdf[j,:], label=this_label)
        ax.legend()
        if not logscale:
            ax.set_xscale('log')
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        if not is_interactive():
            fig.show()

        return fig, ax
    

    def ppf(self) -> tuple[matplotlib.figure.Figure, plt.Axes]:
        """
        Plot posterior predictive probability point functions

        :return: (fig, ax)
        :rtype: tuple[matplotlib.figure.Figure, plt.Axes]
        """    
        logscale = self._logscale
        p = _np.linspace(0, 1, 1000)
        
        obs_label = f'$\\log {self._xvar}$' if logscale else f'{self._xvar}'
        ylabel = f'$\\log {self._yvar}$' if logscale else f'{self._yvar} ({self._yvar_unit})'
        xlabel = f'probability'

        fig, ax = plt.subplots()
        y = self._pred.ppf(p)
        for j, obs in enumerate(self._pred.obs):
            this_label = f'{obs_label} = {obs}'
            if not logscale:
                this_label += f' {self._xvar_unit}'
            ax.plot(p,y[j,:], label=this_label)
        ax.legend()
        if not logscale:
            ax.set_yscale('log')
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        if not is_interactive():
            fig.show()

        return fig, ax


    def dist(self,
        *,
        pscale: Optional[str] = "linear",
        yscale: Optional[str] = "log",
        N: Optional[int] = 200,
        ylow: Optional[_np.float64] = None,
        yhigh: Optional[_np.float64] = None,
    ) -> tuple[matplotlib.figure.Figure, plt.Axes]:
        """
        Plot posterior predictive probability and cumulative density functions

        :param pscale: choice of probability density scale ("linear" or "log"), defaults to "linear"
        :type pscale: Optional[str], optional
        :param yscale: choice of scale for response variable ("linear" or "log"), defaults to "log"
        :type xscale: Optional[str], optional
        :param N: number of points on curves, defaults to 200
        :type xscale: Optional[int], optional
        :param ylow: lower bound for response variable, defaults to None
        :type ylow: Optional[_np.float64], optional
        :param yhigh: upper bound for response variable, defaults to None
        :type yhigh: Optional[_np.float64], optional
        :raises ValueError: if pscale not either 'linear' or 'log'
        :raises ValueError: if yscale not either 'linear' or 'log'
        :return: fig, ax
        :rtype: tuple[matplotlib.figure.Figure, plt.Axes]
        """        
        scale_allowed = {"linear", "log"}
        if pscale not in scale_allowed:
            raise ValueError(
                f"plot_distribution: pscale must be one of {scale_allowed}; received {pscale}"
            )
        if yscale not in scale_allowed:
            raise ValueError(
                f"plot_distribution: xscale must be one of {scale_allowed}; received {yscale}"
            )

        if ylow is None:
            if self._logscale:
                ylow = _np.float64(0.0) if self._yvar == "H" else _np.float64(3.0)
            else:
                ylow = _np.float64(1.0) if self._yvar == "H" else _np.float64(1.0e3)
                    
        if yhigh is None:
            if self._logscale:
                yhigh = _np.log10(20.0) if self._yvar == "H" else _np.float64(12.0)
            else:
                yhigh = _np.float64(20.0) if self._yvar == "H" else _np.float64(1.0e12)

        yp: npt.NDArray[_np.float64]
        if self._logscale:
            yp = _np.linspace(ylow, yhigh, N, dtype=_np.float64)  # type: ignore
        else:
            yp = _np.logspace(_np.log10(ylow), _np.log10(yhigh), N, dtype=_np.float64)  # type: ignore
        pdf = self._pred.pdf(yp=yp)
        cdf = self._pred.cdf(yp=yp)

        if self._logscale:
            varlabel = lambda x: f"$\\log {self._yvar}\\left|\\right.\\log {self._xvar} = {x}$"
        else:
            varlabel = lambda x: f"${self._yvar}\\left|\\right.{self._xvar} = {x}$ ({self._xvar_unit})"
            
        ypfig, ax1 = plt.subplots()
        ax2 = ax1.twinx()
        cmap = mpl.colormaps["tab10"].resampled(self._pred.obs.size+1)
        for j, obs in enumerate(self._pred.obs):
            ax1.plot(yp, pdf[j,:], '-', color=cmap(j), label=f"{varlabel(obs)}")
            ax2.plot(yp, cdf[j,:], '--', color=cmap(j))
            ax1.set_ylabel("PDF")
            ax2.set_ylabel("CDF")
        ax1.legend()
        if (not self._logscale) and self._yvar=='Q':
            ax1.set_xscale('log')
        if pscale=="log":
            ax1.set_yscale('log')
        if yscale=="log":
            ax1.set_xscale('log')
        if yscale=="linear":
            ax1.set_xscale('linear')
        ax2.set_ylim(0., 1.)
        ax2.set_yscale('linear')
            
        title = plotTitle(
                f"Posterior predictive distributions for ${self._yvar}\\left|\\right.{self._xvar}$"
        )
            
        plt.suptitle(title)
        if not is_interactive():
            ypfig.show()
        
        return ypfig, ax1


class PosteriorPredictive:
    """
    Class to access posterior predictive distributions and related quantities
    """

    _xvar: str
    _yvar: str
    _xvar_unit: str 
    _yvar_unit: str 
    _logscale: bool

    _obs: npt.NDArray[_np.float64]

    _loc: npt.NDArray[_np.float64]
    _scale: npt.NDArray[_np.float64]
    _ppd: list[rv_continuous_frozen]

    def __init__(self, parent: Merph, obs: npt.ArrayLike, logscale: bool = False):
        """
        Constructor for PosteriorPredictive subclass of Merph class

        :param parent: Merph object that contains data and MLE parameters
        :type parent: Merph
        :param obs: Array of observations
        :type obs: npt.ArrayLike
        :param logscale: is input/output in logarithmic scale?, defaults to False
        :type logscale: bool, optional
        """        
        parent._check_vars_set()

        self._xvar = parent.xvar
        self._yvar = parent.yvar
        self._xvar_unit = parent.xvar_unit
        self._yvar_unit = parent.yvar_unit
        self._logscale = logscale

        self._obs = _np.atleast_1d(obs)

        if logscale:
            self._xp = self._obs
        else:
            self._xp = _np.log10(self._obs, dtype=_np.float64)
        self._N = self._obs.size

        Xp = _np.ones([self._N, 2], dtype=_np.float64)
        Xp[:, 1] = self._xp

        mu = _np.matmul(Xp, parent.posterior.beta_vec)
        Id = _np.identity(self._N, dtype=_np.float64)
        Sigma2 = parent.posterior.sigma2 * (Id + _np.matmul(_np.matmul(Xp, parent.posterior._matV), Xp.T))

        self._loc = mu
        self._scale = _np.sqrt(_np.diag(Sigma2))

        self._ppd = []
        for j in range(self._N):
            this_t = t(parent._dof, loc=self._loc[j], scale=self._scale[j])
            self._ppd.append(this_t) # type: ignore


    @property
    def obs(self) -> npt.NDArray[_np.float64]:
        """
        Get observations

        :return: array of observations
        :rtype: npt.NDArray[_np.float64]
        """        
        return self._obs
    

    @property
    def loc(self) -> npt.NDArray[_np.float64]:
        """
        Get location parameter for posterior predictive distribution

        :return: array of location parameters, one for each observation
        :rtype: npt.NDArray[_np.float64]
        """        
        return self._loc
    

    @property
    def scale(self) -> npt.NDArray[_np.float64]:
        """
        Get scale parameter for posterior predictive distribution

        :return: array of scale parameters, one for each observation
        :rtype: npt.NDArray[_np.float64]
        """   
        return self._scale
    

    @property
    def ppd(self) -> list[rv_continuous_frozen]:
        """
        Get posterior predictive distributions

        :return: List of posterior predictive distributions, one for each observation
        :rtype: list[rv_continuous_frozen]
        """   
        return self._ppd
    

    @property
    def plot(self) -> PosteriorPredictivePlot:
        """
        Instantiate PosteriorPredictivePlot class

        :return: PosteriorPredictivePlot class
        :rtype: PosteriorPredictivePlot
        """        
        return PosteriorPredictivePlot(self)


    def rvs(self, size: int=1) -> npt.NDArray[_np.float64]:
        """
        Random sample from the posterior predictive distribution

        :param size: number of samples to draw, defaults to 1
        :type size: int, optional
        :return: array of posterior predictive samples
        :rtype: npt.NDArray[_np.float64]
        """        
        rvs = _np.empty([self._N, size], dtype=_np.float64)
        for j in range(self._N):
            rvs[j,:] = self._ppd[j].rvs(size)

        if not self._logscale:
            rvs = _np.power(10., rvs)
        return rvs


    def pdf(self, yp: npt.ArrayLike) -> npt.NDArray[_np.float64]:
        """
        Posterior predictive probability density at yp

        :param yp: array of points
        :type yp: npt.ArrayLike
        :return: 2d-array of posterior probability densities, ordered as [obs.size, yp.size]
        :rtype: npt.NDArray[_np.float64]
        """        
        yp = _np.atleast_1d(yp)
        pz = _np.empty([self._N, yp.size], dtype=_np.float64)
        
        if self._logscale:
            norm = _np.float64(1.0)
            pdf_arg = yp
        else:
            norm = yp * _np.log10(10., dtype=_np.float64)
            pdf_arg = _np.log10(yp, dtype=_np.float64)

        for j in range(self._N):
            pz[j,:] = self._ppd[j].pdf(pdf_arg) / norm
        
        return pz
    

    def logpdf(self, yp: npt.ArrayLike) -> npt.NDArray[_np.float64]:
        """
        Logarithm of posterior predictive probability density at yp

        :param yp: array of points
        :type yp: npt.ArrayLike
        :return: 2d-array of log posterior probability densities, ordered as [obs.size, yp.size]
        :rtype: npt.NDArray[_np.float64]
        """        
        yp = _np.atleast_1d(yp)
        logyp = _np.log10(yp, dtype=_np.float64)
        log10 = _np.log(10., dtype=_np.float64)
        logpz = _np.empty([self._N, yp.size], dtype=_np.float64)

        if self._logscale:
            offset = _np.float64(0.0)
            pdf_arg = yp
        else:
            offset = logyp*log10 * _np.log(log10)
            pdf_arg = logyp

        for j in range(self._N):
            logpz[j,:] = self._ppd[j].logpdf(pdf_arg) - offset
        
        return logpz


    def cdf(self, yp: npt.ArrayLike) -> npt.NDArray[_np.float64]:
        """
        Posterior predictive cumulative density at yp

        :param yp: array of points
        :type yp: npt.ArrayLike
        :return: 2d-array of posterior predictive cumulative densities, ordered as [obs.size, yp.size]
        :rtype: npt.NDArray[_np.float64]
        """   
        yp = _np.atleast_1d(yp)
        cz = _np.empty([self._N, yp.size], dtype=_np.float64)
        if self._logscale:
            cdf_arg = yp
        else:
            cdf_arg = _np.log10(yp, dtype=_np.float64)

        for j in range(self._N):
            cz[j,:] = self._ppd[j].cdf(cdf_arg)
        
        return cz


    def logcdf(self, yp: npt.ArrayLike) -> npt.NDArray[_np.float64]:
        """
        Log posterior predictive cumulative density at yp

        :param yp: array of points
        :type yp: npt.ArrayLike
        :return: 2d-array of log posterior predictive cumulative densities, ordered as [obs.size, yp.size]
        :rtype: npt.NDArray[_np.float64]
        """   
        yp = _np.atleast_1d(yp)
        logcz = _np.empty([self._N, yp.size], dtype=_np.float64)
        if self._logscale:
            cdf_arg = yp
        else:
            cdf_arg = _np.log10(yp, dtype=_np.float64)

        for j in range(self._N):
            logcz[j,:] = self._ppd[j].logcdf(cdf_arg)
            
        return logcz


    def sf(self, yp: npt.ArrayLike) -> npt.NDArray[_np.float64]:
        """
        Survival function (1 - cdf) of the posterior predictive distribution evaluated at yp

        :param yp: array of points
        :type yp: npt.ArrayLike
        :return: 2d-array of survival function, ordered as [obs.size, yp.size]
        :rtype: npt.NDArray[_np.float64]
        """   
        yp = _np.atleast_1d(yp)
        sf = _np.empty([self._N, yp.size], dtype=_np.float64)
        if self._logscale:
            sf_arg = yp
        else:
            sf_arg = _np.log10(yp, dtype=_np.float64)
        
        for j in range(self._N):
            sf[j,:] = self._ppd[j].sf(sf_arg)
            
        return sf


    def logsf(self, yp: npt.ArrayLike) -> npt.NDArray[_np.float64]:
        """
        Log survival function (1 - cdf) of the posterior predictive distribution evaluated at yp

        :param yp: array of points
        :type yp: npt.ArrayLike
        :return: 2d-array of log survival function, ordered as [obs.size, yp.size]
        :rtype: npt.NDArray[_np.float64]
        """   
        yp = _np.atleast_1d(yp)
        logsf = _np.empty([self._N, yp.size], dtype=_np.float64)
        if self._logscale:
            sf_arg = yp
        else:
            sf_arg = _np.log10(yp, dtype=_np.float64)

        for j in range(self._N):
            logsf[j,:] = self._ppd[j].logsf(sf_arg)
        
        return logsf


    def ppf(self, q: npt.ArrayLike) -> npt.NDArray[_np.float64]:
        """
        Percent point function (inverse of cdf) of the posterior predictive distribution evaluated at q

        :param q: array of probabilities
        :type yp: npt.ArrayLike
        :return: 2d-array of output values, ordered as [obs.size, q.size]
        :rtype: npt.NDArray[_np.float64]
        """  
        q = _np.atleast_1d(q)
        ppf = _np.empty([self._N, q.size], dtype=_np.float64)
        for j in range(self._N):
            ppf[j,:] = self._ppd[j].ppf(q)

        if not self._logscale:
            ppf = _np.power(10., ppf)

        return ppf


    def isf(self, q: npt.ArrayLike) -> npt.NDArray[_np.float64]:
        """
        Inverse survival function (inverse of sf) of the posterior predictive distribution evaluated at q

        :param q: array of probabilities
        :type yp: npt.ArrayLike
        :return: 2d-array of output values, ordered as [obs.size, q.size]
        :rtype: npt.NDArray[_np.float64]
        """  
        q = _np.atleast_1d(q)
        isf = _np.empty([self._N, q.size], dtype=_np.float64)
        for j in range(self._N):
            isf[j,:] = self._ppd[j].isf(q)

        if not self._logscale:
            isf = _np.power(10., isf)
            
        return isf


    def median(self) -> npt.NDArray[_np.float64]:
        """
        Median of the posterior predictive distribution

        :return: array of the median of the ppd, one for each observation
        :rtype: npt.NDArray[_np.float64]
        """        
        median = _np.empty([self._N], dtype=_np.float64)
        for j in range(self._N):
            median[j] = self._ppd[j].median()

        if not self._logscale:
            median = _np.power(10., median)
                
        return median


    def mean(self) -> npt.NDArray[_np.float64]:
        """
        Mean of the posterior predictive distribution.
        Note this is the mean of the t-distribution (i.e., in log-log space).

        :return: array of the mean of the ppd, one for each observation
        :rtype: npt.NDArray[_np.float64]
        """        
        mean = _np.empty([self._N], dtype=_np.float64)
        for j in range(self._N):
            mean[j] = self._ppd[j].mean()
        return mean  # type: ignore


    def std(self) -> npt.NDArray[_np.float64]:
        """
        Standard deviation of the posterior predictive distribution.
        Note this is the standard deviation of the t-distribution (i.e., in log-log space).

        :return: array of the mean of the ppd, one for each observation
        :rtype: npt.NDArray[_np.float64]
        """        
        std = _np.empty([self._N], dtype=_np.float64)
        for j in range(self._N):
            std[j] = self._ppd[j].std()
        return std

    
    def var(self) -> npt.NDArray[_np.float64]:
        """
        Variance of the posterior predictive distribution.
        Note this is the variance of the t-distribution (i.e., in log-log space).

        :return: array of the mean of the ppd, one for each observation
        :rtype: npt.NDArray[_np.float64]
        """        
        var = _np.empty([self._N], dtype=_np.float64)
        for j in range(self._N):
            var[j] = self._ppd[j].var()
        return var


    def interval(self, confidence: npt.ArrayLike) -> npt.NDArray[_np.float64]:
        """
        Confidence interval with equal areas around the median of the posterior predictive distribution.

        :param confidence: array of probability levels to take
        :type confidence: npt.ArrayLike
        :return: array of credible intervals, ordered as [obs.size, 2, confidence.size]
        :rtype: npt.NDArray[_np.float64]
        """        
        c = _np.atleast_1d(confidence)
        interval = _np.empty([self._N,2,c.size], dtype=_np.float64)
        for j in range(self._N):
            ci = _np.array(self._ppd[j].interval(c))
            interval[j,0,:] = ci[0,:]
            interval[j,1,:] = ci[1,:]

        if not self._logscale:
            interval[:,0,:] = _np.power(10., interval[:,0,:])
            interval[:,1,:] = _np.power(10., interval[:,1,:])
            
        return interval  # type: ignore


    def simulate(self, samples: int, plot: bool = False) -> pd.DataFrame:
        """
        Draw samples from the posterior predictive distribution for each observation, returned as a DataFrame

        :param samples: number of samples
        :type samples: int
        :param plot: plot histograms of samples?, defaults to False
        :type plot: bool, optional
        :return: posterior predictive samples in a DataFrame
        :rtype: pd.DataFrame
        """
        y: npt.NDArray[_np.float64]
        y = self.rvs(samples)
        
        dfs = []
        logy_col = f"log {self._yvar}"
        logx_col = f"log {self._xvar}"
        if self._logscale:
            for j, x in enumerate(self._obs):  # (variable) x: _np.float64

                d = {
                    logy_col : _np.float64(y[j, :]),
                    logx_col : _np.float64(x),
                    self._yvar: _np.float64(_np.power(10, y[j, :])),
                    self._xvar: _np.float64(_np.power(10, x))
                }
                dfs.append(pd.DataFrame(d))
        else:
            for j, x in enumerate(self._obs):  # (variable) x: _np.float64
                d = {
                    logy_col  : _np.log10(_np.float64(y[j, :])),
                    logx_col  : _np.log10(_np.float64(x)),
                    self._yvar : _np.float64(y[j, :]),
                    self._xvar : _np.float64(x)
                }
                dfs.append(pd.DataFrame(d))
        y_df = pd.concat(dfs, ignore_index=True)

        if plot:
            histfig, ax = plt.subplots()

            cmap = mpl.colormaps['tab10'].resampled(len(self._obs)+1)

            for j, obs in enumerate(self._obs):
                yvar = 'log Q' if self._yvar=="Q" else 'H'

                vals = y_df.loc[y_df[self._xvar]==obs, yvar].values # type: ignore
            
                ax.hist(vals, bins='auto', density=True, histtype='step', color=cmap(j), label=obs)
                ax.hist(vals, bins='auto', density=True, histtype='stepfilled', color=cmap(j), alpha=1./len(self._obs))
            
            ax.set_xlabel(f'{yvar} ({self._yvar_unit})')

            ax.set_title(f"Samples from the posterior predictive distribution {self._yvar}|{self._xvar}")

            leg = ax.legend()
            # leg = ax.get_legend()
            leg.set_title(f'{self._xvar} ({self._xvar_unit})')
            if self._yvar=="Q":
                for t in leg.get_texts():
                    val = _np.float64(t.get_text())
                    t.set_text(sci_string(val, latex=True))
            
            if not is_interactive():
                histfig.show()
            
        return y_df


class JointPredictivePlot:
    """
    Class to create plots of the joint predictive distributions
    """
    _joint: JointPredictive
    _xvar: str
    _yvar: str
    _xvar_unit: str
    _yvar_unit: str
    _logscale: bool

    def __init__(self, joint: JointPredictive):
        """
        Constructor for the JointPredictivePlot class

        :param joint: Instance of the JointPredictive class
        :type joint: JointPredictive
        """        
        self._joint = joint
        self._xvar = joint._xvar
        self._yvar = joint._yvar
        self._xvar_unit = joint._xvar_unit
        self._yvar_unit = joint._yvar_unit
        self._logscale = joint._logscale

    
    def pdf(self,nX: int=100, nY: int=100) -> tuple[matplotlib.figure.Figure, dict[str, plt.Axes]]:
        """
        Plot the joint predictive pdf

        :param nX: number of x-points, defaults to 100
        :type nX: int, optional
        :param nY: number of y-points, defaults to 100
        :type nY: int, optional
        :return: (fig, ax)
        :rtype: tuple[matplotlib.figure.Figure, dict[str, plt.Axes]]
        """        
        fx: rv_continuous_frozen
        fx = self._joint._x_dist
        
        xlow = fx.ppf(0)
        if xlow == -_np.inf:
            xlow = fx.ppf(1e-8)

        xhigh = fx.ppf(1)
        if xhigh == _np.inf:
            xhigh = fx.ppf(1-1e-8)
        
        xlow = 0.9*xlow
        xhigh = 1.1*xhigh
        
        if self._logscale:
            x = _np.linspace(xlow, xhigh, nX, dtype=_np.float64)
            if self._yvar == 'Q':
                y = _np.linspace(3, 9, nY, dtype=_np.float64)
            else:
                y = _np.linspace(0, 50, nY, dtype=_np.float64)
        else:
            x = _np.logspace(_np.log10(xlow), _np.log10(xhigh), nX, dtype=_np.float64)
            if self._yvar == 'Q':
                y = _np.logspace(3, 9, nY, dtype=_np.float64)
            else:
                y = _np.logspace(0, _np.log10(50), nY, dtype=_np.float64)

        joint_pdf = self._joint.pdf(x,y)

        axd: dict[plt.text.Text, plt.Axes]

        fig, axd = plt.subplot_mosaic(
            """
            A.
            BC
            """,
            width_ratios=[10,1],
            height_ratios=[1,5],
            layout="constrained")
            
        axd['A'].plot(x,fx.pdf(x))
        if self._logscale:
            jp_plt = axd['B'].contourf(x,y,joint_pdf)
        else:
            jp_plt = axd['B'].contourf(x,y,_np.ma.masked_less(joint_pdf,1e-20), norm=LogNorm())

        if not self._logscale:
            if self._xvar=='Q':
                axd['B'].set_xscale('log')
            else:
                axd['B'].set_yscale('log')
        
        xlabel = f'log {self._xvar}' if self._logscale else f'{self._xvar} ({self._xvar_unit})'
        ylabel = f'log {self._yvar}' if self._logscale else f'{self._yvar} ({self._yvar_unit})'
        pXlabel = f'p(log {self._xvar})' if self._logscale else f'p({self._xvar})'
        plabel = f'p(log {self._xvar}, log {self._yvar})' if self._logscale else f'p({self._xvar}, {self._yvar})'

        axd['B'].set_xlabel(xlabel)
        axd['B'].set_ylabel(ylabel)
        axd['A'].set_ylabel(pXlabel)

        fig.colorbar(jp_plt, cax=axd['C'])
        axd['C'].set_ylabel(plabel)

        if not is_interactive():
            fig.show()

        return fig, axd


class JointPredictive(object):
    """
    A class for accessing the joint posterior predictive distribution
    """
    _xvar: str
    _yvar: str
    _xvar_unit: str
    _yvar_unit: str

    _logscale: bool
    
    _parent: Merph

    _x_dist: rv_continuous_frozen


    def __init__(self, parent: Merph, obs_dist: rv_continuous_frozen, logscale: bool = False):
        """
        Constructor

        :param parent: an instance of the Merph class, containing data, MLE parameters, 
                       and methods for accessing the posterior predictive distribution
        :type parent: Merph
        :param obs_dist: a scipt.stats.rv_continouus_frozen distribution,
                         giving the probability distribution for the observation
        :type obs_dist: rv_continuous_frozen
        :param logscale: is observational distribution on a logarithmic scale?, defaults to False
        :type logscale: bool, optional
        """        
        parent._check_vars_set()

        self._xvar = parent.xvar
        self._yvar = parent.yvar
        self._xvar_unit = parent.xvar_unit
        self._yvar_unit = parent.yvar_unit
        self._logscale = logscale

        self._parent = parent

        self._x_dist = obs_dist    


    def rvs(self, size: int=1) -> npt.NDArray[_np.float64]:
        """
        Random sample from the joint predictive distribution

        :param size: number of samples, defaults to 1
        :type size: int, optional
        :return: array of samples from joint predictive distribution, ordered as [x,y]
        :rtype: npt.NDArray[_np.float64]
        """        
        rvs = _np.empty([2, size], dtype=_np.float64)
        rvs[0,:] = self._x_dist.rvs(size)
        y_pred = self._parent.posterior_predictive(rvs[0,:], logscale=self._logscale)
        rvs[1,:] = y_pred.rvs(1)[:,0]
        return rvs


    def pdf(
        self, xp: npt.ArrayLike, yp: npt.ArrayLike
    ) -> npt.NDArray[_np.float64]:
        """
        Joint probability density function at xp, yp

        :param xp: array of predictions of x
        :type xp: npt.ArrayLike
        :param yp: array of predictions of y
        :type yp: npt.ArrayLike
        :return: _description_
        :rtype: npt.NDArray[_np.float64]
        """        
                
        xp = _np.atleast_1d(xp)
        yp = _np.atleast_1d(yp)

        [X,Y] = _np.meshgrid(xp,yp)
        
        pxy = _np.empty(X.shape, dtype=_np.float64)
        for i in range(X.shape[0]):
            for j in range(X.shape[1]):
                px = self._x_dist.pdf(X[i,j])
                
                y_pred = self._parent.posterior_predictive(X[i,j], logscale=self._logscale)
                py_given_x = y_pred.pdf(Y[i,j])
                pxy[i,j] = px * py_given_x
        
        return pxy


    def simulate(
        self,
        samples: int,
        plot: bool = False,
    ) -> pd.DataFrame:
        """
        Draw samples from the joint posterior predictive distribution,
        returning values as a DataFrame, with optional plotting

        :param samples: number of samples
        :type samples: int
        :param plot: make plots?, defaults to False
        :type plot: bool, optional
        :return: DataFrame containing random draws from the joint posterior predictive distribution
        :rtype: pd.DataFrame
        """        
        
        xy = npt.NDArray[_np.float64]
        logxy = npt.NDArray[_np.float64]
        
        if self._logscale:
            logxy = self.rvs(samples)
            xy = _np.power(10, logxy)
        else:
            xy = self.rvs(samples)
            logxy = _np.log10(xy)
        
        y_df = pd.DataFrame(
            columns=[
                f"log {self._xvar}",
                f"log {self._yvar}",
                self._xvar,
                self._yvar,
            ]
        )

        y_df[f"log {self._xvar}"] = logxy[0,:]
        y_df[f"log {self._yvar}"] = logxy[1,:]
        y_df[self._xvar] = xy[0,:]
        y_df[self._yvar] = xy[1,:]
        
        if plot:


            axd: dict[plt.text.Text, plt.Axes]
            fig, axd = plt.subplot_mosaic(
                """
                A.
                BC
                """,
                width_ratios=[5,1],
                height_ratios=[1,5],
                layout="constrained")

            x_vals = y_df[self._xvar]
            y_vals = y_df[self._yvar]

            x0 = nice_round_down(y_df[self._xvar].min(), mag = 0 if self._xvar=='H' else None)
            x1 = nice_round_up(y_df[self._xvar].max(), mag = 0 if self._xvar=='H' else None)

            y0 = nice_round_down(y_df[self._yvar].min(), mag = 0 if self._xvar=='H' else None)
            y1 = nice_round_up(y_df[self._yvar].max(), mag = 0 if self._xvar=='H' else None)

            axd['B'].scatter(x_vals, y_vals, alpha=0.1)

            if self._xvar=='Q':
                counts, bins = _np.histogram(_np.log10(x_vals),bins='auto')
                axd['A'].stairs(counts, _np.power(10,bins), fill=True, alpha=0.5, orientation='vertical')
                axd['A'].set_xscale('log')
                axd['B'].set_xscale('log')
            else:
                counts, bins = _np.histogram(x_vals,bins='auto')
                axd['A'].stairs(counts, bins, fill=True, alpha=0.5, orientation='vertical')
            if self._yvar=='Q':
                counts, bins = _np.histogram(_np.log10(y_vals),bins='auto')
                axd['C'].stairs(counts, _np.power(10,bins), fill=True, alpha=0.5, orientation='horizontal')
                axd['C'].set_yscale('log')
                axd['B'].set_yscale('log')
            else:
                counts, bins = _np.histogram(y_vals,bins='auto')
                axd['C'].stairs(counts, bins, fill=True, alpha=0.5, orientation='horizontal')

            axd['A'].set_xlim(float(x0), float(x1))
            axd['B'].set_xlim(float(x0), float(x1))
            axd['B'].set_ylim(float(y0), float(y1))
            axd['C'].set_ylim(float(y0), float(y1))

            axd['A'].set_ylabel('Count')
            axd['B'].set_xlabel(f'{self._xvar} ({self._xvar_unit})')
            axd['B'].set_ylabel(f'{self._yvar} ({self._yvar_unit})')
            axd['C'].set_xlabel('Count')

            axd['A'].set_xticklabels([])
            axd['C'].set_yticklabels([])

            fig.suptitle(f"Samples from the joint predictive distribution p({self._xvar},{self._yvar})")

            if not is_interactive():
                plt.show()
            
        return y_df
    

    @property   
    def plot(self):
        """
        Instantiate JointPredictivePlot subclass

        :return: JointPredictivePlot class
        :rtype: JointPredictivePlot
        """     
        return JointPredictivePlot(self)


class Merph(object):
    """
    A class containing eruption source data and methods to perform Bayesian linear regresion.
    """    
    _name: Optional[str]
    _height_column: str
    _mer_column: str
    _height: npt.NDArray[_np.float64]
    _mer: npt.NDArray[_np.float64]
    _data: pd.DataFrame
    _data_columns: list[str]
    _data_units: dict[str, str]

    _size: int
    _n: int
    _dof: int

    _set_vars: bool
    _xvar: str
    _yvar: str
    _xvar_unit: str
    _yvar_unit: str

    _x: npt.NDArray[_np.float64]
    _y: npt.NDArray[_np.float64]
    _matX: npt.NDArray[_np.float64]
    _matV: npt.NDArray[_np.float64]

    def __init__(
        self,
        dataset: pd.DataFrame,
        name: Optional[str] = None,
        Height: str = "H",
        MER: str = "Q",
    ):
        """
        Constructor method

        :param data: DataFrame containing eruption source data as column headed table
        :type data: pd.DataFrame
        :param name: Name of the dataset, defaults to None
        :type name: Optional[str], optional
        :param Height: Header for plume height column, defaults to "H"
        :type Height: str, optional
        :param MER: Header for MER column, defaults to "Q"
        :type MER: str, optional
        :raises RuntimeError: if Height is not found in data table columns
        :raises RuntimeError: if MER is not found in data table columns
        :raises RuntimeError: if data in Height column cannot be converted to _np.float64
        :raises RuntimeError: if data in MER column cannot be converted to _np.float64
        :raises RuntimeError: if length of Height column is not equal to length of MER column
        """ 
        self._name = name

        self.set_data(dataset)

        if Height not in self._data_columns:
            raise RuntimeError(f"Column {Height} not found in data table")
        self._height_column = Height

        if MER not in self._data_columns:
            raise RuntimeError(f"Column {MER} not found in data table")
        self._mer_column = MER

        try:
            self._height = dataset[Height].to_numpy(dtype="float64", copy=True, na_value=_np.nan)
        except:
            raise RuntimeError(f"Unable to read column {Height} as float64")
        try:
            self._mer = dataset[MER].to_numpy(dtype="float", copy=True, na_value=_np.nan)
        except:
            raise RuntimeError(f"Unable to read column {MER} as float64")

        if len(self._height) != len(self._mer):
            raise RuntimeError("In Merph object, the length of Q and H must be equal")

        self._size = len(self._height)

        self._set_vars = False


    def __str__(self):
        """
        __str__ string

        :return: Summary description of the Merph class
        :rtype: str
        """        
        msg: str
        msg = f"Merph object with {self._size} entries"
        return msg
    

    @property
    def name(self) -> str:
        """Get the name of Merph dataset"""
        return self._name or 'No name provided'


    @property
    def height_column(self) -> str:
        """
        Get the height column in the dataset

        :return: height column
        :rtype: str
        """        
        return self._height_column
    

    @property
    def mer_column(self) -> str:
        """
        Get the MER column in the dataset

        :return: mer column
        :rtype: str
        """        
        return self._mer_column


    @property
    def height(self) -> npt.NDArray[_np.float64]:
        """
        Get the height data

        :return: array of height data
        :rtype: npt.NDArray[_np.float64]
        """        
        return self._height


    @property
    def mer(self) -> npt.NDArray[_np.float64]:
        """
        Get the MER data

        :return: MER data
        :rtype: npt.NDArray[_np.float64]
        """        
        return self._mer


    @property
    def data(self) -> pd.DataFrame:
        """
        Get the data

        :return: the dataset
        :rtype: pd.DataFrame
        """        
        return self._data


    @property
    def size(self) -> int:
        """
        Get number of entries in data set

        :return: size of dataset
        :rtype: int
        """        
        return self._size


    @property
    def xvar(self) -> str:
        """
        Get the x-variable (explanatory variable)

        :return: x-variable
        :rtype: str
        :raises RuntimeError: if _set_vars is False
        """
        if not self._set_vars:
            raise RuntimeError("Variables are not set.  First call 'set_vars'")
        return self._xvar
    

    @property
    def yvar(self) -> str:
        """
        Get the y-variable (response variable)

        :return: y-variable
        :rtype: str
        :raises RuntimeError: if _set_vars is False
        """
        if not self._set_vars:
            raise RuntimeError("Variables are not set.  First call 'set_vars'")
        return self._yvar
    

    @property
    def xvar_unit(self) -> str:
        """
        Get the unit of the x-variable (explanatory variable)

        :return: x-variable unit
        :rtype: str
        :raises RuntimeError: if _set_vars is False
        """        
        if not self._set_vars:
            raise RuntimeError("Variables are not set.  First call 'set_vars'")
        return self._xvar_unit
    
    
    def _set_xvar_unit(self, unit: Optional[str]=None):
        """
        Private setter for _xvar_unit

        :param unit: Unit of x-variable, defaults to None
        :type unit: Optional[str], optional

        :raises warning: if unit is not set
        """        
        if unit:
            self._xvar_unit = unit
        else:
            _warnings.warn(f"Unit of {self.xvar} not set.  Add units by calling 'xvar_unit'")
            self._xvar_unit = ''


    @xvar_unit.setter
    def xvar_unit(self, unit: str):
        """
        Public setter for xvar_unit

        :param unit: unit of x-variable
        :type unit: str
        """        
        self._set_xvar_unit(unit)
    

    @property
    def yvar_unit(self) -> str:
        """
        Get the unit of the y-variable (response variable)

        :return: y-variable unit
        :rtype: str
        :raises RuntimeError: if _set_vars is False
        """        
        if not self._set_vars:
            raise RuntimeError("Variables are not set.  First call 'set_vars'")
        return self._yvar_unit


    def _set_yvar_unit(self, unit: Optional[str]=None):
        """
        Private setter for _yvar_unit

        :param unit: Unit of y-variable, defaults to None
        :type unit: Optional[str], optional

        :raises warning: if unit is not set
        """       
        if unit: 
            self._yvar_unit = unit
        else:
            _warnings.warn(f"Unit of {self.yvar} not set.  Add units by calling 'yvar_unit'")
            self._yvar_unit = ''
            

    @yvar_unit.setter
    def yvar_unit(self, unit: str):
        """
        Public setter for yvar_unit

        :param unit: unit of y-variable
        :type unit: str
        """        
        self._set_yvar_unit(unit)


    def set_data(self, dataset: pd.DataFrame):
        """
        Setup the observational data passed as a pandas DataFrame

        :param data: Pandas dataframe containing the data
        :type data: pd.DataFrame
        """
        units: dict[str, str] = {}
        cols: list[str] = []
        data_cols: list[str] = dataset.columns.tolist()
        for col in data_cols:
            if "(" in col:
                name, unit = col.split("(")
                name = name[:-1]
                unit = unit[:-1]
            else:
                name = col
                unit = ''
            units[name] = unit
            cols.append(name)
        if "References" in cols:
            cols.remove("References")
            dataset.drop(["References"], axis=1, inplace=True)  # type: ignore
        if "Comments" in cols:
            cols.remove("Comments")
            dataset.drop(["Comments"], axis=1, inplace=True)  # type: ignore
        if "VEI" in cols:
            dataset["VEI"] = dataset["VEI"].fillna(0).astype(int)
        if "Climate zone" in cols:
            dataset["Climate zone"] = pd.Categorical(
                dataset["Climate zone"],  # type: ignore
                categories=["Cold", "Temperate", "Subtropics", "Tropical"],
            )
        dataset.columns = cols
        self._data = dataset
        self._data_columns = cols
        self._data_units = units


    def _check_vars_set(self):
        """
        Check that _set_vars is True

        :raises RuntimeError: if _set_vars is False
        """        
        if not self._set_vars:
            msg: str
            msg = "Variables are not set.  First run set_vars "
            if self._name:
                msg += f"on {self.name}"
            raise RuntimeError(msg)


    def set_vars(self, xvar: str, yvar: str):
        """
        Specify the observed variable (x-variable) and inferred variable (y-variable)

        :param xvar: The explanatory variable.  Can be "H" for column height. Can be "Q" or "MER" for mass eruption rate.
        :type xvar: str
        :param yvar: The predicted variable.  Can be "H" for column height.  Can be "Q" or "MER" for mass eruption rate.
        :type yvar: str
        :raises ValueError: if xvar is not "H" or "Q" or "MER".
        :raises ValueError: if yvar is not "H" or "Q" or "MER".
        :raises ValueError: if xvar == yvar.
        :raises RuntimeError: if the sizes of the data are not equal
        :raises RuntimeError: if there are not sufficient data points in the data set to make predictions based on the explantory variable.
        """        
        if xvar not in ["H", "Q", "MER"]:
            raise ValueError(f"xvar must be either H or Q or MER, received {xvar}")
        if yvar not in ["H", "Q", "MER"]:
            raise ValueError(f"yvar must be either H or Q or MER, received {yvar}")

        if xvar == yvar:
            raise ValueError(
                f"xvar must not be the same as yvar, received {xvar}, {yvar}"
            )

        self._xvar = xvar
        self._yvar = yvar

        x: npt.NDArray[_np.float64]
        x = _np.log10(self.height) if xvar == "H" else _np.log10(self.mer)
        
        y: npt.NDArray[_np.float64]
        y = _np.log10(self.height) if yvar == "H" else _np.log10(self.mer)

        if xvar == "H":
            self._set_xvar_unit(self._data_units[self._height_column])
            self._set_yvar_unit(self._data_units[self._mer_column])
        else:
            self._set_xvar_unit(self._data_units[self._mer_column])
            self._set_yvar_unit(self._data_units[self._height_column])

        # Cut out NaNs
        x_nans = _np.isnan(x)  # Logical array with True corresponding to NaN
        y_nans = _np.isnan(y)

        x = x[~x_nans & ~y_nans]  # Select values where both x and y are not NaNs
        y = y[~x_nans & ~y_nans]

        self._x = x
        self._y = y

        if x.size != y.size:
            raise RuntimeError(
                f"Data is not properly sized.  _x has size {x.size}, _y has size {y.size}"
            )

        self._set_vars = True

        n = x.size
        self._n = n
        self._dof = n-2

        if self._n <= 2:
            raise RuntimeError("Too little data for statistics")

        self.posterior = self._fit(self)


    def predictive_plot(self)-> tuple[matplotlib.figure.Figure, tuple[plt.Axes,...]]:
        """
        Make a plot of the data, best-fit curve, and posterior predictive intervals

        :return: _description_
        :rtype: tuple[matplotlib.figure.Figure, tuple[plt.Axes,...]]
        """        
        
        if self._xvar=="H":
            xx = _np.linspace(0,_np.log10(50),100, dtype=_np.float64)
        else:
            xx = _np.linspace(2,9,100, dtype=_np.float64)

        ymean = self.posterior.mean(xx, logscale=True)

        pred = self.posterior_predictive(xx, logscale=True)

        alpha = _np.array([1e-5, 1e-4, 1e-3, 1e-2, 0.1, 0.25, 0.5, 0.75, 0.9])

        nints = alpha.size

        tick_locs = (_np.arange(nints) + 0.5) * (nints - 1) / nints
        clabels = alpha

        cmap = mpl.colormaps["YlGnBu"].resampled(nints+1)
        # cmap = color_palette("ch:s=, rot=", nints)
        # sm = LinearSegmentedColormap.from_list("p", cmap, N=nints)

        fig, (ax0, ax1) = plt.subplots(1,2, figsize=(22/2.54, 10/2.54))
        ax_divider = make_axes_locatable(ax1)
        cbar_ax = ax_divider.append_axes("right", size="7%", pad="2%")

        for j,a in enumerate(alpha):
            interval = pred.interval(1-a)
            pup = interval[:,1,:].flatten()
            plw = interval[:,0,:].flatten()
            ax0.fill_between(xx, pup, plw, color=cmap(j), zorder=j-10)
            ax1.fill_between(10**xx, 10**pup, 10**plw, color=cmap(j), zorder=j-10)

        ax0.plot(xx, ymean, 'k-', zorder=1)
        ax0.scatter(self._x, self._y, color='k', zorder=1)
        # ax[0].plot(xx, pred.ppf(0.025),'k--',zorder=1)
        # ax[0].plot(xx, pred.ppf(0.975),'k--',zorder=1)
        # ax[0].plot(xx, y_lw, 'k:', zorder=1)
        # ax[0].plot(xx, y_up, 'k:', zorder=1)

        ax1.plot(10**xx, 10**ymean, 'k-', zorder=1)
        ax1.scatter(10**self._x, 10**self._y, color='k', zorder=1)
        # ax[1].plot(10**xx, 10**pred.ppf(0.025), 'k--', zorder=1)
        # ax[1].plot(10**xx, 10**pred.ppf(0.975), 'k--', zorder=1)
        # ax[1].plot(10**xx, 10**y_lw, 'k:', zorder=1)
        # ax[1].plot(10**xx, 10**y_up, 'k:', zorder=1)

        fig2, ax2 = plt.subplots()
        sc = ax2.scatter(_np.arange(nints), _np.arange(nints), c=_np.arange(nints), cmap=cmap)

        fig.colorbar(sc, cax=cbar_ax)
        cbar_ax.set_yticks(tick_locs)
        cbar_ax.set_yticklabels([sci_string(c, latex=True) for c in clabels])

        ax0.set_xlabel(f'$\\log\\ {self.xvar}$')
        ax0.set_ylabel(f'$\\log\\ {self.yvar}$')

        if self._xvar=="Q":
            ax1.set_xscale('log')
            ax1.set_xlim([1e2, 1e9])
            ax1.set_ylim([0, 50])
        else:
            ax1.set_yscale('log')
            ax1.set_xlim([0, 50])
            ax1.set_ylim([1e2, 1e9])

        ax1.set_xlabel(f'${self._xvar}$')
        ax1.set_ylabel(f'${self._yvar}$')

        cbar_ax.set_ylabel(r'$\alpha$')

        plt.close(fig2)

        fig.suptitle(f"Posterior predictive intervals $P({self._yvar}|{self._xvar}) = 1-\\alpha$")

        plt.tight_layout()
        if not is_interactive():
            fig.show()
        
        return fig, (ax0, ax1)


    class _fit():
        """
        Private subclass that performs maximum likelihood estimation to fit model parameters
        """        
        _n: int
        _dof: int
        _beta_vec: npt.NDArray[_np.float64]
        _intercept: _np.float64
        _slope: _np.float64
        _sigma2: _np.float64
        _residuals: npt.NDArray[_np.float64]

        _xvar: str
        _yvar: str
        _xvar_unit: str
        _yvar_unit: str

        _x: npt.NDArray[_np.float64]
        _y: npt.NDArray[_np.float64]

        _matX: npt.NDArray[_np.float64]
        _matV: npt.NDArray[_np.float64]

        # Maximum likelihood estimate
        def __init__(self, parent: Merph):
            """
            Constructor method for the _fit subclass

            :param parent: Merph class containing data
            :type parent: Merph
            """            
            parent._check_vars_set()

            self.xvar = parent.xvar
            self.yvar = parent.yvar

            self.xvar_unit = parent.xvar_unit
            self.yvar_unit = parent.yvar_unit

            self._x = parent._x
            self._y = parent._y

            self._n = parent._n
            self._dof = parent._dof

            matX = _np.ones([parent._n, 2], dtype=_np.float64)
            matX[:, 1] = parent._x

            self._matX = matX
            self._matV = _np.linalg.inv(_np.matmul(matX.T, matX))

            self._beta_vec = _np.matmul(_np.matmul(self._matV, self._matX.T), parent._y)

            self._intercept = self._beta_vec[0]
            self._slope = self._beta_vec[1]

            a = parent._y - _np.matmul(self._matX, self._beta_vec)
            self._sigma2 = _np.dot(a, a) / float(self._dof)

            self._residuals = parent._y - _np.matmul(self._matX, self._beta_vec)


        @property
        def beta_vec(self) -> npt.NDArray[_np.float64]:
            """
            Get vector [alpha, beta] of MLE parameters for line fit

            :return: 1D array of fit parameters
            :rtype: npt.NDArray[_np.float64]
            """            
            return self._beta_vec
        

        @property
        def sigma2(self) -> _np.float64:
            """
            Get MLE of error variance sigma^2

            :return: error variance sigma^2
            :rtype: _np.float64
            """            
            return self._sigma2
        

        @property
        def intercept(self) -> _np.float64:
            """
            Get MLE of intercept parameter alpha

            :return: intercept parameter alpha
            :rtype: _np.float64
            """        
            return self._intercept


        @property
        def slope(self) -> _np.float64:
            """
            Get MLE of slope parameter beta

            :return: slope parameter beta
            :rtype: _np.float64
            """        
            return self._slope


        @property
        def prefactor(self) -> _np.float64:
            """
            Get MLE of powerlaw prefactor parameter k

            :return: prefactor parameter k
            :rtype: _np.float64
            """        
            return _np.power(10, self._intercept)
        

        @property
        def exponent(self) -> _np.float64:
            """
            Get MLE of powerlaw exponent parameter beta.
            Note, this is the same as slope parameter

            :return: exponent parameter beta
            :rtype: _np.float64
            """        
            return self._slope
        

        @property
        def residuals(self) -> npt.NDArray[_np.float64]:
            """
            Get array of residuals of data from MLE line fit

            :return: array of residuals
            :rtype: npt.NDArray[_np.float64]
            """            
            return self._residuals
        

        @property
        def matX(self) -> npt.NDArray[_np.float64]:
            """
            Get matrix of explanatory variables X = [[1   ... 1]
                                                    [x_1 ... x_n]].T

            :return: matrix of explanatory variables
            :rtype: npt.NDArray[_np.float64]
            """            
            return self._matX
        

        @property
        def matV(self) -> npt.NDArray[_np.float64]:
            """
            Get matrix of (X.T * X)^{-1}

            :return: matrix (X.T * X)^{-1}
            :rtype: npt.NDArray[_np.float64]
            """            
            return self._matV
        

        def mean(self, x: npt.ArrayLike, logscale: bool=False) -> npt.NDArray[_np.float64]:
            """
            Compute the posterior mean y(x).
            If logscale is True then input is log(x) and output is log(y)

            :param x: values of explanatory variable
            :type x: npt.ArrayLike
            :param logscale: is input/output in logarithmic scale?, defaults to False
            :type logscale: bool, optional
            :return: array of values of y evaluated at x
            :rtype: npt.NDArray[_np.float64]
            """            
            x = _np.atleast_1d(x)
            if logscale:
                y = self._intercept + self._slope*x
            else:
                y = self.prefactor * _np.power(x, self.exponent)

            return y


        def rvs(self, size: int = 1) -> pd.DataFrame:
            """
            Draw samples from the posterior distributions for the model parameters.

            :param size: number of samples to draw, defaults to 1
            :type size: int, optional
            :return: dataframe contains samples of the intercept, slope and sigma^2
            :rtype: pd.DataFrame
            """            
            sigma2 = _np.zeros((size,1), dtype=_np.float64)
            beta_v = _np.zeros((size,2), dtype=_np.float64)

            for j in range(size):
                sigma2[j,0] = invgamma(a=self._dof/2, scale=self._dof/2*self._sigma2).rvs(1)
                beta_v[j,:] = multivariate_normal(mean=self._beta_vec, cov=self._matV*sigma2[j,0]).rvs(1)

            df = pd.DataFrame(columns=["intercept", "slope", "sigma^2"], dtype=_np.float64)
            df["intercept"] = beta_v[:,0]
            df["slope"] = beta_v[:,1]
            df["sigma^2"] = sigma2[:,0]

            return df
        

        def mean_interval(self, x: npt.ArrayLike, alpha: npt.ArrayLike, logscale: bool=False) -> npt.NDArray[_np.float64]:
            """
            Get centered credible intervals on the posterior mean at x.

            :param x: values of the explanatory variable
            :type x: npt.ArrayLike
            :param alpha: credible intervals to compute
            :type alpha: npt.ArrayLike
            :param logscale: are values of the input variable on a logarithmic scale?, defaults to False
            :type logscale: bool, optional
            :raises ValueError: if any element of alpha is outside the range 0...1.
            :return: the credible intervals at level alpha evaluated at values x.  This is ordered as intervals[x,upper/low,alpha]
            :rtype: npt.NDArray[_np.float64]
            """            
            
            alpha = _np.atleast_1d(alpha)
            if any(alpha>1) or any(alpha<0):
                raise ValueError("In posterior.mean_interval, alpha values must be in range 0...1")

            x = _np.atleast_1d(x)
            xx = x if logscale else _np.log10(x)
            
            yy = self.mean(xx, logscale=True)

            mean_x = _np.mean(self._x)
            var_x = _np.var(self._x)

            var = self._sigma2/self._n * (1.0 + (xx-mean_x)**2/var_x)

            tdist = t(self._dof, loc=yy, scale=_np.sqrt(var))

            intervals = _np.zeros((x.size,2,alpha.size))
            for j, a in enumerate(alpha):
                ints = tdist.interval(a)
                intervals[:,0,j] = ints[0]
                intervals[:,1,j] = ints[1]

            if not logscale:
                intervals = _np.power(10., intervals)

            return intervals


        def trace(self) -> pd.DataFrame:
            """
            Get a dataframe of x, y, Q, and H from the MLE fit

            :return: DataFrame with columns x, y, Q and H
            :rtype: pd.DataFrame
            """            
            x: npt.NDArray[_np.float64]
            if self.xvar == "H":
                x = _np.linspace(-1, 1.7, num=100, dtype=_np.float64)  # type: ignore
            else:
                x = _np.linspace(-1, 11, num=100, dtype=_np.float64)  # type: ignore

            y = self.mean(x, logscale=True)

            if self.xvar == "H":
                height = _np.power(10, x)
                mer = _np.power(10, y)
            else:
                mer = _np.power(10, x)
                height = _np.power(10, y)

            df = pd.DataFrame(columns=["x", "y", "Q", "H"])

            df["x"] = x
            df["y"] = y
            df["Q"] = mer
            df["H"] = height

            return df
        

        def plot(self, 
                 samples: Optional[int] = None, 
                 interval: Optional[npt.ArrayLike] = None,
                 alpha: float = 0.1,
                 ) -> tuple[matplotlib.figure.Figure, plt.Axes]:
            """
            Create plot of MLE curve fit, (optionally) together with posterior samples and credible interval

            :param samples: number of posterior samples to draw, defaults to None
            :type samples: Optional[int], optional
            :param interval: credible intervals to add, defaults to None
            :type interval: Optional[npt.ArrayLike], optional
            :param alpha: transparency for posterior sample lines, defaults to 0.1
            :type alpha: float
            :raises ValueError: if any values in interval outside range [0, 1]
            :raises ValueError: if alpha outside range (0, 1]
            :return: figure and axes handles
            :rtype: tuple[matplotlib.figure.Figure, plt.Axes]
            """            

            if alpha<=0 or alpha>1:
                raise ValueError(f"alpha must be in range (0,1]")

            if self.xvar == "H":
                x = _np.linspace(0.1, 50, num=100, dtype=_np.float64)
            else:
                x = _np.logspace(1, 11, num=100, dtype=_np.float64)
            
            y = self.mean(x, logscale=False)
            logx = _np.log10(x)

            mlefig, axs = plt.subplots(nrows=1, ncols=2)
            log_ax, ax = axs
            log_ax.scatter(self._x, self._y, c='k', zorder=1)
            log_ax.plot(_np.log10(x), _np.log10(y), 'k', zorder=1)
            
            ax.scatter(_np.power(10, self._x), _np.power(10, self._y), c='k', zorder=1)
            ax.plot(x, y, 'k', zorder=1)
            
            if interval is not None:
                interval = _np.atleast_1d(interval)
                if any(interval)>1 or any(interval)<0:
                    raise ValueError(f"intervals must be in range [0,1]")
                cmap = mpl.colormaps["Dark2"].resampled(interval.size+1)
                ints = self.mean_interval(x, interval, logscale=False)
                int_logplots = []
                int_plots = []
                int_labels = []
                for j, a in enumerate(interval):
                    lower, = log_ax.plot(logx, _np.log10(ints[:,0,j]), linestyle='--', color=cmap(j), zorder=1)
                    log_ax.plot(logx, _np.log10(ints[:,1,j]), linestyle='--', color=cmap(j), zorder=1)
                    int_logplots.append(lower)
                    
                    lower, = ax.plot(x, ints[:,0,j], linestyle='--', color=cmap(j))
                    ax.plot(x, ints[:,1,j], linestyle='--', color=cmap(j))
                    int_plots.append(lower)

                    int_labels.append(f"$\\alpha = {a}$")
                
                log_ax.legend(tuple(int_logplots), tuple(int_labels))
                ax.legend(tuple(int_plots), tuple(int_labels))

            if samples is not None:
                draws = self.rvs(samples)
                for j in range(samples):
                    logy_j = draws.iloc[j]['intercept'] + draws.iloc[j]['slope']*logx
                    log_ax.plot(logx, logy_j, color='lightgray', alpha=alpha, zorder=0)
                    ax.plot(x, _np.power(10., logy_j), color='lightgray', alpha=alpha, zorder=0)

            if self.xvar=="H":
                ax.set_yscale('log')
            else:
                ax.set_xscale('log')

            log_ax.set_xlabel(f"$\\log_{{10}}({self.xvar})$")
            log_ax.set_ylabel(f"$\\log_{{10}}({self.yvar})$")
            ax.set_xlabel(f"{self.xvar} ({self.xvar_unit})")
            ax.set_ylabel(f"{self.yvar} ({self.yvar_unit})")
            title_str = f"Posterior mean for linear trend in log-transformed data"
            if interval is not None:
                title_str += f" with credible intervals"
            title = plotTitle(title_str)
            plt.suptitle(title)
            mlefig.tight_layout(rect=(0, 0.03, 1, 0.95))
            if not is_interactive():
                mlefig.show()

            return mlefig, ax


    def posterior_predictive(self, obs: npt.ArrayLike, logscale: bool = False) -> PosteriorPredictive:
        """
        Initialize posterior predictive class

        :param obs: observations
        :type obs: npt.NDArray[_np.float64]
        :param logscale: are values of the input variable on a logarithmic scale?, defaults to False
        :type logscale: bool, optional
        :return: PosteriorPredictive instance
        :rtype: PosteriorPredictive
        """        
        return PosteriorPredictive(self, obs, logscale)


    def joint_predictive(self, obs_pdf: rv_continuous_frozen, logscale: bool = False) -> JointPredictive:
        """
        Initialize joint predictive class

        :param obs_pdf: scipy.stats._distn_infrastructure.rv_continuous_frozen distribution
        :type obs_pdf: rv_continuous_frozen
        :param logscale: are values of the input variable on a logarithmic scale?, defaults to False
        :type logscale: bool, optional
        :return: JointPredictive instance
        :rtype: JointPredictive
        """        
        return JointPredictive(self, obs_pdf, logscale)


def read_excel(
    xls: IO,
    name: Optional[str] = None,
    Height: str = "H",
    MER: str = "MER",
    skiprows: int = 0,
) -> Merph:
    """
    Read an excel spreadsheet of eruption source parameters into a Merph instance

    :param xls: filename of excel spreadsheet
    :type xls: IO
    :param name: name for dataset, defaults to None
    :type name: Optional[str], optional
    :param Height: column header for plume height, defaults to "H"
    :type Height: str, optional
    :param MER: column header for MER, defaults to "Q"
    :type MER: str, optional
    :param skiprows: number of header rows to skip when reading, defaults to 0
    :type skiprows: int, optional
    :return: instance of Merph class
    :rtype: Merph
    """    
    df = pd.read_excel(xls, skiprows=skiprows)

    return Merph(df, name=name, Height=Height, MER=MER)


def read_csv(
    csv: IO, name: Optional[str] = None, Height: str = "H", MER: str = "Q"
) -> Merph:
    """
    Read an csv file of eruption source parameters into a Merph instance

    :param xls: filename of excel spreadsheet
    :type xls: IO
    :param name: name for dataset, defaults to None
    :type name: Optional[str], optional
    :param Height: column header for plume height, defaults to "H"
    :type Height: str, optional
    :param MER: column header for MER, defaults to "Q"
    :type MER: str, optional
    :param skiprows: number of header rows to skip when reading, defaults to 0
    :type skiprows: int, optional
    :return: instance of Merph class
    :rtype: Merph
    """    
    df = pd.read_csv(csv)

    return Merph(df, name=name, Height=Height, MER=MER)


def load_Aubry() -> Merph:
    """Load Aubry's data to a Merph instance.

    :return: Aubry's data
    :rtype: Merph
    """    
    datastream = resource_stream(__name__, './data/AubryData.csv')

    df = pd.read_csv(datastream)

    df['MER (kg/s)'] = df['Erupted tephra mass (kg)']/(df['Duration (hrs)']*3600.0)

    df['Name'] = df['Volcano'].combine(df['Eruption'], lambda a, b: a + " " + (str(b) or ""))
    df['Eruption'] = df['Volcano'].combine(df['Eruption'], lambda a, b: a + " " + (str(b) or ""))

    Aubry=Merph(df, name='Aubry', MER='MER', Height='Plume height')
    return Aubry


def load_IVESPA() -> Merph:
    """Load IVESPA data to a Merph instance.

    :return: IVESPA data
    :rtype: Merph
    """    
    datastream = resource_stream(__name__, "./data/IVESPAData.csv")

    df = pd.read_csv(datastream, header=[0, 1, 2], dtype=str, na_filter=False)  # type: ignore

    col_types = df.columns.get_level_values(2)  # type: ignore
    df.columns = df.columns.get_level_values(1)  # type: ignore

    for col_name, col_type in zip(df.columns, col_types):  # type: ignore
        try:
            if col_type == "float":
                df[col_name] = df[col_name].replace(["unknown", "Unknown", "na", "NA"], _np.nan)  # type: ignore
                df[col_name] = df[col_name].astype(_np.float64)  # type: ignore
            elif col_type == "int":
                df[col_name] = df[col_name].replace(["unknown", "Unknown", "na", "NA"], -1)  # type: ignore
                df[col_name] = df[col_name].astype(int)  # type: ignore
            elif col_type == "datetime":
                df[col_name] = pd.to_datetime(  # type: ignore
                    df[col_name], format="dd/mm/yyyy hh:mm:ss", errors="coerce"  # type: ignore
                )
        except:
            raise ValueError(
                f"Could not convert type of column {col_name} to type {col_type}.  Column values are: {df[col_name].values}"  # type: ignore
            )

    df["MER (kg/s)"] = df["TEM Best estimate (kg)"] / (
        df["Duration Best estimate (hours)"] * 3600
    )

    df["Plume Height (km a.v.l.)"] = (
        df["Tephra Plume Top Best estimate (km a.s.l.)"]
        - df["Vent altitude (m a.s.l.)"] / 1000.0
    )

    df["Name"] = df["Volcano"].combine(  # type: ignore
        df["Event Name"], lambda a, b: a + " " + (str(b) or "")  # type: ignore
    )
    df["Eruption"] = df["Volcano"].combine(  # type: ignore
        df["Event Name"], lambda a, b: a + " " + (str(b) or "")  # type: ignore
    )

    IVESPA = Merph(df, name="IVESPA", MER="MER", Height="Plume Height")
    return IVESPA


def load_Mastin() -> Merph:
    """Load Mastin's data to a Merph instance.

    :return: Mastin's data
    :rtype: Merph
    """    
    datastream = resource_stream(__name__, "./data/MastinData.csv")

    df = pd.read_csv(datastream)

    return Merph(df,  name="Mastin", MER="MER", Height="Plume height")


def load_Sparks() -> Merph:
    """Load Sparks' data to a Merph instance.

    :return: Sparks' data
    :rtype: Merph
    """    
    datastream = resource_stream(__name__, './data/SparksData.csv')

    df = pd.read_csv(datastream)
    
    return Merph(df, name='Sparks', MER='MER', Height='Plume height')