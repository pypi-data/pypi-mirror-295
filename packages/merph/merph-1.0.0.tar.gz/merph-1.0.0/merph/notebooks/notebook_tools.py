import os as _os
import subprocess as _subprocess

from pkg_resources import resource_filename as _resource_filename

"""
Tools to launch jupyter notebooks

:raises FileExistsError: if notebook files are not found
:raises ModuleNotFoundError: if jupyter notebook app not found
:raises ValueError: if ide of notebook does not exist
"""

def run_notebook(file: str):
    """
    Run a jupyter notebook

    :param file: path to notebook file
    :type file: str
    :raises FileExistsError: if file not found
    """    
    if not _os.path.exists(file):
        raise FileExistsError(f"notebook file {file} not found")
    child = _subprocess.Popen([f"jupyter notebook {file}"], shell=True)
    _ = child.communicate()[0]
    rc = child.returncode
    if rc > 0:
        raise ModuleNotFoundError(f"jupyter not found.\nTry 'pip install merph[nb]'")


def launch_jupyter_example(id: int):
    """
    Launch a jupyter notebook example

    :param id: id of notebook
    :type id: int
    :raises ValueError: if id of notebook does not exist
    """    
    notebooks = [1, 2]
    if id not in notebooks:
        raise ValueError(f"merph_example{id}.ipynb does not exist; allowed values are {notebooks}")
    file = _resource_filename(__name__, f"/merph_example{id}.ipynb")
    run_notebook(file)
