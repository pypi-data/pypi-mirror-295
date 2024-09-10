import pyodbc
import pandas as pd
import locale
from datetime import datetime

# sudo locale-gen es_ES.UTF-8 if error
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

def get_raw_data(dateInit, dateEnd, server, database, username, password):
    try:
        connection_string = f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password};TrustServerCertificate=yes;"
        conn = pyodbc.connect(connection_string, timeout=30)
        print(conn)
        cursor = conn.cursor()

        sql = """
        SET NOCOUNT ON;
        DECLARE @rv int;
        EXEC @rv = sp_GetTransactionOrderDetailsView @dtFechaInicial = ?, @dtFechaFinal = ?;
        SELECT @rv AS return_value;
        """
        params = (
            dateInit,
            dateEnd,
        )
        
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        
        df = pd.DataFrame.from_records(
            rows,
            columns=[
                "biTransactionID",
                "iPuntoDeVentaID",
                "iSubPuntoDeVentaID",
                "SubPuntoDeVenta",
                "tiTransactionTypeID",
                "TransactionType",
                "vObservations",
                "NombreEnPedido",
                "dtTrxDate",
                "dtSystemDate",
                "biDocumentID",
                "vTerminalID",
                "biEmployeeID",
                "tiStatusID",
                "biClientID",
                "StatusName",
                "tiDeliveryTypeID",
                "DeliveryType",
                "tiTableID",
                "vExternalFurnitureID",
                "PisoDescription",
                "vResolucionImpuestosID",
                "biTransactionOrderDetailID",
                "iItemID",
                "biTransactionID",
                "tiDetailStatusID",
                "DetailStatus",
                "biFatherID",
                "tiDetailTypeID",
                "iPuntoDeVentaID_Item",
                "tiReplicationStatusID",
                "tiDetailStatusID",
                "iPuntoDeVentaID",
                "dtDate",
                "tiItemRoleID",
                "biFatherID",
                "zOrder",
                "tiSeatNumber",
                "ItemName",
                "vExternalCode",
                "tiGroupID",
                "tiSubGroupID",
                "tiMeasureUnitID_Inventory",
                "tiMeasureUnitID_Recipe",
                "SubGroupName",
                "GroupName",
                "vNombres",
                "vApellidos",
                "biEmployeeID_Detail",
                "vNombres_Detail",
                "vApellidos_Detail",
                "mItemPrice",
                "fDiscountPercentage",
                "iDiscountID",
                "iPuntoDeVentaID_Discount",
                "dTaxPercentage",
                "dTaxPercentage2",
                "iTaxID",
                "iTaxID2",
                "TaxName",
                "Tax2Name",
                "vObservationsOnDetail",
                "dQuantity",
                "mTotalNoTax",
                "mTotalDiscount",
                "mSubTotal",
                "mTotalTax",
                "Total",
                "vNombres_Client",
                "vApellidos_Client",
                "vAddress_Client",
                "vPhoneNumber1_Client",
                "vMobilePhone_Client",
                "vEMail_Client",
            ],
        )
        return df
    except Exception as e:
        print(e)

def extract_date_parts(datetime_str):
    if not datetime_str or pd.isnull(datetime_str):
        return None, None, None, None, None, None, None, None

    datetime_object = datetime_str
    year_month = datetime_object.strftime("%Y-%m")
    time = datetime_object.strftime("%H:%M:%S")

    return (
        datetime_object.date(),
        datetime_object.year,
        year_month,
        datetime_object.day,
        datetime_object.month,
        datetime_object.strftime("%A"),
        datetime_object.strftime("%B"),
        time,
    )


def calculate_duration_in_seconds(df, start, end, field):
    df[start] = pd.to_datetime(df[start])
    df[end] = pd.to_datetime(df[end])
    df[field] = (df[end] - df[start]).dt.total_seconds()
    return df

