import tkinter as tk
from tkinter import filedialog
from AStarAlgorithm import AStarAlgorithm
from util import Map
from util import Point


class Application(tk.Frame):

    COLOR_SOLUTION = '#0000FF'
    COLOR_CLOSESET = '#470a0a'
    COLOR_OPENSET  = '#0e592e'
    COLOR_START    = '#0e5159'
    COLOR_GOAL     = '#00FF00'
    COLOR_OBSTACLE = '#000000'
    COLOR_NONE     = '#414949'
    
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack()

        self.frame_toolbar = tk.Frame(self)
        self.frame_toolbar.grid(row=0, column=0)
        self.frame_map = tk.Frame(self)
        self.frame_map.grid(row=1, column=0)
        self.frame_info = tk.Frame(self)
        self.frame_info.grid(row=0, column=1, rowspan=2)

        # declare member variables
        self.alg = None
        self.is_started = False
        self.current_state = None
        self.current_state_iter = None

        self.init_frame_toolbar()
        self.init_frame_map()
        self.init_frame_info()

    def init_frame_toolbar(self):
        button_load_map = tk.Button(self.frame_toolbar, text='Load map')
        button_load_map['command'] = self.on_button_load_map_click
        button_load_map.grid(row=0, column=0)

        button_step = tk.Button(self.frame_toolbar, text='Step')
        button_step['command'] = self.on_button_step_click
        button_step.grid(row=0, column=1)

        button_fast_forward = tk.Button(self.frame_toolbar, text='Fast forward')
        button_fast_forward['command'] = self.on_button_fast_forward_click
        button_fast_forward.grid(row=0, column=2)

        button_restart = tk.Button(self.frame_toolbar, text='Restart')
        button_restart['command'] = self.on_button_restart_click
        button_restart.grid(row=0, column=3)

        self.frame_toolbar.button_load_map = button_load_map
        self.frame_toolbar.button_step = button_step
        self.frame_toolbar.button_fast_forward = button_fast_forward
        self.frame_toolbar.button_restart = button_restart

    def init_frame_map(self):
        pass

    def init_frame_info(self):
        list_box = tk.Listbox(self.frame_info)
        list_box.grid(row=0, column=0, sticky='N')
        list_box.rowconfigure(0, weight=1)
        list_box.columnconfigure(0, weight=1)
        self.frame_info.instance = list_box

    def on_button_load_map_click(self):
        file_name = filedialog.askopenfilename(initialdir='./',
                                              title='Select file',
                                              filetypes=(
                                                  ("txt files", "*.txt"),
                                                  ("all files", "*.*")
                                              ))
        if file_name:
            self.alg = AStarAlgorithm(self.load_map_from_file(file_name))
            self.restart()

    def on_button_restart_click(self):
        self.restart()

    def display_alg_step(self):
        self.current_state = self.current_state_iter.__next__()
        self.updateStepAlgorithm(self.current_state)

    def fast_forward_alg(self):
        try:
            self.display_alg_step()
            self.after(50, self.fast_forward_alg)
        except StopIteration:
            print('Done')

    def on_button_fast_forward_click(self):
        if not self.is_started:
            self.start()
        else:
            self.fast_forward_alg()

    def on_button_step_click(self):
        if not self.is_started:
            self.start()
        else:
            try:
                self.display_alg_step()
            except StopIteration as e:
                print('Done')

    def load_map_from_file(self, file_path):
        file = open(file_path, 'r')

        n = int(file.readline().split()[0])
        sx, sy = [int(x) for x in file.readline().split()]
        start = Point(sx, sy)

        gx, gy = [int(x) for x in file.readline().split()]
        goal = Point(gx, gy)

        matrix = [[int(x) for x in line.split()] for line in file]
        file.close()
        return Map(n, n, start, goal, matrix)

    def display_map(self):
        self.frame_map.instance = []
        for x in range(self.alg.map.col):
            row = []
            for y in range(self.alg.map.row):
                button = tk.Button(self.frame_map)
                if self.alg.map.is_obstacle(Point(x, y)):
                    color = self.COLOR_OBSTACLE
                else:
                    color = self.COLOR_NONE
                button['bg'] = color
                button['bd'] = 3
                button['width'] = 2
                button['height'] = 1
                button['state'] = tk.DISABLED
                button.grid(row=y, column=x)

                button.bind("<Enter>", self.on_mouse_enter_button)
                button.bind("<Leave>", self.on_mouse_leave_button)
                button.position = Point(x, y)
                row.append(button)
            self.frame_map.instance.append(row)
        self.frame_map.instance[self.alg.map.start.x][self.alg.map.start.y]['bg'] = self.COLOR_START
        self.frame_map.instance[self.alg.map.goal.x][self.alg.map.goal.y]['bg'] = self.COLOR_GOAL

    def start(self):
        self.current_state_iter = self.alg.solve()
        self.is_started = True

    def restart(self):
        self.is_started = False
        self.current_state_iter = self.alg.solve()
        self.current_state = None
        # TODO: cancel after() if click restart while fast_forward
        self.display_map()

    def isInSet(self, position, _set):
        for p in _set:
            position_index = self.alg.map.index(position)
            if position_index == p:
                return True
        return False
        
    def updateStepAlgorithm(self, alg_state):
        for row in self.frame_map.instance:
            for button in row:
                button_point = Point(button.position.x, button.position.y)

                if alg_state['flagSolution'] and self.isInSet(button_point, alg_state['solution']):
                    button['bg'] = self.COLOR_SOLUTION
                elif self.isInSet(button_point, alg_state['openSet']):
                    button['bg'] = self.COLOR_OPENSET
                elif self.isInSet(button_point, alg_state['closeSet']):
                    button['bg'] = self.COLOR_CLOSESET
                elif self.alg.map.is_obstacle(button_point):
                    button['bg'] = self.COLOR_OBSTACLE
                elif self.alg.map.is_start(button_point):
                    button['bg'] = self.COLOR_START
                elif self.alg.map.is_goal(button_point):
                    button['bg'] = self.COLOR_GOAL
                else:
                    button['bg'] = self.COLOR_NONE

    def on_mouse_enter_button(self, event):
        button = event.widget
        self.frame_info.instance.insert(1, 'x = {0}'.format(button.position.x))
        self.frame_info.instance.insert(2, 'y = {0}'.format(button.position.y))
        if self.current_state:
            position_index = self.alg.map.index(button.position)
            g_score = self.current_state['gScore'][position_index]
            self.frame_info.instance.insert(3, 'g_score = {0}'.format(g_score))
            h_score = self.alg.heuristic_function(button.position, self.alg.map.goal, self.alg.map)
            self.frame_info.instance.insert(4, 'h_score = {0}'.format(h_score))
            f_score = g_score + h_score
            self.frame_info.instance.insert(5, 'f_score = {0}'.format(f_score))

    def on_mouse_leave_button(self, event):
        del event
        self.frame_info.instance.delete(0, tk.END)


root = tk.Tk()
app = Application(master=root)
app.mainloop()
