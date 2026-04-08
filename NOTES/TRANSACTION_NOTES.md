for every store:

1. Load store metadata (store_id, capacity, reorder_point, delay_prob)

for every product:

2. Load product metadata (shelf_life, lead_time, min_order_qty)

3. Set initial state:

       opening_stock = capacity * 0.8
       pending_delivery = 0
       pending_delivery_day = None
  
4. For each day in the year:

    a. RECEIVE STOCK (if delivery is due today)

           units_received = pending_delivery if date == pending_delivery_day else 0

    b. CALCULATE DEMAND

           base = avg daily demand (capacity / shelf_life_days is a rough proxy)
           seasonal = check if today's month has a multiplier
           noise = truncated normal around 0
           actual_demand = int(base * seasonal + noise)

    c. CALCULATE SALES + STOCKOUT

           sales_fulfilled = min(actual_demand, opening_stock)
           stockout_units = actual_demand - sales_fulfilled

    d. CALCULATE SPOILAGE

           units_spoiled = int(opening_stock * daily_spoilage_rate)

    e. CALCULATE CLOSING STOCK

           closing_stock = opening_stock + units_received - sales_fulfilled - units_spoiled
           closing_stock = max(0, closing_stock)  # never negative

    f. DECIDE WHETHER TO ORDER

           reorder_point = max_inventory_capacity * reorder_point_factor

           if closing_stock < reorder_point:
               units_ordered = max_inventory_capacity - closing_stock
               units_ordered = max(units_ordered, min_order_qty)
               schedule delivery
               delay = 1 if random() < delay_probability else 0
               pending_delivery_day = date + lead_time_days + delay
               pending_delivery = units_ordered
           else:
               units_ordered = 0

    g. APPEND ROW to list

    h. SET next day's opening_stock = closing_stock

5. Write full year list to CSV