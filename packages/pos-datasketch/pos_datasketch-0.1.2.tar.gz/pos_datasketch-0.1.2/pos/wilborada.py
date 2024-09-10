import duckdb
import pandas as pd
import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor

# sudo locale-gen es_ES.UTF-8 if error
import locale
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

def connect_postgres(host, database, user, password, port=5432):
    try:
        # Establish the connection
        conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port=port
        )
        print("Connection to PostgreSQL DB successful")
        
        # Create a cursor
        cur = conn.cursor(cursor_factory=RealDictCursor)

        return cur, conn
    except (Exception, psycopg2.Error) as error:
        print(f"Error while connecting to PostgreSQL: {error}")
        return None, None

def close_connection(conn, cur):
    if cur:
        cur.close()
    if conn:
        conn.close()
        print("PostgreSQL connection is closed")

def extract_date_parts(datetime_str):
    if not datetime_str or pd.isnull(datetime_str):
        return None, None, None, None, None, None, None, None

    datetime_object = datetime_str
    year_month = datetime_object.strftime("%Y-%m")

    return (
        datetime_object.year,
        year_month,
        datetime_object.day,
        datetime_object.month,
        datetime_object.strftime("%A"),
        datetime_object.strftime("%B")
    )

def get_sales(cur, start_date, end_date):
    try:
        cur.execute(f"""
                SELECT 
                    sb.document_id,
                    sb.client_id,
                    sb.amount as total,
                    sb.description,
                    sb.cancelled,
                    sb.real_time as time,
                    d.real_date as date,
                    p.first_name as client_first_name,
                    p.surname as client_surname,
                    p.doc as client_doc,
                    p.sex as client_sex
                FROM 
                    sale_bill sb
                LEFT JOIN 
                    document d ON sb.document_id = d.document_id
                LEFT JOIN 
                    person p ON p.party_id = sb.client_id
                WHERE d.real_date BETWEEN '{start_date}' AND '{end_date}';""")

        results = cur.fetchall()

        df = pd.DataFrame(results)

        df['total'] = df['total'].astype('float64')

        df[["year", "yearmonth", "day", "month", "weekday", "monthstr"]] = (
        df["date"].apply(lambda x: pd.Series(extract_date_parts(x)))
    )

        return df
    except (Exception, psycopg2.Error) as error:
        print(f"Error while fetching data from PostgreSQL: {error}")
        return None

def get_books(cur):
    try:
        cur.execute("""
            SELECT
                b.book_id,
                b.title,
                b.subtitle,
                b.pais_id,
                b.editorial_id,
                b.language_id,
                b.edition,
                b.main_provider_id,
                b.active,
                b.language_id,
                e.name as editorial_name,
                e.pais_id as editorial_pais_id,
                bi.isbn,
                bi.barcode,
                b.visible_author as author_fullname
            FROM
                book b
            LEFT JOIN 
                editorial  e ON b.editorial_id = e.editorial_id
            LEFT JOIN 
                book_isbn bi ON b.book_id = bi.book_id;
                    """)
        results = cur.fetchall()
        df = pd.DataFrame(results)
        return df
    except (Exception, psycopg2.Error) as error:
        print(f"Error while fetching data from PostgreSQL: {error}")
        return None


def get_products_sales(cur, start_date, end_date):
    try:
        cur.execute(f"""
            SELECT 
                sbi.document_id,
                sbi.product_id,
                sbi.quantity,
                sbi.price,
                sbi.discount,
                b.title,
                b.visible_author as author	
            FROM
                sale_bill_item sbi
            LEFT JOIN 
                document d ON sbi.document_id = d.document_id
            LEFT JOIN 
                book b ON sbi.product_id = b.book_id
            WHERE d.real_date BETWEEN '{start_date}' AND '{end_date}';
            """)
        results = cur.fetchall()
        df = pd.DataFrame(results)

        df['price'] = df['price'].astype('float64')
        df['discount'] = df['discount'].astype('float64')

        return df
    except (Exception, psycopg2.Error) as error:
        print(f"Error while fetching data from PostgreSQL: {error}")
        return None

def get_clean_data(cur, start_date, end_date):
    sales = get_sales(cur, start_date, end_date)
    products_sales = get_products_sales(cur, start_date, end_date)

    products_sales = pd.merge(products_sales, sales, how='left', on='document_id')

    return sales, products_sales

def get_clients(cur):
    cur.execute("""
        SELECT
            p.first_name,
            p.surname,
            p.doc,
            p.sex
        FROM
            person p;
    """)
    results = cur.fetchall()
    df = pd.DataFrame(results)
    return df

def get_authors(cur):
    cur.execute("""
        SELECT
            *
        FROM
            book_author;
    """)
    results = cur.fetchall()
    book_author = pd.DataFrame(results)

    cur.execute("""
        SELECT
            *
        FROM
            author;
    """)
    results = cur.fetchall()
    author = pd.DataFrame(results)
    
    return book_author, author

def get_materia(cur):
    cur.execute("""
        SELECT
            *
        FROM
            book_materia;
    """)
    results = cur.fetchall()
    book_materia = pd.DataFrame(results)

    cur.execute("""
        SELECT
            *
        FROM
            materia;
    """)
    results = cur.fetchall()
    materia = pd.DataFrame(results)

    return book_materia, materia

def create_bookpairs(md_token):
    con = duckdb.connect(f'md:wilborada__wilboradadb?motherduck_token={md_token}')
    con.execute("""
                DROP TABLE IF EXISTS book_pairs;
CREATE TABLE book_pairs AS
         WITH joined_sales AS (
   SELECT 
        ps1.document_id,
        ps1.product_id AS product_id1,
        ps2.product_id AS product_id2,
        concat(product_id1, '-', product_id2) as x
    FROM 
        product_sales ps1
    INNER JOIN 
        product_sales ps2 ON ps1.document_id = ps2.document_id
    WHERE 
        ps1.product_id < ps2.product_id
)
SELECT
  x,
  COUNT(*) as count
FROM 
  joined_sales
GROUP BY
  x
ORDER BY
                count desc;
    """)
    con.execute("""
        SELECT
            *
        FROM
            book_pairs;
    """)
    results = con.fetchall()
    print(results)

    con.close()
