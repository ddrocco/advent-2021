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
		res, valves := getMaxPressure(
			30,
			0,
			"AA",
			nodeMap,
			map[string]bool{},
		)
		print(fmt.Sprintf("%s pt1: %d (via %s)\n", caseName, res, strings.Join(keysb(valves), ",")))
	}

	if pt2 {
		res, msg := getMaxPressure2(
			26,
			0,
			"AA",
			nodeMap,
			map[string]bool{},
		)
		print(fmt.Sprintf("%s pt2: %d (%s)\n", caseName, res, msg))
	}
}

func getMaxPressure(daysLeft int, pressureSoFar int, currentNode string, nodeMap map[string]node, valves map[string]bool) (int, map[string]bool) {
	considerations := []string{}
	for _, k := range keys(nodeMap) {
		if _, ok := valves[k]; !ok && k != "AA" {
			considerations = append(considerations, k)
		}
	}
	bestPressure := pressureSoFar
	bestValves := valves
	for _, c := range considerations {
		newDaysLeft := daysLeft - nodeMap[currentNode].DestinationMap[c] - 1
		if newDaysLeft < 0 {
			continue
		}
		dailyPressure := nodeMap[c].Pressure
		newValves := copy(valves)
		newValves[c] = true
		cMaxPressure, cMaxValves := getMaxPressure(
			newDaysLeft,
			pressureSoFar+newDaysLeft*dailyPressure,
			c,
			nodeMap,
			newValves,
		)
		if cMaxPressure > bestPressure {
			bestValves = cMaxValves
			bestPressure = cMaxPressure
		}
		bestPressure = IntMax(bestPressure, cMaxPressure)
	}
	return bestPressure, bestValves
}

func getMaxPressure2(daysLeft int, pressureSoFar int, currentNode string, nodeMap map[string]node, valves map[string]bool) (int, string) {
	considerations := []string{}
	for _, k := range keys(nodeMap) {
		if _, ok := valves[k]; !ok && k != "AA" {
			considerations = append(considerations, k)
		}
	}
	bestPressure := pressureSoFar
	pathMsg := "failure"
	for _, c := range considerations {
		newDaysLeft := daysLeft - nodeMap[currentNode].DestinationMap[c] - 1
		if newDaysLeft < 0 {
			continue
		}
		dailyPressure := nodeMap[c].Pressure
		newValves := copy(valves)
		newValves[c] = true
		cMaxPressure, cPathMsg := getMaxPressure2(
			newDaysLeft,
			pressureSoFar+newDaysLeft*dailyPressure,
			c,
			nodeMap,
			newValves,
		)
		if cMaxPressure > bestPressure {
			bestPressure = cMaxPressure
			pathMsg = cPathMsg
		}
	}
	// Consider "being done" and letting the elephant take over, no matter how much you have left to do.
	elephantPressure, elephantValves := getMaxPressure(
		26,
		pressureSoFar,
		"AA",
		nodeMap,
		valves,
	)
	if elephantPressure > bestPressure {
		for k := range valves {
			delete(elephantValves, k)
		}
		return elephantPressure, fmt.Sprintf("[%s]; [%s]", strings.Join(keysb(elephantValves), ","), strings.Join(keysb(valves), ","))
	}
	return bestPressure, pathMsg
}

type node struct {
	Pressure              int
	ImmediateDestinations []string
	DestinationMap        map[string]int
}
type permutation struct {
	// A map entry whose key is an array of strings.
	// Key: AABB implies starting at AA (but not turning it) and then going to BB and turning it.
	//		AABBCC implies starting at AA (but not turning it) and then going to BB and turning it, then going to CC and turning it.
	// AABBCC == AABB + BBCC (with pressure multipliers applied).
	pressureMult     int
	pressureInternal int
	steps            int
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
