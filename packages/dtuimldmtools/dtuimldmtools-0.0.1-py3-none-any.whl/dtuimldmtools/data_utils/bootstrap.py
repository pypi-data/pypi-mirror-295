import numpy as np


def bootstrap(X, y, N, weights="auto"):
    """
    function: X_bs, y_bs = bootstrap(X, y, N, weights)
    The function extracts the bootstrap set from given matrices X and y.
    The distribution of samples is determined by weights parameter
    (default: 'auto', equal weights).

    Usage:
        X_bs, y_bs = bootstrap(X, y, N, weights)

     Input:
         X: Estimated probability of class 1. (Between 0 and 1.)
         y: True class indices. (Equal to 0 or 1.)
         N: number of samples to be drawn
         weights: probability of occurence of samples (default: equal)

    Output:
        X_bs: Matrix with rows drawn randomly from X wrt given distribution
        y_bs: Matrix with rows drawn randomly from y wrt given distribution
    """
    if type(weights) is str and weights == "auto":
        weights = np.ones((X.shape[0], 1), dtype=float) / X.shape[0]
    else:
        weights = np.array(weights, dtype=float)
        weights = (weights / weights.sum()).ravel().tolist()

    # bc = np.random.multinomial(N, weights, 1).ravel()

    # selected_indices = []
    # while bc.sum()>0:
    #     selected_indices += np.where(bc>0)[0].tolist(); bc[bc>0]-=1
    # np.random.shuffle(selected_indices)

    selected_indices = np.random.choice(
        range(X.shape[0]), size=(N, 1), replace=True, p=weights
    ).flatten()
    if np.ndim(y) == 1:
        return X[selected_indices, :], y[selected_indices]
    else:
        return X[selected_indices, :], y[selected_indices, :]
