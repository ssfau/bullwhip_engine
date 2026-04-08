import numpy as np
from scipy.stats import truncnorm
rng = np.random.default_rng()

def truncated_normal(mean, std_dev, min_val, max_val):
    a = (min_val - mean) / std_dev
    b = (max_val - mean) / std_dev
    return truncnorm.rvs(a, b, loc=mean, scale=std_dev)
