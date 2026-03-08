from pydantic import BaseModel, Field, field_validator, model_validator
from datetime import date

# METADATA

class Store(BaseModel): # in context of small community run stores
    store_id: int
    store_name: str = Field(min_length=1, max_length=50)
    max_inventory_capacity: int = Field(ge=40, le=160) # in units
    reorder_point_factor: float = Field(ge=0.3, le=0.7)
    delay_probability: float = Field(ge=0.1, le=0.5) # value between 0 to 1
    holding_cost_rate: float = Field(ge=0.05, le=0.15) # how much it costs to keep 1 unit in stock per day

class Product(BaseModel):
    product_id: int = Field(gt=0)
    product_name: str = Field(min_length=1, max_length=50)
    unit_cost: float = Field(gt=0)
    unit_price: float 
    shelf_life_days: int = Field(gt=5, le=14) # leafy greens only
    min_order_qty: int = Field(ge=15)
    base_lead_time: int = Field(gt=0, le=3)

    # field cross check requirements
    @model_validator(mode='after')
    def check_cost_order(self) -> 'Product':
        if self.unit_cost > self.unit_price:
            raise ValueError('unit cost must be less than unit price')
        if self.base_lead_time > self.shelf_life_days:
            raise ValueError('base lead time must be less than shelf life days')
        return self

# TRANSACTION DATA

class Transaction(BaseModel):
    date: date # YYYY-MM-DD format
    store_id: int
    product_id: int
    actual_demand: int # by unit
    sales_fulfilled: int # by unit
    stockout_units: int 
    inventory_on_hand: int # by total units of this specific product
    units_ordered: int 
    units_received: int
    units_spoiled: int

