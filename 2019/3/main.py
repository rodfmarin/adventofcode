import re


class Line:
    def __init__(self, board):
        self.x = 0
        self.y = 0
        self.board = board

    def move_up(self, steps):
        for step in range(1, steps + 1):
            self.y += 1
            self.board.store_step(self.x, self.y)

    def move_down(self, steps):
        for step in range(1, steps + 1):
            self.y -= 1
            self.board.store_step(self.x, self.y)

    def move_left(self, steps):
        for step in range(1, steps + 1):
            self.x -= 1
            self.board.store_step(self.x, self.y)

    def move_right(self, steps):
        for step in range(1, steps + 1):
            self.x += 1
            self.board.store_step(self.x, self.y)


class Board:
    def __init__(self):
        self.points = []

    def store_step(self, x, y):
        """
        Stores a step on the board given x, and y
        :param x: int
        :param y: int
        :return:
        """
        self.points.append([x, y])


def detect_collision(board1, board2):
    """
    Given two boards, find duplicate point sets
    :param board1:
    :param board2:
    :return:
    """
    for point in board1.points:
        if point in board2.points:
            print('collision found')
            print(point)
            print('distance')
            print(calculate_fewest_combined_steps(board1.points, board2.points, point))


DIRECTIONS = {
    "U": "move_up",
    "D": "move_down",
    "L": "move_left",
    "R": "move_right"
}


def read_input_file():
    with open('./input.txt') as file:
        return file.read()


def get_method(instruction):
    """

    :param instruction: is like R991 or D123 or L34 or U2
    :return:
    """
    direction = re.findall('^[A-Z]', instruction)[0]
    step_count = re.findall('[0-9]+', instruction)[0]
    the_method = f".{DIRECTIONS[direction]}({step_count})"
    return the_method

def calculate_fewest_combined_steps(set1, set2, point_set):
    """
    Calculates steps from 'point_set' back to origin + 1
    for both set1 and set2
    :param set1:
    :param set2:
    :param point_set:
    :return:
    """
    # set1 = [[1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [7, 0], [8, 0], [8, 1], [8, 2], [8, 3], [8, 4], [8, 5], [7, 5], [6, 5], [5, 5], [4, 5], [3, 5], [3, 4], [3, 3], [3, 2]]
    # set2 = [[0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7], [1, 7], [2, 7], [3, 7], [4, 7], [5, 7], [6, 7], [6, 6], [6, 5], [6, 4], [6, 3], [5, 3], [4, 3], [3, 3], [2, 3]]
    # point_set = [3, 3]

    i = 1
    for set in set1:
        if set == point_set:
            break
        i += 1
    set1_distance = i

    j = 1
    for set in set2:
        if set == point_set:
            break
        j += 1
    set2_distance = j

    return set1_distance + set2_distance



def main():
    """
    Testing Ideas
    """
    lines = read_input_file().splitlines()
    l1_input = lines[0].split(',')
    l2_input = lines[1].split(',')

    line1_board = Board()
    line1 = Line(line1_board)
    for step in l1_input:
        method = get_method(step)
        eval(f"line1{method}")

    line2_board = Board()
    line2 = Line(line2_board)
    for step in l2_input:
        method = get_method(step)
        eval(f"line2{method}")

    print(line1_board.points)
    print(line2_board.points)
    detect_collision(line1_board, line2_board)


main()

"""
...........
.+-----+...
.|.....|...
.|..+--X-+.
.|..|..|.|.
.|.-X--+.|.
.|..|....|.
.|.......|.
.o-------+.
...........
"""