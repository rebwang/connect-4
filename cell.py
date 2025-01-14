"""
file: cell.py
Description:
This file constructs Cell class which contains attributes and methods of
a single board cell
"""


class Cell:
    """A cell"""
    def __init__(self, x, y, row, col, cell_width):
        self.x = x
        self.y = y
        self.row = row
        self.col = col
        self.width = cell_width
        self.disk = None

    def display(self):
        """Draws the cell"""
        noStroke()
        fill(192)
        rect(self.x, self.y, self.width, self.width)

        # When a cell is filled with a disk
        if self.disk:
            self.disk.display()

    def is_empty(self):
        """Check if a cell has a disk inside"""
        return self.disk is None

    def fill(self, disk):
        self.disk = disk
