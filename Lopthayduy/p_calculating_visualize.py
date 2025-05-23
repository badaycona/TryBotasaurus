import single_p_value
import numpy as np
import scipy.stats as sp
import matplotlib.pyplot as plt

def main(debug = False):
    p_values = []
    smaller_than_alpha = 0
    alpha = 0.05
    for i in range(1000):
        p_value = single_p_value.example_two_tail()
        p_values.append(p_value)
        if p_value <= alpha:
            smaller_than_alpha += 1
    print(f'Percentage of p-values smaller than {alpha}: {smaller_than_alpha / 1000 * 100:.2f}%')
    plt.hist(p_values)
    plt.show()
if __name__ == '__main__':
    main()