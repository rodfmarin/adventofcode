"""
--- Day 14: Regolith Reservoir ---
The distress signal leads you to a giant waterfall! Actually, hang on - the signal seems like it's coming from the
waterfall itself, and that doesn't make any sense. However, you do notice a little path that leads behind the waterfall.

Correction: the distress signal leads you behind a giant waterfall! There seems to be a large cave system here, and the
signal definitely leads further inside.

As you begin to make your way deeper underground, you feel the ground rumble for a moment. Sand begins pouring into the
cave! If you don't quickly figure out where the sand is going, you could quickly become trapped!

Fortunately, your familiarity with analyzing the path of falling material will come in handy here. You scan a
two-dimensional vertical slice of the cave above you (your puzzle input) and discover that it is mostly air with
structures made of rock.

Your scan traces the path of each solid rock structure and reports the x,y coordinates that form the shape of the path,
where x represents distance to the right and y represents distance down. Each path appears as a single line of text in
your scan. After the first point of each path, each point indicates the end of a straight horizontal or vertical line
to be drawn from the previous point. For example:

498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
This scan means that there are two paths of rock; the first path consists of two straight lines, and the second path
consists of three straight lines. (Specifically, the first path consists of a line of rock from 498,4 through 498,6 and
another line of rock from 498,6 through 496,6.)

The sand is pouring into the cave from point 500,0.

Drawing rock as #, air as ., and the source of the sand as +, this becomes:
"""

"""
NB: I took the wrong approach on this challenge and tried to build an actual grid that could be viewed while each
grain of sand fell through the cave.  I did end up writing parser that could draw the cave and obstacles so you could
print(Grid) to see it.  My thoughts at the beginning were that I would do some sort of timelapse in the stdout where I 
could watch the sand fall frame by frame.  I abandoned the approach.

Somehow i got turned upside down on x,y
I init-ed a 2d grid of size x * y, though x was not the index in the row it was the index OF the row and col was not the
index in the column it was the index in the row.  Nasty

The efficient solution is as you step through the input list and map the obstacles, add their x,y into a set() of x,y
When you simulate the sand falling, check if beneath the sand's xy there are obstacles based on membership in the
blocked set.  if below the sand is blocked, try to move the sand according to the rules.  if the sand cannot move, the
sand's xy is added to the blocked set (because it is now at rest). continue the loop until:

in part 1 the first grain of sand has fallen off the edge into an abyss (or infinity, beyond the edge of the grid)
in part 2 with a cave floor there is no abyss, loop until the last grain of sand touches the origin (500,0)

"""


def get_input(mode='test'):
    input = []
    filename = './input.txt'
    if mode == 'test':
        # use input2 (example input)
        filename = './input2.txt'
    with open(filename, 'r') as my_file:
        for line in my_file:
            input.append(line)
    return input


class Grid:
    """
    A Grid is a map of x,y coordinates
    """
    def __init__(self, row_length: int, col_length: int, paths: [str]):
        self.row_length = row_length  # How wide is the row
        self.col_length = col_length  # How long is the column
        self.grid = []
        self.prepare_grid()
        self.cursor = {"x": None, "y": None}
        self.sand_origin = [0, 500]
        self.blocked_sand = set()
        self.paths = paths

    def prepare_grid(self):
        """
        Initialize an empty grid of x * y
        """
        self.grid = [["." for col in range(self.col_length + 1)] for row in range(self.row_length + 1)]

    @staticmethod
    def _sanitize_path_string(string: str) -> list:
        """
        Turn:
        503,4 -> 502,4 -> 502,9 -> 494,9
        Into:
        [503,4, 502,4, 502,9, 494,9]
        """
        return string.split(" -> ")

    def draw_paths(self):
        """
        For each path in our paths
            For each x,y in our path
            Use the first x,y as a start point
            Fill in the range between start point and next path x,y
            Next path x,y becomes start
        """
        self.grid[0][500] = "+"
        queue = self.paths[:]
        for path in queue:
            self.cursor["x"] = None
            self.cursor["y"] = None
            path = self._sanitize_path_string(path)
            for item in path:
                points = item.split(",")
                x = int(points[1])
                y = int(points[0])

                # Connect the dots if there is a cursor
                if self.cursor["x"] is not None:

                    x_span = abs(x - self.cursor["x"])
                    y_span = abs(y - self.cursor["y"])
                    # do we draw vertically? that means a difference between x and the cursor's x
                    if x < self.cursor['x']:
                        for item in range(x_span):
                            self.draw_at(x + item, y)
                            self.blocked_sand.add((x + item, y))
                    elif x > self.cursor['x']:
                        for item in range(x_span):
                            self.draw_at(x - item, y)
                            self.blocked_sand.add((x - item, y))
                    # do we draw horizontally? that means a difference between y and the cursor's y
                    if y < self.cursor['y']:
                        for item in range(y_span):
                            self.draw_at(x, y + item)
                            self.blocked_sand.add((x, y + item))
                    elif y > self.cursor['y']:
                        for item in range(y_span):
                            self.draw_at(x, y - item)
                            self.blocked_sand.add((x, y - item))
                else:
                    self.draw_at(x, y)
                    self.blocked_sand.add((x, y))
                self.cursor["x"] = x
                self.cursor["y"] = y

    def draw_at(self, x: int, y: int):
        self.grid[x][y] = "#"

    def __repr__(self):
        """
        Pretty Print the grid
        Matched the example
        """
        s = ""
        for index, row in enumerate(self.grid):
            for jindex, column in enumerate(row):
                if jindex >= 493:
                    if jindex == len(row) - 1:
                        s += self.grid[index][jindex]+'\n'
                    else:
                        s += self.grid[index][jindex]
        return s


