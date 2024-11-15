from turtle import Turtle

FONT = ("Courier", 24, "normal")
HIGH_SCORE_FILE = "high_score.txt"

class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.level = 1
        self.high_score = self.load_high_score()  
        self.hideturtle()
        self.penup()
        self.goto(-280, 260) 
        self.update_scoreboard()

    def update_scoreboard(self):
        self.clear()
        self.goto(-280, 260) 
        self.write(f"Level: {self.level} | High Score: {self.high_score}", align="left", font=FONT)

    def increase_level(self):
        self.level += 1
        if self.level > self.high_score:
            self.high_score = self.level
            self.save_high_score() 
        self.update_scoreboard()

    def game_over(self):
        self.goto(0, 0)  
        self.write("GAME OVER", align="center", font=FONT)
        self.level = 1
        self.update_scoreboard() 

    def save_high_score(self):
        with open(HIGH_SCORE_FILE, mode="w") as file:
            file.write(str(self.high_score))

    def load_high_score(self):
        try:
            with open(HIGH_SCORE_FILE) as file:
                content = file.read()
                if content.strip(): 
                    return int(content)
                else:
                    return 0
        except FileNotFoundError:
            return 0  
