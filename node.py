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
        self.id = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.color = self.COLOR_DEFAULT

        self.canvas = None
        self.state = NodeState.NONE
        self.isSolution = False
        self.isStart = False
        self.isGoal = False
        self.isObstacle = False

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

        if self.isObstacle:
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

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col

    def isState(self, state):
        return self.state == state

    def setState(self, state):
        self.state = state
        self.update(self.canvas)

    def setSolution(self, isSolution):
        self.isSolution = isSolution
        self.update(self.canvas)

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


