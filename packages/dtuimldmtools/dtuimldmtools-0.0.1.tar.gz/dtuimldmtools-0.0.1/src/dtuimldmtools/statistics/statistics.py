import numpy as np
import scipy.stats
import scipy.stats as st


def correlated_ttest(r, rho, alpha=0.05):
    """
    Perform a correlated t-test on a given set of correlation coefficients.

    Parameters:
    - r (array-like): Array of correlation coefficients.
    - rho (float): The assumed population correlation coefficient.
    - alpha (float, optional): The significance level for the test. Default is 0.05.

    Returns:
    - p (float): The p-value of the test.
    - CI (tuple): The confidence interval of the test.

    """
    rhat = np.mean(r)
    shat = np.std(r)
    J = len(r)
    sigmatilde = shat * np.sqrt(1 / J + rho / (1 - rho))

    CI = st.t.interval(
        1 - alpha, df=J - 1, loc=rhat, scale=sigmatilde
    )  # Confidence interval
    p = 2 * st.t.cdf(-np.abs(rhat) / sigmatilde, df=J - 1)  # p-value
    return p, CI


def jeffrey_interval(y, yhat, alpha=0.05):
    """
    Calculate the Jeffrey's interval for a binary classification problem.

    Parameters:
    y (numpy.ndarray): The true labels of the binary classification problem.
    yhat (numpy.ndarray): The predicted labels of the binary classification problem.
    alpha (float, optional): The significance level for the confidence interval. Default is 0.05.

    Returns:
    tuple: A tuple containing the estimated parameter (thetahat) and the confidence interval (CI).
    """
    m = sum(y - yhat == 0)
    n = y.size
    a = m + 0.5
    b = n - m + 0.5
    CI = scipy.stats.beta.interval(1 - alpha, a=a, b=b)
    thetahat = a / (a + b)
    return thetahat, CI


def ttest_onemodel(y_true, yhat, loss_norm_p=1, alpha=0.05):
    """
    Perform a statistical comparison of the models using t-test.

    Parameters:
    - y_true: array-like, true values of the target variable.
    - yhat: array-like, predicted values of the target variable.
    - loss_norm_p: int, optional, the norm to be used for computing the squared error. Default is 1.
    - alpha: float, optional, significance level for the confidence interval. Default is 0.05.

    Returns:
    - mean_squared_error: float, the mean squared error between y_true and yhat.
    - confidence_interval: tuple, the confidence interval for the mean squared error.
    """
    zA = np.abs(y_true - yhat) ** loss_norm_p
    CI = st.t.interval(1 - alpha, df=len(zA) - 1, loc=np.mean(zA), scale=st.sem(zA))
    return np.mean(zA), CI


def ttest_twomodels(y_true, yhatA, yhatB, alpha=0.05, loss_norm_p=1):
    """
    Perform a two-sample t-test on the predicted values of two models.

    Parameters:
    - y_true: array-like, true values
    - yhatA: array-like, predicted values of model A
    - yhatB: array-like, predicted values of model B
    - alpha: float, significance level (default=0.05)
    - loss_norm_p: int, norm order for loss calculation (default=1)

    Returns:
    - mean_diff: float, mean difference between the predicted values of model A and model B
    - confidence_interval: tuple, confidence interval of the mean difference
    - p_value: float, p-value of the null hypothesis that the mean difference is zero
    """
    zA = np.abs(y_true - yhatA) ** loss_norm_p
    zB = np.abs(y_true - yhatB) ** loss_norm_p

    z = zA - zB
    CI = st.t.interval(1 - alpha, len(z) - 1, loc=np.mean(z), scale=st.sem(z))
    p = 2 * st.t.cdf(-np.abs(np.mean(z)) / st.sem(z), df=len(z) - 1)
    return np.mean(z), CI, p


def mcnemar(y_true, yhatA, yhatB, alpha=0.05):
    """
    Perform McNemar's test to compare the accuracy of two classifiers.

    Parameters:
    - y_true: array-like, true labels
    - yhatA: array-like, predicted labels by classifier A
    - yhatB: array-like, predicted labels by classifier B
    - alpha: float, significance level (default: 0.05)

    Returns:
    - thetahat: float, estimated difference in accuracy between classifiers A and B
    - CI: tuple, confidence interval of the estimated difference in accuracy
    - p: float, p-value for the two-sided test of whether classifiers A and B have the same accuracy
    """

    nn = np.zeros((2, 2))
    c1 = yhatA - y_true == 0
    c2 = yhatB - y_true == 0

    nn[0, 0] = sum(c1 & c2)
    nn[0, 1] = sum(c1 & ~c2)
    nn[1, 0] = sum(~c1 & c2)
    nn[1, 1] = sum(~c1 & ~c2)

    n = sum(nn.flat)
    n12 = nn[0, 1]
    n21 = nn[1, 0]

    thetahat = (n12 - n21) / n
    Etheta = thetahat

    Q = (
        n**2
        * (n + 1)
        * (Etheta + 1)
        * (1 - Etheta)
        / ((n * (n12 + n21) - (n12 - n21) ** 2))
    )

    p = (Etheta + 1) * 0.5 * (Q - 1)
    q = (1 - Etheta) * 0.5 * (Q - 1)

    CI = tuple(lm * 2 - 1 for lm in scipy.stats.beta.interval(1 - alpha, a=p, b=q))

    p = 2 * scipy.stats.binom.cdf(min([n12, n21]), n=n12 + n21, p=0.5)
    print("Result of McNemars test using alpha=", alpha)
    print("Comparison matrix n")
    print(nn)
    if n12 + n21 <= 10:
        print("Warning, n12+n21 is low: n12+n21=", (n12 + n21))

    print("Approximate 1-alpha confidence interval of theta: [thetaL,thetaU] = ", CI)
    print(
        "p-value for two-sided test A and B have same accuracy (exact binomial test): p=",
        p,
    )

    return thetahat, CI, p


