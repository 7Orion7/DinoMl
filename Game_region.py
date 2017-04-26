import pyautogui
import logging
import autopy

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s.%(msecs)03d: %(message)s', datefmt='%H:%M:%S')
logging.disable(logging.DEBUG) # uncomment to block debug log messages


'''
Gets the Game region form the pixel and the coordinates of the play again button
Even though I don use it anymore.
'''


class GameRegion(object):
    x_pad = 223 # need to do it like this sonce the highscore changes verytime and locateOnScreen won#t find it otherwise
    y_pad = 143 # very bad solutiuon

    def __init__(self):

        rect = ((self.x_pad + 1, self.y_pad +1), (610, 137)) #rest of the alues hardcoded not that good but changeable
        bitmap = autopy.bitmap.capture_screen(rect)
        bitmap.save('pic/game.png')

        '''
        # There is a known bug with grab() and gtk Xvfb which is an X server
        PyGTK back-end does not check $DISPLAY -> not working with Xvfb
        im = ImageGrab.grab(bbox=(self.x_pad + 1, self.y_pad + 1, self.x_pad + 610, self.y_pad + 137))
        im.save('game.png')
        '''
        self.Game_Region = self.__get_game_region()
    '''
    https://mail.python.org/pipermail/tutor/2003-October/025932.html <= why python has no private methods
    Finds the gameRegion for now but I don#t like it this way
    '''
    def __get_game_region(self):
        logging.debug('Finding game region ....')
        region = pyautogui.locateOnScreen('game.png')
        if region is None:
            raise Exception('Could not find game on screen. Is the game visible?')

        #            x pad      y padding
        top_left = (region[0], region[1])
        #               width of the game       height of the game
        bottom_right = (region[0] + region[2], region[1] + region[3])

        GAME_REGION = (top_left[0], top_left[1], bottom_right[0], bottom_right[1])
        logging.debug('Game region found: %s' % (GAME_REGION,))
        # but you can restart using the Space bar!
        PLAY_AGAIN = (top_left[0] + 304, top_left[1] + 87)
        return GAME_REGION
