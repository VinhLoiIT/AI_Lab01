import tkinter as tk
# Tọa độ là (x,y): x: dòng ngang, y: cột dọc, khác với cách thể hiện đồ họa
import math
from node import NodeState

def heuristic_euclidean(start, goal):
    return math.sqrt((start[0] - goal[0]) ** 2 + (start[1] - goal[1]) ** 2)

def heuristic_diagonal_distance(start, goal):
    return max(math.fabs(start[0] - goal[0]), math.fabs(start[1] - goal[1]))

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
        self.G = [[self.infinity for row in range(self.map.rows)] for col in range(self.map.cols)]
        self.F = [[self.infinity for row in range(self.map.rows)] for col in range(self.map.cols)]

    def onUpdateMap(self):
        self.__AStarInit(1)

    def set_heuristic_function(self, func):
        self.heuristic_function = func

    def restart(self):
        self.reset()
        self.state = AlgorithmState.INIT

    def reset(self):
        self.__clearSolution()
        self.__clearCloseVertices()
        self.__clearOpenVertices()

    def AStarStateMachineStep(self, e):
        if self.state == AlgorithmState.INIT:
            self.__AStarInit(e)
        elif self.state == AlgorithmState.RUN:
            self.__AStarStep(e)
        elif self.state == AlgorithmState.TRACE_SOLUTION:
            self.solution = self.__traceSolution()
        elif self.state == AlgorithmState.DONE:
            pass
        return self.state

    def __appendOpenVertices(self, pos):
        self.openVertices.append(pos)
        self.map.graph[pos[0]][pos[1]].setState(NodeState.OPEN)

    def __removeOpenVertices(self, pos):
        self.openVertices.remove(pos)
        self.map.graph[pos[0]][pos[1]].setState(NodeState.NONE)

    def __clearOpenVertices(self):
        for x in self.openVertices:
            self.map.graph[x[0]][x[1]].setState(NodeState.NONE)
        self.openVertices.clear()

    def __appendCloseVertices(self, pos):
        self.closeVertices.append(pos)
        self.map.graph[pos[0]][pos[1]].setState(NodeState.CLOSE)

    def __removeCloseVertices(self, pos):
        self.closeVertices.remove(pos)
        self.map.graph[pos[0]][pos[1]].setState(NodeState.NONE)

    def __clearCloseVertices(self):
        for x in self.closeVertices:
            self.map.graph[x[0]][x[1]].setState(NodeState.NONE)
        self.closeVertices.clear()

    def __appendSolution(self, solution, pos):
        solution.append(pos)
        self.map.graph[pos[0]][pos[1]].setSolution(True)

    def __removeSolution(self, pos):
        self.solution.remove(pos)
        self.map.graph[pos[0]][pos[1]].setSolution(False)

    def __clearSolution(self):
        for x in self.solution:
            self.map.graph[x[0]][x[1]].setSolution(False)
        self.solution.clear()

    def __fValueOfOpenVertices(self):
        if len(self.openVertices) == 0:
            return None
        current = self.openVertices[0]
        for u in self.openVertices:
            if self.F[current[0]][current[1]] > self.F[u[0]][u[1]]:
                current = u
        return current



    def __AStarInit(self, e):
        self.reset()
        self.cameFrom = {}
        self.incons = []  # local inconsistency
        G = self.G = [[self.infinity for row in range(self.map.rows)] for col in range(self.map.cols)]
        F = self.F = [[self.infinity for row in range(self.map.rows)] for col in range(self.map.cols)]

        self.__appendOpenVertices(self.map.start)

        s = self.map.start
        g = self.map.goal
        F[s[0]][s[1]] = e * self.heuristic_function(s, g)
        G[s[0]][s[1]] = 0

        self.state = AlgorithmState.RUN

    def __AStarStep(self, e):
        F = self.F
        G = self.G
        g = self.map.goal

        if len(self.openVertices) == 0:
            self.state = AlgorithmState.DONE
            return

        self.current = self.__fValueOfOpenVertices()
        if not self.current:
            self.state = AlgorithmState.DONE
            return

        if F[g[0]][g[1]] > F[self.current[0]][self.current[1]]:

            self.__removeOpenVertices(self.current)
            self.__appendCloseVertices(self.current)

            for n in self.map.getVectorNeighborhood(self.current):
                if not self.map.isObstacle(n[0], n[1]):
                    if G[n[0]][n[1]] > G[self.current[0]][self.current[1]] + 1:
                        G[n[0]][n[1]] = G[self.current[0]][self.current[1]] + 1
                        F[n[0]][n[1]] = G[n[0]][n[1]] + e * self.heuristic_function(n, g)
                        self.cameFrom[n] = self.current
                        if n not in self.closeVertices:
                            if n not in self.openVertices:
                                self.__appendOpenVertices(n)
                        else:
                            self.incons.append(n)
            self.current = self.__fValueOfOpenVertices()
            if self.current == None:
                self.state = AlgorithmState.TRACE_SOLUTION
        else:
            self.state = AlgorithmState.TRACE_SOLUTION

    def __traceSolution(self):
        result = []
        if self.map.goal in self.cameFrom:
            x = self.map.goal
            result.append(x)
            while x in self.cameFrom:
                x = self.cameFrom[x]
                result.append(x)
            result.reverse()

        if len(self.solution) == 0 or len(self.solution) > len(result):
            # self.solution = result
            self.__clearSolution()
            for x in result:
                self.__appendSolution(self.solution, x)

            # print(self.solution)

        self.state = AlgorithmState.DONE

        return result

    def AStarOneShot(self, e):
        while self.AStarStateMachineStep(e) != AlgorithmState.DONE:
            self.AStarStateMachineStep(e)

    def ARAStar(self, e):
        self.__AStarInit(e)
        print('Run ARAStar')
        s = self.map.start
        g = self.map.goal

        self.F[s[0]][s[1]] = e * self.heuristic_function(s, g)

        self.AStarOneShot(e)
        self.state = AlgorithmState.RUN

        # while not stopFlag.is_set():
        #     if e > 1:
        #         e = e - 0.5
        #         for x in self.incons:
        #             self.__appendOpenVertices(x)
        #         self.incons.clear()
        #         for u in self.openVertices:
        #             self.F[u[0]][u[1]] = self.G[u[0]][u[1]] + e * self.heuristic_function(u, g)
        #         self.__clearCloseVertices()
        #         self.AStarOneShot(e)
        #         self.state = AlgorithmState.RUN
        #     else:
        #         stopFlag.wait()
        while e > 1:
            e = e - 0.5
            for x in self.incons:
                self.__appendOpenVertices(x)
            self.incons.clear()
            for u in self.openVertices:
                self.F[u[0]][u[1]] = self.G[u[0]][u[1]] + e * self.heuristic_function(u, g)
            self.__clearCloseVertices()
            self.AStarOneShot(e)
            self.state = AlgorithmState.RUN

        self.state = AlgorithmState.DONE
