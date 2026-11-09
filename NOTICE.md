# Notice: sources, licenses and AI assistance

**Different parts of this repository have different origins and different license status.** There is no single license for the whole repository.

## Summary

| Content | Origin | License status |
|---|---|---|
| Intro lessons 1 to 5 (`TechTopia_Industry_Challenge_Intro_Lessons_SenseHat/`) | Adapted from Raspberry Pi Foundation learning resources | **CC BY-SA 4.0** (see below) |
| Curriculum hub and team guides (`.../01_Curriculum_Websites/`, `.../03_Showcase_Team_Guides/`) | Adapted from Raspberry Pi Foundation learning resources | **CC BY-SA 4.0** (see below) |
| Quizzes (`.../02_Student_Assessment/`) | Generated with AI tools (ChatGPT, Claude), no reference material | **No license assigned yet** |
| Python projects (`sensehat_compass/`, `sensehat_maze_joystick/`, `sense_hat_arcade/`, `sense_hat_arcade 2/`) | Generated with AI tools (ChatGPT, Claude), no reference material | **No license assigned yet** |
| Documentation (`README.md`, `CONTRIBUTING.md`, `docs/`, `mkdocs.yml`, `run_tests.py`, `.github/`) | Written for this repository | **No license assigned yet** |

"No license assigned yet" means all rights are reserved by default: others may view the files on GitHub but have no granted right to copy or reuse them. See "Open decisions" below.

## Material adapted from the Raspberry Pi Foundation

The lessons, curriculum hub and team guides were adapted from these Raspberry Pi Foundation projects:

| Source | Source license | Used for |
|---|---|---|
| [Getting started with the Sense HAT](https://projects.raspberrypi.org/en/projects/getting-started-with-the-sense-hat) | CC BY-SA 4.0 (stated on the page, checked 2026-11-09) | Lesson 5 (Sense HAT Interactive Lab) |
| [Physical Computing with Python](https://projects.raspberrypi.org/en/projects/physical-computing) | CC BY-SA 4.0 (stated on the page, checked 2026-11-09) | Physical computing material (curriculum hub, team guides) |

The maintainer states that the lessons came from these sites. The mapping of individual files to individual source pages is not yet recorded; the table above lists the sources, not a file-by-file mapping. The full license text is in [`LICENSE-CC-BY-SA-4.0.txt`](LICENSE-CC-BY-SA-4.0.txt).

Attribution used on the adapted pages:

> Adapted from [Raspberry Pi Foundation](https://www.raspberrypi.org) learning resources, including Physical Computing with Python and Getting started with the Sense HAT, licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). Changes were made for the TechTopia classroom, including AI-assisted drafting. Not endorsed by the Raspberry Pi Foundation.

CC BY-SA 4.0 requires that anyone reusing the adapted files credit the Foundation, link to the license, indicate changes, and share their own adaptations under CC BY-SA 4.0 (or a compatible license).

## AI-generated material

The quizzes and the Python projects were generated with AI tools (ChatGPT and Claude) without reference material, and some drafting assistance was also used elsewhere. Copyright in purely AI-generated output is unsettled and varies by country, so ownership of those parts may be limited or absent. Because they are not derived from the Foundation's material, the CC BY-SA 4.0 share-alike condition does not apply to them.

## Open decisions

- **License for the quizzes, Python projects and documentation.** Options include MIT or Apache 2.0 for code and CC BY 4.0 for text, or CC0 if you want no restrictions. Until chosen, they remain all rights reserved. Who the copyright holder is (if anyone) is for the maintainer to decide.
- **File-to-source mapping** for the adapted lessons and guides, and confirmation that no other source was used. Earlier notes said some material was sourced from others. If any file came from a source other than those above, list it with its own license; it may not be compatible with CC BY-SA 4.0.
- **Embedded third-party code.** The HTML pages may contain Python examples from the Foundation's projects. Those fall under the same CC BY-SA 4.0 terms.

## Other third-party terms

- "Raspberry Pi", "Sense HAT" and "pi-top" are names and marks of their owners; use here does not imply endorsement.
- The `sense_hat` and `pitop` Python libraries, and any fonts or assets loaded by the HTML pages, are separate works with their own licenses.

## No warranty

The Python code has not been tested on physical hardware, and the `pitop` snippets have not been validated on a device. Everything is provided as is.
