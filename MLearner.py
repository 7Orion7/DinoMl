import tensorflow as tf
# Feed forward neural network Perceptron was used with input 3 hidden 4 hidden 4 output 1
# Want neural network that takes as input the distance speed and size and gives output leading to it
# neural network with back propagation for learning should learn after every gameover so linked to that
# or gradient descent as learning method
# should gradient descent every time you get a game over. good when you get more points
# use place holder as input that change when the value changes
# set bias and weights as random
#one input layer then one hidden layer and then the output lawyer
# input will be 3 nodes and output 1 for my value
# output will be between 0 and 1
# input needs to be in the same order e.g not 10  and 10000

# fuck this idea of neural network since i don know which output is good
# Reinforced Learning here is way better since it tries to maximize the points
# So I need Q Learning in an easy way lol
# Network Parameters

# Taking a step is the same as doing an action
# update rule Q(s,a) = r + y(max(Q`(s`,a`)) and the reward is the successful passed obstacles at least I will try with this
# but reward could change for the same input since dist and value could be the same after 10 apssed obstacles
# speed increases over time but not after every obstacle

'''
THIS IS JUST TESTING AND NOT YET IMPLEMENTED
   The reward function should be time to be alive or the points of some sort(jumped cactus) then reinforced learning should work
'''
n_input = 3
n_hidden_1 = 4
n_hidden_2 = 4
n_output = 1
learning_rate = 0.001
n_classes = 10 # divide by 10 to get values between 0 and 1 ? maybe

# create weights and biases for the network
weights = {
    'h1': tf.Variable(tf.random_normal([n_input, n_hidden_1])),
    'h2': tf.Variable(tf.random_normal([n_hidden_1, n_hidden_2])),
    'out': tf.Variable(tf.random_normal([n_hidden_2, n_classes]))
}
biases = {
    'b1': tf.Variable(tf.random_normal([n_hidden_1])),
    'b2': tf.Variable(tf.random_normal([n_hidden_2])),
    'out': tf.Variable(tf.random_normal([n_classes]))
}

