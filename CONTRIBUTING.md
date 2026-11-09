# Contributing to TechTopia

This guide gets a new contributor from clone to a first passing test, and describes the conventions to follow.

## 1. Get set up (about 5 minutes)

```bash
git clone https://github.com/jln1028/TechTopia.git
cd TechTopia
python3 --version        # Python 3 is all you need for logic and tests
```

You do **not** need a Raspberry Pi to contribute to the Python logic or the HTML pages. You do need one (with a Sense HAT) to verify LED, joystick and sensor behaviour.

## 2. Verify your environment

Run every project's tests from the repository root:

```bash
python3 run_tests.py
```

Or run one project's tests from inside its folder:

```bash
cd sensehat_compass
python3 -m unittest -v
```

Running `unittest discover` directly from the repository root finds no tests; use `run_tests.py` instead.

Run a single test:

```bash
python3 -m unittest -v test_compass.CompassTests.test_cardinal_boundaries
```

## 3. Find your way around

| If you want to... | Look at |
|---|---|
| Understand the whole repo | [`README.md`](README.md), then [`docs/repository-guide.md`](docs/repository-guide.md) |
| Change game or compass logic | The `*_core.py` / `maze_logic.py` / `controls.py` module and its `test_*.py` |
| Change what appears on the Sense HAT | The hardware runner (`compass_app.py`, `arcade.py`, `marble_maze.py`, `run_on_pi.py`) |
| Edit a lesson, quiz or team guide | The matching `.html` file; each is a single self-contained page |

## 4. Python conventions

- **Keep logic and hardware separate.** Never import `sense_hat` in a module covered by tests. Put rules in the core module and keep the runner thin.
- **Frames** are flat lists of 64 `(r, g, b)` tuples, index `y*8 + x`.
- **Joystick events:** ignore anything where `event.action != 'pressed'`.
- **Determinism:** accept a `seed` or `rng` argument and advance time through `step()` / `tick(delta)` instead of calling `time.sleep` in core code.
- **Blocking messages:** after `show_message`, call `sense.stick.get_events()` to discard queued presses.
- **Runners:** set `sense.low_light = True` and call `sense.clear()` in a `finally` block.
- **Style:** existing files differ (compact style in `compass_core.py` and `arcade_core.py`, PEP 8 elsewhere). Match the file you are editing; do not reformat unrelated code.
- **Tests first:** the projects were built red/green. Write a failing `unittest` case, then implement.

## 5. Adding a new Sense HAT example (extra exploration)

1. Create a folder named `sensehat_<name>/` (lowercase, underscores).
2. Add `<name>_core.py` (no `sense_hat` import), `<name>_app.py` (runner) and `test_<name>.py`.
3. Add a `README.md` with: what it does, controls, how to run tests, how to run on a Pi, limitations.
4. Add a row to the layout tables in [`README.md`](README.md) and to `docs/projects.md`. `run_tests.py` picks up the new folder automatically.

## 6. Editing HTML lessons and guides

- Pages are standalone files; open them directly in a browser to check your change.
- Add new pages to the folder's `index.html` and to the matching page under `docs/`.
- Keep numbering for the intro lessons (`1-`, `2-`, ...) so the learning path stays obvious.
- State which SDK a page uses: `pitop` (Foundation/Expansion Plate components) or `sense_hat`.
- Do not claim a code sample is hardware-verified unless you ran it on the device.

## 7. Before you commit

- [ ] `python3 run_tests.py` passes (CI runs the same script).
- [ ] New or changed behaviour has a test.
- [ ] README tables updated if you added, renamed or removed a folder.
- [ ] No generated files (`__pycache__/`, `.DS_Store`) are staged; both are in `.gitignore`.
- [ ] `high_scores.json` (created at runtime by `sense_hat_arcade`) is not committed unless intended.

## 8. Reporting hardware results

If you test on a real Sense HAT or pi-top, record the device, OS version and what you observed (orientation, timing, joystick behaviour). This is currently the biggest documentation gap.
