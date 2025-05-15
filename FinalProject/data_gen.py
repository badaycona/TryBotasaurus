from sklearn.datasets import make_blobs
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.datasets import fetch_openml

def generate_blob_data(n_samples=1000, n_features=5, center=10):
    X, y_true=make_blobs(n_samples=n_samples, n_features=n_features, centers=center, random_state=0)
    return X, y_true

def generate_kcc99cup():
    kdd_data = fetch_openml('KDDCup99', version=1)
    X=kdd_data.data
    y_true=kdd_data.target

    np.random.seed(0)
    indices = np.random.choice(X.shape[0], size=5000, replace=False)
    X_sample=X[indices]
    y_true_sample=y_true[indices]
    
    pca=PCA(n_components=20)
    X_sample=pca.fit_transform(X_sample)
    X_sample=StandardScaler().fit_transform(X_sample)
    return X_sample, y_true_sample

def load_fashion_mnist_pca(n_components=2):
    fashion = fetch_openml("Fashion-MNIST", version=1, as_frame=False, parser="liac-arff")

    X = fashion.data
    y_true = fashion.target
    np.random.seed(0)
    indices = np.random.choice(X.shape[0], size=1000, replace=False)
    X=X[indices]
    y_true=y_true[indices]

    pca = PCA(n_components=n_components)
    X_pca = pca.fit_transform(X)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_pca)

    return X_scaled, y_true
if __name__=='__main__':
    kcc=load_fashion_mnist_pca()
    X, y_true=kcc
    print(X.shape)