# MERPH #

Bayesian methods for inferring mass eruption rate from column height (or vice versa) for volcanic eruptions

### Introduction ###

*MERPH* uses Bayesian methods to explore the relationship between the mass eruption rate (Q) of a volcanic eruption and the height reached by the volcanic eruption column (H) that is produced.

The mass eruption rate is a quantity that is very important in volcanology and in the dispersion of volcanic ash in the atmosphere, but it is very difficult to measure directly.

Often the mass eruption rate is inferred from observations of the height of the volcanic eruption column, since the eruption column is often much easier to measure.  The eruption column height is linked to the mass eruption rate through the fluid dynamics of turbulent buoyant plumes, but there are often external volcanological and atmospheric effects that contribute and complicate the relationship.

Datasets of the mass eruption rate and eruption column height have been compiled and used to determine an empirical relationship these quantities, using linear regression.  This has then been used to infer the mass eruption rate from the plume height.

*MERPH* goes further, by using Bayesian methods to perform the regression.  Bayesian methods:
* allow us to incorporate a range of *uncertainties* quantitatively into our model;
* provide a meaningful quantitative comparison of different models.

### Main Features ###

*MERPH* is a python package containing MER--Plume height data sets:
     * Sparks
     * Mastin
     * Aubry
     * IVESPA

and tools to perform Bayesian linear regression of the data and posterior prediction.

The package also contains

* example jupyter notebooks to illustrate the use

* a command line interface to perform regression and posterior predicition

---

### Install ###

*MERPH* can be installed from pypi using pip.

It is recommended to create a virtual environment, e.g. with Anaconda/Miniconda (`conda create --name merph "python=3.11"`), and install in the environment.

#### Basic, light-weight set up ####
The basic modules (with no notebooks or app interface) can be installed with `pip install merph`

#### Other features ####
Install with example notebooks using `pip install merph[nb]`

---

### How to use ###

I recommend looking first at the notebook examples, which show how the *MERPH* module can be used.  After installing, the examples can be launched using the command line interface:
`merph-example 1` and `merph-example 2`.

The command `merph` launches a command line interface for basic use.

---

### Dependencies ###

#### Basic, light-weight set up ####
* matplotlib>=3.7.1
* numpy>=1.24.2
* pandas>=1.4.1
* scipy>=1.8.0
* click>=4.0

#### Other features ####

##### Notebooks #####
* notebook

---

### Contacts ###

Mark J. Woodhouse
<mark.woodhouse@bristol.ac.uk>

#### Repository ####
https://bitbucket.org/markwoodhouse/merph

