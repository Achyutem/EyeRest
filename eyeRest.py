import tkinter as tk
import time
import threading
import os
import signal

WORK_DURATION = 20 * 60
BREAK_DURATION = 60
SKIP_PHRASE = "I dont care about my eyes"


def show_break_screen():
    user_input = []

    def on_key(event):
        if event.char and event.char.isprintable():
            user_input.append(event.char)
            if "".join(user_input[-len(SKIP_PHRASE) :]) == SKIP_PHRASE:
                screen.destroy()

    screen = tk.Tk()
    screen.configure(bg="black")
    screen.attributes("-fullscreen", True)
    screen.attributes("-topmost", True)

    screen.bind("<Escape>", lambda e: None)
    screen.bind("<Key>", on_key)

    label = tk.Label(
        screen,
        text="Stare somewhere far.",
        fg="white",
        bg="black",
        font=("Helvetica", 48),
    )
    label.pack(expand=True)

    # Auto-close after BREAK_DURATION
    screen.after(BREAK_DURATION * 1000, screen.destroy)

    screen.mainloop()


def timer_loop():
    while True:
        time.sleep(WORK_DURATION)
        show_break_screen()


if __name__ == "__main__":
    try:
        timer_thread = threading.Thread(target=timer_loop)
        timer_thread.daemon = True
        timer_thread.start()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting.")
        os.kill(os.getpid(), signal.SIGTERM)
