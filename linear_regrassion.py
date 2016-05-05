import numpy
import theano
import theano.tensor as T
import mysql.connector
import six.moves.cPickle as pickle
import timeit


class LinearRegression(object):
    """Linear Regression Class

    The linear regression is fully described by a weight matrix :math:`W`
    and bias vector :math:`b`. Regression is done by projecting data
    points onto a hyperplanes where the visible values lies, the distance to which is used to
    determine a class membership probability.
    """

    def __init__(self, input_x, input_y, n_in, n_out, W=None, b=None):
        """ Initialize the parameters of the logistic regression

        :type input_x: theano.tensor.TensorType
        :param input_x: symbolic variable that describes the input of the
                      architecture (one minibatch)

        :type input_y: theano.tensor.TensorType
        :param input_y: symbolic variable that describes the input of the
                      architecture (one minibatch)

        :type n_in: int
        :param n_in: number of input units, the dimension of the space in
                     which the data points lie

        :type n_out: int
        :param n_out: number of output units, the dimension of the space in
                      which the labels lie

        """
        # initialize with 0 the weights W as a matrix of shape (n_in, n_out)
        if W is None:
            self.W = theano.shared(
                numpy.asarray(
                    numpy.random.uniform(
                        low=-numpy.sqrt(6. / (n_in + n_out)),
                        high=numpy.sqrt(6. / (n_in + n_out)),
                        size=(n_in, n_out)
                    ),
                    dtype=theano.config.floatX
                )
            )
        else:
            self.W = W

        # initialize the biases b as a vector of n_out 0s
        if b is None:
            self.b = theano.shared(
                value=numpy.ones(
                    (n_out,),
                    dtype=theano.config.floatX
                ),
                name='b',
                borrow=True
            )
        else:
            self.b = b

        # symbolic description of how to compute prediction whose
        # probability is maximal
        self.y_pred = T.dot(input_x, self.W) + self.b

        # symbolic expression for computing the matrix proportional to the prediction
        # probabilities
        # Where:
        # W is a matrix where column-k represent the projection hyperplane for
        # the prediction
        # x is a matrix where row-j  represents input training sample-j
        # b is a vector where element-k represent the free parameter of
        # hyperplane-k
        self.p_d_given_thenta = T.pow(input_y - self.y_pred, 2)

        # L1 norm ; one regularization option is to enforce L1 norm to
        # be small
        self.l1 = (
            T.sum(T.abs_(self.W))
        )

        # square of L2 norm ; one regularization option is to enforce
        # square of L2 norm to be small
        self.l2_sqr = (
            T.sum((self.W ** 2))
        )

        # parameters of the model
        self.params = [self.W, self.b]

        # keep track of model input
        self.input_x = input_x
        self.input_y = input_y

    def negative_log_likelihood(self):
        """Return the mean of the negative log-likelihood of the prediction
        of this model under a given target distribution.

        Note: we use the mean instead of the sum so that
              the learning rate is less dependent on the batch size
        """

        return T.mean(T.log(self.p_d_given_thenta))

    def errors(self):
        """Return a float representing the number of errors in the minibatch
        over the total number of examples of the minibatch ; zero one
        loss over the size of the minibatch
        """
        return self.p_d_given_thenta


