# DinoMl
This project is written in python 2.7 but it should work for python 3.x.
Using machine learning with genetic algorithm to learn the Chrome game with the Dino . (Here should be a picture)
It uses pyautogui for the button clicks tensorflow for the neural net and tkinter for the gui
## Installation

----------

Download the project to your local computer. Then open a terminal in this folder.
 I advice to use a virtual environment to not cluster your python installation. Here is a link for setting up a virtual environment.
http://python-guide-pt-br.readthedocs.io/en/latest/dev/virtualenvs/

	
After that run `pip install -r requirements.txt` to get all necessary dependencies.
Open Chrome as shown in the picture and start the game once ( not sure if needed)
Then run index.py and the dino should start learning.
**How To:  **

 1. Play with a safed genome
	 Change LEARNING to something else in 
`Learner = mlg.GenLearner(Controller, root, 12, 4, 0.2,'LEARNING')`  in `index.py`.
`j = threading.Thread(target=Learner.start_learning, args=(5,))` change the 5 to the generation you want to replay. It will load this specific genome. Note that will it safe genomes every 5 generations while learning.

 2. Visualization of the neural net
		 For visualization of the neural net you can use  `tensorboard --logdir=graph` to get a visualization of the graph. Just go to the website that will be on 127.0.0.1:some port number and then click on graph to see how the output is computed.
 

 
### Known Bugs

 - Color Inverting
One is not a bug but very annoying. The color inverts at 700 points and because my scanner searches for the color of a pixel it won´t work. Therefore open in Chrome the developer tools (`Ctrl + Shift + I`) go the console and copy paste this: `Runner.config.INVERT_DISTANCE = Infinity`. The code is pretty self explanatory (found this fix in Ivan Seidels tracker in git).

 - Dino on Ice
Another one is that the dino position starts to "slide". I started to reload the page after every game but then the other bug fix won´t be applied since this is how the console works. So here is another line of code you need to add to the console:
    `setInterval(function (){Runner.instance_.tRex.xPos = 21}, 2000)`

*** Pro tipp. In the developer tools under network you can go offline.*** 

	
	
#### Credit


----------


I was inspired by Ivan Seidels https://github.com/ivanseidel/IAMDinosaur implementation + video and wanted to write a clone for it. Even though some code is relatively equal especially for the inputs the sensor and the gameController Ivan Seidels implementation works heavily with callbacks( nodeJs) which I found hard to follow and understand. I use a seperate thread for learning the game that controls the flow of the program and my genomes are not neural networks instead they arte just weight and bias dicts that are then fed into the neural net together with the input. The interaction between the different modules are very different.
	For further information see Ivan Seidels video and github for a better explanation of how it works since I'm to lazy right now.

##### To Do

Clean this readme file 
Don´t need the .pyc files
It still does not work correctly but I need it on another pc
> Written with [StackEdit](https://stackedit.io/).
