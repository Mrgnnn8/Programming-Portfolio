from turtle import Turtle
import random

COLORS = ["red", "orange", "yellow", "green", "blue", "purple"]
STARTING_MOVE_DISTANCE = 5
MOVE_INCREMENT = 10
STARTING_POSITIONS = [(300, )]

class CarManager:
    def __init__(self, player):
        self.all_cars = []
        self.car_speed = STARTING_MOVE_DISTANCE
        self.player = player

    def create_car(self):
        random_chance = random.randint(1, 8)  # Controls car frequency
        if random_chance == 1:  # Approximately creates a car every 6th time this method is called
            new_car = Turtle("square")
            new_car.shapesize(stretch_wid=1, stretch_len=2)
            new_car.penup()
            new_car.color(random.choice(COLORS))
            random_y = random.randint(-300 // 2, 300 // 2)
            new_car.goto(300 // 2, random_y)  # Start on the right side of the screen
            self.all_cars.append(new_car)

    def move_cars(self):
        for car in self.all_cars:
            # NEW: Make cars change lanes randomly to simulate AI behavior
            if random.randint(1, 20) == 1:  # 1 in 20 chance to change lanes
                new_y = car.ycor() + random.choice([-20, 20])  # Change lane by moving up or down
                # Ensure the car stays within bounds
                if -300 // 2 <= new_y <= 300 // 2:
                    car.sety(new_y)

            # NEW: Adjust speed based on proximity to player (chasing behavior example)
            if car.distance(self.player) < 100:  # If the car is close to the player
                car_speed = self.car_speed * 1.5  # Speed up
            else:
                car_speed = self.car_speed

            car.backward(car_speed)  # Move cars to the left

    def level_up(self):
        self.car_speed += MOVE_INCREMENT

