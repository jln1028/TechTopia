# Sense HAT Interactive Compass

Three joystick-controlled modes: directional arrow, cardinal text, and three-digit heading.

## Run on Raspberry Pi

1. Connect the Sense HAT to a compatible Raspberry Pi with power off.
2. Install the official package: `sudo apt update && sudo apt install sense-hat python3-sense-hat` (on some Raspberry Pi OS versions the `sense-hat` package is sufficient).
3. In this folder, run `python3 -m unittest -v test_compass`.
4. Run `python3 compass_app.py`.
5. Press joystick up, center or right for next mode; down or left for previous. Press Ctrl+C to quit.

## Modes

- **Arrow**: 8-way arrow represents compass heading: north=top, east=right, south=bottom, west=left. This is a *heading indicator*, not a north-seeking needle. Hold the board level, with its LED display facing up, and use the same edge as the reference orientation.
- **Cardinal**: displays N/NE/E/SE/S/SW/W/NW, cycling letters where necessary.
- **Numeric**: displays the three heading digits in sequence, e.g. 090 for 90 degrees. The degree sign is omitted on the 8x8 display.

## Red / Green tests

The initial RED run failed because `compass_core` had not been implemented (`red_results.txt`). After implementation the GREEN run passed (`green_results.txt`). Tests cover direction boundaries, arrow positions, pixel validity, heading wraparound and joystick mode cycling. The code was not tested against a physical Sense HAT; verify sensor and joystick operation on your device.

## Notes

The `sense.get_compass()` API returns a heading in degrees based on the Sense HAT's sensors. Nearby metal or electronics can distort readings; test away from magnets and verify directions against a known compass. The program does not apply geographic declination and reports magnetic, not true, north. `show_letter` is used instead of blocking scrolling text so joystick presses remain responsive.
