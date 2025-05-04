import tkinter as tk
import time
import threading
import os
import signal
from queue import Queue

WORK_DURATION = 20 * 60
# WORK_DURATION = 60  # 1 minute work for testing
BREAK_DURATION = 60
SKIP_PHRASE = "i dont care"


class EyeRest:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the main window
        self.queue = Queue()

    def show_break_screen(self):
        user_input = []

        def on_key(event):
            if event.char and event.char.isprintable():
                user_input.append(event.char)
                current_input = "".join(user_input[-len(SKIP_PHRASE):])
                if current_input.lower() == SKIP_PHRASE.lower():
                    screen.destroy()

        def update_countdown(remaining):
            """
            Updates the countdown label every second.
            Destroys the screen when countdown reaches zero.
            """
            minutes = remaining // 60
            seconds = remaining % 60
            countdown_label.config(text=f"{minutes:02}:{seconds:02}")
            if remaining > 0:
                screen.after(1000, update_countdown, remaining - 1)
            else:
                screen.destroy()

        # Create a new top-level window for the break screen        
        screen = tk.Toplevel(self.root)
        screen.configure(bg="black")
        screen.attributes("-fullscreen", True)
        screen.attributes("-topmost", True)

        # Disable escape key and set up key tracking
        screen.bind("<Escape>", lambda e: None)
        screen.bind("<Key>", on_key)

        # Central frame for layout
        center_frame = tk.Frame(screen, bg="black")
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Main reminder message
        label_main = tk.Label(
            center_frame,
            text="Stare somewhere far.",
            fg="white",
            bg="black",
            font=("Helvetica", 48, "bold")
        )
        label_main.pack(pady=(0, 20))

        # Sub-message
        label_sub = tk.Label(
            center_frame,
            text="Give rest to your eyes.",
            fg="white",
            bg="black",
            font=("Helvetica", 24)
        )
        label_sub.pack(pady=(0, 40))\
        
        # Countdown timer label
        countdown_label = tk.Label(
            center_frame,
            text="",
            fg="white",
            bg="black",
            font=("Helvetica", 36)
        )
        countdown_label.pack()

        update_countdown(BREAK_DURATION)

    def check_queue(self):
        """
        Periodically checks the message queue for a 'show_break' signal,
        and triggers the break screen when received.
        """
        try:
            while True:
                task = self.queue.get_nowait()
                if task == "show_break":
                    self.show_break_screen()
        except:
            pass
        self.root.after(100, self.check_queue)

    def timer_loop(self):
        """
        Background loop that waits for the work duration,
        then sends a message to trigger a break.
        """
        while True:
            time.sleep(WORK_DURATION)
            self.queue.put("show_break")

    def run(self):
        """
        Starts the timer thread and the Tkinter event loop.
        """
        timer_thread = threading.Thread(target=self.timer_loop)
        timer_thread.daemon = True # Automatically exit with the main thread
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
