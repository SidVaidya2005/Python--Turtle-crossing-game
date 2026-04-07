from turtle import Turtle

import settings


class Player(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("turtle")
        self.penup()
        self.setheading(90)
        self.go_to_start()

    def move_up(self):
        self.sety(self.ycor() + settings.PLAYER_MOVE_DISTANCE)

    def move_left(self):
        self.setx(max(-settings.PLAYER_BOUNDARY_X, self.xcor() - settings.PLAYER_MOVE_DISTANCE))

    def move_right(self):
        self.setx(min(settings.PLAYER_BOUNDARY_X, self.xcor() + settings.PLAYER_MOVE_DISTANCE))

    def go_to_start(self):
        self.goto(settings.PLAYER_START_X, settings.PLAYER_START_Y)

    def is_at_finish_line(self):
        return self.ycor() >= settings.PLAYER_FINISH_LINE_Y
