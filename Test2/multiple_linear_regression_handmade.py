import numpy as np 
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression

def generate_data(size, dimension, true_beta):
    X = np.random.normal(loc = 0, scale = 1, size = (n, p))
    true_beta = np.reshape(true_beta, shape = (p, 1))

    noise = np.random.normal(loc = 0, scale = 1, size = (n, 1))
    y = X@true_beta + noise
    return X, y
n = 40
p = 5
true_beta = [2, 1, 0, 0.5, 1]
X, y = generate_data(n, p, true_beta)
model = LinearRegression()
model.fit(X,y)
print('Accuracy: ', model.score(X,y))

X=sm.add_constant(X)
beta_NE = np.linalg.inv(X.T @ X) @ X.T @ y
y_NE = X@beta_NE
meany= np.mean(y) * np.ones_like(y)
RSS = (y - y_NE).T @ (y - y_NE)
TSS = (y - meany).T @ (y - meany)
accu_NE = 1 - (RSS / TSS)
print('Accuracy',accu_NE[0, 0])

alpha_0 = 0.1
beta_GD = np.random.rand(6, 1)
for _ in range(10000):
    alpha = alpha_0 / (1 + 0.01 * _)
    gradient = (2 / n) * X.T @ (X @ beta_GD - y)
    beta_GD -= alpha * gradient 
y_GD = X @ beta_GD 
RSS = (y - y_GD).T @ (y - y_GD)
TSS = (y - meany).T @ (y - meany)
accu_GD = 1 - (RSS / TSS)
print('Accuracy ', accu_GD[0, 0])