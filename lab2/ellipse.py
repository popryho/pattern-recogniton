import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn.model_selection import train_test_split


def plot_decision_regions(X, y, h=0.01):
    """
    A function for plotting decision regions of classifiers 2 dimensions.
    """
    x1_min, x1_max = X[:, -3].min() - 1, X[:, -3].max() + 1
    x2_min, x2_max = X[:, -2].min() - 1, X[:, -2].max() + 1

    xx1, xx2 = np.meshgrid(np.arange(x1_min, x1_max, h),
                           np.arange(x2_min, x2_max, h))

    Z = ppn.predict(np.array(data_preprocessor(
        np.concatenate((xx1.ravel().reshape(-1, 1), xx2.ravel().reshape(-1, 1)), axis=1)
    )))
    Z = Z.reshape(xx1.shape)

    plt.contourf(xx1, xx2, Z, alpha=0.5, cmap=ListedColormap(['red', 'blue']))

    plt.xlim(xx1.min(), xx1.max())
    plt.ylim(xx2.min(), xx2.max())

    for idx, cl in enumerate(np.unique(y)):
        plt.scatter(X[:, -3:-1][y == cl, 0],
                    X[:, -3:-1][y == cl, 1],
                    alpha=0.8, color=ListedColormap(['red', 'blue'])(idx),
                    marker=['o', 'x'][idx], label=cl)
    plt.legend(loc='best')
    plt.show()


class Perceptron(object):

    def __init__(self, n_epochs=5):
        self.errors_ = []
        self.n_epochs = n_epochs
        self.w_ = 0

    def fit(self, X, y):
        self.w_ = np.zeros(X.shape[1])

        for _ in range(self.n_epochs):
            errors = 0
            for xi, target in zip(X, y):

                if self.predict(xi) == 1 and target == 0:
                    self.w_ -= xi
                elif self.predict(xi) == 0 and target == 1:
                    self.w_ += xi
                else:
                    pass

                errors += 1 if self.predict(xi) != target else 0
            self.errors_.append(errors)

            plot_decision_regions(X, y)
        return self

    def predict(self, xi):
        return np.where(np.dot(xi, self.w_) > 0.0, 1, 0)


def sample_generator(bias, n=50):
    """
    Sample_generator generate sample from multivariate normal distribution
    with given params
    :param bias: bias in mean
    :param n: number of sample to generate
    :return: sample
    """
    mean = np.random.rand(2) + 2 * [bias]
    a = np.random.rand(2, 2)
    cov = np.dot(a, a.transpose())

    return np.random.multivariate_normal(mean, cov, n)


def data_preprocessor(x, label=None):
    """
    Concatenate bias vector and labels to original x
    :param x: generated sample from multivariate normal distribution
    :param label: label(target) vector
    :return: merged data
    """
    n, m = x.shape

    new_features = np.array([x[:, i]*x[:, j] for i in range(m) for j in range(m)]).T
    bias = np.ones(shape=(n, 1))

    if label is None:
        return np.concatenate((new_features, x, bias), axis=1)
    else:
        target = label * np.ones(shape=(n, 1))
        return np.concatenate((new_features, x, bias, target), axis=1)


if __name__ == '__main__':

    # sample generating
    x1 = sample_generator(bias=0, n=50)
    x2 = sample_generator(bias=5, n=50)

    # added bias and label vector
    df1 = data_preprocessor(x1, 1)
    df2 = data_preprocessor(x2, 0)

    # concatenate two different sample
    df = np.concatenate((df1, df2), axis=0)

    # ------------------------------------------------------------------------------------
    # visualize generated set of data
    fig, ax = plt.subplots()
    for *cls, c, m in zip([x1, x2], [0, 1], ['blue', 'red'], ['D', 'o']):
        ax.scatter(cls[0][:, 0], cls[0][:, 1], c=c, s=100, label="class %d" % cls[1], marker=m,
                   alpha=0.5)

    ax.legend(loc='upper left')
    ax.grid(True)

    plt.show()

    # ------------------------------------------------------------------------------------
    # train test split
    X_train, X_test, y_train, y_test = train_test_split(
        df[:, :-1], df[:, -1], test_size=0.1, random_state=42, shuffle=True, stratify=df[:, -1]
    )

    # algorithm training
    ppn = Perceptron()
    ppn.fit(X_train, y_train)

    # ------------------------------------------------------------------------------------
    # learning curve
    plt.plot(range(1, len(ppn.errors_) + 1), ppn.errors_, 'r:', marker='o')

    plt.title('Number of failed classification on each epoch')
    plt.grid()
    plt.show()

    # ------------------------------------------------------------------------------------
    # visualize test set in decision region
    plot_decision_regions(X_test, y_test)
