import time
from turtle import Screen
from player import Player
from car_manager import CarManager
from scoreboard import Scoreboard

STARTING_POSITION = (0, -280)

screen = Screen()
screen.setup(width=600, height=600)
screen.title('Crossy Road')
screen.tracer(0)

player = Player()
car_manager = CarManager(player)
scoreboard = Scoreboard()


screen.listen()
screen.onkey(player.go_up, "Up")
screen.onkey(player.go_down, "Down")
screen.onkey(player.go_left, "Left")
screen.onkey(player.go_right, "Right")

game_is_on = True
while game_is_on:
    time.sleep(0.1)
    screen.update()
    car_manager.create_car()
    car_manager.move_cars()

    for car in car_manager.all_cars:
        if car.distance(player) < 20:
            scoreboard.game_over()
            player.goto(STARTING_POSITION)
            
    if player.ycor() > 280:  
        player.goto(0, -280)  
        car_manager.level_up() 
        scoreboard.increase_level()
        player.increase_speed()

