import numpy as np


class BinClassifierEnsemble:
    """
    A class to aggregate multiple weak classifiers into an ensemble.

    Attributes:
        classifiers (list): A list of weak classifiers.
        alpha (float or str): The weights assigned to each weak classifier. If 'auto', the weights are set to be equal.
        cn (int): The number of weak classifiers in the ensemble.

    Methods:
        __init__(classifier_list, alpha='auto'): Initializes the BinClassifierEnsemble object.
        predict(X): Returns the predicted class for the given input X based on ensemble majority vote.
        predict_proba(X): Returns the proportion of ensemble votes for class being y=1 for the given input X.
    """

    classifiers = []
    alpha = 0
    cn = 0

    def __init__(self, classifier_list, alpha="auto"):
        """
        Initializes the BinClassifierEnsemble object.

        Args:
            classifier_list (list): A list of weak classifiers.
            alpha (float or str): The weights assigned to each weak classifier. If 'auto', the weights are set to be equal.
        """
        self.classifiers = classifier_list
        self.cn = len(self.classifiers)
        if type(alpha) is str and alpha == "auto":
            self.alpha = np.ones((self.cn, 1), dtype=float) / self.cn
        else:
            self.alpha = np.asarray(alpha).ravel()

    def predict(self, X):
        """
        Returns the predicted class (value of y) for the given input X based on ensemble majority vote.

        Args:
            X (array-like): The input data.

        Returns:
            array-like: The predicted class for each input sample in X.
        """
        votes = np.zeros((X.shape[0], 1))
        for c_id, c in enumerate(self.classifiers):
            y_est = np.mat(c.predict(X)).T
            y_est[y_est > 1] = 1  # restrict to binomial (or first-vs-rest)
            votes = votes + y_est * self.alpha[c_id]
        return (votes.astype(float) > 0.5).astype(int)

    def predict_proba(self, X):
        """
        Returns the proportion of ensemble votes for class being y=1 for the given input X.

        Args:
            X (array-like): The input data.

        Returns:
            array-like: The proportion of ensemble votes for class being y=1 for each input sample in X.
        """
        votes = np.ones((X.shape[0], 1))
        for c_id, c in enumerate(self.classifiers):
            y_est = np.mat(c.predict(X)).T
            y_est[y_est > 1] = 1  # restrict to binomial (or first-vs-rest)
            votes = votes - y_est * self.alpha[c_id]
        return votes.astype(float)
