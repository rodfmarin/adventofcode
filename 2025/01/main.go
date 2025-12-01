package main

import (
	"fmt"
	"log"
	"os"
	"strings"
)

/*
--- Day 1: Secret Entrance ---
The Elves have good news and bad news.
The good news is that they've discovered project management! This has given them the tools they need to prevent their
usual Christmas emergency. For example, they now know that the North Pole decorations need to be finished soon so that
other critical tasks can start on time.

The bad news is that they've realized they have a different emergency: according to their resource planning,
none of them have any time left to decorate the North Pole!

To save Christmas, the Elves need you to finish decorating the North Pole by December 12th.

Collect stars by solving puzzles. Two puzzles will be made available on each day; the second puzzle is unlocked
when you complete the first. Each puzzle grants one star. Good luck!

You arrive at the secret entrance to the North Pole base ready to start decorating. Unfortunately, the password seems
to have been changed, so you can't get in. A document taped to the wall helpfully explains:

"Due to new security protocols, the password is locked in the safe below. Please see the attached document for the new
combination."

The safe has a dial with only an arrow on it; around the dial are the numbers 0 through 99 in order. As you turn the
dial, it makes a small click noise as it reaches each number.

The attached document (your puzzle input) contains a sequence of rotations, one per line, which tell you how to open
the safe. A rotation starts with an L or R which indicates whether the rotation should be to the left
(toward lower numbers) or to the right (toward higher numbers). Then, the rotation has a distance value which indicates
how many clicks the dial should be rotated in that direction.

So, if the dial were pointing at 11, a rotation of R8 would cause the dial to point at 19. After that, a rotation of
L19 would cause it to point at 0.

Because the dial is a circle, turning the dial left from 0 one click makes it point at 99. Similarly, turning the dial
right from 99 one click makes it point at 0.

So, if the dial were pointing at 5, a rotation of L10 would cause it to point at 95. After that, a rotation of R5 could
cause it to point at 0.

The dial starts by pointing at 50.

You could follow the instructions, but your recent required official North Pole secret entrance security training
seminar taught you that the safe is actually a decoy. The actual password is the number of times the dial is left
pointing at 0 after any rotation in the sequence.

For example, suppose the attached document contained the following rotations:

L68
L30
R48
L5
R60
L55
L1
L99
R14
L82
Following these rotations would cause the dial to move as follows:

The dial starts by pointing at 50.
The dial is rotated L68 to point at 82.
The dial is rotated L30 to point at 52.
The dial is rotated R48 to point at 0.
The dial is rotated L5 to point at 95.
The dial is rotated R60 to point at 55.
The dial is rotated L55 to point at 0.
The dial is rotated L1 to point at 99.
The dial is rotated L99 to point at 0.
The dial is rotated R14 to point at 14.
The dial is rotated L82 to point at 32.
Because the dial points at 0 a total of three times during this process, the password in this example is 3.

Analyze the rotations in your attached document. What's the actual password to open the door?
*/

func ReadFileLines(path string) ([]string, error) {
	lines, err := os.ReadFile(path)
	if err != nil {
		log.Fatalf("Error reading file: %v", err)
	}
	return strings.Split(string(lines), "\n"), nil
}

// Ring represents the safe dial
type Ring struct {
	position  int
	size      int
	zeroCount int
}

// mod function that is like Python's modulo behavior
func mod(a, b int) int {
	return (a%b + b) % b
}

// NewRing creates a new Ring initialized to position 50
func NewRing() *Ring {
	return &Ring{
		position:  50,
		size:      100,
		zeroCount: 0,
	}
}

// RotateRingLeft rotates the ring left by the given distance accounting for wrap-around via modulo
func RotateRingLeft(r *Ring, distance int) {
	r.position = mod(r.position-distance, r.size)
	if r.position == 0 {
		print("Landed on zero going left!\n")
		r.zeroCount++
	}
}

// RotateRingRight rotates the ring right by the given distance accounting for wrap-around
func RotateRingRight(r *Ring, distance int) {
	r.position = mod(r.position+distance, r.size)
	if r.position == 0 {
		print("Landed on zero going right!\n")
		r.zeroCount++
	}
}

