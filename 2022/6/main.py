"""
--- Day 6: Tuning Trouble ---
The preparations are finally complete; you and the Elves leave camp on foot and begin to make your way toward the star
fruit grove.

As you move through the dense undergrowth, one of the Elves gives you a handheld device. He says that it has many fancy
features, but the most important one to set up right now is the communication system.

However, because he's heard you have significant experience dealing with signal-based systems, he convinced the other
Elves that it would be okay to give you their one malfunctioning device - surely you'll have no problem fixing it.

As if inspired by comedic timing, the device emits a few colorful sparks.

To be able to communicate with the Elves, the device needs to lock on to their signal. The signal is a series of
seemingly-random characters that the device receives one at a time.

To fix the communication system, you need to add a subroutine to the device that detects a start-of-packet marker in
the datastream. In the protocol being used by the Elves, the start of a packet is indicated by a sequence of four
characters that are all different.

The device will send your subroutine a datastream buffer (your puzzle input); your subroutine needs to identify the
first position where the four most recently received characters were all different. Specifically, it needs to report
the number of characters from the beginning of the buffer to the end of the first such four-character marker.

For example, suppose you receive the following datastream buffer:

mjqjpqmgbljsphdztnvjfqwrcgsmlb
After the first three characters (mjq) have been received, there haven't been enough characters received yet to find
the marker. The first time a marker could occur is after the fourth character is received, making the most recent four
characters mjqj. Because j is repeated, this isn't a marker.

The first time a marker appears is after the seventh character arrives. Once it does, the last four characters received
are jpqm, which are all different. In this case, your subroutine should report the value 7, because the first
start-of-packet marker is complete after 7 characters have been processed.

Here are a few more examples:

bvwbjplbgvbhsrlpgdmjqwftvncz: first marker after character 5
nppdvjthqldpwncqszvftbrmjlhg: first marker after character 6
nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg: first marker after character 10
zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw: first marker after character 11
How many characters need to be processed before the first start-of-packet marker is detected?
"""


def get_input():
    input = []
    with open('./input.txt', 'r') as my_file:
        for line in my_file:
            line = line.replace("\n", "")
            input.append(line)
    return input


class CommunicatorReceiver:
    """
    A Device that receives Elf communications through a data stream
    example stream: bvwbjplbgvbhsrlpgdmjqwftvncz
    """
    def __init__(self, data_stream):
        self.data_stream = data_stream
        self.char_list = []
        self.start_of_packet = 0
        self.start_of_message = 0
        self.explode_stream()
        self.find_start_of_packet()
        self.find_start_of_message()

    def explode_stream(self):
        """
        Turn the stream into a list of chars
        """
        self.char_list = [letter for letter in self.data_stream]
        self.char_list.reverse()

    def find_start_of_packet(self):
        """
        first position where the four most recently received characters were all different.
        Specifically, it needs to report the number of characters from the beginning of the buffer to the end of the
        first such four-character marker.
        """

        step_counter = 0
        local_char_list = self.char_list[:]

        for i in range(len(local_char_list)):
            c = local_char_list.pop()
            step_counter += 1
            compare_list = [c, local_char_list[-1], local_char_list[-2], local_char_list[-3]]
            if self.is_unique(compare_list):
                self.start_of_packet = (step_counter + 3)
                break

    def find_start_of_message(self):
        """
        A start-of-message marker is just like a start-of-packet marker, except it consists of 14 distinct characters
        rather than 4.
        """
        step_counter = 0
        local_char_list = self.char_list[:]

        for i in range(len(local_char_list)):
            c = local_char_list.pop()
            step_counter += 1
            compare_list = []
            compare_list.append(c)
            for j in range(1, 14):
                compare_list.append(local_char_list[-j])
            if self.is_unique(compare_list):
                self.start_of_message = (step_counter + 13)
                break

    @classmethod
    def is_unique(cls, chars: list):
        """
        If the list contains no repeating chars it is unique
        """

        compare_list = []
        for char in chars:
            if char in compare_list:
                return False
            compare_list.append(char)

        return True


def do_part_one():
    # How many characters need to be processed before the first start-of-packet marker is detected?

    input = get_input()
    for line in input:
        cr = CommunicatorReceiver(data_stream=line)
        print(cr.start_of_packet)


def do_part_two():
    """
    --- Part Two ---
    Your device's communication system is correctly detecting packets, but still isn't working. It looks like it also
    needs to look for messages.

    A start-of-message marker is just like a start-of-packet marker, except it consists of 14 distinct characters
    rather than 4.

    Here are the first positions of start-of-message markers for all of the above examples:

    mjqjpqmgbljsphdztnvjfqwrcgsmlb: first marker after character 19
    bvwbjplbgvbhsrlpgdmjqwftvncz: first marker after character 23
    nppdvjthqldpwncqszvftbrmjlhg: first marker after character 23
    nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg: first marker after character 29
    zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw: first marker after character 26
    """
    # How many characters need to be processed before the first start-of-message marker is detected?
    input = get_input()
    for line in input:
        cr = CommunicatorReceiver(data_stream=line)
        print(cr.start_of_message)


if __name__ == "__main__":
    do_part_one()
    do_part_two()
