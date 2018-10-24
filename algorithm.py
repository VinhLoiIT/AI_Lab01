# Tọa độ là (x,y): x: dòng ngang, y: cột dọc, khác với cách thể hiện đồ họa
import math
import functools

def heuristic_euclidean(start, goal):
    return math.sqrt((start.row - goal.row) ** 2 + (start.col - goal.col) ** 2)

def heuristic_diagonal_distance(start, goal):
    return max(math.fabs(start.row - goal.row), math.fabs(start.col - goal.col))


class AlgorithmState:
    INIT = 0
    RUN = 1
    TRACE_SOLUTION = 2
    DONE = 3

class Algorithm:

    infinity = 1000000
    HeuristicFunction = {
        'Euclidean Distance': heuristic_euclidean,
        'Diagonal Distance': heuristic_diagonal_distance
    }

    def __init__(self, map, heuristic_function=heuristic_euclidean):
        self.map = map
        self.state = AlgorithmState.INIT
        self.heuristic_function = heuristic_function
        self.openVertices = []
        self.solution = []
        self.closeVertices = []
        self.cameFrom = {}
        self.incons = []  # local inconsistency
        self.coeff = 1

        for rowNode in self.map.graph:
            for node in rowNode:
                node.G = self.infinity
                node.F = self.infinity


    def onUpdateMap(self):
        self.__AStarInit()

    def set_heuristic_function(self, func):
        self.heuristic_function = func

    def restart(self):
        self.reset()
        self.state = AlgorithmState.INIT

    def reset(self):
        while len(self.solution) != 0:
            self.solution[0].removeFromSolutionVertices(self.solution)
        while len(self.closeVertices) != 0:
            self.closeVertices[0].removeFromCloseVertices(self.closeVertices)
        while len(self.openVertices) != 0:
            self.openVertices[0].removeFromOpenVertices(self.openVertices)

    def AStarStateMachineStep(self):
        if self.state == AlgorithmState.INIT:
            self.__AStarInit()
        elif self.state == AlgorithmState.RUN:
            self.__AStarStep()
        elif self.state == AlgorithmState.TRACE_SOLUTION:
            self.solution = self.__traceSolution()
        elif self.state == AlgorithmState.DONE:
            pass
        return self.state

    def __fValueOfOpenVertices(self):
        if len(self.openVertices) == 0:
            return None
        current = self.openVertices[0]
        for u in self.openVertices:
            if current.F > u.F:
                current = u
        return current

    def __AStarInit(self):
        self.reset()
        self.cameFrom = {}
        self.incons = []  # local inconsistency

        for rowNode in self.map.graph:
            for node in rowNode:
                node.G = self.infinity
                node.F = self.infinity

        self.openVertices = []
        self.map.start.addToOpenVertices(self.openVertices)

        self.map.start.F = self.coeff * self.map.start.calcH(self.heuristic_function, self.map.goal)
        self.map.start.G = 0

        self.state = AlgorithmState.RUN


    def __AStarStep(self):

        if len(self.openVertices) == 0:
            self.state = AlgorithmState.DONE
            return

        self.current = self.__fValueOfOpenVertices()
        if not self.current:
            self.state = AlgorithmState.DONE
            return

        if self.map.goal.F > self.current.F:
            self.current.removeFromOpenVertices(self.openVertices)
            self.current.addToCloseVertices(self.closeVertices)

            neighbor = self.map.getVectorNeighborhood(self.current)
            for n in neighbor:
                if not n.isObstacle():
                    if n.G > self.current.G + 1:
                        n.G = self.current.G + 1
                        n.F = n.G + self.coeff * n.calcH(self.heuristic_function, self.map.goal)
                        n.setCameFrom(self.current)
                        if n not in self.closeVertices:
                            if n not in self.openVertices:
                                n.addToOpenVertices(self.openVertices)
                        else:
                            self.incons.append(n)

            # print(2)
            # print(self.openVertices)
            # self.current = self.__fValueOfOpenVertices()
            #
            # if self.current is None:
            #     self.state = AlgorithmState.TRACE_SOLUTION
        else:
            self.state = AlgorithmState.TRACE_SOLUTION

    def __traceSolution(self):
        result = []

        if self.map.goal.cameFrom is not None:
            self.map.goal.trace(result)
            result.reverse()

        if len(self.solution) == 0 or len(self.solution) > len(result):
            for x in self.solution:
                x.removeFromSolutionVertices(self.solution)

            for x in result:
                x.addToSolutionVertices(self.solution)

        self.state = AlgorithmState.DONE

        return result

    def __fastForwardGUI(self):
        if self.AStarStateMachineStep() != AlgorithmState.DONE:
            self.fast_forward_id = self.map.canvas.after(1, self.__fastForwardGUI)

    def __fastForwardNonGUI(self):
        while self.AStarStateMachineStep() != AlgorithmState.DONE:
            self.AStarStateMachineStep()

    def __ARAStarInit(self, e):
        self.coeff = e
        self.__AStarInit()
        print('Run ARAStar')

        self.map.start.F = e * self.map.start.calcH(self.heuristic_function, self.map.goal)

        # self.AStarOneShot(e)


    def ARAStar(self, e):
        if e > 1:
            self.__fastForwardGUI()
            self.state = AlgorithmState.RUN

            e = e - 0.5
            for x in self.incons:
                x.addToOpenVertices(self.openVertices)
            self.incons.clear()
            for u in self.openVertices:
                u.F = u.G + e * u.calcH(self.heuristic_function, self.map.goal)
            while len(self.closeVertices) != 0:
                self.closeVertices[0].removeFromCloseVertices(self.closeVertices)
            # self.AStarOneShot(e)
            # self.__fastForwardGUI()
            # self.state = AlgorithmState.RUN
        else:
            self.state = AlgorithmState.DONE
            self.map.canvas.after_cancel(self.fast_forward_id)
            del self.fast_forward_id
