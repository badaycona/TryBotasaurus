import lasso_example
import numpy as np
import scipy.stats as sp

def main():
    model, x, y = lasso_example.main_model()

    #Calculating p-value for each informative features
    #Null hypothesis H_0 : beta_hat_j == 0 | Alternative hypothesis H_1 : beta_hat_j != 0
    # <=> feature j có giá trị tính toán hay không
    beta_hat = model.coef_
    active_set = np.where(beta_hat != 0)
    
    pass


if __name__ == '__main__':
    main()