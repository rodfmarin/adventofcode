"""
You feel the ground rumble again as the distress signal leads you to a large network of subterranean tunnels.
You don't have time to search them all, but you don't need to: your pack contains a set of deployable sensors that you
imagine were originally built to locate lost Elves.

The sensors aren't very powerful, but that's okay; your handheld device indicates that you're close enough to the
source of the distress signal to use them. You pull the emergency sensor system out of your pack, hit the big button on
top, and the sensors zoom off down the tunnels.

Once a sensor finds a spot it thinks will give it a good reading, it attaches itself to a hard surface and begins
monitoring for the nearest signal source beacon. Sensors and beacons always exist at integer coordinates. Each sensor
knows its own position and can determine the position of a beacon precisely; however, sensors can only lock on to the
one beacon closest to the sensor as measured by the Manhattan distance. (There is never a tie where two beacons are the
same distance to a sensor.)

It doesn't take long for the sensors to report back their positions and closest beacons (your puzzle input). For
example:

Sensor at x=2, y=18: closest beacon is at x=-2, y=15
truncated
"""

# NB: My approach for part 1 was 'correct' but ended up using William Y. Feng's Algorithm in part 2

from dataclasses import dataclass


def get_input(mode='test'):
    input = []
    filename = './input.txt'
    if mode == 'test':
        # use input2 (example input)
        filename = './input2.txt'
    with open(filename, 'r') as my_file:
        for line in my_file:
            line = line.replace("\n", "")
            input.append(line)
    return input


@dataclass
class Sensor:
    x: int
    y: int
    b: 'Beacon'
    d: int = 0


@dataclass
class Beacon:
    x: int
    y: int


def dist(x_1: int, y_1: int, x_2: int, y_2: int):
    """
    Return the sum of the absolute value of the distance in both coordinates
    |x1 - x2| + |y1 - y2|
    """
    return abs(x_1 - x_2) + abs(y_1 - y_2)


def parse_sensors(input: [str]):
    sensors = []
    for index, line in enumerate(input):
        tokens = line.split(" ")
        s_x = int(tokens[2].split("=")[1].replace(",", "").replace(":", ""))
        s_y = int(tokens[3].split("=")[1].replace(",", "").replace(":", ""))
        b_x = int(tokens[8].split("=")[1].replace(",", "").replace(":", ""))
        b_y = int(tokens[9].split("=")[1].replace(",", "").replace(":", ""))

        b = Beacon(b_x, b_y)
        s = Sensor(s_x, s_y, b)

        sensors.append(s)
    return sensors


def do_part_one():
    input = get_input(mode='real')
    sensors = parse_sensors(input)

    for s in sensors:
        # Set the sensor's manhattan distance from its beacon
        s.d = dist(s.x, s.y, s.b.x, s.b.y)

    search_y = 2000000
    intervals = []

    # find the span for a sensor, i.e. the distance on the row
    for index, s in enumerate(sensors):
        dx = s.d - abs(s.y - search_y)
        if dx <= 0:
            continue
        intervals.append((s.x - dx, s.x + dx))

    # if there's a beacon on the line then that's not counted
    allowed_x = []
    for s in sensors:
        if s.b.y == search_y:
            allowed_x.append(s.b.x)

    min_x = min(i[0] for i in intervals)
    max_x = max(i[1] for i in intervals)

    ans = 0
    # go over every position in the span
    # if it's not already a beacon, count that position as an answer in the row
    for x in range(min_x, max_x + 1):
        if x in allowed_x:
            continue

        for left, right in intervals:
            if left <= x <= right:
                ans += 1
                break
    print(ans)


def do_part_two():
    """
    --- Part Two ---
    Your handheld device indicates that the distress signal is coming from a beacon nearby.
    The distress beacon is not detected by any sensor, but the distress beacon must have x and y coordinates each no
    lower than 0 and no larger than 4000000.

    To isolate the distress beacon's signal, you need to determine its tuning frequency, which can be found by
    multiplying its x coordinate by 4000000 and then adding its y coordinate.

    In the example above, the search space is smaller: instead, the x and y coordinates can each be at most 20.
    With this reduced search area, there is only a single position that could have a beacon: x=14, y=11. The tuning
    frequency for this distress beacon is 56000011.

    Find the only possible position for the distress beacon. What is its tuning frequency?
    """

    # NB:The idea here is that when all the sensors are overlapping there is only 1 spot where a beacon could be (maybe)
    # This assumes there is only one spot in the map that has this property.
    # That beacon is the distress beacon.  Imagine four sensors here with the D char being the distress beacon
    # In the center where their ranges do not reach
    """
                      xxxx
           xxxx      xx │xx
          xx │xx    xx  │ xx
         xx  │ xx  xx   │  xx
        xx   │  xxx     │   xxx
      xx     │  xxxx    │     xx
     xx      │ xx  xx   │     xx
    xx       │ xx  xx  x│xx  xx
    xx     xxxx xxxx  xx├xxxx
     xx   xx │xx xxxxxx ├xx
       xxxx  │ xxxxDxxx │xx xx
        xxxx │xxxxxx  xx│x   xxx
      xx   xx│x  xxx     │     xx
     xx      │  xx xx    │     xx
    xx       │  xx xx    │    xx
    xx       │   xxx     │   xx
     xx      │   xxxxx   │  xx
       xxx   │  xx   xxx │xx
         xxx │xx       xx│x
           xx│x
    """

    input = get_input(mode='real')
    sensors = parse_sensors(input)

    for s in sensors:
        s.d = dist(s.x, s.y, s.b.x, s.b.y)

    pos_lines = []
    neg_lines = []

    # Record the positive and negative line boundaries of the sensor
    for s in sensors:
        neg_lines.extend([s.x + s.y - s.d, s.x + s.y + s.d])
        pos_lines.extend([s.x - s.y - s.d, s.x - s.y + s.d])

    pos = None
    neg = None

    # For every positive and negative boundary between sensors
    # if the distance is 2 (really it is 1 but we have boundary / sensor / boundary on the grid )
    # According to William this is a series of linear equations.  to find pos and neg positions
    # you can take pos + neg over 2 as x and neg - pos over 2 as y (as the xs cancel out)
    for i in range(2 * len(sensors)):
        for j in range(i + 1, 2 * len(sensors)):
            a, b = pos_lines[i], pos_lines[j]

            if abs(a - b) == 2:
                pos = min(a, b) + 1

            a, b = neg_lines[i], neg_lines[j]

            if abs(a - b) == 2:
                neg = min(a, b) + 1

    x, y = (pos + neg) // 2, (neg - pos) // 2
    ans = x * 4000000 + y
    print(ans)


if __name__ == "__main__":
    do_part_one()
    do_part_two()
