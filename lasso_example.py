import numpy as np
from sklearn.linear_model import Lasso
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import check_kkt_conditions
MAX_ITERATE = 10000
def soft_thresholding(rho, lam, z):
    if rho < -lam:
        return (rho + lam) / z
    elif rho > lam:
        return (rho - lam) / z
    else:
        return 0
def coordinate_descent_lasso(X, y, lam, num_iter = MAX_ITERATE):
    n, p = X.shape
    beta = np.random.rand(p)
    residual = y - X @ beta
    for _ in range(num_iter):
        for j in range(p):
            r_j = residual + X[:, j] * beta[j]

            rho_j = 1/n * X[:, j].T @ r_j
            z = 1/n * (X[:, j] ** 2).sum()

            beta[j] = soft_thresholding(rho_j, lam, z) 

            residual = r_j - X[:, j] * beta[j]
    sigma = np.sum(np.mean(X, axis = 0) * beta) 
    intercept = np.mean(y) - sigma
    return beta, intercept
def main_model():
    np.random.seed(0)

    x, y = make_regression(n_samples = 1000, n_features = 20, n_informative = 5, noise = 1, random_state = 0)

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state = 0)

    
    scaler = StandardScaler()
    x_train = scaler.fit_transform(x_train)
    x_test = scaler.transform(x_test)
    # x_train : n*p
    # y_train : n*1
    # beta : p * 1
    coef, intercept = coordinate_descent_lasso(x_train, y_train, lam=1)
    

    print(f'By-hand algorithm  coef: {coef}')
    print(f'By-hand algorithm intercept {intercept}')

    model = Lasso(alpha = 1)
    model.fit(x_train, y_train)

    beta_hat = model.coef_

    print(f' Lasso coefficients: {beta_hat}')
    print(f' Lasso intercept: {model.intercept_}')
    # print(f' Lasso score: {model.score(x_test, y_test)}')

    # print(f'Checking kkt condition for each features')

    satisfied = check_kkt_conditions.check_kkt_conditions(x_train, y_train, beta_hat, 1)
    print(satisfied)
    print(x_train.shape, y_train.shape)
    return model, x_train, y_train


if __name__ == "__main__": 
    main_model()