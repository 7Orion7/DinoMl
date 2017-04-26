# Scanner helper class for the ray tracing I need to do
import pyautogui
import Helper

#Indexes for clarity
X = 0
Y = 1


class Scanner(object):

    def __init__(self):
        self.screensize = pyautogui.size()

    def is_out_of_bound(self, pos):

        if(pos[X] < 0 or pos[Y] < 0 or
           pos[X] >= self.screensize[X] or
           pos[Y] >= self.screensize[Y]):
            return True
        else:
            return False
    '''
    sanity check for the start X and Y values given to scanUntil
    returns a list object since it needs to be mutable should be a bit careful
    '''
    def make_in_bounds(self, pos1):
        pos = [pos1[X], pos1[Y]]
        if pos[X] < 0:
            pos[X] = 0

        if pos[X] >= self.screensize[X]:
            pos[X] = self.screensize[X] - 1

        if pos[Y] < 0:
            pos[Y] = 0

        if pos[Y] >= self.screensize[Y]:
            pos[Y] = self.screensize[Y] - 1

        return pos # thats a list lol
    '''
    start [X, Y] and step [X,Y] are also list since they need to be mutable
    looks for matchColor(RGB tuple) and adds step to start every iteration untol
    matchColor is found or it is outOfBounds
    if found returns the point as list
    '''
    def scan_until(self, start, step, matchColor, iterLimit):
        iterations = 0
        current = self.make_in_bounds(start)

        if step[X] == 0 and step[Y] == 0:
            return None

        while not self.is_out_of_bound(current):
            color = Helper.pixel_at(current[X], current[Y])
            if color == matchColor:  #Tuple comparison
                return current

            current[X] += step[X]
            current[Y] += step[Y]
            iterations += 1
            if iterations > iterLimit:
                return None

        return None
