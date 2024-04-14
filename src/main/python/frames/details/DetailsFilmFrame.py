from tkinter.messagebox import showinfo

import customtkinter as ctk
from PIL import Image

from src.main.python.models.models import Opinion


class DetailsFilmFrame(ctk.CTkFrame):
    def __init__(self, parent, film, settings, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.film = film
        self.settings = settings
        self.initialize()

    def initialize(self):
        self.parent.geometry("800x600")
        self.parent.resizable(False, True)
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
        title_frame = ctk.CTkFrame(self.details_frame)
        title_frame.grid(row=0, column=0, sticky="w")

        self.title_label = ctk.CTkLabel(title_frame, text=self.film.title, fg_color="gray30", corner_radius=9,
                                        cursor="hand1")
        self.title_label.grid(row=0, column=0, sticky="w")
        self.title_label.bind("<Button-1>", self.mark_as_favorite)

        self.add_label(self.details_frame, text=self.film.vote_average, row=0, column=1, sticky="w",
                       fg_color=self.get_color(self.film.vote_average), text_color="black")
        if len(self.film.get_genres()) >= 1:
            self.add_label(self.details_frame, text="Genres: ", row=1, column=0, sticky="w", fg_color="gray")
            self.add_scrollable_frame_with_buttons(self.details_frame, self.film.get_genres(), row=2, column=0)
        if len(self.film.get_directors()) >= 1:
            self.add_label(self.details_frame, text="Directors: ", row=3, column=0, sticky="w", fg_color="gray")
            self.add_scrollable_frame_with_buttons(self.details_frame,
                                                   [director.name for director in self.film.get_directors()], row=4,
                                                   column=0)

            self.add_label(self.details_frame, text="Actors: ", row=5, column=0, sticky="w", fg_color="gray")
            self.add_scrollable_frame_with_buttons(self.details_frame, [actor.name for actor in self.film.get_actors()],
                                                   row=6, column=0)
        self.add_label(self.details_frame, text="Description: ", row=7, column=0, sticky="w", fg_color="gray")
        self.add_textbox(self.details_frame, text=self.film.description, row=8, column=0, rowspan=2)

        self.opinion_buttom = ctk.CTkButton(self.details_frame, text="👍 Give your opinion", fg_color="gray", 
                                            command=lambda: self.open_opinion_frame(self.film))
        self.opinion_buttom.grid(row=10, column=0, sticky="w", pady=(10, 0))

        #Mostrar opiniones 

        if len(self.film.get_opinions()) >= 1:
            
            self.add_label(self.details_frame, text="Opinions: ", row=11, column=0, sticky="w", fg_color="gray")
            for i, opinion in enumerate(self.film.get_opinions()):
                print(opinion.text)
                opinion_text = opinion.__str__()
                self.add_label(self.details_frame, text=opinion_text, row=12+i, column=0, sticky="w", fg_color="gray")

        # Add favorite button
        self.favorite_button = ctk.CTkButton(title_frame, text="❤️ Add to Favorites", fg_color="gray",
                                             command=self.mark_as_favorite)
        self.favorite_button.grid(row=0, column=1, sticky="w", pady=(10, 0))

    def add_label(self, parent, text, row, column, sticky, fg_color=None, text_color=None, corner_radius=None):
        label = ctk.CTkLabel(parent, text=text, fg_color=fg_color, text_color=text_color, corner_radius=corner_radius)
        label.grid(row=row, column=column, sticky=sticky, padx=5, pady=5)

    def open_opinion_frame(self, film):
        opinion_window = ctk.CTkToplevel(self.parent)

        opinion_label = ctk.CTkLabel(opinion_window, text="Give your opinion", fg_color="gray30", corner_radius=6)
        opinion_label.pack()

        opinion_textbox = ctk.CTkTextbox(opinion_window, fg_color="gray", corner_radius=6)
        opinion_textbox.pack(padx=5, pady=5)

        opinion_rating_label = ctk.CTkLabel(opinion_window, text="Rating (0-10)", fg_color="gray", corner_radius=6)
        opinion_rating_label.pack(pady=5)

        opinion_rating = ctk.CTkTextbox(opinion_window, fg_color="gray", corner_radius=6)
        opinion_rating.pack(padx=5, pady=5)

        submit_button = ctk.CTkButton(opinion_window, text="Submit", fg_color="gray", corner_radius=6,
                                    command=lambda: self.submit_opinion(film, opinion_textbox.get("1.0", "end-1c"), opinion_rating.get("1.0", "end-1c")))
                                    
        submit_button.pack(pady=5)

    def submit_opinion(self, film, opinion, rating):
        opinon_object = Opinion(film=film, user=self.settings.user, text=opinion, rating=rating)
        opinon_object.save()
        self.film.add_opinion(opinion)
        showinfo("Success", "Opinion added successfully")
    


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
            self.settings.user.remove_favorite_film(self.film)
            showinfo("Success", f"{self.film.title} removed from favorites")
        else:
            self.settings.user.add_favorite_film(self.film)
            showinfo("Success", f"{self.film.title} added to favorites")

        # Actualizar el texto del botón de favoritos
        self.update_favorite_button_text()

    def update_favorite_button_text(self):
        if self.settings.user.state_film(self.film):
            self.favorite_button.configure(text="💔 Remove from Favorites")
        else:
            self.favorite_button.configure(text="❤️ Add to Favorites")





