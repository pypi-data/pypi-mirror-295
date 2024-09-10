import duckdb

def conn_motherduck(df_sales, df_product_sales, db, md_token):
    con = duckdb.connect(f'md:{db}?motherduck_token={md_token}')

    if df_sales is not None:
        try:
            con.execute("PRAGMA table_info('sales')").fetchdf()
            con.execute("INSERT INTO sales SELECT * FROM df_sales")
        except duckdb.CatalogException as err:
            con.execute("CREATE TABLE sales AS SELECT * FROM df_sales")

    if df_product_sales is not None:
        try:
            con.execute("PRAGMA table_info('product_sales')").fetchdf()
            con.execute("INSERT INTO product_sales SELECT * FROM df_product_sales")
        except duckdb.CatalogException as err:
            con.execute("CREATE TABLE product_sales AS SELECT * FROM df_product_sales")
    
    con.close()

def conn_motherduck_singletable(df, table_name, db, md_token):
    con = duckdb.connect(f'md:{db}?motherduck_token={md_token}')
    con.execute(f"CREATE TABLE {table_name} AS SELECT * FROM df")
    con.close()

def upload_to_motherduck(local_path, db_name, api_key):
    # Conectarse a la base de datos local
    conn = duckdb.connect(local_path)
    
    # Conectarse a MotherDuck usando DuckDB con el nombre de la base de datos y la API key
    conn.execute(f"SET motherduck.api_key = '{api_key}'")
    conn.execute(f"CONNECT TO motherduck.database('{db_name}')")
    
    # Subir la base de datos a MotherDuck
    conn.execute(f"IMPORT DATABASE '{local_path}'")

    # Cerrar la conexión
    conn.close()

    print(f"Base de datos '{local_path}' subida a MotherDuck como '{db_name}'.")

def delete_from_motherduck(date, table_name, db_name, api_key):
    con = duckdb.connect(f'md:{db_name}?motherduck_token={api_key}')
    con.execute(f"DELETE FROM {table_name} WHERE date = DATE '{date}'")
    con.close()