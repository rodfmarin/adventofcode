"""
--- Day 6: Custom Customs ---
As your flight approaches the regional airport where you'll switch to a much larger plane, customs declaration forms
are distributed to the passengers.

The form asks a series of 26 yes-or-no questions marked a through z. All you need to do is identify the questions for
which anyone in your group answers "yes". Since your group is just you, this doesn't take very long.

However, the person sitting next to you seems to be experiencing a language barrier and asks if you can help.
For each of the people in their group, you write down the questions for which they answer "yes", one per line.
For example:

abcx
abcy
abcz
In this group, there are 6 questions to which anyone answered "yes": a, b, c, x, y, and z. (Duplicate answers to the
same question don't count extra; each question counts at most once.)

Another group asks for your help, then another, and eventually you've collected answers from every group on the plane
(your puzzle input). Each group's answers are separated by a blank line, and within each group, each person's
answers are on a single line. For example:

abc

a
b
c

ab
ac

a
a
a
a

b
This list represents answers from five groups:

The first group contains one person who answered "yes" to 3 questions: a, b, and c.
The second group contains three people; combined, they answered "yes" to 3 questions: a, b, and c.
The third group contains two people; combined, they answered "yes" to 3 questions: a, b, and c.
The fourth group contains four people; combined, they answered "yes" to only 1 question, a.
The last group contains one person who answered "yes" to only 1 question, b.
In this example, the sum of these counts is 3 + 3 + 3 + 1 + 1 = 11.

For each group, count the number of questions to which anyone answered "yes". What is the sum of those counts?
"""
import string


class Answers:
    def __init__(self, file_path):
        """
        The Answers class represents all group answers with a raw input
        The raw input can appear as:

                abc

                a
                b
                c

                ab
                ac

                a
                a
                a
                a

                b
        :param file_path:
        """
        self.file_path = file_path
        self.setup_letter_buckets()
        self.lines = []
        self.convert_raw()
        self.total = 0

    def setup_letter_buckets(self):
        """
        Create a list of buckets that map to the alphas
        :return:
        """
        for char in string.ascii_lowercase:
            setattr(self, char, 0)

    def convert_raw(self):
        """
        turn raw input into an array of lines
        :return:
        """

        with open(self.file_path) as my_file:
            for line in my_file:
                self.lines.append(line.strip())

    def process_lines(self):
        """
        we want to step through each 'line' which is an element in the array and count its 'yesses'
        we want to keep going and count each subsequent line and also add its 'yeses'.
        we want to stop when we hit a blank line
            add all the yeses and put that count in an accumulator
            zero all the counts
        repeat
        :return:
        """

        for line in self.lines:
            if not line:
                self.do_count()
                self.zero_counts()
            for char in line:
                if getattr(self, char) == 0:
                    setattr(self, char, 1)

        self.do_count()

    def process_lines_everyone_answered_yes(self):
        """
        For part 2, we only count the answer if all persons answered yes.
        This means we have to evaluate the entire group
        :return:
        """
        pass

    def zero_counts(self):
        """
        zero all buckets
        :return:
        """

        for char in string.ascii_lowercase:
            setattr(self, char, 0)

    def do_count(self):
        """
        iterate all buckets and add their sum to total
        :return:
        """
        for char in string.ascii_lowercase:
            if getattr(self, char) > 0:
                self.total += 1


def main():
    answers = Answers('./input.txt')
    # Part 1 solution
    answers.process_lines()
    print(answers.total)

    # Part 2 solution





if __name__ == "__main__":
    main()
