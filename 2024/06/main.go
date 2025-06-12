package main

import (
	"bufio"
	"fmt"
	"os"
)

//
// ..You start by making a map (your puzzle input) of the situation. For example:
//
// ....#.....
// .........#
// ..........
// ..#.......
// .......#..
// ..........
// .#..^.....
// ........#.
// #.........
// ......#...
//
// We'll receive an input like above, and we need to parse it into a map structure.
// The map will be represented as a slice of strings, where each string is a row of the map.
//

type PuzzleMap struct {
	Points    []Point
	Width     int
	Height    int
	Guard     Point
	Obstacle  []Point
	Travelled []Point // Points where the guard has traveled
}

type Point struct {
	x int
	y int
}

func NewPuzzleMap(width, height int) *PuzzleMap {
	return &PuzzleMap{
		Points: make([]Point, 0),
		Width:  width,
		Height: height,
	}
}
func (pm *PuzzleMap) AddPoint(x, y int) {
	if x < 0 || x >= pm.Width || y < 0 || y >= pm.Height {
		return // Out of bounds
	}
	pm.Points = append(pm.Points, Point{x: x, y: y})
}
func (pm *PuzzleMap) SetGuard(x, y int) {
	if x < 0 || x >= pm.Width || y < 0 || y >= pm.Height {
		return // Out of bounds
	}
	pm.Guard = Point{x: x, y: y}
}
func (pm *PuzzleMap) SetObstacle(x, y int) {
	if x < 0 || x >= pm.Width || y < 0 || y >= pm.Height {
		return // Out of bounds
	}
	pm.Obstacle = append(pm.Obstacle, Point{x: x, y: y})
}

// Load the input.txt and parse the map into the PuzzleMap structure.
func (pm *PuzzleMap) LoadFromFile(filename string) error {
	file, err := os.Open(filename)
	if err != nil {
		return fmt.Errorf("failed to open file: %w", err)
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	y := 0
	for scanner.Scan() {
		line := scanner.Text()
		for x, char := range line {
			switch char {
			case '.':
				pm.AddPoint(x, y)
			case '#':
				pm.SetObstacle(x, y)
			case '^':
				pm.SetGuard(x, y)
			}
		}
		y++
	}

	if err := scanner.Err(); err != nil {
		return fmt.Errorf("error reading file: %w", err)
	}
	return nil
}

// String the puzzle map for easy visualization
func (pm *PuzzleMap) String() string {
	result := ""
	for y := 0; y < pm.Height; y++ {
		for x := 0; x < pm.Width; x++ {
			switch {
			case isPointInSlice(x, y, pm.Travelled):
				result += "X"
			case pm.Guard.x == x && pm.Guard.y == y:
				result += "^"
			case isPointInSlice(x, y, pm.Obstacle):
				result += "#"
			default:
				result += "."
			}
		}
		result += "\n"
	}
	return result
}

// Helper function to check if a point is in a slice
func isPointInSlice(x, y int, points []Point) bool {
	for _, p := range points {
		if p.x == x && p.y == y {
			return true
		}
	}
	return false
}

// Method to move the guard in a specific direction, error if out of bounds, update the puzzle map to have an X where the guard was
func (pm *PuzzleMap) MoveGuard(dx, dy int) error {
	newX := pm.Guard.x + dx
	newY := pm.Guard.y + dy

	if newX < 0 || newX >= pm.Width || newY < 0 || newY >= pm.Height {
		return fmt.Errorf("move out of bounds")
	}

	// Mark the old position as travelled
	oldGuard := pm.Guard
	pm.Travelled = append(pm.Travelled, oldGuard)

	pm.Guard = Point{x: newX, y: newY}

	return nil
}

// The Guard Walk Protocol is:
// If there is something directly in front of you, turn right 90 degrees.
// Otherwise, take a step forward.
// In other words, from the starting position, the guard will move in a straight line until it encounters an obstacle, at which point it will turn right and continue moving.
// The guard will continue to move until an obstacle is in front of it, at which point it will turn right and continue moving.
// If the guard reaches beyond the bounds of the map, it will stop moving and return an error. which is the end of the guard's movement.
// The guard will also leave a trail of 'X' where it has been, so we can see its path.
func (pm *PuzzleMap) GuardWalkProtocol() error {
	directions := []Point{
		{0, -1}, // Up
		{1, 0},  // Right
		{0, 1},  // Down
		{-1, 0}, // Left
	}

	currentDirection := 0 // Start facing up

	for {
		nextX := pm.Guard.x + directions[currentDirection].x
		nextY := pm.Guard.y + directions[currentDirection].y

		if nextX < 0 || nextX >= pm.Width || nextY < 0 || nextY >= pm.Height {
			// Set the final position of the guard as travelled
			pm.Travelled = append(pm.Travelled, pm.Guard)
			return fmt.Errorf("guard moved out of bounds")
		}

		if isPointInSlice(nextX, nextY, pm.Obstacle) {
			currentDirection = (currentDirection + 1) % len(directions) // Turn right
			continue
		}

		pm.Travelled = append(pm.Travelled, pm.Guard)
		pm.Guard = Point{x: nextX, y: nextY}
	}
}

// Compact the travelled points to remove duplicates
func compactTravelled(points []Point) []Point {
	uniquePoints := make(map[Point]struct{})
	for _, p := range points {
		uniquePoints[p] = struct{}{}
	}

	result := make([]Point, 0, len(uniquePoints))
	for p := range uniquePoints {
		result = append(result, p)
	}
	return result
}

func doPartOne() {
	// Load the input.txt file from disk and parse the map
	puzzleMap := NewPuzzleMap(130, 130)
	err := puzzleMap.LoadFromFile("input.txt")
	if err != nil {
		fmt.Println("Error loading puzzle map:", err)
		return
	}
	fmt.Println("Puzzle Map Loaded Successfully!")
	fmt.Println(puzzleMap)
	// Move the guard up and then print the map

	// Begin the guard walk protocol
	err = puzzleMap.GuardWalkProtocol()
	if err != nil {
		fmt.Println("Guard has exited the map", err)
		// Print the final state of the puzzle map
		fmt.Println("Final Puzzle Map:")
		fmt.Println("Total Travelled Points:", len(puzzleMap.Travelled))
		// Compact the travelled points to remove duplicates
		puzzleMap.Travelled = compactTravelled(puzzleMap.Travelled)
		fmt.Println("Unique Travelled Points:", len(puzzleMap.Travelled))
		// This gets unreadable with large maps.
		fmt.Println(puzzleMap)
		return
	}
}

func main() {
	doPartOne()
}
