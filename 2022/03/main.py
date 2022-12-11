"""
--- Day 3: Rucksack Reorganization ---
One Elf has the important job of loading all of the rucksacks with supplies for the jungle journey.
Unfortunately, that Elf didn't quite follow the packing instructions, and so a few items now need to be rearranged.

Each rucksack has two large compartments. All items of a given type are meant to go into exactly one of the two
compartments. The Elf that did the packing failed to follow this rule for exactly one item type per rucksack.

The Elves have made a list of all of the items currently in each rucksack (your puzzle input),
but they need your help finding the errors. Every item type is identified by a single
lowercase or uppercase letter (that is, a and A refer to different types of items).

The list of items for each rucksack is given as characters all on a single line. A given rucksack always has the
same number of items in each of its two compartments, so the first half of the characters represent items in the first
compartment, while the second half of the characters represent items in the second compartment.

For example, suppose you have the following list of contents from six rucksacks:

vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw

The first rucksack contains the items vJrwpWtwJgWrhcsFMMfFFhFp, which means its first compartment contains the items
vJrwpWtwJgWr, while the second compartment contains the items hcsFMMfFFhFp. The only item type that appears in both
compartments is lowercase p.

The second rucksack's compartments contain jqHRNqRjqzjGDLGL and rsFMfFZSrLrFZsSL. The only item type that appears in
both compartments is uppercase L.

The third rucksack's compartments contain PmmdzqPrV and vPwwTWBwg; the only common item type is uppercase P.
The fourth rucksack's compartments only share item type v.
The fifth rucksack's compartments only share item type t.
The sixth rucksack's compartments only share item type s.
To help prioritize item rearrangement, every item type can be converted to a priority:

Lowercase item types a through z have priorities 1 through 26.
Uppercase item types A through Z have priorities 27 through 52.
In the above example, the priority of the item type that appears in both compartments of each rucksack is
16 (p), 38 (L), 42 (P), 22 (v), 20 (t), and 19 (s); the sum of these is 157.
"""


def get_input():
    input = []
    with open('./input.txt', 'r') as my_file:
        for line in my_file:
            line = line.replace("\n", "")
            input.append(line)
    return input


class ContentMap:
    """
    Lowercase item types a through z have priorities 1 through 26.
    Uppercase item types A through Z have priorities 27 through 52.

    The capital letter "A" is represented by the binary value:
    0100 0001
    The lowercase letter "a" is represented by the binary value:
    0110 0001
    The difference is the third most significant bit. In decimal and hexadecimal, this corresponds to:

    Character	Binary	    Decimal	    Hexadecimal
    A	        0100 0001	65	        0x41
    a	        0110 0001	97	        0x61
    The difference between upper- and lowercase characters is always 32 (0x20 in hexadecimal),
    so converting from upper- to lowercase and back is a matter of adding or subtracting 32 from the ASCII character
    code.
    """
    def __init__(self):
        self.map = {}
        self.populate_map()

    def populate_map(self):
        """
        enumerate the ascii values for lower and upper
        create a map with the char and value
        """

        # Create the upper case map
        for i in range(65, (65+26)):
            self.map[f"{chr(i)}"] = (i-64) + 26

        # Create the lower case map
        for i in range(97, (97+26)):
            self.map[f"{chr(i)}"] = i-96


