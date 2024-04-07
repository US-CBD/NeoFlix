import customtkinter as ctk
from PIL import Image, ImageTk

class DetailsFilmFrame(ctk.CTkFrame):
    def __init__(self, parent, film, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.film = film
        self.initialize()

    def initialize(self):
        self.parent.geometry("800x600")
        self.parent.resizable(False, False)

        self.image_frame = ctk.CTkFrame(self)
        self.image_frame.grid(row=0, column=0)

        self.details_frame = ctk.CTkFrame(self)
        self.details_frame.grid(row=0, column=1)

        self.configure_widgets()

    def configure_widgets(self):
        self.configure_image()
        self.configure_details()

    def configure_image(self):
        # Convert PIL image to CTkImage
        pil_image = Image.open(self.film.get_path())
        ctk_image = ctk.CTkImage(pil_image)
        image_label = ctk.CTkLabel(self.image_frame, image=ctk_image)
        image_label.grid(row=0, column=0)

    def configure_details(self):
        self.configure_row(self.details_frame, 0, None, data_text=self.film.title, is_title=True)
        self.configure_row(self.details_frame, 1, "Genres: ", ", ".join(self.film.genres))
        self.configure_row(self.details_frame, 2, "Director: ", ", ".join(self.film.directors))
        self.configure_row(self.details_frame, 3, "Actors: ", ", ".join(self.film.actors))
        self.configure_row(self.details_frame, 4, "Description: ", self.film.description, is_textbox=True)

    def configure_row(self, parent, row, label_text, data_text, is_textbox=False, is_color=False, is_title=False):
        if label_text is not None:
            label = ctk.CTkLabel(parent, text=label_text, fg_color="gray")
            label.grid(row=row, column=0)

        if not is_textbox:
            data_label = ctk.CTkLabel(parent, text=data_text, fg_color="gray")
            data_label.grid(row=row + 1, column=0)
        elif not is_color:
            textbox = ctk.CTkTextbox(parent, fg_color=self.get_color(self.film.vote_average), corner_radius=6)
            textbox.insert("1.0", data_text)
            textbox.grid(row=row, column=1)
        elif is_title:
            title = ctk.CTkLabel(parent, text=data_text, fg_color="gray30", corner_radius=9)
            title.grid(row=row, column=0)
        else:
            textbox = ctk.CTkTextbox(parent, fg_color="gray", corner_radius=6)
            textbox.insert("1.0", data_text)
            textbox.grid(row=row + 1, column=0, columnspan=2)

    def get_color(self, rating):
        if rating >= 7.5:
            return "green"
        elif rating >= 5:
            return "yellow"
        else:
            return "red"

