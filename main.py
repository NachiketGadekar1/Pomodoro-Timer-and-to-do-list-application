import tkinter as tk
from tkinter import messagebox
import time
import pygame

root = tk.Tk()
root.title("Pomodoro App")
root.geometry("350x400")

timer_running = False
break_running = False
start_time = 0
remaining_time = 0
elapsed_time = 0

focus_duration = 25
break_duration = 5

pygame.mixer.init()
timer_sound = r"C:\Users\Nachiket Gadekar\Documents\pomodoro project\Temple Bell-Sound.wav"


class Timer:
    def __init__(self, focus_duration, break_duration, root, timer_label, start_button, stop_button, start_break_button):
        self.focus_duration = focus_duration
        self.break_duration = break_duration
        self.root = root
        self.timer_label = timer_label
        self.start_button = start_button
        self.stop_button = stop_button
        self.start_break_button = start_break_button
        self.timer_running = False
        self.break_running = False
        self.start_time = 0
        self.elapsed_time = 0
        self.remaining_time = 0

    def start_timer(self):
        self.break_running = False
        if not self.timer_running:
            self.timer_running = True
            self.start_time = time.time()
            self.update_timer()
            self.start_button.config(state=tk.DISABLED)
            self.start_break_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)

    def stop_timer(self):
        self.timer_running = False
        self.start_button.config(state=tk.NORMAL)
        self.start_break_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def start_break(self):
        self.timer_running = False
        if not self.break_running:
            self.break_running = True
            self.start_time = time.time()
            self.update_timer()
            self.start_break_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.DISABLED)
            self.start_button.config(state=tk.NORMAL)

    def update_timer(self):
        if self.timer_running or self.break_running:
            self.elapsed_time = int(time.time() - self.start_time)
            if self.timer_running and not self.break_running:
                self.remaining_time = self.focus_duration - self.elapsed_time
                if self.remaining_time <= -1:
                    pygame.mixer.music.load(timer_sound)
                    pygame.mixer.music.play()
                    self.stop_timer()
                    return
            elif self.break_running and not self.timer_running:
                self.remaining_time = self.break_duration - self.elapsed_time
                if self.remaining_time <= -1:
                    pygame.mixer.music.load(timer_sound)
                    pygame.mixer.music.play()
                    self.stop_timer()
                    return
            mins, secs = divmod(self.remaining_time, 60)
            self.timer_label.config(text=f"{mins:02d}:{secs:02d}")
            # Schedule next update after 500 milliseconds
            self.root.after(500, self.update_timer)

    def update_focus_duration(self, new_focus_duration):
        # Update attribute
        self.focus_duration = new_focus_duration
        self.timer_running = False
        self.break_running = False
        self.start_time = 0
        self.elapsed_time = 0
        self.remaining_time = 0
        # Update timer label
        mins = self.focus_duration // 60
        secs = self.focus_duration % 60
        self.timer_label.config(text=f"{mins:02d}:{secs:02d}")
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.start_break_button.config(state=tk.DISABLED)


def open_settings():
    settings_window = tk.Toplevel(root)
    settings_window.title("Settings")
    settings_window.geometry("300x200")
    focus_label = tk.Label(settings_window, text="Focus Duration (in minutes):")
    focus_label.pack()
    focus_entry = tk.Entry(settings_window)
    focus_entry.pack()
    save_button = tk.Button(settings_window, text="Save Settings", command=lambda: save_settings(focus_entry.get()))
    save_button.pack()


def save_settings(focus_duration_input):
    global focus_duration
    try:
        focus_duration = int(focus_duration_input)
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numerical values for durations.")
        return
    if focus_duration <= 0:
        messagebox.showerror("Error", "Durations should be positive values.")
        return
    timer.update_focus_duration(focus_duration*60)


def add_task():
    task = task_entry.get()
    if task:
        task_listbox.insert(tk.END, task)  #
        task_entry.delete(0, tk.END)


# remove task from list
def remove_selected_task(event):
    selected_index = task_listbox.curselection()
    if selected_index:
        task_listbox.delete(selected_index)


root.configure(bg="#1a1625")
timer_label = tk.Label(root, bg="#76737e", fg="white", bd=2, relief=tk.GROOVE, text="25:00", font=("Helvetica", 50))
break_label = tk.Label(root, bg="#76737e", fg="white", text="5:00", font=("Helvetica", 50))
start_button = tk.Button(root, bg="#7a5af5", text="Start to focus", font=("Helvetica", 12),command=lambda: timer.start_timer())
stop_button = tk.Button(root, bg="#7a5af5", text="Pause", font=("Helvetica", 12), command=lambda: timer.stop_timer())
start_break_button = tk.Button(root, bg="#7a5af5", text="Start Break", font=("Helvetica", 12),
                               command=lambda: timer.start_break())
settings_button = tk.Button(root, text="Settings", font=("Helvetica", 10),bg="#7a5af5", command=open_settings)

task_entry = tk.Entry(root, font=("Helvetica", 12), width=25,bg="#76737e")
add_button = tk.Button(root, bg="#7a5af5", text="Add Task", font=("Helvetica", 12), command=add_task)
task_listbox = tk.Listbox(root, font=("Helvetica", 16), width=20, selectmode=tk.SINGLE,bg="#76737e")
# bind double click event to remove selected task
task_listbox.bind("<Double-Button-1>", remove_selected_task)

settings_button.pack(anchor="ne", padx=10, pady=10)
if break_running:
    break_label.pack(pady=10)
else:
    timer_label.pack(pady=10)
start_button.pack(pady=5)
stop_button.pack(pady=5)
start_break_button.pack(pady=5)
task_entry.pack(pady=5)
add_button.pack(pady=5)
task_listbox.pack(pady=5)

# timer object
timer = Timer(focus_duration*60, break_duration*60, root, timer_label, start_button, stop_button, start_break_button)

root.mainloop()
