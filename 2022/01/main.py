"""
--- Day 1: Calorie Counting ---
Santa's reindeer typically eat regular reindeer food, but they need a lot of magical energy to deliver presents on
Christmas. For that, their favorite snack is a special type of star fruit that only grows deep in the jungle.
The Elves have brought you on their annual expedition to the grove where the fruit grows.

To supply enough magical energy, the expedition needs to retrieve a minimum of fifty stars by December 25th.
Although the Elves assure you that the grove has plenty of fruit, you decide to grab any fruit you see along the way,
just in case.

Collect stars by solving puzzles. Two puzzles will be made available on each day in the Advent calendar;
the second puzzle is unlocked when you complete the first. Each puzzle grants one star. Good luck!

The jungle must be too overgrown and difficult to navigate in vehicles or access from the air; the Elves' expedition
traditionally goes on foot. As your boats approach land, the Elves begin taking inventory of their supplies.
One important consideration is food - in particular, the number of Calories each Elf is carrying (your puzzle input).

The Elves take turns writing down the number of Calories contained by the various meals, snacks, rations, etc. that
they've brought with them, one item per line. Each Elf separates their own inventory from the previous Elf's
inventory (if any) by a blank line.

For example, suppose the Elves finish writing their items' Calories and end up with the following list:

1000
2000
3000

4000

5000
6000

7000
8000
9000

10000
This list represents the Calories of the food carried by five Elves:

The first Elf is carrying food with 1000, 2000, and 3000 Calories, a total of 6000 Calories.
The second Elf is carrying one food item with 4000 Calories.
The third Elf is carrying food with 5000 and 6000 Calories, a total of 11000 Calories.
The fourth Elf is carrying food with 7000, 8000, and 9000 Calories, a total of 24000 Calories.
The fifth Elf is carrying one food item with 10000 Calories.
In case the Elves get hungry and need extra snacks, they need to know which Elf to ask: they'd like to know how many
Calories are being carried by the Elf carrying the most Calories. In the example above, this is 24000
(carried by the fourth Elf).

Find the Elf carrying the most Calories. How many total Calories is that Elf carrying?
"""


def get_input():
    input = []
    with open('./input.txt', 'r') as my_file:
        for line in my_file:
            input.append(line)
    return input


class Food:
    """
    A Class that represents a food item with Calories
    """

    def __init__(self, calories):
        self.calories = calories


class Elf:
    """
    A Class that represents an Elf with Food
    """

    def __init__(self, food: list):
        self.food = food
        self.sanitize()
        self.sort()
        self.total = self.total_calories()

    def sanitize(self):
        """
        Turn the food list into ints
        :return:
        """
        int_food = []
        for item in self.food:
            int_food.append(int(item))

        self.food = int_food

    def sort(self):
        """
        Sort the list
        :return:
        """
        self.food.sort(reverse=True)

    def total_calories(self):
        """
        Prints the total calories
        :return:
        """
        sum = 0
        for calories in self.food:
            sum += calories

        return sum


class InputParser:
    """
    A Class that parses input to produce Elves and their food
    Returns a list of Elves with their respective Food items
    """

    def __init__(self, input):
        self.input = input
        self.elves = []

    def parse(self):
        """
        Parse an input list
        Blank lines indicate a new Elf
        The items with values indicate that Elf's food list
        :return List of Elves:
        """

        done = False
        while not done:
            food_list = []
            try:
                elf_boundary = self.input.index('\n')
            except ValueError:
                "We're at the end or there are no elf boundaries"
                elf_boundary = len(self.input)

            if elf_boundary == 0:
                # clear this boundary
                self.input.pop(0)
            else:
                for i in range(0, elf_boundary):
                    food_list.append(self.input.pop(0))
                new_elf = Elf(food_list)
                self.elves.append(new_elf)

            if len(self.input) == 0:
                done = True
                # print(len(self.input))


def do_part_one():
    """
    In case the Elves get hungry and need extra snacks,
    they need to know which Elf to ask:
    they'd like to know how many Calories are being carried by the Elf carrying the most Calories.
    In the example above, this is 24000 (carried by the fourth Elf).
    :return:
    """

    input = get_input()

    parser = InputParser(input)
    parser.parse()
    highest_seen = 0
    for elf in parser.elves:
        if elf.total > highest_seen:
            highest_seen = elf.total

    print(f"highest calories: {highest_seen}")  # 67016


def do_part_two():
    """
    By the time you calculate the answer to the Elves' question, they've already realized that the Elf carrying the
    most Calories of food might eventually run out of snacks.
    To avoid this unacceptable situation, the Elves would instead like to know the total Calories carried by the top
    three Elves carrying the most Calories. That way, even if one of those Elves runs out of snacks,
    they still have two backups.

    In the example above, the top three Elves are the fourth Elf (with 24000 Calories), then the third Elf
    (with 11000 Calories), then the fifth Elf (with 10000 Calories). The sum of the Calories carried by these
    three elves is 45000.

    Find the top three Elves carrying the most Calories. How many Calories are those Elves carrying in total?
    :return:
    """

    # Sort the list of elves based on total, sum the top 3

    input = get_input()
    parser = InputParser(input)
    parser.parse()

    totals = []

    for elf in parser.elves:
        totals.append(elf.total)

    totals.sort(reverse=True)

    print(f"Top 3 are: {totals[0], totals[1], totals[2]}")
    print(f"Sum is {totals[0] + totals[1] + totals[2]}")


if __name__ == "__main__":
    do_part_one()
    do_part_two()
