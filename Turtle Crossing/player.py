from turtle import Turtle

# Constants for the player's starting position and finish line
STARTING_POSITION = (0, -280)  # Starting position for the player
FINISH_LINE_Y = 280  # Y-coordinate of the finish line

class Player(Turtle):
    def __init__(self):
        """
        Initializes the Player class, inheriting from Turtle.
        Sets up the player's appearance, starting position, and movement properties.
        """
        super().__init__()  # Call the parent Turtle class's initializer
        self.shape('turtle')  # Set the shape to a turtle
        self.color('green')  # Set the color to green
        self.penup()  # Disable drawing
        self.setheading(90)  # Point the turtle upwards
        self.goto(STARTING_POSITION)  # Move the player to the starting position
        self.move_distance = 10  # Define the initial distance the player moves per step

    def go_up(self):
        """
        Moves the player upward by the defined move distance.
        """
        new_y = self.ycor() + self.move_distance  # Calculate the new y-coordinate
        self.goto(self.xcor(), new_y)  # Move the player to the new position
        self.setheading(90)  # Ensure the turtle is facing upward

    def go_down(self):
        """
        Moves the player downward by the defined move distance.
        """
        new_y = self.ycor() - self.move_distance  # Calculate the new y-coordinate
        self.goto(self.xcor(), new_y)  # Move the player to the new position
        self.setheading(270)  # Ensure the turtle is facing downward

    def go_left(self):
        """
        Moves the player to the left by the defined move distance.
        """
        new_x = self.xcor() - self.move_distance  # Calculate the new x-coordinate
        self.goto(new_x, self.ycor())  # Move the player to the new position
        self.setheading(180)  # Ensure the turtle is facing left

    def go_right(self):
        """
        Moves the player to the right by the defined move distance.
        """
        new_x = self.xcor() + self.move_distance  # Calculate the new x-coordinate
        self.goto(new_x, self.ycor())  # Move the player to the new position
        self.setheading(0)  # Ensure the turtle is facing right

    def increase_speed(self):
        """
        Increases the player's movement speed by incrementing the move distance.
        """
        self.move_distance += 3  # Increase the move distance for faster movement
