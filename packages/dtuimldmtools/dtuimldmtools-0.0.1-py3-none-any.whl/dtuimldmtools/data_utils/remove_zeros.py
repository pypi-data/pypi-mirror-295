import numpy as np


def remove_zero_cols(m):
    """
    Function removes from given matrix m the column vectors containing only zeros.

    Parameters:
        m (numpy.ndarray): The input matrix.

    Returns:
        numpy.ndarray: The matrix with zero columns removed.
    """
    rows = range(m.shape[0])
    cols = np.nonzero(sum(abs(m)))[1].tolist()[0]
    return m[np.ix_(rows, cols)]


def remove_zero_rows(m):
    """
    Function removes from given matrix m the row vectors containing only zeros.

    Parameters:
        m (numpy.ndarray): Input matrix

    Returns:
        numpy.ndarray: Matrix with zero rows removed
    """
    rows = np.nonzero(sum(abs(m.T)).T)[0].tolist()[0]
    cols = range(m.shape[1])
    return m[np.ix_(rows, cols)]


def remove_zero_rows_and_cols(m):
    """
    Function removes from given matrix m the row vectors and the column vectors containing only zeros.

    Parameters:
        m (numpy.ndarray): Input matrix

    Returns:
        numpy.ndarray: Matrix with zero rows and columns removed
    """
    rows = np.nonzero(sum(abs(m.T)).T)[0].tolist()[0]
    cols = np.nonzero(sum(abs(m)))[1].tolist()[0]
    return m[np.ix_(rows, cols)]
