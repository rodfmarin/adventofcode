"""
--- Day 8: Treetop Tree House ---
The expedition comes across a peculiar patch of tall trees all planted carefully in a grid. The Elves explain that a
previous expedition planted these trees as a reforestation effort. Now, they're curious if this would be a good
location for a tree house.

First, determine whether there is enough tree cover here to keep a tree house hidden. To do this, you need to count the
number of trees that are visible from outside the grid when looking directly along a row or column.

The Elves have already launched a quadcopter to generate a map with the height of each tree (your puzzle input). For
example:

30373
25512
65332
33549
35390

Each tree is represented as a single digit whose value is its height, where 0 is the shortest and 9 is the tallest.

A tree is visible if all of the other trees between it and an edge of the grid are shorter than it. Only consider trees
in the same row or column; that is, only look up, down, left, or right from any given tree.

All of the trees around the edge of the grid are visible - since they are already on the edge, there are no trees to
block the view. In this example, that only leaves the interior nine trees to consider:

The top-left 5 is visible from the left and top. (It isn't visible from the right or bottom since other trees of height
5 are in the way.)
The top-middle 5 is visible from the top and right.
The top-right 1 is not visible from any direction; for it to be visible, there would need to only be trees of height 0
between it and an edge.
The left-middle 5 is visible, but only from the right.
The center 3 is not visible from any direction; for it to be visible, there would need to be only trees of at most
height 2 between it and an edge.
The right-middle 3 is visible from the right.
In the bottom row, the middle 5 is visible, but the 3 and 4 are not.
With 16 trees visible on the edge and another 5 visible in the interior, a total of 21 trees are visible in this
arrangement.

Consider your map; how many trees are visible from outside the grid?
"""


def get_input():
    input = []
    with open('./input.txt', 'r') as my_file:
        for line in my_file:
            line = line.replace("\n", "")
            input.append(line)
    return input


class TreeNode:
    """
    A Class that represents a Tree in the TreeGrid
    """
    def __init__(self, height: int, x: int = 0, y: int = 0):
        self.height = height
        self.x = x
        self.y = y
        self.name = None
        self.visible_up = False
        self.visible_down = False
        self.visible_left = False
        self.visible_right = False
        self.is_edge = False
        self.am_i_edge()
        self.set_name()
        self.up_score = 0
        self.down_score = 0
        self.left_score = 0
        self.right_score = 0
        self.scenic_score = 0

    def am_i_edge(self):
        """
        We know if we init a TreeNode with x of 0 or y of 0 it's automatically an edge
        """
        if self.x == 0 or self.y == 0:
            self.is_edge = True

    def set_name(self):
        self.name = str(self.x) + ',' + str(self.y)

    def set_scenic_score(self):
        self.scenic_score = self.up_score * self.left_score * self.down_score * self.right_score


class TreeGrid:
    """
    A Class that holds a grid of Tree Nodes
    """
    def __init__(self, input: [str]):
        self.input = input
        self.grid = []
        self.line_count = 0
        self.column_count = 0
        self.parse()
        self.cell_count = self.line_count * self.column_count

    def parse(self):
        """
        Parse the input lines and populate the tree grid
        """
        for line, item in enumerate(self.input):
            self.grid.insert(line, [])
            self.line_count += 1
            self.column_count = len(item)
            for column, height in enumerate(item):
                # Create a TreeNode at the proper x/y and record its height
                t = TreeNode(height=int(height), x=line, y=column)
                if line + 1 == len(self.input):
                    # line is actually the index but called line here for readability?
                    # if the index is the same as the size of the input then we're on the last line
                    # i.e. if we're on line 3 of a 3 line file, that's the end!
                    # We're on the last line and that node is an edge
                    t.is_edge = True
                elif column + 1 == len(item):
                    # Same deal here just the last *column*
                    t.is_edge = True

                self.grid[line].insert(column, t)

    def get_node(self, name):
        """
        Return the node at coordinates of name
        """
        tokens = name.split(',')
        x = int(tokens[0])
        y = int(tokens[1])

        return self.grid[x][y]


