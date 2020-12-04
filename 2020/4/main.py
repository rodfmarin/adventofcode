"""
--- Day 4: Passport Processing ---
You arrive at the airport only to realize that you grabbed your North Pole Credentials instead of your passport.
While these documents are extremely similar, North Pole Credentials aren't issued by a country and therefore aren't
actually valid documentation for travel in most of the world.

It seems like you're not the only one having problems, though; a very long line has formed for the automatic passport
scanners, and the delay could upset your travel itinerary.

Due to some questionable network security, you realize you might be able to solve both of these problems at the same
time.

The automatic passport scanners are slow because they're having trouble detecting which passports have all required
fields. The expected fields are as follows:

byr (Birth Year)
iyr (Issue Year)
eyr (Expiration Year)
hgt (hgt)
hcl (Hair Color)
ecl (Eye Color)
pid (Passport ID)
cid (Country ID)
Passport data is validated in batch files (your puzzle input). Each passport is represented as a sequence of key:value
pairs separated by spaces or newlines. Passports are separated by blank lines.

Here is an example batch file containing four passports:

ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in
The first passport is valid - all eight fields are present. The second passport is invalid - it is missing hgt
(the hgt field).

The third passport is interesting; the only missing field is cid, so it looks like data from North Pole Credentials,
not a passport at all! Surely, nobody would mind if you made the system temporarily ignore missing cid fields.
Treat this "passport" as valid.

The fourth passport is missing two fields, cid and byr. Missing cid is fine, but missing any other field is not,
so this passport is invalid.

According to the above rules, your improved system would report 2 valid passports.

Count the number of valid passports - those that have all required fields. Treat cid as optional. In your batch file,
how many passports are valid?


"""
import re

input = []
with open('input.txt') as my_file:
    for line in my_file:
        input.append(line.strip('\n'))


class PassPort:
    def __init__(self, byr=None, iyr=None, eyr=None, hgt=None, hcl=None, ecl=None, pid=None, cid=None):
        """

        :param byr:
        :param iyr:
        :param eyr:
        :param hgt:
        :param hcl:
        :param ecl:
        :param pid:
        :param cid:
        """
        self.byr = byr
        self.iyr = iyr
        self.eyr = eyr
        self.hgt = hgt
        self.hcl = hcl
        self.ecl = ecl
        self.pid = pid
        self.cid = cid
        self.is_valid = False

    def validate(self):
        """
        Inspect the Passport's fields for valid pass
        Passwords must have all required fields
        :param passport:
        :return:
        """

        if self.validate_all_fields():
            return True
        return False

    def validate_all_fields(self):
        """
        Checks ALL fields for values
        :return: bool
        """

        if self.validate_byr() and \
                self.validate_iyr() and \
                self.validate_eyr() and \
                self.validate_hgt() and \
                self.validate_hcl() and \
                self.validate_ecl() and \
                self.validate_pid() and \
                self.validate_cid():
            return True
        return False

    def validate_byr(self):
        if self.byr:
            if re.match('[0-9]{4}', self.byr):
                if 1920 <= int(self.byr) <= 2002:
                    return True

    def validate_iyr(self):
        if self.iyr:
            if re.match('[0-9]{4}', self.iyr):
                if 2010 <= int(self.iyr) <= 2020:
                    return True

    def validate_eyr(self):
        if self.eyr:
            if 2020 <= int(self.eyr) <= 2030:
                return True

    def validate_hgt(self):
        if self.hgt:
            number_form = int(self.hgt[:-2])
            if re.match('.+cm', self.hgt):
                # We have a cm height, check range
                if 150 <= number_form <= 193:
                    return True
            if re.match('.+in', self.hgt):
                # We have a in height, check range
                if 59 <= number_form <= 76:
                    return True

    def validate_hcl(self):
        if self.hcl:
            if re.match('#[0-9,a-f]{6}', self.hcl):
                return True

    def validate_ecl(self):
        if self.ecl:
            if re.match('amb{1}|blu{1}|brn{1}|gry{1}|grn{1}|hzl{1}|oth{1}', self.ecl):
                return True

    def validate_pid(self):
        if self.pid:
            if len(self.pid) == 9:
                return True

    def validate_cid(self):
        return True

    def validate_all_but_cid(self):
        if self.byr and \
                self.iyr and \
                self.eyr and \
                self.hgt and \
                self.hcl and \
                self.ecl and \
                self.pid and \
                not self.cid:
            return True
        return False


def passport_parser(raw):
    """
    A Passport entry comes in via Key:Value pairs
    :param raw:
    :return:
    """

    if raw:
        # The Raw is a line of key values, separated by space
        raw = raw.split(" ")
        map = {}
        for item in raw:
            data = item.split(":")
            key = data[0]
            value = data[1]
            map.update({key: value})

        return PassPort(**map)


def prepare_input(input):
    """
    Prepare the input as the fields are on separate lines
    :param input:
    :return:
    """
    new_output = []

    line_cursor = 0
    new_string = ""

    while line_cursor < len(input):
        if input[line_cursor]:
            new_string = new_string + input[line_cursor] + " "
            line_cursor += 1

            if line_cursor == len(input):
                # We're at the end, insert the last string
                new_string = new_string.strip()
                new_output.append(new_string)
        else:
            # Skip on blanks, append what was found
            line_cursor += 1
            new_string = new_string.strip()
            new_output.append(new_string)
            new_string = ""

    return new_output


def main():
    p_input = prepare_input(input)
    valid_passports = 0
    for item in p_input:
        passport = passport_parser(item)
        if passport.validate():
            valid_passports += 1

    print(valid_passports)


if __name__ == '__main__':
    main()
