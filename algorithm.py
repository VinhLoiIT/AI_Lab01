# Tọa độ là (x,y): x: dòng ngang, y: cột dọc, khác với cách thể hiện đồ họa
import math
from map import Map, UIMap
import threading

def heuristic_euclidean(start, goal):
    return math.sqrt((start.row - goal.row) ** 2 + (start.col - goal.col) ** 2)


def heuristic_diagonal_distance(start, goal):
    return max(math.fabs(start.row - goal.row), math.fabs(start.col - goal.col))


HeuristicFunction = {
        'Euclidean Distance': heuristic_euclidean,
        'Diagonal Distance': heuristic_diagonal_distance
}


class AlgorithmState:
    INIT = 0
    RUN = 1
    TRACE_SOLUTION = 2
    DONE = 3


class StateMachine:

    def __init__(self):
        self.state = AlgorithmState.INIT

    def stateInit(self):
        pass

    def stateStep(self):
        pass

    def stateTrace(self):
        pass

    def stateDone(self):
        pass

    def step(self):
        if self.state == AlgorithmState.INIT:
            self.stateInit()
        elif self.state == AlgorithmState.RUN:
            self.stateStep()
        elif self.state == AlgorithmState.TRACE_SOLUTION:
            self.stateTrace()
        elif self.state == AlgorithmState.DONE:
            self.stateDone()
        else:
            raise RuntimeError('Invalid State')

    def setState(self, state):
        self.state = state

    def run(self):
        while self.state != AlgorithmState.DONE:
            self.state = self.step()


class AStarAlgorithm(StateMachine):

    infinity = 1000000

    def __init__(self, map: Map, heuristic_function=heuristic_euclidean):
        super().__init__()
        self.map = map
        self.state = AlgorithmState.INIT
        self.heuristicFunction = heuristic_function
        self.openVertices = []
        self.solution = []
        self.closeVertices = []
        self.cameFrom = {}
        self.incons = []  # local inconsistency
        self.coeff = 1

    def clearSolution(self):
        while len(self.solution) != 0:
            self.solution[0].removeFromSolutionVertices(self.solution)

    def clearCloseVertices(self):
        while len(self.closeVertices) != 0:
            self.closeVertices[0].removeFromCloseVertices(self.closeVertices)

    def clearOpenVertices(self):
        while len(self.openVertices) != 0:
            self.openVertices[0].removeFromOpenVertices(self.openVertices)

    def reset(self):
        self.clearOpenVertices()
        self.clearCloseVertices()
        self.clearSolution()
        self.state = AlgorithmState.INIT

    def setCoeff(self, coeff):
        self.coeff = coeff

    def setHeuristicFunction(self, func):
        self.heuristicFunction = func

    def run(self):
        while self.state != AlgorithmState.DONE:
            self.step()

    def stateInit(self):
        super().stateInit()
        while len(self.solution) != 0:
            self.solution[0].removeFromSolutionVertices(self.solution)
        while len(self.closeVertices) != 0:
            self.closeVertices[0].removeFromCloseVertices(self.closeVertices)
        while len(self.openVertices) != 0:
            self.openVertices[0].removeFromOpenVertices(self.openVertices)

        self.cameFrom = {}
        self.incons = []  # local inconsistency

        for rowNode in self.map.graph:
            for node in rowNode:
                node.G = self.infinity
                node.F = self.infinity

        self.map.start.addToOpenVertices(self.openVertices)

        self.map.start.F = self.coeff * self.map.start.calcH(self.heuristicFunction, self.map.goal)
        self.map.start.G = 0

        self.setState(AlgorithmState.RUN)

    def stateStep(self):
        super().stateStep()

        current = self.__fValueOfOpenVertices()
        if current is None:
            self.setState(AlgorithmState.TRACE_SOLUTION)
            return

        if self.map.goal.F > current.F:
            current.removeFromOpenVertices(self.openVertices)
            current.addToCloseVertices(self.closeVertices)

            neighbor = self.map.getVectorNeighborhood(current)
            for n in neighbor:
                if not n.isObstacle():
                    if n.G > current.G + 1:
                        n.G = current.G + 1
                        n.F = n.G + self.coeff * n.calcH(self.heuristicFunction, self.map.goal)
                        n.setCameFrom(current)
                        if n not in self.closeVertices:
                            if n not in self.openVertices:
                                n.addToOpenVertices(self.openVertices)
                        else:
                            self.incons.append(n)
        else:
            self.setState(AlgorithmState.TRACE_SOLUTION)
            return


    def stateTrace(self):
        super().stateTrace()

        result = []

        if self.map.goal.cameFrom is not None:
            self.map.goal.trace(result)
            result.reverse()

        if len(self.solution) == 0 or len(self.solution) > len(result):
            for x in self.solution:
                x.removeFromSolutionVertices(self.solution)

            for x in result:
                x.addToSolutionVertices(self.solution)

        self.setState(AlgorithmState.DONE)

    def stateDone(self):
        super().stateDone()
        print('Done')

    def __fValueOfOpenVertices(self):
        if len(self.openVertices) == 0:
            return None
        current = self.openVertices[0]
        for u in self.openVertices:
            if current.F > u.F:
                current = u
        return current

    def getSolution(self):
        return self.solution