class Rucksack:
    """
    A Rucksack is a string that represents two 'compartments'
    vJrwpWtwJgWrhcsFMMfFFhFp is a rucksack:
    which means its first compartment contains the items
    vJrwpWtwJgWr, while the second compartment contains the items hcsFMMfFFhFp.
    The only item type that appears in both compartments is lowercase p.
    """
    def __init__(self, contents: str):
        self.contents = contents
        self.compartment_1 = None
        self.compartment_2 = None
        self.content_len = 0
        self.midpoint = 0
        self.matched_pairs = []
        self.priority_value = 0
        self.content_map = ContentMap()
        self.fill_compartments()
        self.find_compartment_matches()
        self.calculate_priority_from_matches()

    def fill_compartments(self):
        """
        A Rucksack's contents is a variable length string.  According to the story it should be evenly divisible
        And the first half is compartment 1 and the second half is compartment 2.
        """
        self.content_len = len(self.contents)
        self.midpoint = int(self.content_len / 2)
        self.compartment_1 = self.contents[0:self.midpoint]
        self.compartment_2 = self.contents[self.midpoint:]

    def find_compartment_matches(self):
        """
        Look through each compartment's contents, find the matched pairs
        """
        for i in self.compartment_1:
            if i in self.matched_pairs:
                break
            for j in self.compartment_2:
                if j in self.matched_pairs:
                    break
                if i == j:
                    self.matched_pairs.append(i)

    def calculate_priority_from_matches(self):
        """
        For compartment matches, calculate their priority value
        """
        for match in self.matched_pairs:
            if match in self.content_map.map:
                self.priority_value += self.content_map.map[match]


class BadgeFinder:
    """
    A Class that searches 3 rucksacks for a common item
    """
    def __init__(self, rucksack_1: Rucksack, rucksack_2: Rucksack, rucksack_3: Rucksack):
        self.rucksack_1 = rucksack_1
        self.rucksack_2 = rucksack_2
        self.rucksack_3 = rucksack_3
        self.common_item = None
        self.find()

    def find(self):
        """
        Compare 3 Rucksacks for an item that is common to all
        """

        for i in self.rucksack_1.contents:
            if i in self.rucksack_2.contents:
                if i in self.rucksack_3.contents:
                    self.common_item = i


def do_part_one():
    """
    Find the item type that appears in both compartments of each rucksack.
    What is the sum of the priorities of those item types?
    """

    input = get_input()
    sum = 0
    for line in input:
        r = Rucksack(contents=line)
        sum += r.priority_value

    print(sum)


def do_part_two():
    """
    --- Part Two ---
    As you finish identifying the misplaced items, the Elves come to you with another issue.

    For safety, the Elves are divided into groups of three. Every Elf carries a badge that identifies their group.
    For efficiency, within each group of three Elves, the badge is the only item type carried by all three Elves.
    That is, if a group's badge is item type B, then all three Elves will have item type B somewhere in their rucksack,
    and at most two of the Elves will be carrying any other item type.

    The problem is that someone forgot to put this year's updated authenticity sticker on the badges. All of the badges
    need to be pulled out of the rucksacks so the new authenticity stickers can be attached.

    Additionally, nobody wrote down which item type corresponds to each group's badges. The only way to tell which item
    type is the right one is by finding the one item type that is common between all three Elves in each group.

    Every set of three lines in your list corresponds to a single group, but each group can have a different badge item
    type. So, in the above example, the first group's rucksacks are the first three lines:

    vJrwpWtwJgWrhcsFMMfFFhFp
    jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
    PmmdzqPrVvPwwTWBwg
    And the second group's rucksacks are the next three lines:

    wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
    ttgJtRGJQctTZtZT
    CrZsJsPPZsGzwwsLwLmpwMDw
    In the first group, the only item type that appears in all three rucksacks is lowercase r; this must be their
    badges. In the second group, their badge item type must be Z.

    Priorities for these items must still be found to organize the sticker attachment efforts: here, they are 18 (r)
    for the first group and 52 (Z) for the second group. The sum of these is 70.
    """

    #     Find the item type that corresponds to the badges of each three-Elf group.
    #     What is the sum of the priorities of those item types?

    input = get_input()
    c = ContentMap()
    sum = 0
    i = 0
    while i <= len(input) - 1:
        r1 = Rucksack(contents=input[i])
        r2 = Rucksack(contents=input[i+1])
        r3 = Rucksack(contents=input[i+2])
        b = BadgeFinder(r1, r2, r3)
        print(b.common_item)
        sum += c.map[b.common_item]
        i += 3
    print(sum)


if __name__ == "__main__":
    do_part_one()
    do_part_two()
