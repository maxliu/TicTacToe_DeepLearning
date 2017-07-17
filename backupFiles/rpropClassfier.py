from __future__ import division
import numpy as np

from sklearn.base import BaseEstimator, ClassifierMixin

from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import RPropMinusTrainer
from pybrain.datasets.supervised import SupervisedDataSet

from math import sqrt


class RPClassifier(BaseEstimator, ClassifierMixin):
    """A network classifier with RPropMinusTrainer in PYbrain
    prarameters
    -----------
    h_size : interger, default = 2.
        Number of neurons in hidden layer.
    epo :  interger, default = 2.
       Train on the current dataset for the given number of epochs.
    verbose: interger, default = 2
            Controls the verbosity of the network building process.
    Attributes
    ----------
    in_size : interger.
        The number of input array columns. This will be number of
        neurons in input layer.
    out_size : interger
        The number of label arrya columns. this will be the number of
        neurons in output layer.
    net : the network.
    references
    ----------
    PyBrain document
    http://pybrain.org/docs/index.html
    """

    def __init__(self, h_size=2, epo=2, verbose=0):
        self.h_size = h_size
        self.epo = epo
        self.verbose = verbose
        pass

    def fit(self, X, y):
        """ build a network from training set (X, y).
        parameters
        ----------
        X : array-like or sparse matrix of shape = [n_samples, n_features]
        y : array-like, shape = [n_samples] or [n_samples, n_output]
        return
        ------
        self : object
        """

        y_train = np.array([[yn] for yn in y])
        _, self.in_size = X.shape
        _, self.out_size = y_train.shape

        ds = SupervisedDataSet(self.in_size, self.out_size)

        ds.setField('input', X)
        ds.setField('target', y_train)

        self.net = buildNetwork(self.in_size,
                                self.h_size, self.out_size, bias=True)
        trainer = RPropMinusTrainer(self.net, dataset=ds)

        if self.verbose > 0:
            print ("start training ...")

        for n in xrange(self.epo):
            mse = trainer.train()
            rmse = sqrt(mse)
            if self.verbose > 0:
                print ("RMSE = %8.3f epoch = %d" % (rmse, n))
        return self

    def predict(self, X):
        """Predict class for X.
        Parameters
        ----------
        X : array-like or sparse matrix of shape = [n_samples, n_features]
        Returns
        -------
        y : array-like, shape = [n_samples] or [n_samples, n_output]
        """
        # TODO for multi output classes
        p = self.predict_proba(X)
        p_class = np.array([1 if pn > 0.5 else 0 for pn in p])
        return p_class

    def predict_proba(self, X):
        """Predict class probabilities for X.
        Parameters
        ----------
        X : array-like or sparse matrix of shape = [n_samples, n_features]
        Returns
        -------
        p : array-like, shape = [n_samples] or [n_samples, n_output]
        """

        row_size, in_size = X.shape

        y_test_dumy = np.zeros([row_size, self.out_size])

        # check size
        assert(self.net.indim == in_size)

        ds = SupervisedDataSet(in_size, self.out_size)

        ds.setField('input', X)
        ds.setField('target', y_test_dumy)

        p = self.net.activateOnDataset(ds)
        return np.array([pn[0] for pn in p])