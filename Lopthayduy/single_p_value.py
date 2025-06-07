import numpy as np
import scipy.stats as sp
def example_two_tail(debug = False):
    # Generate synthetic data
    # Data pha ke
    mu = 0
    std = 1 

    # Generate a random sample from a normal distribution
    # chọn 1 giá trị duy nhất
    x = np.random.normal(loc = mu, scale = std,size = 5)[3]

    # We want to test the following hypotheses
    # H_0: mu = 0   vs.   H_1: mu != 0


    # cdf = cumulative distribution function
    # xét biến ngẫu nhiên Z theo phân phối chuẩn, cdf là P(Z <= mean_of_x)
    cdf = sp.norm.cdf(x, loc = mu, scale = std)
    # p_value
    p_value =  2 * min(cdf, 1 - cdf)
    if debug:
        print(x)
        print(f'p-value: {p_value}')
    return p_value

if __name__ == '__main__':
    example_two_tail(True)
    

