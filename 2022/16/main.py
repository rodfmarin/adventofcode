"""
--- Day 16: Proboscidea Volcanium ---
The sensors have led you to the origin of the distress signal: yet another handheld device, just like the one the Elves
gave you. However, you don't see any Elves around; instead, the device is surrounded by elephants! They must have
gotten lost in these tunnels, and one of the elephants apparently figured out how to turn on the distress signal.

The ground rumbles again, much stronger this time. What kind of cave is this, exactly? You scan the cave with your
handheld device; it reports mostly igneous rock, some ash, pockets of pressurized gas, magma... this isn't just a cave,
it's a volcano!

You need to get the elephants out of here, quickly. Your device estimates that you have 30 minutes before the volcano
erupts, so you don't have time to go back out the way you came in.

You scan the cave for other options and discover a network of pipes and pressure-release valves. You aren't sure how
such a system got into a volcano, but you don't have time to complain; your device produces a report
(your puzzle input) of each valve's flow rate if it were opened (in pressure per minute) and the tunnels you could use
to move between the valves.

There's even a valve in the room you and the elephants are currently standing in labeled AA. You estimate it will take
you one minute to open a single valve and one minute to follow any tunnel from one valve to another. What is the most
pressure you could release?

For example, suppose you had the following scan output:

Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II

All of the valves begin closed. You start at valve AA, but it must be damaged or jammed or something: its flow rate is
0, so there's no point in opening it. However, you could spend one minute moving to valve BB and another minute opening
it; doing so would release pressure during the remaining 28 minutes at a flow rate of 13, a total eventual pressure
release of 28 * 13 = 364. Then, you could spend your third minute moving to valve CC and your fourth minute opening it,
providing an additional 26 minutes of eventual pressure release at a flow rate of 2, or 52 total pressure released by
valve CC.

Making your way through the tunnels like this, you could probably open many or all of the valves by the time 30 minutes
have elapsed. However, you need to release as much pressure as possible, so you'll need to be methodical.
Instead, consider this approach:
truncated
"""

"""
NB: My initial approach ideation was pretty similar to what hyper-neutrino did in their solution.  find each child of 
the root node, find their children, calculate all paths from the root down every node's children and so on
keeping track of the time remaining and what the score would be if the valve was turned on.

I probably would have hit the really tough wall in part 2 and not being able to compute in a reasonable enough time if 
I hadn't heard about collapsing the graph down by removing the 0 flow rate valves.

I got sidetracked into reading about Floyd-Warshall which is a really neat algorithm about shortest path between pairs.
I had an idea about creating weights that were the value of the node's distance from the root minus its flow rate.

The bitmask of the world's state of valves is really great and doing bitwise operations and shifts is also novel.
I like how this easily worked when calculating the Elephant's state to work from in part 2.
"""

import math
from collections import deque
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
class Valve:
    name: str
    flow_rate: int
    valve_closed: bool
    children: []
    visited: bool = False
    distance_from_origin: int = 0


def parse_valves(input: [str]) -> dict:
    valves = {}
    for line in input:
        tokens = line.split(" ")
        v_name = tokens[1]
        flow_rate = int(tokens[4][tokens[4].index("=") + 1:tokens[4].index(";")])
        children = tokens[9:12]
        children = [c.replace(',', '') for c in children]
        valves[v_name] = {
            "name": v_name,
            "flow_rate": flow_rate,
            "valve_closed": True,
            "children": children,
            "distance_from_origin": 0
        }
    return valves


def get_empty_dist_matrix(valve_count: int) -> list[list]:
    return [[math.inf] * valve_count for v in range(valve_count)]


def do_part_one():
    input = get_input(mode="real")

    valves = {}
    tunnels = {}

    for line in input:
        line = line.strip()
        valve = line.split()[1]
        flow = int(line.split(";")[0].split("=")[1])
        targets = line.split("to ")[1].split(" ", 1)[1].split(", ")
        valves[valve] = flow
        tunnels[valve] = targets

    dists = {}
    nonempty = []

    for valve in valves:
        if valve != "AA" and not valves[valve]:
            continue

        if valve != "AA":
            nonempty.append(valve)

        dists[valve] = {valve: 0, "AA": 0}
        visited = {valve}

        queue = deque([(0, valve)])

        while queue:
            distance, position = queue.popleft()
            for neighbor in tunnels[position]:
                if neighbor in visited:
                    continue
                visited.add(neighbor)
                if valves[neighbor]:
                    dists[valve][neighbor] = distance + 1
                queue.append((distance + 1, neighbor))

        del dists[valve][valve]
        if valve != "AA":
            del dists[valve]["AA"]

    indices = {}

    for index, element in enumerate(nonempty):
        indices[element] = index

    cache = {}

    # NB: A novel approach by hyper-neutrino https://www.youtube.com/watch?v=bLMj50cpOug
    # Uses a bitmask that represents the state of the world's valves and if they're on or not
    # Then with memoization / caching doesn't spend time trying to compute an already computed state
    # it is a brute force algorithm that is checking each path
    # In part 2 2^15 states with large depths is a lot to calculate, takes over 20 seconds to run
    def dfs(time, valve, bitmask):
        if (time, valve, bitmask) in cache:
            return cache[(time, valve, bitmask)]

        maxval = 0
        for neighbor in dists[valve]:
            bit = 1 << indices[neighbor]
            if bitmask & bit:
                continue
            remtime = time - dists[valve][neighbor] - 1
            if remtime <= 0:
                continue
            maxval = max(maxval, dfs(remtime, neighbor, bitmask | bit) + valves[neighbor] * remtime)

        cache[(time, valve, bitmask)] = maxval
        return maxval

    print(dfs(30, "AA", 0))

    b = (1 << len(nonempty)) - 1

    m = 0

    for i in range(b + 1):
        m = max(m, dfs(26, "AA", i) + dfs(26, "AA", b ^ i))

    print(m)


def do_part_two():
    # see part 1, solves both.  Great walk-through by hyper-neutrino
    pass


if __name__ == "__main__":
    do_part_one()
    do_part_two()
