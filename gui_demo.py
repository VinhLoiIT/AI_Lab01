import tkinter as tk
from tkinter import filedialog
from tkinter.font import Font
from node import UINode
from map import UIMap, UIEmptyMap
from algorithm import UIAStarAlgorithm, HeuristicFunctions
from tkinter.messagebox import showerror
from tkinter import simpledialog
import sys
import os

def resourcePath(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class Toolbar(tk.Frame):

    def __init__(self, master, eventHandler):
        tk.Frame.__init__(self, master, bg='bisque')
        self.grid_propagate()
        self.controls = dict()

        buttonWidth = 70
        self.controls['loadmap'] = tk.Button(self, text='Load map', command=eventHandler.onLoadMapButtonClick, width=buttonWidth)
        self.controls['loadmap'].icon = tk.PhotoImage(file=resourcePath('images/folder.png'))
        self.controls['loadmap'].config(image=self.controls['loadmap'].icon, compound=tk.LEFT, state=tk.NORMAL)
        self.controls['loadmap'].grid(row=0, column=0, pady=2, padx=2, sticky=tk.NSEW, rowspan=2)

        self.controls['step'] = tk.Button(self, text='Step', command=eventHandler.on_step_button_click,width=buttonWidth)
        self.controls['step'].icon = tk.PhotoImage(file=resourcePath('images/play.png'))
        self.controls['step'].config(image=self.controls['step'].icon, compound=tk.LEFT, state=tk.DISABLED)
        self.controls['step'].grid(row=0, column=1, pady=2, padx=2, sticky=tk.NSEW, rowspan=2)

        self.controls['pause'] = tk.Button(self, text='Pause', command=eventHandler.on_pause_button_click,width=buttonWidth)
        self.controls['pause'].icon = tk.PhotoImage(file=resourcePath('images/pause.png'))
        self.controls['pause'].config(image=self.controls['pause'].icon, compound=tk.LEFT, state=tk.DISABLED)
        self.controls['pause'].grid(row=0, column=2, pady=2, padx=2, sticky=tk.NSEW, rowspan=2)

        self.controls['stop'] = tk.Button(self, text='Stop', command=eventHandler.onStopButtonClick,width=buttonWidth)
        self.controls['stop'].icon = tk.PhotoImage(file=resourcePath('images/cross.png'))
        self.controls['stop'].config(image=self.controls['stop'].icon, compound=tk.LEFT, state=tk.DISABLED)
        self.controls['stop'].grid(row=0, column=3, pady=2, padx=2, sticky=tk.NSEW, rowspan=2)

        self.controls['run'] = tk.Button(self, text="Run", command=eventHandler.on_fast_forward_button_click,width=buttonWidth)
        self.controls['run'].icon = tk.PhotoImage(file=resourcePath('images/next.png'))
        self.controls['run'].config(image=self.controls['run'].icon, compound=tk.LEFT, state=tk.DISABLED)
        self.controls['run'].grid(row=0, column=4, pady=2, padx=2, sticky=tk.NSEW, rowspan=2)

        self.controls['restart'] = tk.Button(self, text='Restart', command=eventHandler.on_restart_button_click,width=buttonWidth)
        self.controls['restart'].icon = tk.PhotoImage(file=resourcePath('images/refresh.png'))
        self.controls['restart'].config(image=self.controls['restart'].icon, compound=tk.LEFT, state=tk.DISABLED)
        self.controls['restart'].grid(row=0, column=5, pady=2, padx=2, sticky=tk.NSEW, rowspan=2)

        self.heuristicOption = tk.StringVar()

        self.controls['heuclidean'] = tk.Radiobutton(self, variable=self.heuristicOption,
                                              text='Euclidean Heuristic', value='Euclidean Distance',
                                              bg='bisque', activebackground='bisque',
                                              command=eventHandler.onChoseHeuristicEuclidean)
        self.controls['heuclidean'].grid(row=0,column=6,pady=2,padx=2,sticky=tk.W)
        self.controls['hdiagonal'] = tk.Radiobutton(self, variable=self.heuristicOption,
                                             text='Diagonal Heuristic', value='Diagonal Distance',
                                             bg='bisque', activebackground='bisque',
                                                    command=eventHandler.onChoseHeuristicDiagonal)
        self.controls['hdiagonal'].grid(row=1, column=6, pady=2, padx=2, sticky=tk.W)
        self.controls['heuclidean'].select()


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
                if name == 'heuristic':
                    self.__setAvailability(isEnable, 'heuclidean')
                    self.__setAvailability(isEnable, 'hdiagonal')
                else:
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
        label = tk.Label(frame, text=labelText, background=self.bgColor, fg='blue', width=5)
        label.pack(side=tk.LEFT, fill=tk.BOTH)
        content = tk.Label(frame, textvariable=observer, background=self.bgColor, width=8, fg='red')
        content.pack(side=tk.LEFT, fill=tk.BOTH)

    def statusChangeCallback(self, node, heuristicValue):
        if node is None:
            strRow = ''
            strCol = ''
            strF = ''
            strG = ''
            strH = ''
        else:
            strRow = str(node.row)
            strCol = str(node.col)
            strF = '{0:.2f}'.format(round(node.F, 2))
            strG = '{0:.2f}'.format(round(node.G, 2))
            strH = '{0:.2f}'.format(round(heuristicValue, 2))

        self.textRow.set(strRow)
        self.textCol.set(strCol)
        self.textF.set(strF)
        self.textG.set(strG)
        self.textH.set(strH)

    def solutionChangeCallback(self, solution):
        if solution is None:
            self.textResult.set('')
        else:
            self.textResult.set(str(len(solution)))

class InfoFrame(tk.Frame):

    CANVAS_WIDTH = 100

    def __init__(self, master):
        self.bgColor = 'bisque'
        self.font = Font(size=8, weight="bold")
        tk.Frame.__init__(self, master, bg=self.bgColor)

        self.showNodeInfo()
        self.showStudentInfo()


    def showNodeInfo(self):
        nodeInfoFrame = tk.Frame(self, bg=self.bgColor)
        nodeInfoFrame.pack(side=tk.TOP, fill=tk.BOTH)
        self.createNodeInfo(nodeInfoFrame, 'Open', UINode.COLOR_OPEN, 0, 0)
        self.createNodeInfo(nodeInfoFrame, 'Close', UINode.COLOR_CLOSE, 1, 0)
        self.createNodeInfo(nodeInfoFrame, 'Solution', UINode.COLOR_SOLUTION, 2, 0)
        self.createNodeInfo(nodeInfoFrame, 'Start', UINode.COLOR_START, 3, 0)
        self.createNodeInfo(nodeInfoFrame, 'Goal', UINode.COLOR_GOAL, 4, 0)
        self.createNodeInfo(nodeInfoFrame, 'Obstacle', UINode.COLOR_OBSTACLE, 5, 0)
        self.createNodeInfo(nodeInfoFrame, 'Free', UINode.COLOR_NONE, 6, 0)

    def createNodeInfo(self, master, labelNode, colorNode, row, col):
        nodeInstance = tk.Frame(master, bg=colorNode, width=50, height=50)
        nodeInstance.grid(row=row, column=col, sticky=tk.NSEW, pady=10, padx=10)
        label = tk.Label(master, text=labelNode, bg=self.bgColor)
        label.grid(row=row, column=col+1, sticky=tk.NSEW, pady=10, padx=10)

    def showStudentInfo(self):
        studentInfoFrame = tk.Frame(self, bg=self.bgColor)
        studentInfoFrame.pack(side=tk.TOP, fill=tk.BOTH)
        self.createStudentInfo(studentInfoFrame, 'Ly Vinh Loi', '1612348', 'vinhloiit1327@gmail.com')
        self.createStudentInfo(studentInfoFrame, 'Nguyen Huu Truong', '1612756', 'ngoctruong9x.inc@gmail.com')
        pass

    def createStudentInfo(self, master, studentName, studentID, studentEmail):
        frame = tk.Frame(master, bg=self.bgColor)
        frame.pack(side=tk.TOP, pady=10, padx=10)

        labelName = tk.Label(frame, text=studentName, bg=self.bgColor, fg='blue', font=self.font)
        labelName.pack(side=tk.TOP)
        labelID = tk.Label(frame, text=studentID, bg=self.bgColor, fg='blue', font=self.font)
        labelID.pack(side=tk.TOP)
        labelEmail = tk.Label(frame, text=studentEmail, bg=self.bgColor, fg='blue', font=self.font)
        labelEmail.pack(side=tk.TOP)
        pass


class Application(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master, bg='bisque')

        self.toolbar = Toolbar(self, self)
        self.toolbar.grid(row=0, column=0, sticky=tk.NSEW)

        self.statusBar = StatusBar(self)
        self.statusBar.grid(row=1, column=0, sticky=tk.NSEW)

        self.infoFrame = InfoFrame(self)
        self.infoFrame.grid(row=0, column=1, rowspan=3, sticky=tk.NSEW)

        self.initDefault()

    def initDefault(self):
        self.currentHeuristic = HeuristicFunctions[self.toolbar.heuristicOption.get()]

        self.alg = UIAStarAlgorithm(self.currentHeuristic)

        self.map = UIEmptyMap(self)
        # self.map.canvas.pack(side=tk.TOP, fill=tk.BOTH)
        self.map.frame.grid(row=2, sticky=tk.NSEW)


    def on_step_button_click(self):
        self.alg.step()
        self.toolbar.setAvailability(True)
        self.toolbar.setAvailability(False, 'pause', 'stop', 'heuristic')

    def onChoseHeuristicEuclidean(self):
        self.onHeuristicOptionChange('Euclidean Distance')

    def onChoseHeuristicDiagonal(self):
        self.onHeuristicOptionChange('Diagonal Distance')

    def onHeuristicOptionChange(self, heuristic_name):
        self.currentHeuristic = HeuristicFunctions[heuristic_name]
        self.alg.setHeuristicFunction(self.currentHeuristic)

    def on_fast_forward_button_click(self):
        self.alg.fastForward()
        self.toolbar.setAvailability(False)
        self.toolbar.setAvailability(True, 'pause', 'stop')

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

    def changeMap(self, newMap):
        self.alg.reset()
        self.map.destroy()
        self.map = newMap
        self.map.draw()
        self.map.frame.grid(row=2, column=0, sticky=tk.NSEW)


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