class UIAStarAlgorithm(AStarAlgorithm):

    def __init__(self, map: UIMap, heuristic_function=heuristic_euclidean):
        super().__init__(map, heuristic_function)

    def __cancelFastForward(self):
        if hasattr(self, 'fast_forward_cb_id'):
            self.map.canvas.after_cancel(self.fast_forward_cb_id)
            del self.fast_forward_cb_id

    def reset(self):
        super().reset()
        self.__cancelFastForward()

    def run(self):
        if self.state != AlgorithmState.DONE:
            super().step()
            self.fast_forward_cb_id = self.map.canvas.after(1, self.run)

    def fastForward(self):
        if not hasattr(self, 'fast_forward_cb_id'):
            self.run()

    def pause(self):
        self.__cancelFastForward()


class ARAAlgorithm(AStarAlgorithm):

    def __init__(self, map, heuristic_function=HeuristicFunction['Euclidean Distance']):
        super().__init__(map, heuristic_function)

    def run(self):
        while self.coeff > 1:
            super().run()
            self.state = AlgorithmState.RUN

            self.coeff = self.coeff - 0.5
            for x in self.incons:
                x.addToOpenVertices(self.openVertices)
            self.incons.clear()
            for u in self.openVertices:
                u.F = u.G + self.coeff * u.calcH(self.heuristicFunction, self.map.goal)
            while len(self.closeVertices) != 0:
                self.closeVertices[0].removeFromCloseVertices(self.closeVertices)
            self.run()
            self.state = AlgorithmState.RUN


class UIARAAlgorithm(UIAStarAlgorithm):

    def __init__(self, map: UIMap, heuristic_function=heuristic_euclidean):
        super().__init__(map, heuristic_function)

    def fastForward(self):
        if not hasattr(self, 'fast_forward_cb_id'):
            araThread = threading.Thread(target=self.run)
            araThread.daemon = True
            araThread.start()
            araThread.join(self.time)

    def setTimeLimit(self, time):
        self.time = time

    def run(self):
        if self.state != AlgorithmState.DONE:
            super().run()
        elif self.coeff > 1:
            self.coeff = self.coeff - 0.5

            for x in self.incons:
                x.addToOpenVertices(self.openVertices)
            self.incons.clear()
            for u in self.openVertices:
                u.F = u.G + self.coeff * u.calcH(self.heuristicFunction, self.map.goal)
            while len(self.closeVertices) != 0:
                self.closeVertices[0].removeFromCloseVertices(self.closeVertices)

            self.setState(AlgorithmState.RUN)



