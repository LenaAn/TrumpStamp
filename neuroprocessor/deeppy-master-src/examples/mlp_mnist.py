#!/usr/bin/env python

"""
Digit classification
====================

"""

import numpy as np
import matplotlib.pyplot as plt
import deeppy as dp


# Fetch MNIST data
dataset = dp.dataset.MNIST()
x_train, y_train, x_test, y_test = dataset.arrays(flat=True, dp_dtypes=True)

# Normalize pixel intensities
scaler = dp.StandardScaler()
x_train = scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)

# Prepare network feeds
batch_size = 128
train_feed = dp.SupervisedFeed(x_train, y_train, batch_size=batch_size)
test_feed = dp.Feed(x_test)

# Setup network
weight_gain = 2.0
weight_decay = 0.0005
net = dp.NeuralNetwork(
    layers=[
        dp.Affine(
            n_out=1024,
            weights=dp.Parameter(dp.AutoFiller(weight_gain),
                                 weight_decay=weight_decay),
        ),
        dp.ReLU(),
        dp.Affine(
            n_out=1024,
            weights=dp.Parameter(dp.AutoFiller(weight_gain),
                                 weight_decay=weight_decay),
        ),
        dp.ReLU(),
        dp.Affine(
            n_out=dataset.n_classes,
            weights=dp.Parameter(dp.AutoFiller()),
        ),
    ],
    loss=dp.SoftmaxCrossEntropy(),
)

# Train network
n_epochs = [50, 15]
learn_rate = 0.05/batch_size
learn_rule = dp.Momentum(momentum=0.94)
trainer = dp.GradientDescent(net, train_feed, learn_rule)
for i, epochs in enumerate(n_epochs):
    learn_rule.learn_rate = learn_rate/10**i
    trainer.train_epochs(n_epochs=25)

# Evaluate on test data
error = np.mean(net.predict(test_feed) != y_test)
print('Test error rate: %.4f' % error)


# Plot dataset examples
def plot_img(img, title):
    plt.figure()
    plt.imshow(img, cmap='gray', interpolation='nearest')
    plt.axis('off')
    plt.title(title)
    plt.tight_layout()

imgs = np.reshape(x_train[:63, ...], (-1, 28, 28))
plot_img(dp.misc.img_tile(dp.misc.img_stretch(imgs)),
         'Dataset examples')

# Plot learned features in first layer
w = np.array(net.layers[0].weights.array)
w = np.reshape(w.T, (-1,) + dataset.img_shape)
w = w[np.argsort(np.std(w, axis=(1, 2)))[-64:]]
plot_img(dp.misc.img_tile(dp.misc.img_stretch(w)),
         'Examples of features learned')
