import tkinter as tk
import time
import threading
import os
import signal
from queue import Queue

WORK_DURATION = 20 * 60
# WORK_DURATION = 10  # 10 seconds for testing
BREAK_DURATION = 60
SKIP_PHRASE = "i dont care"


class EyeRest:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the main window (optional)
        self.queue = Queue()

    def show_break_screen(self):
        user_input = []

        def on_key(event):
            if event.char and event.char.isprintable():
                user_input.append(event.char)
                current_input = "".join(user_input[-len(SKIP_PHRASE):])
                if current_input.lower() == SKIP_PHRASE.lower():
                    screen.destroy()

        screen = tk.Toplevel(self.root)
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

    def check_queue(self):
        try:
            while True:
                task = self.queue.get_nowait()
                if task == "show_break":
                    self.show_break_screen()
        except:
            pass
        self.root.after(100, self.check_queue)

    def timer_loop(self):
        while True:
            time.sleep(WORK_DURATION)
            self.queue.put("show_break")

    def run(self):
        timer_thread = threading.Thread(target=self.timer_loop)
        timer_thread.daemon = True
        timer_thread.start()

        self.check_queue()
        self.root.mainloop()


if __name__ == "__main__":
    try:
        app = EyeRest()
        app.run()
    except KeyboardInterrupt:
        print("Exiting.")
        os.kill(os.getpid(), signal.SIGTERM)