def scan(tree_grid: TreeGrid):
    """
    Just plain ol iterate over the grid
    left to right
    top to bottom
    right to left
    bottom to top
    """

    candidate_trees = []

    # look left to right
    lr = scan_l_r(tree_grid)
    for t in lr:
        candidate_trees.append(t)

    # look up to down
    ud = scan_u_d(tree_grid)
    for t in ud:
        candidate_trees.append(t)

    # look right to left
    rl = scan_r_l(tree_grid)
    for t in rl:
        candidate_trees.append(t)

    # look down to up
    du = scan_d_u(tree_grid)
    for t in du:
        candidate_trees.append(t)

    return candidate_trees


def scan_l_r(tree_grid: TreeGrid):
    candidate_trees = []

    # look left to right
    for row in range(tree_grid.line_count):
        edge_tree = tree_grid.grid[row][0]
        tallest_height = edge_tree.height
        for col in range(tree_grid.column_count):
            tree = tree_grid.grid[row][col]
            if tree.is_edge:
                candidate_trees.append(tree)
                continue
            if tree.height > tallest_height:
                tree.visible_left = True
                candidate_trees.append(tree)
                tallest_height = tree.height

    return candidate_trees


def scan_u_d(tree_grid: TreeGrid):

    candidate_trees = []

    for col_index in range(tree_grid.column_count):
        edge_tree = tree_grid.grid[0][col_index]
        tallest_height = edge_tree.height
        for row_index in range(tree_grid.column_count):
            tree = tree_grid.grid[row_index][col_index]

            if tree.is_edge:
                candidate_trees.append(tree)
                continue
            if tree.height > tallest_height:
                tree.visible_up = True
                tallest_height = tree.height
                candidate_trees.append(tree)

    return candidate_trees


def scan_r_l(tree_grid: TreeGrid):
    candidate_trees = []

    # look right to left
    for row in range(tree_grid.line_count):
        edge_tree = tree_grid.grid[row][-1]
        tallest_height = edge_tree.height
        for col in reversed(range(tree_grid.column_count)):
            tree = tree_grid.grid[row][col]
            if tree.is_edge:
                candidate_trees.append(tree)
                continue
            if tree.height > tallest_height:
                tree.visible_right = True
                candidate_trees.append(tree)
                tallest_height = tree.height

    return candidate_trees


def scan_d_u(tree_grid: TreeGrid):

    candidate_trees = []

    for row_index in reversed(range(tree_grid.line_count)):
        tallest_height = 0
        for col_index in reversed(range(tree_grid.column_count)):

            tree = tree_grid.grid[col_index][row_index]
            if tree.is_edge:
                tallest_height = tree.height
                candidate_trees.append(tree)
                continue
            if tree.height > tallest_height:
                tree.visible_down = True
                candidate_trees.append(tree)
                tallest_height = tree.height

    return candidate_trees


def look_up(node: TreeNode, tree: TreeGrid):
    """
    Walk from this node "up" in the column index, i.e. same column (y) but decremented row (x) moving "up"
    """

    node_score = 0
    if node.is_edge:
        node.up_score = 0
    else:
        for row in reversed(range(node.x)):
            # if edge set score to 0
            # if trees, how many trees can you see in this direction until same or higher
            # set up score to this
            next_node_name = f"{row},{node.y}"
            if tree.get_node(next_node_name).height > node.height:
                node_score += 1
                break
            elif tree.get_node(next_node_name).height == node.height:
                node_score += 1
                break
            elif tree.get_node(next_node_name).height < node.height:
                node_score += 1
            else:
                break
    node.up_score = node_score


def look_down(node: TreeNode, tree: TreeGrid):
    """
    Walk from this node "down" in the column index, i.e. same column (y) but incremented row (x) moving "down"
    """

    node_score = 0
    if node.is_edge:
        node.down_score = 0
    else:
        for row in range(node.x+1, tree.line_count):
            # if edge set score to 0
            # if trees, how many trees can you see in this direction until same or higher
            # set up score to this
            next_node_name = f"{row},{node.y}"
            if tree.get_node(next_node_name).height > node.height:
                node_score += 1
                break
            elif tree.get_node(next_node_name).height == node.height:
                node_score += 1
                break
            elif tree.get_node(next_node_name).height < node.height:
                node_score += 1
            else:
                break
    node.down_score = node_score


