import math



def compute_cycle_period(*args):
    
    
    
    hyper_period = 1
    for period in args:
        hyper_period = int(period) * int(hyper_period) / math.gcd(int(period), int(hyper_period))
    return int(hyper_period)
