import requests
import json
from datetime import datetime
import locale
import pandas as pd
from functools import reduce, partial

# sudo locale-gen es_ES.UTF-8 if error
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

def get_auth(datos):
    url = "https://api.pirpos.com/login"
    headers = {
        "Content-Type": "application/json"
    }
    try:
        # Realizar la petición POST
        respuesta = requests.post(url, json=datos, headers=headers)
        
        # Comprobar si la petición fue exitosa
        respuesta.raise_for_status()

        data = respuesta.json()
        
        # Devolver la respuesta en formato JSON
        return data['tokenCurrent']
    
    except requests.exceptions.HTTPError as errh:
        print("Error HTTP:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error de conexión:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout:", errt)
    except requests.exceptions.RequestException as err:
        print("Error desconocido:", err)

def get_raw_data(dateInit, dateEnd, token):
    query = {
        'pagination': True,
        'page': 0,
        'limit': 100000,
        'dateInit': dateInit,
        'dateEnd': dateEnd
    }
    headers = {
        "Content-Type": "application/json"
    }
    headers['Authorization'] = f"Bearer {token}"

    try:
        # Realizar la petición POST
        respuesta = requests.get('https://api.pirpos.com/invoices', params=query, headers=headers)
        
        # Comprobar si la petición fue exitosa
        respuesta.raise_for_status()
        
        # Devolver la respuesta en formato JSON
        return respuesta.json()
    
    except requests.exceptions.HTTPError as errh:
        print("Error HTTP:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error de conexión:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout:", errt)
    except requests.exceptions.RequestException as err:
        print("Error desconocido:", err)

def transform_it(dato):
    fecha = dato['createdOn']

    fecha_iso = fecha.replace("Z", "+00:00")

    fecha = datetime.fromisoformat(fecha_iso)   
    

    new_data = {
        'order_id': dato['_id'],
        'amount_total': dato['totalPaid'],
        'taxes': dato['totalTaxes'],
        'datetime_open': dato['createdOn'],
        'datetime_close': '',
        'zone_id': '',
        'waiter_id': dato['seller']['idInternal'],
        'invoice_datetime': dato['createdOn'],
        'date': f'{fecha.year}-{fecha.month:02}-{fecha.day:02}',
        'year': fecha.year,
        'yearmonth': f'{fecha.year}-{fecha.month:02}',
        'day': fecha.day,
        'month': fecha.month,
        'weekday': fecha.strftime("%A"),
        'monthstr': fecha.strftime("%B"),
        'hour': fecha.strftime("%H:%M:%S"),
        'duration': '',
        'amount': dato['total'],
        'location': '',
        'gratuity': dato['tip'],
        'waiter_name': dato['seller']['name'],
        'table_id': dato['table']['idInternal'],
        'invoice_id': dato['number'],
        'discounts': dato['totalDiscount'],
        'table_capacity': '',
        'payment_method': dato['paymentMethod'],
        'zone_name': ''
    }

    return new_data

def get_products(next, data):
    fecha = data['createdOn']

    fecha_iso = fecha.replace("Z", "+00:00")

    fecha = datetime.fromisoformat(fecha_iso)

    new_data = {
        'order_id': data['_id'],
        'product_id': next['idInternal'],
        'product_name': next['name'],
        'product_hierarchy_id': next['categoryId'],
        'price': next['price'],
        'quantity': next['quantity'],
        'paid': next['total'],
        'taxes': next['totalTaxes'],
        'product_category': next['categoryName'],
        'date': f'{fecha.year}-{fecha.month:02}-{fecha.day:02}',
        'year': fecha.year,
        'yearmonth': f'{fecha.year}-{fecha.month:02}',
        'day': fecha.day,
        'month': fecha.month,
        'weekday': fecha.strftime("%A"),
        'monthstr': fecha.strftime("%B"),
        'hour': fecha.strftime("%H:%M:%S"),
        'location': ''
    }

    return new_data


def transform_it_products(prev, next):
    fecha = next['createdOn']

    fecha_iso = fecha.replace("Z", "+00:00")

    fecha = datetime.fromisoformat(fecha_iso)

    get_products_0 = partial(get_products, data=next)

    list_propducts = list(map(get_products_0, next['products']))


    prev.extend(list_propducts)
    
    return prev

def clean_data(raw_data):
    sales = list(map(transform_it, raw_data))

    df_sales = pd.DataFrame(sales)
    df_sales['invoice_datetime'] = pd.to_datetime(df_sales['invoice_datetime'])
    df_sales['date'] = pd.to_datetime(df_sales['date'])

    product_sales = reduce(transform_it_products, raw_data, [])

    product_sales = list(filter(lambda n: n['product_category'] != 'COMUNICADOS', product_sales))
    df_product_sales = pd.DataFrame(product_sales)
    df_product_sales['date'] = pd.to_datetime(df_product_sales['date'])

    return df_sales, df_product_sales

