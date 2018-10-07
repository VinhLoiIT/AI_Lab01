# This file contains 2 classes: Point and Map

class Point:
    """This class provide an easy way to compare and hold values x, y for each point on the map"""
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __str__(self):
        """Convert Point to String"""
        return '({0},{1})'.format(self.x, self.y)

    def __eq__(self, other):
        """Compare two Point objects"""
        return self.x == other.x and self.y == other.y


class Map:
    """This class holding all information of the map
    Attributes
    ----------
    row : integer
        Number of rows
    col : integer
        Number of columns
    start : Point
        Position of start
    goal : Point
        Position of goal
    matrix : list(list())
        The map data contains 1 if obstacle or 0 otherwise
    """
    def __init__(self, row, col, start, goal, matrix=None):
        self.row = row
        self.col = col
        self.start = start
        self.goal = goal
        self.data = matrix

    def __str__(self):
        """Print map to matrix 0 and 1
        For example:
            0 1 0 0 0
            0 0 0 0 1
            0 0 0 0 1
            0 0 0 0 0
            1 1 1 1 1
        """
        result = ''
        for row in self.data:
            for number in row:
                result = result + str(number) + ' '
            result = result + '\n'
        return result

    def index(self, position):
        """Indexing a position
        Parameters
        ----------
        position: Point
            Input position to calculate the index
            
        Returns
        -------
            Index of position in map
            For example:
            If the map is as below then the index matrix is:
                0 0 0 1 0         0  1  2  3  4
                1 0 1 1 1         5  6  7  8  9
                0 0 0 0 0    ->  10 11 12 13 14
                1 0 1 1 1        15 16 17 18 19
                0 1 0 0 0        20 21 22 23 24
            And the @position passed is (1,1) will return 6
        """
        return position.y * self.row + position.x

    def size(self, is_index):
        """Indexing a position
        Parameters
        ----------
        is_index: Boolean True/False
            Return the size in index or 2d (width, height)
            
        Returns
        -------
            if is_index is True:
                Return total index in map
            else
                Return Point(width, height):
                
            For example:
                If the map is as below then the index matrix is:
                    0 0 0 1 0         0  1  2  3  4
                    1 0 1 1 1         5  6  7  8  9
                    0 0 0 0 0    ->  10 11 12 13 14
                    1 0 1 1 1        15 16 17 18 19
                    0 1 0 0 0        20 21 22 23 24
                
                if is_index is True 
                    -> return 24
                else
                    -> return Point(5,5)
        """
        if is_index:
            return self.row * self.col
        return Point(self.col, self.row)

    def position(self, index):
        return Point(index % self.col, index // self.row)

    def is_valid_position(self, position):
        return (0 <= position.x < self.col) and (0 <= position.y < self.row)

    def is_obstacle(self, position):
        return self.data[position.y][position.x] == 1

    def is_start(self, position):
        return position == self.start

    def is_goal(self, position):
        return position == self.goal

    def neighbor(self, position):
        delta = [(-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0)]
        result = []
        for d in delta:
            neighbor = Point(position.x + d[0], position.y + d[1])
            if self.is_valid_position(neighbor):
                result.append(neighbor)
        return result
