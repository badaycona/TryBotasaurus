import numpy as np
def check_kkt_conditions(x, y, beta_hat, lam):
    """
    x : n*p
    y : n*1
    beta_hat : p * 1
    """
    # stationary: đạo hàm = 0
    # xét tại mỗi beta_j
    # -1/n * X_j.T @ (y - X @ beta) + lambda * s_j = 0 
    # Tất cả thoả mãn => KKT đúng
    # m * 1
    residual = y - x @ beta_hat

    # p * 1
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
    return np.all(results)