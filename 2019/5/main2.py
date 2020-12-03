import csv


class IntCodeComputer:
    """
    A Computer that processes Int Code Instructions
    """

    instruction_pointer = 0

    def __init__(self, program):
        self.program = program

    def do_code_01(self, first_addend, second_addend, output_location):
        """
        Read the value at first_addend location
        Read the value at second_addend location
        Sum these values
        Store the result in output_location
        :param first_addend: int
        :param second_addend: int
        :param output_location: int
        :return: void
        """

        self.program[output_location] = first_addend + second_addend

    def do_code_02(self, multiplier, multiplicand, output_location):
        """
        Read the value at multiplier
        Read the value at multiplicand
        Multiply these values
        Store the result in output_location
        :param multiplier: int
        :param multiplicand: int
        :param output_location: int
        :return: void
        """

        self.program[output_location] = multiplier * multiplicand

    def do_code_03(self, output_location):
        """
        Takes a single integer as input and saves it to the position
        given by its only parameter
        :param input: int
        :param output_location: int
        :return: void
        """

        the_input = input("Please provide an input")
        self.program[output_location] = the_input

    def do_code_04(self, input):
        """
        Outputs the value of its only parameter
        :param input: int
        :return: int
        """
        return self.program[input]

    @staticmethod
    def do_code_99():
        """
        Code 99 is halt
        :return:
        """
        return

    def increment_instruction_pointer(self, step):
        self.instruction_pointer += step
        if self.instruction_pointer > len(self.program):
            return

    def determine_instruction_width(self, starting_position, program):
        """
        At the beginning, start at 0, read the instruction in that position, increment the program counter
        :param starting_position:
        :param program:
        :return:
        """

        if starting_position >= len(self.program) - 1:
            return
        else:
            op = program[starting_position]
            # explode the first element into a 5 digit string
            instruction_set = str(f"{int(op):05d}")

            if instruction_set[-1] == '1' or instruction_set[-1] == '2':
                width = 4
            elif instruction_set[-1] == '3':
                width = 2

            return width

    def parse_instruction(self, block):
        """
        A block is variable length
        the first element in the block is also variable; it can contain up to 5 digits
        Consider this instruction:
            ABCDE
             1002

        Digits D and E from right to left are '02', a multiply instruction
        Digit  C is 0 and indicates the first parameter is in position mode
        Digit  B is 1 and indicates the second parameter is in immediate mode
        :param block: int[]
        :return: dictionary
        """

        # explode the first element into a 5 digit string
        instruction_set = str(f"{int(block[0]):05d}")

        the_operation = str(f"{instruction_set[-2]}{instruction_set[-1]}")

        the_method = f"do_code_{the_operation}"

        # Read parameter modes
        first_parameter_mode = instruction_set[-3]
        second_parameter_mode = instruction_set[-4]
        third_parameter_mode = instruction_set[-5]

        # need to know how many arguments to read and in which mode
        # look at the instruction, look at the modes and gather the values

        if the_operation == '01' or the_operation == '02':
            # three parameters
            if first_parameter_mode == '1':
                first_parameter = int(block[1])
            else:
                first_parameter = self.program[int(block[1])]
            if second_parameter_mode == '1':
                second_parameter = int(block[2])
            else:
                second_parameter = self.program[int(block[2])]

            if third_parameter_mode == '1':
                third_parameter = int(block[3])
            else:
                third_parameter = int(block[3])
                #third_parameter = self.program[int(block[3])]

            return f"self.{the_method}({first_parameter}, {second_parameter}, {third_parameter})", 4

        elif the_operation == '03':
            if first_parameter_mode == '1':
                first_parameter = self.program[int(block[1])]
            else:
                first_parameter = int(block[1])

            return f"self.{the_method}({first_parameter})", 2
        else:
            return f"self.{the_method}()"

    def process_program(self):
        while True:
            width = self.determine_instruction_width(self.instruction_pointer, self.program)
            if width is None:
                return
            the_block = self.program[self.instruction_pointer:self.instruction_pointer+width]
            call = self.parse_instruction(the_block)
            eval(call[0])
            self.increment_instruction_pointer(call[1])


def read_csv(file_name):
    with open(file_name) as f:
        return list(csv.reader(f))


def main():
    # Get the program
    program = read_csv('./input.txt')[0]
    print(f"starting program {program}")
    computer = IntCodeComputer(program)
    computer.process_program()
    print(computer.program)


main()