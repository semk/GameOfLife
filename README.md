# Conway's Game of Life

The Game of Life, also known simply as Life, is a cellular automaton devised by the British mathematician John Horton Conway in 1970. The "game" is a zero-player game, meaning that its evolution is determined by its initial state, requiring no further input. One interacts with the Game of Life by creating an initial configuration and observing how it evolves.

This application is written in PyQT to simulate Conway's Game of Life using the popular cell patterns.

## Rules of the Game

The universe of the Game of Life is an infinite two-dimensional orthogonal grid of square cells, each of which is in one of two possible states, alive or dead. Every cell interacts with its eight neighbours, which are the cells that are horizontally, vertically, or diagonally adjacent. At each step in time, the following transitions occur:

1. Any live cell with fewer than two live neighbours dies, as if caused by under-population.
2. Any live cell with two or three live neighbours lives on to the next generation.
3. Any live cell with more than three live neighbours dies, as if by overcrowding.
4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.

## Prerequisites

Install PyQt4:-

Widows: Install PyQt4 binaries from [here](http://www.riverbankcomputing.com/software/pyqt/download)
Linux: `sudo apt-get install python-qt4` (on Debian distributions) or `sudo yum install PyQt4` (on RPM distributions)
Mac OSX: Install [PyQtX](http://sourceforge.net/projects/pyqtx/)

## License

All source code is licensed under FreeBSD License. Please refer COPYING.