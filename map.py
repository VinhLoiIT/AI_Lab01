import tkinter as tk
from node import Node

class Map:

    CANVAS_WIDTH = 600
    CANVAS_HEIGHT = 600
    MAX_GUI_SIZE = 100

    def __init__(self, master, isGUI):
        self.graph = []
        self.rows = 0
        self.cols = 0
        self.start = (0, 0)
        self.goal = (0, 0)
        if isGUI:
            self.canvas = tk.Canvas(master, width=self.CANVAS_WIDTH, height=self.CANVAS_HEIGHT, background='bisque')

    def loadFromFile(self, filepath):
        file = open(filepath, 'r')

        n = int(file.readline().split()[0])
        if hasattr(self, 'canvas') and not (1 <= n <= self.MAX_GUI_SIZE):
            raise IOError('Map size must in range 1 <= size <= {}'.format(self.MAX_GUI_SIZE))

        self.rows = n
        self.cols = n

        sx, sy = [int(x) for x in file.readline().split()]
        self.start = (sy, sx)

        gx, gy = [int(x) for x in file.readline().split()]
        self.goal = (gy, gx)

        data = [[int(x) for x in line.split()] for line in file]

        self.clear()
        for row in range(len(data)):
            rowNode = []
            for col in range(len(data[row])):
                node = self.createNode(row, col)
                node.isObstacle = (data[row][col] == 1)
                rowNode.append(node)
            self.graph.append(rowNode)

        self.graph[self.start[0]][self.start[1]].isStart = True
        self.graph[self.goal[0]][self.goal[1]].isGoal = True
        file.close()

    def createNode(self, row, col):
        self.nodeWidth = self.CANVAS_WIDTH / self.cols
        self.nodeHeight = self.CANVAS_HEIGHT / self.rows

        node = Node(row, col, self.nodeWidth, self.nodeHeight)
        return node

    def isValidPosition(self, row, col):
        return 0 <= row < self.rows and 0 <= col < self.cols

    def isObstacle(self, row, col):
        return self.graph[row][col].isObstacle

    def getVectorNeighborhood(self, pos):
        dis = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]
        n = []

        for i, j in dis:
            p = (pos[0] + i, pos[1] + j)
            if self.isValidPosition(p[0], p[1]):
                n.append(p)

        return n

    def draw(self):
        for row in range(self.rows):
            for col in range(self.cols):
                self.graph[row][col].draw(self.canvas)

    def clear(self):
        if hasattr(self, 'canvas'):
            self.canvas.delete(tk.ALL)
        self.graph = []

    def reset(self):
        for row in range(self.rows):
            for col in range(self.cols):
                self.graph[row][col].reset()

    def exportFile(self, file):
        if not file.closed:
            for row in range(self.rows):
                for col in range(self.cols):
                    self.graph[row][col].exportFile(file)
                    print(end=' ', file=file)
                print(file=file)


