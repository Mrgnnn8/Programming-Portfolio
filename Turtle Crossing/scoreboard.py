from turtle import Turtle

# Constants for font style and file name
FONT = ("Courier", 24, "normal")  # Font style for the scoreboard text
HIGH_SCORE_FILE = "high_score.txt"  # File name to store the high score

class Scoreboard(Turtle):
    def __init__(self):
        """
        Initializes the Scoreboard class, which inherits from Turtle.
        Sets up the scoreboard's initial state, including level and high score.
        """
        super().__init__()  # Call the parent Turtle class's initializer
        self.level = 1  # Start at level 1
        self.high_score = self.load_high_score()  # Load the high score from file
        self.hideturtle()  # Hide the turtle shape
        self.penup()  # Disable drawing
        self.goto(-280, 260)  # Position the scoreboard at the top-left corner
        self.update_scoreboard()  # Display the initial score

    def update_scoreboard(self):
        """
        Clears the previous scoreboard display and updates it with the current level and high score.
        """
        self.clear()  # Clear the previous text
        self.goto(-280, 260)  # Position the cursor for the scoreboard
        self.write(f"Level: {self.level} | High Score: {self.high_score}", align="left", font=FONT)  # Display the scores

    def increase_level(self):
        """
        Increases the level by 1, updates the high score if the level surpasses it, and refreshes the scoreboard.
        """
        self.level += 1  # Increment the level
        if self.level > self.high_score:  # Check if the new level is a high score
            self.high_score = self.level  # Update the high score
            self.save_high_score()  # Save the new high score to the file
        self.update_scoreboard()  # Refresh the scoreboard display

    def game_over(self):
        """
        Displays a "GAME OVER" message in the center of the screen and resets the level.
        """
        self.goto(0, 0)  # Move to the center of the screen
        self.write("GAME OVER", align="center", font=FONT)  # Display "GAME OVER"
        self.level = 1  # Reset the level
        self.update_scoreboard()  # Refresh the scoreboard display

    def save_high_score(self):
        """
        Saves the current high score to the file specified by HIGH_SCORE_FILE.
        """
        with open(HIGH_SCORE_FILE, mode="w") as file:  # Open the file in write mode
            file.write(str(self.high_score))  # Write the high score as a string

    def load_high_score(self):
        """
        Loads the high score from the file specified by HIGH_SCORE_FILE.
        Returns 0 if the file is empty or not found.
        """
        try:
            with open(HIGH_SCORE_FILE) as file:  # Open the file in read mode
                content = file.read()  # Read the file content
                if content.strip():  # Check if the file is not empty
                    return int(content)  # Return the high score as an integer
                else:
                    return 0  # Return 0 if the file is empty
        except FileNotFoundError:
            return 0  # Return 0 if the file does not exist

