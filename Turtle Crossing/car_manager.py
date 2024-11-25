from turtle import Turtle
import random

# Constants for car properties and movement
COLORS = ["red", "orange", "yellow", "green", "blue", "purple"]  # Possible car colors
STARTING_MOVE_DISTANCE = 5  # Initial speed of the cars
MOVE_INCREMENT = 10  # Speed increase with each level
STARTING_POSITIONS = [(300,)]  # Initial x-coordinate for new cars

class CarManager:
    def __init__(self, player):
        """
        Initializes the CarManager class, which handles creating and managing cars.
        """
        self.all_cars = []  # List to store all active car objects
        self.car_speed = STARTING_MOVE_DISTANCE  # Initial speed of the cars
        self.player = player  # Reference to the player object for interactions

    def create_car(self):
        """
        Creates a new car at random intervals and assigns it random properties.
        """
        random_chance = random.randint(1, 8)  # Approximately 1 in 8 chance to create a car
        if random_chance == 1:
            new_car = Turtle("square")  # Create a new car object with a rectangular shape
            new_car.shapesize(stretch_wid=1, stretch_len=2)  # Stretch the shape to form a car
            new_car.penup()  # Disable drawing while moving
            new_car.color(random.choice(COLORS))  # Assign a random color to the car
            random_y = random.randint(-300 // 2, 300 // 2)  # Randomize the y-coordinate
            new_car.goto(300 // 2, random_y)  # Place the car on the right side of the screen
            self.all_cars.append(new_car)  # Add the car to the list of active cars

    def move_cars(self):
        """
        Moves all the cars across the screen and implements dynamic behavior based on proximity.
        """
        for car in self.all_cars:
            # Add random lane-changing behavior
            if random.randint(1, 20) == 1:  # 1 in 20 chance to change lanes
                new_y = car.ycor() + random.choice([-20, 20])  # Move up or down by 20 units
                if -300 // 2 <= new_y <= 300 // 2:  # Ensure the new y-coordinate is within bounds
                    car.sety(new_y)

            # Increase speed when a car is near the player
            if car.distance(self.player) < 100:  # Proximity check with the player
                car_speed = self.car_speed * 1.5  # Temporarily increase car speed
            else:
                car_speed = self.car_speed  # Use normal speed otherwise

            car.backward(car_speed)  # Move the car backward (towards the left side of the screen)

    def level_up(self):
        """
        Increases the car speed when the player levels up.
        """
        self.car_speed += MOVE_INCREMENT  # Increment car speed to make the game more challenging


