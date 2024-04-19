import tkinter as tk
from tkinter import ttk


class Tab:
    def __init__(self, root: tk.Tk, notebook: ttk.Notebook):
        self.root = root
        self.notebook = notebook
        self.tab = None
        self.canvas = None

    def create_tab(self):
        tab = ttk.Frame(self.notebook)

        tab_canvas = tk.Canvas(tab)
        tab_canvas.pack(fill=tk.BOTH, expand=True)

        self.tab = tab
        self.canvas = tab_canvas

    def get_tab(self):
        return self.tab

    def get_canvas(self):
        return self.canvas
