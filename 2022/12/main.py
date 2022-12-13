"""
--- Day 12: Hill Climbing Algorithm ---
You try contacting the Elves using your handheld device, but the river you're following must be too low to get a decent
signal.

You ask the device for a heightmap of the surrounding area (your puzzle input). The heightmap shows the local area from
above broken into a grid; the elevation of each square of the grid is given by a single lowercase letter, where a is
the lowest elevation, b is the next-lowest, and so on up to the highest elevation, z.

Also included on the heightmap are marks for your current position (S) and the location that should get the best signal
(E). Your current position (S) has elevation a, and the location that should get the best signal (E) has elevation z.

You'd like to reach E, but to save energy, you should do it in as few steps as possible. During each step, you can move
exactly one square up, down, left, or right. To avoid needing to get out your climbing gear, the elevation of the
destination square can be at most one higher than the elevation of your current square; that is, if your current
elevation is m, you could step to elevation n, but not to elevation o. (This also means that the elevation of the
destination square can be much lower than the elevation of your current square.)
"""
import math


def get_input(mode='test'):
    input = []
    filename = './input.txt'
    if mode == 'test':
        # use input2 (example input)
        filename = './input2.txt'
    with open(filename, 'r') as my_file:
        for line in my_file:
            line = line.replace("\n", "")
            input.append(line)
    return input


class HeightMap:
    """
    A height is a lowercase Alpha
    a being the lowest value, z being the highest
    """

    def __init__(self, char):
        self.char = char
        self.map = {}
        self.populate_map()

    def __getitem__(self, item):
        return self.map[item]

    def populate_map(self):
        # Create a map of chars to values
        # from value of lower a to lower z
        for ordinal in range(97, 123):
            self.map[chr(ordinal)] = ordinal - 96

        # Upper S and Upper E are the origin and destination
        # Those will not be in the map based on the above
        # But they ought to be keys for comparison later
        # We will say they have the lowest value because you start on S
        # And want to end on E
        self.map["E"] = self.map["z"]
        self.map["S"] = 0


class Cell:
    """
    A Cell is an individual spot on the grid
    It has an x and y coordinate and a height value
    """

    def __init__(self, x: int, y: int, char: str):
        self.x = x
        self.y = y
        self.name = f"{self.x:02d}{self.y:02d}"
        self.char = char
        self.height_map = HeightMap(char=self.char)
        self.height = self.height_map[char]
        self.distance = math.inf
        self.visited = False
        self.cell_up = None
        self.cell_down = None
        self.cell_left = None
        self.cell_right = None
        self.neighbors = None
        self.cell_count = None

    def __repr__(self):
        return self.char + f" x:{self.x} y:{self.y}"

    def __lt__(self, other):
        return self.height < other

    def __le__(self, other):
        return self.height <= other

    def __gt__(self, other):
        return self.height > other

    def __ge__(self, other):
        return self.height >= other

    def populate_neighbors(self):
        """
        If a cell's up down left or right is not none, return them
        """
        self.neighbors = [cell for cell in [self.cell_up, self.cell_down, self.cell_left, self.cell_right] if
                          cell is not None]


class PriorityQueue:
    """
    A Priority Queue contains a list of cells and their weight (height distance)
    """

    def __init__(self, vertexes):
        self.vertexes = vertexes
        self.start_vertex = None
        self.visited = []
        self.unvisited = []
        self.populate_unvisited()
        self.set_start()

    def set_start(self):
        """
        Find the S node in the vertices and set that as the first node in the unvisited list
        """

        for v in self.unvisited:
            if v.char == "S":
                self.start_vertex = v
                self.unvisited.remove(v)
                self.unvisited.insert(0, v)
                return

    def populate_unvisited(self):
        for index, row in enumerate(self.vertexes):
            for jindex, cell in enumerate(row):
                self.unvisited.append(cell)

    def insert_item(self, vertex, weight):
        # Insert the vertex at the top
        data = {"vertex": vertex.name, "weight": weight, "instance": vertex}
        self.vertexes.insert(0, data)

    def set_unvisited_weight(self, vertex, weight):
        # Find the vertex in the unvisited list, update it's 'distance'
        for node in self.unvisited:
            if node.name == vertex.name:
                node.distance = weight

    def get_unvisited_node_by_name(self, name):
        for node in self.unvisited:
            if node.name == name:
                return node

    def get_lowest_weighted_item(self):
        # returns the lowest weighted item in the queue
        lowest_seen = math.inf
        for v in self.unvisited:
            if v.distance < lowest_seen:
                lowest_seen = v
                self.unvisited.remove(v)
                return lowest_seen

        if lowest_seen == math.inf:
            # we should have find something by now:
            raise Exception("called get_lowest_weighted_item but nothing was returned")


