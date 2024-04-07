import os
import tkinter as tk

import customtkinter as ctk
from PIL import Image

try:
    from src.main.python.frames.details.DetailsFilmFrame import DetailsFilmFrame
except ModuleNotFoundError:
    from frames.details.DetailsFilmFrame import DetailsFilmFrame


class CardFilmFrame:
    def __init__(self, parent_frame, film , row, column, size):
        self.parent_frame = parent_frame
        self.film = film
        self.row = row
        self.column = column
        self.size = size
        self.initialize()

    def initialize(self):
        name = ctk.CTkLabel(self.parent_frame, text=self.film.title, fg_color="gray30", corner_radius=6)
        name.grid(row=self.row, column=self.column)
        image = ctk.CTkImage(Image.open(self.film.get_path()), size=self.size)
        button = ctk.CTkButton(self.parent_frame, text="", image=image, command=lambda: self.show_detail_frame())
        button.grid(row=self.row + 1, column=self.column)

    def show_detail_frame(self):
        self.details_window = tk.Toplevel(self.parent_frame)
        self.details_window.configure(bg="black")

        # Create an instance of DetailsFilmFrame with the film data and pack it into the new window
        self.detail_frame = DetailsFilmFrame(self.details_window, self.film)
        self.detail_frame.pack()

        # Set the title of the details window
        self.details_window.title(self.film.title)