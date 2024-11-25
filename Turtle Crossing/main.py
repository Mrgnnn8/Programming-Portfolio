import time
from turtle import Screen
from player import Player  # Importing the player class to manage the turtle character
from car_manager import CarManager  # Handles the creation and movement of cars
from scoreboard import Scoreboard  # Displays and updates the score and game status

# Define the starting position for the player
STARTING_POSITION = (0, -280)

# Set up the game window
screen = Screen()
screen.setup(width=600, height=600)  # Define the screen size
screen.title('Crossy Road')  # Set the window title
screen.tracer(0)  # Turn off screen updates for smoother animations

# Create instances of Player, CarManager, and Scoreboard classes
player = Player()
car_manager = CarManager(player)  # Pass the player instance to track interactions
scoreboard = Scoreboard()

# Set up key bindings for player controls
screen.listen()
screen.onkey(player.go_up, "Up")  # Move the player up
screen.onkey(player.go_down, "Down")  # Move the player down
screen.onkey(player.go_left, "Left")  # Move the player left
screen.onkey(player.go_right, "Right")  # Move the player right

# Start the game loop
game_is_on = True
while game_is_on:
    time.sleep(0.1)  # Add a small delay to control the game speed
    screen.update()  # Refresh the screen
    car_manager.create_car()  # Create new cars at random intervals
    car_manager.move_cars()  # Move all cars on the screen

    # Check for collisions between the player and cars
    for car in car_manager.all_cars:
        if car.distance(player) < 20:  # Collision detected if distance is less than 20 units
            scoreboard.game_over()  # Display the game-over message
            player.goto(STARTING_POSITION)  # Reset the player's position

    # Check if the player successfully crossed the road
    if player.ycor() > 280:  # Player reaches the top of the screen
        player.goto(0, -280)  # Reset the player's position
        car_manager.level_up()  # Increase car speed for the next level
        scoreboard.increase_level()  # Update the level displayed
        player.increase_speed()  # Optionally adjust player speed (if implemented)

