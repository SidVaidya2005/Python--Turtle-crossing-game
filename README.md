# Python--Turtle-crossing-game

A Turtle-based crossing game with progression, scoring, obstacle variety, and persistent best stats.

## Features

- Start menu, pause/resume, restart flow
- State machine: `menu`, `running`, `paused`, `game_over`, `win`
- Lives system and positive win condition
- Scoring system with:
  - crossing base points
  - level bonus
  - survival bonus (remaining lives)
  - streak bonus
- Best score and best level persistence in `save_data.json`
- Dynamic difficulty:
  - increasing spawn probability
  - lane density cap scaling
  - level speed scaling
  - lane speed variation
- Obstacle variety:
  - normal cars
  - fast cars
  - trucks (wider hitbox)
  - opposite-direction hazards
- Safe lanes and visual lane markers
- Theme toggle and accessibility mode

## Controls

- `SPACE` → Start from menu
- `↑` → Move up
- `←` / `→` → Move left / right (bounded)
- `P` → Pause / Resume
- `R` → Restart (during play or after end state)
- `T` → Toggle light/dark theme
- `A` → Toggle accessibility mode (slower obstacles + larger hitboxes)

## Gameplay Rules

- Reach the top finish line to advance levels and gain score.
- Colliding with an obstacle loses one life and applies score penalty.
- Game ends at 0 lives.
- You win when you reach the target level.
- Best score and best level are saved locally.

## Project Structure

- `main.py`: entrypoint
- `game_controller.py`: top-level orchestration and state transitions
- `settings.py`: all tunable constants and UI theme values
- `game_logic.py`: testable progression/scoring/persistence/difficulty logic
- `player.py`: player movement and boundary behavior
- `car_manager.py`: obstacle spawn/move/collision/cleanup lifecycle
- `scoreboard.py`: HUD and overlay rendering
- `lane_markers.py`: lane and safe-zone rendering

## Extension Points

- Add new obstacle types in `settings.OBSTACLE_TYPES` and adjust balancing in `DifficultyModel.obstacle_weights`.
- Tune pacing in `settings.py` (spawn chance, speed multipliers, lane density cap).
- Add new game states or overlays in `game_controller.py` + `scoreboard.py`.
- Expand scoring by adjusting formulas in `GameStats.register_crossing`.

## Testing

Run unit tests for non-graphics logic:

```bash
python -m unittest discover -s tests -q
```
