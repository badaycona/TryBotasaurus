import cvxpy as cv
import numpy as np
beta = cv.Variable(2)

x = np.array([1, 2, 3])
x = x.reshape((3, 1))
print(x.shape)
one = np.ones((3, 1))
print(one.shape)
x = np.hstack([one, x])

y = np.array([2, 3, 5]).reshape((3, 1))

y.reshape((3, 1))
Q = 0.5 * x.T @ x
c = -x.T @ y
objective = cv.Minimize(cv.quad_form(beta, Q) + c.T @ beta )

problem = cv.Problem(objective)

problem.solve()

print(f'Optimal mse {objective.value :f}')
print(f'Optimal b0 : {beta[0].value:f}')
print(f'Optimal b1: {beta[1].value :f}')