def sgd_optimization(data, learning_rate=0.01, l1_reg=0.000, l2_reg=0.05, n_epochs=10000, batch_size=1):
    """
    Minimal example.

    Demonstrate stochastic gradient descent optimization of a log-linear
    model

    :type learning_rate: float
    :param learning_rate: learning rate used (factor for the stochastic
                          gradient)
    :type l1_reg: float
    :param l1_reg: L1-norm's weight when added to the cost

    :type l2_reg: float
    :param l2_reg: L2-norm's weight when added to the cost

    :type n_epochs: int
    :param n_epochs: maximal number of epochs to run the optimizer

    """

    train_set_x, train_set_y = data
    #test_set_x, test_set_y = datasets[1]

    # compute number of minibatches for training, validation and testing
    n_train_batches = train_set_x.get_value(borrow=True).shape[0]
    #n_train_batches = train_set_x.get_value(borrow=True).shape[0] // batch_size
    #n_test_batches = test_set_x.get_value(borrow=True).shape[0] // batch_size

    ######################
    # BUILD ACTUAL MODEL #
    ######################
    print('... building the model')

    # allocate symbolic variables for the data
    index = T.lscalar()  # index to a [mini]batch

    # generate symbolic variables for input (x and y represent a
    # minibatch)
    x = T.dvector('x')  # data, presented as rasterized images
    y = T.dscalar('y')  # labels, presented as 1D vector of [int] labels

    # construct the logistic regression class
    # Each MNIST image has size 28*28
    classifier = LinearRegression(input_x=x, input_y=y, n_in=train_set_x.get_value(borrow=True).shape[0], n_out=1)

    # the cost we minimize during training is the negative log likelihood of
    # the model in symbolic format
    cost = classifier.negative_log_likelihood() + l1_reg * classifier.l1 + l2_reg * classifier.l2_sqr

    # compiling a Theano function that computes the mistakes that are made by
    # the model on a minibatch
    #test_model = theano.function(
    #    inputs=[index],
    #    outputs=classifier.errors(),
    #    givens={
    #        x: test_set_x[index * batch_size: (index + 1) * batch_size],
    #        y: test_set_y[index * batch_size: (index + 1) * batch_size]
    #    }
    #)

    # compute the gradient of cost with respect to theta = (W,b)
    g_W = T.grad(cost=cost, wrt=classifier.W)
    g_b = T.grad(cost=cost, wrt=classifier.b)


    # specify how to update the parameters of the model as a list of
    # (variable, update expression) pairs.
    updates = [(classifier.W, classifier.W - learning_rate * g_W),
               (classifier.b, classifier.b - learning_rate * g_b)]

    # compiling a Theano function `train_model` that returns the cost, but in
    # the same time updates the parameter of the model based on the rules
    # defined in `updates`
    train_model = theano.function(
        inputs=[],
        outputs=cost,
        updates=updates,
        givens={
            x: train_set_x,
            y: train_set_y
        }
    )

    ###############
    # TRAIN MODEL #
    ###############
    print('... training the model')

    start_time = timeit.default_timer()

    epoch = 0
    while (epoch < n_epochs):
        epoch = epoch + 1
        minibatch_avg_cost = train_model()

    # compute zero-one loss on validation set
    #validation_losses = [test_model(i)
    #                     for i in range(n_test_batches)]
    #this_validation_loss = numpy.mean(validation_losses)

    # save the best model
    best_b = classifier.b
    best_W = classifier.W
    #with open('best_model.pkl', 'wb') as f:
    #    pickle.dump(classifier, f)

    end_time = timeit.default_timer()

    print('The code run for %d epochs, with %f epochs/sec' % (epoch, 1. * epoch / (end_time - start_time)))
    print(('The code  ran for %.1fs' % (end_time - start_time)))
    return [best_W, best_b]

def shared_dataset(data_xy, borrow=True):
    """ Function that loads the dataset into shared variables

    The reason we store our dataset in shared variables is to allow
    Theano to copy it into the GPU memory (when code is run on GPU).
    Since copying data into the GPU is slow, copying a minibatch everytime
    is needed (the default behaviour if the data is not in a shared
    variable) would lead to a large decrease in performance.
    """

    shared = theano.shared(numpy.asarray(data_xy, dtype=theano.config.floatX), borrow=borrow)

    return shared


def execute(games=39):
    seasons = [2011, 2012, 2013, 2014]

    scores = dict()

    cnx = mysql.connector.connect(user="inf2290", host="localhost", database="cartola", password="^inf2290$")
    for season in seasons:
        query = (
            "select atleta_id, pontos_num from atleta_rodada_%d where rodada_id<%d and "
            "(status_id=1 or status_id=7) order by rodada_id asc"
            %(season, games)
        )

        cursor = cnx.cursor()
        cursor.execute(query)
        for line in cursor:
            if line[1] == 0:
                continue
            if line[0] in scores:
                scores[line[0]].append(line[1])
            else:
                scores[line[0]] = [line[1]]
    cnx.close()
    params = []

    start_time = timeit.default_timer()

    for id, score in scores.items():
        print(score)
        print(id)
        if len(score) >= 7:
            param = sgd_optimization([shared_dataset(score[:len(score)-1]), shared_dataset(score[-1])])
            params.append(param)

    end_time = timeit.default_timer()
    print(('The code  ran for %.1fs' % (end_time - start_time)))

    #with open('params.pkl', 'wb') as f:
    #    pickle.dump(params, f)

if __name__ == "__main__":
    execute()