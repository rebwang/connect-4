"""
This game_controller_test.py tests the constructor of GameController class
"""
from game_controller import GameController
from score import Score


def test_constructor():
    score_file = "score_test.txt"
    score = Score(score_file)
    gc = GameController(300, 450, 150, 30, score)
    assert gc.board_width == 300
    assert gc.board_height == 450
    assert gc.cell_width == 150
    assert gc.font_size == 30
    assert gc.yellow_wins is False
    assert gc.red_wins is False
    assert gc.tie is False
