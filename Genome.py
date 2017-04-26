from numpy import random
import json
import numpy as np

'''
Class for Genomes
A Genome has a weight and bias list
Feed the Genome to the neural network.
This way I have one neural net and just plug in the genomes + input
'''

class Genome(object):
    n_hidden_1 = 4
    n_hidden_2 = 4
    # tuple of dimensions for the weights

    def __init__(self, num_weights, num_biases):
        # kann num_weights eig aus dimensions tupel lesen
        self.num_weights = num_weights
        self.num_biases = num_biases
        self.fitness = 0
        self.biases = {
            'b1': [],
            'b2': [],
            'out': []
        }
        self.weights = {
            'h1': [],
            'h2': [],
            'out': []
        }
        self.init()
    '''
    Initializes the weights and biases for this genome with stdev of 0.1
    it is the same as the perceptron form the dimensions so I hardcoded it
    '''
    def init(self):
        self.weights['h1'] = random.normal(0, 1, (3, self.n_hidden_1))
        self.weights['h2'] = random.normal(0, 1, (self.n_hidden_1, self.n_hidden_2))
        self.weights['out'] = random.normal(0, 1, (self.n_hidden_2, 3))

        self.biases['b1'] = random.normal(0, 1, self.n_hidden_1)
        self.biases['b2'] = random.normal(0, 1, self.n_hidden_2)
        self.biases['out'] = random.normal(0, 1, 3)

    '''
    Returns the dimension of a given np_array or array
    returns: Tuple(m, n) m= rows n = columns
    '''
    def get_dimension(self, np_array):
        return np_array.shape

    '''
    Saves the weights and biases in one JSON file.
    With generation and genNr. Since I can serialize numpy arrays I need to first create arrays.
    I use an array/list with two dicts to put it into one JSON file.
    '''
    def save_genome(self, generation, genNr):
        filename = 'genome_' + str(genNr) + "_generation_" + str(generation) + ".json"
        new_dict_weights = {}
        new_dict_biases = {}
        for key, value in sorted(self.weights.iteritems()):
            new_dict_weights[key] = value.tolist()
        for key in self.biases:
            new_dict_biases[key] = self.biases[key].tolist()

        new_list = [new_dict_weights, new_dict_biases]
        with open('genomes/' + filename, 'w') as fp:
            json.dump(new_list, fp, sort_keys=True, indent=4)

    '''
    Loads the weights and biases of a saved genome to this one.
    '''
    def load_genome(self, generation, genNr):
        filename = 'genome_' + str(genNr) + "_generation_" + str(generation) + ".json"
        with open('genomes/' + filename, 'r') as fp:
            new_list = json.load(fp)
        self.weights = new_list[0]
        self.biases = new_list[1]
        #Create numpy arrays
        for key in self.weights:
            self.weights[key] = np.array(self.weights[key])
        for key in self.biases:
            self.biases[key] = np.array(self.biases[key])

def main():
    p = Genome(2, 3)

    genA = Genome(3,3)
    print genA.weights
    genB = Genome(3,3)
    genA.save_genome(1, 2)
    genA.load_genome(1, 2)
    print "Weights before"
    print genA.weights['h2']
    print genA.biases

if __name__ == "__main__": main()

