"""
--- Day 5: Supply Stacks ---
The expedition can depart as soon as the final supplies have been unloaded from the ships. Supplies are stored in
stacks of marked crates, but because the needed supplies are buried under many other crates, the crates need to be
rearranged.

The ship has a giant cargo crane capable of moving crates between stacks. To ensure none of the crates get crushed or
fall over, the crane operator will rearrange them in a series of carefully-planned steps. After the crates are
rearranged, the desired crates will be at the top of each stack.

The Elves don't want to interrupt the crane operator during this delicate procedure, but they forgot to ask her which
crate will end up where, and they want to be ready to unload them as soon as possible so they can embark.

They do, however, have a drawing of the starting stacks of crates and the rearrangement procedure (your puzzle input).
For example:

    [D]
[N] [C]
[Z] [M] [P]
 1   2   3

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
In this example, there are three stacks of crates. Stack 1 contains two crates: crate Z is on the bottom, and crate N
is on top. Stack 2 contains three crates; from bottom to top, they are crates M, C, and D. Finally, stack 3 contains a
single crate, P.

Then, the rearrangement procedure is given. In each step of the procedure, a quantity of crates is moved from one stack
to a different stack. In the first step of the above rearrangement procedure, one crate is moved from stack 2 to stack
1, resulting in this configuration:

[D]
[N] [C]
[Z] [M] [P]
 1   2   3
In the second step, three crates are moved from stack 1 to stack 3. Crates are moved one at a time, so the first crate
to be moved (D) ends up below the second and third crates:

        [Z]
        [N]
    [C] [D]
    [M] [P]
 1   2   3
Then, both crates are moved from stack 2 to stack 1. Again, because crates are moved one at a time, crate C ends up
below crate M:

        [Z]
        [N]
[M]     [D]
[C]     [P]
 1   2   3
Finally, one crate is moved from stack 1 to stack 2:

        [Z]
        [N]
        [D]
[C] [M] [P]
 1   2   3
The Elves just need to know which crate will end up on top of each stack; in this example, the top crates are C in
stack 1, M in stack 2, and Z in stack 3, so you should combine these together and give the Elves the message CMZ.
"""


def get_input():
    input = []
    with open('./input.txt', 'r') as my_file:
        for line in my_file:
            line = line.replace("\n", "")
            input.append(line)
    return input


class CrateParser:
    """
    A Class that will convert raw textual input (crate and move instructions) to Columns and Move List
    """
    def __init__(self, input: [str]):
        """
        input is the raw textual input:
            [D]
        [N] [C]
        [Z] [M] [P]
         1   2   3

        move 1 from 2 to 1
        move 3 from 1 to 3
        move 2 from 2 to 1
        move 1 from 1 to 2
        """
        self.input = input
        self.column_count = 0
        self.moves_list = []
        self.columns = []
        self.separator_start = 0
        self.columns_start = 0
        self.moves_start = 0
        self.parse()
        self.detect_columns(self.input[self.columns_start])
        self.populate_move_list()
        self.populate_columns()
        self.process_moves()

    def parse(self):
        """
        Find the break in the input which is an empty line
        The column width is the line before this line
        The instruction sets start on the line after this line
        """
        i = 0
        for line in self.input:
            if line == "":
                # Found the separator
                self.separator_start = i
                self.columns_start = i-1
                self.moves_start = i+1
            i += 1

    def detect_columns(self, input: str):
        """
        Given a string of space seperated numbers, return the number of columns the string represents
        i.e.
        1   2   3   4   5   6   7   8   9
        should return 9
        """
        # space separator is 3 spaces
        space_separator = "   "
        columns = input.strip().split(space_separator)
        self.column_count = int(columns[-1])

        for c in range(self.column_count):
            self.columns.insert(c, [])

    def populate_move_list(self):
        """
        Populate a list of moves starting from the move_start
        An instruction is like:
        move 1 from 2 to 1
        we'll turn this into [1,2,1] as a representation of a move
        """

        for line in self.input[self.moves_start:]:
            parts = line.split(" ")
            instruction = [parts[1], parts[3], parts[5]]
            self.moves_list.append(instruction)

    def populate_columns(self):
        """
        Given a line representing a layer in a stack
        Fill the appropriate column with that crate in the stack
            [D]
        [N] [C]
        [Z] [M] [P]
         1   2   3

         In Line 0 D would be at the top of stack 2
         In line 1 N would be at the top of stack 1 but C would be the next layer in stack 2
         And so on
        """

        for line in self.input[self.columns_start-1::-1]:
            self.walk_layer(line)

    def walk_layer(self, line: str):
        """
        'Walk' a layer of the crate line and populate each column with the letter found
        """

        # Keep track of the column we're on based on how many 'steps' we've taken through the line
        column_tracker = 0
        step_counter = 0

        for char in line:
            if char.isalpha():
                self.columns[column_tracker].append(char)

            if step_counter % 4 == 0:
                if step_counter == 0:
                    pass
                else:
                    column_tracker += 1
            step_counter += 1

    def process_moves(self):
        """
        For each move in the move list, apply the moves across the column stacks
        move 1 from 2 to 1
        turns into [1,2,1] as a representation of a move
        the from and to column will need to be decremented by 1 as columns are 0 based
        """
        for move in self.moves_list:
            job = []
            mv = int(move[0])
            frm = int(move[1])-1
            to = int(move[2])-1
            for i in range(mv):
                job.append(self.columns[frm].pop())
            for j in job:
                self.columns[to].append(j)

    def get_column_tops(self):
        """
        After the moves are processed, which crates are on top?
        In the example after the moves are processed C M and Z are on the top
        Would return the string "CMZ"
        """
        s = ""
        for c in self.columns:
            s += c[-1]
        return s


