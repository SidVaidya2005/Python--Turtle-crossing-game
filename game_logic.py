import json
import random
from dataclasses import dataclass
from pathlib import Path

import settings


class DifficultyModel:
    def spawn_probability(self, level: int) -> float:
        return min(
            settings.MAX_SPAWN_PROBABILITY,
            settings.BASE_SPAWN_PROBABILITY + (max(level, 1) - 1) * settings.SPAWN_PROBABILITY_INCREMENT,
        )

    def lane_density_cap(self, level: int) -> int:
        cap = settings.BASE_LANE_DENSITY_CAP + (max(level, 1) - 1) // settings.LANE_DENSITY_INCREMENT_EVERY_LEVELS
        return min(settings.MAX_LANE_DENSITY_CAP, cap)

    def level_speed_multiplier(self, level: int) -> float:
        return 1.0 + (max(level, 1) - 1) * settings.LEVEL_SPEED_MULTIPLIER

    def lane_speed_variation(self, lane_y: int) -> float:
        lane_bucket = abs(lane_y) // 50
        return 0.9 + (lane_bucket % 3) * 0.1

    def active_lanes(self) -> list[int]:
        return [lane for lane in settings.LANES if lane not in settings.SAFE_LANES]

    def obstacle_weights(self, level: int) -> dict[str, int]:
        level = max(level, 1)
        fast_boost = min(10, level - 1)
        truck_boost = min(8, max(0, level - 2))
        opposite_boost = min(6, max(0, level - 3))
        normal_drop = fast_boost + truck_boost + opposite_boost
        normal_weight = max(40, settings.OBSTACLE_TYPES["normal"]["weight"] - normal_drop)

        return {
            "normal": normal_weight,
            "fast": settings.OBSTACLE_TYPES["fast"]["weight"] + fast_boost,
            "truck": settings.OBSTACLE_TYPES["truck"]["weight"] + truck_boost,
            "opposite": settings.OBSTACLE_TYPES["opposite"]["weight"] + opposite_boost,
        }

    def choose_obstacle_type(self, level: int, rng: random.Random | None = None) -> str:
        rng = rng or random
        weights = self.obstacle_weights(level)
        names = list(weights.keys())
        probs = [weights[name] for name in names]
        return rng.choices(names, weights=probs, k=1)[0]


@dataclass
class BestStats:
    best_score: int = 0
    best_level: int = settings.INITIAL_LEVEL


class StatsStorage:
    def __init__(self, path: Path):
        self.path = path

    def load(self) -> BestStats:
        if not self.path.exists():
            return BestStats()
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
            return BestStats(
                best_score=max(0, int(data.get("best_score", 0))),
                best_level=max(settings.INITIAL_LEVEL, int(data.get("best_level", settings.INITIAL_LEVEL))),
            )
        except (json.JSONDecodeError, OSError, ValueError, TypeError):
            return BestStats()

    def save(self, best_stats: BestStats) -> None:
        payload = {"best_score": best_stats.best_score, "best_level": best_stats.best_level}
        self.path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


class GameStats:
    def __init__(self, best_stats: BestStats):
        self.best_score = best_stats.best_score
        self.best_level = best_stats.best_level
        self.reset_for_new_game()

    def reset_for_new_game(self) -> None:
        self.level = settings.INITIAL_LEVEL
        self.lives = settings.INITIAL_LIVES
        self.score = 0
        self.streak = 0
        self.max_streak = 0

    def register_crossing(self) -> int:
        gained = (
            settings.SCORE_CROSSING_BASE
            + (self.level * settings.SCORE_LEVEL_MULTIPLIER)
            + (self.lives * settings.SCORE_SURVIVAL_BONUS)
            + (self.streak * settings.SCORE_STREAK_BONUS_STEP)
        )
        self.score += gained
        self.streak += 1
        self.max_streak = max(self.max_streak, self.streak)
        self.level += 1
        self._refresh_bests()
        return gained

    def register_collision(self) -> None:
        self.streak = 0
        self.lives -= 1
        self.score = max(0, self.score - settings.SCORE_COLLISION_PENALTY)
        self._refresh_bests()

    def is_game_over(self) -> bool:
        return self.lives <= 0

    def has_won(self) -> bool:
        return self.level >= settings.TARGET_WIN_LEVEL

    def _refresh_bests(self) -> None:
        self.best_score = max(self.best_score, self.score)
        self.best_level = max(self.best_level, self.level)

    def persist(self, storage: StatsStorage) -> None:
        self._refresh_bests()
        storage.save(BestStats(best_score=self.best_score, best_level=self.best_level))

