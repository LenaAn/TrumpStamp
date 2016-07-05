import cudarray as ca
from ...base import ParamMixin
from ...parameter import Parameter
from ..base import Unary


def padding(win_shape, border_mode):
    if border_mode == 'valid':
        def pad_fun(win_size): return 0
    elif border_mode == 'same':
        def pad_fun(win_size): return win_size // 2
    elif border_mode == 'full':
        def pad_fun(win_size): return win_size - 1
    else:
        raise ValueError('invalid mode: "%s"' % border_mode)
    return tuple(pad_fun(win_size) for win_size in win_shape)


class Convolution(Unary, ParamMixin):
    def __init__(self, n_filters, filter_shape, weights, bias=0.0,
                 strides=(1, 1), border_mode='valid'):
        self.name = 'conv'
        self.n_filters = n_filters
        self.filter_shape = filter_shape
        self.weights = Parameter.from_any(weights)
        if bias is not None:
            bias = Parameter.from_any(bias)
        self.bias = bias
        self.padding = padding(filter_shape, border_mode)
        self.strides = strides
        self.conv_op = ca.nnet.ConvBC01(self.padding, self.strides)

    def __call__(self, x):
        super(Convolution, self).__call__(x)
        self.bpropable = True
        return self

    @staticmethod
    def img_out_shape(img_shape, win_shape, strides, padding):
        return tuple((img_size + 2*pad - win_size) // stride + 1
                     for img_size, win_size, stride, pad
                     in zip(img_shape, win_shape, strides, padding))

    def setup(self):
        x_shape = self.x.shape
        batch_size, n_channels = x_shape[:2]
        self.weights.setup((self.n_filters, n_channels) + self.filter_shape)
        if self.bias is not None:
            self.bias.setup((1, self.n_filters, 1, 1))
        img_shape = self.img_out_shape(x_shape[2:], self.filter_shape,
                                       self.strides, self.padding)
        self.shape = (batch_size, self.n_filters) + img_shape
        self.array = ca.zeros(self.shape)
        self.grad_array = ca.zeros(self.shape)

    def fprop(self):
        self.conv_op.fprop(self.x.array, self.weights.array,
                           convout=self.array)
        if self.bias is not None:
            self.array += self.bias.array

    def bprop(self):
        self.conv_op.bprop(
            self.x.array, self.weights.array, self.grad_array,
            filters_d=self.weights.grad_array, imgs_d=self.x.grad_array
        )
        if self.bias is not None:
            ca.sum(ca.sum(self.grad_array, axis=(2, 3), keepdims=True), axis=0,
                   keepdims=True, out=self.bias.grad_array)

    @property
    def params(self):
        if self.bias is None:
            return self.weights,
        else:
            return self.weights, self.bias

    @params.setter
    def params(self, params):
        if self.bias is None:
            self.weights, = params
        else:
            self.weights, self.bias = params


class BackwardConvolution(Convolution):
    def __init__(self, n_filters, filter_shape, weights, bias=0.0,
                 strides=(2, 2), border_mode='valid'):
        super(BackwardConvolution, self).__init__(
            n_filters, filter_shape, weights, bias, strides, border_mode
        )
        self.conv_op = ca.nnet.ConvBC01(self.padding, self.strides)

    @staticmethod
    def img_out_shape(img_shape, win_shape, strides, padding):
        return tuple((img_size + 2*pad - win_size + 1) * stride
                     for img_size, win_size, stride, pad
                     in zip(img_shape, win_shape, strides, padding))

    def setup(self):
        x_shape = self.x.shape
        batch_size, n_channels = x_shape[:2]
        self.weights.setup((n_channels, self.n_filters) + self.filter_shape)
        if self.bias is not None:
            self.bias.setup((1, self.n_filters, 1, 1))
        img_shape = self.img_out_shape(x_shape[2:], self.filter_shape,
                                       self.strides, self.padding)
        self.shape = (batch_size, self.n_filters) + img_shape
        self.array = ca.zeros(self.shape)
        self.grad_array = ca.zeros(self.shape)
        # make sure conv_op is initialized
        self.conv_op.fprop(self.grad_array, self.weights.array,
                           convout=self.x.grad_array)

    def fprop(self):
        self.conv_op.bprop(
            None, self.weights.array, self.x.array,
            to_filters=False, imgs_d=self.array
        )
        if self.bias is not None:
            self.array += self.bias.array

    def bprop(self):
        self.conv_op.bprop(
            self.grad_array, self.weights.array, self.x.array,
            filters_d=self.weights.grad_array, to_imgs=False
        )
        self.conv_op.fprop(self.grad_array, self.weights.array,
                           convout=self.x.grad_array)
        if self.bias is not None:
            ca.sum(ca.sum(self.grad_array, axis=(2, 3), keepdims=True), axis=0,
                   keepdims=True, out=self.bias.grad_array)


class Pool(Unary):
    def __init__(self, win_shape=(3, 3), method='max', strides=(2, 2),
                 border_mode='valid'):
        pad = padding(win_shape, border_mode)
        self.pool_op = ca.nnet.PoolB01(win_shape, pad, strides, method)
        self.img_shape = None

    def setup(self):
        self.shape = self.pool_op.fprop(self.x.array).shape
        self.array = ca.zeros(self.shape)
        self.grad_array = ca.zeros(self.shape)

    def fprop(self):
        self.pool_op.fprop(self.x.array, self.array)

    def bprop(self):
        self.pool_op.bprop(self.x.shape[2:], self.grad_array,
                           self.x.grad_array)


class Rescale(Unary):
    def __init__(self, factor, method):
        self.factor = factor
        self.method = method

    def setup(self):
        self.shape = ca.nnet.rescale(self.x.array, self.factor,
                                     self.method).shape
        self.array = ca.zeros(self.shape)
        self.grad_array = ca.zeros(self.shape)

    def fprop(self):
        ca.nnet.rescale(self.x.array, self.factor, self.method, self.array)
        if self.factor > 1.0 and self.method != 'perforated':
            self.array *= 1.0/(self.factor*self.factor)

    def bprop(self):
        ca.nnet.rescale(self.grad_array, 1./self.factor, self.method,
                        self.x.grad_array)
