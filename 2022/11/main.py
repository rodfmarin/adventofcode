"""
--- Day 11: Monkey in the Middle ---
As you finally start making your way upriver, you realize your pack is much lighter than you remember. Just then, one
of the items from your pack goes flying overhead. Monkeys are playing Keep Away with your missing things!

To get your stuff back, you need to be able to predict where the monkeys will throw your items. After some careful
observation, you realize the monkeys operate based on how worried you are about each item.

You take some notes (your puzzle input) on the items each monkey currently has, how worried you are about those items,
and how the monkey makes decisions based on your worry level. For example:

Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3
(truncated)
"""
import functools
import operator


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


class Operation:
    """
    An operation performs an arithmetic operation on the worry number
    """

    def __init__(self, operation_string: str, old: int):
        self.operation_string = operation_string
        self.operation = str()
        self.operator = None
        self.first_operand = None
        self.second_operand = None
        self.old = old
        self.new = 0
        self.parse_operation()
        self.ops = None

    def perform_operation(self):
        self.new = self.operator(self.old, self.second_operand)

        return int(self.new)

    def parse_operation(self):
        """
        i.e. new = old * 19
        fill in the value of 'old' with the passed value
        """
        self.ops = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.truediv,
            '%': operator.mod,
            '^': operator.xor,
        }

        tokens = self.operation_string.split()
        self.first_operand = tokens[2]
        self.operator = self.ops[tokens[3]]
        self.second_operand = tokens[4]
        if self.first_operand == "old":
            self.first_operand = self.old
        if self.second_operand == "old":
            self.second_operand = self.old
        if type(self.second_operand == str):
            self.second_operand = int(self.second_operand)


class Test:
    """
    A Test is a textual string that represents a condition
    i.e. 'Divisible by 19'
    if the test statement is true, return true
    if the test statement is false, return false
    """

    def __init__(self, test_string: str, operand: int):
        self.test_string = test_string
        self.operand = operand
        self.operation = None
        self.right_operand = None
        self.parse_test()

    def parse_test(self):
        tokens = self.test_string.split()
        self.operation = tokens[0]
        self.right_operand = tokens[2]

    def perform_test(self):

        if self.operation.lower() == "divisible":
            # get modulus of the operand mod divisor, if 0 it IS divisible by the divisor
            if self.operand % int(self.right_operand) == 0:
                return True
            return False


class Monkey:
    """
    A Monkey has a monkey number (its id)
    A List of Starting Items [79, 98]
    An operation to perform on the worry_number (new = old * 19)
    A Test to perform on the worry number (divisible by 23)
    operations to perform if the test is true or false:
        if true: throw to monkey 2
        if false: throw to monkey 3
    """

    def __init__(self, monkey_number: int, starting_items: [int], operation: str, test: str, true_condition: int,
                 false_condition: int, lcm=0):
        self.monkey_number = monkey_number
        self.starting_items = starting_items
        self.operation = operation
        self.test = test
        # The monkey number to throw to if true or false
        self.true_condition = true_condition
        self.false_condition = false_condition
        self.inspection_count = 0
        self.lcm = lcm
        global monkeys

    def inspect(self):
        # for each item in starting_items, 'inspect' it but before testing it divide the item's value by 3
        # rounded down to nearest integer

        # if items is empty, just return (end the turn)
        if len(self.starting_items) == 0:
            return

        # iterate over starting items and perform a worry operation on it
        while len(self.starting_items) > 0:
            item = self.starting_items.pop(0)
            self.inspection_count += 1

            worry_level = Operation(self.operation, item).perform_operation()
            # In part 1 we divided the worry level by 3
            # worry_level = worry_level // 3
            worry_level = worry_level % lcm
            test = Test(self.test, worry_level).perform_test()

            if test == True:
                monkeys[self.true_condition].starting_items.append(worry_level)
            elif test == False:
                monkeys[self.false_condition].starting_items.append(worry_level)

        # How many inspections have I done?

        print(f"Monkey {self.monkey_number} inspected items {self.inspection_count} times.")


