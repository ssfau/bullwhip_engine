import pandas as pd
import numpy as np
import src.utils as utils

from pathlib import Path
from config.schemas.raw import Product, Store

script = Path(__file__).resolve().parent

# META DATA HANDLING

"""
this function returns dataframe of a csv by automatically selecting type
"""
def get_df_metadata_csv(type):
    csv_path = script.parent / 'data' / 'raw' / 'metadata'
    if type == "store":
        csv_path = csv_path / 'store.csv'
    elif type == "product":
        csv_path = csv_path / 'product.csv'
    else:
        raise ValueError("Invalid type")

    with open(csv_path, "a") as file:
        # read csv to generate store id
        df = pd.read_csv(csv_path)
    
    return df, csv_path

"""
this function generates STORE metadata and writes it into the csv
- assigns crude integer store IDs based on the chronological order of creation and insertion
- generates random with fixed values according to the given schema
- in this simulation, every store sells the same products
- random generation exists only, no manual input
"""
def generate_store_metadata(n_stores):
    df, csvpath = get_df_metadata_csv("store")

    # store id generation
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
    df.to_csv(csvpath, index=False)
    
    return

"""
this function generates PRODUCT metadata and writes it into the csv
- assigns crude integer store IDs based on the chronological order of creation and insertion
- generates random with fixed values according to the given schema
- both random and manual key in exists
"""
def generate_product_metadata_manual(product_name, unit_cost, unit_price, shelf_life_days, min_order_qty, base_lead_time):
    # check if csv exists
    df, csvpath = get_df_metadata_csv("store")

    # store id generation
    newdatalist = []
    currentproductid = len(df)+1

    if product_name == None:
        product_name = "product_" + str(currentproductid)

    # assign dictionaries for each column
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
    df.to_csv(csvpath, index=False)
    
    return

# random generation extension
def generate_product_metadata(n_products):
    generate_product_metadata_manual(
        None,                       # product_name
        np.random.randint(1,5),     # unit_cost
        10, # placeholder           # unit_price
        np.random.randint(5,14),    # shelf_life_days
        np.random.randint(15, 20),  # min_order_qty
        10, # placeholder           # base_lead_time
    )

