import os
import tkinter as tk

import customtkinter as ctk
from PIL import Image

try:
    from src.main.python.frames.details.DetailsPersonFrame import DetailsPersonFrame
except ModuleNotFoundError:
    from frames.details.DetailsPersonFrame import DetailsPersonFrame


class CardPersonFrame:
    def __init__(self, parent_frame, person, row, column, size):
        self.parent_frame = parent_frame
        self.person = person
        self.row = row
        self.column = column
        self.size = size

    def initialize(self):
        name = ctk.CTkLabel(self.parent_frame, text=self.person.name, fg_color="gray30", corner_radius=6)
        name.grid(row=self.row, column=self.column)
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), self.person.image)
        image = ctk.CTkImage(Image.open(image_path), size=self.size)
        button = ctk.CTkButton(self.parent_frame, text="", image=image, command=lambda: self.show_detail_frame())
        button.grid(row=self.row+1, column=self.column)

    def show_detail_frame(self):
        self.details_window = tk.Toplevel(self.parent_frame)
        self.details_window.configure(bg="black")

        # Create an instance of DetailsFilmFrame with the film data and pack it into the new window
        self.detail_frame = DetailsPersonFrame(self.details_window, self.person)
        self.detail_frame.pack()

        # Set the title of the details window
        self.details_window.title(self.person.name)