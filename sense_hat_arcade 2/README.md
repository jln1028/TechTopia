# Sense HAT Arcade — Enhanced Edition

Six Python games for a physical Raspberry Pi Sense HAT: Marble Maze, Tetris Survival, Snake, Asteroid Dodge, Joysticker, and Light Racer.

## New features

- Six different 8×8 LED menu icons (one for each game), all with a cyan background.
- Three-second LED countdown (3, 2, 1) before gameplay, including restarts.
- Individual best scores retained during the running arcade session.
- After game over, the LED matrix scrolls `S<score> H<best>` (S = score, H = high score), then displays the game-over frame. The selected game's best score also prints in the terminal when browsing the menu.
- Middle joystick press restarts the current game; at game over, left/up returns to menu.

## Install and run

On Raspberry Pi OS with a Sense HAT installed, make sure the Sense HAT Python package is available (on many systems: `sudo apt install sense-hat`). Extract the ZIP and open a terminal in `sense_hat_arcade`:

```bash
python3 -m unittest discover -v
python3 run_on_pi.py
```

## Joystick controls

- **Menu:** left/right/up/down cycles between six game icons; middle selects.
- **Countdown:** wait for 3, 2, 1; middle restarts the countdown.
- **Playing:** use directional controls; middle restarts with countdown.
- **Game over:** middle restarts; left/up returns to menu.

## Game rules

- Marble Maze: navigate walls to the yellow goal; 100 points.
- Tetris Survival: dodge falling red blocks; 1 point per avoided block.
- Snake: collect red apples; 10 points per apple; starts with three apples and adds one on-screen apple for every three eaten, up to eight when space permits.
- Asteroid Dodge: avoid falling red asteroids; 1 point per avoided asteroid.
- Joysticker: match the blue direction arrow within two seconds; 10 points per correct response.
- Light Racer: avoid the border and your trail; 1 point per successful move.

## Red / Green TDD

New tests were written first and run against the previous implementation. They failed (5 failures, 1 error), demonstrating missing countdown, restart, and best-score features. The implementation and existing tests were then updated for the new countdown behavior. All **17 automated tests pass** on a non-Pi machine. `py_compile` also passes for all Python files.

The tests verify logic, not physical Sense HAT behavior. Test LED orientation, scrolling, joystick events, and timing on the real device. Best scores are **session-only**, not saved to disk. The score scroll temporarily blocks gameplay, only after game over.

## AI-drafted code and licensing

This code was drafted with AI tools (ChatGPT and Claude) without reference material. No license has been assigned to it yet. See [`NOTICE.md`](../NOTICE.md).
