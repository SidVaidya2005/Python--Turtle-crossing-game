import tempfile
import unittest
from pathlib import Path

import settings
from game_logic import BestStats, DifficultyModel, GameStats, StatsStorage


class TestDifficultyModel(unittest.TestCase):
    def setUp(self):
        self.model = DifficultyModel()

    def test_spawn_probability_scales_and_caps(self):
        low = self.model.spawn_probability(1)
        mid = self.model.spawn_probability(4)
        high = self.model.spawn_probability(100)
        self.assertLess(low, mid)
        self.assertEqual(high, settings.MAX_SPAWN_PROBABILITY)

    def test_lane_density_cap_scales_and_caps(self):
        self.assertEqual(self.model.lane_density_cap(1), settings.BASE_LANE_DENSITY_CAP)
        self.assertGreaterEqual(self.model.lane_density_cap(5), settings.BASE_LANE_DENSITY_CAP)
        self.assertEqual(self.model.lane_density_cap(100), settings.MAX_LANE_DENSITY_CAP)

    def test_active_lanes_exclude_safe_lanes(self):
        active = self.model.active_lanes()
        for lane in settings.SAFE_LANES:
            self.assertNotIn(lane, active)


class TestGameStats(unittest.TestCase):
    def test_crossing_updates_score_level_and_streak(self):
        stats = GameStats(BestStats())
        gained = stats.register_crossing()
        expected = (
            settings.SCORE_CROSSING_BASE
            + settings.INITIAL_LEVEL * settings.SCORE_LEVEL_MULTIPLIER
            + settings.INITIAL_LIVES * settings.SCORE_SURVIVAL_BONUS
        )
        self.assertEqual(gained, expected)
        self.assertEqual(stats.level, settings.INITIAL_LEVEL + 1)
        self.assertEqual(stats.streak, 1)
        self.assertEqual(stats.score, expected)

    def test_collision_reduces_life_resets_streak_and_penalizes_score(self):
        stats = GameStats(BestStats())
        stats.register_crossing()
        stats.register_collision()
        self.assertEqual(stats.lives, settings.INITIAL_LIVES - 1)
        self.assertEqual(stats.streak, 0)
        self.assertGreaterEqual(stats.score, 0)

    def test_win_and_game_over_conditions(self):
        stats = GameStats(BestStats())
        while not stats.has_won():
            stats.register_crossing()
        self.assertTrue(stats.has_won())

        stats = GameStats(BestStats())
        for _ in range(settings.INITIAL_LIVES):
            stats.register_collision()
        self.assertTrue(stats.is_game_over())


class TestStatsStorage(unittest.TestCase):
    def test_persistence_roundtrip(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            path = Path(tmp_dir) / "save_data.json"
            storage = StatsStorage(path)
            storage.save(BestStats(best_score=1234, best_level=9))
            loaded = storage.load()
            self.assertEqual(loaded.best_score, 1234)
            self.assertEqual(loaded.best_level, 9)


if __name__ == "__main__":
    unittest.main()
