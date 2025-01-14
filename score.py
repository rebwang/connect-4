"""
class Score does the below functions:
1. Read score file and save the existing data into a dictionary
2. Takes a string of a player's name, and calculates win counts
3. Sort players according to their win counts
4. Write the data into score file
"""


class Score:
    def __init__(self, score_file):
        self.score_file = score_file
        self.scores = {}

    def read_score_file(self):
        # Read scores file and save data into dictionary self.scores
        # exception handling
        try:
            file = open(self.score_file, "r")
            for line in file:
                name = ""
                score = ""
                for c in line:
                    if c.isdigit():
                        score += c
                    else:
                        name += c
                lower_name = name.strip().lower()
                int_score = int(score)
                self.scores[lower_name] = int_score
            return ""
        except FileNotFoundError:
            return "Score file not found."

    def record_score(self, name):
        """
        Calculate winner score and writes data into scores file
        Name format:
        1. case insensitive string intake
        2. allows space between name, for example: 'jay chou'
        3. strip out head and tail spaces, and lower all cases before adding to self.scores dictionary
        4. capitalize the first character in the score file, for example: 'Jay'
        """
        error_message = self.read_score_file()
        if error_message:
            print(error_message)
            return

        lower_winner_name = name.lower()
        if lower_winner_name in self.scores:
            self.scores[lower_winner_name] += 1
        else:
            self.scores[lower_winner_name] = 1

        # write the sorted scores into file
        f = open(self.score_file, 'w')
        for key, value in sorted(self.scores.items(), key=lambda x: x[1], reverse=True):
            name = key.capitalize()
            score = str(value)
            f.write(name + " " + score + "\n")

        f.close()

    def reset_score(self):
        """Clean up all the records in score file"""
        with open(self.score_file, 'w') as f:
            pass

        f.close()
