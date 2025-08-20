# timer.py
from dataclasses import dataclass

@dataclass
class PomodoroConfig:
    work_minutes: int = 25
    short_break_minutes: int = 5
    long_break_minutes: int = 20
    long_break_every: int = 4  # after N pomodoros, take a long break

class PomodoroState:
    WORK = "work"
    BREAK = "break"

class PomodoroTimer:
    def __init__(self, config: PomodoroConfig | None = None):
        self.config = config or PomodoroConfig()
        self.reset(full=True)

    def reset(self, full: bool = False):
        self.state = PomodoroState.WORK
        self.remaining = self.config.work_minutes * 60
        if full:
            self.pomodoros_completed = 0
        self.running = False

    def set_config(self, work: int, short_break: int, long_break: int, long_break_every: int | None = None):
        self.config.work_minutes = work
        self.config.short_break_minutes = short_break
        self.config.long_break_minutes = long_break
        if long_break_every:
            self.config.long_break_every = long_break_every
        # If not running, reflect new config immediately
        if not self.running:
            self.reset(full=False)

    def start(self):
        self.running = True

    def stop(self):
        self.running = False

    def tick(self):
        """Call once per second from the UI. Returns an event string when a phase ends."""
        if not self.running:
            return None
        if self.remaining > 0:
            self.remaining -= 1
            return None

        # Phase just ended
        if self.state == PomodoroState.WORK:
            self.pomodoros_completed += 1
            self.state = PomodoroState.BREAK
            # Decide long or short break
            long_break = (self.pomodoros_completed % self.config.long_break_every == 0)
            self.remaining = (self.config.long_break_minutes if long_break else self.config.short_break_minutes) * 60
            return "work_complete_long" if long_break else "work_complete_short"
        else:
            self.state = PomodoroState.WORK
            self.remaining = self.config.work_minutes * 60
            return "break_complete"

    def mm_ss(self):
        m, s = divmod(max(self.remaining, 0), 60)
        return f"{m:02d}:{s:02d}"
