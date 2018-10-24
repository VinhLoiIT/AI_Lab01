class NodeState:
    NONE = 0
    OPEN = 1
    CLOSE = 2


class Node:
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

    def __init__(self, row, col, width, height):
        # Graphics
        self.id = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.color = self.COLOR_DEFAULT
        self.canvas = None

        # Logic
        self.state = NodeState.NONE
        self.value = 0
        self.cameFrom = None
        self.isSolution = False
        self.isStart = False
        self.isGoal = False
        self._G = 0
        self._F = 0



    @property
    def G(self):
        return self._G

    @G.setter
    def G(self, value):
        self._G = value

    @property
    def F(self):
        return self._F

    @F.setter
    def F(self, value):
        self._F = value


    def update(self, canvas):
        """I was drawn, I have had index, so just update me"""
        if canvas:
            canvas.itemconfigure(self.id, fill=self._getColor())
        # self.canvas.update()
        pass

    def draw(self, canvas):
        """"Draw me on canvas"""
        if canvas:
            x0 = self.col * self.width
            y0 = self.row * self.height
            x1 = x0 + self.width
            y1 = y0 + self.height
            self.id = canvas.create_rectangle(x0, y0, x1, y1, fill=self._getColor())
            self.canvas = canvas

    def _getColor(self):
        color = self.COLOR_DEFAULT

        if self.isObstacle():
            color = Node.COLOR_OBSTACLE
        else:
            color = Node.COLOR_NONE

        if self.isStart:
            color = Node.COLOR_START
        elif self.isGoal:
            color = Node.COLOR_GOAL

        if self.state == NodeState.OPEN:
            color = Node.COLOR_OPEN
        elif self.state == NodeState.CLOSE:
            color = Node.COLOR_CLOSE

        if self.isSolution:
            color = Node.COLOR_SOLUTION

        return color

    def setCameFrom(self, nodeBeforeThisNode):
        self.cameFrom = nodeBeforeThisNode

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col

    def trace(self, resultList):
        resultList.append(self)
        if self.cameFrom is not None:
            self.cameFrom.trace(resultList)

    def isState(self, state):
        return self.state == state

    def isObstacle(self):
        return self.value == 1

    def addToOpenVertices(self, openVertices):
        openVertices.append(self)
        self.state = NodeState.OPEN
        self.update(self.canvas)

    def removeFromOpenVertices(self, openVertices):
        openVertices.remove(self)
        self.state = NodeState.NONE
        self.update(self.canvas)

    def addToCloseVertices(self, closeVertices):
        closeVertices.append(self)
        self.state = NodeState.CLOSE
        self.update(self.canvas)

    def removeFromCloseVertices(self, closeVertices):
        closeVertices.remove(self)
        self.state = NodeState.NONE
        self.update(self.canvas)

    def addToSolutionVertices(self, solutionVertices):
        solutionVertices.append(self)
        self.isSolution = True
        self.update(self.canvas)

    def removeFromSolutionVertices(self, solutionVertices):
        solutionVertices.remove(self)
        self.isSolution = False
        self.update(self.canvas)

    def calcH(self, hFunction, otherNode):
        return hFunction(self, otherNode)

    def reset(self):
        self.state = NodeState.NONE
        self.isSolution = False
        self.color = self.COLOR_DEFAULT

    def exportFile(self, file):
        if self.isStart:
            c = 'S'
        elif self.isGoal:
            c = 'G'
        elif self.isSolution:
            c = 'x'
        elif self.isObstacle:
            c = 'o'
        else:
            c = '-'
        print(c, file=file, end='')


