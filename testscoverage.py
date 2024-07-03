#!/usr/bin/env python3
"""Custom scripts to run pytest and generate reports."""
import subprocess
import sys
import git
from cachorro import VERSION

readme_path = 'README.md'
coverage_path = 'TESTS.md'


def run_tests():
    """Set up and run pytest."""
    try:
        # Run pytest and generate a coverage report
        result = subprocess.run(
            ['pytest', '--cov=my_library', '--cov-report=term-missing'],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        passed = True
    except subprocess.CalledProcessError as e:
        result = e
        passed = False

    return result.stdout, passed


def update_readme(test_output, passed):
    """Update the README.md file, by changing the Test Coverage badge."""
    badge = "![Test Coverage](https://img.shields.io/badge/Tests-"
    badge_passed = 'PASSED-brightgreen' if passed else 'FAILED-red'
    badge_params = "?style=plastic&labelColor=blue"
    status_line = f"{badge}{badge_passed}{badge_params})\n"

    version_badge = "![Version](https://img.shields.io/badge/Version-"
    version_badge_params = f"{VERSION}-blue?style=plastic"
    version_line = f"{version_badge}{version_badge_params})\n"

    report_lines = f"# Tests Report\n\n```text\n{test_output}\n```\n"

    with open(readme_path, 'r') as file:
        lines = file.readlines()

    with open(readme_path, 'w') as file:
        for line in lines:
            if line.startswith(badge):
                file.write(status_line)
            elif line.startswith(version_badge):
                file.write(version_line)
            else:
                file.write(line)

    with open(coverage_path, 'w') as file:
        file.write(report_lines)


def stage_report_file():
    """Stage the report file for commit."""
    repo = git.Repo('.')
    repo.index.add([coverage_path])


if __name__ == '__main__':
    test_output, passed = run_tests()
    update_readme(test_output, passed)
    stage_report_file()

    # Exit with 0 to allow the commit to proceed
    sys.exit(0)
