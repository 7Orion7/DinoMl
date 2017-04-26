import collections

'''
Sensor class for saving the all the values
'''
class Sensors(object):

    def __init__(self):
        # value for the lastDistance
        self.lastValue = 1
        # value is the distance
        self.value = 0
        self.lastScore = 0
        # from the start of the strret from the dino to the dino so i just measure before the dino and at the height of the middle of the dino
        # need to compute this initial offset in Game_region and put this in GameController
        self.offset = [84, -15]
        self.step = (4, 0)
        self.length = 0.4      # was 0.3
        # should be around 15 iterations more at least for end

        #Speed
        self.speed = 0
        self.lastComputeSpeed = 0
        # for computing the average speed
        self.lastSpeeds = collections.deque()
        #for size of object cactus
        self.size = 0
        self.computeSize = True
