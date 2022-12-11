"""
--- Day 2: Rock Paper Scissors ---
The Elves begin to set up camp on the beach. To decide whose tent gets to be closest to the snack storage,
a giant Rock Paper Scissors tournament is already in progress.

Rock Paper Scissors is a game between two players. Each game contains many rounds; in each round,
the players each simultaneously choose one of Rock, Paper, or Scissors using a hand shape.
Then, a winner for that round is selected: Rock defeats Scissors, Scissors defeats Paper, and Paper defeats Rock.
If both players choose the same shape, the round instead ends in a draw.

Appreciative of your help yesterday, one Elf gives you an encrypted strategy guide (your puzzle input) that they say
will be sure to help you win. "The first column is what your opponent is going to play: A for Rock, B for Paper, and C
for Scissors. The second column--" Suddenly, the Elf is called away to help with someone's tent.

The second column, you reason, must be what you should play in response: X for Rock, Y for Paper, and Z for Scissors.
Winning every time would be suspicious, so the responses must have been carefully chosen.

The winner of the whole tournament is the player with the highest score. Your total score is the sum of your scores for
each round. The score for a single round is the score for the shape you selected (1 for Rock, 2 for Paper, and 3 for
Scissors) plus the score for the outcome of the round (0 if you lost, 3 if the round was a draw, and 6 if you won).

Since you can't be sure if the Elf is trying to help you or trick you, you should calculate the score you would get if
you were to follow the strategy guide.

For example, suppose you were given the following strategy guide:

A Y
B X
C Z
This strategy guide predicts and recommends the following:

In the first round, your opponent will choose Rock (A), and you should choose Paper (Y). This ends in a win for you
with a score of 8 (2 because you chose Paper + 6 because you won).
In the second round, your opponent will choose Paper (B), and you should choose Rock (X). This ends in a loss for you
with a score of 1 (1 + 0).
The third round is a draw with both players choosing Scissors, giving you a score of 3 + 3 = 6.
In this example, if you were to follow the strategy guide, you would get a total score of 15 (8 + 1 + 6).
"""

"""
Rock is       A | X
Paper is      B | Y
Scissors is   C | Z
"""


def get_input():
    input = []
    with open('./input.txt', 'r') as my_file:
        for line in my_file:
            input.append(line)
    return input


class Weapon:
    def __init__(self, letter):
        self.letter = letter


class Rock(Weapon):
    def __init__(self, letter="A"):
        super().__init__(letter)
        self.score = 1
        self.lose_against = Paper
        self.win_against = Scissors


class Paper(Weapon):
    def __init__(self, letter="B"):
        super().__init__(letter)
        self.score = 2
        self.lose_against = Scissors
        self.win_against = Rock


class Scissors(Weapon):
    def __init__(self, letter="C"):
        super().__init__(letter)
        self.score = 3
        self.lose_against = Rock
        self.win_against = Paper


def weapon_factory(letter):
    letter = letter.upper()
    if letter == "A" or letter == "X":
        return Rock(letter)
    if letter == "B" or letter == "Y":
        return Paper(letter)
    if letter == "C" or letter == "Z":
        return Scissors(letter)


class Game:
    def __init__(self, opponent, player):
        self.opponent = opponent
        self.player = player

        self.WIN_SCORE = 6
        self.LOSE_SCORE = 0
        self.DRAW_SCORE = 3

    def play(self):
        """
        Compare the opponent and the player weapons
        Return a score for the player depending on the outcome according to these rules:

        The score for a single round is the score for the shape you selected
        (1 for Rock, 2 for Paper, and 3 forScissors) plus the score for the outcome of the round
        (0 if you lost, 3 if the round was a draw, and 6 if you won).

        Scissors > Paper > Rock > Scissors
        """
        if self.opponent.__class__ == self.player.__class__:
            # Draw, return the DRAW Score + the weapon's value
            print("draw")
            return self.DRAW_SCORE + self.player.score

        if self.player.lose_against == self.opponent.__class__:
            # A Loss, return the LOSE Score + the weapon's value
            print("lose")
            return self.LOSE_SCORE + self.player.score

        if self.opponent.lose_against == self.player.__class__:
            # A Win, return the WIN Score + the weapon's value
            print("win")
            return self.WIN_SCORE + self.player.score


def do_part_one():
    """
    What would your total score be if everything goes exactly according to your strategy guide?
    """
    input = get_input()

    tally = 0

    for line in input:
        line = line.replace("\n","")
        line = line.split(" ")
        opponent = weapon_factory(line[0])
        player = weapon_factory(line[1])

        g = Game(opponent=opponent, player=player)
        tally += g.play()
    print(tally)


def do_part_two():
    """
    The Elf finishes helping with the tent and sneaks back over to you. "Anyway, the second column says how
    the round needs to end:
    X means you need to lose,
    Y means you need to end the round in a draw,
    and Z means you need to win. Good luck!"
    """

    input = get_input()

    tally = 0

    for line in input:
        line = line.replace("\n","")
        line = line.split(" ")
        opponent = weapon_factory(line[0])
        # We now need to play according to a rule instead of creating a weapon
        action = weapon_factory(line[1])

        if action.letter == "X":
            # Lose the game, who loses to opponent?
            player = opponent.win_against()
        if action.letter == "Y":
            # Draw the game, become the opponent
            player = opponent
        if action.letter == "Z":
            # Win the game, become the winner
            player = opponent.lose_against()

        g = Game(opponent=opponent, player=player)
        tally += g.play()
    print(tally)


if __name__ == "__main__":
    do_part_one()
    do_part_two()