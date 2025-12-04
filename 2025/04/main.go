package main

import (
	"log"
	"os"
	"strings"
)

/*
--- Day 4: Printing Department ---
You ride the escalator down to the printing department. They're clearly getting ready for Christmas; they have lots of
large rolls of paper everywhere, and there's even a massive printer in the corner (to handle the really big print jobs).

Decorating here will be easy: they can make their own decorations. What you really need is a way to get further into
the North Pole base while the elevators are offline.

"Actually, maybe we can help with that," one of the Elves replies when you ask for help. "We're pretty sure there's a
cafeteria on the other side of the back wall. If we could break through the wall, you'd be able to keep moving. It's
too bad all of our forklifts are so busy moving those big rolls of paper around."

If you can optimize the work the forklifts are doing, maybe they would have time to spare to break through the wall.

The rolls of paper (@) are arranged on a large grid; the Elves even have a helpful diagram (your puzzle input)
indicating where everything is located.

For example:

..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.
The forklifts can only access a roll of paper if there are fewer than four rolls of paper in the eight adjacent
positions. If you can figure out which rolls of paper the forklifts can access, they'll spend less time looking and
more time breaking down the wall to the cafeteria.

In this example, there are 13 rolls of paper that can be accessed by a forklift (marked with x):

..xx.xx@x.
x@@.@.@.@@
@@@@@.x.@@
@.@@@@..@.
x@.@@@@.@x
.@@@@@@@.@
.@.@.@.@@@
x.@@@.@@@@
.@@@@@@@@.
x.x.@@@.x.
Consider your complete diagram of the paper roll locations. How many rolls of paper can be accessed by a forklift?

--- Part Two ---
Now, the Elves just need help accessing as much of the paper as they can.

Once a roll of paper can be accessed by a forklift, it can be removed. Once a roll of paper is removed, the forklifts
might be able to access more rolls of paper, which they might also be able to remove. How many total rolls of paper
could the Elves remove if they keep repeating this process?

Starting with the same example as above, here is one way you could remove as many rolls of paper as possible,
using highlighted @ to indicate that a roll of paper is about to be removed, and using x to indicate that a roll of
paper was just removed:

Initial state:
..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.

Remove 13 rolls of paper:
..xx.xx@x.
x@@.@.@.@@
@@@@@.x.@@
@.@@@@..@.
x@.@@@@.@x
.@@@@@@@.@
.@.@.@.@@@
x.@@@.@@@@
.@@@@@@@@.
x.x.@@@.x.

Remove 12 rolls of paper:
.......x..
.@@.x.x.@x
x@@@@...@@
x.@@@@..x.
.@.@@@@.x.
.x@@@@@@.x
.x.@.@.@@@
..@@@.@@@@
.x@@@@@@@.
....@@@...

Remove 7 rolls of paper:
..........
.x@.....x.
.@@@@...xx
..@@@@....
.x.@@@@...
..@@@@@@..
...@.@.@@x
..@@@.@@@@
..x@@@@@@.
....@@@...

Remove 5 rolls of paper:
..........
..x.......
.x@@@.....
..@@@@....
...@@@@...
..x@@@@@..
...@.@.@@.
..x@@.@@@x
...@@@@@@.
....@@@...

Remove 2 rolls of paper:
..........
..........
..x@@.....
..@@@@....
...@@@@...
...@@@@@..
...@.@.@@.
...@@.@@@.
...@@@@@x.
....@@@...

Remove 1 roll of paper:
..........
..........
...@@.....
..x@@@....
...@@@@...
...@@@@@..
...@.@.@@.
...@@.@@@.
...@@@@@..
....@@@...

Remove 1 roll of paper:
..........
..........
...x@.....
...@@@....
...@@@@...
...@@@@@..
...@.@.@@.
...@@.@@@.
...@@@@@..
....@@@...

Remove 1 roll of paper:
..........
..........
....x.....
...@@@....
...@@@@...
...@@@@@..
...@.@.@@.
...@@.@@@.
...@@@@@..
....@@@...

Remove 1 roll of paper:
..........
..........
..........
...x@@....
...@@@@...
...@@@@@..
...@.@.@@.
...@@.@@@.
...@@@@@..
....@@@...
Stop once no more rolls of paper are accessible by a forklift. In this example, a total of 43 rolls of paper can be
removed.

Start with your original diagram. How many rolls of paper in total can be removed by the Elves and their forklifts?
*/

