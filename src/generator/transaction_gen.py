import pandas as pd
import numpy as np
from datetime import date
import src.utils as utils

from pathlib import Path
from config.schemas.raw import Transaction

script = Path(__file__).resolve().parent

# TRANSACTION DATA HANDLING
""" this function returns dataframe of a csv by automatically selecting type """
def get_df_metadata_csv(type):
    csv_path = script.parent / 'data' / 'raw' / 'metadata'
    if type == "store":
        csv_path = csv_path / 'store.csv'
    elif type == "product":
        csv_path = csv_path / 'product.csv'
    else:
        raise ValueError("Invalid type")

    df = pd.read_csv(csv_path)
    
    return df

def generate_transaction_data_store_by_year(store_id, year):
    # loading variables

    storedf = get_df_metadata_csv('store')

    filtered = storedf[storedf['store_id'] == store_id]
    if not filtered.empty:
        row = filtered.iloc[0]
    else:
        raise ValueError('store not found')

    ## loading store metadata

    print("generating for store: ", row.store_name)
    max_inventory_capacity = row.max_inventory_capacity
    reorder_point_factor = row.reorder_point_factor
    delay_probability = row.delay_probability
    holding_cost_rate = row.holding_cost_rate

    

    start = pd.Timestamp(year=year, month=1, day=1)
    end = pd.Timestamp(year=year, month=12, day=31)

    

    ## loading product metadata for each product
    productdf = get_df_metadata_csv('product')

    # initializing rememberance state values for products
    product_state = {}
    for productrow in productdf.itertuples():
        product_state[productrow.product_id] = {
            'opening_stock': max_inventory_capacity * 0.8,
            'pending_deliveries': [] # tuple format: (arrival_day, units)
        }

    ## loop through the year and generate for every product on a daily basis

    for day in pd.date_range(start=start, end=end):
        for productrow in productdf.itertuples():
            
            print("generating for product: " , productrow.product_name)
            
            unit_cost = productrow.unit_cost
            unit_price = productrow.unit_price
            shelf_life_days = productrow.shelf_life_days
            min_order_qty = productrow.min_order_qty
            base_lead_time = productrow.base_lead_time
            units_received = 0

            pid = productrow.product_id
        
            # read state for this product
            opening_stock = product_state[pid]['opening_stock']
            pending_deliveries = product_state[pid]['pending_deliveries'] # tuple format: (arrival_day, units)
            
            for arrival_day, qty in pending_deliveries[:]:
                if day == arrival_day:
                    units_received = qty
                    opening_stock += qty
                    pending_deliveries.remove((arrival_day, qty))

            # demand calculation
            base = max_inventory_capacity / shelf_life_days
            seasonal = 1.0 # place holder
            noise = utils.truncated_normal(
                mean=0.0,
                std_dev=base*0.15,
                min_val=-base*0.3,
                max_val=base*0.3
            )
            actual_demand = max(0, int(base * seasonal + noise))

            # extra calculations for sales, stockout and spoilage
            sales_fulfilled = min(actual_demand, opening_stock)
            stockout_units = actual_demand - sales_fulfilled
            units_spoiled = int(opening_stock * (1 / shelf_life_days))  # pyright: ignore[reportOperatorIssue]
            
            # closing stock
            closing_stock = opening_stock + units_received - sales_fulfilled - units_spoiled
            closing_stock = max(0, closing_stock)  

            # deliver new items

            reorder_point = max_inventory_capacity * reorder_point_factor

            if closing_stock < reorder_point:
                units_ordered = max_inventory_capacity - closing_stock
                units_ordered = max(units_ordered, min_order_qty) # pyright: ignore[reportArgumentType, reportOperatorIssue]
                delay = 1 if utils.rng.random() < delay_probability else 0

                pending_delivery_day = day + pd.Timedelta(days=base_lead_time + utils.rng.integers(0, 2) + delay) # pyright: ignore[reportArgumentType, reportOperatorIssue]
                pending_deliveries.append((pending_delivery_day, units_ordered))
            else:
                units_ordered = 0

            # row append placeholder

            # update state
            product_state[pid]['opening_stock'] = closing_stock
            product_state[pid]['pending_deliveries'] = pending_deliveries
            
    return