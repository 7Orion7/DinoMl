import tensorflow as tf
import time
import collections
import copy
import Perceptron as nn
import Genome as gen
import random as rnd
import logging
'''
DINGE DIE ICH DENKE DIE EIN PROBLEM SIND.
2) der output aendert sich nicht waehrend das genome laeuft groestes problem
als ich die weights noch als variablen hatte undhat er mir verschiiedenen ouput gegeben gkaub ich?
3) werden die mutationen richtig ausgefuehrt
kann mit numpy.copy arrays kopieren
4) THE LAST 2 GENOMES NUMBERS ARE STILL WRONG PROBABLY NEED TO PRINT THEM OUT NEXT STEP

'''
class GenLearner(object):
    # hier obens sollte vllt inputs und ouptus mit rein fpr das network
    def __init__(self, Controller, Gui, genomeUnits, selection, mutation_prob, Learning):
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s.%(msecs)03d: %(message)s', datefmt='%H:%M:%S')
        # logging.disable(logging.DEBUG)  # uncomment to block debug log messages

        # Array of netwroks for the current genoems
        self.genomes = []

        self.state = Learning

        #Curent genome/generation tryout
        self.genomeNr = 0
        self.generation = 0
        # set this to verify genome experience BEFORE running it
        self.should_check_experience = True # + was false and slows it down

        self.gc = Controller
        self.gui = Gui
        # genoems per generatin
        self.genome_units = genomeUnits
        # number of genomes that will survive for select the best
        self.selection = selection
        # probability for mutatuion
        self.mutation_prob = mutation_prob
        self.network = nn.Perceptron(3, 3) #inputs and outputs
        #Session to use for running
        self.sess = self.network.init_variables()

    '''
    Builds a genome which is just two lists for the weights and biases
    '''
    def build_genome(self):
        genome = gen.Genome(self.network.num_weights, self.network.num_biases)
        return genome
    '''
    Takes a generation as an argument if you want to execute a specific genome
    '''
    def start_learning(self, generation):
        # build genomes for this generation
        logging.info('Start Learning')
        if self.state == 'LEARNING':
            while len(self.genomes) < self.genome_units:
                self.genomes.append(self.build_genome())
            #wait until the game dies then start again
            while self.gc.gameState != 'OVER':
                self.gc.read_game_state()
            self.execute_generation()
        else:
            self.play_learned(generation)

    '''
    Core
    Given entire generation of genomes as deque execute every genome
    Afterthe generation was executed do:
    1) Select best genomes
    2) Do Cross over (except for 2 genomes
    3) Does Mutation only on remaining genomes
    4) Execute generation recursive?
    I could get control flow problems
    '''
    def execute_generation(self):
        if self.state == 'STOP':
            return
        self.generation += 1
        logging.info('Executing generation ' + str(self.generation))
        # Here is a logger entry
        # THIS COULD NOT WORK
        for genome in self.genomes:
            self.execute_genome(genome)
            time.sleep(1) #timing things
            #here reload the page to stop the bug of sliding sliding bug fixed with code
            #self.gc.reload_page()
        # Kill the worst genomes but this does not return a deque
        self.genomes = self.select_best_genomes(self.selection)
        # copy the best genomes this is a shallow copy could be bad MAYBE NEED DEEEP COPY !
        best_genomes = copy.deepcopy(self.genomes)

        # Safe the best genome every 10 generations
        if self.generation % 5 == 0:
            best_genomes[0].save_genome(self.generation, 0)
            logging.info("Saved Genome")
        #Cross over
        while len(self.genomes) < self.genome_units - 2:
            # get two random genomes
            genA = rnd.choice(best_genomes) # get one random dunno if sample takes deque as argument
            genB = rnd.choice(best_genomes) # the same genome could be chosen twice

            new_genome = self.mutate(self.cross_over(genA, genB))

            self.genomes.append(new_genome) # at end of list
        # Mutation only for the last two genomes
        while len(self.genomes) < self.genome_units:
            gen_ = rnd.choice(best_genomes)
            new_genome = self.mutate(gen_)
            self.genomes.append(new_genome)

        logging.info('Completed generation ' + str(self.generation))
        # call yourself again
        self.genomeNr = 0 #reset
        self.execute_generation()

    '''
    Executes the genome waits until game has ended and starts it with this genome
    so he starts the game
    '''
    def execute_genome(self, genome):
        # logging.info('Executing genome: ' + str(self.genomeNr + 1))
        if self.state == 'STOP':
            return
        self.genomeNr = self.genomes.index(genome) + 1 # returns the number of the genome for execution I can print this

        if self.should_check_experience:
            #Here i need to check the experience of a genome for testing I suppose
            if not self.check_experience:
                genome.fitness = 0
                return # use the next genome
        # Sanity check before the genome starts
        self.gc.read_game_state()
        if self.gc.gameState == 'OVER':
            self.gc.start_new_game() # start a new game for the genome
        # readSensors should update fast enough I think otherwise I need to call it in here
        self.gc.read_game_state()
        # Then it is finished
        while self.gc.gameState != 'OVER':
            self.gc.read_sensors()
            inputs = [
                self.gc.sensor.value,
                self.gc.sensor.size,
                self.gc.sensor.speed
            ]
            # Apply input to the network
            output = self.network.activate([inputs], genome.weights, genome.biases, self.sess)
            self.gc.set_game_output(output)
            # Timing for action should maybe need a stop here or a sleep for a few milii seconds
            time.sleep(.05) # sleeps for 50 ms TESTING IF NOT SLEEPING HELPS
        genome.fitness = self.gc.points
        logging.info('Genome ' + str(self.genomeNr) + " " + 'ended. Fitness: ' + str(self.gc.points))

        return

    def select_best_genomes(self, selectN):
        selected = sorted(self.genomes, key=lambda x: x.fitness, reverse=True)  # sorts by fitness
        print [x.fitness for x in selected]
        # smallest value on last position
        while len(selected) > selectN:
            selected.pop()
        fitness = ','.join([str(x.fitness) for x in selected])  # this should give me the fitness of all the values
        logging.info('Fitness ' + fitness)
        return selected
    '''
    Checks if a given genome has variety.
    '''
    def check_experience(self, genome):
        step, start, stop = 0.1, 0.0, 1
        # default inputs for testing
        inputs = [0.0, 0.3, 0.2]
        outputs = {}
        for k in range(start, stop):
            inputs[0] = k
            activation = genome.activate(inputs)
            state = self.gc.get_discrete_state(activation) # get the action corresponding to it works with the indices what activation returns
            outputs[state] = True
        # Count the states in the outputs dictionary and return true or false
        return len(outputs) > 1

    '''
    Cross over between two genomes
    '''
    def cross_over(self, genA, genB):
        if rnd.random() > 0.5:
            tmp = genA
            genA = genB
            genB = tmp
        # Maybe I need deepcopies

        genA = copy.deepcopy(genA)
        genB = copy.deepcopy(genB)

        self.cross_over_data_keys(genA, genB, 'bias')

        return genA

    '''
    Mutation call for bias and weights
    '''
    def mutate(self, gen):
        new_gen = copy.deepcopy(gen) #I think this is necessary otherwise the last two genomes could be the same strange bug in the logs
        self.mutate_data_keys(new_gen, 'weights', self.mutation_prob)

        self.mutate_data_keys(new_gen, 'bias', self.mutation_prob)
        return gen

    '''
    Given two Genomes A and B
    1) Select cross over point randomly ( from 0 to A.num_biases)
    2) Swap value from 'key'(in this case biases other not implemented) to another
        starting at cutLocation
        If cut_location is max it won't vut anything
    '''
    # Careful internally the keys are correctly ordered in the hash map so I don need iteritems() for the biases
    # This is not true for the weights!
    def cross_over_data_keys(self, genA, genB, key):
        cut_location = int(round(rnd.random() * genA.num_biases))
        for key in genA.biases:
            # this shit return the dimension as integer
            dimension = genA.get_dimension(genA.biases[key])[0]
            # If cut_location is bigger then the key entry dimension these biases will not get changed# find starting point from which to cut
            if dimension < cut_location:
                cut_location -= dimension
                continue
            else:
                for x in range(cut_location, dimension):
                    tmp = genA.biases[key][x]
                    genA.biases[key][x] = genB.biases[key][x]
                    genB.biases[key][x] = tmp
                #set cut_location to zero since we want to update every will now
                cut_location = 0

    '''
    Random mutation on all the biases and weights of one network
    key is either bias or weights as string !
    changes values if threshhold is not reached mutationRate should be low
    '''
    def mutate_data_keys(self, gen, key, mutationRate):

        if key == 'weights':
            # This iterates in the correct order over the elements
            for key, value in sorted(gen.weights.iteritems()):
                dimension = gen.get_dimension(value)
                for x in range(0, dimension[0]):
                    for y in range(0, dimension[1]):
                        # Should I mutate?
                        if rnd.random() > mutationRate:
                            continue
                        # I dunno why these values
                        value[x][y] += value[x][y] + (rnd.random() - 0.5) * 3 + (rnd.random() - 0.5)

        else:
            for key, value in gen.biases.iteritems():
                dimension = gen.get_dimension(value)
                for x in range(0, dimension[0]):
                    # Should i mutate?
                    if rnd.random() > mutationRate:
                        continue
                    value[x] += value[x] + (rnd.random() - 0.5) * 3 + (rnd.random() - 0.5)
                    # Added += instead of only = COULD BE HUGE
    '''
    Plays one game with the learned genome. Maybe should make an iteration constant to see more games in a loop
    '''
    def play_learned(self, generation):
        # filename is hardcoded
        filename = "genomes/genome_0_generation_" + str(generation) + ".json"
        genome = self.build_genome()
        genome.load_genome(generation, 0)
        # now execute genome
        self.execute_genome(genome)
        return
