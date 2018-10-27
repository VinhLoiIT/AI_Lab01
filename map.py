import tkinter as tk
from node import Node, UINode


class Map:
    """This class is a logical map. Nothing to do with graphics here"""
    def __init__(self):
        self.graph = []
        self.rows = 0
        self.cols = 0
        self.start = None
        self.goal = None

    def isValidMapSize(self, totalRows, totalCols):
        return totalRows > 0 and totalCols > 0

    def isValidPosition(self, row, col):
        return 0 <= row < self.rows and 0 <= col < self.cols

    def isMapLoaded(self):
        return self.isValidMapSize(self.rows, self.cols)

    def loadFromFile(self, filepath):
        file = open(filepath, 'r')

        n = int(file.readline().split()[0])
        rows = n
        cols = n

        if not self.isValidMapSize(rows, cols):
            raise IOError('Invalid map size')

        sx, sy = [int(x) for x in file.readline().split()]
        startRow, startCol = sy, sx
        gx, gy = [int(x) for x in file.readline().split()]
        goalRow, goalCol = gy, gx
        graph = [[int(x) for x in line.split()] for line in file]

        file.close()

        self.__load(rows, cols, startRow, startCol, goalRow, goalCol, graph)

    def __load(self, rows, cols, startRow, startCol, goalRow, goalCol, graph):
        self.clear()
        self.rows = rows
        self.cols = cols
        for row in range(len(graph)):
            rowNode = []
            for col in range(len(graph[row])):
                node = self.createNode(row, col, rows, cols, graph[row][col])
                rowNode.append(node)
            if len(rowNode) != cols:
                raise IOError("Map data row {0} has {1} cols while number cols defined is {2}".format(row, len(rowNode), cols))
            self.graph.append(rowNode)
        if len(self.graph) != rows:
            raise IOError("Map data has {0} rows while number rows defined is {1}".format(len(self.graph), rows))

        self.rows = rows
        self.cols = cols
        self.start = self.graph[startRow][startCol]
        self.start.isStart = True
        self.goal = self.graph[goalRow][goalCol]
        self.goal.isGoal = True


    def getVectorNeighborhood(self, node):
        dis = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]
        n = []

        for i, j in dis:
            if self.isValidPosition(node.row + i, node.col + j):
                n.append(self.graph[node.row + i][node.col + j])

        return n

    def exportFile(self, file):
        if not file.closed:
            for row in range(self.rows):
                for col in range(self.cols):
                    self.graph[row][col].exportFile(file)
                    print(end=' ', file=file)
                print(file=file)

    def createNode(self, row, col, totalRows, totalCols, value):
        node = Node(row, col, value)
        return node

    def clear(self):
        self.graph = []

    def reset(self):
        for rowNode in self.graph:
            for node in rowNode:
                node.reset()


class UIMap(Map):
    """This class provide graphical user interface for Map"""
    CANVAS_WIDTH = 600
    CANVAS_HEIGHT = 600
    MAX_GUI_SIZE = 100

    def __init__(self, master):
        super().__init__()
        self.canvas = tk.Canvas(master, width=self.CANVAS_WIDTH, height=self.CANVAS_HEIGHT, background='bisque')
        self.canvas.bind('<Motion>', self.onMouseMove)
        self.callbackMouseMove = []

    def registerCallbackMouseMove(self, callback):
        self.callbackMouseMove.append(callback)

    def isValidMapSize(self, totalRows, totalCols):
        return 1 <= totalRows <= self.MAX_GUI_SIZE and 1 <= totalCols <= self.MAX_GUI_SIZE

    def draw(self):
        for rowNode in self.graph:
            for node in rowNode:
                node.draw(self.canvas)

    def createNode(self, row, col, totalRows, totalCols, value):
        self.nodeWidth = self.CANVAS_WIDTH / totalCols
        self.nodeHeight = self.CANVAS_HEIGHT / totalRows

        node = UINode(row, col, value, self.nodeWidth, self.nodeHeight)
        return node

    def clear(self):
        super().clear()
        self.canvas.delete(tk.ALL)

    def destroy(self):
        self.canvas.destroy()

    def onMouseMove(self, _):
        if self.isMapLoaded():
            nodeId = self.canvas.find_withtag(tk.CURRENT)
            coord = self.canvas.coords(nodeId)
            if len(coord) != 0:
                x = coord[0]
                y = coord[1]
                row = int(y / self.nodeWidth)
                col = int(x / self.nodeHeight)
                for callback in self.callbackMouseMove:
                    callback(self.graph[row][col])


class UIEmptyMap(UIMap):
    """This class provide graphical user interface for Empty Map"""

    def __init__(self, master):
        super().__init__(master)

    def isValidMapSize(self, totalRows, totalCols):
        return False

    def isMapLoaded(self):
        return False

    def draw(self):
        pass

    def createNode(self, row, col, totalRows, totalCols, value):
        pass

    def clear(self):
        pass

    def onMouseMove(self, _):
        pass



