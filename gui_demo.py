import tkinter as tk
from tkinter import filedialog
from map import UIMap, UIEmptyMap
from algorithm import UIAStarAlgorithm, HeuristicFunctions, UIARAAlgorithm
from tkinter.messagebox import showerror
from tkinter import simpledialog

class Toolbar(tk.Frame):

    def __init__(self, master, eventHandler):
        tk.Frame.__init__(self, master)

        self.controls = dict()

        self.controls['loadmap'] = tk.Button(self, text='Load map', command=eventHandler.onLoadMapButtonClick)
        self.controls['loadmap'].icon = tk.PhotoImage(file='./images/folder.png')
        self.controls['loadmap'].config(image=self.controls['loadmap'].icon, compound=tk.LEFT, state=tk.NORMAL)
        self.controls['loadmap'].pack(side=tk.LEFT, fill=tk.BOTH, pady=2)

        self.alg_option = tk.StringVar()
        self.alg_option.set(Application.alg_option_list[0])
        self.controls['algorithm'] = tk.OptionMenu(self, self.alg_option, *Application.alg_option_list,
                                                   command=eventHandler.onAlgorithmOptionChange)
        self.controls['algorithm'].config(state=tk.DISABLED)
        self.controls['algorithm'].pack(side=tk.LEFT, fill=tk.BOTH, pady=0)

        heuristic_option_list = list(HeuristicFunctions.keys())
        self.heuristic_option = tk.StringVar()
        self.heuristic_option.set(heuristic_option_list[0])
        self.controls['heuristic'] = tk.OptionMenu(self, self.heuristic_option, *heuristic_option_list,
                                                   command=eventHandler.onHeuristicOptionChange)
        self.controls['heuristic'].config(state=tk.DISABLED)
        self.controls['heuristic'].pack(side=tk.LEFT, fill=tk.BOTH, pady=0)

        self.controls['step'] = tk.Button(self, text='Step', command=eventHandler.on_step_button_click)
        self.controls['step'].icon = tk.PhotoImage(file='./images/play.png')
        self.controls['step'].config(image=self.controls['step'].icon, compound=tk.LEFT, state=tk.DISABLED)
        self.controls['step'].pack(side=tk.LEFT, fill=tk.BOTH, pady=2)

        self.controls['pause'] = tk.Button(self, text='Pause', command=eventHandler.on_pause_button_click)
        self.controls['pause'].icon = tk.PhotoImage(file='./images/pause.png')
        self.controls['pause'].config(image=self.controls['pause'].icon, compound=tk.LEFT, state=tk.DISABLED)
        self.controls['pause'].pack(side=tk.LEFT, fill=tk.BOTH, pady=2)

        self.controls['stop'] = tk.Button(self, text='Stop', command=eventHandler.onStopButtonClick)
        self.controls['stop'].icon = tk.PhotoImage(file='./images/cross.png')
        self.controls['stop'].config(image=self.controls['stop'].icon, compound=tk.LEFT, state=tk.DISABLED)
        self.controls['stop'].pack(side=tk.LEFT, fill=tk.BOTH, pady=2)

        self.controls['fastforward'] = tk.Button(self, text="Fast Forward", command=eventHandler.on_fast_forward_button_click)
        self.controls['fastforward'].icon = tk.PhotoImage(file='./images/next.png')
        self.controls['fastforward'].config(image=self.controls['fastforward'].icon, compound=tk.LEFT, state=tk.DISABLED)
        self.controls['fastforward'].pack(side=tk.LEFT, fill=tk.BOTH, pady=2)

        self.controls['restart'] = tk.Button(self, text='Restart', command=eventHandler.on_restart_button_click)
        self.controls['restart'].icon = tk.PhotoImage(file='./images/refresh.png')
        self.controls['restart'].config(image=self.controls['restart'].icon, compound=tk.LEFT, state=tk.DISABLED)
        self.controls['restart'].pack(side=tk.LEFT, fill=tk.BOTH, pady=2)

    def __setAvailability(self, isEnable, nameControl):
        try:
            if isEnable:
                self.controls[nameControl].config(state=tk.NORMAL)
            else:
                self.controls[nameControl].config(state=tk.DISABLED)
        except KeyError:
            print('Key wrong:', nameControl)

    def setAvailability(self, isEnable, *args):
        """If args is None, then apply isEnable to ALL controls"""
        if args:
            for name in args:
                self.__setAvailability(isEnable, name)

        else:
            for name, _ in self.controls.items():
                self.__setAvailability(isEnable, name)



class StatusBar(tk.Frame):
    def __init__(self, master):
        self.bgColor = 'bisque'
        tk.Frame.__init__(self, master, background=self.bgColor)
        self.textRow = tk.StringVar()
        self.textCol = tk.StringVar()
        self.textF = tk.StringVar()
        self.textG = tk.StringVar()
        self.textH = tk.StringVar()
        self.textResult = tk.StringVar()

        self.addTextStatus('Row:', self.textRow)
        self.addTextStatus('Col:', self.textCol)
        self.addTextStatus('G:', self.textG)
        self.addTextStatus('H:', self.textH)
        self.addTextStatus('F:', self.textF)
        self.addTextStatus('Result:', self.textResult)

    def addTextStatus(self, labelText, observer):
        frame = tk.Frame(self)
        frame.pack(side=tk.LEFT, fill=tk.BOTH)
        label = tk.Label(frame, text=labelText, background=self.bgColor, fg='blue')
        label.pack(side=tk.LEFT, fill=tk.BOTH)
        content = tk.Label(frame, textvariable=observer, background=self.bgColor, width=10, fg='red')
        content.pack(side=tk.LEFT, fill=tk.BOTH)

    def statusChangeCallback(self, node, heuristicValue):
        self.textRow.set(str(node.row))
        self.textCol.set(str(node.col))
        self.textF.set('{0:.2f}'.format(round(node.F, 2)))
        self.textG.set('{0:.2f}'.format(round(node.G, 2)))
        self.textH.set('{0:.2f}'.format(round(heuristicValue, 2)))

    def solutionChangeCallback(self, solution):
        self.textResult.set(str(len(solution)))


