import tensorflow as tf

'''
Perceptron with 2 hidden layers. Weights and Biases are placeholders aswell as the input so I
can just put a genome in there + the input. The activation function is the sigmoid function.
'''
class Perceptron(object):
    n_hidden_1 = 4
    n_hidden_2 = 4

    def __init__(self, inputs, outputs):#
        self.input = tf.placeholder(tf.float32, [None, inputs], name='Input')
        # fitness of this 'genome'
        self.fitness = 0
        self.num_inputs = inputs

        self.weights = {
            'h1': tf.placeholder(tf.float32, [inputs, self.n_hidden_1], name="Weights_hidden_1"),
            'h2': tf.placeholder(tf.float32, [self.n_hidden_1, self.n_hidden_2], name="Weights_hidden_2"),
            'out': tf.placeholder(tf.float32, [self.n_hidden_2, outputs], name="Weights_out")
        }
        self.biases = {
            'b1': tf.placeholder(tf.float32, [self.n_hidden_1], name="Bias_hidden_1"),
            'b2': tf.placeholder(tf.float32, [self.n_hidden_2], name="Bias_hidden_2"),
            'out': tf.placeholder(tf.float32, [outputs], name="Bias_out")
        }
        # BRAUCHE ICH DEN UNTEREN KRAM GERADE NOCH ?
        # pack die beiden zahlen in ein dict damit ich den key auswaehlen kann
        self.num_biases_weights = {"weights": 0, "bias": 0}
        self.num_biases = 0
        # gives me the number of biases in my network
        for key in self.biases:
            self.num_biases += self.biases[key].get_shape().as_list()[0]
        self.num_biases_weights["bias"] = self.num_biases

        self.num_weights = 0
        # number of weights in the network
        for key in self.weights:
            dimension = self.weights[key].get_shape().as_list()
            self.num_weights += dimension[0] * dimension[1]

        self.num_biases_weights["weights"] = self.num_weights
        self.prediction = self.define_model()

    '''
    Initializes all variables by creating a session
    and returns the session so can use to change values
    PROBABLY DONT NEED THIS ANYMORE SINCE I DONT HAVE VARTIABLES
    '''
    def init_variables(self):
        sess = tf.Session()
        init = tf.global_variables_initializer()
        sess.run(init)
        return sess
    '''
    Defines the model of this Perceptron and also the names that will show in the graph
    when called with tensorboard --logdir=path/to/log/directory
    '''
    def define_model(self):
        # Hidden layer with Sigmoid activation
        with tf.name_scope("Hidden_Layer_1"):
            layer_1 = tf.add(tf.matmul(self.input, self.weights['h1']), self.biases['b1'])
            layer_1 = tf.nn.sigmoid(layer_1)
        # Hidden layer with Sigmoid activation
        with tf.name_scope("Hidden_Layer_2"):
            layer_2 = tf.add(tf.matmul(layer_1, self.weights['h2']), self.biases['b2'])
            layer_2 = tf.nn.sigmoid(layer_2)
        # Output layer with linear activation
        with tf.name_scope('Output_layer'):
            out_layer = tf.matmul(layer_2, self.weights['out']) + self.biases['out']

        prediction = tf.argmax(out_layer, 1, name='Prediction')
        return prediction

    '''
    Activates the current neural net with the input x and the current weights and biases of the genome
    This return a list and I return the integer
    Weights and biases are dictionaries
    '''
    def activate(self, x, weights, biases, sess):
        prediction = sess.run(self.prediction, feed_dict={self.input: x,
                                                          self.weights['h1']: weights['h1'],
                                                          self.weights['h2']: weights['h2'],
                                                          self.weights['out']: weights['out'],
                                                          self.biases['b1']: biases['b1'],
                                                          self.biases['b2']: biases['b2'],
                                                          self.biases['out']: biases['out']
                                                          })
        return prediction[0]

    '''
    Safes the weights and biases of this network to a file
    The session has to be passed and the variables need to initialized
    Don't need it anymore because I have only placeholders in my model
    '''
    def safe_model(self, sess):
        weights_saver = tf.train.Saver()
        save_path = weights_saver.save(sess, "tmp/model1.cpkt")
        print("Model saved in file: %s" % save_path)


# FOR TESTING
def main():
    p = Perceptron(3, 3)
    writer = tf.summary.FileWriter("graph", graph=tf.get_default_graph())
    writer.flush()



if __name__ == "__main__": main()