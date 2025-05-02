import tkinter as tk
import time
import threading
import os
import signal

WORK_DURATION = 20 * 60
BREAK_DURATION = 20
SKIP_PHRASE = "i dont care"

def show_break_screen():
    user_input = []

    def on_key(event):
        if event.char and event.char.isprintable():
            user_input.append(event.char)
            current_input = "".join(user_input[-len(SKIP_PHRASE):])
            if current_input.lower() == SKIP_PHRASE.lower():
                screen.destroy()

    screen = tk.Tk()
    screen.configure(bg="black")
    screen.attributes("-fullscreen", True)
    screen.attributes("-topmost", True)

    screen.bind("<Escape>", lambda e: None)
    screen.bind("<Key>", on_key)

    # Create a centered frame
    center_frame = tk.Frame(screen, bg="black")
    center_frame.place(relx=0.5, rely=0.5, anchor="center")

    # Large headline
    label_main = tk.Label(
        center_frame,
        text="Stare somewhere far.",
        fg="white",
        bg="black",
        font=("Helvetica", 48, "bold")
    )
    label_main.pack(pady=(0, 20))  # Space between lines

    # Smaller subtitle
    label_sub = tk.Label(
        center_frame,
        text="Give rest to your eyes.",
        fg="white",
        bg="black",
        font=("Helvetica", 24)
    )
    label_sub.pack()

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
