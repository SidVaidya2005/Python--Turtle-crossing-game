from pathlib import Path

# Screen
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
WINDOW_TITLE = "Turtle Crossing Game+"
FRAME_DELAY_SECONDS = 0.1

# Game states
STATE_MENU = "menu"
STATE_RUNNING = "running"
STATE_PAUSED = "paused"
STATE_GAME_OVER = "game_over"
STATE_WIN = "win"

# Player
PLAYER_START_X = 0
PLAYER_START_Y = -280
PLAYER_FINISH_LINE_Y = 280
PLAYER_MOVE_DISTANCE = 20
PLAYER_BOUNDARY_X = 280

# Progression
INITIAL_LEVEL = 1
INITIAL_LIVES = 3
TARGET_WIN_LEVEL = 8

# Scoring
SCORE_CROSSING_BASE = 100
SCORE_LEVEL_MULTIPLIER = 20
SCORE_SURVIVAL_BONUS = 15
SCORE_STREAK_BONUS_STEP = 10
SCORE_COLLISION_PENALTY = 40

# Difficulty and obstacles
CAR_COLORS = ["red", "orange", "yellow", "green", "blue", "purple", "cyan", "magenta"]
LANES = list(range(-250, 251, 50))
SAFE_LANES = {-250, 250}
BASE_SPAWN_PROBABILITY = 0.18
SPAWN_PROBABILITY_INCREMENT = 0.03
MAX_SPAWN_PROBABILITY = 0.62
BASE_LANE_DENSITY_CAP = 1
LANE_DENSITY_INCREMENT_EVERY_LEVELS = 2
MAX_LANE_DENSITY_CAP = 3
BASE_CAR_SPEED = 8.0
LEVEL_SPEED_MULTIPLIER = 0.13
OFFSCREEN_PADDING = 80

OBSTACLE_TYPES = {
    "normal": {"weight": 70, "speed_multiplier": 1.0, "stretch_len": 2.0, "hitbox": 20},
    "fast": {"weight": 16, "speed_multiplier": 1.6, "stretch_len": 2.0, "hitbox": 20},
    "truck": {"weight": 10, "speed_multiplier": 0.8, "stretch_len": 3.2, "hitbox": 28},
    "opposite": {"weight": 4, "speed_multiplier": 1.1, "stretch_len": 2.4, "hitbox": 24},
}

# Persistence
PERSISTENCE_FILE = Path(__file__).resolve().parent / "save_data.json"

# UI
HUD_FONT = ("Courier", 16, "normal")
TITLE_FONT = ("Courier", 24, "bold")
THEMES = {
    "dark": {
        "bg": "black",
        "hud": "white",
        "overlay": "white",
        "safe_lane": "#1f5130",
        "lane": "#5f6368",
    },
    "light": {
        "bg": "white",
        "hud": "black",
        "overlay": "black",
        "safe_lane": "#9dd9b5",
        "lane": "#b7b7b7",
    },
}
