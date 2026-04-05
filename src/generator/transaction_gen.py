import pandas as pd
import numpy as np
import src.utils as utils

from pathlib import Path
from config.schemas.raw import Transaction

script = Path(__file__).resolve().parent

# TRANSACTION DATA HANDLING

def generate_transaction_data_by_year(year):
    return