def parse_paths(lines: [str]) -> list:
    """
    498,4 -> 498,6 -> 496,6\n
    503,4 -> 502,4 -> 502,9 -> 494,9
    Return a list of paths, each line is a path
    """
    paths = []

    for line in lines:
        line = line.replace("\n", "")
        paths.append(line)
    return paths


def find_grid_boundaries(paths: [str]) -> tuple:
    """
    From all given paths find the largest x and largest y to init a grid of that size
    Returns a tuple of the form x,y
    """
    max_x = 0
    max_y = 0
    for path in paths:
        xy = path.split(" -> ")
        for pair in xy:
            parts = pair.split(",")
            x = int(parts[0])
            y = int(parts[1])
            if x > max_x:
                max_x = x
            if y > max_y:
                max_y = y

    return max_y, max_x


def run_tests():
    input = get_input(mode="test")
    paths = parse_paths(input)

    x, y = find_grid_boundaries(paths)
    g = Grid(x, y, paths)
    g.draw_paths()
    print(g)
    assert (9, 503) == find_grid_boundaries(paths)


def do_part_one():
    input = get_input(mode="real")
    paths = parse_paths(input)

    x, y = find_grid_boundaries(paths)
    g = Grid(x, y, paths)
    g.draw_paths()
    print(g)

    sand_start = (0, 500)
    counter = 0
    depth = g.row_length
    done = False
    while not done:
        sand_pos_x, sand_pos_y = sand_start
        blocked = False
        while not blocked:
            if sand_pos_x > depth:
                done = True
                break
            elif (sand_pos_x + 1, sand_pos_y) not in g.blocked_sand:
                sand_pos_x, sand_pos_y = sand_pos_x + 1, sand_pos_y
            elif (sand_pos_x + 1, sand_pos_y - 1) not in g.blocked_sand:
                sand_pos_x, sand_pos_y = sand_pos_x + 1, sand_pos_y - 1
            elif (sand_pos_x + 1, sand_pos_y + 1) not in g.blocked_sand:
                sand_pos_x, sand_pos_y = sand_pos_x + 1, sand_pos_y + 1
            else:
                blocked = True
        if blocked:
            g.blocked_sand.add((sand_pos_x, sand_pos_y))
            counter += 1

    print(counter)


def do_part_two():

    input = get_input(mode="real")
    paths = parse_paths(input)

    x, y = find_grid_boundaries(paths)
    g = Grid(x, y, paths)
    g.draw_paths()
    print(g)

    sand_start = (0, 500)
    counter = 0
    depth = g.row_length

    for i in range(1000):
        g.blocked_sand.add((depth + 2, i))

    done = False
    while not done:
        sand_pos_x, sand_pos_y = sand_start
        blocked = False
        while not blocked:
            if (sand_pos_x + 1, sand_pos_y) not in g.blocked_sand:
                sand_pos_x, sand_pos_y = sand_pos_x + 1, sand_pos_y
            elif (sand_pos_x + 1, sand_pos_y - 1) not in g.blocked_sand:
                sand_pos_x, sand_pos_y = sand_pos_x + 1, sand_pos_y - 1
            elif (sand_pos_x + 1, sand_pos_y + 1) not in g.blocked_sand:
                sand_pos_x, sand_pos_y = sand_pos_x + 1, sand_pos_y + 1
            else:
                blocked = True
        if sand_pos_y == 500 and sand_pos_x == 0:
            done = True
        else:
            g.blocked_sand.add((sand_pos_x, sand_pos_y))
            counter += 1

    print(counter + 1)  # account for sand start


if __name__ == "__main__":
    do_part_one()
    do_part_two()