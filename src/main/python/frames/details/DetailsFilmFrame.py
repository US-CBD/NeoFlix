from tkinter.messagebox import showinfo

import customtkinter as ctk
from PIL import Image


class DetailsFilmFrame(ctk.CTkFrame):
    def __init__(self, parent, film, settings, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.film = film
        self.settings = settings
        self.initialize()

    def initialize(self):
        self.parent.geometry("800x600")
        self.parent.resizable(False, False)
        self.parent.pack_propagate(True)

        self.image_frame = ctk.CTkFrame(self)
        self.image_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        self.details_frame = ctk.CTkFrame(self)
        self.details_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.configure_widgets()

    def configure_widgets(self):
        self.configure_image()
        self.configure_details()

    def configure_image(self):
        pil_image = Image.open(self.film.get_path())
        ctk_image = ctk.CTkImage(pil_image, size=(200, 400))
        image_label = ctk.CTkLabel(self.image_frame, text="", image=ctk_image, width=200, height=400, corner_radius=6)
        image_label.pack(fill="both", expand=True)

    def configure_details(self):
        self.add_label(self.details_frame, text=self.film.title, row=0, column=0, sticky="w", fg_color="gray30", corner_radius=9)
        self.add_label(self.details_frame, text=self.film.vote_average, row=0, column=1, sticky="w", fg_color=self.get_color(self.film.vote_average), text_color="black")
        if len(self.film.get_genres()) >= 1:
            self.add_label(self.details_frame, text="Genres: ", row=1, column=0, sticky="w", fg_color="gray")
            self.add_scrollable_frame_with_buttons(self.details_frame, self.film.get_genres(), row=2, column=0)
        if len(self.film.get_directors()) >= 1:
            self.add_label(self.details_frame, text="Directors: ", row=3, column=0, sticky="w", fg_color="gray")
            self.add_scrollable_frame_with_buttons(self.details_frame, [director.name for director in self.film.get_directors()], row=4, column=0)
        if len(self.film.get_actors()) >= 1:
            self.add_label(self.details_frame, text="Actors: ", row=5, column=0, sticky="w", fg_color="gray")
            self.add_scrollable_frame_with_buttons(self.details_frame, [actor.name for actor in self.film.get_actors()], row=6, column=0)
        self.add_label(self.details_frame, text="Description: ", row=7, column=0, sticky="w", fg_color="gray")
        self.add_textbox(self.details_frame, text=self.film.description, row=8, column=0, rowspan=2)

        # Add favorite button
        favorite_button = ctk.CTkButton(self.details_frame, text="Favorite", fg_color="gray", command=self.mark_as_favorite)
        favorite_button.grid(row=10, column=0, sticky="w", pady=(10, 0))

    def add_label(self, parent, text, row, column, sticky, fg_color=None, text_color=None, corner_radius=None):
        label = ctk.CTkLabel(parent, text=text, fg_color=fg_color, text_color=text_color, corner_radius=corner_radius)
        label.grid(row=row, column=column, sticky=sticky, padx=5, pady=5)

    def add_scrollable_frame_with_buttons(self, parent, items, row, column):
        scrollable_frame = ctk.CTkScrollableFrame(parent, orientation="horizontal", width=200, height=30)
        scrollable_frame.grid(row=row, column=column, sticky="w", columnspan=2)
        for i, item in enumerate(items):
            button = ctk.CTkButton(scrollable_frame, text=item, command=lambda: ())
            button.grid(row=row, column=i, sticky="w", padx=2, pady=2)

    def add_textbox(self, parent, text, row, column, rowspan):
        textbox = ctk.CTkTextbox(parent, fg_color="gray", corner_radius=6)
        textbox.insert("1.0", text)
        textbox.grid(row=row, column=column, columnspan=2, rowspan=rowspan, sticky="w", padx=5, pady=5)

    def get_color(self, rating):
        if rating >= 7.5:
            return "green"
        elif rating >= 5:
            return "yellow"
        else:
            return "red"

    def mark_as_favorite(self):
        if self.settings.user.state_film(self.film):
            self.settings.user.remove_film(self.film)
            showinfo("Success", f"{self.film.title} removed from favorites")
        else:
            self.settings.user.add_film(self.film)
            showinfo("Success", f"{self.film.title} added to favorites")




