import tkinter as tk
from tkinter import messagebox
import time
import pygame

root = tk.Tk()
root.title("Pomodoro App")
root.geometry("430x550")

timer_running = False
break_running = False
start_time = 0
remaining_time = 0
elapsed_time = 0

focus_duration = 1500  # 25 minutes
break_duration = 300  # 5 minutes

pygame.mixer.init()
timer_sound = r"C:\Users\Nachiket Gadekar\Documents\pomodoro project\Temple Bell-Sound.wav"


def start_timer():
    global timer_running, start_time, break_running
    break_running = False
    if not timer_running:
        timer_running = True
        start_time = time.time()

        update_timer()
        start_button.config(state=tk.DISABLED)
        start_break_button.config(state=tk.DISABLED)
        stop_button.config(state=tk.NORMAL)


def stop_timer():
    global timer_running, start_time
    timer_running = not timer_running
    if timer_running == True:
        start_time = time.time() - elapsed_time

        update_timer()
        start_break_button.config(state=tk.DISABLED)
        stop_button.config(state=tk.NORMAL)
    else:
        start_button.config(state=tk.NORMAL)
        start_break_button.config(state=tk.NORMAL)


def start_break():
    global break_running, start_time, break_duration, remaining_time, timer_running
    timer_running = False
    if not break_running:
        break_running = True
        start_time = time.time()

        update_timer()
        start_break_button.config(state=tk.DISABLED)
        stop_button.config(state=tk.DISABLED)
        start_button.config(state=tk.NORMAL)


def update_timer():
    global timer_running, start_time, break_running, elapsed_time, remaining_time
    if timer_running or break_running:
        elapsed_time = int(time.time() - start_time)
        if timer_running == True and break_running == False:
            remaining_time = focus_duration - elapsed_time
            if remaining_time <= -1:
                pygame.mixer.music.load(timer_sound)
                pygame.mixer.music.play()
                stop_timer()
                return
        elif break_running == True and timer_running == False:
            remaining_time = break_duration - elapsed_time
            if remaining_time <= -1:
                pygame.mixer.music.load(timer_sound)
                pygame.mixer.music.play()
                stop_timer()
                return
        mins, secs = divmod(remaining_time, 60)
        timer_label.config(text=f"{mins:02d}:{secs:02d}")

        # Schedule next update after 1000 milliseconds
        root.after(1000, update_timer)


def open_settings():
    settings_window = tk.Toplevel(root)
    settings_window.title("Settings")
    settings_window.geometry("300x200")

    focus_label = tk.Label(settings_window, text="Focus Duration (seconds):")
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


# add task to-do list
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


root.configure(bg="#DBF6FA")
timer_label = tk.Label(root, bg="#D8F3F6", fg="black", bd=2, relief=tk.GROOVE, text="25:00", font=("Helvetica", 72))
break_label = tk.Label(root, bg="#D8F3F6", fg="white", text="5:00", font=("Helvetica", 72))
start_button = tk.Button(root, bg="#E66C41", fg="white", text="Start to focus", font=("Helvetica", 16),
                         command=start_timer)
stop_button = tk.Button(root, bg="#E66C41", fg="white", text="Pause", font=("Helvetica", 16), command=stop_timer)
start_break_button = tk.Button(root, bg="#E66C41", fg="white", text="Start Break", font=("Helvetica", 16),
                               command=start_break)
settings_button = tk.Button(root, text="Settings", font=("Helvetica", 10), command=open_settings)

task_entry = tk.Entry(root, font=("Helvetica", 16), width=30)
add_button = tk.Button(root, bg="#E66C41", fg="white", text="Add Task", font=("Helvetica", 16), command=add_task)
task_listbox = tk.Listbox(root, font=("Helvetica", 16), width=20, selectmode=tk.SINGLE)
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

root.mainloop()
