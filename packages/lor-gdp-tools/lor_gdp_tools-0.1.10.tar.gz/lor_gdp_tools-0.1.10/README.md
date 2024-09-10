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

### Credentials

See .env file for credentials. Contact a member of the Laing O'Rourke Data Science team to access these

### Functionality

**validate_odbc_drivers** - check if the correct ODBC connectors are installed, install them as necessary automatically [**check_odbc_driver**, **install_odbc_driver**] 

**setup_odbc_connection** - set up the ODBC with your credentials. Happens when class is initalised

**query_gdp_to_pd** - enter a SQL query as a string, return the data as a pandas dataframe

**search_tables** - will return a list of all table in the GDP. give it the argument 'source_system' = '[COINS]' to narrow your search for any table with the term 'COINS' in it (for example)  






