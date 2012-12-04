#! /usr/bin/env python
#
# Simulation of Conway's Game of Life using PyQt
#
# @author: Sreejith K <sreejithemk@gmail.com>
# Created on 4th Dec 2012
#
# Licensed under FreeBSD license. Refer COPYING for more info.


import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import life


DEFAULT_UNIV_X = 40
DEFAULT_UNIV_Y = 40


class UniverseView(QGraphicsView):
    """The Qt Graphics Grid where the whole action takes place.
    """

    def __init__(self):
        QGraphicsView.__init__(self)
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.drawUniverse(DEFAULT_UNIV_X, DEFAULT_UNIV_Y)
        self.timer = QTimer()
        self.timer.timeout.connect(self.rePaint)

    def startAnimation(self, universe):
        self.universe = universe
        self.timer.start(1000)

    def stopAnimation(self):
        self.timer.stop()

    def rePaint(self):
        """Animate the cell generations.
        """
        self.clearScene()
        self.drawUniverse(DEFAULT_UNIV_X, DEFAULT_UNIV_Y)
        self.populateCells()
        self.universe.nextGeneration()

    def clearScene(self):
        """Clear the scene.
        """
        self.scene.clear()

    def drawUniverse(self, rows, columns):
        """Draw the universe grid.
        """
        # self.scene.setSceneRect(QRectF(0, 0, 39, 14))
        # draw vertical lines
        for x in xrange(rows):
            self.scene.addLine(x, 0, x, columns, QPen(Qt.yellow))

        # draw horrizontal lines
        for y in xrange(columns):
            self.scene.addLine(0, y, rows, y, QPen(Qt.yellow))

        self.fitInView(self.scene.itemsBoundingRect());

    def populateCells(self):
        """Populate the grid with living cells.
        """
        # populate the grid with black cells representing life
        for row in self.universe.population:
            rowNum = self.universe.population.index(row)
            for cell in row:
                colNum = row.index(cell)
                if cell.isAlive():
                    self.drawCellAt(rowNum, colNum)

    def drawCellAt(self, x, y):
        """Fill the cell at grid location (x, y)
        """
        item = QGraphicsRectItem(x, y, 1, 1)
        item.setBrush(QBrush(Qt.black))
        self.scene.addItem(item)


class GameOfLifeApp(QDialog):
    """Main Dialog window for GameOfLife
    """

    def __init__(self, parent=None):
        super(GameOfLifeApp, self).__init__(parent)
        # Qt Graphics view where the whole action happens
        self.universeView = UniverseView()

        # set the window layout
        layout = QVBoxLayout()
        layout.addWidget(self.universeView)

        selectionArea = QGroupBox('Select a Pattern')
        selectionLayout = QHBoxLayout()
        selectionArea.setLayout(selectionLayout)

        self.patternBox = QComboBox()
        self.patternBox.addItem('Random')
        self.startButton = QPushButton('&Start')
        self.startButton.clicked.connect(self.animate)
        selectionLayout.addWidget(self.patternBox)
        selectionLayout.addWidget(self.startButton)

        layout.addWidget(selectionArea)
        self.setLayout(layout)

        self.setWindowTitle('Conway\'s Game of Life')

    def animate(self):
        """Start/Stop animating the selected pattern.
        """
        action = self.startButton.text()
        selected = self.patternBox.currentText()
        if action == '&Start':
            auto = (selected == 'Random')
            universe = life.Universe(auto=auto, 
                                     rows=DEFAULT_UNIV_X, 
                                     columns=DEFAULT_UNIV_Y)
            self.universeView.startAnimation(universe)
            self.startButton.setText('&Stop')
        else:
            self.universeView.stopAnimation()
            self.startButton.setText('&Start')


def start_app():
    """Start the application
    """
    app = QApplication(sys.argv)
    gol = GameOfLifeApp()
    gol.show()
    app.exec_()


if __name__ == '__main__':
    start_app()
