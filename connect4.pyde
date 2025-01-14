# flake8: noqa
from board import Board
from game_controller import GameController
from score import Score

CONNECT_TARGET = 4
COL_NUM = 7
ROW_NUM = 6
CELL_WIDTH = 100
BOARD_WIDTH =  CELL_WIDTH * COL_NUM
BOARD_HEIGHT = CELL_WIDTH * (ROW_NUM + 1)
GAP_WIDTH = 10
DROP_SPEED = 10
DROP_ACCELERATION_SPEED = 2
FONT_SIZE = 30
COM_COUNTDOWN = 100
score_file = "scores.txt"

score = Score(score_file)
game_controller = GameController(BOARD_WIDTH, BOARD_HEIGHT, CELL_WIDTH, FONT_SIZE, score)
board = Board(CONNECT_TARGET, COL_NUM, ROW_NUM, CELL_WIDTH, BOARD_WIDTH, BOARD_HEIGHT, GAP_WIDTH, DROP_SPEED, DROP_ACCELERATION_SPEED, COM_COUNTDOWN, game_controller)

def setup():
    size(BOARD_WIDTH, BOARD_HEIGHT)

def draw():
    board.display()
    game_controller.display()

def mousePressed():
    board.mousePressed(mouseX, mouseY)

def mouseDragged():
    board.mouseDragged(mouseX, mouseY)

def mouseReleased():
    board.mouseReleased(mouseX, mouseY)

def keyPressed():
    game_controller.keyPressed(key)
