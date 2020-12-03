"""
--- Day 3: Toboggan Trajectory ---
With the toboggan login problems resolved, you set off toward the airport. While travel by toboggan might be easy,
it's certainly not safe: there's very minimal steering and the area is covered in trees. You'll need to see which angles will take you near the fewest trees.

Due to the local geology, trees in this area only grow on exact integer coordinates in a grid. You make a map
(your puzzle input) of the open squares (.) and trees (#) you can see. For example:

..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#
These aren't the only trees, though; due to something you read about once involving arboreal genetics and biome
stability, the same pattern repeats to the right many times:

..##.........##.........##.........##.........##.........##.......  --->
#...#...#..#...#...#..#...#...#..#...#...#..#...#...#..#...#...#..
.#....#..#..#....#..#..#....#..#..#....#..#..#....#..#..#....#..#.
..#.#...#.#..#.#...#.#..#.#...#.#..#.#...#.#..#.#...#.#..#.#...#.#
.#...##..#..#...##..#..#...##..#..#...##..#..#...##..#..#...##..#.
..#.##.......#.##.......#.##.......#.##.......#.##.......#.##.....  --->
.#.#.#....#.#.#.#....#.#.#.#....#.#.#.#....#.#.#.#....#.#.#.#....#
.#........#.#........#.#........#.#........#.#........#.#........#
#.##...#...#.##...#...#.##...#...#.##...#...#.##...#...#.##...#...
#...##....##...##....##...##....##...##....##...##....##...##....#
.#..#...#.#.#..#...#.#.#..#...#.#.#..#...#.#.#..#...#.#.#..#...#.#  --->
You start on the open square (.) in the top-left corner and need to reach the bottom (below the bottom-most row on
your map).

The toboggan can only follow a few specific slopes (you opted for a cheaper model that prefers rational numbers);
start by counting all the trees you would encounter for the slope right 3, down 1:

From your starting position at the top-left, check the position that is right 3 and down 1. Then, check the position
that is right 3 and down 1 from there, and so on until you go past the bottom of the map.

The locations you'd check in the above example are marked here with O where there was an open square and X where
there was a tree:

..##.........##.........##.........##.........##.........##.......  --->
#..O#...#..#...#...#..#...#...#..#...#...#..#...#...#..#...#...#..
.#....X..#..#....#..#..#....#..#..#....#..#..#....#..#..#....#..#.
..#.#...#O#..#.#...#.#..#.#...#.#..#.#...#.#..#.#...#.#..#.#...#.#
.#...##..#..X...##..#..#...##..#..#...##..#..#...##..#..#...##..#.
..#.##.......#.X#.......#.##.......#.##.......#.##.......#.##.....  --->
.#.#.#....#.#.#.#.O..#.#.#.#....#.#.#.#....#.#.#.#....#.#.#.#....#
.#........#.#........X.#........#.#........#.#........#.#........#
#.##...#...#.##...#...#.X#...#...#.##...#...#.##...#...#.##...#...
#...##....##...##....##...#X....##...##....##...##....##...##....#
.#..#...#.#.#..#...#.#.#..#...X.#.#..#...#.#.#..#...#.#.#..#...#.#  --->
In this example, traversing the map using this slope would cause you to encounter 7 trees.

Starting at the top-left corner of your map and following a slope of right 3 and down 1, how many trees would you encounter?
"""


input = []
with open('input.txt') as my_file:
    for line in my_file:
        input.append(line.strip('\n'))


class Map:
    def __init__(self, grid_array):
        self.grid = grid_array
        self.grid_width = len(grid_array[0])
        self.grid_height = len(grid_array)


class Cursor:
    def __init__(self, map):
        self.x = 0
        self.y = 0
        self.trees_encountered = 0
        self.map = map

    def move(self, x, y):
        self.x = x
        self.y = y

    def inspect(self):
        if self.map.grid[self.y][self.x] == '#':
            self.trees_encountered += 1

    def slide_alpha(self):
        # Move X >>>> 1 spaces and Y >>> 1 check and add tree then stop at end
        while self.y < self.map.grid_height - 1:
            self.x = (self.x + 1) % self.map.grid_width
            self.y += 1
            self.inspect()

    def slide_beta(self):
        """
        'move' the cursor in a knight's L across 3 down 1 and inspect the tile
        We want to 'wrap' over in x to the start so let's use modulo division to wrap around
        We want to stop when we've reached the last line
        """

        # Move X >>>> 3 spaces and Y >>> 1 check and add tree then stop at end
        while self.y < self.map.grid_height - 1:
            self.x = (self.x + 3) % self.map.grid_width
            self.y += 1
            self.inspect()

    def slide_gamma(self):
        # Move X >>>> 5 spaces and Y >>> 1 check and add tree then stop at end
        while self.y < self.map.grid_height - 1:
            self.x = (self.x + 5) % self.map.grid_width
            self.y += 1
            self.inspect()

    def slide_delta(self):
        # Move X >>>> 7 spaces and Y >>> 1 check and add tree then stop at end
        while self.y < self.map.grid_height - 1:
            self.x = (self.x + 7) % self.map.grid_width
            self.y += 1
            self.inspect()

    def slide_epsilon(self):
        # Move X >>>> 3 spaces and Y >>> 1 check and add tree then stop at end
        while self.y < self.map.grid_height - 1:
            self.x = (self.x + 1) % self.map.grid_width
            self.y += 2
            self.inspect()

def main():
    map = Map(input)
    cursor = Cursor(map)

    cursor.slide_alpha()
    a_trees = cursor.trees_encountered

    cursor = Cursor(map)
    cursor.slide_beta()
    b_trees = cursor.trees_encountered

    cursor = Cursor(map)
    cursor.slide_gamma()
    g_trees = cursor.trees_encountered

    cursor = Cursor(map)
    cursor.slide_delta()
    d_trees = cursor.trees_encountered

    cursor = Cursor(map)
    cursor.slide_epsilon()
    e_trees = cursor.trees_encountered

    print(a_trees * b_trees * g_trees * d_trees * e_trees)


if __name__ == '__main__':
    main()