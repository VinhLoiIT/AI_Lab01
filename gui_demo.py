import tkinter as tk
from tkinter import filedialog
from map import Map
from algorithm import Algorithm, AlgorithmState

class Toolbar(tk.Frame):
    def __init__(self, master, map, eventHandler):
        tk.Frame.__init__(self, master, background='bisque')

        self.buttons = dict()

        self.buttons['loadmap'] = tk.Button(self, text='Load map', command=eventHandler.on_load_map_button_click)
        self.buttons['loadmap'].icon = tk.PhotoImage(file='./images/folder.png')
        self.buttons['loadmap'].config(image=self.buttons['loadmap'].icon, compound=tk.LEFT)
        self.buttons['loadmap'].pack(side=tk.LEFT, expand=1)
        self.map = map

        self.buttons['step'] = tk.Button(self, text='Step', command=eventHandler.on_step_button_click)
        self.buttons['step'].icon = tk.PhotoImage(file='./images/play.png')
        self.buttons['step'].config(image=self.buttons['step'].icon, compound=tk.LEFT)
        self.buttons['step'].pack(side=tk.LEFT, expand=1)

        self.buttons['pause'] = tk.Button(self, text='Pause', command=eventHandler.on_pause_button_click)
        self.buttons['pause'].icon = tk.PhotoImage(file='./images/pause.png')
        self.buttons['pause'].config(image=self.buttons['pause'].icon, compound=tk.LEFT)
        self.buttons['pause'].pack(side=tk.LEFT, expand=1)

        self.buttons['fastforward'] = tk.Button(self, text="Fast Forward", command=eventHandler.on_fast_forward_button_click)
        self.buttons['fastforward'].icon = tk.PhotoImage(file='./images/next.png')
        self.buttons['fastforward'].config(image=self.buttons['fastforward'].icon, compound=tk.LEFT)
        self.buttons['fastforward'].pack(side=tk.LEFT, expand=1)

        self.buttons['restart'] = tk.Button(self, text='Restart', command=eventHandler.on_restart_button_click)
        self.buttons['restart'].icon = tk.PhotoImage(file='./images/refresh.png')
        self.buttons['restart'].config(image=self.buttons['restart'].icon, compound=tk.LEFT)
        self.buttons['restart'].pack(side=tk.LEFT, expand=1)

        heuristic_option_list = list(Algorithm.HeuristicFunction.keys())
        self.heuristic_option = tk.StringVar()
        self.heuristic_option.set(heuristic_option_list[0])
        self.heuristic_option_menu = tk.OptionMenu(self, self.heuristic_option, *heuristic_option_list,
                                                   command=eventHandler.on_heuristic_change)
        self.heuristic_option_menu.pack(side=tk.LEFT, expand=1)



    def setAvailability(self, isEnable):
        for name, button in self.buttons.items():
            if isEnable:
                button.config(state=tk.NORMAL)
            else:
                button.config(state=tk.DISABLED)


class Application(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.map = Map(self)
        self.toolbar = Toolbar(self, self.map, self)
        self.toolbar.pack(side=tk.TOP)
        # self.toolbar.place(x=MapView.CANVAS_WIDTH+5, y=0, anchor=tk.NW)

        # self.map.loadFromFile('../input_4.txt')
        self.map.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.map.draw()

        self.alg = Algorithm(self.map)

    def on_step_button_click(self):
        self.alg.AStarStateMachineStep(1)

    def on_heuristic_change(self, heuristic_name):
        print(heuristic_name)
        self.alg.set_heuristic_function(Algorithm.HeuristicFunction[heuristic_name])

    def on_fast_forward_button_click(self):
        self.fast_forward()

    def on_pause_button_click(self):
        if hasattr(self, 'fast_forward_cb_id'):
            self.after_cancel(self.fast_forward_cb_id)
            del self.fast_forward_cb_id

    def fast_forward(self):
        if self.alg.AStarStateMachineStep(1) != AlgorithmState.DONE:
            self.fast_forward_cb_id = self.after(1, self.fast_forward)


    def on_load_map_button_click(self):
        file_path = filedialog.askopenfilename(initialdir='./',
                                               title='Select file',
                                               filetypes=(
                                                   ("txt files", "*.txt"),
                                                   ("all files", "*.*")
                                               ))
        if file_path:
            self.map.loadFromFile(file_path)
            self.map.draw()
            pass

    def on_restart_button_click(self):
        self.toolbar.setAvailability(False)
        self.alg.restart()
        self.toolbar.setAvailability(True)
        pass


def run_app():
    root = tk.Tk()
    root.resizable(False, False)
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    WIN_WIDTH = 600
    WIN_HEIGHT = 650

    center_screen_x = int((screen_width - WIN_WIDTH) / 2)
    center_screen_y = int((screen_height - WIN_HEIGHT) / 2)

    root.geometry('{0}x{1}+{2}+{3}'.format(WIN_WIDTH, WIN_HEIGHT, center_screen_x, center_screen_y))

    app = Application(master=root)
    app.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    app.mainloop()

#TODO dang chay, doi thuat toan, restart, fast forward