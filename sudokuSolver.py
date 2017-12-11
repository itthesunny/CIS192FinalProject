import numpy as np
import random
import math
import copy
import time

# Global headers and constants
SUDOKU_DIMENSIONS = 9
BOX_SIZE = int(math.sqrt(SUDOKU_DIMENSIONS))
isSolved = 0
startTime = 0

# 3 dimensionional sudoku
degreesOfFreedom = int(SUDOKU_DIMENSIONS * SUDOKU_DIMENSIONS)
sudoku = np.ones(
    shape=(
        SUDOKU_DIMENSIONS,
        SUDOKU_DIMENSIONS,
        SUDOKU_DIMENSIONS),
    dtype=int)
resolvedSudoku = np.ones(
    shape=(
        SUDOKU_DIMENSIONS,
        SUDOKU_DIMENSIONS),
    dtype=int) * -1


# Solved square in the sudoku
def setDefiniteSudokuValue(row, col, val):
    global degreesOfFreedom
    resolvedSudoku[row, col] = val

    # Adjust probability sets
    sudoku[row, col, ] = 0
    sudoku[row, col, val] = 1
    degreesOfFreedom = degreesOfFreedom - 1

    # Adjust vertical neighbor probability sets
    for row2 in range(SUDOKU_DIMENSIONS):
        if (row2 == row):
            continue
        sudoku[row2, col, val] = 0

    # Adjust horizontal neighbor probability sets
    for col2 in range(SUDOKU_DIMENSIONS):
        if (col == col2):
            continue
        sudoku[row, col2, val] = 0

    # Adjust box neighbor probability sets
    rowStart = int(row / BOX_SIZE)
    colStart = int(col / BOX_SIZE)

    # Box checking body
    for k in range(BOX_SIZE):
        rowValue = BOX_SIZE * rowStart + k
        for l in range(BOX_SIZE):
            colValue = BOX_SIZE * colStart + l

            if (row == rowValue and col == colValue):
                continue
            sudoku[rowValue, colValue, val] = 0


def verticalUniquePossibilitySet():
    for i in range(SUDOKU_DIMENSIONS):
        for j in range(SUDOKU_DIMENSIONS):
            if (resolvedSudoku[i, j] >= 0):
                continue

            # For each box look at every element in vertical
            probabilitySet = [x for x in range(
                SUDOKU_DIMENSIONS) if sudoku[i, j, x] == 1]

            # Determine if we took a wrong turn
            if (len(probabilitySet) == 0):
                return -1

            if (len(probabilitySet) == 1):
                setDefiniteSudokuValue(i, j, probabilitySet[0])
                continue

            for k in range(SUDOKU_DIMENSIONS):
                if (k == i):
                    continue

                # Get this indexes probability set
                probabilitySetTarget = [x for x in range(
                    SUDOKU_DIMENSIONS) if sudoku[k, j, x] == 1]
                probabilitySet = [
                    x for x in probabilitySet if x not in probabilitySetTarget]

            # Get Vertically Unique probabilities
            if (len(probabilitySet) == 1):
                setDefiniteSudokuValue(i, j, probabilitySet[0])
    return 1


def horizontalUniquePossibilitySet():
    for i in range(SUDOKU_DIMENSIONS):
        for j in range(SUDOKU_DIMENSIONS):
            if (resolvedSudoku[i, j] >= 0):
                continue

            # For each box look at every element in vertical
            probabilitySet = [x for x in range(
                SUDOKU_DIMENSIONS) if sudoku[i, j, x] == 1]

            # Determine if we took a wrong turn
            if (len(probabilitySet) == 0):
                return -1

            if (len(probabilitySet) == 1):
                setDefiniteSudokuValue(i, j, probabilitySet[0])
                continue

            for k in range(SUDOKU_DIMENSIONS):
                if (k == j):
                    continue
                # Get this indexes probability set
                probabilitySetTarget = [x for x in range(
                    SUDOKU_DIMENSIONS) if sudoku[i, k, x] == 1]
                probabilitySet = [
                    x for x in probabilitySet if x not in probabilitySetTarget]

            # Get Vertically Unique probabilities
            if (len(probabilitySet) == 1):
                setDefiniteSudokuValue(i, j, probabilitySet[0])
    return 1