if __name__ == "__main__":
    z = [
        -9.94147773e02,
        1.26057137e02,
        2.43068571e03,
        1.34943873e02,
        -7.32103331e02,
        2.37564709e02,
        2.50241916e02,
        2.57480953e02,
        -2.63697057e02,
        -6.87957076e01,
        -2.79913347e02,
        1.88978039e02,
        1.98121892e02,
        5.41920321e01,
        1.70814489e02,
        9.50546024e02,
        -1.42327811e02,
        1.76465996e02,
        6.87389306e01,
        1.73725613e03,
        -1.78676140e02,
        1.52421405e03,
        -5.30574002e01,
        1.95582309e00,
        -1.94314010e02,
        -6.72125537e02,
        1.62167916e02,
        1.78461753e02,
        -1.24817459e02,
        1.43904422e02,
        2.45598432e02,
        4.17515769e02,
        1.34710476e02,
        -4.48734895e01,
        1.05674612e02,
        -3.39105804e02,
        -5.34365506e02,
        2.23486078e02,
        1.97750315e02,
        -3.00557776e03,
        9.63587836e01,
        -1.85012667e02,
        2.54862222e02,
        -1.78881284e02,
        -1.03805766e02,
        2.52354768e02,
        -6.00848307e02,
        3.71357436e00,
        2.38950633e02,
        -1.88401811e03,
        1.86325333e02,
        2.45168149e02,
        1.14115851e01,
        1.18459847e02,
        4.20244456e02,
        -1.96854780e02,
        -1.24603029e01,
        -5.54211898e02,
        -1.57707245e01,
        -5.39761905e02,
        -2.82533665e02,
        1.42265335e02,
        1.30362591e02,
        3.63309122e01,
        1.38202398e02,
        1.58929137e02,
        1.58929177e02,
        7.10797177e02,
        1.34089160e01,
        9.32132688e02,
        3.46853860e01,
        6.27785220e01,
        2.81806999e-02,
        -1.52944174e02,
        2.66329889e02,
        1.62190118e02,
        -3.89048944e-03,
        -2.60694426e02,
        -7.15940302e02,
        2.25831089e02,
        -1.77851578e01,
        2.66329889e02,
        1.08980992e03,
        1.56404585e02,
        2.66329889e02,
        6.63044600e02,
        8.08266552e01,
        1.83926579e02,
        1.77769644e02,
        -5.92678110e01,
        1.86044032e02,
        1.59819830e02,
        2.60035987e02,
        1.60910872e02,
        -2.39925571e02,
        -1.03542616e02,
        -1.30351275e01,
        3.88166963e03,
        1.51075198e02,
        -1.65484521e02,
        9.08165687e01,
        1.18686751e03,
        1.65290154e02,
        -1.91692974e02,
        2.75584781e02,
        -1.91227724e03,
        -9.14883857e00,
        -6.03404163e01,
        1.26539212e02,
        5.32728542e01,
        7.13462504e02,
        2.24593771e02,
        1.16993301e02,
        1.08405310e02,
        5.76378276e01,
        1.27516156e02,
        1.93353908e01,
        2.75555832e02,
        -8.77754648e01,
        -3.75658826e02,
        -7.52816578e02,
        -4.34021742e02,
        5.95930150e01,
        9.43829397e02,
        -4.37258761e02,
        1.27857209e02,
        4.36410358e01,
        -9.96612122e01,
        2.24738210e03,
        1.60453092e02,
        2.03273360e02,
        -8.06696669e01,
        9.88763264e01,
        5.55727999e02,
        -2.18588047e02,
        1.91855517e02,
        1.26188907e03,
        -6.70477718e02,
        -3.28242036e02,
        4.25807472e01,
        2.87933046e03,
        1.28770056e03,
        1.77890518e02,
        9.42159762e02,
        1.97441517e02,
        6.71145887e01,
        1.97441517e02,
        1.38789855e02,
        2.30957514e02,
        -1.18130059e02,
        -1.09434948e02,
        -3.46961432e02,
        1.25455407e02,
        -1.97299428e03,
        1.77283165e02,
        -3.36631354e02,
        -2.60743339e01,
        -2.24421069e02,
        1.95480316e02,
        3.54171629e02,
        1.65461586e02,
        1.05668384e02,
        1.67418017e01,
        -8.44526008e02,
        2.58552624e02,
        2.56605849e02,
        1.91315916e02,
    ]

    alpha = 0.05
    CI = st.t.interval(
        1 - alpha, len(z) - 1, loc=np.mean(z), scale=st.sem(z)
    )  # Confidence interval
    p = 2 * st.t.cdf(-np.abs(np.mean(z)) / st.sem(z), df=len(z) - 1)  # p-value

    print(p)
    print(CI)
    a = 123
