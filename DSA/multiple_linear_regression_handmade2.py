import numpy as np
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression

def generate_data(size, dimensions, true_beta):
    X = np.random.normal(loc=0, scale=1, size=(size, dimensions))
    true_beta = np.reshape(true_beta, shape = (dimensions, 1))
    noise = np.random.normal(loc=0, scale=1, size=(size,1))
    y = X @ true_beta + noise
    return X, y

size = 40
dimensions = 5
true_beta = [1, 0, 0.5, 2, 1]
X, y = generate_data(size,dimensions, true_beta)
model = LinearRegression()
model.fit(X, y)
print('Weight and bias', model.coef_, model.intercept_)
print('Accuracy', model.score(X,y))
