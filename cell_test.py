"""
This cell_test.py tests constructor and functions in Cell class
"""
from cell import Cell
from disk import Disk


def test_cell_constructor():
    cell = Cell(0, 0, 0, 0, 100)
    assert cell.x == 0
    assert cell.row == 0
    assert cell.col == 0
    assert cell.width == 100
    assert not cell.disk


def test_is_empty():
    disk = Disk(50, 50, "RED", 100)
    cell = Cell(0, 0, 0, 0, 100)
    cell.disk = disk
    assert not cell.is_empty()


def test_fill():
    disk = Disk(50, 50, "RED", 100)
    cell = Cell(0, 0, 0, 0, 100)
    cell.fill(disk)
    assert cell.disk == disk
