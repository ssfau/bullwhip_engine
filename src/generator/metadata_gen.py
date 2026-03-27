import pandas as pd
import numpy as np
import src.utils as utils

from pathlib import Path
from config.schemas.raw import Product, Store

script = Path(__file__).resolve().parent

# META DATA HANDLING

"""
this function returns dataframe from within the csv file
"""
def define_metadata_csv(type):
    metadata_csv_dir = script.parent / 'data' / 'raw' / 'metadata' / 'store.csv'
    if type == "store":
        metadata_csv_dir = script.parent / 'data' / 'raw' / 'metadata' / 'store.csv'
    elif type == "product":
        metadata_csv_dir = script.parent / 'data' / 'raw' / 'metadata' / 'product.csv'
    
    with open(metadata_csv_dir, "a") as file:
        # read csv to generate product id
        df = pd.read_csv(metadata_csv_dir)

    return df

"""
this function inserts new rows (LIST ONLY) into a csv file
"""
def insert_metadata_csv(type, df, datalist):
    metadata_csv_dir = script.parent / 'data' / 'raw' / 'metadata' / 'store.csv'
    if type == "store":
        metadata_csv_dir = script.parent / 'data' / 'raw' / 'metadata' / 'store.csv'
    elif type == "product":
        metadata_csv_dir = script.parent / 'data' / 'raw' / 'metadata' / 'product.csv'
    
    df2 = pd.DataFrame(datalist)
    df = pd.concat([df, df2])
    df.to_csv(metadata_csv_dir, index=False)

"""
this function generates STORE metadata and writes it into the csv
- assigns crude integer store IDs based on the chronological order of creation and insertion
- generates random with fixed values according to the given schema
- in this simulation, every store sells the same products
- random generation exists only, no manual input
"""
def generate_store_metadata(n_stores):
    metadata_csv_dir = script.parent / 'data' / 'raw' / 'metadata' / 'store.csv'

    with open(metadata_csv_dir, "a") as file:
        # read csv to generate store id
        df = pd.read_csv(metadata_csv_dir)

    newdatalist = []
    currentstoreid = len(df)+1

    # assign dictionaries for each column
    for i in range(n_stores):
        new_row_data = {
            'store_id':  currentstoreid,
            'store_name': "store_" + str(currentstoreid),
            'max_inventory_capacity': np.random.triangular(40, 80, 160),
            'reorder_point_factor': utils.truncated_normal(0.5, 0.2, 0.3, 0.7),
            'delay_probability': np.random.triangular(0.1,0.2,0.5),
            'holding_cost_rate': utils.truncated_normal(0.2, 0.1, 0.1, 0.5),
        }

        newdatalist.append(new_row_data)
        currentstoreid += 1

    df2 = pd.DataFrame(newdatalist)
    df = pd.concat([df, df2])
    df.to_csv(metadata_csv_dir, index=False)
    
    return

"""
this function generates PRODUCT metadata and writes it into the csv
- assigns crude integer store IDs based on the chronological order of creation and insertion
- generates random with fixed values according to the given schema
- both random and manual key in exists
"""
def generate_product_metadata(product_name, unit_cost, unit_price, shelf_life_days, min_order_qty, base_lead_time):
    # check if csv exists
    metadata_csv_dir = script.parent / 'data' / 'raw' / 'metadata' / 'product.csv'

    with open(metadata_csv_dir, "a") as file:
        # read csv to generate product id
        df = pd.read_csv(metadata_csv_dir)

    newdatalist = []
    currentproductid = len(df)+1

    new_row_data = {
        'product_id': currentproductid,
        'product_name': product_name or ("product_" + str(currentproductid)),
        'unit_cost': unit_cost,
        'unit_price': unit_price,
        'shelf_life_days': shelf_life_days,
        'min_order_qty': min_order_qty,
        'base_lead_time': base_lead_time,
    }

    newdatalist.append(new_row_data)
    df2 = pd.DataFrame(newdatalist)
    df = pd.concat([df, df2])
    df.to_csv(metadata_csv_dir, index=False)
    
    return

def generate_product_metadata_random(n_products):
    # check if csv exists
    metadata_csv_dir = script.parent / 'data' / 'raw' / 'metadata' / 'product.csv'
    with open(metadata_csv_dir, "a") as file:
        # read csv to generate product id
        df = pd.read_csv(metadata_csv_dir)

    # read csv to generate product id
    df = pd.read_csv(metadata_csv_dir)
    newdatalist = []
    currentproductid = len(df)+1

    # assign dictionaries for each column
    for i in range(n_products):
        new_row_data = {
            'product_id': currentproductid,
            'product_name': "product_" + str(currentproductid),
            'unit_cost': np.random.randint(1,5),
            'unit_price': 10, # placeholder
            'shelf_life_days': np.random.randint(5,14),
            'min_order_qty': np.random.randint(15, 20),
            'base_lead_time': 10, # placeholder
        }

        new_row_data['unit_price'] = new_row_data['unit_cost'] * utils.rng.uniform(1.05,1.4)
        new_row_data['base_lead_time'] = np.random.randint(1,3)
        
        newdatalist.append(new_row_data)
        currentproductid += 1

    df2 = pd.DataFrame(newdatalist)
    df = pd.concat([df, df2])
    df.to_csv(metadata_csv_dir, index=False)
    
    return

# TRANSACTION DATA HANDLING

def generate_transaction_data_by_year(year):
    return