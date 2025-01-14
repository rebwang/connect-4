"""
This grid_test.py tests the constructor of Grid class
"""
from grid import Grid


def test_constructor():
    grid = Grid(0, 0, 7, 6, 100, 10, 700, 700)
    assert grid.x == 0
    assert grid.y == 0
    assert grid.col_num == 7
    assert grid.row_num == 6
    assert grid.cell_width == 100
    assert grid.gap_width == 10
    assert grid.board_width == 700
    assert grid.board_height == 700
