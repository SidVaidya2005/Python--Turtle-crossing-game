from car_manager import CarManager
from scoreboard import Scoreboard
from turtle import Screen
from player import Player
import time


# ---------------------- INITIALIZING ------------------- #
car_manager = CarManager()
scoreboard = Scoreboard()
player = Player()
screen = Screen()


# ------------------------ SCREEN -------------------- #
screen.setup(width=600, height=600)
screen.tracer(0)


# --------------------------- CONTROLS ------------------- #
screen.listen()
screen.onkey(player.move_up,"Up")


# -------------------- MAIN ------------------- #
game_is_on = True

while game_is_on:
    time.sleep(0.1)
    screen.update()
    car_manager.create_car()
    car_manager.move_cars()
    scoreboard.update_scoreboard()

    # Detect Collision With Cars
    for car in car_manager.all_cars:
        if player.distance(car) < 20:
            scoreboard.game_over()
            game_is_on = False

    # Detect Successful Crossing
    if player.is_at_finish_line():
        player.go_to_start()
        car_manager.level_up()
        scoreboard.level_increase()
    
screen.exitonclick()
