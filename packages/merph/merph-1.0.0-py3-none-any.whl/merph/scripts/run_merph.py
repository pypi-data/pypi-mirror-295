import ast
import pathlib
import warnings
from typing import Callable, Optional, TypedDict, Union

try:
    from typing import NotRequired
except:
    from typing_extensions import NotRequired

import click
import matplotlib.pyplot as plt
import scipy.stats
from numpy import atleast_1d
from scipy.stats import truncnorm, uniform
from scipy.stats._distn_infrastructure import (rv_continuous_frozen,
                                               rv_discrete_frozen)

import merph

try:
    from merph.notebooks import launch_jupyter_example
except ImportError:
    _has_nb = False
else:
    _has_nb = True

"""
CLI to run MERPH
"""

warnings.filterwarnings("ignore", module=".*merph.*") ## TODO: change to only matplotlib warnings

class PythonLiteralOption(click.Option):
    """
    Coerce click into taking multiple list arguments for lists formatted as strings.

    Taking from accepted answer at
    <https://stackoverflow.com/questions/47631914/how-to-pass-several-list-of-arguments-to-click-option>
    """    
    def type_cast_value(self, ctx, value):
        try:
            return ast.literal_eval(value)
        except:
            raise click.BadParameter(value)


class ObservableValues(click.ParamType):
    """
    Click custom class for input of observations.
    Allows observations to be set as either:
    - single value
    - comma separated list of values
    - a scipy.stats frozen distribution (current uniform and truncnorm)
    """

    name = 'Observation values'

    def convert(self, value, param, ctx):
        """
        converter of command line string.
        Acts as an input validator, returning inputted string is valid,
        failing if not
        """        
        try:
            parse_obs_string(value)
            return value
        except:
            self.fail(f"{value!r} is not a valid observation", param, ctx)
OBS_TYPE = ObservableValues()


class ObsDict(TypedDict):
    dist: str
    value: NotRequired[float | list[float]]
    loc: NotRequired[float]
    scale: NotRequired[float]
    a: NotRequired[float]
    b: NotRequired[float]


class Observations(object):
    """
    Class to contain observations data
    """    
    name: str
    dist: str
    var: str
    value: Optional[Union[float, list[float]]]
    loc: Optional[float]
    scale: Optional[float]
    a: Optional[float]
    b: Optional[float]

    func: dict[str, Callable]

    name = 'Observation'

    def __init__(self, d: ObsDict, var: str) -> None:
        """
        Constructor from ObsDict dictionary

        :param d: A dictionary with observation parameters
        :type d: ObsDict
        :param var: Label of observed variable
        :type var: str
        """        
        self.dist = d['dist']
        self.value = d['value'] if 'value' in d.keys() else None
        self.loc = d['loc'] if 'loc' in d.keys() else None
        self.scale = d['scale'] if 'scale' in d.keys() else None
        self.a = d['a'] if 'a' in d.keys() else None
        self.b = d['b'] if 'b' in d.keys() else None

        self.func = self._type_caller[self.dist](self)

        self.var = var

    # def __call__(self) -> rv_continuous_frozen | rv_discrete_frozen | float | list[float]:
    #     """
    #     __call__ method

    #     :return: _description_
    #     :rtype: _type_
    #     """        
    #     return self.func(self)

    def __str__(self) -> str:
        """
        Print summary

        :return: Summary message
        :rtype: str
        """        
        msg = "observation: "
        fmt = '.2f' if self.var=='H' else '.2e'
        match self.dist:
            case 'uniform':
                msg += f"{self.var} ~ uniform(loc={self.loc:{fmt}}, scale={self.scale:{fmt}})"
            case 'truncnorm':
                msg += f"{self.var} ~ truncnorm(loc={self.loc:{fmt}}, scale={self.scale:{fmt}}, a={self.a:{fmt}}, b={self.b:{fmt}})"
            case 'discrete-single':
                msg += f"H = {self.value:{fmt}}"
            case 'discrete-multi':
                msg += f"H \u220A [" 
                for v in self.value:
                    msg += f"{v:{fmt}},"
                msg = msg[:-1]
                msg += "]"
        return msg
    
    def _uniform(self) -> rv_continuous_frozen | rv_discrete_frozen:
        """
        private method to set uniform distribution

        :return: scipy.stats frozen uniform distribution
        :rtype: rv_continuous_frozen | rv_discrete_frozen
        """        
        return uniform(loc=self.loc, scale=self.scale)

    def _truncnorm(self) -> rv_continuous_frozen | rv_discrete_frozen:
        """
        private method to set truncated normal distribution

        :return: scipy.stats frozen truncnorm distribution
        :rtype: rv_continuous_frozen | rv_discrete_frozen
        """        
        return truncnorm(loc=self.loc, scale=self.scale, a=self.a, b=self.b)
    
    def _discrete_single(self) -> float:
        """
        private method to set single discrete observation

        :return: observation value
        :rtype: float
        """        
        if self.value is None:
            raise RuntimeError(f"value not set in Observations")
        return self.value
    
    def _discrete_multi(self) -> list[float]:
        """
        _summary_

        :raises RuntimeError: if value is not set
        :return: observed values
        :rtype: list[float]
        """        
        if self.value is None:
            raise RuntimeError(f"value not set in Observations")
        return self.value
    

    _type_caller = {
        "uniform": _uniform,
        "truncnorm": _truncnorm,
        "discrete-single": _discrete_single,
        "discrete-multi": _discrete_multi,
    }
    

