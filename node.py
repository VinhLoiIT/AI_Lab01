class NodeState:
    NONE = 0
    OPEN = 1
    CLOSE = 2


class Node:
    """This class provide logical structure of a node"""

    def __init__(self, row: int, col: int, value: int):
        self.row = row
        self.col = col
        self.state = NodeState.NONE
        self.value = value
        self.cameFrom = None
        self.isSolution = False
        self.isStart = False
        self.isGoal = False
        self.G = 0
        self.F = 0

    def setCameFrom(self, nodeBeforeThisNode):
        self.cameFrom = nodeBeforeThisNode

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col

    def trace(self, resultList):
        resultList.append(self)
        if self.cameFrom is not None:
            self.cameFrom.trace(resultList)

    def isObstacle(self):
        return self.value == 1

    def addToOpenVertices(self, openVertices):
        """Tell, don't ask rule: Let me self-adding to the list!"""
        openVertices.append(self)
        self.state = NodeState.OPEN

    def removeFromOpenVertices(self, openVertices):
        """Tell, don't ask rule: Let me self-removing from the list!"""
        openVertices.remove(self)
        self.state = NodeState.NONE

    def addToCloseVertices(self, closeVertices):
        """Tell, don't ask rule: Let me self-adding to the list!"""
        closeVertices.append(self)
        self.state = NodeState.CLOSE

    def removeFromCloseVertices(self, closeVertices):
        """Tell, don't ask rule: Let me self-removing from the list!"""
        closeVertices.remove(self)
        self.state = NodeState.NONE

    def addToSolutionVertices(self, solutionVertices):
        """Tell, don't ask rule: Let me self-adding to the list!"""
        solutionVertices.append(self)
        self.isSolution = True

    def removeFromSolutionVertices(self, solutionVertices):
        """Tell, don't ask rule: Let me self-removing from the list!"""
        solutionVertices.remove(self)
        self.isSolution = False

    def calcH(self, hFunction, otherNode):
        """Tell, don't ask rule: Let me calculate heuristic value by myself"""
        return hFunction(self, otherNode)

    def reset(self):
        self.state = NodeState.NONE
        self.isSolution = False

    def exportFile(self, file):
        """Tell, don't ask rule: Gimme an opened file, I will write myself"""
        if self.isStart:
            c = 'S'
        elif self.isGoal:
            c = 'G'
        elif self.isSolution:
            c = 'x'
        elif self.isObstacle():
            c = 'o'
        else:
            c = '-'
        print(c, file=file, end='')


class UINode(Node):
    """This class provide graphical user interface of a node"""
    COLOR_SOLUTION = '#12FF10'  # Green
    COLOR_CLOSE = '#970E0E'  # Dark Red
    COLOR_OPEN = '#F6EC48'  # Yellow
    COLOR_START = '#0904FF'  # Blue
    COLOR_GOAL = '#FF070A'  # Red
    COLOR_OBSTACLE = '#726E69'  # Gray
    COLOR_NONE = '#000000'  # Black
    COLOR_DEFAULT = '#8e4216'  # Orange

    PADX = 1
    PADY = 1

    def __init__(self, row, col, value, width, height):
        super().__init__(row, col, value)
        self.width = width
        self.height = height
        self.color = self.COLOR_DEFAULT
        self.canvas = None
        self.id = -1

    def draw(self, canvas):
        """"Draw me on canvas"""
        if canvas:
            x0 = self.col * self.width
            y0 = self.row * self.height
            x1 = x0 + self.width
            y1 = y0 + self.height
            self.canvas = canvas
            self.id = canvas.create_rectangle(x0, y0, x1, y1, fill=self._getColor())

    def update(self):
        """I was drawn, I have had an id, so just update me"""
        self.canvas.itemconfigure(self.id, fill=self._getColor())

    def reset(self):
        super().reset()
        self.color = self.COLOR_DEFAULT
        self.F = 0
        self.G = 0
        self.update()

    def addToOpenVertices(self, openVertices):
        super().addToOpenVertices(openVertices)
        self.update()

    def removeFromOpenVertices(self, openVertices):
        super().removeFromOpenVertices(openVertices)
        self.update()

    def addToCloseVertices(self, closeVertices):
        super().addToCloseVertices(closeVertices)
        self.update()

    def removeFromCloseVertices(self, closeVertices):
        super().removeFromCloseVertices(closeVertices)
        self.update()

    def addToSolutionVertices(self, solutionVertices):
        super().addToSolutionVertices(solutionVertices)
        self.update()

    def removeFromSolutionVertices(self, solutionVertices):
        super().removeFromSolutionVertices(solutionVertices)
        self.update()

    def _getColor(self):

        if self.isObstacle():
            color = self.COLOR_OBSTACLE
        else:
            color = self.COLOR_NONE

        if self.isStart:
            color = self.COLOR_START
        elif self.isGoal:
            color = self.COLOR_GOAL

        if self.state == NodeState.OPEN:
            color = self.COLOR_OPEN
        elif self.state == NodeState.CLOSE:
            color = self.COLOR_CLOSE

        if self.isSolution:
            color = self.COLOR_SOLUTION

        return color

