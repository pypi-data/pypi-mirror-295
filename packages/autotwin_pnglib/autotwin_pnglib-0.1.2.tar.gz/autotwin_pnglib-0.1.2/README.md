[![PyPI - License](https://img.shields.io/pypi/l/autotwin_pnglib)](https://github.com/AutotwinEU/petri_net_model_gen/blob/master/LICENSE) [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/autotwin_gmglib)](https://www.python.org/downloads/) [![PyPI - Version](https://img.shields.io/pypi/v/autotwin_pnglib)](https://pypi.org/project/autotwin_pnglib/)

# Petri Net Model Generation Library for Auto-Twin

## Introduction

The Petri Net Model Generation Library is a Python package designed to create, manipulate, and export Petri net models to a Neo4j database.

## Installation

To facilitate installation, the PMS WSGI is released as a Python module, `autotwin_pmswsgi`, in the PyPI repository.

`autotwin_pnglib` has implicit dependencies on `autotwin_gmglib` and the optimization solver [SCIP](https://scipopt.org/). These dependencies cannot be automatically resolved by `pip` and must be installed manually.

1. Install `autotwin_gmglib` by following the instructions provided [here](https://github.com/AutotwinEU/proc-mining-serv/blob/main/README.md).
2. Install SCIP by following the instructions [here](https://www.scipopt.org/doc/html/INSTALL.php). Using the precompiled binary for version 9.1.0 is sufficient.

Once `autotwin_gmglib` and SCIP are installed, you can easily install the other required Python packages with:

`pip install -r requirements.txt `
