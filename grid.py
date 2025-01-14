"""
File: grid.py
Description:
This file constructs Grid class that draws the blue lines of grid
"""


class Grid:
    def __init__(self, x, y, col_num, row_num, cell_width, gap_width, board_width, board_height):
        self.x = x
        self.y = y
        self.col_num = col_num
        self.row_num = row_num
        self.cell_width = cell_width
        self.gap_width = gap_width
        self.board_width = board_width
        self.board_height = board_height

    def display(self):
        # draw horizontal grid lines
        horizontal_x = self.x
        horizontal_y = self.y
        for i in range(self.row_num + 1):
            stroke(0, 0, 204)
            strokeWeight(self.gap_width)
            line(horizontal_x, horizontal_y, horizontal_x + self.board_width, horizontal_y)
            horizontal_y += self.cell_width

        # draw vertical grid lines
        vertical_x = self.x
        vertical_y = self.y
        for i in range(self.col_num + 1):
            stroke(0, 0, 204)
            strokeWeight(self.gap_width)
            line(vertical_x, vertical_y, vertical_x, vertical_y + self.board_height)
            vertical_x += self.cell_width
