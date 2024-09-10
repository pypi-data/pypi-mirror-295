import numpy as np
from matplotlib import cm
from matplotlib import pyplot as plt
from sklearn import metrics
from sklearn.metrics import confusion_matrix

from ..clustering import gauss_2d


def bmplot(yt, xt, X):
    """
    Function plots matrix X as image with lines separating fields.

    Parameters:
    yt (list): List of labels for the y-axis.
    xt (list): List of labels for the x-axis.
    X (numpy.ndarray): Matrix to be plotted as an image.

    Returns:
    None
    """
    plt.imshow(X, interpolation="none", cmap="bone")
    plt.xticks(range(0, len(xt)), xt)
    plt.yticks(range(0, len(yt)), yt)
    for i in range(0, len(yt)):
        plt.axhline(i - 0.5, color="black")
    for i in range(0, len(xt)):
        plt.axvline(i - 0.5, color="black")


def dbplotf(X, y, fun, grid_range, resolution=100.0):
    """
    Plot the model prediction and decision boundary.

    Parameters:
    X (numpy.ndarray): Input features.
    y (numpy.ndarray): Target labels.
    fun (function): Function that predicts the values for the given coordinates.
    grid_range (str or list): Range of the grid. If 'auto', it is computed based on the minimum and maximum values of X.
    resolution (float): Resolution of the grid.

    Raises:
    ValueError: If the predicted values are not a vector or if all predictions are equal.

    Returns:
    None
    """
    # smoothness of color-coding:
    levels = 100
    # convert from one-out-of-k encoding, if necessary:
    if np.ndim(y) > 1:
        y = np.argmax(y, 1)
    # compute grid range if not given explicitly:
    if grid_range == "auto":
        grid_range = [
            X.min(axis=0)[0],
            X.max(axis=0)[0],
            X.min(axis=0)[1],
            X.max(axis=0)[1],
        ]

    delta_f1 = float(grid_range[1] - grid_range[0]) / float(resolution)
    delta_f2 = float(grid_range[3] - grid_range[2]) / float(resolution)
    f1 = np.arange(grid_range[0], grid_range[1], delta_f1)
    f2 = np.arange(grid_range[2], grid_range[3], delta_f2)
    F1, F2 = np.meshgrid(f1, f2)
    C = len(np.unique(y).tolist())
    # adjust color coding:
    if C == 2:
        C_colors = ["b", "r"]
        C_legend = ["Class A (y=0)", "Class B (y=1)"]
        C_levels = [0.5]
    if C == 3:
        C_colors = ["b", "g", "r"]
        C_legend = ["Class A (y=0)", "Class B (y=1)", "Class C (y=2)"]
        C_levels = [0.66, 1.34]
    if C == 4:
        C_colors = ["b", "w", "y", "r"]
        C_legend = ["Class A (y=0)", "Class B (y=1)", "Class C (y=2)", "Class D (y=3)"]
        C_levels = [0.74, 1.5, 2.26]
    if C > 4:
        # One way to get class colors for more than 4 classes. Note this may result in illegible figures!
        C_colors = []
        C_legend = []
        for c in range(C):
            C_colors.append(plt.cm.jet.__call__(c * 255 / (C - 1))[:3])
            C_legend.append("Class {0}".format(c))
        C_levels = [0.74, 1.5, 2.26]

    coords = np.mat([[f1[i], f2[j]] for i in range(len(f1)) for j in range(len(f2))])
    values_list = fun(coords)  # np.mat(classifier.predict(coords))
    if np.ndim(values_list) > 1:
        raise ValueError("Expected vector got something else")
    if len(set(values_list)) == 1:
        raise ValueError(
            "Expect multiple predicted value, but all predictions are equal. Try a more complex model"
        )

    if values_list.shape[0] != len(f1) * len(f2):
        values_list = values_list.T

    values = np.asarray(np.reshape(values_list, (len(f1), len(f2))).T)

    # hold(True)
    for c in range(C):
        cmask = y == c
        plt.plot(X[cmask, 0], X[cmask, 1], ".", color=C_colors[c], markersize=10)
    plt.title("Model prediction and decision boundary")
    plt.xlabel("Feature 1")
    plt.ylabel("Feature 2")
    plt.contour(F1, F2, values, levels=C_levels, colors=["k"], linestyles="dashed")
    plt.contourf(
        F1,
        F2,
        values,
        levels=np.linspace(values.min(), values.max(), levels),
        cmap=plt.cm.jet,
        origin="image",
    )
    plt.colorbar(format="%.1f")
    plt.legend(C_legend)


