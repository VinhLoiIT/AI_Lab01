import tkinter as tk
from node import Node

class Map:

    CANVAS_WIDTH = 600
    CANVAS_HEIGHT = 600

    def __init__(self, master):
        self.graph = []
        self.rows = 0
        self.cols = 0
        self.start = (0, 0)
        self.goal = (0, 0)
        self.canvas = tk.Canvas(master)
        # self.canvas.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def loadFromFile(self, filepath):
        file = open(filepath, 'r')

        n = int(file.readline().split()[0])
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
        nodeWidth = self.CANVAS_WIDTH // self.cols
        nodeHeight = self.CANVAS_HEIGHT // self.rows

        node = Node(row, col, nodeWidth, nodeHeight)
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


