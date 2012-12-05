#! /usr/bin/env python
#
# Implementation Game of Life in Python.
#
# @author: Sreejith K <sreejithemk@gmail.com>
# Created On 25th May 2012
#
# Licensed under FreeBSD license. Refer COPYING for more info.


import itertools
import random


class Universe(object):
    """Implements a Universe of living/dead cells.
    """
    def __init__(self, auto=False, rows=10, columns=10, expand=False):
        """Initialize the Universe.
        """
        # if true, the universe will automatically expand when necessary
        self.expand = expand
        # if auto, fills the universe grid with random cells.
        if auto:
            self.autoFill(rows, columns)

    def autoFill(self, rows, columns):
        """Automatically fill the Universe with random cells.
        """
        population = []
        for _ in range(rows):
            row = []
            for _ in range(columns):
                cell = Cell(random.choice([AliveState(), DeadState()]))
                row.append(cell)
            population.append(row)
        self.seed(population)

    def seed(self, population):
        """Seed the Universe with a Cell pattern. Sets neighbor cells
        for each cells.
        """
        self.population = population
        rowMax, colMax = self.getDimension()
        # set neighbor cells.
        for row in self.population:
            rowNum = self.population.index(row)
            for cell in row:
                colNum = row.index(cell)
                [cell.setNeighbor(self.population[i][j]) \
                    for i in range(rowNum-1, rowNum+2) \
                        for j in range(colNum-1, colNum+2) \
                            if ((i, j) != (rowNum, colNum)) and \
                                -1 < i < rowMax and -1 < j < colMax]

    def getDimension(self):
        """Get the dimensions of the Universe.
        """
        return (len(self.population), len(self.population[0]))

    def nextGeneration(self):
        """Move to next generation.
        """
        # Determine the next states for all cells.
        for row in self.population:
            for cell in row:
                cell.computeNextGen()

        # Move to next generation.
        for row in self.population:
            for cell in row:
                cell.updateGen()

        # Check of expansion is needed
        if self.expand:
            self.expandUniverse()

    def expandUniverse(self):
        if any(self.population[0]):
            newRow = len(self.population[0]) * [Cell(DeadState())]
            self.population.insert(0, newRow)
        if any(self.population[-1]):
            newRow = len(self.population[-1]) * [Cell(DeadState())]
            self.population.append(newRow)

        if any([row[0] for row in self.population]):
            map(lambda row: row.insert(0, Cell(DeadState())), self.population)
        if any([row[-1] for row in self.population]):
            map(lambda row: row.append(Cell(DeadState())), self.population)

    def __eq__(self, other):
        if isinstance(other, Universe) and (self.getDimension() == other.getDimension()):
            for a, b in itertools.izip(self.population, other.population):
                for c, d in itertools.izip(a, b):
                    if c.isAlive() != d.isAlive():
                        return False
            return True
        else:
            return False

    def __str__(self):
        return '\n'.join([' '.join([str(cell) for cell in row]) for row in self.population])


class CellState(object):
    """Abstract CellState class
    """
    def isAlive(self):
        """Checks whether the state is Live
        """
        raise NotImplementedError


class DeadState(CellState):
    """State representing a Dead Cell
    """
    def __init__(self):
        self.state = False

    def isAlive(self):
        """Checks whether the state is LiveState
        """
        return self.state

    def __nonzero__(self):
        return False


class AliveState(CellState):
    """State representing Live Cell
    """
    def __init__(self):
        self.state = True

    def isAlive(self):
        """Checks whether the state is LiveState
        """
        return self.state

    def __nonzero__(self):
        return True


class GenMap(object):
    """A class to track current and next cell states 
    using State Pattern.
    """
    def __init__(self, currentState=None):
        self.currentState = currentState
        self.nextState = currentState

    def updateGen(self):
        self.currentState = self.nextState

    def getCurrentState(self):
        return self.currentState 

    def setNextStateToAlive(self):
        self.nextState = AliveState()

    def setNextStateToDead(self):
        self.nextState = DeadState()


class Cell(object):
    """Represents a Cell. Either DeadState or AliveState.
    """
    def __init__(self, state=AliveState()):
        self.genMap = GenMap(currentState=state)
        self.neighbors = []

    def setNeighbor(self, cell):
        """Add neighbor cells.
        """
        self.neighbors.append(cell)

    def numOfLiveNeighbors(self):
        """Find the number of live neighbors for this cell.
        """
        return len(filter(lambda x: x.isAlive(), self.neighbors))

    def computeNextGen(self):
        """Determines whether this cell should live or die based on the
        number of live neighbors.
        """
        aliveNeighbors = self.numOfLiveNeighbors()
        if aliveNeighbors < 2 or aliveNeighbors > 3:
            self.genMap.setNextStateToDead()
        if not self.isAlive() and aliveNeighbors == 3:
            self.genMap.setNextStateToAlive()

    def isAlive(self):
        """Checks whether this cell is alive.
        """
        return self.genMap.getCurrentState().isAlive()

    def updateGen(self):
        """Moves to next generation.
        """
        self.genMap.updateGen()

    def __str__(self):
        return self.isAlive() and 'X' or '-'

    __nonzero__ = isAlive


def test():
    """Test with sample inputs.
    """
    u = Universe()
    world = [
        [Cell(AliveState()), Cell(AliveState())],
        [Cell(AliveState()), Cell(AliveState())],
        ]
    u.seed(world)
    print 'INPUT (Block Pattern)'
    print u
    u.nextGeneration()
    print 'OUTPUT'
    print u, '\n'

    world = [
        [Cell(AliveState()), Cell(AliveState()), Cell(DeadState())],
        [Cell(AliveState()), Cell(DeadState()), Cell(AliveState())],
        [Cell(DeadState()), Cell(AliveState()), Cell(DeadState())],
        ]
    u.seed(world)
    print 'INPUT (Boat Pattern)'
    print u
    u.nextGeneration()
    print 'OUTPUT'
    print u, '\n'

    world = [
        [Cell(DeadState()), Cell(AliveState()), Cell(DeadState())],
        [Cell(DeadState()), Cell(AliveState()), Cell(DeadState())],
        [Cell(DeadState()), Cell(AliveState()), Cell(DeadState())],
        ]
    u.seed(world)
    print 'INPUT (Blinker Pattern)'
    print u
    u.nextGeneration()
    print 'OUTPUT'
    print u, '\n'

    world = [
        [Cell(DeadState()), Cell(DeadState()), Cell(DeadState()), Cell(DeadState())],
        [Cell(DeadState()), Cell(AliveState()), Cell(AliveState()), Cell(AliveState())],
        [Cell(AliveState()), Cell(AliveState()), Cell(AliveState()), Cell(DeadState())],
        [Cell(DeadState()), Cell(DeadState()), Cell(DeadState()), Cell(DeadState())]
        ]
    u.seed(world)
    print 'INPUT (Toad Pattern)'
    print u
    u.nextGeneration()
    print 'OUTPUT'
    print u, '\n'

    print '4 generations of Toad Pattern'
    for i in range(4):
        u.nextGeneration()
        print u, '\n'

    print '4 generations of a Random Cell Pattern'
    u = Universe(auto=True, expand=True)
    for i in range(4):
        u.nextGeneration()
        print u, '\n'

if __name__ == '__main__':
    test()
