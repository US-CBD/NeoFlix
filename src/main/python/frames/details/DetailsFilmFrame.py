import customtkinter as ctk
from PIL import Image


class DetailsFilmFrame(ctk.CTkFrame):
    def __init__(self, parent, film, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.film = film
        self.initialize()

    def initialize(self):
        self.parent.geometry("800x600")
        self.parent.resizable(False, False)
        self.parent.pack_propagate(True)

        self.image_frame = ctk.CTkFrame(self)
        self.image_frame.pack(side="left",fill="both", expand=True)

        self.details_frame = ctk.CTkFrame(self)
        self.details_frame.pack(fill="both", expand=True)

        self.configure_widgets()

    def configure_widgets(self):
        self.configure_image()
        self.configure_details()

    def configure_image(self):
        # Convert PIL image to CTkImage
        pil_image = Image.open(self.film.get_path())
        ctk_image = ctk.CTkImage(pil_image, size=(200, 400))
        image_label = ctk.CTkLabel(self.image_frame, image=ctk_image, width=200, height=400, corner_radius=6)
        image_label.grid(row=0, column=0)

    def configure_details(self):

        title = ctk.CTkLabel(self.details_frame, text=self.film.title, fg_color="gray30", corner_radius=9)
        title.grid(row=0, column=0, sticky="nsew")

        vote = ctk.CTkLabel(self.details_frame, text=self.film.vote_average, fg_color=self.get_color(self.film.vote_average))
        vote.grid(row=0, column=1, sticky="nsew")

        genres = ctk.CTkLabel(self.details_frame, text="Genres: ", fg_color="gray")
        genres.grid(row=1, column=0, sticky="nsew")

        for i, genre in enumerate(self.film.get_genres()):
            genres = ctk.CTkLabel(self.details_frame, text=genre, fg_color="gray")
            genres.grid(row=2, column=i, sticky="nsew")

        directors = ctk.CTkLabel(self.details_frame, text="Directors: ", fg_color="gray")
        directors.grid(row=3, column=0, sticky="nsew")

        for i, director in enumerate(self.film.get_directors()):
            director = ctk.CTkLabel(self.details_frame, text=director.name, fg_color="gray")
            director.grid(row=4, column=i, sticky="nsew")

        actors = ctk.CTkLabel(self.details_frame, text="Actors: ", fg_color="gray")
        actors.grid(row=5, column=0, sticky="nsew")

        for i, actor in enumerate(self.film.get_actors()):
            actor = ctk.CTkLabel(self.details_frame, text=actor.name, fg_color="gray")
            actor.grid(row=6, column=i, sticky="nsew")

        description = ctk.CTkLabel(self.details_frame, text="Description: ", fg_color="gray")
        description.grid(row=7, column=0, sticky="nsew")

        description_text = ctk.CTkTextbox(self.details_frame, fg_color="gray", corner_radius=6)
        description_text.insert("1.0", self.film.description)
        description_text.grid(row=8, column=0, columnspan=2, sticky="nsew")

    def configure_row(self, parent, row, column, label_text, data_text, is_textbox=False, is_color=False, is_title=False):
        if label_text is not None:
            label = ctk.CTkLabel(parent, text=label_text, fg_color="gray")
            label.grid(row=row, column=column, sticky="nsew")
        print(data_text)
        if not is_textbox:
            print(data_text)
            data_label = ctk.CTkLabel(parent, text=data_text, fg_color="gray")
            data_label.grid(row=row + 1, column=column, sticky="nsew")
        elif not is_color:
            textbox = ctk.CTkTextbox(parent, fg_color=self.get_color(self.film.vote_average), corner_radius=6)
            textbox.insert("1.0", data_text)
            textbox.grid(row=row, column=column, sticky="nsew")
        elif is_title:
            title = ctk.CTkLabel(parent, text=data_text, fg_color="gray30", corner_radius=9)
            title.grid(row=row, column=column, sticky="nsew")
        else:
            textbox = ctk.CTkTextbox(parent, fg_color="gray", corner_radius=6)
            textbox.insert("1.0", data_text)
            textbox.grid(row=row + 1, column=column, columnspan=2, sticky="nsew")

    def get_color(self, rating):
        if rating >= 7.5:
            return "green"
        elif rating >= 5:
            return "yellow"
        else:
            return "red"