def parse_obs_string(value: str) -> ObsDict:
    """
    Parse an observation provided as a string into a ObsDict

    :param value: _description_
    :type value: str
    :raises ValueError: if values in string cannot be parsed
    :return: a dictionary of observation parameters
    :rtype: ObsDict
    """    
    if "uniform" in value:
        try:
            range_str = value[value.find("(") + 1 : value.find(")")]
            loc, scale = range_str.split(",")
            if "loc" in loc:
                loc = loc.split('=')[1]
            if "scale" in scale:
                scale = scale.split('=')[1]
            loc = float(loc)
            scale = float(scale)
            return {"dist":"uniform", "loc": loc, "scale": scale}
        except:
            raise ValueError(f"{value!r} is not a value obs string")
    elif "truncnorm" in value:
        try:
            param_str = value[value.find("(") + 1 : value.find(")")]
            loc, scale, p1, p2 = param_str.split(",")
            if "loc" in loc:
                loc = loc.split('=')[1]
            loc = float(loc)
            if "scale" in scale:
                scale = scale.split('=')[1]
            scale = float(scale)
            if "lower" in p1:
                lower = p1.split('=')[1]
                lower = float(lower)
                a = (lower - loc) / scale
            elif "a" in p1:
                a = p1.split('=')[1]
                a = float(a)
            else:
                a = float(p1)
            if "upper" in p2:
                upper = p2.split('=')[1]
                upper = float(upper)
                b = (upper - loc) / scale
            elif "b" in p2:
                b = p2.split('=')[1]
                b = float(b)
            else:
                b = float(p2)
            return {"dist":"truncnorm", "loc":loc, "scale":scale, "a":a, "b": b}
        except:
            raise ValueError(f"{value!r} is not a value obs string")
    elif "," in value:
        try:
            valuelist = [float(v) for v in value.split(",")]
            return {"dist":"discrete-multi", "value":valuelist}
        except:
            raise ValueError(f"{value!r} is not a value obs string")
    else:
        try:
            value_float = float(value)
            return {"dist":"discrete-single", "value":value_float}
        except:
            raise ValueError(f"{value!r} is not a value obs string")

def header():
    click.secho("""
                 
           ++++++     
         ++++++++++    __  ______________  _____  _    _ 
           ++++++     |  \/    ____   __ \|  __ \| |  | |
            ++÷÷      | \  /  |__  | |__)   |__)   |__| |
             ++       | |\/|   __| |  _  /|  ___/|  __  |
             /\       | |  |  |____| | \ \| |    | |  | |
            /  \      |_|  |_________|  \___|    |_|  |_|
           /    \ 
        """, fg=206)
    click.secho(f"Version {merph.__version__}", fg=98)
    click.secho(f"\u00a9 Mark J. Woodhouse, University of Bristol, 2024", fg=98)


