import tkinter.messagebox as tkmessagebox

import PIL
import customtkinter as ctk
from PIL import Image

from src.main.python.frames.review_frame import ReviewFrame


class DetailFrame:
    def __init__(self, item, settings):
        self.root = ctk.CTkToplevel()
        self.item = item
        self.settings = settings
        self.initialize()
        self.root.mainloop()

    def initialize(self):
        self.root.title(self.item.name if hasattr(self.item, 'name') else self.item.title)
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        self.root.configure(bg="black")

        self.image_frame = ctk.CTkFrame(self.root)
        self.image_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        self.details_frame = ctk.CTkScrollableFrame(self.root, orientation="vertical", width=1200, height=1400)
        self.details_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.configure_widgets()

    def configure_widgets(self):
        self.configure_image()
        self.configure_details()

    def configure_image(self):
        try:
            pil_image = Image.open(self.item.get_path())
        except PIL.UnidentifiedImageError:
            pil_image = Image.new("RGB", (200, 400), "gray")

        ctk_image = ctk.CTkImage(pil_image, size=(200, 400))
        image_label = ctk.CTkLabel(self.image_frame, text="", image=ctk_image, width=200, height=400, corner_radius=6)
        image_label.pack(fill="both", expand=True)

    def configure_details(self):
        pass  # Esta función será implementada en las subclases

    def add_label(self, parent, text, row, column, sticky, fg_color=None, text_color=None, corner_radius=None,
                  font=None, cursor=None):
        label = ctk.CTkLabel(parent, text=text or "Not available", fg_color=fg_color, text_color=text_color,
                             corner_radius=corner_radius, font=font, cursor=cursor)
        label.grid(row=row, column=column, sticky=sticky, padx=5, pady=5)
        return label

    def add_textbox(self, parent, text, row, column, rowspan):
        textbox = ctk.CTkTextbox(parent, fg_color="gray", corner_radius=6, width=400)
        textbox.insert("1.0", text or "Not available")
        textbox.grid(row=row, column=column, columnspan=2, rowspan=rowspan, sticky="w", padx=5, pady=5)


