import click as _click

from ..notebooks import launch_jupyter_example

"""
CLI to run an examples jupyter notebook
"""

@_click.command()
@_click.argument("n", type=int)
def run_example(n):
    """Run a MERPH jupyter notebook example.

    n is the example number; choices are 1"""

    _click.echo(f"Running MERPH Example {n}")

    launch_jupyter_example(n)
