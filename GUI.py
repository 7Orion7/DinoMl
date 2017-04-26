import Tkinter as tk
import TextHandler as th
import logging
import ScrolledText
# Geometry String wxh+x+y w and h = width and height in pixels seperated by character x
# +x = left side of window should be x pixels from left side of desktop. If -x right side of window is x pixels from right desktop

class Application(tk.Frame):
    def __init__(self, parent, Controller, Learner):
       self.parent = parent
       self.gc = Controller
       self.mlg = Learner
       tk.Frame.__init__(self, parent)
       # y_strecth = Highest y = max_data_value * y_stretch
       # y_gap = The gap between lower canvas edge and x axis
       # x_stretch = Strecth x wide enough to fit the variables
       #x_width =  the width of the x axis
       #x_gap The gap between the left canvas edge and y axis
       self.bar_settings = { "y_stretch": 25,
                             "y_gap": 20,
                             "x_stretch": 50,
                             "x_width": 90,
                             "x_gap": 50
                             }
       # The tags for the numbers in the bars
       self.tags_text = ["n1", "n2", "n3", "n4"]
       # The tags for the bars
       self.tags_bars = ["b1", "b2", "b3", "b4"]

       self.gameStatus = tk.StringVar()
       self.generation = tk.StringVar()
       self.fitness = tk.StringVar()
       self.genome = tk.StringVar()
       self.action = tk.StringVar()
       self.create_widgets()

    def create_widgets(self):
        self.graph = self.create_graph()

        mlgamestat_frame = tk.Frame(self.parent, width=600, height=300, bg="blue")

        log_frame = tk.Frame(self.parent, width=600, height=300, bg="black")
        self.create_log(log_frame)

        gamestat_frame = tk.Frame(mlgamestat_frame, width=300, height=300, bd=10, bg="black")
        self.create_gameStat(gamestat_frame)

        ml_frame = tk.Frame(mlgamestat_frame, width=300, height=300, bg="black")
        self.create_ml_stats(ml_frame)

        self.graph.grid(row=0, column=0)
        mlgamestat_frame.grid(row=1, column=0)
        gamestat_frame.grid(row=0, column=0)
        ml_frame.grid(row=0, column=1)
        log_frame.grid(row=2, column=0)
        gamestat_frame.grid_propagate(False) # so it won't  collapse
        ml_frame.grid_propagate(False)

    def create_gameStat(self, gamestat_frame):
        l1 = tk.Label(gamestat_frame, text="GameStatus: ", bg="black", fg="white")
        l2 = tk.Label(gamestat_frame, textvariable=self.gameStatus, bg="black", fg="white")
        l1.grid(row=0, column=0)
        l2.grid(row=0, column=1)

        l3 = tk.Label(gamestat_frame, text="Action: ", bg="black", fg="white")
        l4 = tk.Label(gamestat_frame, textvariable=self.action, bg="black", fg="white")
        l3.grid(row=1, column=0)
        l4.grid(row=1, column=1)

    def create_ml_stats(self, ml_stat_frame):
        l1 = tk.Label(ml_stat_frame, text="Generation: ", bg="black", fg="white")
        l2 = tk.Label(ml_stat_frame, textvariable=self.generation, bg="black", fg="white")
        l1.grid(row=0, column=0)
        l2.grid(row=0, column=1)

        l5 = tk.Label(ml_stat_frame, textvariable=self.genome, bg="black", fg="white")
        l5.grid(row=0, column=2)

        l3 = tk.Label(ml_stat_frame, text="Fitness:", bg="black", fg="white")
        l4 = tk.Label(ml_stat_frame, textvariable=self.fitness, bg="black", fg="white")
        l3.grid(row=1, column=0)
        l4.grid(row=1, column=1)

    def create_graph(self):
        graph = tk.Canvas(self.parent, width=600, height=300, bg="black")
        labels = ["Distance", "Size", "Speed", "Activation"]
        test_data = [7, 10, 1, 4]

        for x, y in enumerate(test_data):
            x0 = x * self.bar_settings["x_stretch"] + x * self.bar_settings["x_width"] + self.bar_settings["x_gap"]
            y0 = 300 - (y * self.bar_settings["y_stretch"] + self.bar_settings["y_gap"])
            x1 = x * self.bar_settings["x_stretch"] + x * self.bar_settings["x_width"] + self.bar_settings["x_width"] + self.bar_settings["x_gap"]
            y1 = 300 - self.bar_settings["y_gap"]
            graph.create_rectangle(x0, y0, x1, y1, fill="blue", tag=self.tags_bars[x])
            graph.create_text(x0 + 2, y1 + 15, anchor=tk.SW, text=labels[x], fill="white")
            graph.create_text(x0 + 2, y1, anchor=tk.SW, text=test_data[x] * 10, tag=self.tags_text[x], fill="white")

        return graph

    def create_log(self, log_frame):
        st = ScrolledText.ScrolledText(log_frame, state='disabled', bg="black")
        #st.configure(font='TkFixedFont')
        st.grid(row=0, column=0)
        text_handler = th.TextHandler(st)
        logger = logging.getLogger()
        logger.addHandler(text_handler)


    def render(self):
        # Takes data rounds it and the casts it to integer
        data = [
            int(round(self.gc.sensor.value * 100)),
            int(round(self.gc.sensor.size * 100)),
            int(round(self.gc.sensor.speed * 100)),
            int(round(self.gc.gameOutput * 50 ))
        ]
        '''
        print "RENDER DATA"
        print "Value: " + str(data[0])
        print "Size: " + str(data[1])
        print "Speed: " + str(data[2])
        '''

        #print str(data[3])
        for x, y in enumerate(data):
            x0 = x * self.bar_settings["x_stretch"] + x * self.bar_settings["x_width"] + self.bar_settings["x_gap"]
            y0 = 300 - (y * self.bar_settings["y_stretch"] / 10 + self.bar_settings["y_gap"])
            x1 = x * self.bar_settings["x_stretch"] + x * self.bar_settings["x_width"] + self.bar_settings["x_width"] + \
                 self.bar_settings["x_gap"]
            y1 = 300 - self.bar_settings["y_gap"]
            # changes the graph
            self.graph.coords(self.tags_bars[x],x0, y0, x1, y1)
            # changes the text
            self.graph.itemconfigure(self.tags_text[x], text=str(data[x]))

        # updates for the GameStat Frame maybe using it for debugging
        self.gameStatus.set(self.gc.gameState)
        self.action.set(self.gc.gameOutputString )
        #updates the Ml stats
        self.generation.set(str(self.mlg.generation) + ':')
        self.genome.set(str(self.mlg.genomeNr) + '/' + str(len(self.mlg.genomes)))
        # need the genomes number
        self.fitness.set(str(self.gc.points))

        # can do that when
        self.parent.after(25, self.render) # recursive call




