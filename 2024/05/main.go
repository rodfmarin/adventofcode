package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"slices"
	"sort"
	"strconv"
	"strings"
)

/*
--- Day 5: Print Queue ---
Satisfied with their search on Ceres, the squadron of scholars suggests subsequently scanning the stationery stacks of
sub-basement 17.

The North Pole printing department is busier than ever this close to Christmas, and while The Historians continue their
search of this historically significant facility, an Elf operating a very familiar printer beckons you over.

The Elf must recognize you, because they waste no time explaining that the new sleigh launch safety manual updates
won't print correctly. Failure to update the safety manuals would be dire indeed, so you offer your services.

Safety protocols clearly indicate that new pages for the safety manuals must be printed in a very specific order.
The notation X|Y means that if both page number X and page number Y are to be produced as part of an update,
page number X must be printed at some point before page number Y.

The Elf has for you both the page ordering rules and the pages to produce in each update (your puzzle input),
but can't figure out whether each update has the pages in the right order.

For example:

47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
The first section specifies the page ordering rules, one per line. The first rule, 47|53, means that if an update
includes both page number 47 and page number 53, then page number 47 must be printed at some point before
page number 53. (47 doesn't necessarily need to be immediately before 53; other pages are allowed to be between them.)

The second section specifies the page numbers of each update. Because most safety manuals are different, the pages
needed in the updates are different too. The first update, 75,47,61,53,29, means that the update consists of
page numbers 75, 47, 61, 53, and 29.

To get the printers going as soon as possible, start by identifying which updates are already in the right order.

In the above example, the first update (75,47,61,53,29) is in the right order:

75 is correctly first because there are rules that put each other page after it: 75|47, 75|61, 75|53, and 75|29.
47 is correctly second because 75 must be before it (75|47) and every other page must be after it
according to 47|61, 47|53, and 47|29.
61 is correctly in the middle because 75 and 47 are before it (75|61 and 47|61)
and 53 and 29 are after it (61|53 and 61|29).
53 is correctly fourth because it is before page number 29 (53|29).
29 is the only page left and so is correctly last.
Because the first update does not include some page numbers, the ordering rules involving
those missing page numbers are ignored.

The second and third updates are also in the correct order according to the rules.
Like the first update, they also do not include every page number, and so only some of the ordering rules apply -
within each update, the ordering rules that involve missing page numbers are not used.

The fourth update, 75,97,47,61,53, is not in the correct order: it would print 75 before 97, which violates
the rule 97|75.

The fifth update, 61,13,29, is also not in the correct order, since it breaks the rule 29|13.

The last update, 97,13,75,29,47, is not in the correct order due to breaking several rules.

For some reason, the Elves also need to know the middle page number of each update being printed.
Because you are currently only printing the correctly-ordered updates, you will need to find the middle page
number of each correctly-ordered update. In the above example, the correctly-ordered updates are:

75,47,61,53,29
97,61,53,29,13
75,29,13
These have middle page numbers of 61, 53, and 29 respectively. Adding these page numbers together gives 143.

Of course, you'll need to be careful: the actual list of page ordering rules is bigger and more complicated than
the above example.

Determine which updates are already in the correct order. What do you get if you add up the middle page number from
those correctly-ordered updates?
*/

func readInput() (rules []string, updates [][]string) {
	file, err := os.Open("input.txt")
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	var section int
	for scanner.Scan() {
		line := scanner.Text()
		if line == "" {
			section++
			continue
		}
		if section == 0 {
			rules = append(rules, line)
		} else if section == 1 {
			updates = append(updates, strings.Split(line, ","))
		}
	}
	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}
	return rules, updates
}

type Rules map[int][]int

func parseRules(rules []string) Rules {
	ruleMap := make(Rules)
	for _, rule := range rules {
		parts := strings.Split(rule, "|")
		if len(parts) != 2 {
			log.Fatalf("Invalid rule format: %s", rule)
		}
		before, _ := strconv.Atoi(parts[0])
		after, _ := strconv.Atoi(parts[1])
		ruleMap[before] = append(ruleMap[before], after)
	}
	return ruleMap
}

func (r Rules) compare(a, b int) int {
	if pagesAfter, ok := r[a]; ok {
		if slices.Contains(pagesAfter, b) {
			return -1 // a should come before b
		}
	}
	if pagesAfter, ok := r[b]; ok {
		if slices.Contains(pagesAfter, a) {
			return 1 // b should come before a
		}
	}
	return 0 // No rule specified
}

// SortPages sorts a slice of page numbers according to the provided rules.
func SortPages(pages []int, rules Rules) {
	sort.Slice(pages, func(i, j int) bool {
		// This anonymous function serves as the 'less' function for sort.Slice.
		// It returns true if the element at index i should come before the element at index j.
		return rules.compare(pages[i], pages[j]) < 0
	})
}

func main() {
	rules, updates := readInput()

	fmt.Println("Rules:", rules)
	// Function to parse the rules into a map
	fmt.Println("Updates:", updates)
	ruleList := parseRules(rules)
	fmt.Println("Parsed Rules:", ruleList)

	var totalMiddle int
	for _, update := range updates {
		if len(update) == 0 {
			continue
		}

		isOrdered := true
		for i := range len(update) - 1 {
			a, _ := strconv.Atoi(update[i])
			b, _ := strconv.Atoi(update[i+1])
			if ruleList.compare(a, b) == -1 {
				//fmt.Println("Update is ordered:", update)
			}
			if ruleList.compare(a, b) == 1 {
				fmt.Println("Update is not ordered:", update)
				fmt.Printf("Page %d should come after page %d\n", a, b)
				isOrdered = false
			}
		}

		if isOrdered {
			// middleIndex := len(update) / 2
			// middlePage, _ := strconv.Atoi(update[middleIndex])
			// totalMiddle += middlePage
		}
		if !isOrdered {
			intUpdate := make([]int, len(update))
			for i, s := range update {
				intUpdate[i], _ = strconv.Atoi(s)
			}
			SortPages(intUpdate, ruleList)
			fmt.Println("Sorted update:", intUpdate)
			middleIndex := len(intUpdate) / 2
			middlePage := intUpdate[middleIndex]
			totalMiddle += middlePage
		}
	}
	fmt.Println("Total middle page number from correctly-ordered updates:", totalMiddle)
	if len(updates) == 0 {
		fmt.Println("No updates found.")
		return
	}

}
