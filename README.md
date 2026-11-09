# TechTopia

Classroom materials for the TechTopia Industry Challenge on physical computing: four small Raspberry Pi Sense HAT Python projects, plus HTML lessons, curriculum, quiz and team-guide pages.

## Repository layout

| Folder | What it is |
|---|---|
| [`sensehat_compass/`](sensehat_compass/README.md) | Joystick-controlled compass with arrow, cardinal and numeric heading modes |
| [`sensehat_maze_joystick/`](sensehat_maze_joystick/README.md) | Marble maze controlled by joystick or by tilting the board |
| [`sense_hat_arcade/`](sense_hat_arcade/README.md) | Arcade with 3 games (Tetris Survival, Jumpy Cubes, Flood Escape), difficulty levels and persistent high scores |
| [`sense_hat_arcade 2/`](sense_hat_arcade%202/README.md) | Separate "Enhanced Edition" arcade with 6 games, countdown and session-only best scores |
| [`TechTopia_Industry_Challenge_Intro_Lessons_SenseHat/`](TechTopia_Industry_Challenge_Intro_Lessons_SenseHat/) | Five numbered interactive HTML intro lessons (pi-top [4], terminal, Python, Sense HAT) |
| [`TechTopia_Industry_Challenge_Physical_Computing_Materials/`](TechTopia_Industry_Challenge_Physical_Computing_Materials/README.txt) | Static HTML: curriculum hub, quizzes, and three team build guides |

The projects are independent; none shares code with another. The two arcade folders are different codebases, not versions of one program.

## Requirements

- Python 3 (standard library only for the logic and tests).
- To run on hardware: a Raspberry Pi with a Sense HAT and the `sense-hat` package (`sudo apt install sense-hat`).
- No `requirements.txt`, build step or linter configuration.

## Running tests

Tests use `unittest` and do not need a Sense HAT. Modules import each other by bare name, so run them from inside the project folder:

```bash
cd sensehat_compass            # or any other project folder
python3 -m unittest discover -v
```

Run a single test:

```bash
cd sensehat_compass
python3 -m unittest -v test_compass.CompassTests.test_cardinal_boundaries
```

Running `unittest discover` from the repository root finds no tests.

## Running the programs (on a Raspberry Pi)

| Project | Command |
|---|---|
| Compass | `python3 compass_app.py` |
| Maze | `python3 marble_maze.py` |
| Arcade | `python3 arcade.py` |
| Arcade 2 | `python3 run_on_pi.py` |

Press Ctrl+C to quit. Controls for each program are in its own README.

## Design: hardware-free core, thin hardware shell

Game and compass logic lives in modules that never import `sense_hat`, so it can be tested on any computer. Only the runner script talks to the hardware.

| Project | Testable logic | Hardware runner |
|---|---|---|
| `sensehat_compass` | `compass_core.py` | `compass_app.py` |
| `sensehat_maze_joystick` | `maze_logic.py`, `controls.py` | `marble_maze.py` |
| `sense_hat_arcade` | `arcade_core.py`, `high_scores.py` | `arcade.py` |
| `sense_hat_arcade 2` | `arcade.py` | `run_on_pi.py` |

Note that `arcade.py` is the hardware runner in `sense_hat_arcade` but the pure game logic in `sense_hat_arcade 2`.

Conventions shared across the projects:

- A display frame is a flat list of 64 `(r, g, b)` tuples; the pixel at column `x`, row `y` is index `y*8 + x`.
- Joystick handlers ignore every event whose `action` is not `'pressed'`.
- Tests fake joystick events with `types.SimpleNamespace(direction=..., action='pressed')`.
- Game classes take an optional `seed` or `rng` so behaviour is repeatable in tests.
- After a blocking `show_message`, runners call `sense.stick.get_events()` to discard presses made during the scroll.
- Runners set `sense.low_light = True` and call `sense.clear()` on exit.

## Project notes

- **Compass:** reports magnetic north (no declination). Uses `show_letter` rather than scrolling text so the joystick stays responsive. The `red_results.txt` and `green_results.txt` files record the failing-then-passing TDD runs.
- **Maze:** tilt direction depends on how the board is mounted; adjust `tilt_step` in `maze_logic.py` if movement is reversed.
- **Arcade:** `high_scores.json` is created at runtime on the first new high score.
- **Arcade 2:** best scores last only for the running session.

## Classroom materials

Open the HTML files in a browser; there is no build step.

**Intro lessons** (`TechTopia_Industry_Challenge_Intro_Lessons_SenseHat/`), intended to be taken in order:

1. Using Your pi-top [4]
2. Introduction to the Terminal
3. Pac-Man Terminal Treasure Hunt
4. Intro to Python
5. Sense HAT Interactive Lab

**Challenge materials**: see the [materials README](TechTopia_Industry_Challenge_Physical_Computing_Materials/README.txt) for the contents of each folder:

- `01_Curriculum_Websites/`: Physical Computing Hub
- `02_Student_Assessment/`: 20-question physical computing quiz and a Sense HAT getting-started quiz
- `03_Showcase_Team_Guides/`: Team 1 Smart Security System, Team 2 Reaction Challenge, Team 3 Smart Crosswalk

The Python snippets in these pages target pi-top [4] hardware and were not validated on a device; check SDK component names, ports and sensor ranges before classroom use.

## Known limitations

- The Python projects have not been tested on physical Sense HAT hardware. Check LED orientation, timing, joystick events and sensor readings on the device.
- The materials folder has no embedded hardware photos or background images.