class DetailsFilmFrame(DetailFrame):
    def configure_details(self):
        title_frame = ctk.CTkFrame(self.details_frame)
        title_frame.grid(row=0, column=0, sticky="w")

        self.title_label = self.add_label(title_frame, text=self.item.title, row=0, column=0, sticky="w",
                                          fg_color="gray30", corner_radius=9, font=("Helvetica", 24, "bold"),
                                          cursor="hand1")
        self.title_label.bind("<Button-1>", self.mark_as_favorite)
        self.update_favorite_button_text()

        self.add_label(self.details_frame, text=self.item.vote_average, row=0, column=1, sticky="w",
                       fg_color=self.get_color(self.item.vote_average), text_color="black", corner_radius=10,
                       font=("Helvetica", 12, "bold"))
        if len(self.item.get_genres()) >= 1:
            self.add_label(self.details_frame, text="Genres: ", row=1, column=0, sticky="w", fg_color="gray",
                           corner_radius=6, font=("Helvetica", 16, "bold"))
            self.add_scrollable_frame_with_buttons(self.details_frame, self.item.get_genres(), row=2, column=0)
        if len(self.item.get_directors()) >= 1:
            self.add_label(self.details_frame, text="Directors: ", row=3, column=0, sticky="w", fg_color="gray",
                           corner_radius=6, font=("Helvetica", 16, "bold"))
            self.add_scrollable_frame_with_buttons_for_persons(self.details_frame,
                                                               self.item.get_directors(), row=4,
                                                               column=0)
        if len(self.item.get_actors()) >= 1:
            self.add_label(self.details_frame, text="Actors: ", row=5, column=0, sticky="w", fg_color="gray",
                           corner_radius=6, font=("Helvetica", 16, "bold"))
            self.add_scrollable_frame_with_buttons_for_persons(self.details_frame, self.item.get_actors(),
                                                               row=6, column=0)
        self.add_label(self.details_frame, text="Description: ", row=7, column=0, sticky="w", fg_color="gray",
                       corner_radius=6, font=("Helvetica", 16, "bold"))
        self.add_textbox(self.details_frame, text=self.item.description, row=8, column=0, rowspan=2)

        self.opinion_buttom = ctk.CTkButton(self.details_frame, text="👍 Give your opinion", fg_color="gray",
                                            command=self.open_opinion_frame)
        self.opinion_buttom.grid(row=10, column=0, sticky="w", pady=(10, 0))

        if len(self.item.get_opinions()) >= 1:

            self.add_label(self.details_frame, text="Opinions: ", row=11, column=0, sticky="w", fg_color="gray")
            for i, opinion in enumerate(self.item.get_opinions()):
                self.add_label(self.details_frame, text=str(opinion), row=12 + i, column=0, sticky="w", fg_color="gray")

    def add_scrollable_frame_with_buttons(self, parent, items, row, column):
        scrollable_frame = ctk.CTkScrollableFrame(parent, orientation="horizontal", width=500, height=30)
        scrollable_frame.grid(row=row, column=column, sticky="w", columnspan=2)
        for i, item in enumerate(items):
            button = ctk.CTkButton(scrollable_frame, text=item, command=lambda: ())
            button.grid(row=row, column=i, sticky="w", padx=2, pady=2)

    def open_opinion_frame(self):
        ReviewFrame(self.item, self.settings)

    def get_color(self, rating):
        if rating >= 7.5:
            return "green"
        elif rating >= 5:
            return "yellow"
        else:
            return "red"

    def mark_as_favorite(self, event):
        if self.settings.user.state_film(self.item):
            self.settings.user.remove_favorite_film(self.item)
            tkmessagebox.showinfo("Success", f"{self.item.title} removed from favorites")
        else:
            self.settings.user.add_favorite_film(self.item)
            tkmessagebox.showinfo("Success", f"{self.item.title} added to favorites")
        self.settings.update_favourites = True
        self.update_favorite_button_text()

    def update_favorite_button_text(self):
        if self.settings.user.state_film(self.item):
            self.title_label.configure(text=f"{self.item.title} ⭐️")
        else:
            self.title_label.configure(text=f"{self.item.title}")

    def add_scrollable_frame_with_buttons_for_persons(self, parent, items, row, column):
        scrollable_frame = ctk.CTkScrollableFrame(parent, orientation="horizontal", width=500, height=30)
        scrollable_frame.grid(row=row, column=column, sticky="w", columnspan=2)
        for i, item in enumerate(items):
            button = ctk.CTkButton(scrollable_frame, text=item.name,
                                   command=lambda person=item: DetailsPersonFrame(person, self.settings))
            button.grid(row=row, column=i, sticky="w", padx=2, pady=2)


class DetailsPersonFrame(DetailFrame):
    def configure_details(self):
        title_frame = ctk.CTkFrame(self.details_frame)
        title_frame.grid(row=0, column=0, sticky="w")

        self.title_label = self.add_label(title_frame, text=self.item.name, row=0, column=0, sticky="w",
                                          fg_color="gray30", corner_radius=9, font=("Helvetica", 24, "bold"),
                                          cursor="hand1")

        self.add_label(self.details_frame, text="Bibliography:", row=1, column=0, sticky="w", fg_color="gray",
                       font=("Helvetica", 16, "bold"), corner_radius=6)
        self.add_textbox(self.details_frame, text=self.item.bibliography, row=2, column=0, rowspan=2)

        self.add_label(self.details_frame, text="Birthday:", row=4, column=0, sticky="w", fg_color="gray",
                       font=("Helvetica", 16, "bold"), corner_radius=6)
        self.add_label(self.details_frame, text=self.item.birthday, row=5, column=0, sticky="w", fg_color="gray")

        self.configure_films()

    def configure_films(self):
        films = self.item.get_films()
        self.add_label(self.details_frame, text="Films:", row=6, column=0, sticky="w",
                       fg_color="gray", font=("Helvetica", 16, "bold"), corner_radius=6)
        if len(films) == 0:
            self.add_label(self.details_frame, text="No films available", row=7, column=0, sticky="w",
                           fg_color="gray")
            return
        self.add_scrollable_frame_with_buttons_for_films(self.details_frame, films, row=7, column=0)

    def add_scrollable_frame_with_buttons_for_films(self, parent, items, row, column):
        scrollable_frame = ctk.CTkScrollableFrame(parent, orientation="horizontal", width=200, height=30)
        scrollable_frame.grid(row=row, column=column, sticky="w", columnspan=2)
        for i, item in enumerate(items):
            button = ctk.CTkButton(scrollable_frame, text=item.title,
                                   command=lambda film=item: DetailsFilmFrame(film, self.settings))
            button.grid(row=row, column=i, sticky="w", padx=2, pady=2)
