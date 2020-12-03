# http://yann.lecun.com/exdb/mnist/

from pandas import read_csv
from numpy import (
    unique, random, newaxis, dot, empty, prod, array, uint8
)
from PIL import Image


class BMM(object):

    def __init__(self, n_epochs=1):

        self.n_epochs_ = n_epochs
        self.X_ = empty(0)
        self.k_ = 0
        self.n_, self.m_ = 0, 0

        self.p_k = empty(self.k_)
        self.p_k_x = empty((self.n_, self.k_))
        self.p_x_k = empty((self.k_, self.m_))
    def fit(self, X, n_clusters):

        self.X_ = X.to_numpy()
        self.k_ = n_clusters
        self.n_, self.m_ = self.X_.shape

        self.p_k = empty(self.k_)
        self.p_k_x = empty((self.n_, self.k_))
        self.p_x_k = empty((self.k_, self.m_))

        expert_values_p_k_x = random.rand(self.n_, self.k_)
        self.p_k_x = expert_values_p_k_x / expert_values_p_k_x.sum(axis=1)[:, newaxis]

        for i in range(self.n_epochs_):
            self.m_step()
            self.e_step()
def data_preprocessor(df):

    labels, values = df.iloc[:, 0], df.iloc[:, 1:]
    values_binarize = values.astype("bool")
    inverted_values = values_binarize.applymap(lambda x: True if x is False else False)
    return inverted_values, labels


def show_image(vector, i):

    output_image = vector.reshape((28, 28))
    Image.fromarray(uint8(output_image * 255), 'L').save('output_{}.png'.format(i))


if __name__ == '__main__':

    mnist = read_csv('data/mnist_train.csv')
    mnist = mnist[mnist.iloc[:, 0].isin([0, 1])].reset_index(drop=True)

    X, y = data_preprocessor(mnist)
    k = unique(y).shape[0]

    bmm = BMM()
    bmm.fit(X, k)