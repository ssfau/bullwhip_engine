import numpy as np
rng = np.random.default_rng()

def truncated_normal(mean, std_dev, min_val, max_val):
    while True:
        x = rng.normal(loc=mean, scale=std_dev) # Generate sample
        if min_val <= x <= max_val:
            return x
