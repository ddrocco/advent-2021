package main

import (
	"fmt"
	"math"
	"os"
	"strconv"
	"strings"
)

const (
	QNUM    = 15
	PT1TEST = false
	PT1PROD = false
	PT2TEST = false
	PT2PROD = true

	PT1_YROW_TEST = 10
	PT1_YROW_PROD = 2000000

	PT2_MAX_COORD_TEST = 20
	PT2_MAX_COORD_PROD = 4000000
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
	runCase("test", testRows, PT1TEST, PT2TEST, PT1_YROW_TEST, PT2_MAX_COORD_TEST)

	prodDat, err := os.ReadFile(fmt.Sprintf("%d.input", QNUM))
	check(err)
	prodRows := parseToRows(string(prodDat))
	runCase("prod", prodRows, PT1PROD, PT2PROD, PT1_YROW_PROD, PT2_MAX_COORD_PROD)
}

func parseToRows(raw string) []string {
	rows := strings.Split(raw, "\n")
	return rows
}

type sensor struct {
	X            int
	Y            int
	BuffDistance int
}

func runCase(caseName string, input []string, pt1 bool, pt2 bool, pt1_yrow int, pt2_max_coord int) {
	if pt1 {
		var sensors []sensor = []sensor{}
		blacklistX := map[int]bool{}
		minPossibleX := math.MaxInt
		maxPossibleX := math.MinInt
		for _, row := range input {
			// Break down line into components
			rowComps := strings.Split(row, ":")

			// Parse sensor coordinates
			sensorCoordsStr := rowComps[0][len("Sensor at "):]
			sensorCoordsComps := strings.Split(sensorCoordsStr, ", ")
			sensorX, _ := strconv.Atoi(sensorCoordsComps[0][len("x="):])
			sensorY, _ := strconv.Atoi(sensorCoordsComps[1][len("y="):])

			// Parse beacon coordinates
			beaconCoordsStr := rowComps[1][len(" closest beacon is at "):]
			beaconCoordsComps := strings.Split(beaconCoordsStr, ", ")
			beaconX, _ := strconv.Atoi(beaconCoordsComps[0][len("x="):])
			beaconY, _ := strconv.Atoi(beaconCoordsComps[1][len("y="):])

			buffDistance := Manhattan(sensorX, sensorY, beaconX, beaconY)
			s := sensor{
				sensorX,
				sensorY,
				buffDistance,
			}
			sensors = append(sensors, s)
			maxPossibleX = IntMax(maxPossibleX, sensorX+buffDistance)
			minPossibleX = IntMin(minPossibleX, sensorX-buffDistance)
			if beaconY == pt1_yrow {
				blacklistX[beaconX] = true
			}
			// print(fmt.Sprintf("(%d,%d): %d\n", s.X, s.Y, s.BuffDistance))
		}

		res := 0
		for x := minPossibleX; x < maxPossibleX+1; x++ {
			if blacklistX[x] {
				continue
			}
			possible := true
			for _, s := range sensors {
				if Manhattan(x, pt1_yrow, s.X, s.Y) <= s.BuffDistance {
					possible = false
					/*print(
						fmt.Sprintf("x=%d: M(%d, %d, %d, %d) = %d <= %d [ADDED]\n",
							x, x, pt1_yrow, s.X, s.Y, Manhattan(x, pt1_yrow, s.X, s.Y), s.BuffDistance),
					)*/
					break
				} else {
					/*print(
						fmt.Sprintf("\tx=%d: M(%d, %d, %d, %d) = %d > %d [NOT ADDED]\n",
							x, x, pt1_yrow, b.X, b.Y, Manhattan(x, pt1_yrow, b.X, b.Y), b.BuffDistance),
					)*/
				}
			}
			if !possible {
				res += 1
			} else {
				// print(fmt.Sprintf("x=%d: [NONE]\n", x))
			}
		}
		print(fmt.Sprintf("%s pt1: %d\n", caseName, res))
	}

	if pt2 {
		var sensors []sensor = []sensor{}
		for _, row := range input {
			// Break down line into components
			rowComps := strings.Split(row, ":")

			// Parse sensor coordinates
			sensorCoordsStr := rowComps[0][len("Sensor at "):]
			sensorCoordsComps := strings.Split(sensorCoordsStr, ", ")
			sensorX, _ := strconv.Atoi(sensorCoordsComps[0][len("x="):])
			sensorY, _ := strconv.Atoi(sensorCoordsComps[1][len("y="):])

			// Parse beacon coordinates
			beaconCoordsStr := rowComps[1][len(" closest beacon is at "):]
			beaconCoordsComps := strings.Split(beaconCoordsStr, ", ")
			beaconX, _ := strconv.Atoi(beaconCoordsComps[0][len("x="):])
			beaconY, _ := strconv.Atoi(beaconCoordsComps[1][len("y="):])

			buffDistance := Manhattan(sensorX, sensorY, beaconX, beaconY)
			s := sensor{
				sensorX,
				sensorY,
				buffDistance,
			}
			sensors = append(sensors, s)
		}
		solutions := map[coordinates]bool{}
		for _, s1 := range sensors {
			for _, c := range getManhattanAtRange(s1.X, s1.Y, s1.BuffDistance+1) {
				if solutions[coordinates{c.X, c.Y}] {
					continue
				}
				if c.X < 0 || c.X > pt2_max_coord || c.Y < 0 || c.Y > pt2_max_coord {
					continue
				}
				ok := true
				for _, s2 := range sensors {
					d := Manhattan(c.X, c.Y, s2.X, s2.Y)
					if d <= s2.BuffDistance {
						ok = false
						break
					}
				}
				if ok {
					solutions[coordinates{
						c.X,
						c.Y,
					}] = true
				}
			}
		}
		i := 0
		for c, _ := range solutions {
			if i > 5 {
				break
			} else {
				i++
			}
			pt2Calc := 4000000*c.X + c.Y
			print(fmt.Sprintf("%s pt2: %d (%d,%d)\n", caseName, pt2Calc, c.X, c.Y))
		}
	}
	return
}

func Manhattan(x1 int, y1 int, x2 int, y2 int) int {
	return IntAbs(x2-x1) + IntAbs(y2-y1)
}

// Abs returns the absolute value of x.
func IntAbs(x int) int {
	if x < 0 {
		return -x
	}
	return x
}

func IntMax(x1 int, x2 int) int {
	if x1 > x2 {
		return x1
	}
	return x2
}
func IntMin(x1 int, x2 int) int {
	if x1 < x2 {
		return x1
	}
	return x2
}

type coordinates struct {
	X int
	Y int
}

func getManhattanAtRange(x int, y int, r int) []coordinates {
	coords := []coordinates{}
	for i := 0; i < r; i++ {
		// left-to-up
		coords = append(coords, coordinates{
			x - r + i,
			y + i,
		})
		// up-to-right
		coords = append(coords, coordinates{
			x + i,
			y + r - i,
		})
		// right-to-down
		coords = append(coords, coordinates{
			x + r - i,
			y - i,
		})
		// down-to-left
		coords = append(coords, coordinates{
			x - i,
			y - r + i,
		})
	}
	return coords
}
