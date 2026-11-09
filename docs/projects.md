# Sense HAT projects

Four independent Python projects for the Raspberry Pi Sense HAT. The logic is testable on any computer; only the runner script needs the hardware.

| Project | What it does | Run on a Pi | Details |
|---|---|---|---|
| Compass (`sensehat_compass`) | Joystick-controlled compass: arrow, cardinal and numeric modes | `python3 compass_app.py` | [README](https://github.com/jln1028/TechTopia/blob/main/sensehat_compass/README.md) |
| Maze (`sensehat_maze_joystick`) | Marble maze by joystick or tilt | `python3 marble_maze.py` | [README](https://github.com/jln1028/TechTopia/blob/main/sensehat_maze_joystick/README.md) |
| Arcade (`sense_hat_arcade`) | 3 games, difficulty levels, persistent high scores | `python3 arcade.py` | [README](https://github.com/jln1028/TechTopia/blob/main/sense_hat_arcade/README.md) |
| Enhanced arcade (`sense_hat_arcade 2`) | 6 games, countdown, session-only best scores | `python3 run_on_pi.py` | [README](https://github.com/jln1028/TechTopia/blob/main/sense_hat_arcade%202/README.md) |

The two arcades are different codebases, not versions of one program.

## Run the tests

From the repository root, on any computer with Python 3:

```bash
python3 run_tests.py
```

To run one project or one test, work inside the project folder:

```bash
cd sensehat_compass
python3 -m unittest -v test_compass.CompassTests.test_cardinal_boundaries
```

Running `unittest discover` from the repository root finds no tests, because each project imports its modules by bare name.

## Design

Logic modules never import `sense_hat`; only the runner does.

| Project | Testable logic | Hardware runner |
|---|---|---|
| Compass | `compass_core.py` | `compass_app.py` |
| Maze | `maze_logic.py`, `controls.py` | `marble_maze.py` |
| Arcade | `arcade_core.py`, `high_scores.py` | `arcade.py` |
| Enhanced arcade | `arcade.py` | `run_on_pi.py` |

`arcade.py` is the hardware runner in the arcade and the pure game logic in the enhanced arcade.

!!! warning "Not yet hardware-verified"
    Check LED orientation, timing, joystick events and sensor readings on a real Sense HAT.
