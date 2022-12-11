"""
--- Day 10: Cathode-Ray Tube ---
You avoid the ropes, plunge into the river, and swim to shore.

The Elves yell something about meeting back up with them upriver, but the river is too loud to tell exactly what
they're saying. They finish crossing the bridge and disappear from view.

Situations like this must be why the Elves prioritized getting the communication system on your handheld device
working. You pull it out of your pack, but the amount of water slowly draining from a big crack in its screen tells you
it probably won't be of much immediate use.

Unless, that is, you can design a replacement for the device's video system! It seems to be some kind of cathode-ray
tube screen and simple CPU that are both driven by a precise clock circuit. The clock circuit ticks at a constant rate;
each tick is called a cycle.

Start by figuring out the signal being sent by the CPU. The CPU has a single register, X, which starts with the
value 1. It supports only two instructions:

addx V takes two cycles to complete. After two cycles, the X register is increased by the value V. (V can be negative.)
noop takes one cycle to complete. It has no other effect.
The CPU uses these instructions in a program (your puzzle input) to, somehow, tell the screen what to draw.

Consider the following small program:

noop
addx 3
addx -5
Execution of this program proceeds as follows:

At the start of the first cycle, the noop instruction begins execution. During the first cycle, X is 1. After the first
cycle, the noop instruction finishes execution, doing nothing.
At the start of the second cycle, the addx 3 instruction begins execution. During the second cycle, X is still 1.
During the third cycle, X is still 1. After the third cycle, the addx 3 instruction finishes execution, setting X to 4.
At the start of the fourth cycle, the addx -5 instruction begins execution. During the fourth cycle, X is still 4.
During the fifth cycle, X is still 4. After the fifth cycle, the addx -5 instruction finishes execution, setting X
to -1.
Maybe you can learn something by looking at the value of the X register throughout execution. For now, consider the
signal strength (the cycle number multiplied by the value of the X register) during the 20th cycle and every 40 cycles
after that (that is, during the 20th, 60th, 100th, 140th, 180th, and 220th cycles).

For example, consider this larger program:
(program removed for brevity)
The interesting signal strengths can be determined as follows:

During the 20th cycle, register X has the value 21, so the signal strength is 20 * 21 = 420.
(The 20th cycle occurs in the middle of the second addx -1, so the value of register X is the starting value, 1, plus
all of the other addx values up to that point: 1 + 15 - 11 + 6 - 3 + 5 - 1 - 8 + 13 + 4 = 21.)
During the 60th cycle, register X has the value 19, so the signal strength is 60 * 19 = 1140.
During the 100th cycle, register X has the value 18, so the signal strength is 100 * 18 = 1800.
During the 140th cycle, register X has the value 21, so the signal strength is 140 * 21 = 2940.
During the 180th cycle, register X has the value 16, so the signal strength is 180 * 16 = 2880.
During the 220th cycle, register X has the value 18, so the signal strength is 220 * 18 = 3960.
The sum of these signal strengths is 13140.

Find the signal strength during the 20th, 60th, 100th, 140th, 180th, and 220th cycles. What is the sum of
these six signal strengths?
"""


def get_input():
    input = []
    with open('input.txt', 'r') as my_file:
        for line in my_file:
            line = line.replace("\n", "")
            input.append(line)
    return input


class Instruction:
    """
    A Class that represents an Instruction processed by the CPU
    """

    def __init__(self, cycles: int, value: int):
        self.cycles = cycles
        self.value = value

    @staticmethod
    def parse_instruction(input: str):
        tokens = input.split()
        if tokens[0] == "noop":
            return Instruction(1, 0)
        elif tokens[0] == 'addx':
            return Instruction(2, int(tokens[1]))

    @staticmethod
    def parse_instructions(input: [str]) -> ['Instruction']:
        instructions = []
        for line in input:
            instructions.append(Instruction.parse_instruction(line))
        return instructions


