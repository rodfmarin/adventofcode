"""
--- Day 13: Distress Signal ---
You climb the hill and again try contacting the Elves. However, you instead receive a signal you weren't expecting: a
distress signal.

Your handheld device must still not be working properly; the packets from the distress signal got decoded out of order.
You'll need to re-order the list of received packets (your puzzle input) to decode the message.

Your list consists of pairs of packets; pairs are separated by a blank line. You need to identify how many pairs of
packets are in the right order.

For example:

[1,1,3,1,1]
[1,1,5,1,1]
truncated
"""
from functools import cmp_to_key


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


def get_input_2(mode='test'):
    filename = './input.txt'
    if mode == 'test':
        # use input2 (example input)
        filename = './input2.txt'
    with open(filename, 'r') as my_file:
        return my_file.read().strip().replace("\n\n", "\n").split("\n")


def compare(a, b):
    # Comparator Functions are Fun :)
    # Lesson Learned: Try not to use Booleans but  integers for the result of a compare
    # This way you can return -1, 0, 1 etc.
    if isinstance(a, list) and isinstance(b, int):
        b = [b]

    if isinstance(a, int) and isinstance(b, list):
        a = [a]

    if isinstance(a, int) and isinstance(b, int):
        if a < b:
            return 1
        if a == b:
            return 0
        return -1

    if isinstance(a, list) and isinstance(b, list):
        i = 0
        while i < len(a) and i < len(b):
            x = compare(a[i], b[i])
            if x == 1:
                return 1
            if x == -1:
                return -1

            i += 1

        if i == len(a):
            if len(a) == len(b):
                return 0
            return 1  # a ended first

        # If i didn't hit the end of a, it hit the end of b first
        # This means that b is shorter, which is bad
        return -1


class Pair:
    """
    A Pair represents two lists to seek through and find out if their in the correct order
    """

    def __init__(self, left_string: str, right_string: str):
        self.left_string = left_string
        self.right_string = right_string
        self.left = None
        self.right = None
        self.try_parse()

    def try_parse(self):
        """
        Try to eval left and right and assign their expressions to left and right
        """
        self.left = eval(self.left_string)
        self.right = eval(self.right_string)

    def __repr__(self):
        return f"left:{str(self.left_string)}, right:{str(self.right_string)}"


def parse_input(input: [str]):
    """
    Input is a list of lines
    Pairs are next to each other separated by a blank line
    """
    pairs = []
    for i in range(0, len(input), 3):
        left = input[i]
        right = input[i + 1]
        p = Pair(left, right)
        pairs.append(p)
    return pairs


def parse_input_part_two(input: [str]):
    """
    Disregard the lines just get all the packets
    """
    lines = []
    lines.append([[2]])
    lines.append([[6]])
    for line in input:
        if str.isprintable(line):
            lines.append(line)
    return lines


def do_part_one():
    input = get_input(mode='real')
    pairs = parse_input(input)
    sum = 0

    for index, p in enumerate(pairs):
        if compare(p.left, p.right) == 1:
            sum += index + 1
    print(sum)


def do_part_two():
    """
    --- Part Two ---
    Now, you just need to put all of the packets in the right order. Disregard the blank lines in your list of received
    packets.

    The distress signal protocol also requires that you include two additional divider packets:

    [[2]]
    [[6]]
    Using the same rules as before, organize all packets - the ones in your list of received packets as well as the two
    divider packets - into the correct order.

    For the example above, the result of putting the packets in the correct order is:
    truncated
    """
    input = get_input_2(mode='real')
    packets = list(map(eval, input))

    packets.append([[2]])
    packets.append([[6]])
    # Super neat cmp_to_key function in functools
    packets = sorted(packets, key=cmp_to_key(compare), reverse=True)

    a = 0
    b = 0
    # We just want to multiply the index of divider packets in the sorted list
    for i, li in enumerate(packets):
        if li == [[2]]:
            a = i + 1
        if li == [[6]]:
            b = i + 1

    print(a*b)


if __name__ == "__main__":
    do_part_one()
    do_part_two()
