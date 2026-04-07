from turtle import Turtle
import random

import settings
from game_logic import DifficultyModel


class CarManager:
    def __init__(self):
        self.rng = random.Random()
        self.difficulty_model = DifficultyModel()
        self.all_cars = []
        self.level = settings.INITIAL_LEVEL
        self.accessibility_mode = False
        self._refresh_level_settings()

    def _refresh_level_settings(self):
        self.spawn_probability = self.difficulty_model.spawn_probability(self.level)
        self.lane_density_cap = self.difficulty_model.lane_density_cap(self.level)
        self.level_speed_multiplier = self.difficulty_model.level_speed_multiplier(self.level)
        self.active_lanes = self.difficulty_model.active_lanes()

    def move_cars(self):
        for obstacle in self.all_cars:
            sprite = obstacle["sprite"]
            sprite.setx(sprite.xcor() + (obstacle["speed"] * obstacle["direction"]))

    def _lane_counts(self) -> dict[int, int]:
        lane_counts = {lane: 0 for lane in self.active_lanes}
        for obstacle in self.all_cars:
            lane_counts[obstacle["lane"]] += 1
        return lane_counts

    def create_car(self):
        if self.rng.random() > self.spawn_probability:
            return

        lane_counts = self._lane_counts()
        available_lanes = [lane for lane, count in lane_counts.items() if count < self.lane_density_cap]
        if not available_lanes:
            return

        lane = self.rng.choice(available_lanes)
        obstacle_type = self.difficulty_model.choose_obstacle_type(self.level, self.rng)
        config = settings.OBSTACLE_TYPES[obstacle_type]

        direction = 1 if obstacle_type == "opposite" else -1
        start_x = (
            -(settings.SCREEN_WIDTH // 2 + 40)
            if direction == 1
            else (settings.SCREEN_WIDTH // 2 + 40)
        )

        sprite = Turtle("square")
        sprite.penup()
        sprite.color(self.rng.choice(settings.CAR_COLORS))
        sprite.shapesize(stretch_len=config["stretch_len"], stretch_wid=1)
        sprite.goto(start_x, lane)

        speed = (
            settings.BASE_CAR_SPEED
            * self.level_speed_multiplier
            * config["speed_multiplier"]
            * self.difficulty_model.lane_speed_variation(lane)
        )
        if self.accessibility_mode:
            speed *= 0.75

        self.all_cars.append(
            {
                "sprite": sprite,
                "lane": lane,
                "kind": obstacle_type,
                "direction": direction,
                "speed": speed,
                "hitbox": max(12, config["hitbox"] - (4 if self.accessibility_mode else 0)),
            }
        )

    def cleanup_offscreen(self):
        min_x = -(settings.SCREEN_WIDTH // 2 + settings.OFFSCREEN_PADDING)
        max_x = settings.SCREEN_WIDTH // 2 + settings.OFFSCREEN_PADDING
        kept = []
        for obstacle in self.all_cars:
            x = obstacle["sprite"].xcor()
            if min_x <= x <= max_x:
                kept.append(obstacle)
            else:
                obstacle["sprite"].hideturtle()
        self.all_cars = kept

    def check_collision(self, player) -> bool:
        for obstacle in self.all_cars:
            if player.distance(obstacle["sprite"]) < obstacle["hitbox"]:
                return True
        return False

    def set_level(self, level: int):
        self.level = max(settings.INITIAL_LEVEL, level)
        self._refresh_level_settings()

    def set_accessibility_mode(self, enabled: bool):
        self.accessibility_mode = enabled
        self._refresh_level_settings()

    def reset(self, level: int):
        self.clear_all()
        self.level = max(settings.INITIAL_LEVEL, level)
        self._refresh_level_settings()

    def clear_all(self):
        for obstacle in self.all_cars:
            obstacle["sprite"].hideturtle()
        self.all_cars.clear()