def dbplot(classifier, X, y, grid_range, resolution=100):
    """
    Plot decision boundary for a given binomial or multinomial classifier.

    Parameters:
    classifier (object): The trained classifier object.
    X (array-like): The input features.
    y (array-like): The target labels.
    grid_range (str or list): The range of the grid. If 'auto', it will be computed based on the minimum and maximum values of X.
    resolution (int): The number of points in the grid.

    Returns:
    None
    """

    # smoothness of color-coding:
    levels = 100
    # convert from one-out-of-k encoding, if necessary:
    if np.ndim(y) > 1:
        y = np.argmax(y, 1)
    # compute grid range if not given explicitly:
    if grid_range == "auto":
        grid_range = [X.min(0)[0], X.max(0)[0], X.min(0)[1], X.max(0)[1]]

    delta_f1 = float(grid_range[1] - grid_range[0]) / resolution
    delta_f2 = float(grid_range[3] - grid_range[2]) / resolution
    f1 = np.arange(grid_range[0], grid_range[1], delta_f1)
    f2 = np.arange(grid_range[2], grid_range[3], delta_f2)
    F1, F2 = np.meshgrid(f1, f2)
    C = len(np.unique(y).tolist())
    # adjust color coding:
    if C == 2:
        C_colors = ["b", "r"]
        C_legend = ["Class A (y=0)", "Class B (y=1)"]
        C_levels = [0.5]
    if C == 3:
        C_colors = ["b", "g", "r"]
        C_legend = ["Class A (y=0)", "Class B (y=1)", "Class C (y=2)"]
        C_levels = [0.66, 1.34]
    if C == 4:
        C_colors = ["b", "w", "y", "r"]
        C_legend = ["Class A (y=0)", "Class B (y=1)", "Class C (y=2)", "Class D (y=3)"]
        C_levels = [0.74, 1.5, 2.26]
    if C > 4:
        # One way to get class colors for more than 4 classes. Note this may result in illegible figures!
        C_colors = []
        C_legend = []
        for c in range(C):
            C_colors.append(plt.cm.jet.__call__(c * 255 / (C - 1))[:3])
            C_legend.append("Class {0}".format(c))
        C_levels = [0.74, 1.5, 2.26]

    coords = np.array([[f1[i], f2[j]] for i in range(len(f1)) for j in range(len(f2))])
    values_list = classifier.predict(coords)
    if values_list.shape[0] != len(f1) * len(f2):
        values_list = values_list.T
    values = np.reshape(values_list, (len(f1), len(f2))).T

    # hold(True)
    for c in range(C):
        cmask = y == c
        plt.plot(X[cmask, 0], X[cmask, 1], ".", color=C_colors[c], markersize=10)
    plt.title("Model prediction and decision boundary")
    plt.xlabel("Feature 1")
    plt.ylabel("Feature 2")
    plt.contour(F1, F2, values, levels=C_levels, colors=["k"], linestyles="dashed")
    plt.contourf(
        F1,
        F2,
        values,
        levels=np.linspace(values.min(), values.max(), levels),
        cmap=plt.cm.jet,
        origin="image",
    )
    plt.colorbar(format="%.1f")
    plt.legend(C_legend)