def boxUniquePossibilitySet():
    for i in range(SUDOKU_DIMENSIONS):
        for j in range(SUDOKU_DIMENSIONS):
            if (resolvedSudoku[i, j] >= 0):
                continue

            # Adjust box neighbor probability sets
            rowStart = int(i / BOX_SIZE)
            colStart = int(j / BOX_SIZE)
            probabilitySet = [x for x in range(
                SUDOKU_DIMENSIONS) if sudoku[i, j, x] == 1]

            # Determine if we took a wrong turn
            if (len(probabilitySet) == 0):
                return -1

            # Box checking body
            for k in range(BOX_SIZE):
                rowValue = BOX_SIZE * rowStart + k
                for l in range(BOX_SIZE):
                    colValue = BOX_SIZE * colStart + l

                    if (i == rowValue and j == colValue):
                        continue
                    probabilitySetTarget = [x for x in range(
                        SUDOKU_DIMENSIONS) if sudoku[rowValue, colValue, x] == 1]
                    probabilitySet = [
                        x for x in probabilitySet if x not in probabilitySetTarget]

            # Get Vertically Unique probabilities
            if (len(probabilitySet) == 1):
                setDefiniteSudokuValue(i, j, probabilitySet[0])
    return 1


def forcedGuess(i, j):
    probabilitySet = [x for x in range(
        SUDOKU_DIMENSIONS) if sudoku[i, j, x] == 1]
    global degreesOfFreedom
    global sudoku
    global resolvedSudoku

    backupSudoku = copy.deepcopy(sudoku)
    backupresolvedSudoku = copy.deepcopy(resolvedSudoku)
    backupDOG = copy.deepcopy(degreesOfFreedom)

    for elem in probabilitySet:
        isStuck = 0
        isBad = 0
        setDefiniteSudokuValue(i, j, elem)
        # Continue the loop
        while (True):
            prevDOG = degreesOfFreedom
            vret = verticalUniquePossibilitySet()
            bret = boxUniquePossibilitySet()
            hret = horizontalUniquePossibilitySet()

            # deterministically know of a bad guess
            if (vret < 0 or bret < 0 or hret < 0):
                isBad = 1
                break

            # Stuck again make an other guess
            if (prevDOG == degreesOfFreedom):
                isStuck = 1
                break

            # We are done
            if (degreesOfFreedom == 0):
                print("Done!")
                print(resolvedSudoku + 1)
                executionTime = int(time.time() - startTime)
                exit(1)

        # Make an other guess
        if (isStuck):
            newPair = findLeastProblematic()
            forcedGuess(newPair[0], newPair[1])

        # Restore the state from bad guess
        sudoku = copy.deepcopy(backupSudoku)
        resolvedSudoku = copy.deepcopy(backupresolvedSudoku)
        degreesOfFreedom = copy.deepcopy(backupDOG)


def findLeastProblematic():
    leastEntropy = SUDOKU_DIMENSIONS
    canditateI = -1
    candidateJ = -1

    for i in range(SUDOKU_DIMENSIONS):
        for j in range(SUDOKU_DIMENSIONS):
            if (resolvedSudoku[i, j] >= 0):
                continue

            # Get entropy
            candidate = len(
                [x for x in range(SUDOKU_DIMENSIONS) if sudoku[i, j, x] == 1])
            if (candidate < leastEntropy):
                leastEntropy = candidate
                canditateI = i
                candidateJ = j

    return (canditateI, candidateJ)


def mainSolver():
    global degreesOfFreedom
    global degreesOfFreedomStack
    global resolvedSudokuStack
    global sudokuStack
    global startTime

    prevDegreesOfFreedom = -1
    startTime = time.time()
    print("Starting to solve!")

    while (degreesOfFreedom > 0):
        horizontalUniquePossibilitySet()
        verticalUniquePossibilitySet()
        boxUniquePossibilitySet()

        # Check if stuck
        if (prevDegreesOfFreedom == degreesOfFreedom):
            guessPair = findLeastProblematic()
            val = forcedGuess(guessPair[0], guessPair[1])

            # If code reaches here no solution
            print("Sorry no solution")
            exit(1)

        prevDegreesOfFreedom = degreesOfFreedom

    print(resolvedSudoku + 1)


def reset():
    degreesOfFreedom = int(SUDOKU_DIMENSIONS * SUDOKU_DIMENSIONS)
    sudoku = np.ones(
        shape=(
            SUDOKU_DIMENSIONS,
            SUDOKU_DIMENSIONS,
            SUDOKU_DIMENSIONS),
        dtype=int)
    resolvedSudoku = np.ones(
        shape=(
            SUDOKU_DIMENSIONS,
            SUDOKU_DIMENSIONS),
        dtype=int) * -1
    isSolved = 0