def get_sales_tables(source: pd.DataFrame):
    # TODO: unknown column to extract fiscalId
    
    
    df = source.copy(deep=True)
    # Filter by
    df = df[df.TransactionType == "VENTA"]

    
    group = df.groupby(df['biTransactionID'].iloc[:, 0]).agg(
        amount_total=('Total', lambda x: round(x.sum(), 2)),
        taxes=('mTotalTax', lambda x: round(x.sum(), 2)),
        dateOpen=('dtSystemDate', 'first'),
        dateClosed=('dtTrxDate', 'first'),
        invoice_datetime=('dtTrxDate', 'first'),
        zone_id=('iSubPuntoDeVentaID', 'first'),
        waiter_id=('biEmployeeID_Detail', 'first'),
        amount=('mTotalNoTax', lambda x: round(x.sum(), 2)),
        location=('PisoDescription', 'first'),
        waiter_name1=('vNombres', 'first'),
        waiter_name2=('vApellidos', 'first'),
        discounts=('mTotalDiscount', lambda x: round(x.sum(), 2)),
        table_id=('vExternalFurnitureID', 'first'),
        zone_name=('SubPuntoDeVenta', 'first'),
    ).reset_index()
    
    
    
    # Add computed columns
    group["waiter_name"] = group.apply(
        lambda row: f"{row.waiter_name1} {row.waiter_name2}".strip(), axis=1
    )
    group["invoice_datetime"] =  pd.to_datetime(group["invoice_datetime"])
    group[["date", "year", "yearmonth", "day", "month", "weekday", "monthstr", "hour"]] = (
        group["invoice_datetime"].apply(lambda x: pd.Series(extract_date_parts(x)))
    )
    group = calculate_duration_in_seconds(group, "dateOpen", "dateClosed", "duration")
    
    group = group.rename(columns={'biTransactionID': 'order_id'})
    
    group = group.drop(columns=['waiter_name1', 'waiter_name2'])
    
    group['gratuity'] = 0
    
    group['payment_method'] = ''
    
    group['table_capacity'] = ''
    
    group['invoice_id'] = ''
    
    group['amount'] = group['amount'].astype('float64')
    
    return group

""" def get_sales_tables(source: pd.DataFrame):
    # TODO: unknown column to extract fiscalId
    columns = {
        "biTransactionID": "orderId",
        "Total": "total",
        "mTotalTax": "taxes",
        "PisoDescription": "zoneName",
        "SubPuntoDeVenta": "branch",
        "dtSystemDate": "dateOpen",
        "dtTrxDate": "dateClosed",
    }
    df = source.copy(deep=True)
    # Filter by
    df = df[df.TransactionType == "VENTA"]
    # Rename columns
    df = df.rename(columns=columns)
    # Add computed columns
    df["waiterName"] = df.apply(
        lambda row: f"{row.vNombres} {row.vApellidos}".strip(), axis=1
    )
    df["datetime"] = df["dateClosed"]
    df[["date", "year", "yearmonth", "day", "month", "weekday", "monthstr", "time"]] = (
        df["datetime"].apply(lambda x: pd.Series(extract_date_parts(x)))
    )
    df = calculate_duration_in_seconds(df, "dateOpen", "dateClosed", "duration")
    # Select
    select = list(columns.values()) + [
        "waiterName",
        "datetime",
        "date",
        "year",
        "yearmonth",
        "day",
        "month",
        "weekday",
        "monthstr",
        "time",
        "duration",
    ]
    df = df[select]
    
    print(df)
    
    return df
 """

def get_product_sales_table(source: pd.DataFrame):
    columns = {
        "biTransactionID": "order_id",
        "dtTrxDate": "invoice_datetime",
        "vExternalCode": "product_id",
        "ItemName": "product_name",
        "tiSubGroupID": "product_hierarchy_id",
        "dQuantity": "quantity",
        "mItemPrice": "price",
        "Total": "paid",
        "mTotalTax": "taxes",
        "SubGroupName": "product_category",
        "SubPuntoDeVenta": "location"
    }
    df = source.copy(deep=True)
    # Filter by
    df = df[df.TransactionType == "VENTA"]
    # Rename columns
    df = df.rename(columns=columns)
    # Add computed columns
    """ df["category"] = df.apply(lambda x: f"{x.GroupName} | {x.SubGroupName}", axis=1) """
    df["invoice_datetime"] = pd.to_datetime(df["invoice_datetime"])
    df[["datetime", "year", "yearmonth", "day", "month", "weekday", "monthstr", "time"]] = (
        df["invoice_datetime"].apply(lambda x: pd.Series(extract_date_parts(x)))
    )
    df["invoice_datetime"] = pd.to_datetime(df["invoice_datetime"])
    # Select
    select = list(columns.values()) + [
        "datetime",
        "year",
        "yearmonth",
        "day",
        "month",
        "weekday",
        "monthstr",
        "time",
    ]
    df = df[select]
    
    
    df['quantity'] = df['quantity'].astype('float64')
    df['price'] = df['price'].astype('float64')
    df['paid'] = df['paid'].round(2)
    df['taxes'] = df['taxes'].round(2)
    
    return df

def clean_data(raw_data):
    sales = get_sales_tables(raw_data)
    product_sales = get_product_sales_table(raw_data)
    
    return sales, product_sales