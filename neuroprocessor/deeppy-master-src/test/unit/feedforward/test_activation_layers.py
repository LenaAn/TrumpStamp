import itertools
import numpy as np
import deeppy as dp
from test_layers import check_grad


batch_sizes = [1, 4, 5, 10]
n_ins = [1, 2, 7, 8, 18]
activations = ['leaky_relu', 'parametric_relu', 'relu', 'sigmoid', 'softplus',
               'tanh']


def test_activation():
    confs = itertools.product(batch_sizes, n_ins, activations)
    for batch_size, n_in, activation in confs:
        print('Activation: batch_size=%i, n_in=%i, method=%s'
              % (batch_size, n_in, str(activation)))
        x_shape = (batch_size, n_in)
        x = np.random.normal(size=x_shape).astype(dp.float_)
        layer = dp.Activation.from_any(activation)
        layer.setup(x_shape)
        assert layer.y_shape(x_shape) == x_shape
        if dp.float_ != np.float_:
            rtol = 1e-02
        else:
            rtol = None
        check_grad(layer, x, rtol=rtol)
