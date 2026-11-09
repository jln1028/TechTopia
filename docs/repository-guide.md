# Repository guide

An analysis of how the TechTopia repository is organised today, a proposed structure, and recommendations for onboarding and for a future documentation site.

## 1. Current structure

| Folder | Purpose | Format | Hardware / SDK |
|---|---|---|---|
| `TechTopia_Industry_Challenge_Intro_Lessons_SenseHat/` | Five numbered interactive lessons: pi-top [4] basics, terminal, terminal treasure hunt, Python, Sense HAT lab | 5 self-contained HTML pages | pi-top [4]; `sense_hat` (lesson 5) |
| `TechTopia_Industry_Challenge_Physical_Computing_Materials/` | Curriculum hub, assessments, and team build guides for the showcase | 6 HTML pages in 3 subfolders, plus `README.txt` | `pitop` SDK |
| `sensehat_compass/` | Interactive compass (arrow, cardinal, numeric) | Python + `unittest` | Sense HAT |
| `sensehat_maze_joystick/` | Marble maze, joystick or tilt | Python + `unittest` | Sense HAT |
| `sense_hat_arcade/` | 3-game arcade, difficulty levels, persistent high scores | Python + `unittest` | Sense HAT |
| `sense_hat_arcade 2/` | 6-game arcade, countdown, session-only best scores | Python + `unittest` | Sense HAT |

### What each group of materials contains

- **Intro lessons:** `1-using-your-pitop4`, `2-intro-to-terminal-pitop4`, `3-pacman-terminal-treasure-hunt-pitop4`, `4-intro-to-python`, `5-sense-hat-interactive-lab`.
- **Challenge materials:**
  - `01_Curriculum_Websites/TechTopia_Physical_Computing_Hub.html`: concepts, project library, naming guide, coding constructs, glossary, teacher note.
  - `02_Student_Assessment/`: `TechTopia_20_Question_Quiz.html`, `TechTopia_sense_hat_quiz.html`.
  - `03_Showcase_Team_Guides/`: Team 1 Smart Security System, Team 2 Reaction Challenge, Team 3 Smart Crosswalk. Each has a wiring guide, team roles, build checklist, build steps, finished code and presentation reminders.

## 2. Logical groupings

By **use case**:

| Group | Members | Audience |
|---|---|---|
| A. Foundations (learn) | Intro lessons 1 to 4 | Students, no prior experience |
| B. Sense HAT track (learn, then build) | Lesson 5, quiz `TechTopia_sense_hat_quiz`, the four Python projects | Students and teachers |
| C. pi-top component track (build for the showcase) | Physical Computing Hub, team guides 1 to 3, 20-question quiz | Teams and teachers |

By **technology**:

| Technology | Members |
|---|---|
| `pitop` SDK (Foundation/Expansion Plate) | Hub, team guides, 20-question quiz, lesson 1 (miniscreen) |
| `sense_hat` | Lesson 5, Sense HAT quiz, all four Python projects |
| Terminal / generic Python | Lessons 2 to 4 |

By **maturity**:

| Maturity | Members |
|---|---|
| Automated tests (off-device) | Four Python projects |
| Hardware-verified | None documented. This is stated in the compass, arcade and materials READMEs |

## 3. Observed issues affecting discoverability

1. **Long, inconsistent folder names.** `TechTopia_Industry_Challenge_...` repeats in both HTML folders; the Python folders use three different naming patterns (`sensehat_*`, `sense_hat_arcade`, `sense_hat_arcade 2`).
2. **A folder name with a space** (`sense_hat_arcade 2`) breaks shell commands unless quoted.
3. **Ambiguous names.** `sense_hat_arcade 2` is not a "version 2" of `sense_hat_arcade`; it is a separate codebase with different games and score handling. `arcade.py` is the hardware runner in one and pure game logic in the other.
4. **Two hardware tracks are not distinguished** (`pitop` vs `sense_hat`) in folder names.
5. **No entry page for the HTML content.** Pages are not linked to each other, and the only guide to them is `README.txt`.
6. **Mixed documentation formats.** READMEs are `.md` except `README.txt` in the materials folder.
7. **No shared contributor guidance** and no automated way to run all tests at once.

## 4. Proposed structure

This is a proposal only; no folders have been moved. Moving folders breaks links in the READMEs and in any existing bookmarks, so do it in a single commit with `git mv` and update links at the same time.

