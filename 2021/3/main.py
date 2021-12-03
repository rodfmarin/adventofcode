"""
--- Day 3: Binary Diagnostic ---
The submarine has been making some odd creaking noises, so you ask it to produce a diagnostic report just in case.

The diagnostic report (your puzzle input) consists of a list of binary numbers which, when decoded properly, can tell
you many useful things about the conditions of the submarine. The first parameter to check is the power consumption.

You need to use the binary numbers in the diagnostic report to generate two new binary numbers
(called the gamma rate and the epsilon rate). The power consumption can then be found by multiplying
the gamma rate by the epsilon rate.

Each bit in the gamma rate can be determined by finding the most common bit in the corresponding position of all
numbers in the diagnostic report. For example, given the following diagnostic report:

00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010

Considering only the first bit of each number, there are five 0 bits and seven 1 bits. Since the most common bit is 1,
the first bit of the gamma rate is 1.

The most common second bit of the numbers in the diagnostic report is 0, so the second bit of the gamma rate is 0.

The most common value of the third, fourth, and fifth bits are 1, 1, and 0, respectively,
and so the final three bits of the gamma rate are 110.

So, the gamma rate is the binary number 10110, or 22 in decimal.

The epsilon rate is calculated in a similar way; rather than use the most common bit, the least common bit from each
position is used. So, the epsilon rate is 01001, or 9 in decimal.
Multiplying the gamma rate (22) by the epsilon rate (9) produces the power consumption, 198.

Use the binary numbers in your diagnostic report to calculate the gamma rate and epsilon rate,
then multiply them together. What is the power consumption of the submarine?
(Be sure to represent your answer in decimal, not binary.)
"""
"""
--- Part Two ---
Next, you should verify the life support rating, which can be determined by multiplying the oxygen generator
rating by the CO2 scrubber rating.

Both the oxygen generator rating and the CO2 scrubber rating are values that can be found in your diagnostic report - 
finding them is the tricky part. Both values are located using a similar process that involves filtering out values 
until only one remains. Before searching for either rating value, start with the full list of binary numbers from 
your diagnostic report and consider just the first bit of those numbers. Then:

Keep only numbers selected by the bit criteria for the type of rating value for which you are searching. 
Discard numbers which do not match the bit criteria.
If you only have one number left, stop; this is the rating value for which you are searching.
Otherwise, repeat the process, considering the next bit to the right.
The bit criteria depends on which type of rating value you want to find:

To find oxygen generator rating, determine the most common value (0 or 1) in the current bit position, and keep only 
numbers with that bit in that position. If 0 and 1 are equally common, keep values with a 1 in the position being 
considered.

To find CO2 scrubber rating, determine the least common value (0 or 1) in the current bit position, and keep only 
numbers with that bit in that position. If 0 and 1 are equally common, keep values with a 0 in the position being
considered.
For example, to determine the oxygen generator rating value using the same example diagnostic report from above:

Start with all 12 numbers and consider only the first bit of each number. There are more 1 bits (7) than 0 bits (5), 
so keep only the 7 numbers with a 1 in the first position: 11110, 10110, 10111, 10101, 11100, 10000, and 11001.
Then, consider the second bit of the 7 remaining numbers: there are more 0 bits (4) than 1 bits (3), so keep only the 4
numbers with a 0 in the second position: 10110, 10111, 10101, and 10000.
In the third position, three of the four numbers have a 1, so keep those three: 10110, 10111, and 10101.
In the fourth position, two of the three numbers have a 1, so keep those two: 10110 and 10111.
In the fifth position, there are an equal number of 0 bits and 1 bits (one each). So, to find the oxygen generator
rating, keep the number with a 1 in that position: 10111.
As there is only one number left, stop; the oxygen generator rating is 10111, or 23 in decimal.
Then, to determine the CO2 scrubber rating value from the same example above:

Start again with all 12 numbers and consider only the first bit of each number. There are fewer 0 bits (5) than 1 bits 
(7), so keep only the 5 numbers with a 0 in the first position: 00100, 01111, 00111, 00010, and 01010.
Then, consider the second bit of the 5 remaining numbers: there are fewer 1 bits (2) than 0 bits (3), so keep only the 
2 numbers with a 1 in the second position: 01111 and 01010.
In the third position, there are an equal number of 0 bits and 1 bits (one each). So, to find the CO2 scrubber rating, 
keep the number with a 0 in that position: 01010.
As there is only one number left, stop; the CO2 scrubber rating is 01010, or 10 in decimal.
Finally, to find the life support rating, multiply the oxygen generator rating (23) by the CO2 scrubber rating (10) to 
get 230.

Use the binary numbers in your diagnostic report to calculate the oxygen generator rating and CO2 scrubber rating, 
then multiply them together. What is the life support rating of the submarine? (Be sure to represent your answer in 
decimal, not binary.)
"""


input = []
with open('input.txt') as my_file:
    for line in my_file:
        input.append(line)


