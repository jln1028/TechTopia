# Sense HAT Arcade 2.0

A joystick-controlled arcade for Raspberry Pi Sense HAT with three games, difficulty selection, restart controls, and persistent high scores.

## Files
- `arcade.py`: Sense HAT hardware interface and LED menus
- `arcade_core.py`: testable game rules and menu controller
- `high_scores.py`: persistent JSON high scores
- `test_arcade_core.py`, `test_arcade_features.py`: automated tests
- `high_scores.json`: created automatically on the first new high score (do not delete if you want to keep records)

## Install
Copy all `.py` files into one directory on a Raspberry Pi with the Sense HAT Python library installed. Run:

```bash
python3 arcade.py
```

Run automated tests on a Raspberry Pi or any computer with Python 3:

```bash
python3 -m unittest discover -v
```

## Controls
- **Game selection:** Left/Right (or Up/Down) to browse, Center to choose.
- **Difficulty:** Left/Down to decrease, Right/Up to increase; Center to start. Easy (green E), Normal (yellow N), Hard (red H).
- **Tetris Survival:** Left/Right move, Up shoots. Center ends the current round.
- **Jumpy Cubes:** Up jumps. Center ends the current round.
- **Flood Escape:** Left/Right move, Up jumps. Center ends the current round.
- **Results screen:** Center to retry same game and level, Left/Down to return to game selection, Right/Up to change difficulty.
- **Quit the program:** Ctrl+C in the terminal.

At the end of each round the Sense HAT scrolls status, score, best score and health (where applicable). A new record displays NEW HIGH SCORE. An exited round is treated as a paused/ended round and its score is eligible for a high score.

## Difficulty rules
- **Easy:** 25% slower simulation ticks; hazards spawn 50% less often, and water rises 50% less often.
- **Normal:** Baseline timing.
- **Hard:** 20% faster simulation ticks; hazards spawn more often and water rises more often.

## Tests and limitations
The project has 18 passing automated unit tests, including six new tests for menu flow, difficulty behavior, restarting, and score persistence. The Sense HAT hardware interface has not been tested on physical hardware. Flood Escape is a compact 8x8 platform game; students should playtest and adjust level difficulty. Tetris crushers are square clusters rather than the seven traditional tetromino shapes. The LED matrix has no sound output.

## AI-drafted code and licensing

This code was drafted with AI tools (ChatGPT and Claude) without reference material. No license has been assigned to it yet. See [`NOTICE.md`](../NOTICE.md).
