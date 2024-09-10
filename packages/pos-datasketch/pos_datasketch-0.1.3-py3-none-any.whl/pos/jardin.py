import pyodbc
import pandas as pd
import locale
from datetime import datetime

def get_conn(server, database, username, password):
    try:
        connection_string = f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password};TrustServerCertificate=yes;"
        conn = pyodbc.connect(connection_string, timeout=30)
        print(conn)
        cursor = conn.cursor()
                
        sql = 'SELECT * FROM T_City;'

        cursor.execute(sql)
        
        rows = cursor.fetchall()

        print(rows) 
        
        
        return conn
    except Exception as e:
        print(e)
