# Extra exploration: activity sheets

Optional activities for the four Sense HAT Python examples, for students who have finished [lesson 5](lessons.md). Each sheet follows the same pattern: **Run it, Predict and change it, Read the tests, Extend it.**

**Before you start**

- You need a Raspberry Pi (or pi-top) with a Sense HAT, and the example's folder.
- Run the examples from inside their own folder, for example `cd sensehat_compass`.
- Make a copy of the file before you change it, or use `git checkout <file>` to undo.
- To check that your change did not break anything, run the tests from the repository root: `python3 run_tests.py` (the tests do not need a Sense HAT).
- Joystick controls for each example are in its README.

!!! warning "Not yet verified on hardware"
    The example code has been run on pi-top hardware by the maintainer. If something does not behave as the sheet says, note what you saw: that is useful feedback.

Difficulty: ★ easy, ★★ medium, ★★★ challenge.

---

## 1. Compass (`sensehat_compass`)

Run with `python3 compass_app.py`. Move the joystick up, right or middle for the next mode, and down or left for the previous one.

**Run it (★)**

1. Turn the board slowly. Does the arrow always point the same way? Compare with a phone compass.
2. Switch through the three modes. Which one is easiest to read at a glance? Why?

**Predict and change it (★)** — in `compass_core.py`

| Change | Predict first |
|---|---|
| Edit the colours `RED`, `BLUE` and `WHITE` at the top | What will the arrow look like? |
| Change `MODES` to `('cardinal','arrow','numeric')` | Which mode appears first after you switch? (Check the starting mode in `compass_app.py` too.) |
| Change `22.5` to `10` in `cardinal()` | What happens to the directions in the compass? Test with the tests below. |

**Read the tests (★★)** — `test_compass.py`

- `test_cardinal_boundaries` lists angles such as `22.49` and `22.5`. Why were those two chosen?
- `test_arrow_points_east_for_ninety` checks a single pixel. Which one, and why that pixel?

**Extend it (★★ / ★★★)**

- ★★ Add a fourth mode that shows only a red dot at north.
- ★★★ Add a "magnetic declination" setting so the compass can show true north for your location, and write a test for it. The README explains why declination is not applied now.

---

## 2. Marble maze (`sensehat_maze_joystick`)

Run with `python3 marble_maze.py`. Push the joystick to move one step, and press the centre button to switch between joystick and tilt.

**Run it (★)**

1. Reach the green goal in joystick mode, then in tilt mode. Which is harder?
2. If tilt moves the marble the wrong way, the README says to adjust `tilt_step`. Try it.

**Predict and change it (★)** — in `maze_logic.py`

| Change | Predict first |
|---|---|
| Change `threshold=0.35` in `tilt_step` to `0.15` | Will the marble be easier or harder to hold still? |
| Change `GOAL`'s position (and keep it reachable) | What else must change so the maze still works? |
| In `marble_maze.py`, change `time.sleep(0.18)` | What happens to the feel of the game? |

**Read the tests (★★)** — `test_maze_logic.py`, `test_controls.py`

- `test_1000_mazes_are_valid_and_solvable` generates 1000 mazes. Why test so many instead of one?
- `test_tilt_deadzone_and_single_axis`: what is the "deadzone", and what value is it testing?

**Extend it (★★ / ★★★)**

- ★★ Add a move counter and show it after each round.
- ★★★ Add a timer and award a better score for faster solutions, with a test.

---

## 3. Arcade (`sense_hat_arcade`)

Run with `python3 arcade.py`. Pick a game, then a difficulty. There are three games: Tetris Survival, Jumpy Cubes and Flood Escape.

**Run it (★)**

1. Play each game on Easy, then on Hard. What changes?
2. Beat a high score and quit. Restart the arcade: is it still there? (Scores are saved in `high_scores.json`.)

**Predict and change it (★)** — in `arcade_core.py`

| Change | Predict first |
|---|---|
| In `TetrisGame`, change `self.health=5` | How does the game change? |
| In `DIFFICULTY_SETTINGS`, change the `'hard'` numbers | Which one makes the game faster, and which makes hazards more frequent? |
| In `JumpyGame`, change the `arc=(6,5,5,6,6,7)` tuple | What happens to the height and length of a jump? |
| In `FloodGame`, add a coin to `self.coins` (use a spot over a platform) | What must you do for the player to win? |

**Read the tests (★★)** — `test_arcade_core.py`, `test_arcade_features.py`

- `test_difficulty_changes_game_speed_and_spawning`: what exactly is measured?
- `test_corrupt_scores_recover`: what is the file doing, and why should the game not crash?

**Extend it (★★ / ★★★)**

- ★★ Add a fourth difficulty called `'insane'` and make it selectable.
- ★★★ Add a new game class with `handle`, `step` and `pixels`, and add it to the menu.

---

## 4. Enhanced arcade (`sense_hat_arcade 2`)

Run with `python3 run_on_pi.py`. Six games: Marble Maze, Tetris Survival, Snake, Asteroid Dodge, Joysticker and Light Racer. Press the middle button to restart the current game.

**Run it (★)**

1. Play all six. Which uses the joystick in the most interesting way?
2. Watch the 3, 2, 1 countdown. What does the middle button do during it?

**Predict and change it (★)** — in `arcade.py`

| Change | Predict first |
|---|---|
| Change the `MAZE` rows (keep a `G` for the goal) | Can you still reach the goal? |
| In `Arcade.start`, change `self.delay=0.35` | Which games get faster or slower? |
| In `Joysticker`, change the `2.0` second limit (in `start` and `tick`) | How does the game feel with 1 second? |
| Edit one of the `ICONS` rows | What changes in the menu? |

**Read the tests (★★)** — `test_arcade.py`, `test_improvements.py`

- `test_no_reverse_snake`: why must a snake not reverse into itself?
- `test_countdown_no_game_movement`: why does the game ignore input during the countdown?

**Extend it (★★ / ★★★)**

- ★★ Make best scores survive between sessions. (The README says they last only for the running session. The classic arcade's `high_scores.py` is one way to do it.)
- ★★★ Add a seventh game and its menu icon.

---

## Tips for all examples

- **Hardware-free core.** Game rules live in a module that never imports `sense_hat`. That is why the tests can run on any computer. Put new rules there and keep the runner script small.
- **Pixels.** A frame is a list of 64 `(r, g, b)` colours. The pixel at column `x`, row `y` is at index `y*8 + x`.
- **Test first.** Write a failing test for your change, then make it pass.
- **Share what you learn.** If you test on a real Sense HAT, note the device and OS version and what you observed.
