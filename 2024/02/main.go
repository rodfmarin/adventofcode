package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

/*
--- Day 2: Red-Nosed Reports ---
Fortunately, the first location The Historians want to search isn't a long walk from the Chief Historian's office.

While the Red-Nosed Reindeer nuclear fusion/fission plant appears to contain no sign of the Chief Historian, the
engineers there run up to you as soon as they see you. Apparently, they still talk about the time Rudolph was saved
through molecular synthesis from a single electron.

They're quick to add that - since you're already here - they'd really appreciate your help analyzing some unusual data
from the Red-Nosed reactor. You turn to check if The Historians are waiting for you, but they seem to have already
divided into groups that are currently searching every corner of the facility. You offer to help with the unusual data.

The unusual data (your puzzle input) consists of many reports, one report per line. Each report is a list of numbers
called levels that are separated by spaces. For example:

7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
This example data contains six reports each containing five levels.

The engineers are trying to figure out which reports are safe. The Red-Nosed reactor safety systems can only tolerate
levels that are either gradually increasing or gradually decreasing. So, a report only counts as safe if both of the
following are true:

The levels are either all increasing or all decreasing.
Any two adjacent levels differ by at least one and at most three.
In the example above, the reports can be found safe or unsafe by checking those rules:

7 6 4 2 1: Safe because the levels are all decreasing by 1 or 2.
1 2 7 8 9: Unsafe because 2 7 is an increase of 5.
9 7 6 2 1: Unsafe because 6 2 is a decrease of 4.
1 3 2 4 5: Unsafe because 1 3 is increasing but 3 2 is decreasing.
8 6 4 4 1: Unsafe because 4 4 is neither an increase or a decrease.
1 3 6 7 9: Safe because the levels are all increasing by 1, 2, or 3.
So, in this example, 2 reports are safe.

Analyze the unusual data from the engineers. How many reports are safe?

--- Part Two ---
The engineers are surprised by the low number of safe reports until they realize they forgot to tell you about the
Problem Dampener.

The Problem Dampener is a reactor-mounted module that lets the reactor safety systems tolerate a single bad level in
what would otherwise be a safe report. It's like the bad level never happened!

Now, the same rules apply as before, except if removing a single level from an unsafe report would make it safe, the
report instead counts as safe.

More of the above example's reports are now safe:

7 6 4 2 1: Safe without removing any level.
1 2 7 8 9: Unsafe regardless of which level is removed.
9 7 6 2 1: Unsafe regardless of which level is removed.
1 3 2 4 5: Safe by removing the second level, 3.
8 6 4 4 1: Safe by removing the third level, 4.
1 3 6 7 9: Safe without removing any level.
Thanks to the Problem Dampener, 4 reports are actually safe!

Update your analysis by handling situations where the Problem Dampener can remove a single level from unsafe reports.
How many reports are now safe?
*/

type Report struct {
	levels []int
}

func readReportsFromFile(filename string) ([]Report, error) {
	file, err := os.Open(filename)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	var reports []Report
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		parts := strings.Fields(line)
		var levels []int
		for _, part := range parts {
			level, err := strconv.Atoi(part)
			if err != nil {
				return nil, err
			}
			levels = append(levels, level)
		}
		reports = append(reports, Report{levels: levels})
	}

	if err := scanner.Err(); err != nil {
		return nil, err
	}

	return reports, nil
}

func (r *Report) isSafe() bool {
	// Base case: check if the report is already safe
	if checkSafety(r.levels) {
		return true
	}

	// Try applying the Problem Dampener to each level
	for i := 0; i < len(r.levels); i++ {
		// Create a new slice excluding the current level
		modifiedLevels := make([]int, 0, len(r.levels)-1)
		modifiedLevels = append(modifiedLevels, r.levels[:i]...)   // Add levels before index i
		modifiedLevels = append(modifiedLevels, r.levels[i+1:]...) // Add levels after index i

		if checkSafety(modifiedLevels) {
			return true // Safe after removing one level
		}
	}

	// If no safe configuration is found, return false
	return false
}

func checkSafety(levels []int) bool {
	if len(levels) < 2 {
		return false // A single level cannot form a valid sequence
	}

	increasing := true
	decreasing := true
	for i := 1; i < len(levels); i++ {
		diff := levels[i] - levels[i-1]
		if abs(diff) < 1 || abs(diff) > 3 {
			return false // Invalid difference
		}
		if levels[i] > levels[i-1] {
			decreasing = false
		} else if levels[i] < levels[i-1] {
			increasing = false
		}
	}

	return increasing || decreasing
}

func abs(x int) int {
	if x < 0 {
		return -x
	}
	return x
}

func main() {
	reports, err := readReportsFromFile("input.txt")
	if err != nil {
		panic(err)
	}

	safeReports := 0
	for _, report := range reports {
		fmt.Printf("Checking report: %v\n", report.levels)
		if report.isSafe() {
			fmt.Printf("Report is safe: %v\n", report.levels)
			safeReports++
		} else {
			fmt.Printf("Report is unsafe: %v\n", report.levels)
		}
	}

	fmt.Printf("Total safe reports: %d\n", safeReports)
}