def dbprobplot(classifier, X, y, grid_range, resolution=100):
    """
    Plot decision boundary for a given binomial classifier.

    Parameters:
    classifier (object): The trained classifier object.
    X (array-like): The input features.
    y (array-like): The target labels.
    grid_range (str or list): The range of the grid. If 'auto', it will be computed based on the input features.
    resolution (int): The resolution of the grid.

    Returns:
    None
    """

    # smoothness of color-coding:
    levels = 100
    # convert from one-out-of-k encoding, if necessary:
    if np.ndim(y) > 1:
        y = np.argmax(y, 1)
    # compute grid range if not given explicitly:
    if grid_range == "auto":
        grid_range = [X.min(0)[0], X.max(0)[0], X.min(0)[1], X.max(0)[1]]
    # if more than two classes, display the first class against the rest:
    y[y > 1] = 1
    C = 2
    C_colors = ["b", "r"]
    C_legend = ["Class A (y=0)", "Class B (y=1)"]
    C_levels = [0.5]

    delta_f1 = float(grid_range[1] - grid_range[0]) / resolution
    delta_f2 = float(grid_range[3] - grid_range[2]) / resolution
    f1 = np.arange(grid_range[0], grid_range[1], delta_f1)
    f2 = np.arange(grid_range[2], grid_range[3], delta_f2)
    F1, F2 = np.meshgrid(f1, f2)

    coords = np.array([[f1[i], f2[j]] for i in range(len(f1)) for j in range(len(f2))])
    values_list = classifier.predict_proba(coords)
    if values_list.shape[0] != len(f1) * len(f2):
        values_list = values_list.T
    values_list = 1 - values_list[:, 0]  # probability of class being y=1
    values = np.reshape(values_list, (len(f1), len(f2))).T

    # hold(True)
    for c in range(C):
        cmask = y == c
        plt.plot(X[cmask, 0], X[cmask, 1], ".", color=C_colors[c], markersize=10)
    plt.title("Model prediction and decision boundary")
    plt.xlabel("Feature 1")
    plt.ylabel("Feature 2")

    plt.contour(F1, F2, values, levels=C_levels, colors=["k"], linestyles="dashed")
    plt.contourf(
        F1,
        F2,
        values,
        levels=np.linspace(values.min(), values.max(), levels),
        cmap=cm.jet,
        origin="image",
    )
    plt.colorbar(format="%.1f")
    plt.legend(C_legend)


def rocplot(p, y):
    """
    Plots the receiver operating characteristic (ROC) curve and calculates the area under the curve (AUC).

    Args:
        p (array-like): Estimated probability of class 1. Values should be between 0 and 1.
        y (array-like): True class indices. Values should be equal to 0 or 1.

    Returns:
        float: The area under the ROC curve (AUC).
        array-like: True positive rate (TPR).
        array-like: False positive rate (FPR).
    """

    fpr, tpr, thresholds = metrics.roc_curve(y, p)
    AUC = metrics.roc_auc_score(y, p)
    plt.plot(fpr, tpr, "r", [0, 1], [0, 1], "k")
    plt.grid()
    plt.xlim([-0.01, 1.01])
    plt.ylim([-0.01, 1.01])
    plt.xticks(np.arange(0, 1.1, 0.1))
    plt.yticks(np.arange(0, 1.1, 0.1))
    plt.xlabel("False positive rate (1-Specificity)")
    plt.ylabel("True positive rate (Sensitivity)")
    plt.title("Receiver operating characteristic (ROC)\n AUC={:.3f}".format(AUC))

    return AUC, tpr, fpr


def confmatplot(y_true, y_est):
    """
    The function plots confusion matrix for classification results.

    Usage:
        confmatplot(y_true, y_estimated)

     Input:
         y_true: Vector of true class labels.
         y_estimated: Vector of estimated class labels.

     Output:
         None
    """

    y_true = np.asarray(y_true).ravel()
    y_est = np.asarray(y_est).ravel()
    C = np.unique(y_true).shape[0]
    cm = confusion_matrix(y_true, y_est)
    accuracy = 100 * cm.diagonal().sum() / cm.sum()
    error_rate = 100 - accuracy
    plt.imshow(cm, cmap="binary", interpolation="None")
    plt.colorbar(format="%.2f")
    plt.xticks(range(C))
    plt.yticks(range(C))
    plt.xlabel("Predicted class")
    plt.ylabel("Actual class")
    plt.title(
        "Confusion matrix (Accuracy: {:}%, Error Rate: {:}%)".format(
            accuracy, error_rate
        )
    )


