package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

const (
	QNUM    = 16
	PT1TEST = true
	PT1PROD = true
	PT2TEST = true
	PT2PROD = true
)

func check(e error) {
	if e != nil {
		panic(e)
	}
}

func main() {
	testDat, err := os.ReadFile(fmt.Sprintf("%d.test_input", QNUM))
	check(err)
	testRows := parseToRows(string(testDat))
	runCase("test", testRows, PT1TEST, PT2TEST)

	prodDat, err := os.ReadFile(fmt.Sprintf("%d.input", QNUM))
	check(err)
	prodRows := parseToRows(string(prodDat))
	runCase("prod", prodRows, PT1PROD, PT2PROD)
}

func parseToRows(raw string) []string {
	rows := strings.Split(raw, "\n")
	return rows
}

func runCase(caseName string, input []string, pt1 bool, pt2 bool) {
	var nodeMap = map[string]node{}
	for _, row := range input {
		// Break down line into components
		valveName := row[len("Valve "):len("Valve AA")]
		flowRate, _ := strconv.Atoi(strings.Split(row, ";")[0][len("Valve AA has flow rate="):])
		destinationsStr := strings.Split(row, ";")[1]
		var destinationsList = []string{}
		if destinationsStr[:len(" tunnels")] == " tunnels" {
			destinationsList = strings.Split(destinationsStr[len(" tunnels lead to valves "):], ", ")
		} else {
			destinationsList = strings.Split(destinationsStr[len(" tunnel leads to valve "):], ", ")
		}
		nodeMap[valveName] = node{flowRate, destinationsList, map[string]int{}}
		for _, d := range destinationsList {
			nodeMap[valveName].DestinationMap[d] = 1
		}
	}
	for k, v := range nodeMap {
		newKeys := v.ImmediateDestinations
		currDepth := 2
		for len(v.DestinationMap) < len(nodeMap)-1 {
			nextNewKeys := []string{}
			for _, newKey := range newKeys {
				for _, destinationKey := range nodeMap[newKey].ImmediateDestinations {
					if _, ok := v.DestinationMap[destinationKey]; !ok && k != destinationKey {
						v.DestinationMap[destinationKey] = currDepth
						nextNewKeys = append(nextNewKeys, destinationKey)
					}
				}
			}
			newKeys = nextNewKeys
			currDepth += 1
		}
	}
	// Remove entries other than "AA" with 0 pressure.
	for k, v := range nodeMap {
		for k1, _ := range v.DestinationMap {
			if v2, ok := nodeMap[k1]; !ok || v2.Pressure == 0 {
				delete(v.DestinationMap, k1)
			}
		}
		if v.Pressure == 0 && k != "AA" {
			delete(nodeMap, k)
		}
	}

	if pt1 {
		res := getMaxPressure(
			30,
			0,
			"AA",
			nodeMap,
			map[string]bool{},
		)
		print(fmt.Sprintf("%s pt1: %d\n", caseName, res))
	}

	if pt2 {
		res := getMaxPressure2(
			nodeMap,
		)
		print(fmt.Sprintf("%s pt2: %d\n", caseName, res))
	}
}

func getMaxPressure(daysLeft int, pressureSoFar int, currentNode string, nodeMap map[string]node, valves map[string]bool) int {
	considerations := []string{}
	for _, k := range keys(nodeMap) {
		if _, ok := valves[k]; !ok && k != "AA" {
			considerations = append(considerations, k)
		}
	}
	bestPressure := pressureSoFar
	for _, c := range considerations {
		newDaysLeft := daysLeft - nodeMap[currentNode].DestinationMap[c] - 1
		if newDaysLeft < 0 {
			continue
		}
		dailyPressure := nodeMap[c].Pressure
		newValves := copy(valves)
		newValves[c] = true
		bestPressure = IntMax(bestPressure, getMaxPressure(
			newDaysLeft,
			pressureSoFar+newDaysLeft*dailyPressure,
			c,
			nodeMap,
			newValves,
		))
	}
	return bestPressure
}

func getMaxPressure2(nodeMap map[string]node) int {
	// Create a blacklist of every random item for Part 1.  But include the first entry on it deterministically, since the second can choose whether to use it.
	// This will reduce a lot of redundancy.
	allDestinations := []string{}
	for k := range nodeMap {
		if k != "AA" {
			allDestinations = append(allDestinations, k)
		}
	}
	// Remove 1 digit because the first entry is always in the blacklist of A.
	permutations := Int2Pow(len(allDestinations) - 1)
	bestSum := 0
	for i := 0; i < permutations; i++ {
		if i%100 == 0 {
			print(fmt.Sprintf("\t%d/%d...\n", i, permutations))
		}
		blackListA := map[string]bool{allDestinations[0]: true}
		for j := range allDestinations {
			if i&(1<<(j)) != 0 {
				// Include i+1 in the blacklist
				blackListA[allDestinations[j]] = true
			} // else exclude i+1 from the blacklist
		}
		blackListB := map[string]bool{}
		for _, k := range allDestinations {
			if _, ok := blackListA[k]; !ok {
				blackListB[k] = true
			}
		}

		bestSum = IntMax(
			bestSum,
			getMaxPressure(26, 0, "AA", nodeMap, blackListA)+getMaxPressure(26, 0, "AA", nodeMap, blackListB),
		)
	}
	return bestSum
}

type node struct {
	Pressure              int
	ImmediateDestinations []string
	DestinationMap        map[string]int
}

func keys(inMap map[string]node) []string {
	res := []string{}
	for k := range inMap {
		res = append(res, k)
	}
	return res
}
func keysb(inMap map[string]bool) []string {
	res := []string{}
	for k := range inMap {
		res = append(res, k)
	}
	return res
}
func copy(inMap map[string]bool) map[string]bool {
	retMap := map[string]bool{}
	for k, v := range inMap {
		retMap[k] = v
	}
	return retMap
}
func IntMax(x1 int, x2 int) int {
	if x1 > x2 {
		return x1
	}
	return x2
}
func Int2Pow(x int) int {
	pow := 1
	for i := 0; i < x; i++ {
		pow *= 2
	}
	return pow
}