def parse_monkeys(input: [str]):
    """
    Take the input which is multi line
    A Monkey starts after an empty line and ends on the next empty line
    """

    monkeys = []

    # A Monkey in the text input is 6 lines long + a break
    for i in range(0, len(input), 7):
        monkey_number = int(input[i].split(" ")[1].replace(":", ""))
        starting_items = [int(item) for item in input[i + 1].replace("  Starting items: ", "").split(", ")]
        operation = input[i + 2].split(": ")[1]
        test = input[i + 3].split(": ")[1]
        true_condition = int(input[i + 4].split(": ")[1].split(" ")[3])
        false_condition = int(input[i + 5].split(": ")[1].split(" ")[3])

        m = Monkey(monkey_number, starting_items, operation, test, true_condition, false_condition)
        monkeys.append(m)
    return monkeys


def test_operation():
    """
    Test that the Operation class is doing what is expected
    """
    assert 19 == Operation("new = old * 19", old=1).perform_operation()
    assert 6 == Operation("new = old + 5", old=1).perform_operation()
    assert 0 == Operation("new = old + old", old=0).perform_operation()


def test_test():
    """
    test that the Test class is doing what is expected
    """

    assert True == Test(test_string="divisible by 19", operand=19).perform_test()
    assert False == Test(test_string="divisible by 19", operand=20).perform_test()


def test_monkey_parser():
    list = get_input(mode='test')
    monkeys = parse_monkeys(list)

    assert monkeys[0].monkey_number == 0
    assert monkeys[0].starting_items == [79, 98]
    assert monkeys[0].test == "divisible by 23"
    assert monkeys[0].true_condition == 2
    assert monkeys[0].false_condition == 3


def create_lcm(monkeys):
    """
    Create a least common multiple by getting the product of all the divisors in the operation field
    """

    divisor_list = []
    for m in monkeys:
        divisor = int(m.test.split("divisible by ")[1])
        divisor_list.append(divisor)

    lcm = functools.reduce(lambda x, y: x * y, divisor_list)
    return lcm


input = get_input(mode='real')
monkeys = parse_monkeys(input)
lcm = create_lcm(monkeys)
for monkey in monkeys:
    monkey.lcm = lcm


def do_part_one():
    test_operation()
    test_test()
    test_monkey_parser()

    for round in range(20):
        for m in monkeys:
            m.inspect()
    for m in monkeys:
        print(f"Monkey {m.monkey_number} inspected items {m.inspection_count} times.")
    top2 = sorted(monkeys, key=lambda x: x.inspection_count, reverse=True)[0:2]

    monkey_business = top2[0].inspection_count * top2[1].inspection_count
    print(monkey_business)


del monkeys
del lcm
del input
del monkey

input = get_input(mode='test')
monkeys = parse_monkeys(input)
lcm = create_lcm(monkeys)
for monkey in monkeys:
    monkey.lcm = lcm


def do_part_two():
    """
    --- Part Two ---
    You're worried you might not ever get your items back. So worried, in fact, that your relief that a monkey's
    inspection didn't damage an item no longer causes your worry level to be divided by three.

    Unfortunately, that relief was all that was keeping your worry levels from reaching ridiculous levels.
    You'll need to find another way to keep your worry levels manageable.

    At this rate, you might be putting up with these monkeys for a very long time - possibly 10000 rounds!
    """
    # NB: The problem with not dividing the worry level by 3 is that the values get very large very fast
    # The solution is to find the least common multiple by multiplying all the divisors of every monkey
    # With the LCM you can modulo the worry value over this and still perform the same monkey tests without
    # operating on a really large value.

    test_operation()
    test_test()
    test_monkey_parser()

    for round in range(10000):
        for m in monkeys:
            m.inspect()
    for m in monkeys:
        print(f"Monkey {m.monkey_number} inspected items {m.inspection_count} times.")
    top2 = sorted(monkeys, key=lambda x: x.inspection_count, reverse=True)[0:2]

    monkey_business = top2[0].inspection_count * top2[1].inspection_count
    print(monkey_business)


if __name__ == "__main__":
    # I think something is polluting the global scope
    # I get the right answers when running each section separately but a slightly wrong answer when run
    # consecutively
    do_part_one()
    do_part_two()