def string_to_decimal(string):
    """
    Convert a binary string to decimal
    :param string:
    :return:
    """
    return int(string, 2)


def filter_array_for_oxygen_reading(array, index=0):
    """
    To find oxygen generator rating,
    determine the most common value (0 or 1) in the current bit position,
    and keep only numbers with that bit in that position.
    If 0 and 1 are equally common, keep values with a 1 in the position being considered.
    :param array:
    :param index:
    :return:
    """

    ones = 0
    zeroes = 0
    new_array = []

    # if index > bit_width:
    #     return

    if len(array) == 1:
        return array

    for item in array:
        if item[index] == "0":
            zeroes += 1
        elif item[index] == "1":
            ones += 1

    if ones >= zeroes:
        for item in array:
            if item[index] == "1":
                new_array.append(item)
    elif zeroes > ones:
        for item in array:
            if item[index] == "0":
                new_array.append(item)

    index += 1

    return filter_array_for_oxygen_reading(new_array, index)


def filter_array_for_co2_reading(array, index=0):
    """
    To find c02 scrubber rating,
    determine the lease common value (0 or 1) in the current bit position,
    and keep only numbers with that bit in that position.
    If 0 and 1 are equally common, keep values with a 0 in the position being considered.
    :param array:
    :param index:
    :return:
    """

    ones = 0
    zeroes = 0
    new_array = []

    if len(array) == 1:
        return array

    for item in array:
        if item[index] == "0":
            zeroes += 1
        elif item[index] == "1":
            ones += 1

    if zeroes <= ones:
        for item in array:
            if item[index] == "0":
                new_array.append(item)
    elif ones < zeroes:
        for item in array:
            if item[index] == "1":
                new_array.append(item)

    index += 1

    return filter_array_for_co2_reading(new_array, index)


class Tabulator:
    def __init__(self, bit_width):
        self.bit_width = bit_width
        self.zeroes = [0] * self.bit_width
        self.ones = [0] * self.bit_width
        self.most_common_bit_string = ""
        self.least_common_bit_string = ""
        self.gamma_value = 0
        self.epsilon_value = 0

    def add_one(self, index):
        """
        We found a one in the given index, increment the value at the index
        :param index:
        :return:
        """
        self.ones[index] += 1

    def add_zero(self, index):
        """
        We found a zero in the given index, increment the value at the index
        :param index:
        :return:
        """
        self.zeroes[index] += 1

    def get_most_common_bit(self):
        """
        Compare ones vs zeroes and construct a string that contains the winner
        :return:
        """

        for i in range(self.bit_width):
            if self.zeroes[i] > self.ones[i]:
                # zeroes win
                # what if they're equal :O
                self.most_common_bit_string += "0"
            elif self.ones[i] > self.zeroes[i]:
                # ones win
                self.most_common_bit_string += "1"

    def get_least_common_bit(self):
        """
        Must be run after get_most_common
        :return:
        """

        # Do a bit flip of the most common to get least common
        for char in self.most_common_bit_string:
            if char == "1":
                self.least_common_bit_string += "0"
            elif char == "0":
                self.least_common_bit_string += "1"

    def get_gamma_value(self):
        """
        Take the most common bits string and find the gamma value
        :return:
        """
        self.gamma_value = string_to_decimal(self.most_common_bit_string)

    def get_epsilon_value(self):
        """
        Take the least common bits string and find the epsilon value
        :return:
        """
        self.epsilon_value = string_to_decimal(self.least_common_bit_string)

    def calculate_power_consumption(self):
        """
        Multiply gamma by epsilon to return power consumption rate
        :return:
        """

        self.get_gamma_value()
        self.get_epsilon_value()

        return self.gamma_value * self.epsilon_value


def do_part_one():
    # what we're doing here is evaluating which bit is the most common in each index position.
    # for example in a two number diagnostic:
    # 01
    # 01
    # The most common bit in position 1 is 0
    # The least common would be 1 and in position 2 the most common would be 1.

    tabulator = Tabulator(bit_width=12)
    for line in input:
        for i in range(len(line)):
            if line[i] == "0":
                tabulator.add_zero(i)
            elif line[i] == "1":
                tabulator.add_one(i)

    tabulator.get_most_common_bit()
    tabulator.get_least_common_bit()
    print(tabulator.calculate_power_consumption())


def do_part_two():
    # Similar to the first though this time we're filtering out numbers in the list based on who wins (or loses)
    # the bit popularity contest.
    # we're looking to provide a life support rating by finding the oxygen generator rating and  C02 scrubber rating.

    oxygen = str(filter_array_for_oxygen_reading(input)[0])
    co2 = str(filter_array_for_co2_reading(input)[0])

    oxygen = string_to_decimal(oxygen)
    co2 = string_to_decimal(co2)
    print(oxygen * co2)


if __name__ == '__main__':
    do_part_one()
    do_part_two()
