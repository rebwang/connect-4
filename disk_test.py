"""
This disk_test.py tests the constructor and the methods in Disk class
"""
from disk import Disk


def test_constructor():
    disk = Disk(50, 50, "RED", 100)
    assert disk.center_x == 50
    assert disk.center_y == 50
    assert disk.color == "RED"
    assert disk.cell_width == 100


def test_drop():
    disk = Disk(50, 50, "RED", 100)
    disk.drop(100)
    assert disk.center_y == 150


def test_move():
    disk = Disk(50, 50, "RED", 100)
    disk.move(250, 250)
    assert disk.center_x == 250
    assert disk.center_y == 250
