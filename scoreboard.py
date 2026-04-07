from turtle import Turtle

import settings


class Scoreboard:
    def __init__(self):
        self.hud_turtle = Turtle()
        self.hud_turtle.hideturtle()
        self.hud_turtle.penup()

        self.overlay_turtle = Turtle()
        self.overlay_turtle.hideturtle()
        self.overlay_turtle.penup()
        self.theme_name = "dark"

    def draw_hud(self, stats):
        self.hud_turtle.clear()
        self.hud_turtle.color(settings.THEMES[self.theme_name]["hud"])
        self.hud_turtle.goto(-285, 260)
        self.hud_turtle.write(
            f"Level: {stats.level}  Lives: {stats.lives}  Score: {stats.score}  "
            f"Best Score: {stats.best_score}  Best Level: {stats.best_level}  Streak: {stats.streak}",
            font=settings.HUD_FONT,
            align="left",
        )

    def set_theme(self, theme_name: str):
        self.theme_name = theme_name
        theme = settings.THEMES[theme_name]
        self.hud_turtle.color(theme["hud"])
        self.overlay_turtle.color(theme["overlay"])

    def clear_overlay(self):
        self.overlay_turtle.clear()

    def show_menu(self):
        self.overlay_turtle.clear()
        self.overlay_turtle.goto(0, 70)
        self.overlay_turtle.write("Turtle Crossing Game+", align="center", font=settings.TITLE_FONT)
        self.overlay_turtle.goto(0, 20)
        self.overlay_turtle.write("Press SPACE to start", align="center", font=settings.HUD_FONT)
        self.overlay_turtle.goto(0, -20)
        self.overlay_turtle.write("Arrow keys move • P pause • R restart", align="center", font=settings.HUD_FONT)
        self.overlay_turtle.goto(0, -60)
        self.overlay_turtle.write("T toggle theme • A accessibility mode", align="center", font=settings.HUD_FONT)

    def show_paused(self):
        self.overlay_turtle.clear()
        self.overlay_turtle.goto(0, 0)
        self.overlay_turtle.write("PAUSED", align="center", font=settings.TITLE_FONT)

    def show_game_over(self):
        self.overlay_turtle.clear()
        self.overlay_turtle.goto(0, 20)
        self.overlay_turtle.write("GAME OVER", align="center", font=settings.TITLE_FONT)
        self.overlay_turtle.goto(0, -20)
        self.overlay_turtle.write("Press R to restart", align="center", font=settings.HUD_FONT)

    def show_win(self):
        self.overlay_turtle.clear()
        self.overlay_turtle.goto(0, 20)
        self.overlay_turtle.write("YOU WIN!", align="center", font=settings.TITLE_FONT)
        self.overlay_turtle.goto(0, -20)
        self.overlay_turtle.write("Press R to play again", align="center", font=settings.HUD_FONT)

    def flash(self, message: str):
        self.overlay_turtle.clear()
        self.overlay_turtle.goto(0, -90)
        self.overlay_turtle.write(message, align="center", font=settings.HUD_FONT)
