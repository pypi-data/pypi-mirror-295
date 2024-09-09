import tkinter as tk

class Root(tk.Tk):
    def __init__(self):
        super().__init__()

        start_width = 750
        min_width = 400
        start_height = 750
        min_height = 400

        self.geometry(f"{start_width}x{start_height}")
        self.minsize(width=min_width, height=min_height)
        self.title("mayako GUI")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)