/*
--- Part Two ---
You're sure that's the right password, but the door won't open. You knock, but nobody answers. You build a snowman
while you think.

As you're rolling the snowballs for your snowman, you find another security document that must have fallen into the
snow:

"Due to newer security protocols, please use password method 0x434C49434B until further notice."

You remember from the training seminar that "method 0x434C49434B" means you're actually supposed to count the number of
times any click causes the dial to point at 0, regardless of whether it happens during a rotation or at the end of one.

Following the same rotations as in the above example, the dial points at zero a few extra times during its rotations:

The dial starts by pointing at 50.
The dial is rotated L68 to point at 82; during this rotation, it points at 0 once.
The dial is rotated L30 to point at 52.
The dial is rotated R48 to point at 0.
The dial is rotated L5 to point at 95.
The dial is rotated R60 to point at 55; during this rotation, it points at 0 once.
The dial is rotated L55 to point at 0.
The dial is rotated L1 to point at 99.
The dial is rotated L99 to point at 0.
The dial is rotated R14 to point at 14.
The dial is rotated L82 to point at 32; during this rotation, it points at 0 once.
In this example, the dial points at 0 three times at the end of a rotation, plus three more times during a rotation.
So, in this example, the new password would be 6.

Be careful: if the dial were pointing at 50, a single rotation like R1000 would cause the dial to point at 0 ten times
before returning back to 50!

Using password method 0x434C49434B, what is the password to open the door?
*/

// I'm sure there's a fancier way to do this, but the brute force way will have to do for now.
// New methods on Ring will decrement and check for zeroes during rotation.

type CountingRing struct {
	position  int
	size      int
	zeroCount int
}

func NewCountingRing() *CountingRing {
	return &CountingRing{
		position:  50,
		size:      100,
		zeroCount: 0,
	}
}

func (ring *CountingRing) RotateLeft(steps int) {
	// We want to wrap around the ring and count zeroes
	for i := 0; i < steps; i++ {
		ring.position = (ring.position - 1 + ring.size) % ring.size
		if ring.position == 0 {
			ring.zeroCount++
		}
	}
}

func (ring *CountingRing) RotateRight(steps int) {
	// We want to wrap around the ring and count zeroes
	for i := 0; i < steps; i++ {
		ring.position = (ring.position + 1) % ring.size
		if ring.position == 0 {
			ring.zeroCount++
		}
	}
}

// Part One solution
func main() {
	doPartOne()
	doPartTwo()
}

// Part One solution
func doPartOne() {
	lines, err := ReadFileLines("2025/01/input.txt")
	if err != nil {
		log.Fatalf("Error reading input file: %v", err)
	}

	ring := NewRing()
	for _, line := range lines {
		if len(line) < 2 {
			continue
		}
		direction := line[0]
		var distance int
		_, err := fmt.Sscanf(line[1:], "%d", &distance)
		if err != nil {
			log.Fatalf("Error parsing line '%s': %v", line, err)
		}
		if direction == 'L' {
			RotateRingLeft(ring, distance)
		} else if direction == 'R' {
			RotateRingRight(ring, distance)
		} else {
			log.Fatalf("Invalid direction '%c' in line '%s'", direction, line)
		}
		//fmt.Printf("After %s%d, position: %d, zeroCount: %d\n", string(direction), distance, ring.position, ring.zeroCount)
	}
	fmt.Printf("Final zero count (password): %d\n", ring.zeroCount)

}

// Part Two solution
func doPartTwo() {
	lines, err := ReadFileLines("2025/01/input.txt")
	if err != nil {
		log.Fatalf("Error reading input file: %v", err)
	}

	ring := NewCountingRing()
	for _, line := range lines {
		if len(line) < 2 {
			continue
		}
		direction := line[0]
		var distance int
		_, err := fmt.Sscanf(line[1:], "%d", &distance)
		if err != nil {
			log.Fatalf("Error parsing line '%s': %v", line, err)
		}
		if direction == 'L' {
			ring.RotateLeft(distance)
		} else if direction == 'R' {
			ring.RotateRight(distance)
		} else {
			log.Fatalf("Invalid direction '%c' in line '%s'", direction, line)
		}
		//fmt.Printf("After %s%d, position: %d, zeroCount: %d\n", string(direction), distance, ring.position, ring.zeroCount)
	}
	fmt.Printf("Final zero count (password): %d\n", ring.zeroCount)

}