class Application(tk.Frame):

    alg_option_list = ['A*', 'ARA']

    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.toolbar = Toolbar(self, self)
        self.toolbar.pack(side=tk.TOP, fill=tk.NONE, expand=True)

        self.statusBar = StatusBar(master)
        self.statusBar.pack(side=tk.TOP, fill=tk.BOTH)

        currentHeuristicKey = list(HeuristicFunctions.keys())[0]
        self.currentHeuristic = HeuristicFunctions[currentHeuristicKey]

        self.alg = UIAStarAlgorithm(self.currentHeuristic)
        self.map = UIEmptyMap(self)

        currentAlgKey = self.alg_option_list[0]
        self.changeAlgorithm(currentAlgKey)

    def initDefault(self):
        self.map = UIEmptyMap(self)
        self.map.canvas.pack(side=tk.TOP, fill=tk.BOTH)


    def on_step_button_click(self):
        self.alg.step()
        self.toolbar.setAvailability(True)
        self.toolbar.setAvailability(False, 'algorithm', 'heuristic')

    def onHeuristicOptionChange(self, heuristic_name):
        self.currentHeuristic = HeuristicFunctions[heuristic_name]
        self.alg.setHeuristicFunction(self.currentHeuristic)

    def on_fast_forward_button_click(self):
        self.alg.fastForward()
        self.toolbar.setAvailability(False)
        self.toolbar.setAvailability(True, 'pause', 'stop')
        if isinstance(self.alg, UIARAAlgorithm):
            self.toolbar.setAvailability(False, 'pause')

    def on_pause_button_click(self):
        self.alg.pause()
        self.toolbar.setAvailability(False)
        self.toolbar.setAvailability(True, 'step', 'fastforward', 'restart')

    def onStopButtonClick(self):
        self.alg.stop()
        self.toolbar.setAvailability(False)
        self.toolbar.setAvailability(True, 'loadmap', 'restart')

    def onAlgorithmDone(self, solution):
        self.statusBar.solutionChangeCallback(solution)
        self.toolbar.setAvailability(False)
        self.toolbar.setAvailability(True, 'loadmap', 'restart')


    def onLoadMapButtonClick(self):
        file_path = filedialog.askopenfilename(initialdir='./',
                                               title='Select file',
                                               filetypes=(
                                                   ("txt files", "*.txt"),
                                                   ("all files", "*.*")
                                               ))
        if file_path:
            try:
                map = UIMap(self)
                map.loadFromFile(file_path)
                self.changeMap(map)
            except IOError as err:
                showerror('Error', err)

    def restart(self):
        self.alg.stop()
        self.alg.restart()
        self.statusBar.textResult.set('')

    def on_restart_button_click(self):
        self.restart()
        self.buttonAlgorithmState()

    def buttonAlgorithmState(self):
        self.toolbar.setAvailability(True)
        self.toolbar.setAvailability(False, 'pause', 'stop')
        if isinstance(self.alg, UIARAAlgorithm):
            self.toolbar.setAvailability(False, 'step')

    def changeAlgorithm(self, name):
        self.alg.map.reset() #TODO co the luc moi vao chua co map!!
        if name == 'A*' and self.alg is not UIAStarAlgorithm:
            self.alg = UIAStarAlgorithm(self.currentHeuristic)
        elif name == 'ARA' and self.alg is not UIARAAlgorithm:
            self.alg = UIARAAlgorithm(self.currentHeuristic)
        else:
            raise ValueError('Invalid type')
        # self.restart()

        self.alg.setMap(self.map)
        self.alg.registerCallbackDone(self.onAlgorithmDone)
        self.alg.registerStatusNodeCallback(self.statusBar.statusChangeCallback)

    def onAlgorithmOptionChange(self, name):
        """Called when user click on option menu 'ARA' or 'A*'"""
        self.changeAlgorithm(name)

    def changeMap(self, newMap):
        self.alg.reset()
        self.map.destroy()
        self.map = newMap
        self.map.draw()
        self.map.canvas.pack(side=tk.TOP, fill=tk.BOTH)

        self.alg.setMap(self.map)
        self.alg.registerCallbackDone(self.onAlgorithmDone)
        self.alg.registerStatusNodeCallback(self.statusBar.statusChangeCallback)

        self.buttonAlgorithmState()





def run_app():
    root = tk.Tk()
    root.title(' '*80 + 'Demo A*')
    root.resizable(False, False)
    app = Application(master=root)
    app.pack(side=tk.TOP, fill=tk.BOTH)

    app.mainloop()
