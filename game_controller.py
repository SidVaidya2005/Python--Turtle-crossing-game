import time
from turtle import Screen, Terminator

import settings
from car_manager import CarManager
from game_logic import GameStats, StatsStorage
from lane_markers import LaneMarkers
from player import Player
from scoreboard import Scoreboard


class GameController:
    def __init__(self):
        self.screen = Screen()
        self.screen.setup(width=settings.SCREEN_WIDTH, height=settings.SCREEN_HEIGHT)
        self.screen.title(settings.WINDOW_TITLE)
        self.screen.tracer(0)

        self.theme_name = "dark"
        self.state = settings.STATE_MENU
        self.accessibility_mode = False

        self.storage = StatsStorage(settings.PERSISTENCE_FILE)
        self.stats = GameStats(self.storage.load())

        self.player = Player()
        self.car_manager = CarManager()
        self.scoreboard = Scoreboard()
        self.lane_markers = LaneMarkers(theme_name=self.theme_name)

        self._apply_theme()
        self.lane_markers.draw()
        self.scoreboard.draw_hud(self.stats)
        self.scoreboard.show_menu()

        self._bind_controls()

    def _bind_controls(self):
        self.screen.listen()
        self.screen.onkey(self.start_game, "space")
        self.screen.onkey(self.toggle_pause, "p")
        self.screen.onkey(self.restart, "r")
        self.screen.onkey(self.toggle_theme, "t")
        self.screen.onkey(self.toggle_accessibility_mode, "a")
        self.screen.onkey(self.move_up, "Up")
        self.screen.onkey(self.move_left, "Left")
        self.screen.onkey(self.move_right, "Right")

    def _apply_theme(self):
        theme = settings.THEMES[self.theme_name]
        self.screen.bgcolor(theme["bg"])
        self.scoreboard.set_theme(self.theme_name)
        self.lane_markers.set_theme(self.theme_name)
        self.scoreboard.draw_hud(self.stats)

    def toggle_theme(self):
        self.theme_name = "light" if self.theme_name == "dark" else "dark"
        self._apply_theme()
        if self.state == settings.STATE_MENU:
            self.scoreboard.show_menu()
        elif self.state == settings.STATE_PAUSED:
            self.scoreboard.show_paused()
        elif self.state == settings.STATE_GAME_OVER:
            self.scoreboard.show_game_over()
        elif self.state == settings.STATE_WIN:
            self.scoreboard.show_win()

    def toggle_accessibility_mode(self):
        self.accessibility_mode = not self.accessibility_mode
        self.car_manager.set_accessibility_mode(self.accessibility_mode)
        status = "ON" if self.accessibility_mode else "OFF"
        self.scoreboard.flash(f"Accessibility mode: {status}")

    def start_game(self):
        if self.state != settings.STATE_MENU:
            return
        self.state = settings.STATE_RUNNING
        self.scoreboard.clear_overlay()

    def toggle_pause(self):
        if self.state == settings.STATE_RUNNING:
            self.state = settings.STATE_PAUSED
            self.scoreboard.show_paused()
        elif self.state == settings.STATE_PAUSED:
            self.state = settings.STATE_RUNNING
            self.scoreboard.clear_overlay()

    def restart(self):
        if self.state not in {settings.STATE_GAME_OVER, settings.STATE_WIN, settings.STATE_RUNNING, settings.STATE_PAUSED}:
            return
        self.stats.reset_for_new_game()
        self.player.go_to_start()
        self.car_manager.reset(level=self.stats.level)
        self.state = settings.STATE_RUNNING
        self.scoreboard.clear_overlay()
        self.scoreboard.draw_hud(self.stats)

    def move_up(self):
        if self.state == settings.STATE_RUNNING:
            self.player.move_up()

    def move_left(self):
        if self.state == settings.STATE_RUNNING:
            self.player.move_left()

    def move_right(self):
        if self.state == settings.STATE_RUNNING:
            self.player.move_right()

    def _step_running_game(self):
        self.car_manager.set_level(self.stats.level)
        self.car_manager.create_car()
        self.car_manager.move_cars()
        self.car_manager.cleanup_offscreen()

        if self.car_manager.check_collision(self.player):
            self.stats.register_collision()
            self.player.go_to_start()
            self.car_manager.clear_all()
            self.scoreboard.flash("Hit! Watch out.")
            if self.stats.is_game_over():
                self.state = settings.STATE_GAME_OVER
                self.scoreboard.show_game_over()
                self.stats.persist(self.storage)

        if self.player.is_at_finish_line() and self.state == settings.STATE_RUNNING:
            gained = self.stats.register_crossing()
            self.player.go_to_start()
            self.car_manager.set_level(self.stats.level)
            self.scoreboard.flash(f"+{gained} points")
            if self.stats.has_won():
                self.state = settings.STATE_WIN
                self.scoreboard.show_win()
                self.stats.persist(self.storage)

        self.scoreboard.draw_hud(self.stats)

    def run(self):
        while True:
            time.sleep(settings.FRAME_DELAY_SECONDS)
            try:
                if self.state == settings.STATE_RUNNING:
                    self._step_running_game()
                self.screen.update()
            except Terminator:
                self.stats.persist(self.storage)
                break
