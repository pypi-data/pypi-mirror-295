# hra_jupyter_widgets

[![PyPI - Version](https://img.shields.io/pypi/v/hra-jupyter-widgets.svg)](https://pypi.org/project/hra-jupyter-widgets)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/hra-jupyter-widgets.svg)](https://pypi.org/project/hra-jupyter-widgets)
<a target="_blank" href="https://colab.research.google.com/github/x-atlas-consortia/hra-jupyter-widgets/blob/main/usage.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

-----

## Table of Contents

- [hra\_jupyter\_widgets](#hra_jupyter_widgets)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Development installation](#development-installation)

## Installation

```sh
pip install hra_jupyter_widgets
```

## Usage

HRA Jupyter Widgets are designed to be used from python notebooks. See [usage.ipynb](usage.ipynb) for examples on how to use them from notebooks. You can also open it directly from colab here:

<a target="_blank" href="https://colab.research.google.com/github/x-atlas-consortia/hra-jupyter-widgets/blob/main/usage.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

## Development installation

Create a virtual environment and and install hra_jupyter_widgets in *editable* mode with the
optional development dependencies:

```sh
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

Open [usage.ipynb](usage.ipynb) in JupyterLab, VS Code, or your favorite editor
to start developing. Changes made in `src/hra_jupyter_widgets/static/` will be reflected
in the notebook.