```text
TechTopia/
├── README.md
├── CONTRIBUTING.md
├── docs/                          # documentation site source (see section 6)
│   ├── index.md
│   ├── getting-started.md
│   ├── repository-guide.md
│   └── hardware-notes.md
├── lessons/                       # Group A + lesson 5
│   ├── index.html
│   ├── 1-using-your-pitop4.html
│   ├── 2-intro-to-terminal-pitop4.html
│   ├── 3-pacman-terminal-treasure-hunt-pitop4.html
│   ├── 4-intro-to-python.html
│   └── 5-sense-hat-interactive-lab.html
├── challenge/                     # Group C
│   ├── README.md                  # converted from README.txt
│   ├── curriculum/
│   ├── assessment/
│   └── team-guides/
└── sensehat-projects/             # Group B
    ├── README.md                  # table of projects + shared conventions
    ├── compass/
    ├── maze/
    ├── arcade-classic/            # was sense_hat_arcade
    └── arcade-enhanced/           # was "sense_hat_arcade 2"
```

Rationale:

- Top-level names say **what the content is for** (learn, challenge, build) instead of repeating the programme name.
- No spaces in any folder name.
- `arcade-classic` / `arcade-enhanced` states the relationship that the current names hide.
- Each group gets its own index page, so no part of the repo is more than two clicks from the root README.

Lower-effort alternative (no moves): keep all folders and apply only the documentation changes in sections 5 to 7. The root README already routes by audience, which removes most of the confusion.

## 5. Onboarding recommendations

**New student or teacher**

- Open the root README and use the "Where do I start?" table.
- Add a one-page **Teacher quick start**: required hardware per track, expected time per lesson, which quiz follows which lesson, and a pre-class checklist (the materials README already warns that SDK component names and port numbers must be validated on the device).

**New contributor**

- Follow [CONTRIBUTING.md](https://github.com/jln1028/TechTopia/blob/main/CONTRIBUTING.md): clone, run the tests, read the conventions, check the pre-commit list.
- Added: `run_tests.py` at the root runs every project's tests (running `unittest discover` from the root finds none), and `.github/workflows/tests.yml` runs it in CI.
- Still open:
  - Licensing for the quizzes, Python projects and docs: not assigned yet (see `NOTICE.md`). The adapted lessons and guides are CC BY-SA 4.0.
  - Issue templates for "hardware test report" and "lesson content error".

**Hardware testers**

- Create `docs/hardware-notes.md` with a table: project, device, OS version, date, result, issues. All READMEs say the code has not been verified on a physical Sense HAT.

## 6. Documentation site recommendations

A first MkDocs site is now scaffolded (`mkdocs.yml`, `docs/*.md`, `.github/workflows/docs.yml`). MkDocs with the Material theme suits this repo: Markdown source, built-in search, and static output hosted on GitHub Pages alongside the existing HTML. The workflow copies the two HTML folders into the built site so the links from `docs/` resolve.

The navigation below is the longer-term target; the current `mkdocs.yml` is a shorter version of it:

```yaml
site_name: TechTopia
nav:
  - Home: index.md
  - Getting started:
      - Teacher quick start: getting-started.md
      - Contributor setup: contributing.md
  - Learn:
      - Intro lessons: lessons.md
  - Challenge:
      - Overview: challenge.md
      - Team guides: team-guides.md
  - Sense HAT projects:
      - Overview: projects/index.md
      - Compass: projects/compass.md
      - Maze: projects/maze.md
      - Classic arcade: projects/arcade-classic.md
      - Enhanced arcade: projects/arcade-enhanced.md
  - Reference:
      - Repository guide: repository-guide.md
      - Hardware notes: hardware-notes.md
```

Information-architecture recommendations:

1. **Organise by task, not by folder.** Learn, build, assess and contribute are the questions visitors ask.
2. **One page per project**, using the same headings as the current READMEs: what it does, controls, run tests, run on a Pi, limitations. Reuse the existing content.
3. **Link to the HTML pages** from the site (copy them under `docs/` as static assets, or link to the GitHub Pages path) and add a back link to the site from each page.
4. **Add an `index.html`** in the lessons and challenge folders that lists the pages in order, so students are not browsing files.
5. **State the SDK on every page** (`pitop` or `sense_hat`) in a consistent banner, because the two are not interchangeable.
6. **Add a "last verified on hardware" line** to each project page, empty until tested.
7. **Convert `README.txt` to `README.md`** so formatting and links render on GitHub.

## 7. Suggested order of work

1. Root README with audience routing and learning path (done).
2. `CONTRIBUTING.md` (done).
3. Root test script and CI (done: `run_tests.py`, `.github/workflows/tests.yml`).
4. `index.html` pages for the lessons and challenge folders (done).
5. MkDocs site scaffold and Pages workflow (done; enable GitHub Pages with source "GitHub Actions" in the repository settings).
6. Licence for the quizzes, Python projects and docs (open: needs the owner's choice; lessons and guides are CC BY-SA 4.0, see `NOTICE.md`).
7. Rename and move folders per section 4, in one commit with `git mv`, then update links in the READMEs, `docs/` and `index.html` pages (open: deliberately not done, because it breaks existing links and bookmarks).
