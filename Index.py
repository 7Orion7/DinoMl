import threading
import pyautogui
import Helper
import Tkinter as tk
import GUI

import logging
import MLGen as mlg
import GameController as GC
'''
Speed is buggy bestimmt bei dem crouchen ist der pixel wert falsch das war aber eig nur um 1 muss nochmal testen mit den alten werten
bei alten wert funktioniert es auch niocht richtig. Ich glaube beim buecken findet er seine eigen schnauze bei 321 x wert er sucht ab 314 vorwaerts
WAS because of sliding bug while crouching the ray scan would find the dinos body and then set the distance.
3) I only use the root logger which is maybe bad practice
Genetic algorithm does not work
'''
def main():
    root = tk.Tk()
    screen_sol = (root.winfo_screenwidth(), root.winfo_screenheight())

    Controller = GC.GameController(root, screen_sol)
    game_pos = Controller.find_game_position()
    if game_pos is None:
        print "GAME NOT FOUND"
        return

    Learner = mlg.GenLearner(Controller, root, 12, 4, 0.2, 'LEARNING') # other string if you dont want to learn
    root.geometry('600x900-0+0')  # 120* 50 ppixels in top right corner of desktop
    gui = GUI.Application(root, Controller, Learner)

    gui.master.title('Graph&Stuff')

    # setting the intervals for the game and creating the Learner thread
    t = Helper.set_interval(Controller.read_sensors, 0.04)
    i = Helper.set_interval(Controller.read_game_state, 0.2)

    j = threading.Thread(target=Learner.start_learning, args=(10,)) #did not test if args=5 does work
    #I dont think I start the new game
    Controller.start_new_game()

    root.after(1000, click_on_game, game_pos) # so that the game is focused at the beginning
    root.after(0, gui.render)
    root.after(2000, j.start)
    #root.after(0, Controller.simple_ki) # just for testing button presses
    # Try to learn Vim use Vimtutor is pre installed on linux
    #Helpful to remap CapsLock to Esc for easier switching between lines
    # more sources vim wiki vimcasts
    root.after(0, gui.render)
    gui.mainloop()
    # cancels the intervals but not the Learn thread need to cancel it yourself( You have to kill it)
    t.cancel()
    i.cancel()


'''
    #SHIT INVERTS AT 700 POINTS LOL AND FIX DRIFT BUG
    # when i refresh the code for stopping invertion will not execture
    # Go to console developer tools F12 and Enter: Runner.config.INVERT_DISTANCE = Infinity
    # stops night mode found at github poage https://github.com/ivanseidel/IAMDinosaur/issues/24
      PASTE N CONSOLE IN THE ELEMENT INSPECTOR
setInterval(function (){Runner.instance_.tRex.xPos = 21}, 2000)
    '''
    #t.cancel()

def click_on_game(GR):
    pyautogui.click(x=GR[0], y=GR[1])

if __name__ == "__main__": main()