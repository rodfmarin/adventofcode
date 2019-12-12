import csv

class IntCodeComputer:

    def __init__(self, program):
        self.OPCODES = {
            "1": "+",
            "2": "*",
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

#[21202657, '97', '11', 2, '1', '1', '2', '3', '1', '3', '4', '3', '1', '5', '0', '3', '2', '10', '1', 388, '1', '19', '6', 390, '2', '13', '23', 1950, '1', '27', '13', 1955, '1', '9', '31', 1958, '1', '35', '9', 1961, '1', '39', '5', 1962, '2', '6', '43', 3924, '1', '47', '6', 3926, '2', '51', '9', 11778, '2', '55', '13', 58890, '1', '59', '6', 58892, '1', '10', '63', 58896, '2', '67', '9', 176688, '2', '6', '71', 353376, '1', '75', '5', 353377, '2', '79', '10', 1413508, '1', '5', '83', 1413509, '2', '9', '87', 4240527, '1', '5', '91', 4240528, '2', '13', '95', 21202640, '1', '99', '10', 21202644, '1', '103', '2', 21202655, '1', '107', '6', '0', '99', '2', '14', '0', '0']

def run_main():

    for noun in xrange(0,100):
        for verb in xrange(0,100):
            with open("./scratch.txt") as input:
                reader = csv.reader(input)
                the_list = list(reader)
                program = the_list[0]

            test_program = program


            test_program[1] = str(noun)
            test_program[2] = str(verb)
            #print('test_program is {}'.format(test_program))
            result = run_a_test(test_program)
            if result[0] == 19690720:
                print('noun and verb are {}, {}'.format(noun,verb))


def run_a_test(program):
    computer = IntCodeComputer(program)
    computer.process_program()
    return computer.program


run_main()