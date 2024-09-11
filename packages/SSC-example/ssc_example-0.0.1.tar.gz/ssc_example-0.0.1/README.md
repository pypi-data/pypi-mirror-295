# Welcome to SSC-example

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/PierreGratier/SSC-example/ci.yml?branch=main)](https://github.com/PierreGratier/SSC-example/actions/workflows/ci.yml)
[![Documentation Status](https://readthedocs.org/projects/SSC-example/badge/)](https://SSC-example.readthedocs.io/)
[![codecov](https://codecov.io/gh/PierreGratier/SSC-example/branch/main/graph/badge.svg)](https://codecov.io/gh/PierreGratier/SSC-example)

## Installation

The Python package `SSC_example` can be installed from PyPI:

```
python -m pip install SSC_example
```

## Development installation

If you want to contribute to the development of `SSC_example`, we recommend
the following editable installation from this repository:

```
git clone git@github.com-PierreGratier:PierreGratier/SSC-example.git
cd SSC-example
python -m pip install --editable .[tests]
```

Having done so, the test suite can be run using `pytest`:

```
python -m pytest
```

## Acknowledgments

This repository was set up using the [SSC Cookiecutter for Python Packages](https://github.com/ssciwr/cookiecutter-python-package).