def look_left(node: TreeNode, tree: TreeGrid):
    """
    Walk from this node "left" in the row index, i.e. same row (x) but decremented column (y) moving "left"
    """

    node_score = 0
    if node.is_edge:
        node.left_score = 0
    else:
        for col in reversed(range(node.y)):
            # if edge set score to 0
            # if trees, how many trees can you see in this direction until same or higher
            # set up score to this
            next_node_name = f"{node.x},{col}"
            if tree.get_node(next_node_name).height > node.height:
                node_score += 1
                break
            elif tree.get_node(next_node_name).height == node.height:
                node_score += 1
                break
            elif tree.get_node(next_node_name).height < node.height:
                node_score += 1
            else:
                break
    node.left_score = node_score


def look_right(node: TreeNode, tree: TreeGrid):
    """
    Walk from this node "right" in the row index, i.e. same row (x) but incremented column (y) moving "right"
    """

    node_score = 0
    if node.is_edge:
        node.right_score = 0
    else:
        for col in range(node.y+1, tree.line_count):
            # if edge set score to 0
            # if trees, how many trees can you see in this direction until same or higher
            # set up score to this
            next_node_name = f"{node.x},{col}"
            if tree.get_node(next_node_name).height > node.height:
                node_score += 1
                break
            elif tree.get_node(next_node_name).height == node.height:
                node_score += 1
                break
            elif tree.get_node(next_node_name).height < node.height:
                node_score += 1
            else:
                break
    node.right_score = node_score


def do_part_one():
    input = get_input()

    g = TreeGrid(input)

    trees = {tree for tree in scan(g)}
    print(len(trees))


def do_part_two():
    """
    --- Part Two ---
    Content with the amount of tree cover available, the Elves just need to know the best spot to build their tree
    house: they would like to be able to see a lot of trees.

    To measure the viewing distance from a given tree, look up, down, left, and right from that tree; stop if you reach
    an edge or at the first tree that is the same height or taller than the tree under consideration. (If a tree is
    right on the edge, at least one of its viewing distances will be zero.)

    The Elves don't care about distant trees taller than those found by the rules above; the proposed tree house has
    large eaves to keep it dry, so they wouldn't be able to see higher than the tree house anyway.

    In the example above, consider the middle 5 in the second row:

    30373
    25512
    65332
    33549
    35390

    Looking up, its view is not blocked; it can see 1 tree (of height 3).
    Looking left, its view is blocked immediately; it can see only 1 tree (of height 5, right next to it).
    Looking right, its view is not blocked; it can see 2 trees.
    Looking down, its view is blocked eventually; it can see 2 trees (one of height 3, then the tree of height 5 that
    blocks its view).
    A tree's scenic score is found by multiplying together its viewing distance in each of the four directions.
    For this tree, this is 4 (found by multiplying 1 * 1 * 2 * 2).

    However, you can do even better: consider the tree of height 5 in the middle of the fourth row:

    30373
    25512
    65332
    33549
    35390
    Looking up, its view is blocked at 2 trees (by another tree with a height of 5).
    Looking left, its view is not blocked; it can see 2 trees.
    Looking down, its view is also not blocked; it can see 1 tree.
    Looking right, its view is blocked at 2 trees (by a massive tree of height 9).
    This tree's scenic score is 8 (2 * 2 * 1 * 2); this is the ideal spot for the tree house.

    Consider each tree on your map. What is the highest scenic score possible for any tree?
    """

    input = get_input()

    g = TreeGrid(input)
    trees = {tree for tree in scan(g)}

    for tree in trees:
        look_up(tree, g)
        look_down(tree, g)
        look_left(tree, g)
        look_right(tree, g)

        tree.set_scenic_score()

    highest_score = 0

    for tree in trees:
        if tree.scenic_score > highest_score:
            highest_score = tree.scenic_score
    print(highest_score)


if __name__ == "__main__":
    do_part_one()
    do_part_two()