def clusterplot(X, clusterid, centroids="None", y="None", covars="None"):
    """
    CLUSTERPLOT Plots a clustering of a data set as well as the true class
    labels. If data is more than 2-dimensional it should be first projected
    onto the first two principal components. Data objects are plotted as a dot
    with a circle around. The color of the dot indicates the true class,
    and the cicle indicates the cluster index. Optionally, the centroids are
    plotted as filled-star markers, and ellipsoids corresponding to covariance
    matrices (e.g. for gaussian mixture models).

    Usage:
    clusterplot(X, clusterid)
    clusterplot(X, clusterid, centroids=c_matrix, y=y_matrix)
    clusterplot(X, clusterid, centroids=c_matrix, y=y_matrix, covars=c_tensor)

    Input:
    X           N-by-M data matrix (N data objects with M attributes)
    clusterid   N-by-1 vector of cluster indices
    centroids   K-by-M matrix of cluster centroids (optional)
    y           N-by-1 vector of true class labels (optional)
    covars      M-by-M-by-K tensor of covariance matrices (optional)
    """

    X = np.asarray(X)
    cls = np.asarray(clusterid)
    if type(y) is str and y == "None":
        y = np.zeros((X.shape[0], 1))
    else:
        y = np.asarray(y)
    if type(centroids) is not str:
        centroids = np.asarray(centroids)
    K = np.size(np.unique(cls))
    C = np.size(np.unique(y))
    ncolors = np.max([C, K])

    # plot data points color-coded by class, cluster markers and centroids
    # hold(True)
    colors = [0] * ncolors
    for color in range(ncolors):
        colors[color] = plt.cm.jet(color / (ncolors - 1))[:3]
    for i, cs in enumerate(np.unique(y)):
        plt.plot(
            X[(y == cs).ravel(), 0],
            X[(y == cs).ravel(), 1],
            "o",
            markeredgecolor="k",
            markerfacecolor=colors[i],
            markersize=6,
            zorder=2,
        )
    for i, cr in enumerate(np.unique(cls)):
        plt.plot(
            X[(cls == cr).ravel(), 0],
            X[(cls == cr).ravel(), 1],
            "o",
            markersize=12,
            markeredgecolor=colors[i],
            markerfacecolor="None",
            markeredgewidth=3,
            zorder=1,
        )
    if type(centroids) is not str:
        for cd in range(centroids.shape[0]):
            plt.plot(
                centroids[cd, 0],
                centroids[cd, 1],
                "*",
                markersize=22,
                markeredgecolor="k",
                markerfacecolor=colors[cd],
                markeredgewidth=2,
                zorder=3,
            )
    # plot cluster shapes:
    if type(covars) is not str:
        for cd in range(centroids.shape[0]):
            x1, x2 = gauss_2d(centroids[cd], covars[cd, :, :])
            plt.plot(x1, x2, "-", color=colors[cd], linewidth=3, zorder=5)

    # create legend
    legend_items = (
        np.unique(y).tolist() + np.unique(cls).tolist() + np.unique(cls).tolist()
    )
    for i in range(len(legend_items)):
        if i < C:
            legend_items[i] = "Class: {0}".format(legend_items[i])
        elif i < C + K:
            legend_items[i] = "Cluster: {0}".format(legend_items[i])
        else:
            legend_items[i] = "Centroid: {0}".format(legend_items[i])
    plt.legend(legend_items, numpoints=1, markerscale=0.75, prop={"size": 9})
