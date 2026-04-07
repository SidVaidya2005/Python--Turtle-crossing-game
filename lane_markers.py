from turtle import Turtle

import settings


class LaneMarkers:
    def __init__(self, theme_name: str = "dark"):
        self.theme_name = theme_name
        self.turtle = Turtle()
        self.turtle.hideturtle()
        self.turtle.penup()
        self.turtle.speed("fastest")

    def set_theme(self, theme_name: str):
        self.theme_name = theme_name
        self.draw()

    def draw(self):
        self.turtle.clear()
        for lane_y in settings.LANES:
            color = (
                settings.THEMES[self.theme_name]["safe_lane"]
                if lane_y in settings.SAFE_LANES
                else settings.THEMES[self.theme_name]["lane"]
            )
            self.turtle.color(color)
            self.turtle.goto(-(settings.SCREEN_WIDTH // 2), lane_y)
            self.turtle.pendown()
            self.turtle.goto(settings.SCREEN_WIDTH // 2, lane_y)
            self.turtle.penup()
