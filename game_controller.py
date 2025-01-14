"""
file: game_controller.py
Description:
This file contructs GameController class which monitors the game status
such as yellow/red wins or tie, also displays game result.
"""


class GameController:
    def __init__(self, board_width, board_height, cell_width, font_size, score):
        self.board_width = board_width
        self.board_height = board_height
        self.cell_width = cell_width
        self.font_size = font_size
        self.score = score

        self.yellow_wins = False
        self.red_wins = False
        self.tie = False

        # player name input status
        self.display_input = False
        self.player_name = ""

    def display(self):
        """Display end game status at the center of dropping area"""
        if self.display_input:
            fill(255)
            textSize(self.font_size)
            textAlign(CENTER, CENTER)
            text("YOU WIN! PLEASE ENTER YOUR NAME: " + self.player_name, self.board_width/2, self.cell_width/2)
            return

        if self.player_name:
            fill(255)
            textSize(self.font_size)
            textAlign(CENTER, CENTER)
            text("CONGRATULATIONS " + self.player_name + "!", self.board_width/2, self.cell_width/2)
            return

        if self.red_wins:
            self.display_input = True

        elif self.yellow_wins:
            fill(255)
            textSize(self.font_size)
            textAlign(CENTER, CENTER)
            text("YELLOW WINS", self.board_width/2, self.cell_width/2)

        elif self.tie:
            fill(255)
            textSize(self.font_size)
            textAlign(CENTER, CENTER)
            text("BOARD IS FULL. TIE.", self.board_width/2, self.cell_width/2)

        else:
            fill(0)
            textSize(self.font_size)
            textAlign(CENTER, CENTER)
            text(self.board.cur_player + "'S TURN.", self.board_width/2, self.cell_width/2)

    def keyPressed(self, key):
        # player name input
        if not self.display_input:
            return

        if key == "\n":
            # save player name and calculate score
            self.score.record_score(self.player_name)
            self.display_input = False
            return

        self.player_name += key
        return
