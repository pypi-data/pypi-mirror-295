import numpy as np


def get_data_ranges(x):
    """
    Determine minimum and maximum for each feature in input x and output as
    numpy array.

    Args:
            x:          An array of shape (N,M), where M corresponds to
                        features and N corresponds to observations.

    Returns:
            ranges:     A numpy array of minimum and maximum values for each
                        feature dimension.
    """
    N, M = x.shape
    ranges = []
    for m in range(M):
        ranges.append(np.min(x[:, m]))
        ranges.append(np.max(x[:, m]))
    return np.array(ranges)
