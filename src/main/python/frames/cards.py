import os

import PIL
import customtkinter as ctk
from PIL import Image

from src.main.python.frames.details import DetailsFilmFrame, DetailsPersonFrame


class CardFrame:
    def __init__(self, parent_frame, item, settings, row, column, size, title_attribute, image_path_method, details_frame_class):
        self.parent_frame = parent_frame
        self.item = item
        self.settings = settings
        self.row = row
        self.column = column
        self.size = size
        self.title_attribute = title_attribute
        self.image_path_method = image_path_method
        self.details_frame_class = details_frame_class
        self.initialize()

    def initialize(self):
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), self.image_path_method(self.item))
        try:
            image = ctk.CTkImage(Image.open(image_path), size=self.size)
        except PIL.UnidentifiedImageError:
            image = ctk.CTkImage(Image.new("RGB", self.size, "gray"), size=self.size)

        # Crear un botón
        button = ctk.CTkButton(self.parent_frame, text=getattr(self.item, self.title_attribute), image=image, command=self.show_detail_frame, compound="top")
        button.grid(row=self.row, column=self.column)


        

    def show_detail_frame(self):
        self.details_frame_class(self.item, self.settings)

class CardFilmFrame(CardFrame):
    def __init__(self, parent_frame, film, settings, row, column, size):
        super().__init__(parent_frame, film, settings, row, column, size, 'title', lambda film: film.get_path(), DetailsFilmFrame)

class CardPersonFrame(CardFrame):
    def __init__(self, parent_frame, person, settings, row, column, size):
        super().__init__(parent_frame, person, settings, row, column, size, 'name', lambda person: person.get_path(), DetailsPersonFrame)


