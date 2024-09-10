# Gdp Tools Package

[![Code Checks](https://github.com/laingorourke/gdp-tools/actions/workflows/code-checks.yml/badge.svg)](https://github.com/laingorourke/gdp-tools/actions/workflows/code-checks.yml)
[![Code Style](https://img.shields.io/badge/Code%20Style-flake8-blue)](https://flake8.pycqa.org/)

This is a utility package designed to enable data scientists and analysts to easily access GDP data within a python environment

Requirements:
- The data professional should be able to clone the package at the start of new project and when in production
- The package will contain a number of support functions serving the following objectives:
-- Accessing data on GDP Base/CIM/Warehouse 
-- Accessing data in temp storage (LAB)
-- Querying that data in SQL
-- utlising that data as a Python/PySpark DataFrame
-- Storing processed data to the temp storage space (LAB)
- any data access configs should available to be used 






## Project Installation

This project uses Conda to manage dependencies. For the fastest way of obtaining conda, install [Miniconda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html). After installation, to install the dependencies, run this command in the root directory of the project:

```
conda env update environment.yml --prune
```

## Project Organisation

```
├── README.md          <- The top-level README for developers using this project.
|
├── .github            <- Github related files.
│   └── workflows      <- Github workflows for Github Actions.
|
├── config             <- Config files for the project. By default this will include the AML
|                         staging config.
├── data
│   ├── external       <- Data from third party sources.
│   ├── processed      <- The final, canonical data sets for modelling and analysis.
│   ├── raw            <- The original, immutable data dump.
|   └── sql            <- SQL used to query data.
│
├── models_store       <- Trained and serialized models, model predictions, or model summaries.
│
├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering) and
│                         a short `-` delimited description, e.g.
│                         `1.0-jqp-initial-data-exploration`.
│
├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures        <- Generated graphics and figures to be used in reporting
│
├── gdp_tools   <- Source code for use in this project.
│   ├── __init__.py    <- Makes gdp_tools a Python module
│   │
│   ├── data           <- Scripts to download or generate data
│   │   └── make_dataset.py
│   │
│   ├── features       <- Scripts to turn raw data into features for modelling
│   │   └── build_features.py
│   │
│   ├── models         <- Scripts to train models and then use trained models to make
│   │   │                 predictions
│   │   ├── predict_model.py
│   │   └── train_model.py
|   |
|   ├── tests          <- Scripts used to perform unit tests.
|   |                     Check tests > data > test_make_dataset.py for an example.
│   │
│   └── visualization  <- Scripts to create exploratory and results oriented visualizations
│       └── visualize.py
|
├── environment.yml    <- Conda environment file.
├── setup.py           <- Makes project pip installable (pip install -e .) so src can be imported.
```
