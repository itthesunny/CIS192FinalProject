import numpy as np
import random
import math

SUDOKU_DIMENSIONS = 9
BOX_SIZE = int(math.sqrt(SUDOKU_DIMENSIONS))


# Generator for random number
def generateRandom():
    while (True):
        yield random.randint(1, 9)

# Vertical check if piece fits


def verticalCheck(row, col, val, resolvedSudoku):
    for i in range(SUDOKU_DIMENSIONS):
        if (resolvedSudoku[i, col] == val):
            return -1
    return 1

# Vertical check if piece fits


def horizontalCheck(row, col, val, resolvedSudoku):
    for i in range(SUDOKU_DIMENSIONS):
        if (resolvedSudoku[row, i] == val):
            return -1
    return 1


def boxCheck(i, j, val, resolvedSudoku):
    # Determine how mhuch to go in X
    rowStart = int(i / BOX_SIZE)
    colStart = int(j / BOX_SIZE)
    # Box checking body
    for k in range(BOX_SIZE):
        rowValue = BOX_SIZE * rowStart + k
        for l in range(BOX_SIZE):
            colValue = BOX_SIZE * colStart + l

            if (resolvedSudoku[rowValue, colValue] == val):
                return -1
    return 1


class Sudoku():

    def __init__(self, value):
        self.numClues = 16
        self.sudoku = np.ones(
            shape=(
                SUDOKU_DIMENSIONS,
                SUDOKU_DIMENSIONS),
            dtype=int) * -1

        if (value == 'H'):
            self.numClues = 13
        if (value == 'M'):
            self.numClues = 15

        # Create the generator
        generator = generateRandom()

        while (self.numClues > 0):
            randomX = next(generator) - 1
            randomY = next(generator) - 1

            if (self.sudoku[randomX, randomY] >= 0):
                continue

            # After finding free index find a value
            while (True):
                randVal = next(generator) - 1

                hval = horizontalCheck(randomX, randomY, randVal, self.sudoku)
                vval = verticalCheck(randomX, randomY, randVal, self.sudoku)
                bval = boxCheck(randomX, randomY, randVal, self.sudoku)

                if (hval < 0 or vval < 0 or bval < 0):
                    continue

                self.sudoku[randomX, randomY] = randVal
                self.numClues = self.numClues - 1
                break
            print(self.numClues)

        print(self.sudoku + 1)

    # Check for equality for an answer --> Override equality
    def __eq__(self, candidate):

        for i in range(SUDOKU_DIMENSIONS):
            for j in range(SUDOKU_DIMENSIONS):

                if (self.sudoku[i, j] < 0):
                    continue

                # none equal to our answer
                if (self.sudoku[i, j] != candidate[i, j]):
                    return False

        # Now check if correct!
        for i in range(SUDOKU_DIMENSIONS):
            for j in range(SUDOKU_DIMENSIONS):

                hval = horizontalCheck(i, j, candidate[i, j], candidate)
                vval = verticalCheck(i, j, candidate[i, j], candidate)
                bval = boxCheck(i, j, candidate[i, j], candidate)

                if (hval < 0 or vval < 0 or bval < 0):
                    return -1

        return 1
