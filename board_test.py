"""
File: board_test.py
Description:
This file tests constructor and methods in Board class
"""
from board import Board
from game_controller import GameController
from score import Score
from cell import Cell
from disk import Disk


def test_constructor():
    score_file = "score_test.txt"
    score = Score(score_file)

    game_controller = GameController(700, 700, 100, 30, score)
    board = Board(4, 7, 6, 100, 700, 700, 10, 10, 2, 100, game_controller)
    assert board.connect_target == 4
    assert board.x == 0
    assert board.y == 0
    assert board.col_num == 7
    assert board.row_num == 6
    assert board.cell_width == 100
    assert board.board_width == 700
    assert board.board_height == 700
    assert board.gap_width == 10
    assert board.drop_speed == 10
    assert board.drop_acceleration_speed == 2

    assert board.drop_area_width == 700
    assert board.drop_area_height == 100

    assert board.cur_player == "RED"
    assert board.last_move_cell is None

    assert board.com_countdown == 100
    assert board.gc is game_controller

    assert board.floating_disk is None
    assert board.is_dropping is False
    assert board.dropping_target_cell is None
    assert board.dropping_speed == 10
    assert board.gc.board == board


def test_playground_cells():
    score_file = "score_test.txt"
    score = Score(score_file)
    game_controller = GameController(700, 700, 100, 30, score)
    board = Board(2, 2, 2, 100, 200, 300, 10, 10, 2, 100, game_controller)
    assert len(board.playground_cells) == board.row_num
    assert len(board.playground_cells[0]) == board.col_num


# ----- Computer Actions -----
def test_is_computer_player_ready():
    score_file = "score_test.txt"
    score = Score(score_file)
    game_controller = GameController(700, 700, 100, 30, score)
    board = Board(2, 2, 2, 100, 200, 300, 10, 10, 2, 100, game_controller)
    board.cur_com_countdown = 0
    result = board.is_computer_player_ready()
    assert board.cur_com_countdown == 100
    assert result is True

    board.cur_com_countdown = 5
    result = board.is_computer_player_ready()
    assert board.cur_com_countdown == 4
    assert result is False


# ----- Disk Dropping -----
def test_create_floating_disk_by_col():
    score_file = "score_test.txt"
    score = Score(score_file)
    game_controller = GameController(700, 700, 100, 30, score)
    board = Board(2, 2, 2, 100, 200, 300, 10, 10, 2, 100, game_controller)
    board.create_floating_disk_by_col(0)
    assert board.floating_disk is not None
    disk = board.floating_disk

    # Assert the position of the disk
    expected_center_x = 50
    expected_center_y = 50

    assert disk.center_x == expected_center_x
    assert disk.center_y == expected_center_y

    # Assert the player and cell width
    assert disk.color == board.cur_player
    assert disk.cell_width == board.cell_width


def test_drop_disk():
    score_file = "score_test.txt"
    score = Score(score_file)
    game_controller = GameController(700, 700, 100, 30, score)
    board = Board(2, 2, 2, 100, 200, 300, 10, 10, 2, 100, game_controller)
    board.drop_disk(0)
    assert board.is_dropping is True
    assert board.dropping_target_cell == board.playground_cells[1][0]


def test_reset_dropping():
    score_file = "score_test.txt"
    score = Score(score_file)
    game_controller = GameController(700, 700, 100, 30, score)
    board = Board(2, 2, 2, 100, 200, 300, 10, 10, 2, 100, game_controller)
    board.is_dropping = True
    assert board.is_dropping is True
    board.reset_dropping()
    assert board.floating_disk is None
    assert board.is_dropping is False
    assert board.dropping_target_cell is None
    assert board.dropping_speed == 10


# ----- Game State -----
def test_update_game_state():
    score_file = "score_test.txt"
    score = Score(score_file)
    game_controller = GameController(700, 700, 100, 30, score)
    board = Board(2, 2, 2, 100, 200, 300, 10, 10, 2, 100, game_controller)
    board.last_move_cell = Cell(0, 100, 1, 1, 100)
    assert board.last_move_cell.row == 1
    assert board.last_move_cell.col == 1
    assert board.last_move_cell.disk is None
    board.last_move_cell.disk = Disk(50, 150, "RED", 100)
    assert board.last_move_cell.disk.color == "RED"


def test_check_winner():
    score_file = "score_test.txt"
    score = Score(score_file)
    game_controller = GameController(700, 700, 100, 30, score)
    board = Board(2, 2, 2, 100, 200, 300, 10, 10, 2, 100, game_controller)
    assert board.check_if_board_is_full() is False

    # fill down right cell with red disk
    x = 150
    y = 250
    color = "RED"
    cell_width = board.cell_width
    board.playground_cells[1][1].disk = Disk(x, y, color, cell_width)
    assert board.check_winner(1, 1, "RED") == ""

    # fill upper right cell with red disk
    x2 = 150
    y2 = 150
    board.playground_cells[0][1].disk = Disk(x2, y2, color, cell_width)
    assert board.check_winner(0, 1, "RED") == "RED"


