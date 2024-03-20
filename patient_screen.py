import tkinter as tk
from tkinter import font as tkfont


class FullScreenTextDisplay:
    def __init__(self):
        self.root = tk.Tk()
        self.root.configure(bg='black')

        # Calculate window size and position (1/4 of the screen size)
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = screen_width // 2
        window_height = screen_height // 2
        position_right = screen_width // 4
        position_down = screen_height // 4

        # Set window size and position
        self.root.geometry(f"{window_width}x{window_height}+{position_right}+{position_down}")

        # Set up the text font and size
        self.text_font = tkfont.Font(size=25)
        self.label = tk.Label(self.root, font=self.text_font, fg='white', bg='black', wraplength=window_width,
                              justify="center")
        self.label.pack(expand=True)

        # Placeholder text, can be updated with any string
        self.update_text("Hello! :)")

    def update_text(self, text):
        self.label.config(text=text)
        self.label.update()

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    app = FullScreenTextDisplay()
    app.run()
else:
    # Create an instance to be used when imported elsewhere
    shared_display = FullScreenTextDisplay()