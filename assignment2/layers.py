import numpy as np

def softmax(predictions):
    '''
    Computes probabilities from scores

    Arguments:
      predictions, np array, shape is either (N) or (batch_size, N) -
        classifier output

    Returns:
      probs, np array of the same shape as predictions -
        probability for every class, 0..1
    '''
    if len(predictions.shape) == 1:
        predictions = predictions[np.newaxis, :]
    return np.exp(predictions - np.max(predictions, axis=1, keepdims =True))/np.sum(np.exp(predictions - np.max(predictions, axis=1, keepdims = True)), axis=1, keepdims = True)

def cross_entropy_loss(probs, target_index):
    '''
    Computes cross-entropy loss

    Arguments:
      probs, np array, shape is either (N) or (batch_size, N) -
        probabilities for every class
      target_index: np array of int, shape is (1) or (batch_size) -
        index of the true class for given sample(s)

    Returns:
      loss: single value
    '''
    if len(probs.shape) == 1:
        probs = probs[np.newaxis, :]
    target_index_arr = np.zeros_like(probs)
    target_index_arr[np.arange(len(probs)), target_index] = 1
    return -np.mean(np.log(probs[np.arange(len(probs)), target_index]))
    #return -np.sum(np.log(probs[np.arange(len(probs)), target_index]))

def l2_regularization(W, reg_strength):
    '''
    Computes L2 regularization loss on weights and its gradient

    Arguments:
      W, np array - weights
      reg_strength - float value

    Returns:
      loss, single value - l2 regularization loss
      gradient, np.array same shape as W - gradient of weight by l2 loss
    '''

    loss = reg_strength*np.sum(W**2)
    grad = 2*reg_strength*W
    return loss, grad


def softmax_with_cross_entropy(predictions, target_index):
    '''
    Computes softmax and cross-entropy loss for model predictions,
    including the gradient

    Arguments:
      predictions, np array, shape is either (N) or (batch_size, N) -
        classifier output
      target_index: np array of int, shape is (1) or (batch_size) -
        index of the true class for given sample(s)

    Returns:
      loss, single value - cross-entropy loss
      dprediction, np array same shape as predictions - gradient of predictions by loss value
    '''
    if len(predictions.shape) == 1:
        predictions = predictions[np.newaxis, :]
    target_index_arr = np.zeros_like(predictions)
    target_index_arr[np.arange(len(predictions)), target_index] = 1
    loss = cross_entropy_loss(softmax(predictions), target_index)
    dprediction = (softmax(predictions) - target_index_arr)/len(target_index_arr)
    #dprediction = (softmax(predictions) - target_index_arr)
    return loss, dprediction


class Param:
    """
    Trainable parameter of the model
    Captures both parameter value and the gradient
    """

    def __init__(self, value):
        self.value = value
        self.grad = np.zeros_like(value)


class ReLULayer:
    def __init__(self):
        pass

    def forward(self, X):
        self.X = X
        return (np.abs(X) + X)/2

    def backward(self, d_out):
        """
        Backward pass

        Arguments:
        d_out, np array (batch_size, num_features) - gradient
           of loss function with respect to output

        Returns:
        d_result: np array (batch_size, num_features) - gradient
          with respect to input
        """
        return d_out * (np.abs(self.X) + self.X) / (2 * np.abs(self.X) + 1e-7)

    def params(self):
        # ReLU Doesn't have any parameters
        return {}


class FullyConnectedLayer:
    def __init__(self, n_input, n_output):
        self.W = Param(0.001 * np.random.randn(n_input, n_output))
        self.B = Param(0.001 * np.random.randn(1, n_output))
        self.X = None

    def forward(self, X):
        self.X = X
        return X @ self.W.value + self.B.value

    def backward(self, d_out):
        """
        Backward pass
        Computes gradient with respect to input and
        accumulates gradients within self.W and self.B

        Arguments:
        d_out, np array (batch_size, n_output) - gradient
           of loss function with respect to output

        Returns:
        d_result: np array (batch_size, n_input) - gradient
          with respect to input
        """
        dx = d_out @ self.W.value.T
        dw = self.X.T @ d_out
        db = np.sum(d_out, axis=0)
        self.B.grad += db
        self.W.grad += dw
        return dx

    def params(self):
        return {'W': self.W, 'B': self.B}
