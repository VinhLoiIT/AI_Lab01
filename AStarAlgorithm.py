import math
from util import Map


def heuristic_euclidean(position, goal, input_map):
    del input_map  # not used, but net for prototyping
    return math.sqrt((position.x - goal.x)**2 + (position.y - goal.y)**2)


class AStarAlgorithm:
    INFINITY = 2000000

    def __init__(self, input_map, heuristic_function=heuristic_euclidean):
        if not isinstance(input_map, Map):
            raise TypeError
        
        self.map = input_map
        self.state = {}
        self.heuristic_function = heuristic_function

    def set_heuristic_function(self, func):
        self.heuristic_function = func

    def trace(self, previous):
        solution = []
        if self.state['flagSolution']:
            x = self.map.index(self.map.goal)
            solution.insert(0, x)
            while x != self.map.index(self.map.start):
                x = previous[x]
                solution.insert(0, x)
                yield solution
        return solution

    @staticmethod
    def get_min_cost(score, _set):
        cost_list = [score[x] for x in _set]
        return _set[cost_list.index(min(cost_list))]

    def solve(self):
        state = self.state
        state['openSet'] = [self.map.index(self.map.start)]
        state['closeSet'] = []
        state['solution'] = []
        state['cameFrom'] = {}
        state['gScore'] = [AStarAlgorithm.INFINITY] * self.map.size(True)
        state['fScore'] = list(state['gScore'])
        start_index = self.map.index(self.map.start)
        state['gScore'][start_index] = 0
        state['fScore'][start_index] = self.heuristic_function(self.map.start, self.map.goal, self.map)
        state['flagSolution'] = False

        open_set = state['openSet']
        close_set = state['closeSet']
        yield state

        while len(open_set) != 0:
            index_current = AStarAlgorithm.get_min_cost(state['fScore'], open_set)
            yield state
            
            if index_current == self.map.index(self.map.goal):
                self.state['flagSolution'] = True
                break

            open_set.remove(index_current)
            yield state
            close_set.append(index_current)
            yield state
            
            for neighbor in self.map.neighbor(self.map.position(index_current)):
                index_neighbor = self.map.index(neighbor)

                if self.map.is_obstacle(neighbor):
                    continue

                if index_neighbor in close_set:
                    continue

                score_tentative = self.state['gScore'][index_current] + 1  # 1 = current to neighbor

                if index_neighbor not in self.state['openSet']:
                    open_set.append(index_neighbor)
                    yield state
                elif score_tentative >= self.state['gScore'][index_neighbor]:
                    continue

                self.state['cameFrom'][index_neighbor] = index_current
                self.state['gScore'][index_neighbor] = score_tentative
                self.state['fScore'][index_neighbor] = self.state['gScore'][index_neighbor] +\
                                                       self.heuristic_function(neighbor, self.map.goal, self.map)
                yield state

        if self.state['flagSolution']:
            trace_generator = self.trace(state['cameFrom'])
            try:
                while True:
                    state['solution'] = trace_generator.__next__()
                    yield state
            except StopIteration:
                pass

        return state['solution']

