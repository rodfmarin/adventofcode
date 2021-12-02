"""
--- Day 2: Dive! ---
Now, you need to figure out how to pilot this thing.

It seems like the submarine can take a series of commands like forward 1, down 2, or up 3:

forward X increases the horizontal position by X units.
down X increases the depth by X units.
up X decreases the depth by X units.
Note that since you're on a submarine, down and up affect your depth, and so they have the opposite result of what
you might expect.

The submarine seems to already have a planned course (your puzzle input). You should probably figure out where it's
going. For example:

forward 5
down 5
forward 8
up 3
down 8
forward 2
Your horizontal position and depth both start at 0. The steps above would then modify them as follows:

forward 5 adds 5 to your horizontal position, a total of 5.
down 5 adds 5 to your depth, resulting in a value of 5.
forward 8 adds 8 to your horizontal position, a total of 13.
up 3 decreases your depth by 3, resulting in a value of 2.
down 8 adds 8 to your depth, resulting in a value of 10.
forward 2 adds 2 to your horizontal position, a total of 15.
After following these instructions, you would have a horizontal position of 15 and a depth of 10.
(Multiplying these together produces 150.)

Calculate the horizontal position and depth you would have after following the planned course.
What do you get if you multiply your final horizontal position by your final depth?


--- Part Two ---
Based on your calculations, the planned course doesn't seem to make any sense. You find the submarine
manual and discover that the process is actually slightly more complicated.

In addition to horizontal position and depth, you'll also need to track a third value, aim,
which also starts at 0. The commands also mean something entirely different than you first thought:

down X increases your aim by X units.
up X decreases your aim by X units.
forward X does two things:
It increases your horizontal position by X units.
It increases your depth by your aim multiplied by X.
Again note that since you're on a submarine, down and up do the opposite of what you might expect:
"down" means aiming in the positive direction.

Now, the above example does something different:

forward 5 adds 5 to your horizontal position, a total of 5. Because your aim is 0, your depth does not change.
down 5 adds 5 to your aim, resulting in a value of 5.
forward 8 adds 8 to your horizontal position, a total of 13. Because your aim is 5, your depth increases by 8*5=40.
up 3 decreases your aim by 3, resulting in a value of 2.
down 8 adds 8 to your aim, resulting in a value of 10.
forward 2 adds 2 to your horizontal position, a total of 15. Because your aim is 10, your depth increases by 2*10=20 to a total of 60.
After following these new instructions, you would have a horizontal position of 15 and a depth of 60. (Multiplying these produces 900.)

Using this new interpretation of the commands, calculate the horizontal position and depth you would have after following the
planned course. What do you get if you multiply your final horizontal position by your final depth?

"""


# I think we model a submarine class
# We instantiate a sub and for each instruction in the input we modify the sub's state
# Sub can have a move_'direction' method that takes a value and updates the internal state according to the rules above.

class Submarine:
    def __init__(self, h_pos, v_pos):
        self.h_pos = h_pos
        self.v_pos = v_pos

    def move_forward(self, value):
        """
        update the sub's h_pos state by 'value'
        :param value:
        :return:
        """
        self.h_pos += value

    def move_down(self, value):
        """
        update the sub's v_pos state by value, down increases the v_pos depth
        :param value:
        :return:
        """
        self.v_pos += value

    def move_up(self, value):
        """
        update the sub's v_pos state by value, up decreases the v_pos depth
        :param value:
        :return:
        """
        self.v_pos -= value


# For part two we need to model a different type of Sub
# There's now an aim value we need to track, and moving in certain ways updates values according to some rules
# down X increases your aim by X units.
# up X decreases your aim by X units.
# forward X does two things:
# It increases your horizontal position by X units.
# It increases your depth by your aim multiplied by X.
class SubmarineTwo:
    def __init__(self, h_pos, v_pos, aim):
        self.h_pos = h_pos
        self.v_pos = v_pos
        self.aim = aim

    def move_forward(self, value):
        """
        update the sub's h_pos state by 'value'
        :param value:
        :return:
        """
        self.h_pos += value
        self.v_pos += (value * self.aim)

    def move_down(self, value):
        """
        update the sub's v_pos state by value, down increases the v_pos depth
        :param value:
        :return:
        """
        self.aim += value

    def move_up(self, value):
        """
        update the sub's v_pos state by value, up decreases the v_pos depth
        :param value:
        :return:
        """
        self.aim -= value

input = []
with open('input.txt') as my_file:
    for line in my_file:
        input.append(line)


def do_part_one():
    # Create a blank sub
    submarine = Submarine(h_pos=0, v_pos=0)

    # iterate over our move list
    for item in input:
        move = item.strip().split(" ")[0]
        value = int(item.strip().split(" ")[1])
        method_name = f"move_{move}"
        move_func = getattr(submarine, method_name)
        move_func(value)

    # calculate the final ask, what do you get after following your course when you
    # multiply your h_pos * v_pos

    print(submarine.h_pos * submarine.v_pos)


def do_part_two():
    # Create a blank subTwo
    submarine = SubmarineTwo(h_pos=0, v_pos=0, aim=0)

    # iterate over our move list
    for item in input:
        move = item.strip().split(" ")[0]
        value = int(item.strip().split(" ")[1])
        method_name = f"move_{move}"
        move_func = getattr(submarine, method_name)
        move_func(value)

    # calculate the final ask, what do you get after following your course when you
    # multiply your h_pos * v_pos

    print(submarine.h_pos * submarine.v_pos)


if __name__ == '__main__':
    do_part_one()
    do_part_two()


