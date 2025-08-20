import tkinter as tk
from tkinter import messagebox
from ttkbootstrap import ttk, Style

class PomodoroTimer:
    def __init__(self):
        self.WORK_TIME = 25 * 60
        self.SHORT_BREAK_TIME = 5 * 60
        self.LONG_BREAK_TIME = 20 * 60

        self.root = tk.Tk()
        self.root.geometry("300x300")
        self.root.title("Pomodoro Timer")
        self.style = Style(theme="simplex")
        self.style.theme_use()

        self.timer_label = tk.Label(self.root, text="", font=("TkDefaultFont", 40))
        self.timer_label.pack(pady=20)

        self.start_button = ttk.Button(self.root, text="Start", command=self.start_timer)
        self.start_button.pack(pady=5)

        self.stop_button = ttk.Button(self.root, text="Stop", command=self.stop_timer, state=tk.DISABLED)
        self.stop_button.pack(pady=5)

        self.reset_button = ttk.Button(self.root, text="Reset", command=self.reset_timer)
        self.reset_button.pack(pady=5)

        self.config_button = ttk.Button(self.root, text="Config", command=self.open_config_window)
        self.config_button.pack(pady=5)

        self.cycle_label = tk.Label(self.root, text="Pomodoros Completed: 0", font=("TkDefaultFont", 14))
        self.cycle_label.pack(pady=10)

        self.reset_timer()
        self.root.mainloop()

    def start_timer(self):
        self.set_button_states(start=False, stop=True)
        self.is_running = True
        self.update_timer()

    def stop_timer(self):
        self.set_button_states(start=True, stop=False)
        self.is_running = False

    def reset_timer(self):
        self.is_running = False
        self.is_work_time = True
        self.work_time = self.WORK_TIME
        self.break_time = self.SHORT_BREAK_TIME
        self.pomodoros_completed = 0
        self.update_timer_label()
        self.set_button_states(start=True, stop=False)
        self.cycle_label.config(text="Pomodoros Completed: 0")

    def set_button_states(self, start, stop):
        self.start_button.config(state=tk.NORMAL if start else tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL if stop else tk.DISABLED)

    def open_config_window(self):
        config_window = tk.Toplevel(self.root)
        config_window.geometry("250x200")
        config_window.title("Configure Timer")

        tk.Label(config_window, text="Work Time (minutes):").pack(pady=5)
        self.work_entry = tk.Entry(config_window)
        self.work_entry.pack(pady=5)
        self.work_entry.insert(0, str(self.WORK_TIME // 60))

        tk.Label(config_window, text="Short Break Time (minutes):").pack(pady=5)
        self.short_break_entry = tk.Entry(config_window)
        self.short_break_entry.pack(pady=5)
        self.short_break_entry.insert(0, str(self.SHORT_BREAK_TIME // 60))

        tk.Label(config_window, text="Long Break Time (minutes):").pack(pady=5)
        self.long_break_entry = tk.Entry(config_window)
        self.long_break_entry.pack(pady=5)
        self.long_break_entry.insert(0, str(self.LONG_BREAK_TIME // 60))

        save_button = ttk.Button(config_window, text="Save", command=lambda: self.save_config(config_window))
        save_button.pack(pady=20)

    def save_config(self, window):
        try:
            self.WORK_TIME = int(self.work_entry.get()) * 60
            self.SHORT_BREAK_TIME = int(self.short_break_entry.get()) * 60
            self.LONG_BREAK_TIME = int(self.long_break_entry.get()) * 60
            self.reset_timer()
            messagebox.showinfo("Config Saved", "Timer settings have been updated.")
            window.destroy()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid integer values.")

    def update_timer(self):
        if self.is_running:
            if self.is_work_time:
                self.work_time -= 1
                if self.work_time == 0:
                    self.is_work_time = False
                    self.pomodoros_completed += 1
                    self.break_time = self.LONG_BREAK_TIME if self.pomodoros_completed % 4 == 0 else self.SHORT_BREAK_TIME
                    self.notify("Break Time!", "Take a long break and rest your mind." if self.pomodoros_completed % 4 == 0 else "Take a short break and stretch your legs!")
                    self.cycle_label.config(text=f"Pomodoros Completed: {self.pomodoros_completed}")
            else:
                self.break_time -= 1
                if self.break_time == 0:
                    self.is_work_time, self.work_time = True, self.WORK_TIME
                    self.notify("Work Time", "Get back to work!")

            self.update_timer_label()
            self.root.after(1000, self.update_timer)

    def update_timer_label(self):
        minutes, seconds = divmod(self.work_time if self.is_work_time else self.break_time, 60)
        self.timer_label.config(text="{:02d}:{:02d}".format(minutes, seconds))

    def notify(self, title, message):
        messagebox.showinfo(title, message)

if __name__ == "__main__":
    PomodoroTimer()