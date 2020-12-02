"""
--- Day 2: Password Philosophy ---
Your flight departs in a few days from the coastal airport; the easiest way down to the coast from here is via toboggan.

The shopkeeper at the North Pole Toboggan Rental Shop is having a bad day. "Something's wrong with our computers;
we can't log in!" You ask if you can take a look.

Their password database seems to be a little corrupted: some of the passwords wouldn't have been allowed by the
Official Toboggan Corporate Policy that was in effect when they were chosen.

To try to debug the problem, they have created a list (your puzzle input) of passwords (according to the corrupted
database) and the corporate policy when that password was set.

For example, suppose you have the following list:

1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc
Each line gives the password policy and then the password. The password policy indicates the lowest and highest number
 of times a given letter must appear for the password to be valid. For example, 1-3 a means that the password must
 contain a at least 1 time and at most 3 times.

In the above example, 2 passwords are valid. The middle password, cdefg, is not; it contains no instances of b, but
needs at least 1. The first and third passwords are valid: they contain one a or nine c, both within the limits of
their respective policies.

How many passwords are valid according to their policies?

--- Part Two ---
While it appears you validated the passwords correctly, they don't seem to be what the Official Toboggan Corporate
Authentication System is expecting.

The shopkeeper suddenly realizes that he just accidentally explained the password policy rules from his old job at the
 sled rental place down the street! The Official Toboggan Corporate Policy actually works a little differently.

Each policy actually describes two positions in the password, where 1 means the first character, 2 means the second
character, and so on. (Be careful; Toboggan Corporate Policies have no concept of "index zero"!) Exactly one of these
positions must contain the given letter. Other occurrences of the letter are irrelevant for the purposes of policy
enforcement.

Given the same example list from above:

1-3 a: abcde is valid: position 1 contains a and position 3 does not.
1-3 b: cdefg is invalid: neither position 1 nor position 3 contains b.
2-9 c: ccccccccc is invalid: both position 2 and position 9 contain c.

"""


input = []
with open('input.txt') as my_file:
    for line in my_file:
        input.append(line)


class Policy:
    def __init__(self, min_count, max_count, letter, password):
        self.min_count = int(min_count)
        self.max_count = int(max_count)
        self.letter = letter
        self.password = password

    def is_valid_password(self):
        """
        We want to inspect the password string and see if it conforms to policy
        That means if our policy is 1-3 a: abcde, then 'a' must appear once, but no more than 3 times.
        :return: boolean
        """

        if self.password.count(self.letter) >= self.min_count:
            # We're valid here because we have at least the minimum
            if self.password.count(self.letter) <= self.max_count:
                # We're valid here because we have less than the maximum
                return True
            return False
        return False

    def is_valid_toboggan_password(self):
        """
        In a Toboggan Corp policy the min and max count actually describe the index positions of the letter
        in a password.
        in 1-3 a: abcde, it's valid because position 1 contains a and position 3 does not.
        Exactly one position can contain the letter, otherwise it is invalid.
        Toboggans don't know about about index 0 either, meaning we might need to subtract 1 from each index
        :return: boolean
        """

        index_one = self.min_count - 1
        index_two = self.max_count - 1

        # If they're the same just return false
        if self.password[index_one] == self.letter and self.password[index_two] == self.letter:
            return False
        elif self.password[index_one] == self.letter:
            return True
        elif self.password[index_two] == self.letter:
            return True

        return False


def parse_policy(string):
    """
    Parse the policy
    A Policy looks like:
    1-3 a: abcde
    :param string: The Policy String
    :return: A Policy Object
    """

    # Split the string on space
    policy = string.split(" ")

    # First field is the min and max count
    min_count = policy[0].split("-")[0]
    max_count = policy[0].split("-")[1]

    # Second field is the letter
    letter = policy[1].strip(":")

    # Third field is the password
    password = policy[2]

    return Policy(min_count, max_count, letter, password)


def main():
    valid_passwords = 0
    for item in input:
        policy = parse_policy(item)
        if policy.is_valid_toboggan_password():
            valid_passwords += 1

    print(valid_passwords)


if __name__ == '__main__':
    main()