def run_example(ctx, param, value):
    """Run a MERPH jupyter notebook example.

    value is the example number; choices are 1, 2"""

    if not _has_nb:
        raise ImportError("notebook has dependencies, try: pip install merph[nb]")

    if not value or ctx.resilient_parsing:
        return

    if value not in ["1", "2"]:
        return

    header()
    msg = "Running MERPH Example " + value
    click.echo(msg)

    launch_jupyter_example(int(value))
    ctx.exit()
                                             
@click.command()
@click.option(
    "-data",
    "--dataset",
    type=click.Choice(["Mastin", "Sparks", "Aubry", "IVESPA"], case_sensitive=False),
    prompt="Select dataset",
    required=True,
)
@click.option(
    "-x",
    "--xvar",
    type=click.Choice(["H", "Q", "MER"], case_sensitive=False),
    prompt="Set observed variable",
    help="Set observed variable",
    required=True,
)
@click.option(
    "-obs",
    "--observation",
    default='10.0',
    prompt="Set observations (e.g. '10.0,' or '10., 15.' or 'uniform(loc=10,scale=5)')",
    type=OBS_TYPE,
    help="Set observations as discrete values or from a [uniform/truncnorm] distribution using scipy.stats specification.  For multiple discrete values, quoted strings are needed",
    required=True,
)
@click.option(
    "-s",
    "--samples",
    type=int,
    default=1000,
    prompt="Set number of samples to draw from the posterior predictive distribution",
    help="Number of samples to draw from the posterior predictive distribution",
)
@click.option(
    "-o",
    "--out",
    type=str,
    prompt="Filename to save (in CSV format)",
    help="Filename to save (in CSV format)",
    default = '',
    required=False,
    prompt_required=False,
)
@click.option(
    "--example",
    prompt=False,
    type=click.Choice(["1", "2"]),
    default=None,
    callback=run_example,
    expose_value=True,
    is_eager=True,
    help="Launch a jupyter notebook containing an example"
)
@click.version_option()
def run_merph(
    dataset: str, xvar: str, observation: str, samples: int, out: Optional[str]=None, example: Optional[int]=None,
) -> None:
    """
    Run MERPH from the command line.

    Example: run merph with Mastin's dataset for an observation H=10 km, drawing 500 samples
    
    \b
    merph --dataset Mastin --xvar H --obs 10 --samples 500

    Example: run merph with the IVESPA dataset for an uncertain observation with a uniform distribution for 10 < H < 15 km, drawing 1000 samples,
    and saving results to merph_ex2.txt

    \b
    merph --dataset IVESPA --xvar H --obs "uniform(10,5)" --samples 1000 -o merph_ex2.txt

    \f
    :param dataset: choice of dataset
    :type dataset: str
    :param xvar: explanatory variable that is observed
    :type xvar: str
    :param observation: observed values selection
    :type observation: str
    :param samples: number of samples to draw
    :type samples: int
    :param out: filename for output
    :type out: Optional[str], optional
    :type example: Optional[int], optional
    :raises ValueError: if dataset is not one of known datasets
    """    
    
    header()

    datasets = {"Mastin","Sparks","Aubry","IVESPA"}

    if dataset not in datasets:
        raise ValueError(f"Dataset {dataset} not recognized.  Available datasets are {datasets}.")
    
    obs = Observations(parse_obs_string(observation),xvar)

    if xvar == "H":
        yvar = "Q"
    else:
        yvar = "H"

    click.echo(f"Running MERPH with dataset {dataset} for {yvar}|{xvar} \n and {obs}")

    match dataset:
        case 'Aubry':
            data = merph.load_Aubry()
        case 'IVESPA':
            data = merph.load_IVESPA()
        case 'Mastin':
            data = merph.load_Mastin()
        case 'Sparks':
            data = merph.load_Sparks()

    data.set_vars(xvar=xvar, yvar=yvar)  # sets independent and variables

    data.posterior.plot()  # maximum likelihood estimator (Mastin curve)

    data.predictive_plot()

    match obs.dist:
        case "uniform" | "truncnorm":
            df = data.joint_predictive(obs.func).simulate(samples, plot=True)
        case "discrete-single" | "discrete-multi":
            df = data.posterior_predictive(obs.value).simulate(samples, plot=True)

    if out:
        outname = pathlib.Path(out).stem + '.csv'
        df.to_csv(outname, index=False)
    
    plt.show()
