#!/usr/bin/env python3
"""Run the unittest suite of every project folder in this repository.

Each project imports its own modules by bare name, so its tests must run with
that project folder as the working directory. Usage: python3 run_tests.py
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def project_dirs():
    """Return every directory that directly contains a test_*.py file."""
    return sorted({p.parent for p in ROOT.glob('*/test_*.py')})


def main():
    failures = []
    dirs = project_dirs()
    if not dirs:
        print('No test folders found.')
        return 1
    for directory in dirs:
        print(f'\n=== {directory.name} ===', flush=True)
        result = subprocess.run(
            [sys.executable, '-m', 'unittest', 'discover', '-v'], cwd=directory)
        if result.returncode != 0:
            failures.append(directory.name)
    print('\n=== Summary ===')
    for directory in dirs:
        status = 'FAIL' if directory.name in failures else 'ok'
        print(f'{status:4}  {directory.name}')
    return 1 if failures else 0


if __name__ == '__main__':
    sys.exit(main())
