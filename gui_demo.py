import tkinter as tk
from tkinter import filedialog
from map import Map
from algorithm import Algorithm, AlgorithmState
from tkinter.messagebox import showerror


class Toolbar(tk.Frame):
    def __init__(self, master, map, eventHandler):
        tk.Frame.__init__(self, master)

        self.buttons = dict()

        self.buttons['loadmap'] = tk.Button(self, text='Load map', command=eventHandler.on_load_map_button_click)
        self.buttons['loadmap'].icon = tk.PhotoImage(file='./images/folder.png')
        self.buttons['loadmap'].config(image=self.buttons['loadmap'].icon, compound=tk.LEFT, state=tk.NORMAL)
        self.buttons['loadmap'].pack(side=tk.LEFT, fill=tk.BOTH, pady=2)
        self.map = map

        self.buttons['step'] = tk.Button(self, text='Step', command=eventHandler.on_step_button_click)
        self.buttons['step'].icon = tk.PhotoImage(file='./images/play.png')
        self.buttons['step'].config(image=self.buttons['step'].icon, compound=tk.LEFT, state=tk.DISABLED)
        self.buttons['step'].pack(side=tk.LEFT, fill=tk.BOTH, pady=2)

        self.buttons['pause'] = tk.Button(self, text='Pause', command=eventHandler.on_pause_button_click)
        self.buttons['pause'].icon = tk.PhotoImage(file='./images/pause.png')
        self.buttons['pause'].config(image=self.buttons['pause'].icon, compound=tk.LEFT, state=tk.DISABLED)
        self.buttons['pause'].pack(side=tk.LEFT, fill=tk.BOTH, pady=2)

        self.buttons['fastforward'] = tk.Button(self, text="Fast Forward", command=eventHandler.on_fast_forward_button_click)
        self.buttons['fastforward'].icon = tk.PhotoImage(file='./images/next.png')
        self.buttons['fastforward'].config(image=self.buttons['fastforward'].icon, compound=tk.LEFT, state=tk.DISABLED)
        self.buttons['fastforward'].pack(side=tk.LEFT, fill=tk.BOTH, pady=2)

        self.buttons['restart'] = tk.Button(self, text='Restart', command=eventHandler.on_restart_button_click)
        self.buttons['restart'].icon = tk.PhotoImage(file='./images/refresh.png')
        self.buttons['restart'].config(image=self.buttons['restart'].icon, compound=tk.LEFT, state=tk.DISABLED)
        self.buttons['restart'].pack(side=tk.LEFT, fill=tk.BOTH, pady=2)

        heuristic_option_list = list(Algorithm.HeuristicFunction.keys())
        self.heuristic_option = tk.StringVar()
        self.heuristic_option.set(heuristic_option_list[0])
        self.heuristic_option_menu = tk.OptionMenu(self, self.heuristic_option, *heuristic_option_list,
                                                   command=eventHandler.on_heuristic_change)
        self.heuristic_option_menu.pack(side=tk.LEFT, fill=tk.BOTH, pady=0)

    def setAvailability(self, isEnable):
        for name, button in self.buttons.items():
            if isEnable:
                button.config(state=tk.NORMAL)
            else:
                button.config(state=tk.DISABLED)


class StatusBar(tk.Frame):
    def __init__(self, master):
        self.bgColor = 'bisque'
        tk.Frame.__init__(self, master, background=self.bgColor)
        self.textRow = tk.StringVar()
        self.textCol = tk.StringVar()
        self.textF = tk.StringVar()
        self.textG = tk.StringVar()
        self.textH = tk.StringVar()

        self.addTextStatus('Row:', self.textRow)
        self.addTextStatus('Col:', self.textCol)
        self.addTextStatus('G:', self.textG)
        self.addTextStatus('H:', self.textH)
        self.addTextStatus('F:', self.textF)

    def addTextStatus(self, label, observer):
        frame = tk.Frame(self, width=100)
        frame.pack(side=tk.LEFT, fill=tk.BOTH)
        tk.Label(frame, text=label, background=self.bgColor, width=5, fg='blue').pack(side=tk.LEFT, fill=tk.BOTH)
        tk.Label(frame, textvariable=observer, background=self.bgColor, width=10, fg='red').pack(side=tk.LEFT, fill=tk.BOTH)

class Application(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.map = Map(self, True)
        self.toolbar = Toolbar(self, self.map, self)
        self.statusBar = StatusBar(self)

        self.toolbar.pack(side=tk.TOP, fill=tk.NONE, expand=True)
        self.map.canvas.pack(side=tk.TOP, fill=tk.BOTH)
        self.map.canvas.bind('<Motion>', self.onMouseMove)
        self.statusBar.pack(side=tk.TOP, fill=tk.BOTH)

        self.alg = Algorithm(self.map)

    def isMapLoaded(self):
        return self.map.rows != 0 and self.map.cols != 0

    def onMouseMove(self, event):
        if self.isMapLoaded():
            nodeId = self.map.canvas.find_withtag(tk.CURRENT)
            coord = self.map.canvas.coords(nodeId)
            if len(coord) != 0:
                x = coord[0]
                y = coord[1]
                row = int(y / self.map.nodeWidth)
                col = int(x / self.map.nodeHeight)
                self.triggerStatusText(row, col)

    def triggerStatusText(self, row, col):
        self.statusBar.textRow.set(str(row))
        self.statusBar.textCol.set(str(col))
        self.statusBar.textF.set('{0:.2f}'.format(round(self.alg.F[row][col], 2)))
        self.statusBar.textG.set('{0:.2f}'.format(round(self.alg.G[row][col], 2)))
        self.statusBar.textH.set('{0:.2f}'.format(round(self.alg.heuristic_function((row, col), self.map.goal), 2)))

    def on_step_button_click(self):
        self.alg.AStarStateMachineStep(1)

    def on_heuristic_change(self, heuristic_name):
        print(heuristic_name)
        self.alg.set_heuristic_function(Algorithm.HeuristicFunction[heuristic_name])

    def on_fast_forward_button_click(self):
        if not hasattr(self, 'fast_forward_cb_id'):
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
            try:
                self.map.loadFromFile(file_path)
                self.map.draw()
                self.alg.onUpdateMap()
                self.toolbar.setAvailability(True)
            except IOError as err:
                showerror('Error', err)
            pass

    def on_restart_button_click(self):
        self.toolbar.setAvailability(False)
        self.alg.restart()
        self.toolbar.setAvailability(True)
        pass


def run_app():
    root = tk.Tk()
    root.title(' '*80 + 'Demo A*')
    root.resizable(False, False)
    app = Application(master=root)
    app.pack(side=tk.TOP, fill=tk.BOTH)

    app.mainloop()
