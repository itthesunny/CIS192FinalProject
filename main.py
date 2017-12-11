import sys
import cmd
import time
from sudokuSolver import setDefiniteSudokuValue
from sudokuSolver import mainSolver
from sudokuSolver import reset
from sudokuMaker import *
SUDOKU_DIMENSIONS = 9

print("Sudoku Solver:For simplicity this program assumes all inputsvalid")

while (True):
    str1 = "Enter 1 if you have sudoku you want me to solve or 2"
    print(str1 + " if you want to solve a sudoku 3 to quit")
    args = input("")
    args = int(args)

    if (args == 3):
        print("Goodbye!")
        exit(0)

    if (args == 2):
        str1 = "Please enter you sudoku in specified format:Write row by"
        print(str1 + " row: If number is not known put - character")

        # get the sudoku
        for i in range(SUDOKU_DIMENSIONS):
            args = input("")
            for j in range(SUDOKU_DIMENSIONS):

                # Check if known
                if (args[j] is '-'):
                    continue

                # set state
                setDefiniteSudokuValue(i, j, int(args[j]) - 1)

        # Solve the sudoku
        mainSolver()
        reset()

    if (args == 1):
        print("Please type H for hard, M for medium and E for easy")
        args = input("")

        print("Here is you sudoku-> 0's are unknows")
        sudoku = Sudoku(args)

        answer = np.ones(
            shape=(
                SUDOKU_DIMENSIONS,
                SUDOKU_DIMENSIONS),
            dtype=int) * -1

        print("Please write you answer row by row")
        for i in range(SUDOKU_DIMENSIONS):
            args = input("")
            for j in range(SUDOKU_DIMENSIONS):

                # set state
                answer[i, j] = int(args[j]) - 1

        # Check for our sudokus answer
        if (sudoku == answer):
            print("Thats correct!")
        else:
            print("Thats wrong")
