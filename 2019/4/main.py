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


def password_filter(number):
    """
    Using the rules, does a number pass through the filter
    :param number: a six digit number
    :return: True|False
    """

    number_list = [int(d) for d in str(number)]

    # having a list of numbers, starting at the beginning check for doubles

    double_digits = False
    for index, digit in enumerate(number_list):
        if index < len(number_list) - 1:
            if number_list[index] == number_list[index+1]:
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