class Grid:
    """
    A collection of cells
    """

    def __init__(self, input: [str]):
        self.input = input
        self.grid = None
        self.cell_count = None
        self.parse_grid()
        self.find_cell_neighbors()
        self.set_cell_count()

    def parse_grid(self):
        """
        The input is an array of lines, return a 2D array/grid
        Sabqponm
        abcryxxl
        accszExk
        acctuvwj
        abdefghi
        """
        two_d = [[char for char in row] for row in [row for index, row in enumerate(self.input)]]
        grid = []

        for index, row in enumerate(two_d):
            grid.insert(index, [])
            for jindex, char in enumerate(row):
                c = Cell(x=index, y=jindex, char=char)
                grid[index].insert(jindex, c)
        self.grid = grid

    def find_cell_neighbors(self):
        for index, row in enumerate(self.grid):
            for jindex, cell in enumerate(row):
                left = cell.y - 1
                up = cell.x - 1
                down = cell.x + 1
                right = cell.y + 1

                if left < 0:
                    cell.cell_left = None
                else:
                    cell.cell_left = self.grid[index][cell.y - 1]
                if up < 0:
                    cell.cell_up = None
                else:
                    cell.cell_up = self.grid[index - 1][cell.y]
                if right >= len(self.grid[0]):
                    cell.cell_right = None
                else:
                    cell.cell_right = self.grid[index][cell.y + 1]
                # The size/len of the grid is max rows
                if down >= len(self.grid):
                    cell.cell_down = None
                else:
                    cell.cell_down = self.grid[index + 1][cell.y]
                cell.populate_neighbors()

    def find_start_or_end(self, cell_name="S"):
        # Finds the first cell matching cell_name
        for index, row in enumerate(self.grid):
            for jindex, cell in enumerate(row):
                if cell.char == cell_name:
                    return cell

    def set_cell_count(self):
        total = 0
        for index, row in enumerate(self.grid):
            for jindex, cell in enumerate(row):
                total += 1
        self.cell_count = total


def do_part_one():
    input = get_input(mode='real')

    """
    Time for Djikstra
    1) Initialize distances of all vertices as infinite.

    2) Create an empty priority_queue pq.  Every item
       of pq is a pair (weight, vertex). Weight (or 
       distance) is used  as first item  of pair
       as first item is by default used to compare
       two pairs
    """

    g = Grid(input)

    pq = PriorityQueue(g.grid)
    start = g.find_start_or_end()
    pq.set_unvisited_weight(start, weight=0)

    i = 0
    while len(pq.unvisited) != 0:
        try:
            u = pq.get_lowest_weighted_item()
        except Exception as e:
            print(f"error on index {i}")
            print(f"unvisited remains {pq.unvisited}")
            for item in pq.unvisited:
                print(item.name, item)
            break

        pq.visited.append(u)
        if u.char == "E":
            break
        for n in u.neighbors:
            height_difference = n.height - u.height
            if height_difference <= 1:
                pq.set_unvisited_weight(n, u.distance + 1)

        i += 1

    sort = sorted(pq.visited, key=lambda d: d.distance)
    for item in sort:
        if item.char == "E":
            print(item, item.char, item.distance)


def do_part_two():
    pass


if __name__ == "__main__":
    do_part_one()
    do_part_two()
