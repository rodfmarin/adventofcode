"""
--- Day 4: Secure Container ---
You arrive at the Venus fuel depot only to discover it's protected by a password. The Elves had written the password on
a sticky note, but someone threw it out.

However, they do remember a few key facts about the password:

It is a six-digit number.
The value is within the range given in your puzzle input.
Two adjacent digits are the same (like 22 in 122345).
Going from left to right, the digits never decrease; they only ever increase or stay the same (like 111123 or 135679).
Other than the range rule, the following are true:

111111 meets these criteria (double 11, never decreases).
223450 does not meet these criteria (decreasing pair of digits 50).
123789 does not meet these criteria (no double).
How many different passwords within the range given in your puzzle input meet these criteria?

Your puzzle input is 271973-785961.

"""

# NB: There's probably several solutions within a boundary of 0 + 100,000
#   that are multiplied for every 100,000 under 785,961
#   the 'edges' are between        271973      -> 300000
#                              and 700,000     -> 785961
#

# NB: Update, just used an algorithm, a stack and recursion to check digits

THE_RANGE = range(271973, 785961+1)


def number_stack(number):
    the_number = number
    the_stack = []
    for digit in reversed((str(the_number))):
        the_stack.append(digit)
    return the_stack


def test_stack(stack, previous_digit=0):
    if len(stack) == 0:
        return True
    else:
        first = int(stack.pop())
        second = int(stack.pop())
        if (first <= second) and (first >= previous_digit):
            return test_stack(stack, second)
        else:
            return False


def make_number_map(number):
    number_map = {}

    for digit in str(number):
        if number_map.get(digit):
            number_map[digit] += 1
        else:
            number_map[digit] = 1
    return number_map


def double_digits_check(number):
    """
    For day 4.b, the additional constraint:
    An Elf just remembered one more important detail: the two adjacent matching digits are not part of a larger group of matching digits.

    Given this additional criterion, but still ignoring the range rule, the following are now true:

    112233 meets these criteria because the digits never decrease and all repeated digits are exactly two digits long.
    123444 no longer meets the criteria (the repeated 44 is part of a larger group of 444).
    111122 meets the criteria (even though 1 is repeated more than twice, it still contains a double 22).
    How many different passwords within the range given in your puzzle input meet all of the criteria?
    :param number:
    :return: True|False
    """

    # NB: How to approach?
    #   do we just keep track of every digit seen in the number?
    #   i.e.
    #   |0|1|2|3|4|5|6|7|8|9|
    #   |0|2|2|2|0|0|0|0|0|0|
    #   If a number is seen more than once it is >1
    #   if there is a number that is >1 but >2 then it does not meet the criteria; throw it out
    #   if there are multiple numbers seen more than once the larger value set must only be = 2
    #

    number_map = make_number_map(number)
    greater_than_one = {k: v for (k, v) in number_map.items() if v >= 2}

    delete_list = []
    for item in greater_than_one.items():
        # how many digits do we have that appear more than once
        if item[1] > 2:
            delete_list.append(item[0])

    for key in delete_list:
        del greater_than_one[key]

    if 0 < len(greater_than_one):
        highest_seen = 0

        for item in greater_than_one.items():
            if item[1] > int(highest_seen):
                highest_seen = item[0]

        if greater_than_one[str(highest_seen[0])] == 2:
            return True

    return False


def password_filter(number):
    """
    Using the rules, does a number pass through the filter
    :param number: a six digit number
    :return: True|False
    """

    number_list = [int(d) for d in str(number)]

    # having a list of numbers, starting at the beginning check for (valid) doubles

    double_digits = False
    if double_digits_check(number):
        double_digits = True

    s = number_stack(number)

    if test_stack(s):
        same_or_incrementing = True
    else:
        same_or_incrementing = False

    if double_digits and same_or_incrementing:
        return True


def main():
    list = []
    for number in THE_RANGE:
        if password_filter(number):
            print(f"passed check {number}")
            list.append(number)

    print(len(list))


main()