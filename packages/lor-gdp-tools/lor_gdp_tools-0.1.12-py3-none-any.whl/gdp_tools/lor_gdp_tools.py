#from dotenv import load_dotenv
import subprocess
import os
import pyodbc
import pandas as pd
import json

#from tests import test_deffined_connection

class GlobalDataPlatformTools():
    """
    This package will support you in accessing, and working with data from the GDP. 
    It's functional requirements are:
    - Accessing data on GDP Base/CIM/Warehouse 
    - Accessing data in temp storage (LAB)
    - Querying that data in SQL
    - utlising that data as a Python/PySpark DataFrame
    - Storing processed data to the temp storage space (LAB)    

    Note on publishing the package on PyPI:
    - pip install twine
    - rm -r build/ dist/
    - python setup.py sdist bdist_wheel
    - twine upload -u __token__ -p [PYPI API KEY - in ENV file] dist/*
    """

    def __init__(self,USERNAME: str, PASSWORD: str):

        # Step 1: Read the JSON configuration file
        with open('config.json', 'r') as file:
            self.config = json.load(file)

        # Access the variables
        self.SERVER = self.config['SERVER']
        self.DATABASE = self.config['DATABASE'] # Location of Synapse
        self.USERNAME = USERNAME # user entry
        self.PASSWORD = PASSWORD # user entry
        self.AUTH = 'ActiveDirectoryInteractive' #aka Azure Active Directory - Universal with MFA # using sbaadminuk and setting this auth method results in a connection timeout

        print(f'using credentials of {self.USERNAME}')

        # deffine connectors
        self.setup_odbc_connection()

    def validate_odbc_drivers(self,):
        # Check if the ODBC Driver 18 for SQL Server is installed, if not install it
        if not self.check_odbc_driver():
            self.install_odbc_driver()

    def check_odbc_driver(self,):
        try:
            # Check if the ODBC Driver 18 for SQL Server is installed
            result = subprocess.run(['odbcinst', '-q', '-d'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if 'ODBC Driver 18 for SQL Server' in result.stdout:
                print("ODBC Driver 18 for SQL Server is already installed.")
                return True
            else:
                print("ODBC Driver 18 for SQL Server is not installed.")
                return False
        except FileNotFoundError:
            print("odbcinst command not found. Please install unixODBC.")
            return False
            
    def install_odbc_driver(self):
        try:
            # Add the Microsoft repository key
            subprocess.run(['curl', 'https://packages.microsoft.com/keys/microsoft.asc', '|', 'sudo', 'apt-key', 'add', '-'], check=True)

            # Add the Microsoft repository
            subprocess.run(['sudo', 'curl', 'https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/prod.list', '-o', '/etc/apt/sources.list.d/mssql-release.list'], check=True)
            
            # Update package list
            subprocess.run(['sudo', 'apt-get', 'update'], check=True)
            
            # Install the ODBC driver
            subprocess.run(['sudo', 'ACCEPT_EULA=Y', 'apt-get', 'install', '-y', 'msodbcsql18'], check=True)
            
            print("ODBC Driver 18 for SQL Server has been installed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while installing the ODBC driver: {e}")        
        

    def setup_odbc_connection(self,):
        #https://learn.microsoft.com/en-us/sql/connect/python/pyodbc/step-3-proof-of-concept-connecting-to-sql-using-pyodbc?view=sql-server-ver16
        #https://github.com/mkleehammer/pyodbc/wiki/The-pyodbc-Module#connect
        #https://learn.microsoft.com/en-us/azure/synapse-analytics/sql-data-warehouse/sql-data-warehouse-connect-overview

        # Setup connection using ODBC Driver
        connectionString = f'''
                             DRIVER={{ODBC Driver 18 for SQL Server}};
                             SERVER=tcp:{self.SERVER};
                             DATABASE={self.DATABASE};
                             UID={self.USERNAME};
                             PWD={self.PASSWORD};
                             Encrypt=yes;
                             TrustServerCertificate=no;
                             Connection Timeout=30;
                            '''
        
        #SQL Server Native Client 11.0
        try:
            self.conn = pyodbc.connect(connectionString)
            print("Connected Successfully") 
        except Exception as e:
            print("Connection failed: ", e )

    def query_gdp_to_pd(self,sql_query: str):
        """
        Input: user enters a SQL query as a string
        Output: returns a python dataframe
        """
        
        # test if connection is deffined
        #test_deffined_connection(self.conn)

        return pd.read_sql(sql_query, self.conn)
    
    def search_tables(self, database = 'BASE', **kwargs):
        """
        Input: 
        - database: str - take 'BASE' as a default (as opposed to CIM)
        - Kwargs:
            - source_system = str - deffine a source system to reffine the search to certain term
        Output: 
        - df - list of tables within the database
        """

        source_system = kwargs.get('source_system', None)
        if source_system:
            source_system_condition = f"AND table_name like '%{source_system}%'"
            print(f'Searching for tables like {source_system}')
        else:
            source_system_condition = ''        
    
        sql_query = f'''
        SELECT table_name
        FROM information_schema.tables
        WHERE table_type = 'BASE TABLE' AND table_schema = '{database}'
        {source_system_condition};
        '''
        #print(sql_query)
        return pd.read_sql(sql_query, self.conn)    