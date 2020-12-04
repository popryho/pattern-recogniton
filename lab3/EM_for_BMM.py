# http://yann.lecun.com/exdb/mnist/

from pandas import DataFrame, concat
from numpy import (
    unique, random, newaxis, dot, empty, prod, array, uint8
)
from PIL import Image
import mnist


class BMM(object):

    def __init__(self, n_epochs=10):

        self.n_epochs_ = n_epochs
        self.X_ = empty(0)
        self.k_ = 0
        self.n_, self.m_ = 0, 0

        self.p_k = empty(self.k_)
        self.p_k_x = empty((self.n_, self.k_))
        self.p_x_k = empty((self.k_, self.m_))
        
    def e_step(self):

        for i in range(self.n_):
            for k in range(self.k_):
                self.p_k_x[i, k] = self.p_k[k]*prod(a=[self.p_x_k[k] ** self.X_[i],
                                                       ((1 - self.p_x_k[k]) ** (1 - self.X_[i]))])
        self.p_k_x /= self.p_k_x.sum(axis=1)[:, newaxis]

    def m_step(self):

        self.p_k = self.p_k_x.sum(axis=0) / self.n_
        self.p_x_k = array([dot(self.X_.T, self.p_k_x).T[i] /
                            self.p_k_x.sum(axis=0)[i] for i in range(self.k_)])   
        
    def fit(self, X, n_clusters):

        self.X_ = X.to_numpy()
        self.k_ = n_clusters
        self.n_, self.m_ = self.X_.shape

        expert_values_p_k_x = random.rand(self.n_, self.k_)
        self.p_k_x = expert_values_p_k_x / expert_values_p_k_x.sum(axis=1)[:, newaxis]

        for i in range(self.n_epochs_):
            self.m_step()
            self.e_step()
            for image in range(self.k_):
                show_image(self.p_x_k[image], i+image)


def data_preprocessor(df):

    labels, values = df.iloc[:, 0], df.iloc[:, 1:]
    values_binarize = values.astype("bool")
    inverted_values = values_binarize.applymap(lambda x: True if x is False else False)
    return inverted_values, labels


def show_image(vector, i):

    output_image = vector.reshape((28, 28))
    Image.fromarray(uint8(output_image * 255), 'L').save('output_{}.png'.format(i))


if __name__ == '__main__':
    
    X, y = DataFrame(mnist.train_images().reshape(60000, -1)), DataFrame(mnist.train_labels())
    mnist_df = concat([y, X], axis=1)
    mnist_df = mnist_df[mnist_df.iloc[:, 0].isin([2, 3, 4])].reset_index(drop=True)

    X, y = data_preprocessor(mnist_df)
    k = unique(y).shape[0]

    bmm = BMM()
    bmm.fit(X, k)