class CRT:
    """
    Represent a 40 char X 6 display
    """
    def __init__(self):
        self.pixels = ['.'] * 240

    def __str__(self):
        # 'Display' the CRT
        the_display = str()

        for i, p in enumerate(self.pixels):
            if i > 0 and (i+1) % 40 == 0:
                the_display += p + '\n'
            else:
                the_display += p

        return the_display

    def draw_pixel(self, cycle: int, x_register: int):
        # cycle is where we are in the index of the screen and is 0 based while cycle is 1 based
        # x_register and x_register -1 and x_register +1 is the sprite horiz pos
        # if cycle is the same as any of those positions then draw that pixel
        # cycle needs modulo around 40 because instead of being contiguous
        # the challenge wants you to use an array of arrays
        # but we need to actually update the correct index on the screen

        char_pos = cycle
        if cycle > 40:
            cycle = cycle % 40
        if cycle - 1 in [x_register - 1, x_register, x_register + 1]:
            self.pixels[char_pos-1] = "#"


class CPU:
    """
    A Class that represents a CPU
    """
    def __init__(self, program: [Instruction]):
        self.program = program
        self.x = 1
        self.next_cycle = 1
        self.cycles_remaining = self.program[0].cycles
        self.current_instruction = program[0]
        self.current_instruction_idx = 0
        self.crt = CRT()

    def load_next_instruction(self):
        if self.current_instruction_idx < len(self.program) + 1:
            self.current_instruction_idx += 1
            self.current_instruction = self.program[self.current_instruction_idx]
            self.cycles_remaining = self.current_instruction.cycles

    def tick(self):
        self.crt.draw_pixel(self.next_cycle, self.x)
        self.cycles_remaining -= 1
        # we're at the end of the cycle
        if self.cycles_remaining <= 0:
            self.x = self.current_instruction.value + self.x
            self.load_next_instruction()
        self.next_cycle += 1


def do_part_one():
    input = get_input()
    instructions = Instruction.parse_instructions(input)
    cpu = CPU(instructions)
    score = 0
    while cpu.next_cycle < 220:
        cpu.tick()
        if cpu.next_cycle == 20 or (cpu.next_cycle + 20) % 40 == 0:
            score += cpu.next_cycle * cpu.x
            print(f"Counter {cpu.next_cycle} | Score {score}")


def do_part_two():
    """
    --- Part Two ---
    It seems like the X register controls the horizontal position of a sprite. Specifically, the sprite is 3 pixels
    wide, and the X register sets the horizontal position of the middle of that sprite.
    (In this system, there is no such thing as "vertical position": if the sprite's horizontal position puts its pixels
    where the CRT is currently drawing, then those pixels will be drawn.)

    You count the pixels on the CRT: 40 wide and 6 high. This CRT screen draws the top row of pixels left-to-right,
    then the row below that, and so on. The left-most pixel in each row is in position 0, and the right-most pixel in
    each row is in position 39.

    Like the CPU, the CRT is tied closely to the clock circuit: the CRT draws a single pixel during each cycle.
    Representing each pixel of the screen as a #, here are the cycles during which the first and last pixel in each
    row are drawn:

    Cycle   1 -> ######################################## <- Cycle  40
    Cycle  41 -> ######################################## <- Cycle  80
    Cycle  81 -> ######################################## <- Cycle 120
    Cycle 121 -> ######################################## <- Cycle 160
    Cycle 161 -> ######################################## <- Cycle 200
    Cycle 201 -> ######################################## <- Cycle 240
    So, by carefully timing the CPU instructions and the CRT drawing operations, you should be able to determine
    whether the sprite is visible the instant each pixel is drawn. If the sprite is positioned such that one of its
    three pixels is the pixel currently being drawn, the screen produces a lit pixel (#); otherwise, the screen leaves
    the pixel dark (.).

    The first few pixels from the larger example above are drawn as follows:
    """

    """
    Each cycle the CRT is drawing in the pixel position that matches the pixel index in the graphic above
    e.g. in cycle 1 the crt is drawing where pixel 1 is
    
    The X register controls the horiz pos of a sprite
    a sprite is 3 pixels wide.  The x register sets horizontal position of the MIDDLE of that sprite
    if the sprite's horiz pos puts its pixels where the crt is CURRENTLY DRAWING, then those pixels  will be drawn
    
    If the sprite is positioned such that one of its three pixels is the pixel currently being drawn, 
    the screen produces a lit pixel (#); otherwise, the screen leaves the pixel dark (.).
    """
    input = get_input()
    instructions = Instruction.parse_instructions(input)
    cpu = CPU(instructions)

    while cpu.next_cycle < 240:
        cpu.tick()
    print(cpu.crt)


if __name__ == "__main__":
    do_part_one()
    do_part_two()