def test_get_max_consecutive_count_and_cols():
    score_file = "score_test.txt"
    score = Score(score_file)
    game_controller = GameController(700, 700, 100, 30, score)
    board = Board(2, 2, 2, 100, 200, 300, 10, 10, 2, 100, game_controller)
    assert board.check_if_board_is_full() is False

    # fill down right cell with red disk
    x = 150
    y = 250
    color = "RED"
    cell_width = board.cell_width
    board.playground_cells[1][1].disk = Disk(x, y, color, cell_width)

    # get max_consecutive_count and a list of availble cols
    max_consecutive_count, max_consecutive_cols = board.get_max_consecutive_count_and_cols(color)
    assert max_consecutive_count == 2
    assert max_consecutive_cols == [0, 1]


def test_get_max_consecutive():
    score_file = "score_test.txt"
    score = Score(score_file)
    game_controller = GameController(700, 700, 100, 30, score)
    board = Board(2, 2, 2, 100, 200, 300, 10, 10, 2, 100, game_controller)

    for i in range(2):
        for j in range(2):
            x = board.cell_width//2 + (j * board.cell_width)
            y = board.drop_area_height + board.cell_width//2 + (i * board.cell_width)
            color = "RED"
            cell_width = board.cell_width
            board.playground_cells[i][j].disk = Disk(x, y, color, cell_width)

    # upper left cell
    row = 0
    col = 0
    color = "RED"
    offset = (1, 0)  # down left cell
    assert board.get_max_consecutive(row, col, offset, color) == 1


def test_check_if_board_is_full():
    score_file = "score_test.txt"
    score = Score(score_file)
    game_controller = GameController(700, 700, 100, 30, score)
    board = Board(2, 2, 2, 100, 200, 300, 10, 10, 2, 100, game_controller)
    assert board.check_if_board_is_full() is False

    # fill all cells with red disk
    for i in range(2):
        for j in range(2):
            x = board.cell_width//2 + (j * board.cell_width)
            y = board.drop_area_height + board.cell_width//2 + (i * board.cell_width)
            color = "RED"
            cell_width = board.cell_width
            board.playground_cells[i][j].disk = Disk(x, y, color, cell_width)

    assert board.check_if_board_is_full() is True


def test_is_game_over():
    score_file = "score_test.txt"
    score = Score(score_file)
    game_controller = GameController(700, 700, 100, 30, score)
    board = Board(2, 2, 2, 100, 200, 300, 10, 10, 2, 100, game_controller)

    board.gc.yellow_wins = True
    assert board.is_game_over() is True

    board.gc.yellow_wins = False
    assert board.is_game_over() is False


def test_alternate_player():
    score_file = "score_test.txt"
    score = Score(score_file)
    game_controller = GameController(700, 700, 100, 30, score)
    board = Board(2, 2, 2, 100, 200, 300, 10, 10, 2, 100, game_controller)
    board.alternate_player()
    assert board.cur_player == "YELLOW"


def test_is_computer_player_turn():
    score_file = "score_test.txt"
    score = Score(score_file)
    game_controller = GameController(700, 700, 100, 30, score)
    board = Board(2, 2, 2, 100, 200, 300, 10, 10, 2, 100, game_controller)
    assert board.is_computer_player_turn() is False


# ----- Helper Functions -----
def test_is_in_drop_area():
    score_file = "score_test.txt"
    score = Score(score_file)
    game_controller = GameController(700, 700, 100, 30, score)
    board = Board(2, 2, 2, 100, 200, 300, 10, 10, 2, 100, game_controller)
    assert board.is_in_drop_area(150, 75) is True


def test_get_col_by_x():
    score_file = "score_test.txt"
    score = Score(score_file)
    game_controller = GameController(700, 700, 100, 30, score)
    board = Board(2, 2, 2, 100, 200, 300, 10, 10, 2, 100, game_controller)
    col = board.get_col_by_x(150)
    assert col == 2


def test_get_lowest_empty_cell_by_col():
    score_file = "score_test.txt"
    score = Score(score_file)
    game_controller = GameController(700, 700, 100, 30, score)
    board = Board(2, 2, 2, 100, 200, 300, 10, 10, 2, 100, game_controller)
    cell = board.get_lowest_empty_cell_by_col(0)
    assert cell == board.playground_cells[1][0]
