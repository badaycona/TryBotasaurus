import numpy as np
from sklearn.linear_model import Lasso
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
def main_model():
    np.random.seed(0)

    x, y = make_regression(n_samples = 1000, n_features = 20, n_informative = 5, noise = 0.1, random_state = 0)

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state = 0)


    scaler = StandardScaler()
    x_train = scaler.fit_transform(x_train)
    x_test = scaler.transform(x_test)

    model = Lasso(alpha = 1)
    model.fit(x_train, y_train)

    beta_hat = model.coef_

    print(f' Lasso coefficients: {beta_hat}')
    print(f' Lasso intercept: {model.intercept_}')
    print(f' Lasso score: {model.score(x_test, y_test)}')

    print(f'Checking kkt condition for each features')
    satisfied = check_kkt_conditions(x_train, y_train, beta_hat, 1)
    print(satisfied)
    return model, x_train, y_train

def check_kkt_conditions(x, y, beta_hat, lam):
    """
    x : m*n
    y : m*1
    beta_hat : n * 1
    """
    # m * 1
    residual = y - x @ beta_hat

    # n * 1
    xTy = x.T @ residual
    results = []
    for j in range(x.shape[1]):
        if beta_hat[j] != 0:
            expected = lam * np.sign(beta_hat[j])
            if not np.isclose(xTy[j], expected, atol = 1e-4):
                results.append(True)
            else:
                results.append(False)
        else:
            if np.abs(xTy[j]) > lam + 1e-6:
                results.append(True)
            else:
                results.append(False)
    return results

if __name__ == "__main__":
    main_model()