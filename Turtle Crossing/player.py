from turtle import Turtle

STARTING_POSITION = (0, -280)
FINISH_LINE_Y = 280


class Player(Turtle):
    def __init__(self):
        super().__init__()
        self.shape('turtle')
        self.color('green')
        self.penup()
        self.setheading(90)
        self.goto(STARTING_POSITION)
        self.move_distance = 10

    def go_up(self):
        new_y = self.ycor() + self.move_distance
        self.goto(self.xcor(), new_y)
        self.setheading(90)
    def go_down(self):
        new_y = self.ycor() - self.move_distance
        self.goto(self.xcor(), new_y)
        self.setheading(270)

    def go_left(self):
        new_x = self.xcor() - self.move_distance
        self.goto(new_x, self.ycor())
        self.setheading(180)

    def go_right(self):
        new_x = self.xcor() + self.move_distance
        self.goto(new_x, self.ycor())
        self.setheading(0)

    def increase_speed(self):
        self.move_distance += 3