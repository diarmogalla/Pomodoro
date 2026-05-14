# Codebase Scope: Pomodoro Timer

## Overview

A desktop Pomodoro timer application with configurable work and break intervals, task management, progress display, and optional sound notifications. Built with Python, Tkinter, and ttkbootstrap, it runs locally via a simple GUI.

## Main Features

- Configurable work, short break, and long break intervals
- Start / Stop / Reset timer controls
- Automatic long break after a configurable number of pomodoros
- Task list UI with add, remove, mark done, and set current task
- Progress bar reflecting current phase progress
- Config window to adjust timer settings
- Optional sound/chime notifications using pygame
- Themed UI using ttkbootstrap

## Entry Points

| Path | Description |
| --- | --- |
| main.py | Application entry point that imports and runs the UI via run_app() |
| run.sh | Shell script that installs required Python packages and launches the application |

## Key Modules

| Path | Responsibility |
| --- | --- |
| ui.py | Defines the graphical user interface, integrates timer logic, handles user interactions, task management, configuration UI, and sound playback |
| timer.py | Core Pomodoro timer logic, state management, configuration handling, and time calculations |
| pomodoro.py | Legacy/alternative implementation of the timer UI; not referenced by the main entry point but provides similar functionality |
| sounds.py | Utility for playing alert sound files using pygame, with graceful fallback when pygame is unavailable |

## External Dependencies

| Dependency | Purpose |
| --- | --- |
| ttkbootstrap | Provides themed Tkinter widgets and styling for the GUI |
| pygame | Enables playback of alert sound files for timer notifications |
| tkinter | Standard Python GUI toolkit used for window and widget creation |

## Runtime / Deployment

Runs as a local desktop application on any OS with Python 3.8+; launched via the run.sh script or directly with python main.py, using Tkinter's event loop for the GUI.

## Documentation Gaps

- No detailed usage guide beyond the brief README
- Missing docstrings and inline documentation for classes and functions
- No unit tests or CI configuration included
- No packaging or distribution scripts (e.g., setup.py, pyproject.toml)
- Sound file (alert.wav) is referenced but not included in the repository
- pomodoro.py appears unused and duplicates functionality provided by ui.py
- No persistence mechanism for tasks or user settings
- No instructions for cross‑platform packaging (e.g., executable bundles)
