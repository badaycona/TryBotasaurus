# import numpy as np
# import matplotlib.pyplot as plt
# from sklearn.model_selection import train_test_split
# from sklearn.linear_model import LinearRegression

# # Step 1: Create synthetic data
# np.random.seed(0)
# X = np.random.rand(100, 2)  # 100 samples, 2 features
# y = 3 * X[:, 0] + 2 * X[:, 1] + np.random.randn(100) * 0.1  # target variable with some noise

# # Step 2: Split data into training and testing sets
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# # Step 3: Train a model
# model = LinearRegression()
# model.fit(X_train, y_train)

# # Step 4: Make predictions
# predictions = model.predict(X_test)

# # Step 5: Plot a histogram of the predictions
# plt.hist(predictions, bins=10, edgecolor='black')
# plt.title("Histogram of Model Predictions")
# plt.xlabel("Predicted Values")
# plt.ylabel("Frequency")
# plt.show()


import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# Step 1: Create synthetic data
np.random.seed(0)
X = np.random.rand(100, 2)  # 100 samples, 2 features
print(X)
y = 3 * X[:, 0] + 2 * X[:, 1] + np.random.randn(100) * 0.1  # target variable with some noise

# Step 2: Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# Step 3: Train a model
model = LinearRegression()
model.fit(X_train, y_train)

# Step 4: Make predictions
predictions = model.predict(X_test)

# 3D Scatter Plot
fig = plt.figure(figsize=(12, 6))
ax = fig.add_subplot(121, projection='3d')
ax.scatter(X_test[:, 0], X_test[:, 1], y_test, color='blue', label='Actual')
ax.scatter(X_test[:, 0], X_test[:, 1], predictions, color='red', marker='x', label='Predicted')
ax.set_xlabel("Feature 1")
ax.set_ylabel("Feature 2")
ax.set_zlabel("Target")
ax.set_title("3D Scatter Plot of Actual vs Predicted")
ax.legend()

# 3D Surface Plot of the Model's Predictions
# Create a mesh grid for surface plot
x_range = np.linspace(0, 1, 20)
y_range = np.linspace(0, 1, 20)
x_surf, y_surf = np.meshgrid(x_range, y_range)
z_surf = model.predict(np.c_[x_surf.ravel(), y_surf.ravel()]).reshape(x_surf.shape)

# Plot the surface
ax = fig.add_subplot(122, projection='3d')
ax.plot_surface(x_surf, y_surf, z_surf, color='lightgreen', alpha=0.6, edgecolor='w')
ax.scatter(X_test[:, 0], X_test[:, 1], y_test, color='blue', label='Actual')
ax.set_xlabel("Feature 1")
ax.set_ylabel("Feature 2")
ax.set_zlabel("Predicted Target")
ax.set_title("3D Surface Plot of Model Predictions")
plt.show()

