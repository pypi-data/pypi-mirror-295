import numpy as np
import sklearn.metrics.cluster as cluster_metrics


def gauss_2d(centroid, ccov, std=2, points=100):
    """
    Returns two vectors representing slice through gaussian, cut at given standard deviation.

    Parameters:
    centroid (array-like): The centroid of the Gaussian distribution.
    ccov (array-like): The covariance matrix of the Gaussian distribution.
    std (float, optional): The standard deviation at which to cut the Gaussian distribution. Default is 2.
    points (int, optional): The number of points to sample along the slice. Default is 100.

    Returns:
    tuple: A tuple containing two vectors representing the slice through the Gaussian distribution.
    """
    mean = np.c_[centroid]
    tt = np.c_[np.linspace(0, 2 * np.pi, points)]
    x = np.cos(tt)
    y = np.sin(tt)
    ap = np.concatenate((x, y), axis=1).T
    d, v = np.linalg.eig(ccov)
    d = std * np.sqrt(np.diag(d))
    bp = np.dot(v, np.dot(d, ap)) + np.tile(mean, (1, ap.shape[1]))
    return bp[0, :], bp[1, :]


def gausKernelDensity(X, width):
    """
    GAUSKERNELDENSITY Calculate efficiently leave-one-out Gaussian Kernel Density estimate
    Input:
        X        N x M data matrix
        width    variance of the Gaussian kernel

    Output:
        density        vector of estimated densities
        log_density    vector of estimated log_densities
    """
    X = np.mat(np.asarray(X))
    N, M = X.shape

    # Calculate squared euclidean distance between data points
    # given by ||x_i-x_j||_F^2=||x_i||_F^2-2x_i^Tx_j+||x_i||_F^2 efficiently
    x2 = np.square(X).sum(axis=1)
    D = x2[:, [0] * N] - 2 * X.dot(X.T) + x2[:, [0] * N].T

    # Evaluate densities to each observation
    Q = np.exp(-1 / (2.0 * width) * D)
    # do not take density generated from the data point itself into account
    Q[np.diag_indices_from(Q)] = 0
    sQ = Q.sum(axis=1)

    density = 1 / ((N - 1) * np.sqrt(2 * np.pi * width) ** M + 1e-100) * sQ
    log_density = -np.log(N - 1) - M / 2 * np.log(2 * np.pi * width) + np.log(sQ)
    return np.asarray(density), np.asarray(log_density)


def clusterval(y, clusterid):
    """
    CLUSTERVAL Estimate cluster validity using Entropy, Purity, Rand Statistic,
    and Jaccard coefficient.

    Usage:
      Entropy, Purity, Rand, Jaccard = clusterval(y, clusterid);

    Input:
       y         N-by-1 vector of class labels
       clusterid N-by-1 vector of cluster indices

    Output:
      Entropy    Entropy measure.
      Purity     Purity measure.
      Rand       Rand index.
      Jaccard    Jaccard coefficient.

    Calculates the cluster validity measures including Entropy, Purity, Rand Statistic,
    and Jaccard coefficient for evaluating the quality of clustering results.

    Parameters:
        y (numpy.ndarray): N-by-1 vector of class labels.
        clusterid (numpy.ndarray): N-by-1 vector of cluster indices.

    Returns:
        tuple: A tuple containing the following cluster validity measures:
            - Entropy (float): Entropy measure.
            - Purity (float): Purity measure.
            - Rand (float): Rand index.
            - Jaccard (float): Jaccard coefficient.
    """
    NMI = cluster_metrics.normalized_mutual_info_score(y, clusterid)

    # y = np.asarray(y).ravel(); clusterid = np.asarray(clusterid).ravel()
    C = np.unique(y).size
    K = np.unique(clusterid).size
    N = y.shape[0]
    EPS = 2.22e-16

    p_ij = np.zeros(
        (K, C)
    )  # probability that member of i'th cluster belongs to j'th class
    m_i = np.zeros((K, 1))  # total number of objects in i'th cluster
    for k in range(K):
        m_i[k] = (clusterid == k).sum()
        yk = y[clusterid == k]
        for c in range(C):
            m_ij = (yk == c).sum()  # number of objects of j'th class in i'th cluster
            p_ij[k, c] = m_ij.astype(float) / m_i[k]
    entropy = ((1 - (p_ij * np.log2(p_ij + EPS)).sum(axis=1)) * m_i.T).sum() / (N * K)
    purity = (p_ij.max(axis=1)).sum() / K

    f00 = 0
    f01 = 0
    f10 = 0
    f11 = 0
    for i in range(N):
        for j in range(i):
            if y[i] != y[j] and clusterid[i] != clusterid[j]:
                f00 += 1
                # different class, different cluster
            elif y[i] == y[j] and clusterid[i] == clusterid[j]:
                f11 += 1
                # same class, same cluster
            elif y[i] == y[j] and clusterid[i] != clusterid[j]:
                f10 += 1
                # same class, different cluster
            else:
                f01 += 1
                # different class, same cluster
    rand = float(f00 + f11) / (f00 + f01 + f10 + f11)
    jaccard = float(f11) / (f01 + f10 + f11)

    return rand, jaccard, NMI
