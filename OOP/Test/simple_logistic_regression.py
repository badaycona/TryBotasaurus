import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score


def generate_data(n):
    X = []
    y = []
    for i in range(n):
        if i <= n/2:
            X.append(np.random.nonrmal(loc=4, scale=1))
            y.append(0)
        else:
            X.append(np.random.normal(loc=8, scale=1))
            y.append(1)

    return np.array(X).reshape(n, 1), np.array(y)


n_train = 80
n_test = 20
X_train, y_train = generate_data(n_train)
X_test, y_test = generate_data(n_test)

plt.scatter(X_train, y_train, c=y_train)
plt.show()

classifier = LogisticRegression()
classifier.fit(X_train, y_train)

y_pred = classifier.predict(X_test)
print(y_pred)
print(y_test)

print('Accuracy: ', accuracy_score(y_pred, y_test))




