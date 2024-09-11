# AI-eXtended Design (AIXD)

## Introduction

In the current repository we collect the code for the general methodology for AI-augmented generative design. This methodology allows to invert the standard paradigm of parametric modelling, where the designer needs to tweak and tune the input parameters, iteratively or through trial and error, for achieving some desired performance values. 

Instead, this method allows to, by just specifying the requirements' values, obtain a range of designs that closely approximate those. Besides, the present methodology allows the user to explore the design space, understand how different parameters relate to each other, areas of feasible and unfeasible designs, etc.

## Documentation

A detailed documentation of the ``aixd`` library is provided [here](https://docs.gramaziokohler.arch.ethz.ch/aixd/docs/). The documentation includes detailed installation instructions, API references, a user guide, application examples and more.

## Installation

#### Requirements:

- Python >= 3.9

#### Latest stable version
Install `aixd` using `pip`
```
pip install aixd
```

Install `aixd` using `conda`:
```
conda install -c conda-forge aixd
```

**Note**: It is recommended to use virtual environments to manage the dependencies of your projects. If you are using 
`conda`, you can create a new environment with `conda create -n myproject python=3.9` and then activate it with
`conda activate myproject` before installing `aixd`.

#### Latest unstable version

Install the latest version using `pip` from the git repository:
```
pip install --upgrade git+https://gitlab.renkulab.io/ai-augmented-design/aixd.git
```

## Development

If you are going to develop on this repository, perform an installation from source:

```
git clone https://gitlab.renkulab.io/ai-augmented-design/aixd.git
cd aixd
```

Then, install using conda, to install all the dependencies into a new environment called `aixd`:
```
conda env create -f environment.yml
```

Or using pip:
```
pip install -e ".[examples, dev]"
```

Check the [contribution guidelines](CONTRIBUTING.md) for more details.

## Folders and structure

The structure we follow on the current repo is as follows:

* `examples` : all example applications of the `aixd` toolbox
* `src` : for all source code. It can be structure following the next structures
    * `src/aixd` : source code of `aixd` toolbox

## Known issues

* Plotly image export can cause a hang of the system. This is due to a bug in Kaleido (the library
  used by Plotly for image export) reported in [here](https://github.com/plotly/Kaleido/issues/134). A workaround is to
  downgrade Kaleido to version `0.1.0.post1`, which can be done by running `pip install kaleido==0.1.0.post1`. 

