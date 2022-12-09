package main

import (
	"fmt"
	"os"
)

func check(e error) {
	if e != nil {
		panic(e)
	}
}

func main() {
	testDat, err := os.ReadFile("9.test_input")
	check(err)
	runCase(string(testDat))

	prodDat, err := os.ReadFile("9.input")
	check(err)
	runCase(string(prodDat))
}

func runCase(input string) {
	print("\n")
	for _, foo := range input {
		fmt.Printf("%c", foo)
		print("\n")
	}
	return
	// Guess I didn't use this.  Womp womp.
}
