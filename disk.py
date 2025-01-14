"""
file: disk.py
Description: This file contains class Disk that
has attributes and methods of a single disk
"""


class Disk:
    def __init__(self, center_x, center_y, color, cell_width):
        self.center_x = center_x
        self.center_y = center_y
        self.color = color
        self.cell_width = cell_width

    def display(self):
        """Display disk"""
        if self.color == "YELLOW":
            fill(255, 255, 0)
        else:
            fill(255, 0, 0)

        noStroke()
        ellipse(self.center_x, self.center_y, self.cell_width, self.cell_width)

    def drop(self, dy):
        """The drop movement(animation) of a disk"""
        self.center_y += dy

    def move(self, center_x, center_y):
        """"Place disk at the final destination"""
        self.center_x = center_x
        self.center_y = center_y
