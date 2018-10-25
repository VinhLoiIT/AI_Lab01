import tkinter as tk
from tkinter import filedialog
from map import UIMap
from algorithm import UIAStarAlgorithm, HeuristicFunction, UIARAAlgorithm
from tkinter.messagebox import showerror
from tkinter import simpledialog

class Toolbar(tk.Frame):
    def __init__(self, master, eventHandler):
        tk.Frame.__init__(self, master)

        self.buttons = dict()

        self.buttons['loadmap'] = tk.Button(self, text='Load map', command=eventHandler.on_load_map_button_click)
        self.buttons['loadmap'].icon = tk.PhotoImage(file='./images/folder.png')
        self.buttons['loadmap'].config(image=self.buttons['loadmap'].icon, compound=tk.LEFT, state=tk.NORMAL)
        self.buttons['loadmap'].pack(side=tk.LEFT, fill=tk.BOTH, pady=2)

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

        self.buttons['ara'] = tk.Button(self, text='ARA', command=eventHandler.on_ara_button_click)
        self.buttons['ara'].icon = tk.PhotoImage(file='./images/next.png')
        self.buttons['ara'].config(image=self.buttons['ara'].icon, compound=tk.LEFT, state=tk.DISABLED)
        self.buttons['ara'].pack(side=tk.LEFT, fill=tk.BOTH, pady=2)

        self.buttons['restart'] = tk.Button(self, text='Restart', command=eventHandler.on_restart_button_click)
        self.buttons['restart'].icon = tk.PhotoImage(file='./images/refresh.png')
        self.buttons['restart'].config(image=self.buttons['restart'].icon, compound=tk.LEFT, state=tk.DISABLED)
        self.buttons['restart'].pack(side=tk.LEFT, fill=tk.BOTH, pady=2)

        heuristic_option_list = list(HeuristicFunction.keys())
        self.heuristic_option = tk.StringVar()
        self.heuristic_option.set(heuristic_option_list[0])
        self.heuristic_option_menu = tk.OptionMenu(self, self.heuristic_option, *heuristic_option_list,
                                                   command=eventHandler.on_heuristic_change)
        self.heuristic_option_menu.pack(side=tk.LEFT, fill=tk.BOTH, pady=0)

    def setAvailability(self, isEnable, *buttonName):
        if len(buttonName) == 0:
            for name, button in self.buttons.items():
                if isEnable:
                    button.config(state=tk.NORMAL)
                else:
                    button.config(state=tk.DISABLED)
        else:
            for name in buttonName:
                if isEnable:
                    self.buttons[name].config(state=tk.NORMAL)
                else:
                    self.buttons[name].config(state=tk.DISABLED)

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

        self.toolbar = Toolbar(self, self)
        self.toolbar.pack(side=tk.TOP, fill=tk.NONE, expand=True)

        self.statusBar = StatusBar(self)
        self.statusBar.pack(side=tk.TOP, fill=tk.BOTH)

        self.map = None
        self.alg = None

        currentHeuristicKey = list(HeuristicFunction.keys())[0]
        self.currentHeuristic = HeuristicFunction[currentHeuristicKey]

    def isMapLoaded(self):
        return self.map is not None

    def onMouseMove(self, _):
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

        node = self.map.graph[row][col]
        self.statusBar.textF.set('{0:.2f}'.format(round(node.F, 2)))
        self.statusBar.textG.set('{0:.2f}'.format(round(node.G, 2)))
        self.statusBar.textH.set('{0:.2f}'.format(round(node.calcH(self.alg.heuristicFunction, self.map.goal), 2)))

    def on_step_button_click(self):
        if self.alg is None:
            # run AStar by default
            self.alg = UIAStarAlgorithm(self.map, self.currentHeuristic)
        self.alg.step()

    def on_heuristic_change(self, heuristic_name):
        self.currentHeuristic = HeuristicFunction[heuristic_name]
        if self.alg is not None:
            print(heuristic_name)
            self.alg.setHeuristicFunction(self.currentHeuristic)

    def on_fast_forward_button_click(self):
        if self.alg is None:
            self.alg = UIAStarAlgorithm(self.map, self.currentHeuristic)
        self.alg.fastForward()

    def on_pause_button_click(self):
        if self.alg is not None:
            self.alg.pause()

    def on_load_map_button_click(self):
        file_path = filedialog.askopenfilename(initialdir='./',
                                               title='Select file',
                                               filetypes=(
                                                   ("txt files", "*.txt"),
                                                   ("all files", "*.*")
                                               ))
        if file_path:
            try:
                if self.map is None:
                    self.map = UIMap(self)
                self.map.clear()
                self.map.loadFromFile(file_path)
                self.map.draw()
                self.map.canvas.pack(side=tk.TOP, fill=tk.BOTH)
                self.map.canvas.bind('<Motion>', self.onMouseMove)
                self.toolbar.setAvailability(True)
            except IOError as err:
                showerror('Error', err)
            pass

    def on_restart_button_click(self):
        self.toolbar.setAvailability(False)
        self.alg.reset()
        self.toolbar.setAvailability(True)

    def on_ara_button_click(self):
        if self.alg is not UIARAAlgorithm:
            coeff = simpledialog.askfloat('Set coefficient', 'Coefficient', parent=self)
            if coeff is not None:
                print('Start algorithm...')
                # timelimit = 1
                self.alg = UIARAAlgorithm(self.map, self.currentHeuristic)
                self.alg.setCoeff(coeff)
                # self.alg.setLimitedTime(timelimit)
                self.alg.fastForward()
                # self.after(timelimit, self.alg.stop)


def run_app():
    root = tk.Tk()
    root.title(' '*80 + 'Demo A*')
    root.resizable(False, False)
    app = Application(master=root)
    app.pack(side=tk.TOP, fill=tk.BOTH)

    app.mainloop()
