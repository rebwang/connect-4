"""
File: board.py
Description:
This file constructs Board class that controls the states of the board
Including mouse listener functions and disk animation
"""
from cell import Cell
from disk import Disk
from grid import Grid
import math
import random


class Board:
    def __init__(self, connect_target, col_num, row_num, cell_width, board_width, board_height, gap_width, drop_speed, drop_acceleration_speed, com_countdown, game_controller):
        self.connect_target = connect_target
        self.x = 0
        self.y = 0
        self.col_num = col_num
        self.row_num = row_num
        self.cell_width = cell_width
        self.board_width = board_width
        self.board_height = board_height
        self.gap_width = gap_width
        self.drop_speed = drop_speed
        self.drop_acceleration_speed = drop_acceleration_speed

        self.drop_area_width = self.col_num * self.cell_width
        self.drop_area_height = self.cell_width

        # create cells in drop area
        self.drop_area_cells = []
        for i in range(self.col_num):
            cell_x = self.x + (i * self.cell_width)
            cell_y = self.y
            self.drop_area_cells.append(Cell(cell_x, cell_y, -1, -1, self.cell_width))

        # create cells in playground area
        self.playground_cells = []
        for i in range(self.row_num):
            playground_row = []
            for j in range(self.col_num):
                cell_x = self.x + (j * self.cell_width)
                cell_y = self.y + self.drop_area_height + (i * self.cell_width)
                playground_row.append(Cell(cell_x, cell_y, i, j, self.cell_width))
            self.playground_cells.append(playground_row)

        # Initialize player & last move status, start with human RED
        self.cur_player = "RED"
        self.last_move_cell = None

        # offsets for checking winner -> direction: [(row_offset, col_offset)]
        self.direction_offsets = {
            "horizontal": [(0, 1), (0, -1)],  # right, left
            "vertical": [(1, 0), (-1, 0)],    # down, up
            "diagonal": [(1, 1), (-1, -1)],   # down right, up left
            "reverse_diagonal": [(-1, 1), (1, -1)]  # up right, down left
        }

        # dropping status
        self.floating_disk = None
        self.is_dropping = False
        self.dropping_target_cell = None
        self.dropping_speed = self.drop_speed

        self.grid = Grid(self.x, self.y+self.drop_area_height, self.col_num, self.row_num, self.cell_width, self.gap_width, self.board_width, self.board_height)

        self.com_countdown = com_countdown
        self.cur_com_countdown = self.com_countdown

        self.gc = game_controller
        self.gc.board = self

    def display(self):
        # display dropping area
        for cell in self.drop_area_cells:
            cell.display()

        # display playground cells
        for row in self.playground_cells:
            for cell in row:
                cell.display()

        # computer actions
        if self.is_computer_player_turn():
            self.drop_disk_strategy_by_computer()

        # actions for a disk drop from start to end
        if self.is_dropping:
            self.update_floating_disk()

        if self.floating_disk:
            self.floating_disk.display()

        self.grid.display()

        # check cell status after each disk dropped
        self.update_game_state()

    # ----- Human Actions -----
    def mousePressed(self, mouseX, mouseY):
        if self.is_game_over():
            return

        if self.is_computer_player_turn():
            return

        if self.is_dropping:
            return

        if self.is_in_drop_area(mouseX, mouseY):
            # Detect user's mouse is within dropping area
            col = self.get_col_by_x(mouseX)
            self.create_floating_disk_by_col(col)

    def mouseDragged(self, mouseX, mouseY):
        if self.is_game_over():
            return

        if self.is_computer_player_turn():
            return

        if self.is_dropping:
            return

        if self.is_in_drop_area(mouseX, mouseY):
            col = self.get_col_by_x(mouseX)
            self.create_floating_disk_by_col(col)
        else:
            self.reset_dropping()

    def mouseReleased(self, mouseX, mouseY):
        if self.is_game_over():
            return

        if self.is_computer_player_turn():
            return

        if self.is_dropping:
            return

        if not self.floating_disk:
            return

        col = self.get_col_by_x(mouseX)
        self.drop_disk(col)

    # ----- Computer Actions -----
    def drop_disk_random_by_computer(self):
        """Computer drop disk at a random available cell (not AI)"""
        if self.is_game_over():
            return

        if self.is_dropping:
            return

        if not self.is_computer_player_ready():
            return

        available_cols = []
        for col in range(self.col_num):
            if self.get_lowest_empty_cell_by_col(col) is not None:
                available_cols.append(col)
        target_col = available_cols[random.randint(0, len(available_cols)-1)]

        self.create_floating_disk_by_col(target_col)
        self.drop_disk(target_col)

        return

    def drop_disk_strategy_by_computer(self):
        """Computer's AI strategy against human player"""
        if self.is_game_over():
            return

        if self.is_dropping:
            return

        if not self.is_computer_player_ready():
            return

        # Get max consecutive count and columns for both color
        yellow_max_consecutive_count, yellow_max_consecutive_cols = self.get_max_consecutive_count_and_cols("YELLOW")
        red_max_consecutive_count, red_max_consecutive_cols = self.get_max_consecutive_count_and_cols("RED")

        target_col = -1
        if yellow_max_consecutive_count >= self.connect_target:
            # yellow will reach the connect target count
            target_col = yellow_max_consecutive_cols[0]
        elif red_max_consecutive_count >= self.connect_target:
            # red will reach the connect target count
            target_col = red_max_consecutive_cols[0]
        elif yellow_max_consecutive_count >= red_max_consecutive_count:
            # stack yellow disk instead of stopping red, pick a column from the list
            target_col = yellow_max_consecutive_cols[random.randint(0, len(yellow_max_consecutive_cols)-1)]
        else:
            target_col = red_max_consecutive_cols[random.randint(0, len(red_max_consecutive_cols)-1)]
            # stop red instead of stacking yellow, pick a column from the list

        self.create_floating_disk_by_col(target_col)
        self.drop_disk(target_col)

        return

    def is_computer_player_ready(self):
        """Time delay counter for the pause before computer starts action"""
        if self.cur_com_countdown <= 0:
            # reset the counter back to the original value
            self.cur_com_countdown = self.com_countdown
            return True

        # keep counting down before reaching 0
        self.cur_com_countdown -= 1
        return False

    # ----- Disk Dropping -----
    def create_floating_disk_by_col(self, col):
        """Create a floating disk in the top most row given a column"""
        center_x = self.x + self.cell_width//2 + col * self.cell_width
        center_y = self.y + self.cell_width//2
        self.floating_disk = Disk(center_x, center_y, self.cur_player, self.cell_width)

    def drop_disk(self, col):
        self.is_dropping = True
        self.dropping_target_cell = self.get_lowest_empty_cell_by_col(col)

        if self.dropping_target_cell is None:
            # the column is full, do nothing
            self.reset_dropping()
        return

    def update_floating_disk(self):
        """Actions for a disk drop from start to end"""

        # dropping animation
        target_center_x = self.dropping_target_cell.x + self.cell_width//2
        target_center_y = self.dropping_target_cell.y + self.cell_width//2
        if self.floating_disk.center_y + self.dropping_speed <= target_center_y:
            self.floating_disk.drop(self.dropping_speed)
            # drop speed increases as the disk drops
            self.dropping_speed += self.drop_acceleration_speed
            return

        # fill disk in target cell and record last move
        self.floating_disk.move(target_center_x, target_center_y)
        self.dropping_target_cell.fill(self.floating_disk)
        self.last_move_cell = self.dropping_target_cell

        # switch player and reset dropping states
        self.alternate_player()
        self.reset_dropping()

    def reset_dropping(self):
        # Reset floating_disk and dropping status after a disk completed dropping
        self.floating_disk = None
        self.is_dropping = False
        self.dropping_target_cell = None
        self.dropping_speed = self.drop_speed

    # ----- Game State -----
    def update_game_state(self):
        # player hasn't started
        if self.last_move_cell is None:
            return

        # check if there is a winner
        last_row = self.last_move_cell.row
        last_col = self.last_move_cell.col
        last_color = self.last_move_cell.disk.color
        winner = self.check_winner(last_row, last_col, last_color)
        if winner == "RED":
            self.gc.red_wins = True
            return
        elif winner == "YELLOW":
            self.gc.yellow_wins = True
            return

        # check if there is a tie due to full board
        if self.check_if_board_is_full():
            self.gc.tie = True
            return

        return

    def check_winner(self, last_row, last_col, last_color):
        """
        Check if there is any player reach connect target
        if red wins -> return RED
        if yellow wins -> return YELLOW
        if no one wins -> return empty string
        """
        for offsets in self.direction_offsets.values():
            consecutive_count = 1  # count self
            for offset in offsets:
                consecutive_count += self.get_max_consecutive(last_row, last_col, offset, last_color)

            if consecutive_count >= self.connect_target:
                return last_color

        return ""

    def get_max_consecutive_count_and_cols(self, color):
        """
        Computer AI strategy:
        Calculate the maximum consecutive disk count (in the same color) once a disk dropped,
        and record the correspondent columns into a list.
        Return two things:
            (1) maximum consecutive count -> int
            (2) maximum consecutive columns -> list
        """
        max_consecutive_count = 0
        max_consecutive_cols = []

        for col in range(self.col_num):
            # iterate through all columns
            lowest_empty_cell = self.get_lowest_empty_cell_by_col(col)
            if lowest_empty_cell is None:
                continue

            row = lowest_empty_cell.row
            col_max_consecutive_count = 0
            # iterate through adjacent cells in each direction
            # total 4 directions: horizontal, vertical, diagonals
            for offsets in self.direction_offsets.values():
                direction_max_consecutive_count = 1  # counting self
                for offset in offsets:
                    direction_max_consecutive_count += self.get_max_consecutive(row, col, offset, color)
                col_max_consecutive_count = max(col_max_consecutive_count, direction_max_consecutive_count)

            if col_max_consecutive_count > max_consecutive_count:
                max_consecutive_count = col_max_consecutive_count
                max_consecutive_cols = [col]
            elif col_max_consecutive_count == max_consecutive_count:
                max_consecutive_cols.append(col)

        return max_consecutive_count, max_consecutive_cols

    def get_max_consecutive(self, row, col, offset, color):
        """
        Calculate the adjacent disk count after a disk drop
        offset: direction -> tuple: (row, col), total 8 directions.
        color: player's color
        return: adjacent count -> int
        """
        count = 0
        cur_row = row
        cur_col = col
        while True:
            cur_row += offset[0]
            cur_col += offset[1]
            # Out of bound
            if cur_row >= self.row_num or cur_row < 0 or cur_col >= self.col_num or cur_col < 0:
                break
            if self.playground_cells[cur_row][cur_col].is_empty():
                break
            if self.playground_cells[cur_row][cur_col].disk.color != color:
                break
            count += 1

        return count

    def check_if_board_is_full(self):
        for row in self.playground_cells:
            for cell in row:
                if cell.is_empty():
                    return False
        return True

    def is_game_over(self):
        # Check game over status after each disk dropped
        return self.gc.tie or self.gc.yellow_wins or self.gc.red_wins

    def alternate_player(self):
        if self.cur_player == "RED":
            self.cur_player = "YELLOW"
        else:
            self.cur_player = "RED"

    def is_computer_player_turn(self):
        return self.cur_player == "YELLOW"

    # ----- Helper Functions -----
    def is_in_drop_area(self, mouseX, mouseY):
        # Detect user's mouse is within the upper part of the board
        return self.x <= mouseX <= self.x + self.drop_area_width and self.y <= mouseY <= self.y + self.drop_area_height

    def get_col_by_x(self, x):
        """
        param: mouse x
        return: column number start from 1(left)
        """
        return int(math.ceil((x - self.x) / self.cell_width))

    def get_lowest_empty_cell_by_col(self, col):
        # Return the lowest empty cell given a col index
        # return None if whole col is ful

        for i in range(self.row_num-1, -1, -1):
            if self.playground_cells[i][col].is_empty():
                return self.playground_cells[i][col]
        return None