def test_deffined_connection(conn):
    try:
        conn
    except NameError:
        print("ODBC Connection is not defined")