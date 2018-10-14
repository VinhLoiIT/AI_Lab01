import math


# Tọa độ là (x,y): x: dòng ngang, y: cột dọc, khác với cách thể hiện đồ họa

def heuristic_euclidean(start, goal):
    return math.sqrt((start[0] - goal[0]) ** 2 + (start[1] - goal[1]) ** 2)


def heuristic_diagonal_distance(start, goal):
    return max(math.fabs(start[0] - goal[0]), math.fabs(start[1] - goal[1]))


class AStarAlgorithm():
    class Map:
        # Nhận tham số kiểu tuple
        # start = (row, col)
        def __init__(self, map):
            self.row, self.col, self.start, self.goal, self.graph = map

        def is_valid_position(self, pos):
            return (0 <= pos[0] < self.row and 0 <= pos[1] < self.col)

        def is_obstacle(self, position):
            return self.graph[position[0]][position[1]] == 1

        def is_start(self, position):
            return position == self.start

        def is_goal(self, position):
            return position == self.goal

        def getVecteNeighborhood(self, pos):
            dis = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]
            n = []

            for i, j in dis:
                p = (pos[0] + i, pos[1] + j)
                if self.is_valid_position(p):
                    n.append(p)

            return n

    def __init__(self, map, heureistic_function=heuristic_euclidean):
        self.map = self.Map(map)
        self.state = {}
        self.heuristic_function = heureistic_function

    def set_heuristic_function(self, func):
        self.heuristic_function = func

    def syncCode(self):
        state = self.state
        state['openSet'] = [self.map.start]
        state['closeSet'] = []
        state['cameFrom'] = {}
        state['gScore'] = {}
        state['fScore'] = {}
        return (state['openSet'], state['closeSet'], state['cameFrom'], state['gScore'], state['fScore'])

    # Trả về mảng vecter lưu những điểm lân cận của pos
    def findPath(self):

        state = self.state
        start = self.map.start
        goal = self.map.goal

        state['flagSolution'] = False
        openVertices, closeVertices, cameFrom, G, F = self.syncCode()
        G[start] = 0
        F[start] = self.heuristic_function(start, goal)

        yield state

        while len(openVertices) > 0:

            yield state
            current = None
            currentFscore = None
            for pos in openVertices:
                if current is None or F[pos] < currentFscore:
                    current = pos
                    currentFscore = F[pos]

            # Kiểm tra xem đã về đích chưa
            # Check if we have reached the goal
            if current == goal:
                state['flagSolution'] = True
                state['solution'] = [current]
                while current in cameFrom:
                    yield state
                    current = cameFrom[current]
                    state['solution'].append(current)
                state['solution'].reverse()
                print(len(state['solution']))

                return state['solution']  # Done!!!!!!!!!!!!!!!!!

            # Đánh dấu current bị đóng
            # Mark the current as closed
            openVertices.remove(current)
            closeVertices.append(current)

            # Cập nhật hàm G và F cho các đỉnh lân cận current
            # Update scores for vertices near the current position
            for neighbour in self.map.getVecteNeighborhood(current):
                if (not self.map.is_obstacle(neighbour) and neighbour not in closeVertices):
                    # move cost = 1

                    nG = G[current] + 1
                    if neighbour not in openVertices:
                        openVertices.append(neighbour)
                    elif nG >= G[neighbour]:
                        continue

                    cameFrom[neighbour] = current
                    G[neighbour] = nG
                    F[neighbour] = G[neighbour] + self.heuristic_function(neighbour, goal)

        return None
