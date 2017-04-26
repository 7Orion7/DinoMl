from __future__ import division #forces division to be floating point not integer
import Sensors as sensor
import Scanner as sc
import pyautogui
import time

'''
Controls the game by controlling the sensor and the gameState.
'''
class GameController(object):
    COLOR_DINOSAUR = (83, 83, 83)

    def __init__(self, root, screen_sol): #root is the window need it for after calls
        self.offset = (230, 270) #hardcoded Offset but I calculate it now
        #Start of the black line
        self.width = 600 # game is always 600 pixels long
        # game over position
        self.gameOverOffset = [190, -82]    # Thats possibly not working => it does
        # Stores points (jumps)
        self.points = 0
        self.lastScore = 0

        #Game State
        self.gameState = 'OVER'
        self.gameOutput = 0
        self.gameOutputString = 'None'

        self.sensor = sensor.Sensors()
        self.Scanner = sc.Scanner()
        self.root = root

        # Checking that he can jump while he is jumping
        self.lastOutputSet = 'NONE'
        self.lastOutputSetTime = 0
        #screen is a tuple width x height
        self.screensize = screen_sol

    def find_game_position(self):
        pos, dino_pos, skip_x_fast = (15, 15, 15)
        #Finds the start of the black line start, stop, steps
        for x in range(20, self.screensize[0], skip_x_fast):
            dino_pos = self.Scanner.scan_until(
                [x, 80],
                [0, skip_x_fast],
                self.COLOR_DINOSAUR,
                500 / skip_x_fast
            )
            if dino_pos:
                break
        if not dino_pos:
            return None

        for x in range(dino_pos[0] - 50, dino_pos[0]):
            pos = self.Scanner.scan_until(
                [x, dino_pos[1] - 2],
                [0, 1],
                self.COLOR_DINOSAUR,
                100
            )
            if pos:
                break
        if not pos:
            return None
        self.offset = (pos[0], pos[1] - 1)
        return pos
    '''
    Checks if dino passed an obstacle since value gives the distance to one
    obstacle close => value small
    '''
    def compute_points(self):
        if self.sensor.value > 0.5 and self.sensor.lastValue < 0.2:  #: changed to 0.2
            self.points += 1

    def read_game_state(self):
        # search if Game ended
        found = self.Scanner.scan_until(
            [self.offset[0] + self.gameOverOffset[0],
             self.offset[1] + self.gameOverOffset[1]],

            [2, 0], self.COLOR_DINOSAUR, 20
        )
        # Case when the game is over
        if found and self.gameState != 'OVER':
            self.gameState = 'OVER'

            self.set_game_output(1)

        #Case when the game is not over but gameState not refreshed clear all the keys only called after game over
        elif not found and self.gameState != 'PLAYING':

            self.gameState = 'PLAYING'
            #pyautogui.keyDown('down')
            #pyautogui.press('space') # up works but down does not or I just don
            #clear Points
            self.points = 0
            self.lastScore = 0

            #clear keys
            # setGameOitput().05

            #clear Sensors
            self.sensor.lastComputeSpeed = 0
            self.sensor.lastSpeeds.clear()
            self.sensor.lastValue = 0
            self.sensor.value = 1
            self.sensor.speed = 0
            self.sensor.size = 0

            #clear output flags
            self.lastOutputSet = 'NONE'

        #self.root.after(200, self.readGameState) # recursive call

            # Here is a call to the onGAme Start function

    '''
    Called when the game is over. Maybe I should clear all the stuff in here

    '''
    def start_new_game(self):
        '''
        pyautogui.keyDown('space')
        pyautogui.keyUp('space')
        '''
        pyautogui.press('space')

        #pyautogui.press('  ')

    """
    Reads the sensors and fills in the values core element
    """
    def read_sensors(self):
        offset = self.offset

        startTime = time.time() # UNIX time
        start = [offset[0] + self.sensor.offset[0],
                 offset[1] + self.sensor.offset[1]
                 ]
        # searches for the next obstacle in front of the dino to as specific length
        end = self.Scanner.scan_until(
            [start[0], start[1]],
            self.sensor.step,
            self.COLOR_DINOSAUR,
            (self.width * self.sensor.length) / self.sensor.step[0]
        )
        # save lsat value
        self.sensor.lastValue = self.sensor.value
        # what is value
        if end:
            self.sensor.value = (end[0] - start[0]) / (self.width * self.sensor.length)

            # Calculate the size of the obstacle by scanning from behind
            end_point = self.Scanner.scan_until(
                [end[0] + 75, end[1]],
                (-2, 0),
                self.COLOR_DINOSAUR,
                75/2
            )
            # If no endPoint set the start poiint as end
            if not end_point:
                end_point = end
            sizeTmp = (end_point[0] - end[0]) / 100.0

            if self.points == self.sensor.lastScore:
                # Then it is the same obstacle and size is max of old and new
                self.sensor.size = max(self.sensor.size, sizeTmp)
            else:
                self.sensor.size = sizeTmp
            # current Score for object equality
            self.sensor.lastScore = self.points
        else:
            self.sensor.value = 1
            self.sensor.size = 0

        # compute speed
        dt = (time.time() - self.sensor.lastComputeSpeed) #time returns the number in seconds whereas in js it is in milli sedconds thats why he divides by 1000
        self.sensor.lastComputeSpeed = time.time()

        if self.sensor.value < self.sensor.lastValue:
            new_speed = (self.sensor.lastValue - self.sensor.value) / (dt * 10)  # speed is factor 10 to big
            '''
            print 'SENSORDATA'
            #print "newSpeed:" + str(newSpeed)
            print "value:" + str(self.sensor.value)
            #print "lastValue:" + str(self.sensor.lastValue)
            #print "dt:" + str(dt)
            #print "newSpeed:" + str(newSpeed)
            '''
            self.sensor.lastSpeeds.appendleft(new_speed)

            while len(self.sensor.lastSpeeds) > 10:
                self.sensor.lastSpeeds.pop()

            # compute average
            avg_speed = 0
            length = len(self.sensor.lastSpeeds)

            for speed in self.sensor.lastSpeeds:
                avg_speed += speed / length

            # In the dinoAi there is this mysterious -1.5 from the avgSpeed but it does not semm to fit for me
            self.sensor.speed = max(avg_speed, self.sensor.speed)

        self.sensor.size = min(self.sensor.size, 1.0)
        startTime = time.time()
        #Compute points dunno if it is best here
        self.compute_points()
    '''
    Maps the output to an string corresponding to the action
    Why these numbers react to these values was chosen randomly and should not be important
    '''
    def get_discrete_state(self, output):
        if output == 0:
            return 'DOWN'
        elif output == 1:
            return 'NORM'
        return 'JUMP'

    def set_game_output(self, output):
        self.gameOutput = output
        self.gameOutputString = self.get_discrete_state(output)

        if self.gameOutputString == 'DOWN':
            # press the down key
            pyautogui.keyUp('up') # just for safety measures
            # hold down the down key lol
            pyautogui.keyDown('down')
        elif self.gameOutputString == 'NORM':
            # release both keys
            pyautogui.keyUp('up')
            pyautogui.keyUp('down')
        else:
            # need to filter jump since I can jump while I jump
            # pressing down after jump makes me fall faster
            if self.lastOutputSet is not 'JUMP':
                self.lastOutputSetTime = time.time()  # returns time in seconds
                # if i Did jump lastOutputSetTime would be bigger and not samller than 3 3 seconds is the time for one jump
            if time.time() - self.lastOutputSetTime < 3:
                # here I jump
                #HE holds down the jump buztton
                #but this should be a press not a holdin g but since it was buggy testing I let this be for now
                #pyautogui.press('up') still need to release down key otherwise I won jump
                pyautogui.keyUp('down')
                pyautogui.keyDown('up')
            else:
                # 'here I don jump'
                pyautogui.keyUp('up')
                pyautogui.keyUp('down')

        self.lastOutputSet = self.gameOutputString
    '''
    Reload the page since the dino starts to slide off
    Works only for linux and windows since I press Ctrl R and not the mac version
    After the press I need to wait or everything is too fast
    '''
    def reload_page(self):
        pyautogui.hotkey('ctrl', 'r')
        self.gameState = 'OVER'
        time.sleep(.7)  # wait one second

    def simple_ki(self):
        '''
        if self.sensor.value < 0.4:
            pyautogui.keyUp('down')
            pyautogui.keyDown('up')
            pyautogui.keyUp('up')
        else:
            pyautogui.keyDown('down')
        '''
        if self.sensor.value > 0.8:
            pyautogui.keyUp('up')  # just for safety measures
            # hold down the down key lol
            pyautogui.keyDown('down')
        elif self.sensor.value < 0.4:
            pyautogui.keyUp('down')
            pyautogui.keyDown('up')
            pyautogui.keyUp('up')
        self.root.after(50,  self.simple_ki) #testing