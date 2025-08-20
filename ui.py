# ui.py
import tkinter as tk
from tkinter import messagebox
from ttkbootstrap import ttk, Style

from timer import PomodoroTimer, PomodoroConfig, PomodoroState
import sounds
import os

SOUND_FILE = os.path.join("sounds", "alert.wav")

class PomodoroApp:
    def __init__(self):
        # ---- Window & theme ----
        self.root = tk.Tk()
        self.root.title("Pomodoro Timer")
        self.root.geometry("380x520")
        self.style = Style(theme="simplex")

        # ---- Timer core ----
        self.timer = PomodoroTimer(PomodoroConfig())

        # ---- Header / time ----
        self.timer_label = ttk.Label(self.root, text=self.timer.mm_ss(), font=("TkDefaultFont", 44), anchor="center")
        self.timer_label.pack(pady=16)

        self.phase_label = ttk.Label(self.root, text="Work", font=("TkDefaultFont", 14))
        self.phase_label.pack()

        # ---- Controls ----
        controls = ttk.Frame(self.root)
        controls.pack(pady=10)

        self.start_btn = ttk.Button(controls, text="Start", command=self.start)
        self.stop_btn = ttk.Button(controls, text="Stop", command=self.stop, state=tk.DISABLED)
        self.reset_btn = ttk.Button(controls, text="Reset", command=self.reset)

        self.start_btn.grid(row=0, column=0, padx=6)
        self.stop_btn.grid(row=0, column=1, padx=6)
        self.reset_btn.grid(row=0, column=2, padx=6)

        # ---- Progress / Stats ----
        self.progress = ttk.Progressbar(self.root, orient="horizontal", mode="determinate", length=320)
        self.progress.pack(pady=10)
        self.cycle_label = ttk.Label(self.root, text="Pomodoros Completed: 0")
        self.cycle_label.pack()

        # ---- Config button ----
        ttk.Button(self.root, text="Config", command=self.open_config_window).pack(pady=8)

        # ---- Task List ----
        self.build_tasks_ui(self.root)

        # ---- Loop ----
        self._after_id = None
        self.update_ui()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    # ---------- Task List ----------
    def build_tasks_ui(self, parent):
        wrapper = ttk.Labelframe(parent, text="Tasks")
        wrapper.pack(fill="both", expand=True, padx=12, pady=12)

        row1 = ttk.Frame(wrapper)
        row1.pack(fill="x", padx=8, pady=6)

        self.task_entry = ttk.Entry(row1)
        self.task_entry.pack(side="left", fill="x", expand=True)
        ttk.Button(row1, text="Add", command=self.add_task).pack(side="left", padx=6)

        # Treeview with two columns: Task, Status
        self.task_tree = ttk.Treeview(wrapper, columns=("task", "status"), show="headings", height=8)
        self.task_tree.heading("task", text="Task")
        self.task_tree.heading("status", text="Status")
        self.task_tree.column("task", width=220, anchor="w")
        self.task_tree.column("status", width=80, anchor="center")
        self.task_tree.pack(fill="both", expand=True, padx=8, pady=4)

        btns = ttk.Frame(wrapper)
        btns.pack(pady=6)
        ttk.Button(btns, text="Mark Done", command=self.mark_done).pack(side="left", padx=4)
        ttk.Button(btns, text="Remove", command=self.remove_task).pack(side="left", padx=4)
        ttk.Button(btns, text="Set as Current", command=self.set_current_task).pack(side="left", padx=4)

        self.current_task_label = ttk.Label(wrapper, text="Current: (none)")
        self.current_task_label.pack(pady=4)

    def add_task(self):
        text = self.task_entry.get().strip()
        if not text:
            return
        self.task_tree.insert("", "end", values=(text, "todo"))
        self.task_entry.delete(0, "end")

    def remove_task(self):
        for sel in self.task_tree.selection():
            self.task_tree.delete(sel)

    def mark_done(self):
        for sel in self.task_tree.selection():
            task, _ = self.task_tree.item(sel, "values")
            self.task_tree.item(sel, values=(task, "done"))

    def set_current_task(self):
        sel = self.task_tree.selection()
        if not sel:
            return
        task, status = self.task_tree.item(sel[0], "values")
        self.current_task_label.config(text=f"Current: {task}")

    # ---------- Timer controls ----------
    def start(self):
        self.timer.start()
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.tick()

    def stop(self):
        self.timer.stop()
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        if self._after_id:
            self.root.after_cancel(self._after_id)
            self._after_id = None

    def reset(self):
        was_running = self.timer.running
        self.timer.reset(full=not was_running)
        self.update_ui()
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)

    def open_config_window(self):
        w = tk.Toplevel(self.root)
        w.title("Configure Timer")
        w.geometry("280x260")

        def add_row(parent, label, default):
            ttk.Label(parent, text=label).pack(pady=(10, 4))
            e = ttk.Entry(parent, width=10)
            e.insert(0, str(default))
            e.pack()
            return e

        work_e = add_row(w, "Work (minutes):", self.timer.config.work_minutes)
        short_e = add_row(w, "Short Break (minutes):", self.timer.config.short_break_minutes)
        long_e = add_row(w, "Long Break (minutes):", self.timer.config.long_break_minutes)
        every_e = add_row(w, "Long Break Every N Pomodoros:", self.timer.config.long_break_every)

        def save():
            try:
                work = int(work_e.get())
                short = int(short_e.get())
                longb = int(long_e.get())
                every = int(every_e.get())
                self.timer.set_config(work, short, longb, every)
                self.update_ui()
                messagebox.showinfo("Saved", "Settings updated.")
                w.destroy()
            except ValueError:
                messagebox.showerror("Invalid", "Please enter valid integers.")

        ttk.Button(w, text="Save", command=save).pack(pady=14)

    # ---------- Loop & UI ----------
    def tick(self):
        event = self.timer.tick()
        if event == "work_complete_short":
            self.notify("Break Time!", "Take a short break and stretch your legs!")
            self.play_chime()
        elif event == "work_complete_long":
            self.notify("Long Break!", "Great job! Take a long break and recharge.")
            self.play_chime()
        elif event == "break_complete":
            self.notify("Work Time", "Back to focus—let’s go!")
            self.play_chime()

        self.update_ui()
        if self.timer.running:
            self._after_id = self.root.after(1000, self.tick)

    def update_ui(self):
        self.timer_label.config(text=self.timer.mm_ss())
        self.phase_label.config(text="Work" if self.timer.state == PomodoroState.WORK else "Break")
        # update progress bar (0..100)
        total = (self.timer.config.work_minutes if self.timer.state == PomodoroState.WORK
                 else (self.timer.config.long_break_minutes
                       if (self.timer.pomodoros_completed % self.timer.config.long_break_every == 0 and self.timer.state == PomodoroState.BREAK)
                       else self.timer.config.short_break_minutes)) * 60
        progressed = total - self.timer.remaining
        self.progress["maximum"] = total
        self.progress["value"] = max(progressed, 0)
        self.cycle_label.config(text=f"Pomodoros Completed: {self.timer.pomodoros_completed}")

    def play_chime(self):
        # try pygame sound; also do a UI bell as a lightweight fallback
        sounds.play_sound(SOUND_FILE)
        try:
            self.root.bell()
        except Exception:
            pass

    def notify(self, title, message):
        # simple modal; you could replace with system notifications later
        messagebox.showinfo(title, message)

    def on_close(self):
        self.stop()
        self.root.destroy()

def run_app():
    app = PomodoroApp()
    app.root.mainloop()
