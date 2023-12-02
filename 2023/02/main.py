"""
--- Day 2: Cube Conundrum ---
You're launched high into the atmosphere! The apex of your trajectory just barely reaches the surface of a large island
floating in the sky. You gently land in a fluffy pile of leaves. It's quite cold, but you don't see much snow.
An Elf runs over to greet you.

The Elf explains that you've arrived at Snow Island and apologizes for the lack of snow. He'll be happy to explain the
situation, but it's a bit of a walk, so you have some time. They don't get many visitors up here; would you like to
play a game in the meantime?

As you walk, the Elf shows you a small bag and some cubes which are either red, green, or blue. Each time you play this
game, he will hide a secret number of cubes of each color in the bag, and your goal is to figure out information about
the number of cubes.

To get information, once a bag has been loaded with cubes, the Elf will reach into the bag, grab a handful of random
cubes, show them to you, and then put them back in the bag. He'll do this a few times per game.

You play several games and record the information from each game (your puzzle input). Each game is listed with its ID
number (like the 11 in Game 11: ...) followed by a semicolon-separated list of subsets of cubes that were revealed from
the bag (like 3 red, 5 green, 4 blue).

For example, the record of a few games might look like this:

Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
In game 1, three sets of cubes are revealed from the bag (and then put back again). The first set is 3 blue cubes and 4
red cubes; the second set is 1 red cube, 2 green cubes, and 6 blue cubes; the third set is only 2 green cubes.

The Elf would first like to know which games would have been possible if the bag contained only 12 red cubes, 13 green
cubes, and 14 blue cubes?

In the example above, games 1, 2, and 5 would have been possible if the bag had been loaded with that configuration.
However, game 3 would have been impossible because at one point the Elf showed you 20 red cubes at once; similarly,
game 4 would also have been impossible because the Elf showed you 15 blue cubes at once. If you add up the IDs of the
games that would have been possible, you get 8.

Determine which games would have been possible if the bag had been loaded with only 12 red cubes, 13 green cubes, and 14
blue cubes. What is the sum of the IDs of those games?
"""
import re
from pprint import pprint


def get_input():
    input = []
    with open('./input.txt', 'r') as my_file:
        for line in my_file:
            input.append(line)
    return input


class Round:
    """A Round is the number and color of cubes retrieved during a round of the game"""
    def __init__(self, red: int = 0, blue: int = 0, green: int = 0):
        self.red = red
        self.blue = blue
        self.green = green

class Game:
    """A Game with its ID and rounds"""
    def __init__(self, id: str, rounds: [Round]):
        self.id = id
        self.rounds = rounds


class GameParser:
    """Parse A Line and return a Game"""

    def __init__(self, line: str):
        self.line = line

    def parse(self) -> Game:
        """
        Parse A Line and Return a Game
        A Game Str Representation looks like:
        Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
        """
        game_id = self.__get_game_id()
        rounds = self.__get_rounds()
        return Game(id=game_id, rounds=rounds)

    def __get_game_id(self) -> str:
        """Extract the game id from the string"""
        return self.line.split(":")[0].split("Game ")[1]

    def __get_rounds(self):
        """For each round, separated by semicolon; create a Round"""
        raw_rounds = re.sub(r'^.+\:.', '', self.line).strip()
        raw_rounds = raw_rounds.split('; ')
        all_rounds = []

        for r in raw_rounds:
            round_data = {}
            raw_cubes = r.split(", ")
            for rc in raw_cubes:
                cube_split = rc.split(' ')
                #print(f"cube split is {cube_split}")
                cube_num = cube_split[0]
                cube_color = cube_split[1]
                round_data[cube_color] = cube_num
            #pprint(round_data)
            all_rounds.append(Round(**round_data))
        return all_rounds


class GameInspector:
    """
    Inspects a Game to determine if it is possible, given some limits
    for example if red limit is 12
    and blue limit is 13
    and green limit is 14
    Could a game with r,g,b of x,y,z be 'valid'
    """
    def __init__(self, game: Game,  red_limit: int = 12, blue_limit: int = 14, green_limit: int = 13):
        self.game = game
        self.red_limit = red_limit
        self.blue_limit = blue_limit
        self.green_limit = green_limit

    def is_valid_game(self) -> bool:
        """
        Look at a Game's rounds
        for each round, if any rgb is over the limit, the game is invalid
        """
        for r in self.game.rounds:
            if int(r.red) > self.red_limit or int(r.blue) > self.blue_limit or int(r.green) > self.green_limit:
                return False
        return True


def do_part_one():
    lines = get_input()
    games = []
    valid_games = []
    for line in lines:
        games.append(GameParser(line).parse())

    for g in games:
        i = GameInspector(g)
        if i.is_valid_game():
            valid_games.append(g)
    valid_ids = [i.id for i in valid_games]
    print(valid_ids)
    print("Total: ", sum(int(i) for i in valid_ids))

def do_part_two():
    pass

if __name__ == "__main__":
    do_part_one()
    do_part_two()
