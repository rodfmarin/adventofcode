package main

import (
	"fmt"
	"log"
	"os"
	"sort"
	"strings"
)

/*
--- Day 5: Cafeteria ---
As the forklifts break through the wall, the Elves are delighted to discover that there was a cafeteria on the other
side after all.

You can hear a commotion coming from the kitchen. "At this rate, we won't have any time left to put the wreaths up in
the dining hall!" Resolute in your quest, you investigate.

"If only we hadn't switched to the new inventory management system right before Christmas!" another Elf exclaims.
You ask what's going on.

The Elves in the kitchen explain the situation: because of their complicated new inventory management system, they
can't figure out which of their ingredients are fresh and which are spoiled. When you ask how it works, they give you a
copy of their database (your puzzle input).

The database operates on ingredient IDs. It consists of a list of fresh ingredient ID ranges, a blank line, and a list
of available ingredient IDs. For example:

3-5
10-14
16-20
12-18

1
5
8
11
17
32
The fresh ID ranges are inclusive: the range 3-5 means that ingredient IDs 3, 4, and 5 are all fresh. The ranges can
also overlap; an ingredient ID is fresh if it is in any range.

The Elves are trying to determine which of the available ingredient IDs are fresh. In this example, this is done as
follows:

Ingredient ID 1 is spoiled because it does not fall into any range.
Ingredient ID 5 is fresh because it falls into range 3-5.
Ingredient ID 8 is spoiled.
Ingredient ID 11 is fresh because it falls into range 10-14.
Ingredient ID 17 is fresh because it falls into range 16-20 as well as range 12-18.
Ingredient ID 32 is spoiled.
So, in this example, 3 of the available ingredient IDs are fresh.

Process the database file from the new inventory management system. How many of the available ingredient IDs are fresh?

--- Part Two ---
The Elves start bringing their spoiled inventory to the trash chute at the back of the kitchen.

So that they can stop bugging you when they get new inventory, the Elves would like to know all of the IDs that the
fresh ingredient ID ranges consider to be fresh. An ingredient ID is still considered fresh if it is in any range.

Now, the second section of the database (the available ingredient IDs) is irrelevant. Here are the fresh ingredient ID
ranges from the above example:

3-5
10-14
16-20
12-18
The ingredient IDs that these ranges consider to be fresh are 3, 4, 5, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, and 20.
So, in this example, the fresh ingredient ID ranges consider a total of 14 ingredient IDs to be fresh.

Process the database file again. How many ingredient IDs are considered to be fresh according to the fresh ingredient
ID ranges?
*/

func ReadFileLines(path string) ([]string, error) {
	lines, err := os.ReadFile(path)
	if err != nil {
		log.Fatalf("Error reading file: %v", err)
	}
	return strings.Split(string(lines), "\n"), nil
}

type FreshRange struct {
	start int
	end   int
}

type IngredientID struct {
	id int
}

type Database struct {
	freshRanges  []FreshRange
	availableIDs []IngredientID
}

func ParseLinesToDatabase(lines []string) Database {
	var db Database
	section := 0 // 0 for fresh ranges, 1 for available IDs
	for _, line := range lines {
		line = strings.TrimSpace(line)
		if line == "" {
			section++
			continue
		}
		if section == 0 {
			var r FreshRange
			fmt.Sscanf(line, "%d-%d", &r.start, &r.end)
			db.freshRanges = append(db.freshRanges, r)
		}
		if section == 1 {
			var id IngredientID
			fmt.Sscanf(line, "%d", &id.id)
			db.availableIDs = append(db.availableIDs, id)
		}
	}
	return db
}

func IsFresh(id int, ranges []FreshRange) bool {
	for _, r := range ranges {
		if id >= r.start && id <= r.end {
			return true
		}
	}
	return false
}

func main() {
	doPartOne()
	doPartTwo()
}

func doPartOne() {
	lines, err := ReadFileLines("2025/05/input.txt")
	if err != nil {
		log.Fatalf("Error reading input file: %v", err)
	}

	db := ParseLinesToDatabase(lines)

	freshCount := 0
	for _, id := range db.availableIDs {
		if IsFresh(id.id, db.freshRanges) {
			freshCount++
		}
	}

	fmt.Printf("Total fresh ingredient IDs: %d\n", freshCount)
}

func doPartTwo() {
	// For this part, we need to find all unique fresh IDs from the ranges
	// I think we could build a map to track unique IDs that exist in the ranges
	// Update: lol, those are some really big ranges, runtime will be bad if we do that naively

	// I think the algorithm we want to use here is sort all the ranges by start value,
	// then merge overlapping ranges, and finally sum the lengths of the merged ranges.
	lines, err := ReadFileLines("2025/05/input.txt")
	if err != nil {
		log.Fatalf("Error reading input file: %v", err)
	}

	db := ParseLinesToDatabase(lines)

	// Sort ranges by start value
	sort.Slice(db.freshRanges, func(i, j int) bool {
		return db.freshRanges[i].start < db.freshRanges[j].start
	})

	// Merge overlapping ranges
	var mergedRanges []FreshRange
	for _, r := range db.freshRanges {
		if len(mergedRanges) == 0 || mergedRanges[len(mergedRanges)-1].end < r.start {
			mergedRanges = append(mergedRanges, r)
		} else {
			if r.end > mergedRanges[len(mergedRanges)-1].end {
				mergedRanges[len(mergedRanges)-1].end = r.end
			}
		}
	}

	// Calculate total unique fresh IDs
	totalFreshIDs := 0
	for _, r := range mergedRanges {
		totalFreshIDs += r.end - r.start + 1 // +1 because ranges are inclusive
	}
	fmt.Printf("Total unique fresh ingredient IDs: %d\n", totalFreshIDs)
}
