"""
--- Day 1: Trebuchet?! ---
Something is wrong with global snow production, and you've been selected to take a look. The Elves have even given
you a map; on it, they've used stars to mark the top fifty locations that are likely to be having problems.

You've been doing this long enough to know that to restore snow operations, you need to check all fifty stars by
December 25th.

Collect stars by solving puzzles. Two puzzles will be made available on each day in the Advent calendar; the second
puzzle is unlocked when you complete the first. Each puzzle grants one star. Good luck!

You try to ask why they can't just use a weather machine ("not powerful enough") and where they're even sending you
("the sky") and why your map looks mostly blank ("you sure ask a lot of questions") and hang on did you just say the
sky ("of course, where do you think snow comes from") when you realize that the Elves are already loading you into a
trebuchet ("please hold still, we need to strap you in").

As they're making the final adjustments, they discover that their calibration document (your puzzle input) has been
amended by a very young Elf who was apparently just excited to show off her art skills. Consequently, the Elves are
having trouble reading the values on the document.

The newly-improved calibration document consists of lines of text; each line originally contained a specific
calibration value that the Elves now need to recover. On each line, the calibration value can be found by combining
the first digit and the last digit (in that order) to form a single two-digit number.

For example:

1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
In this example, the calibration values of these four lines are 12, 38, 15, and 77. Adding these together produces 142.

Consider your entire calibration document. What is the sum of all of the calibration values?
"""
from pprint import pprint


def get_input():
    input = []
    with open('./input.txt', 'r') as my_file:
        for line in my_file:
            input.append(line)
    return input


def do_part_one():
    """
    For each line, walk the line looking for the first int
    when found break
    then walk backward and find the first int
    when found break
    Store the ints to add
    return the sum
    """
    lines = get_input()
    to_sum = []
    total = 0
    for line in lines:
        pair = []
        for char in line:
            if char.isdigit():
                pair.append(char)
                break
        for char in reversed(line):
            if char.isdigit():
                pair.append(char)
                break
        sb = ""
        for p in pair:
            sb += p
        to_sum.append(sb)
    print(to_sum)
    for item in to_sum:
        total += int(item)
    print(total)


Numbers = {
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9
}


def find_all_substrings(string, substring):
    """Get the indicies of all occurences of substring in string"""
    indices = []
    i = 0
    while i < len(string):
        j = string.find(substring, i)
        if j == -1:
            break
        indices.append(j)
        i = j + len(substring)
    return indices


def find_indices_of_all_num_occurrences(string: str, substring: str):
    """
    for each number in the numbers list
    if it occurs in the string
        keep searching, increasing the index to search after the length of the string until you can't find it
        the first hit should be recorded
        the last hit should be recorded

    """
    return find_all_substrings(string, substring)

def do_part_two():
    """
    Your calculation isn't quite right. It looks like some of the digits are actually spelled out with letters:
    one, two, three, four, five, six, seven, eight, and nine also count as valid "digits".

    Equipped with this new information, you now need to find the real first and last digit on each line. For example:

    two1nine
    eightwothree
    abcone2threexyz
    xtwone3four
    4nineeightseven2
    zoneight234
    7pqrstsixteen
    In this example, the calibration values are 29, 83, 13, 24, 42, 14, and 76. Adding these together produces 281.


    """

    # You almost have to find all the indexes of each occurrence of digits and all words
    # Then compare who is the most forward and most aft
    # Those are the digits to sum

    lines = get_input()
    ranking = []

    for line in lines:
        lowest_seen = {"num": "", "index": 1000000000000}
        highest_seen = {"num": "", "index": 0}
        data = {}
        for num in Numbers:
            indices = find_indices_of_all_num_occurrences(line, num)
            indices_numerical = find_indices_of_all_num_occurrences(line, str(Numbers[num]))
            all_indices = indices + indices_numerical
            if all_indices:
                for i in all_indices:
                    if i <= lowest_seen["index"]:
                        lowest_seen["num"] = num
                        lowest_seen["index"] = i
                    if i >= highest_seen["index"]:
                        highest_seen["num"] = num
                        highest_seen["index"] = i
                data["line"] = line.strip()
                data[num] = all_indices
                data["highest"] = highest_seen
                data["lowest"] = lowest_seen
        ranking.append(data)

    pprint(ranking)

    total = 0
    # for line in ranking:
    for line in ranking:
        lowest = Numbers[line["lowest"]["num"]]
        highest = Numbers[line["highest"]["num"]]
        digits = int(str(lowest)+str(highest))
        print(digits)
        total += digits

    print(total)




if __name__ == "__main__":
    do_part_one()
    do_part_two()
