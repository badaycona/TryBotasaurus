import torch 
import matplotlib.pyplot as plt

class SinglePerceptron:
    def __init__(self):
        self.weights = torch.randn(13,1)
        self.bias = torch.randn(1)
        self.train_losses=[]
        self.test_losses=[]
    def sigmoid(self, z):
        return 1 / (1 + np.exp(-z))
    
    def predict(self, X):
        z = X@self.weights + self.bias
        return self.sigmoid(z)
    
    def bce_loss(self, y_true, y_pred):
        return -torch.mean(y_true * torch.log(y_pred) + (1 - y_true) * torch.log(1 - y_pred))
    
    def fit(self, X_train, y_train, X_test, y_test, epochs=2000, lr=0.01):
        train_losses = []
        test_losses = []
        
        for epoch in range(epochs):
            # Forward pass
            y_pred = self.predict(X_train)
            
            # Compute loss
            loss = self.bce_loss(y_train, y_pred)
            self.train_losses.append(loss)
            
            # Backward pass
            error = y_pred - y_train.unsqueeze(dim=1)
            dW = X_train.T@error / len(X_train)
            db = torch.mean(error)
            
            # Update weights and bias
            self.weights -= lr * dW
            self.bias -= lr * db
            
            # Compute test loss
            y_test_pred = self.predict(X_test)
            test_loss = self.bce_loss(y_test, y_test_pred)
            self.test_losses.append(test_loss)

            if epoch % 100 == 0:
                print(f"Epoch {epoch}, Train Loss: {loss.item()}, Test Loss: {test_loss.item()}")
    
    def score(self, X, y):
        with torch.no_grad():
            y_pred = self.predict(X) >= 0.5
            accuracy = (y_pred == y).float().mean().item()
        return accuracy