class CrateParser9001(CrateParser):
    """
    Handle the moving a bit differently
    """

    def process_moves(self):
        """
        Can handle multiple moves at once
        """
        for move in self.moves_list:
            job = []
            mv = int(move[0])
            frm = int(move[1])-1
            to = int(move[2])-1
            for i in range(mv):
                job.append(self.columns[frm].pop())
            job.reverse()
            for j in job:
                self.columns[to].append(j)


def do_part_one():
    # After the rearrangement procedure completes, what crate ends up on top of each stack?
    input = get_input()
    c = CrateParser(input)
    print(c.get_column_tops())


def do_part_two():
    """
    --- Part Two ---
    As you watch the crane operator expertly rearrange the crates, you notice the process isn't following your
    prediction.

    Some mud was covering the writing on the side of the crane, and you quickly wipe it away. The crane isn't a
    CrateMover 9000 - it's a CrateMover 9001.

    The CrateMover 9001 is notable for many new and exciting features: air conditioning, leather seats, an extra cup
    holder, and the ability to pick up and move multiple crates at once.

    Again considering the example above, the crates begin in the same configuration:

        [D]
    [N] [C]
    [Z] [M] [P]
     1   2   3
    Moving a single crate from stack 2 to stack 1 behaves the same as before:

    [D]
    [N] [C]
    [Z] [M] [P]
     1   2   3
    However, the action of moving three crates from stack 1 to stack 3 means that those three moved crates stay in the
    same order, resulting in this new configuration:

            [D]
            [N]
        [C] [Z]
        [M] [P]
     1   2   3
    Next, as both crates are moved from stack 2 to stack 1, they retain their order as well:

            [D]
            [N]
    [C]     [Z]
    [M]     [P]
     1   2   3
    Finally, a single crate is still moved from stack 1 to stack 2, but now it's crate C that gets moved:

            [D]
            [N]
            [Z]
    [M] [C] [P]
     1   2   3
    In this example, the CrateMover 9001 has put the crates in a totally different order: MCD.

    Before the rearrangement process finishes, update your simulation so that the Elves know where they should stand to
    be ready to unload the final supplies. After the rearrangement procedure completes, what crate ends up on top of
    each stack?
    """

    # After the rearrangement procedure completes, what crate ends up on top of each stack?
    # NB: Crates can now be moved in multiples
    input = get_input()
    c = CrateParser9001(input)
    print(c.get_column_tops())


if __name__ == "__main__":
    do_part_one()
    do_part_two()