func ReadFileLines(path string) ([]string, error) {
	lines, err := os.ReadFile(path)
	if err != nil {
		log.Fatalf("Error reading file: %v", err)
	}
	return strings.Split(string(lines), "\n"), nil
}

// Point represents a coordinate in the grid
type Point struct {
	X int
	Y int
}

// Roll represents a roll of paper with its position and access status
type Roll struct {
	Position Point
	Access   bool
}

// Grid represents the grid of rolls of paper
type Grid struct {
	Rolls  map[Point]*Roll
	Width  int
	Height int
}

// ParseLinesToGrid parses the input lines into a Grid structure
func ParseLinesToGrid(lines []string) *Grid {
	grid := &Grid{
		Rolls:  make(map[Point]*Roll),
		Height: len(lines),
	}
	for y, line := range lines {
		grid.Width = len(line)
		for x, char := range line {
			if char == '@' {
				grid.Rolls[Point{X: x, Y: y}] = &Roll{Position: Point{X: x, Y: y}, Access: false}
			}
		}
	}
	return grid
}

func main() {
	doPartOne()
	doPartTwo()
}

func doPartOne() {
	lines, err := ReadFileLines("2025/04/input.txt")
	if err != nil {
		log.Fatalf("Error reading input file: %v", err)
	}

	grid := ParseLinesToGrid(lines)

	// Directions for the 8 adjacent positions
	directions := []Point{
		{-1, -1}, {0, -1}, {1, -1},
		{-1, 0}, {1, 0},
		{-1, 1}, {0, 1}, {1, 1},
	}

	// Check access for each roll of paper
	for _, roll := range grid.Rolls {
		adjacentCount := 0
		for _, dir := range directions {
			adjacentPos := Point{X: roll.Position.X + dir.X, Y: roll.Position.Y + dir.Y}
			if _, exists := grid.Rolls[adjacentPos]; exists {
				adjacentCount++
			}
		}
		if adjacentCount < 4 {
			roll.Access = true
		}
	}

	// Count accessible rolls
	accessibleCount := 0
	for _, roll := range grid.Rolls {
		if roll.Access {
			accessibleCount++
		}
	}

	log.Printf("Number of accessible rolls of paper: %d", accessibleCount)
}

func doPartTwo() {
	lines, err := ReadFileLines("2025/04/input.txt")
	if err != nil {
		log.Fatalf("Error reading input file: %v", err)
	}

	grid := ParseLinesToGrid(lines)
	// Directions for the 8 adjacent positions
	directions := []Point{
		{-1, -1}, {0, -1}, {1, -1},
		{-1, 0}, {1, 0},
		{-1, 1}, {0, 1}, {1, 1},
	}

	totalRemoved := 0

	for {
		removedThisRound := 0
		// Check access for each roll of paper
		for _, roll := range grid.Rolls {
			if roll.Access {
				continue // Already accessible
			}
			adjacentCount := 0
			for _, dir := range directions {
				adjacentPos := Point{X: roll.Position.X + dir.X, Y: roll.Position.Y + dir.Y}
				if _, exists := grid.Rolls[adjacentPos]; exists {
					adjacentCount++
				}
			}
			if adjacentCount < 4 {
				roll.Access = true
				removedThisRound++
			}
		}

		if removedThisRound == 0 {
			break // No more rolls can be removed
		}

		totalRemoved += removedThisRound

		// Remove accessible rolls
		for pos, roll := range grid.Rolls {
			if roll.Access {
				delete(grid.Rolls, pos)
			}
		}
	}

	log.Printf("Total rolls of paper removed: %d", totalRemoved)

}
