import os

import customtkinter as ctk
from PIL import Image


class ScrollableFilmsFrames(ctk.CTkFrame):
    def __init__(self, parent_frame, films, width=500, height=150, size=(100, 100), *args, **kwargs):
        super().__init__(parent_frame, *args, **kwargs)
        self.films = films
        self.width = width
        self.height = height
        self.size = size
        self.initialize()

    def initialize(self):
        scrollable_frame = ctk.CTkScrollableFrame(self, orientation="horizontal", width=self.width, height=self.height)
        scrollable_frame.grid(row=1, column=0, sticky="ew")

        for i, (title, image) in enumerate(self.films):
            title = ctk.CTkLabel(scrollable_frame, text=title, fg_color="gray30", corner_radius=6)
            title.grid(row=0, column=i)
            image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), image)
            button_with_image = ctk.CTkImage(Image.open(image_path), size=self.size)
            ###
            # TODO: Al pulsar debería de redirigir a detalles de la película.
            title = ctk.CTkLabel(scrollable_frame, text="", fg_color="gray30", corner_radius=6,
                                 image=button_with_image)
            title.grid(row=1, column=i)
            ###
