# Sense HAT Marble Maze — joystick + tilt

Install `sense-hat` on the Raspberry Pi OS if needed. Keep all Python files together.

Run tests (no Sense HAT required): `python3 -m unittest discover -v`

Run game on Raspberry Pi with Sense HAT: `python3 marble_maze.py`

- Starts in **JOY** mode: push joystick up/down/left/right one step per press.
- Press the **center joystick button** to switch to **TILT** mode; press again to return to **JOY**.
- In tilt mode, tilt the device to move the blue marble.
- White = wall, black = corridor, green = goal, blue = marble.
- Reach the goal to see yellow **Score!** scrolling over blue, then a new maze appears.
- Ctrl+C exits and clears the LED matrix.

Tilt orientation depends on mounting. If movement is reversed, adjust `tilt_step` in `maze_logic.py`.

## License and attribution

Adapted from learning resources by the [Raspberry Pi Foundation](https://www.raspberrypi.org), licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). Changes were made for the TechTopia classroom, including AI-assisted drafting. Not endorsed by the Raspberry Pi Foundation. See [`NOTICE.md`](../NOTICE.md) and [`LICENSE`](../LICENSE).
