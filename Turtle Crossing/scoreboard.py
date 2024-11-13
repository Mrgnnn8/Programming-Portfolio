from turtle import Turtle

FONT = ("Courier", 24, "normal")
HIGH_SCORE_FILE = "high_score.txt"

class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.level = 1
        self.high_score = self.load_high_score()  # Load the high score from the file
        self.hideturtle()
        self.penup()
        self.goto(-280, 260)  # Position in the top-left corner of the screen
        self.update_scoreboard()

    def update_scoreboard(self):
        self.clear()
        self.goto(-280, 260)  # Ensure the "Level" text is always in the top-left corner
        self.write(f"Level: {self.level} | High Score: {self.high_score}", align="left", font=FONT)

    def increase_level(self):
        self.level += 1
        if self.level > self.high_score:
            self.high_score = self.level
            self.save_high_score()  # Save the new high score
        self.update_scoreboard()

    def game_over(self):
        # Display "GAME OVER" message
        self.goto(0, 0)  # Move to the center of the screen
        self.write("GAME OVER", align="center", font=FONT)
        # Reset the level after displaying the message
        self.level = 1
        self.update_scoreboard()  # Update the scoreboard with the reset level

    def save_high_score(self):
        with open(HIGH_SCORE_FILE, mode="w") as file:
            file.write(str(self.high_score))

    def load_high_score(self):
        try:
            with open(HIGH_SCORE_FILE) as file:
                content = file.read()
                if content.strip():  # Check if the file is not empty
                    return int(content)
                else:
                    return 0  # Return 0 if the file is empty
        except FileNotFoundError:
            return 0  # Default high score if the file does not exist
