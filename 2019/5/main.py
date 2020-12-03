import csv


class IntCodeComputer:

    def __init__(self, program):
        self.OPCODES = {
            "1": "+",
            "2": "*",
            "3": "",
            "99": "None"
        }

        self.program = program
        self.current_position = 0
        self.current_operation = None
        self.calculated_value = 0
        self.current_opcode = 0

    def process_program(self):
        """
        The program is a comma seperated list of numbers
        Start at position 0
        check opcode
        perform operation on numbers given in position 1 and 2
        place value in position 3
        move forward 4 positions
        if opcode is 99, terminate
        if opcode is unrecognized, something has gone wrong
        repeat
        """

        while self.current_opcode != 99:
            self.process_block()

    def process_block(self):
        """
        start at the current_position
        read the opcode
        perform the operation on
        :return:
        """

        operation = self.program[self.current_position]
        if operation not in ['1', '2']:
            self.current_opcode = 99
            return
        else:
            operation = self.OPCODES[operation]

            first_operand = int(self.program[self.current_position+1])
            second_operand = int(self.program[self.current_position+2])
            result_index = int(self.program[self.current_position+3])
            value = eval("{} {} {}".format(self.program[first_operand], operation, self.program[second_operand]))
            self.program[result_index] = value
            self.current_position = self.current_position + 4


def run_main():

    for noun in range(0,100):
        for verb in range(0,100):
            with open("./input.txt") as input:
                reader = csv.reader(input)
                the_list = list(reader)
                program = the_list[0]

            test_program = program

            test_program[1] = str(noun)
            test_program[2] = str(verb)

            result = run_a_test(test_program)
            if result[0] == 19690720:
                print('noun and verb are {}, {}'.format(noun,verb))


def run_a_test(program):
    computer = IntCodeComputer(program)
    computer.process_program()
    return computer.program


run_main()